from argparse import ArgumentParser
import argparse
import requests
import datetime
import json
import os
import urllib3


def to_date(date_str):
    try:
        # parse utc date
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Not a valid date: '{date_str}'. Expected format: YYYY-MM-DD")


if __name__ == "__main__":
    parser = ArgumentParser(description="Example script to interact with the Cloud Integration API")

    # parse optional start and end dates
    parser.add_argument('-s', '--start', type=to_date, help="Start date in format YYYY-MM-DD", default=datetime.datetime.utcnow() - datetime.timedelta(days=5))
    parser.add_argument('-e', '--end', type=to_date, help="End date in format YYYY-MM-DD", default=datetime.datetime.utcnow())

    args = parser.parse_args()

    # Disable SSL warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Check if the credentials file exists
    if not os.path.exists('credentials.json'):
        print("Credentials file not found. Please create a 'credentials.json' file with the required credentials.")
        exit(1)

    # Load credentials from a JSON file
    print("Loading credentials from 'credentials.json'...")
    with open('credentials.json') as f:
        credentials = json.load(f)

    # Extract credentials
    BASE_URL = credentials["url"]
    APP_ID = credentials["app-id"]
    SECRET = credentials["app-secret"]
    TENANT_ID = credentials["tenant-id"]

    # print credential TENANT_ID / APP_ID
    print(f"Tenant ID: {TENANT_ID} / App ID: {APP_ID}")

    # Define the URLs for the API endpoints
    url_device_list = f"{BASE_URL}/api/org/integrations/configs/"
    url_get_data = f"{BASE_URL}/api/tms/integrations/data/"

    # Make a GET request to retrieve the list of devices
    print("Fetching device list...")
    response = requests.get(url_device_list, headers={
        "X-AppID": APP_ID,
        "X-TenantID": TENANT_ID,
        "X-Secret": SECRET
    }, verify=False)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching device list: {response.status_code}")
        exit(1)

    # If the request was successful, parse the JSON response
    device_list = response.json()
    print(f"Found {len(device_list['vss'])} devices.")

    # Format the start and end times in the required format
    # The format is YYYY-MM-DDTHH:MM:SS
    # Note: The time is in UTC
    start_str = args.start.strftime("%Y-%m-%dT%H:%M:%S")
    end_str = args.end.strftime("%Y-%m-%dT%H:%M:%S")

    # Select the first 5 devices from the list
    # and use the first measureKey for each device
    # Note: This is just an example, you can modify it as needed
    # Create a list of dictionaries with the UUID and measureKey for each device
    # Note: The measureKey is a nested structure, so we need to access it correctly
    vss_get_data = [{"uuid": vs['uuid'], "measureKeys": [m['measureKey'] for m in vs['measureKeys']]} for vs in device_list['vss'][:5]]

    # Create the payload for the request
    payload = {
        "start": start_str,
        "stop": end_str,
        "vss": vss_get_data
    }

    # Build the headers for the request
    headers = {
        "X-AppID": APP_ID,
        "X-TenantID": TENANT_ID,
        "X-Secret": SECRET,
        "Content-Type": "application/json"
    }

    # Make a POST request to retrieve the data
    print(f"Fetching data between {start_str} and {end_str}...")
    response = requests.post(url_get_data, headers=headers, json=payload, verify=False)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(response.text)
        exit(1)

    # If the request was successful, parse the JSON response
    data = response.json()

    # print(json.dumps(data, indent=2))

    # Build CSV file
    for device in data['vss']:
        # Get the device UUID
        uuid = device['uuid']

        rows = {}
        measureKeys = set()
        for measure in device['items']:
            measureKey = measure['measureKey']
            for unix_timestamp, value in measure['data']:
                # Check if the value is None
                if value is None:
                    continue
                # Convert the timestamp to a human-readable format, original format is unix*1000 (e.g. 1745915121000)
                timestamp = datetime.datetime.fromtimestamp(unix_timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
                # Create a new row for each timestamp
                if timestamp not in rows:
                    rows[timestamp] = {}
                # Add the value to the row
                rows[timestamp][measureKey] = value
                # Add the measureKey to the set
                measureKeys.add(measureKey)

        # Sort the rows by timestamp
        rows = dict(sorted(rows.items()))

        # final directory shoud be data/<tentant_id>/<device_uuid>
        # Create the directory if it doesn't exist
        final_dir = f"data/{TENANT_ID}/{uuid}"
        os.makedirs(final_dir, exist_ok=True)

        # final_file should be <final_dir>/<extraction-timestamp>.csv
        extraction_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        final_file = f"{final_dir}/{extraction_timestamp}.csv"
            
        # Create a CSV file for each device
        with open(final_file, "w") as f:
            # Write the header
            f.write("timestamp," + ",".join(measureKeys) + "\n")
            # Write the data
            for timestamp, values in rows.items():
                # Write the timestamp
                f.write(timestamp + ",")
                # Write the values
                f.write(",".join([str(values.get(key, "")) for key in measureKeys]) + "\n")
        print(f"CSV file created for device {uuid} with {len(rows)} rows and {len(measureKeys)} columns.")

    print("All CSV files created successfully.")