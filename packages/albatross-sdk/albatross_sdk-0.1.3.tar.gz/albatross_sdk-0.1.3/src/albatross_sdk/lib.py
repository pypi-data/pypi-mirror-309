import csv
import secrets
from typing import Any, Dict, List, NotRequired, Optional, Tuple, TypedDict

import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from jose import jwt as jose_jwt


class OptionSet(TypedDict):
    uuid: str
    name: str


Unit = OptionSet


class UnitListResponse(TypedDict):
    appList: List[Unit]


class Event(TypedDict):
    units: Dict[str, str]  # this must be {unit_uuid: unit_value}
    value: NotRequired[str]
    eventType: str  # this must be a uuid
    payload: NotRequired[Dict[str, Any]]
    timestamp: NotRequired[str]


class CategoryData(TypedDict):
    unit: str  # this must be {unit_uuid: unit_value}
    values: Dict[str, Any]


class CategoryResponse(TypedDict):
    ids: List[int]
    cardinality: int


class Feature(TypedDict):
    uuid: str
    name: str
    config: Any


class EventReponseBatch(TypedDict):
    cardinality: int
    uuids: List[str]


class EventTypeListResponse(TypedDict):
    uuid: str
    name: str


def option_set_to_dict(option_set: List[OptionSet]) -> Dict[str, str]:
    r: Dict[str, str] = {}

    for row in option_set:
        r[row["name"]] = row["uuid"]

    return r


class AlbatrossSDK:
    instance: str
    private_key: Optional[PrivateKeyTypes]
    base_url: str
    superadmin_key: Optional[str]

    def __init__(
        self,
        instance: str,
        private_key: Optional[PrivateKeyTypes] = None,
        base_url: str = "https://app.usealbatross.ai/api",
        superadmin_key: Optional[str] = None,
    ):
        self.instance = instance
        self.private_key = private_key
        self.base_url = base_url
        self.superadmin_key = superadmin_key
        self.is_superadmin = superadmin_key is not None

    @staticmethod
    def load_private_key(private_key_path) -> PrivateKeyTypes:
        with open(private_key_path, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None)

    @staticmethod
    def generate_nonce(length: int = 21) -> str:
        return secrets.token_hex(length)

    @staticmethod
    def handle_not_ok(response: requests.models.Response):
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        raise Exception("could not make request successfully")

    def get_jwt(self, nonce: str, instance: str) -> str:
        if not self.private_key:
            raise ValueError("Private key not loaded. Call load_private_key() first.")

        claims = {
            "instance": instance,
            "nonce": nonce,
        }

        return jose_jwt.encode(claims, self.private_key, algorithm="ES256")  # type: ignore

    def get_api_version(self):
        res = requests.get(f"{self.base_url}/version")
        return res.json()

    def prepare_request(self) -> Tuple[Dict[str, str], str]:
        nonce = self.generate_nonce()

        if self.is_superadmin:
            headers = {
                "Content-Type": "application/json",
                "x-superadmin-key": self.superadmin_key,
                "x-instance-id": self.instance,
            }

            return headers, nonce

        token = self.get_jwt(nonce, self.instance)
        headers = {"Content-Type": "application/json", "Authorization": token}
        return headers, nonce

    def put_event(self, payload: Event):
        url = f"{self.base_url}/event"

        headers, nonce = self.prepare_request()
        response = requests.put(url, json={**payload, "nonce": nonce}, headers=headers)
        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res["uuid"]

    def put_events(self, payload: List[Event]) -> EventReponseBatch:
        url = f"{self.base_url}/event/batch"

        headers, nonce = self.prepare_request()
        response = requests.put(
            url, json={"events": payload, "nonce": nonce}, headers=headers
        )
        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res

    def put_categories_csv(self, csv_file_path: str, unit: str):
        # Initialize an empty list to hold EventCategory or dictionary objects
        category_data = []

        # Open and read the CSV file
        with open(csv_file_path, "r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                category_row = {"unit": unit, "values": row}
                category_data.append(category_row)

        return self.put_categories(category_data)

    def put_categories(self, cat_data: List[CategoryData]) -> CategoryResponse:
        url = f"{self.base_url}/category"
        headers, nonce = self.prepare_request()

        response = requests.put(
            url, json={"data": cat_data, "nonce": nonce}, headers=headers
        )

        if not response.ok:
            raise Exception("request was not succesful", response.text)

        res = response.json()

        return res

    def list_unit(self) -> UnitListResponse:
        url = f"{self.base_url}/unit/list"

        headers, _ = self.prepare_request()
        response = requests.post(url, json={"uuid": self.instance}, headers=headers)
        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res

    def list_event_type(self) -> List[EventTypeListResponse]:
        url = f"{self.base_url}/event-type/list"

        headers, _ = self.prepare_request()
        response = requests.post(url, json={"uuid": self.instance}, headers=headers)
        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res

    def list_feature(self) -> List[Any]:
        url = f"{self.base_url}/feature-catalog/list"
        headers, _ = self.prepare_request()
        response = requests.post(
            url, json={"instance": {"uuid": self.instance}}, headers=headers
        )
        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res

    def prediction(
        self,
        model_uuid: str,
        context: Dict[str, str],
        actions: List[Dict[str, str]],
    ):
        headers, _ = self.prepare_request()
        url = f"{self.base_url}/prediction/ranking"

        response = requests.post(
            url,
            headers=headers,
            json={
                "modelUuid": model_uuid,
                "context": context,
                "actions": actions,
            },
        )

        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res

    def feedback(self, model_uuid: str, prediction_uuid: str, feedback):
        headers, _ = self.prepare_request()
        url = f"{self.base_url}/feedback"

        payload = {
            "modelUuid": model_uuid,
            "predictionUuid": prediction_uuid,
            "value": feedback,
        }

        response = requests.post(url, headers=headers, json=payload)

        if not response.ok:
            self.handle_not_ok(response)

        res = response.json()

        return res
