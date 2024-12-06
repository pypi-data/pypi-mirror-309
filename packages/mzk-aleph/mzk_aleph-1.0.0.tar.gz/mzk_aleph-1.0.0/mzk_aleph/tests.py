from unittest import skipIf, TestCase

from oai import AlephOAISession
from x import AlephXSession
from .mzk_client import AlephMzkClient
from .datatypes import (
    AlephField,
    AlephResponseStatus,
    MaterialType,
    IssuanceType,
)
from .schemas import AlephMzkIssue, Frequency


MZK_ALEPH_HOST = "https://aleph.mzk.cz"


def skipIfXApiNotAvailable(test_func):
    return skipIf(
        not AlephXSession(MZK_ALEPH_HOST).is_available(),
        "Aleph find endpoint is not available",
    )(test_func)


class TestAlephCatalog(TestCase):
    def setUp(self):
        self.client = AlephMzkClient(
            AlephOAISession(MZK_ALEPH_HOST), AlephXSession(MZK_ALEPH_HOST)
        )

    def test_search_for_record(self):
        # Arrange
        field = AlephField.Sysno
        # value="MZK01-000229421",
        value = "MZK01-000724903"
        # value="MZK01-001884485",

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertIsNotNone(aleph_record)
        self.assertIsNotNone(status)

    def test_get_using_dashless_prefixed_sysno(self):
        # Arrange
        field = AlephField.Sysno
        value = "mzk01000724903"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-000724903")

    @skipIfXApiNotAvailable
    def test_get_using_sysno_without_prefix(self):
        # Arrange
        field = AlephField.Sysno
        value = "000724903"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-000724903")

    @skipIfXApiNotAvailable
    def test_get_using_sysno_without_prefix_and_with_omitted_zeros(self):
        # Arrange
        field = AlephField.Sysno
        value = "724903"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-000724903")

    def test_get_one_edition_document(self):
        # Arrange
        field = AlephField.Sysno
        value = "MZK01-000724903"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)

        self.assertEqual(aleph_record.sysno, "MZK01-000724903")
        self.assertEqual(aleph_record.material_type, MaterialType.Book)
        self.assertEqual(aleph_record.size, "19 cm")
        self.assertEqual(aleph_record.signature, "1-0022.371")
        self.assertEqual(aleph_record.cnb, "cnb002147995")
        self.assertEqual(aleph_record.isxn, None)
        self.assertEqual(aleph_record.frequencies, [])
        self.assertEqual(aleph_record.publishing_year, "1899")

        issues = AlephMzkIssue.from_record(aleph_record.record)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].signature, "1-0022.371")
        self.assertEqual(issues[0].barcode, "2619213824")
        self.assertEqual(issues[0].issuance_type, IssuanceType.Unit)
        self.assertEqual(issues[0].volume, None)
        self.assertEqual(issues[0].volume_year, None)
        self.assertEqual(issues[0].bundle, None)
        self.assertEqual(aleph_record.parse_page_count(issues[0].volume), 755)

    def test_get_multiple_issues_document(self):
        # Arrange
        field = AlephField.Sysno
        value = "MZK01-001273598"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)

        self.assertEqual(aleph_record.sysno, "MZK01-001273598")
        self.assertEqual(
            aleph_record.material_type, MaterialType.ContinuingResource
        )
        self.assertEqual(aleph_record.size, "12 cm")
        self.assertEqual(aleph_record.signature, "CDR-1298.303")
        self.assertEqual(aleph_record.cnb, None)
        self.assertEqual(aleph_record.isxn, None)
        self.assertEqual(
            aleph_record.frequencies,
            [
                Frequency("3x ročně", "2016-"),
                Frequency("2x ročně,", "2015"),
                Frequency("1x ročně,", "2012-2014"),
            ],
        )
        self.assertEqual(aleph_record.publishing_year, "2012-")

        issues = AlephMzkIssue.from_record(aleph_record.record)
        self.assertEqual(len(issues), 14)
        self.assertEqual(issues[0].signature, "CDR-1298.303")
        self.assertEqual(issues[0].barcode, "2610534453")
        self.assertEqual(issues[0].issuance_type, IssuanceType.Bundle)
        self.assertEqual(issues[0].volume, "2012")
        self.assertEqual(issues[0].volume_year, "2012")
        self.assertEqual(issues[0].bundle, "1")
        self.assertIsNone(aleph_record.parse_page_count(issues[0].volume))

    @skipIfXApiNotAvailable
    def test_parse_can_not_be_digitized(self):
        # Arrange
        field = AlephField.Signature
        value = "4-1144.857"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)

        issues = AlephMzkIssue.from_record(aleph_record.record)
        self.assertFalse(issues[0].can_digitize)

    @skipIfXApiNotAvailable
    def test_find_document_by_barcode(self):
        # Arrange
        field = AlephField.Barcode
        value = "2610629074"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-001449649")

    @skipIfXApiNotAvailable
    def test_find_document_by_signature(self):
        # Arrange
        field = AlephField.Signature
        value = "OB3-0114.497"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-001091763")

    @skipIfXApiNotAvailable
    def test_find_document_by_signature_2(self):
        # Arrange
        field = AlephField.Signature
        value = "Bf3-0289.114"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-001091763")

    def test_parse_frequencies(self):
        # Arrange
        field = AlephField.Sysno
        value = "MZK01-000230291"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)
        self.assertEqual(aleph_record.sysno, "MZK01-000230291")

    def test_parse_pages_count(self):
        from schemas.parsers import parse_page_count

        self.assertEqual(parse_page_count("66 s."), 66)
        self.assertEqual(parse_page_count("17 s. :"), 17)
        self.assertEqual(parse_page_count("86 - [II] s. "), 86)
        self.assertEqual(parse_page_count("[I]-16-[III] s. ;"), 16)
        self.assertEqual(parse_page_count("41, [i] s. ;"), 41)
        self.assertEqual(parse_page_count("22, [3] s. ;"), 22)
        self.assertEqual(parse_page_count("55, 1 s., 3 l. ;"), 55)
        self.assertEqual(parse_page_count("67, [2] s. :"), 67)
        self.assertEqual(parse_page_count("27 stran :"), 27)
        self.assertEqual(parse_page_count("[52] s. :"), 52)
        self.assertEqual(parse_page_count("14, 104 s."), 14)
        self.assertEqual(parse_page_count("x, [196] s. :"), 196)
        self.assertEqual(parse_page_count("[35] s. :"), 35)
        self.assertEqual(parse_page_count("77 l. ;"), 77)
        self.assertEqual(parse_page_count("99 l. ;"), 99)
        self.assertEqual(
            parse_page_count("2 sv. (759, 623 s.) :", "I. díl"), 759
        )
        self.assertEqual(
            parse_page_count("2 sv. (759, 623 s.) :", "II. díl"), 623
        )
        self.assertEqual(
            parse_page_count("3 sv. (383; 358; 229 s.) ;", "1. díl"), 383
        )
        self.assertEqual(
            parse_page_count("3 sv. (383; 358; 229 s.) ;", "2. díl"), 358
        )
        self.assertEqual(
            parse_page_count("3 sv. (383; 358; 229 s.) ;", "3. díl"), 229
        )
        self.assertIsNone(parse_page_count("12 sv."))
        self.assertIsNone(parse_page_count("7 sv."))

    def test_parse_location_uri(self):
        # Arrange
        field = AlephField.Sysno
        value = "MZK01-000258273"

        # Act
        aleph_record, status = self.client.search_for_record(field, value)

        # Assert
        self.assertEqual(status, AlephResponseStatus.Success)

        self.assertEqual(
            aleph_record.location_uri,
            "http://www.digitalniknihovna.cz/mzk/uuid/"
            "uuid:21834a15-a176-11e0-8965-0050569d679d",
        )
