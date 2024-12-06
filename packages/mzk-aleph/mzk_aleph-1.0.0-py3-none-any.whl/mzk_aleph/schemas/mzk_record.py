from pymarc import Record
from typing import List, Optional
from ..datatypes import MaterialType
from .parsers import parse_page_count, parse_material_type
from .frequency import Frequency


DEFAULT_DOCUMENT_LANGUAGE = "cze"


class AlephMzkRecord:
    def __init__(
        self,
        record: Record,
        base: str | None = None,
        doc_number: str | None = None,
        sysno: str | None = None,
    ):
        if sysno is None and (base is None or doc_number is None):
            raise ValueError(
                "Either sysno or both base and doc_number must be provided."
            )

        self.record = record
        self.base = base
        self.doc_number = doc_number
        self._sysno = sysno

    def get_values(self, tag, code, ind1=None, ind2=None):
        return [
            subfield
            for field in self.record.get_fields(tag)
            for subfield in field.get_subfields(code)
            if ind1 is None or field.indicator1 == ind1
            if ind2 is None or field.indicator2 == ind2
        ]

    def get_value(self, tag, code):
        values = self.get_values(tag, code)
        return values[0] if values else None

    @property
    def sysno(self) -> str:
        return self._sysno or f"{self.base}-{self.doc_number}"

    @property
    def control_number(self) -> Optional[str]:
        field = self.record["001"]
        return field.data if field else None

    @property
    def cnb(self) -> Optional[str]:
        return self.get_value("015", "a")

    @property
    def language(self) -> Optional[str]:
        fields = self.record.get_fields("008")
        return fields[0].data[35:38] if fields else None

    @property
    def isbn(self) -> Optional[str]:
        return self.get_value("020", "a")

    @property
    def issn(self) -> Optional[str]:
        return self.get_value("022", "a")

    @property
    def isxn(self) -> Optional[str]:
        return self.isbn if self.isbn else self.issn

    @property
    def sigla(self) -> Optional[str]:
        return self.get_value("910", "a")

    @property
    def signature(self) -> Optional[str]:
        signature = self.get_value("910", "b")
        return signature if signature else self.get_value("910", "c")

    @property
    def title(self) -> Optional[str]:
        return self.record.title

    @property
    def part_number(self) -> Optional[str]:
        return self.get_value("245", "n")

    @property
    def part_title(self) -> Optional[str]:
        return self.get_value("245", "p")

    @property
    def edition(self) -> Optional[str]:
        return self.get_value("250", "a")

    @property
    def material_type_str(self) -> Optional[str]:
        return self.get_value("990", "a")

    @property
    def material_type(self) -> MaterialType:
        return parse_material_type(self.material_type_str)

    @property
    def publishers(self) -> List[str]:
        values = self.get_values("260", "b")
        values.extend(self.get_values("264", "b", ind2="1"))
        return values

    @property
    def publishing_places(self) -> List[str]:
        values = self.get_values("260", "a")
        values.extend(self.get_values("264", "a", ind2="1"))
        return values

    @property
    def publisher(self) -> Optional[str]:
        publisher = self.record.publisher
        return publisher.strip(" ,") if publisher else None

    @property
    def publishing_place(self) -> Optional[str]:
        publishing_places = self.get_values("260", "a")
        publishing_places.extend(self.get_values("264", "a", ind2="1"))
        return publishing_places[0] if publishing_places else None

    @property
    def publishing_year(self) -> Optional[str]:
        return self.record.pubyear

    @property
    def languages(self) -> List[str]:
        languages = self.get_values("041", "a")
        return languages if languages else [DEFAULT_DOCUMENT_LANGUAGE]

    @property
    def extent(self) -> Optional[str]:
        return self.get_value("300", "a")

    @property
    def additional_physical_data(self) -> Optional[str]:
        return self.get_value("300", "b")

    @property
    def size(self) -> Optional[str]:
        return self.get_value("300", "c")

    @property
    def location_uri(self) -> Optional[str]:
        values = self.get_values("856", "u", ind1="4", ind2="1")
        return values[0] if values else None

    @property
    def frequencies(self) -> List[Frequency]:
        frequencies_list = []
        for field in self.record.get_fields("310", "321"):
            subfields = field.subfields
            i = 0
            while i < len(subfields):
                frequency = subfields[i].value
                if i + 1 < len(subfields) and subfields[i + 1].code == "b":
                    while (
                        i + 1 < len(subfields) and subfields[i + 1].code == "b"
                    ):
                        frequencies_list.append(
                            Frequency(
                                frequency=frequency,
                                date=subfields[i + 1].value,
                            )
                        )
                        i += 1
                else:
                    frequencies_list.append(Frequency(frequency=frequency))
                i += 1
        return frequencies_list

    @property
    def keywords(self) -> List[str]:
        return self.get_values("650", "a")

    def parse_page_count(self, volume: Optional[str]) -> Optional[int]:
        return parse_page_count(self.extent, volume)

    def __str__(self) -> str:
        properties = [
            f"sysno: {self.sysno}",
            f"cnb: {self.cnb}",
            f"isxn: {self.isxn}",
            f"sigla: {self.sigla}",
            f"signature: {self.signature}",
            f"title: {self.title}",
            f"part_number: {self.part_number}",
            f"part_title: {self.part_title}",
            f"edition: {self.edition}",
            f"material_type: {self.material_type}",
            f"publishers: {self.publishers}",
            f"publishing_places: {self.publishing_places}",
            f"publisher: {self.publisher}",
            f"publishing_place: {self.publishing_place}",
            f"publishing_year: {self.publishing_year}",
            f"languages: {self.languages}",
            f"extent: {self.extent}",
            f"additional_physical_data: {self.additional_physical_data}",
            f"size: {self.size}",
            f"locationUri: {self.location_uri}",
            f"frequencies: {self.frequencies}",
        ]
        return "\n".join(properties)


if __name__ == "__main__":
    from lxml import etree

    with open("/tmp/marc_response.xml", "r") as f:
        marc_response = f.read()
        content = etree.fromstring(marc_response)
        marc_xml_data = content.find(".//record").find(".//oai_marc")
        marc_xml_content = etree.tostring(marc_xml_data, encoding="utf-8")
        # record = parse_oai_marc(marc_xml_content)
        # print(record)
