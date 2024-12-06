from typing import List, Optional
from urllib.parse import quote
from pymarc import Field, Record
from ..datatypes import IssuanceType


DEFAULT_DOCUMENT_LANGUAGE = "cze"
CAN_NOT_BE_DIGITIZED_FLAG = "nelze digi"


def encode(text: Optional[str]) -> Optional[str]:
    return quote(text.encode("utf-8")) if text is not None else None


class AlephMzkIssue:
    def __init__(self, field: Field):
        self.field = field

    @staticmethod
    def from_record(record: Record) -> List["AlephMzkIssue"]:
        return [AlephMzkIssue(field) for field in record.get_fields("996")]

    @staticmethod
    def specific_issue_from_record(
        record: Record, barcode: Optional[str], volume: Optional[str]
    ) -> Optional["AlephMzkIssue"]:
        for field in record.get_fields("996"):
            issue = AlephMzkIssue(field)
            if barcode is None and volume == issue.volume:
                return issue
            if barcode == issue.barcode:
                return issue
        return None

    def get_code_value(self, code) -> Optional[str]:
        values = self.field.get_subfields(code)
        return values[0] if values else None

    @property
    def issuance_type(self) -> IssuanceType:
        if self.field.get_subfields("i"):
            return IssuanceType.Bundle
        if self.field.get_subfields("y"):
            return IssuanceType.Volume
        return IssuanceType.Unit

    @property
    def barcode(self) -> Optional[str]:
        return self.get_code_value("b")

    @property
    def signature(self) -> Optional[str]:
        return self.get_code_value("c")

    @property
    def volume(self) -> Optional[str]:
        return (
            self.get_code_value("d")
            if self.issuance_type == IssuanceType.Unit
            else self.get_code_value("v")
        )

    @property
    def volume_year(self) -> Optional[str]:
        return self.get_code_value("y")

    @property
    def bundle(self) -> Optional[str]:
        return self.get_code_value("i")

    @property
    def can_digitize(self) -> bool:
        p = self.get_code_value("p")
        return CAN_NOT_BE_DIGITIZED_FLAG not in p if p else True

    def __str__(self):
        properties = [
            f"issuance_type: {self.issuance_type}",
            f"barcode: {self.barcode}",
            f"signature: {self.signature}",
            f"volume: {self.volume}",
            f"volume_year: {self.volume_year}",
            f"bundle: {self.bundle}",
            f"can_digitize: {self.can_digitize}",
        ]
        return "\n".join(properties)
