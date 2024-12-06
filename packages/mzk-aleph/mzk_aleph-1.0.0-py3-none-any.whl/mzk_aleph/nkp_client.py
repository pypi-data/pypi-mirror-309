from pymarc import Record
from typing import Optional, List
from .datatypes import CatalogBase, LibrarySigla
from .exceptions import MultipleRecordsFoundError
from .nkp_z3950_session import NkpZ3950Session


class AlephNkpClient:
    def __init__(self, nkp_z3950_session: NkpZ3950Session, base: str):
        self._z3950_session = nkp_z3950_session
        self._base = base

    def get_record(self, doc_number: str) -> Optional[Record]:
        records = self._z3950_session.search(
            self._base, f"@attr 1=1032 {doc_number}"
        )

        if len(records) > 1:
            raise MultipleRecordsFoundError()

        return records[0] if len(records) == 1 else None

    def find_record_by_mzk_control_number(
        self, mzk_control_number: str
    ) -> Optional[Record]:
        records = self._z3950_session.search(
            self._base,
            f"@attr 1=12 {LibrarySigla.MZK.value}+{mzk_control_number}",
        )

        if len(records) > 1:
            raise MultipleRecordsFoundError()

        return records[0] if len(records) == 1 else None

    def find_by_identifiers(
        self,
        isbn: str | None = None,
        issn: str | None = None,
        cnb: str | None = None,
    ) -> List[Record]:
        if isbn is not None and issn is not None:
            raise ValueError(
                "Only one of isbn or issn can be provided, not both."
            )

        filters = []

        if isbn is not None:
            filters.append(f"@attr 1=7 {isbn}")
        if issn is not None:
            filters.append(f"@attr 1=8 {issn}")
        if cnb is not None:
            filters.append(f"@attr 1=48 {cnb}")

        if len(filters) == 0:
            return []

        query = (
            filters[0]
            if len(filters) == 1
            else f"@or {filters[0]} {filters[1]}"
        )

        return self._z3950_session.search(self._base, query)

    def parse_sysno(self, record: Record) -> str:
        return record["998"]["a"]


class AlephSkcClient(AlephNkpClient):
    def __init__(self, nkp_z3950_session: NkpZ3950Session):
        super().__init__(nkp_z3950_session, CatalogBase.SKC.value)


class AlephCnbClient(AlephNkpClient):
    def __init__(self, nkp_z3950_session: NkpZ3950Session):
        super().__init__(nkp_z3950_session, CatalogBase.CNB.value)

    def find_record_by_mzk_control_number(
        self, mzk_control_number: str
    ) -> Optional[Record]:
        raise NotImplementedError(
            "CnbClient does not support finding by mzk control number"
        )


if __name__ == "__main__":
    import time

    session = NkpZ3950Session("aleph.nkp.cz", 9991)
    skc_client = AlephSkcClient(session)
    cnb_client = AlephCnbClient(session)

    start_time = time.time()

    print(f"Timestamp: {time.time() - start_time:.4f} seconds")
    print("Searching by mzk control number in SKC:")
    print(skc_client.find_record_by_mzk_control_number("nkc20132482603"))
    print("\n")

    print(f"Timestamp: {time.time() - start_time:.4f} seconds")
    print("Searching by doc number in CNB:")
    print(cnb_client.get_record("003590887"))
    print("\n")

    print(f"Timestamp: {time.time() - start_time:.4f} seconds")
    print("Searching by identifiers in SKC:")
    print(
        skc_client.find_by_identifiers(
            isbn="978-80-242-4175-3", cnb="cnb002482603"
        )[0]
    )
    print("\n")

    print(f"Timestamp: {time.time() - start_time:.4f} seconds")
    print("Searching by identifiers in CNB:")
    print(
        cnb_client.find_by_identifiers(
            isbn="978-80-242-4175-3", cnb="cnb002482603"
        )[0]
    )
    print("\n")

    print(f"Timestamp: {time.time() - start_time:.4f} seconds")
