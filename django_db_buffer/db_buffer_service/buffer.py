import logging
import time
from collections import defaultdict
from multiprocessing import current_process

from typing import ContextManager, Optional

from django.db import connections, OperationalError, InterfaceError
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.base import ModelBase

logger = logging.getLogger(__name__)

ModelClassName: str
InstancesList: list[Model]
UpdateInstanceValue: tuple[Model, list[str]]

class Buffer:

    _MAX_CONNECTION_ATTEMPTS: int = 5_000
    _BUFFER_SIZE_RECORDS: int = 1

    def __init__(self, unique_id: str, records_in_buffer: int = 1):
        self._unique_id = unique_id
        self._storage: dict[ModelClassName, InstancesList or UpdateInstanceValue] = {}
        self.connection = self.__init_connection()
        self._BUFFER_SIZE_RECORDS = records_in_buffer

    def add(self, instance: Model) -> None:
        if not isinstance(instance, Model):
            raise TypeError(f"Specified `instance` argument should be a `Model` instance. Received - {type(instance)}")
        object_name: str = instance.__class__.__name__
        if object_name not in self._storage:
            self._storage[object_name] = []
        self._storage[object_name].append(instance)
        if len(self._storage[object_name]) >= self._BUFFER_SIZE_RECORDS:
            self._save(object_name, wait=False)

    def update(self, instance: Model, update_fields: Optional[list[str]] = None) -> None:
        if not isinstance(instance, Model):
            raise TypeError(f"Specified `instance` argument should be a `Model` instance. Received - {type(instance)}")
        if not instance.pk:
            raise ValueError("Specified instance should have a `pk` if you want to update it.")
        object_name = instance.__class__.__name__ + "_" + str(instance.pk)
        self._storage[object_name] = (instance, update_fields)
        self._save(object_name, False)

    def release_buffer(self) -> None:
        for model_name in list(self._storage.keys()):
            self._save(model_name, wait=True)

    def _save(self, instance_name: str, wait: bool) -> None:
        try:
            if not self.connection.connection:
                self._connect_to_database(wait=wait)
            self.__save_instance(instance_name=instance_name)

        except (OperationalError, InterfaceError):
            print("Lost connection with db... Save record in buffer")
            if self.connection.connection is not None:
                self.connection.close()
            if wait:
                self._connect_to_database(wait=wait)
                try:
                    self.__save_instance(instance_name=instance_name)
                except Exception as ex:
                    raise TimeoutError(f"Failed to save instance. {ex}")

    def __save_instance(self, instance_name: str) -> None:
        instance = self._storage[instance_name]
        if isinstance(instance, tuple) and len(instance_name.split("_")) == 2:
            instance, update_fields = instance
            instance.save(update_fields=update_fields)
        elif isinstance(instance, list):
            model = instance[0].__class__
            if not isinstance(model, ModelBase):
                raise TypeError
            model.objects.bulk_create(instance)
        del self._storage[instance_name]

    def _connect_to_database(self, wait: bool = False) -> BaseDatabaseWrapper:
        """
        Try to establish connection with DB and if it's ok - return connection.
        If flag `wait` - True: do it in cycle
        If flag `wait` - False: try to establish connection just 1 time
          and if it's unsuccessful - raise an `OperationalError` exception.
        """

        iterations = 1
        if wait:
            iterations = self._MAX_CONNECTION_ATTEMPTS

        for iteration in range(iterations):
            try:
                connection = connections['default']
                connection.ensure_connection()
                if iteration > 1:
                    logger.debug(f"Database connection established on the {iteration} attempt.")
                    logger.debug(f"All records inside the Buffer storage will be released")
                return connection

            except (OperationalError, InterfaceError) as ex:
                if wait:
                    logger.debug("Lost connection with DB. Trying to establish connection...")
                    time.sleep(10)
                else:
                    raise ex
        raise TimeoutError("Failed to establish database connection")

    def __init_connection(self) -> BaseDatabaseWrapper:
        connections.close_all()
        connection = connections['default']
        connection.ensure_connection()
        return connection

    def buffer_is_empty(self) -> bool:
        return len(self._storage) == 0

    def __enter__(self) -> ContextManager['Buffer']:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release_buffer()

########################################################################################################


def db_buffer(func):

    bufferDict: dict[str, Buffer] = defaultdict(Buffer)

    def wrap(buffer_name: str, **kwargs):
        nonlocal bufferDict
        if not buffer_name:
            raise ValueError("Specify the buffer unique name")
        ui_id = f"{buffer_name}_{current_process().pid}"
        if ui_id not in bufferDict:
            bufferDict[ui_id] = func(ui_id)
        return bufferDict[ui_id]

    return wrap


@db_buffer
def get_buffer(ui_id) -> Buffer:
    """
    This function is used to create a new or get an existing instance of a class Buffer.
    Use it to perform database operations.
    Use this function every time if needed to work with Buffer object.
    Every Buffer instance should be use ONLY inside current process.
    If you need to manipulate with Buffer in another process - use this function to create new Buffer instance!
    """
    return Buffer(ui_id)
