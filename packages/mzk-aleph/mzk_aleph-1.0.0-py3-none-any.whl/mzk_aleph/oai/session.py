from lxml import etree
from pymarc import marcxml
from io import BytesIO
from requests import Session


NS_0 = {"ns0": "http://www.openarchives.org/OAI/2.0/"}
MARC_NS = {"marc": "http://www.loc.gov/MARC21/slim"}


class AlephOAISession:
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
            response = self._session.get(f"{self._host}/OAI")
            return response.status_code == 200
        except Exception:
            return False

    def get_record(self, base: str, doc_number: str):
        response = self._session.get(
            f"{self._host}/OAI",
            params={
                "verb": "GetRecord",
                "metadataPrefix": "marc21",
                "identifier": f"oai:aleph.mzk.cz:{base}-{doc_number}",
            },
        )

        if response.status_code != 200:
            response.raise_for_status()

        content = etree.fromstring(response.content)

        error = content.find(".//ns0:error", namespaces=NS_0)
        if error is not None:
            raise Exception(error.text)

        xml_marc = content.find(".//marc:record", namespaces=MARC_NS)
        if xml_marc is None:
            return None

        return marcxml.parse_xml_to_array(BytesIO(etree.tostring(xml_marc)))[0]
