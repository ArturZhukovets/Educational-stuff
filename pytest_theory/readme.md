## PyTest

### Фикстура.

В pytest есть фикстура нужна, чтобы выполнять какое-то действие перед или после запуска тестов.  
Фикстура описывается в `conftest.py`. В этом примере будет описана фикстура перезатирающая каждый раз файл и записывающая в него определённые данные.  

```python
import pytest

def create_test_data(testdata: [list[str]]):
    if not isinstance(testdata, list):
        raise TypeError
    with open("data/testfile.txt", 'a') as file:
        file.writelines(testdata)
        
@pytest.fixture(autouse=True)   # `autouse` flag позволяет каждый раз запускать данную фикстуру
def clean_text_file():
    with open("data/testfile.txt", "w"):
        pass
    create_test_data(testdata=["one\n", "two\n", "three\n"])
```

> Важный момент.

Для того чтобы не вызывать одну и ту же текстуру для каждого теста, файл с нужными тестами и с нужным конфигом `conftest.py` можно вынести в отельный модуль.

***

### Mock

В тестировании мок - это концепция, позволяющая симулировать поведение внешних зависимостей в тестовой среде.  
Т.е мок применяться в ситуациях, когда необходимо воссоздать поведение какого либо сервиса, АПИ, базы данных без прямого взаимодействия с ним.  
В данном примере `web_service_test` был описан простой веб сервис, который шлёт запрос и получает ответ.  
Для тестирования данного сервиса был создан `mock request`, который возвращал ожидаемый ответ.  
Это позволяет не загружать сервис и получать статичный ответ (для проведения теста).

```python
import responses
from web_service_test.src.web_client import SomeWebClient
from datetime import datetime

@responses.activate
def test_web_client():
    valid_json_answer = {
        "lastActionTime": 1687078973,
        "timeDiff": 19371,
    }
    responses.add(
        responses.GET, "https://www.avito.ru/web/user/get-status/51005",
        json=valid_json_answer, status=200,
    )
    web_client = SomeWebClient("https://www.avito.ru")
    response = web_client.get_user_last_action_time(51005)

    last_action_time = valid_json_answer["lastActionTime"]
    time_diff = valid_json_answer["timeDiff"]

    assert response == datetime.fromtimestamp(last_action_time - time_diff)
```

В данном случае для симуляции ответа от сервиса использовалась библиотека `responses`, но также можно использовать такие пакеты как:  
> `pytest-mock`, `unittest.mock`, `mockito`

###
***
## Django tests

+ Первый экзампл показывает как тестировать url в дажнго.
Была создана апп `budget`, в которой первым делом затестил 3 эндпоинта.
В каждом тесте убеждаюсь, что резолвнутый url совпадает с ожидаемой функцией.

+ Врой экзампл о том как тестировать views.  
При тестировании views задача - протестировать каждый endpoint, что он выполняет свой функционал.
Здесь в методе setUp прописывались объекты, необходимые для тестирования views.  

```python
def setUp(self) -> None:
    self.client = Client()
    self.list_url = reverse("budget:list")
    self.detail_url = reverse("budget:detail", args=["project-test"])
    self.create_url = reverse("budget:add")
    self.project_test_obj = Project.objects.create(
        name="project-test",
        budget=1_000_000,
    )
    self.category_test_obj = Category.objects.create(
        project=self.project_test_obj,
        name="development",
    )
```

> Разница между setUp и setUpData.
> Оба этих метода - методы класса TestCase, переопределяя их можно задать первичные настройки и окружение перед:
> 1. запуском каждого теста (в случае `setUp`)
> 2. запуском сразу всех тестов (в случае `setUpData`)  
> то есть setUp вызывается и инициализирует свои данные перед каждым тестом, а классовый метод setUpData вызывается один раз  
> для всего класса.

+ В третьем примере тестируются модели. Задача протестировать все методы и проперти класса Модели.

+ Также отдельно тестируются формы. В моём примере была 2 тест кейса.  
1 - Форма валидна; 2 - Форма не валидна.


```python
class TestForms(SimpleTestCase):

    def test_expense_form_is_valid(self):
        data = {
            "title": "SomeTestTitle",
            "amount": 10_000,
            "category": "SomeTestCategory"
        }
        self.assertTrue(ExpenseForm(data=data).is_valid())

    def test_expense_form_no_data(self):
        data = {}
        self.assertFalse(ExpenseForm(data=data).is_valid())
```



