import logging
from typing import Optional, Tuple, Generator
import re
from .schemas import AlephMzkRecord
from .datatypes import AlephField, AlephResponseStatus
from .x import AlephXSession
from .oai import AlephOAISession


logger = logging.getLogger(__name__)


PAGE_SIZE = 10

SYSNO_BASES = ["MZK01", "MZK03"]
SYSNO_FORMAT_1 = r"^\d{1,9}$"
SYSNO_FORMAT_2 = r"^(?:MZK|mzk)(\d{2})-?(\d{9})$"


class AlephMzkClient:
    def __init__(self, oai_session: AlephOAISession, x_session: AlephXSession):
        self.oai_session = oai_session
        self.x_session = x_session

    def get_record(
        self, base: str, doc_number: str
    ) -> Tuple[Optional[AlephMzkRecord], AlephResponseStatus]:
        try:
            record = self.oai_session.get_record(base, doc_number)
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
            return None, AlephResponseStatus.RequestFailed

        if record is None:
            return None, AlephResponseStatus.RecordNotFound

        return (
            AlephMzkRecord(record, base=base, doc_number=doc_number),
            AlephResponseStatus.Success,
        )

    def find_record(
        self, base: str, field: AlephField, value: str
    ) -> Tuple[Optional[str], AlephResponseStatus]:
        try:
            set_number, num_records = self.x_session.search(
                base, field.value, value
            )
        except Exception as e:
            logger.warning(f"An error occurred: {e}")
            return None, AlephResponseStatus.RequestFailed

        if num_records == 0:
            return None, AlephResponseStatus.RecordNotFound
        if num_records > 1:
            return None, AlephResponseStatus.MultipleRecordsFound

        doc_number = self.x_session.list_record(set_number)

        return self.get_record(base, doc_number)

    def search_in_all_bases(
        self, field: AlephField, value: str
    ) -> Tuple[Optional[AlephMzkRecord], AlephResponseStatus]:
        for base in SYSNO_BASES:
            try:
                record, status = self.find_record(base, field, value)
                if record is not None:
                    return record, status
            except Exception as e:
                logger.warning(f"An error occurred: {e}")
        return None, AlephResponseStatus.RecordNotFound

    def parse_sysno(self, sysno: str) -> Optional[str]:
        if re.match(SYSNO_FORMAT_1, sysno):
            return f"MZK01-{sysno.zfill(9)}"
        if re.match(SYSNO_FORMAT_2, sysno):
            return re.sub(SYSNO_FORMAT_2, r"MZK\1-\2", sysno).split("-")
        return None

    def search_for_record_using_sysno(
        self, sysno: str
    ) -> Tuple[Optional[AlephMzkRecord], AlephResponseStatus]:
        if re.match(SYSNO_FORMAT_1, sysno):
            return self.search_in_all_bases(AlephField.Sysno, sysno.zfill(9))

        if not re.match(SYSNO_FORMAT_2, sysno):
            return None, AlephResponseStatus.InvalidSysno

        sysno_split = re.sub(SYSNO_FORMAT_2, r"MZK\1-\2", sysno).split("-")
        base = sysno_split[0]
        doc_number = sysno_split[1]
        return (
            self.get_record(base, doc_number)
            if base in SYSNO_BASES
            else (None, AlephResponseStatus.InvalidSysnoBase)
        )

    def search_for_record(
        self, field: AlephField, value: str
    ) -> Tuple[Optional[AlephMzkRecord], AlephResponseStatus]:
        if field == AlephField.Sysno:
            return self.search_for_record_using_sysno(value)
        return self.search_in_all_bases(field, value)

    def find_all_sysnos(
        self, base: str, field: AlephField, value: str
    ) -> Generator[str, None, None]:
        set_number, num_records = self.x_session.search(
            base, field.value, value
        )

        if num_records == 0:
            return []

        for page in range(0, num_records // PAGE_SIZE + 1):
            self.x_session.list_records(set_number, page, PAGE_SIZE)
