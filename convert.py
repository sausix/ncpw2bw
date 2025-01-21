#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import json
import os.path
from datetime import datetime, timezone
from collections import namedtuple
from typing import Optional


USAGE_HELP_STR = f"""Converts a Nextcloud CSV export into a Bitwarden JSON import file.
https://github.com/sausix/ncpw2bw

Usage:
{sys.argv[0]} (no arguments)          converts 'passwords_nc_export.csv' into 'passwords_bw_import.json'.
{sys.argv[0]} SOURCE_FILE             converts SOURCE_FILE into SOURCE_FILE.json.
{sys.argv[0]} SOURCE_FILE DEST_FILE   converts SOURCE_FILE into DEST_FILE.

{sys.argv[0]} -h, --help              This help.
"""


PasswordIn = namedtuple("PasswordIn",
                        [
                            "name",
                            "username",
                            "password",
                            "notes",
                            "login_uris_uri",
                            "userfields",
                            "folder",
                            "tags",
                            "favorite",
                            "revisionDate",
                            "id_uuid",
                            "version_uuid",
                            "folder_uuid"
                        ]
                        )


EMPTY_UUID_STR = "00000000-0000-0000-0000-000000000000"


def iter_passwords(csv_file: str):
    with open(csv_file, encoding="utf-8", newline="") as fh:
        csv_data = csv.reader(fh, dialect="unix", quoting=csv.QUOTE_ALL)
        next(csv_data, None)
        for pw in csv_data:
            yield PasswordIn._make(pw)


def mergefields(*args) -> Optional[str]:
    cleaned = [a.strip() for a in args if len(a.strip())]

    if not cleaned:
        return None

    return "\n".join(cleaned)


def convert(src_csv: str, dest_json: str):
    if not os.path.exists(src_csv):
        sys.stderr.write(f"SOURCE_FILE '{src_csv}' not found. Have a look at --help.")
        sys.exit(1)

    # Variables for collecting data
    folders = {}
    items = []

    # Same dates for all passwords.
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for pw in iter_passwords(src_csv):
        # Collect all unique folders
        if pw.folder_uuid != EMPTY_UUID_STR:
            folders[pw.folder_uuid] = pw.folder

        # Assemble a password entry into a Bitwarden structure
        item = {
          "passwordHistory": None,
          "revisionDate": now_str,  # TODO: revisionDate: "2025-01-21T15:22:11.892Z"
          "creationDate": now_str,
          "deletedDate": None,
          "id": pw.id_uuid,
          "organizationId": None,
          "folderId": pw.folder_uuid,
          "type": 1,
          "reprompt": 0,
          "name": pw.name,
          "notes": mergefields(pw.notes, pw.userfields, pw.tags),
          "favorite": False,  # TODO Preprocess options and let user select. Or --favorite-value=yes
          "collectionIds": None,
          "login": {
            "fido2Credentials": [],
            "uris": [
              {
                "match": None,
                "uri": pw.login_uris_uri
              }
            ] if pw.login_uris_uri else [],
            "username": pw.username or None,
            "password": pw.password or None,
            "totp": None
          }
        }

        # Append to password list
        items.append(item)

    # Write result JSON file
    with open(dest_json, "wt", encoding="utf-8") as fh:
        json.dump(
            dict(
                encrypted=False,
                folders=[dict(id=fid, name=fname) for fid, fname in folders.items()],
                items=items),
            fh,
            indent=4
        )


if __name__ == '__main__':
    cmdargs = sys.argv[1:]

    if "-h" in cmdargs or "--help" in cmdargs:
        sys.stdout.write(USAGE_HELP_STR)
        sys.exit(0)

    if len(cmdargs) == 0:
        source = "passwords_nc_export.csv"
        destination = "passwords_bw_import.json"

    elif len(cmdargs) == 1:
        source = cmdargs[0]
        destination = source + ".json"

    elif len(cmdargs) == 2:
        source = cmdargs[0]
        destination = cmdargs[1]

    else:
        sys.stderr.write("Error: Wrong amount of arguments. See help with --help.\n")
        sys.exit(1)

    convert(source, destination)
