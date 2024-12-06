import argparse
import pathlib
import subprocess
import tempfile

from google.auth.transport.requests import Request  # type: ignore
from google.oauth2.credentials import Credentials  # type: ignore
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore

from .display import show_unseens
from .passwordstore import get_item_from_pass, store_item_in_pass

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]

PASS_TOKEN_KEY = "google/{email}.mail.token"
PASS_CRED_KEY = "google/{email}.mail.credential"


def getCred(args: argparse.Argument):
    creds = None
    tokentJson = ""
    try:
        tokentJson = get_item_from_pass(
            args.gauth_pass_token_key.format(email=args.email)
        )
    except (subprocess.CalledProcessError, Exception):
        pass
    if tokentJson:
        with tempfile.NamedTemporaryFile() as tf:
            tf.write(tokentJson.encode())
            tf.flush()
            creds = Credentials.from_authorized_user_file(pathlib.Path(tf.name), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                clientJson = get_item_from_pass(
                    args.gauth_pass_cred_key.format(email=args.email)
                )
            except (subprocess.CalledProcessError, Exception) as e:
                raise Exception("No credentials found", e)

            with tempfile.NamedTemporaryFile() as tf:
                tf.write(clientJson.encode())
                tf.flush()
                flow = InstalledAppFlow.from_client_secrets_file(
                    pathlib.Path(tf.name),
                    SCOPES,
                )
                creds = flow.run_local_server(port=0)

        store_item_in_pass(PASS_TOKEN_KEY, creds.to_json())
    return creds


def gauth_check_unseens(args: argparse.Namespace) -> list:
    creds = getCred()
    service = build("gmail", "v1", credentials=creds)
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], q="is:unread")
        .execute()
    )
    messages = results.get("messages", [])
    if not messages:
        return []
    ret = []
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        email_data = msg["payload"]["headers"]
        row = {
            x["name"]: x["value"]
            for x in email_data
            if x["name"] in ("Subject", "From", "To", "Message-ID", "Date")
        }
        row["snippet"] = msg["snippet"]
        ret.append(row)

    return ret


def gauth_check_accounts(args: argparse.Namespace) -> str:
    return show_unseens(args, gauth_check_unseens(args))


if __name__ == "__main__":
    print(gauth_check_unseens())
