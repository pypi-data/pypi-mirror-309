from pymarc import MARCReader, Record
import argparse
from .mzk_client import AlephMzkClient
from .datatypes import AlephField
from .oai import AlephOAISession
from .x import AlephXSession


ALEPH_HOST = "https://aleph.mzk.cz"


def pretty_print_marc_format(record: Record):
    formatted_record = []

    for field in record.get_fields():
        if field.is_control_field():
            formatted_record.append(f"{field.tag} CTL |  {field.data}")
        else:
            subfields = " ".join(
                [f"|{subfield.code} {subfield.value}" for subfield in field]
            )
            formatted_record.append(
                f"{field.tag} {field.indicator1} {field.indicator2} "
                f"{subfields}"
            )

    return "\n".join(formatted_record)


def write_pretty_printed_marcs(record, output_file):
    with open(output_file, "w") as file:
        formatted_record = pretty_print_marc_format(record)
        file.write(formatted_record + "\n\n")


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", help="MARC file to parse and print")
    argparser.add_argument(
        "--field",
        type=AlephField,
        default=AlephField.Sysno,
        help="Aleph field to search for",
    )
    argparser.add_argument(
        "--value",
        help="Value to search for in the Aleph based on the Aleph field",
    )
    argparser.add_argument(
        "--find-by-prefix",
        help="Find records by prefix in the Aleph based on the Aleph field",
    )
    argparser.add_argument(
        "--base",
        help="Base to search in the Aleph based on the Aleph field",
        default="MZK01",
    )
    argparser.add_argument(
        "--output", help="Output file to print the parsed record to"
    )

    args = argparser.parse_args()

    if args.file is None and args.value is None:
        argparser.print_help()
        exit(0)

    client = AlephMzkClient(
        AlephOAISession(ALEPH_HOST), AlephXSession(ALEPH_HOST)
    )

    if args.find_by_prefix is not None:
        for sysno in client.find_all_sysnos(
            args.base, args.field, args.find_by_prefix
        ):
            print(sysno)
        exit(0)

    record = (
        [r for r in MARCReader(open(args.file, "rb"))][0]
        if args.file
        else client.search_for_record(args.field, args.value)[0]
    )

    if record is None:
        print("Record not found")
    elif args.output is not None:
        write_pretty_printed_marcs(record.record, args.output)
    else:
        print(pretty_print_marc_format(record.record))


if __name__ == "__main__":
    main()
