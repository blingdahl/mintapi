import sys
import configargparse
import json
import csv
import re

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1D2NI8NGyEonv8HV7BJ19WJTw8_-zbjNcUldNONyKvfw'
RANGE_NAME = 'This Year!A:I'


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
            ("--json_creds",),
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


def maybe_float(string):
    try:
        return float(string)
    except ValueError:
        return string


def main():
    parsed_args = parse_arguments(sys.argv[1:])
    filepath_in = parsed_args.filepath_in
    
    csvreader = csv.reader(open(filepath_in), delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    values = [[]]
    for row in csvreader:
        if csvreader.line_num == 1:
            continue
        values.append([maybe_float(val) for val in row])

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                parsed_args.json_creds, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().update(body={'values' : values},
                                       spreadsheetId=SPREADSHEET_ID,
                                       range=RANGE_NAME,
                                       valueInputOption='RAW').execute()

    except HttpError as err:
        print(err)
    

if __name__ == "__main__":
    main()
