import requests
from datetime import datetime


class SomeWebClient:
    def __init__(self, url: str):
        self._url = url

    def __user_get_status(self, user_id: int) -> dict[str: int, str: int]:
        response = requests.get(f"{self._url}/web/user/get-status/{user_id}")
        if not response.ok:
            raise requests.HTTPError(f"Error. Status code - {response.status_code}")
        return response.json()

    def get_user_last_action_time(self, user_id: int | str) -> datetime:
        try:
            json_data = self.__user_get_status(user_id)
            last_action_time = json_data["lastActionTime"]
            time_diff = json_data['timeDiff']
        except requests.HTTPError as e:
            print(e)
            raise
        else:
            return datetime.fromtimestamp(last_action_time - time_diff)
