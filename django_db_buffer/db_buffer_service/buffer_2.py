import time
from collections import defaultdict
from multiprocessing import current_process

from django.db import connections, OperationalError, InterfaceError
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model
from django.db.models.base import ModelBase

ModelClassName: str
InstancesList: list[Model]

class BufferFirstVerison:
    def __init__(self, unique_id: str):
        self._unique_id = unique_id
        self._add_storage: dict[ModelClassName, InstancesList] = defaultdict(list)
        self._update_storage: dict[ModelClassName, Model] = {}

        self.connection = self._connect_to_database()

    def _save_instance(self, instance: Model | list[Model], wait: bool) -> None:
        """
        :param: instance - Model instance or list of model instances
        """
        try:
            if not self.connection.connection:
                self._connect_to_database(wait=wait)
                self.release_buffer()
            if isinstance(instance, Model):
                instance.save()
            elif isinstance(instance, list):
                model = instance[0].__class__
                if not isinstance(model, ModelBase):
                    raise TypeError
                model.objects.bulk_create(instance)
            else:
                raise TypeError("Pass list of `Model` instances or just `Model` instance")
        except (OperationalError, InterfaceError) as ex:
            if self.connection.connection is not None:
                self.connection.close()   # После этого connection = None
                print("An error occurred while db connection. Write to buffer...")
            raise ex

    def add(self, instance: Model):
        try:
            self._save_instance(instance, wait=False)
        except (OperationalError, InterfaceError):
            object_name = instance.__class__.__name__
            self._add_storage[object_name].append(instance)

    def update(self, instance: Model):
        try:
            self._save_instance(instance, wait=False)
        except (OperationalError, InterfaceError):
            object_name = instance.__class__.__name__
            if self._update_storage.get(object_name):
                self._update_storage.update({object_name: instance})
            else:
                self._update_storage[object_name] = instance

    def release_buffer(self) -> None:
        _is_connected = False
        while not _is_connected:
            try:
                self.connection.ensure_connection()
                _is_connected = True
            except (OperationalError, InterfaceError):
                time.sleep(1)
        else:
            self._release()

    def _connect_to_database(self, wait: bool = False) -> BaseDatabaseWrapper:
        try:
            connection = connections['default']
            connection.ensure_connection()
            return connection
        except Exception as ex:
            print(ex)
            time.sleep(0.1)
            if wait:
                self._connect_to_database()
            raise ex

    def _release(self) -> None:
        if not self._add_storage_is_empty():
            for model_name in self._add_storage:
                self._save_instance(self._add_storage[model_name], wait=True)
            self._add_storage.clear()

        if not self._update_storage_is_empty():
            for model_name in self._update_storage:
                self._save_instance(self._update_storage[model_name], wait=True)
            self._update_storage.clear()

    def _add_storage_is_empty(self) -> bool:
        return len(self._add_storage) == 0

    def _update_storage_is_empty(self) -> bool:
        return len(self._update_storage) == 0


def db_buffer(func):

    bufferDict: dict[str, BufferFirstVerison] = defaultdict(BufferFirstVerison)

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
def get_buffer(ui_id) -> BufferFirstVerison:
    return BufferFirstVerison(ui_id)