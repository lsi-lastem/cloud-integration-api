#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from json import dump
from os import listdir, remove
import os


PATH_CREDENTIALS = 'credentials'


if not os.path.exists(PATH_CREDENTIALS):
    os.makedirs(PATH_CREDENTIALS)


# credentials are file json with these keys:
# - url
# - app-id
# - app-secret
# - tenant-id


if __name__ == "__main__":
    parser = ArgumentParser(description="Credential Manager")
    parser.add_argument('action', choices=['list', 'add', 'show', 'delete', 'apply'], help="Action to perform")
    args = parser.parse_args()

    if args.action == 'list':
        print("Listing all credentials...")
        # Code to list all credentials (file json in PATH_CREDENTIALS)
        for filename in listdir(PATH_CREDENTIALS):
            if filename.endswith('.json'):
                print(f"- {filename[:-5]}")
        print("Done.")
    elif args.action == 'add':
        # read from input
        print("Adding new credentials...")
        name = input("Enter the name of the credentials: ").strip()
        url = input("Enter the url: ").strip()

        # if url is: test, demo, staging, dev --> use https://lsicp.it
        # if url is: prod, production, live --> use https://lsicp.com
        if url in ['test', 'demo', 'staging', 'dev']:
            url = "https://lsicp.it"
        elif url in ['prod', 'production', 'live']:
            url = "https://lsi-lastem.cloud"
        else:
            # check if is url or error
            if not url.startswith('http'):
                print("Error: url must be a valid url or one of the following: test, demo, staging, dev, prod, production, live")
                exit(1)
            else:
                url = url.strip()

        app_id = input("Enter the app id: ").strip()
        app_secret = input("Enter the app secret: ").strip()    
        tenant_id = input("Enter the tenant id: ").strip()
        # create the file
        cred_obj = {
            "name": name,
            "url": url,
            "app-id": app_id,
            "app-secret": app_secret,
            "tenant-id": tenant_id
        }
        with open(f"{PATH_CREDENTIALS}/{name}.json", 'w') as f:
            dump(cred_obj, f, indent=2)
        print(f"Credentials {name} added.")
        print("Done.")
    elif args.action == 'show':
        # read from input
        print("Showing credentials...")
        name = input("Enter the name of the credentials: ")
        # read the file
        try:
            with open(f"{PATH_CREDENTIALS}/{name}.json", 'r') as f:
                cred_obj = f.read()
            print(cred_obj)
        except FileNotFoundError:
            print(f"Credentials {name} not found.")
        print("Done.")
    elif args.action == 'delete':
        # read from input
        print("Deleting credentials...")
        name = input("Enter the name of the credentials: ")
        # delete the file
        try:
            remove(f"{PATH_CREDENTIALS}/{name}.json")
            print(f"Credentials {name} deleted.")
        except FileNotFoundError:
            print(f"Credentials {name} not found.")
        print("Done.")
    elif args.action == 'apply':
        # read from input
        print("Applying credentials...")
        name = input("Enter the name of the credentials: ")
        # copy the file to the current directory as credentials.json
        with open(f"{PATH_CREDENTIALS}/{name}.json", 'r') as f:
            cred_obj = f.read()
        with open('credentials.json', 'w') as f:
            f.write(cred_obj)
        print(f"Credentials {name} applied.")
    else:
        print("Invalid action. Use 'list', 'add', 'show' or 'delete'.")
        exit(1)

