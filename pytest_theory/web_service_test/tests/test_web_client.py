import pytest
import requests
import responses
from datetime import datetime
from web_service_test.src.web_client import SomeWebClient


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


@responses.activate
def test_web_client_with_error():
    json_data_with_error = {
        "errors": ["Not found"]
    }
    responses.add(
        responses.GET, "https://www.avito.ru/web/user/get-status/510050000!",
        json=json_data_with_error, status=404
                  )
    with pytest.raises(requests.HTTPError):
        web_client = SomeWebClient("https://www.avito.ru")
        web_client.get_user_last_action_time("510050000!")




