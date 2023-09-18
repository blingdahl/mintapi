import sys
import configargparse
import json
import csv
import re


def parse_arguments(args):
    ARGUMENTS = [
        (
            ("filepath_in",),
            {
                "nargs": "?",
                "default": None,
                "help": "The filename to read from.",
            },
        ),
        (
            ("filepath_out",),
            {
                "nargs": "?",
                "default": None,
                "help": "The filename to write to.",
            },
        ),
    ]

    # Parse command-line arguments {{{
    cmdline = configargparse.ArgumentParser()

    for argument_commands, argument_options in ARGUMENTS:
        cmdline.add_argument(*argument_commands, **argument_options)

    return cmdline.parse_args(args)

# Date	Description	Original Description	Amount	Transaction Type	Category	Account Name	Labels	Notes

def main():
    parsed_args = parse_arguments(sys.argv[1:])
    filepath_in = parsed_args.filepath_in
    filepath_out = parsed_args.filepath_out
    input = json.load(open(filepath_in))
    # Convert json to csv
    csvwriter = csv.writer(open(filepath_out, 'w'), delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["Date", "Description", "Original Description", "Amount", "Transaction Type", "Category", "Account Name", "Labels", "Notes"])

    for transaction in input:
        date_parts = transaction["date"].split("-")
        date = f'{date_parts[1]}/{date_parts[2]}/{date_parts[0]}'
        description = re.sub(r'  +', ' ', transaction["description"])
        original_description = description
        # Backward-compatibility with manual export
        amount = abs(transaction["amount"])
        transaction_type = transaction["transactionType"].lower()
        category = transaction["category"]["name"]
        account_name = transaction["accountRef"]["name"]
        labels = ""
        if "tagData" in transaction and "tags" in transaction["tagData"]:
            labels = ", ".join([tag["name"] for tag in transaction["tagData"]["tags"]])
        notes = ""
        csvwriter.writerow(
            [
                date,
                description,
                description,
                amount,
                transaction_type,
                category,
                account_name,
                labels,
                notes,
            ]
        )
    

if __name__ == "__main__":
    main()
