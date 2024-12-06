from lxml import etree
from typing import Tuple
from requests import Session


SEARCH_OPERATION = "find"
LIST_RECORDS_OPERATION = "present"


class AlephXSession:
    def __init__(self, host: str, timeout: int = 30):
        self._host = host.strip("/")
        self._session = Session()
        self._session.timeout = timeout

    def close(self):
        if self._session:
            self._session.close()

    def __del__(self):
        self.close()

    def is_available(self) -> bool:
        try:
            response = self._session.get(f"{self._host}/X")
            return response.status_code == 200
        except Exception:
            return False

    def search(self, base: str, field: str, value: str) -> Tuple[str, int]:
        response = self._session.get(
            f"{self._host}/X",
            params={
                "op": SEARCH_OPERATION,
                "base": base,
                "code": field,
                "request": value,
            },
        )

        if response.status_code != 200:
            response.raise_for_status()

        content = etree.fromstring(response.content)

        session_id = content.find(".//session-id")

        if session_id is None:
            h1 = content.find(".//h1")
            if h1 is not None:
                raise Exception(h1.text)
            raise Exception("Unexpected response")

        self._session.params["session_id"] = session_id.text

        return content.find(".//set_number").text, int(
            content.find(".//no_records").text
        )

    def list_record(self, set_number: str):
        response = self._session.get(
            f"{self._host}/X",
            params={
                "op": LIST_RECORDS_OPERATION,
                "set_number": set_number,
                "set_entry": "1",
            },
        )

        if response.status_code != 200:
            response.raise_for_status()

        content = etree.fromstring(response.content)

        self._session.params["session_id"] = content.find(".//session-id").text

        return content.find(".//doc_number").text

    def list_records(self, set_number: str, page: int, size: int):
        response = self._session.get(
            f"{self._host}/X",
            params={
                "op": LIST_RECORDS_OPERATION,
                "set_number": set_number,
                "set_entry": f"{page * size + 1}-{page * size + size}",
            },
        )

        if response.status_code != 200:
            response.raise_for_status()

        content = etree.fromstring(response.content)

        self._session.params["session_id"] = content.find(".//session-id").text

        for doc_number in content.findall(".//doc_number"):
            yield doc_number.text
