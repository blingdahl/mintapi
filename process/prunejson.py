import sys
import configargparse
import json


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
        (
            ("--min_date",),
            {
                "nargs": "?",
                "default": None,
                "help": "Minimum date.",
            },
        ),
    ]

    # Parse command-line arguments {{{
    cmdline = configargparse.ArgumentParser()

    for argument_commands, argument_options in ARGUMENTS:
        cmdline.add_argument(*argument_commands, **argument_options)

    return cmdline.parse_args(args)

def main():
    parsed_args = parse_arguments(sys.argv[1:])
    filepath_in = parsed_args.filepath_in
    filepath_out = parsed_args.filepath_out
    print(filepath_in)
    input = json.load(open(filepath_in))
    print(input[0])
    output=[]
    for transaction in input:
        if transaction["date"] >= parsed_args.min_date:
            output.append(transaction)
    json.dump(output, open(filepath_out, "w"), indent=4)
    

if __name__ == "__main__":
    main()
