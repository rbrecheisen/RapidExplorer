import requests
import time
import sys
import argparse
from getpass import getpass

def main():
    arg = argparse.ArgumentParser()
    arg.add_argument("--new-user", default=False, action=argparse.BooleanOptionalAction, required=False, help="Create a new user")
    arg.add_argument("--existing-user", default=True, action=argparse.BooleanOptionalAction, required=False, help="Use an existing user")
    args = arg.parse_args()

    print("new-user: ", args.new_user)
    print("existing-user: ", args.existing_user)

    if args.new_user:
        create_user_url = 'http://127.0.0.1:8000/users'
        premission_key = input("Enter permission key: ")
        username = input("Create new username: ")
        password = getpass("Create password: ")
        re_password = getpass("Re-enter password: ")
        if password != re_password:
            print("Passwords do not match")
            exit(1)
        data = {
                "username": username,
                "password_hash": password,
                "permission_key": premission_key
            }

        header = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(create_user_url, headers=header, json=data)
        print(f"Response: {response.status_code}, {response.content.decode('utf-8')}")
    elif args.existing_user:
        username = input("Enter username: ")
        password = getpass("Enter password: ")

    auth_url = "http://127.0.0.1:8000/token"
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    # Send the first request to obtain the JWT token
    response = requests.post(auth_url, data=data, headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"})

    if response.status_code == 200:
        # Extract the JWT token from the response
        response_data = response.json()
        jwt_token = response_data.get("access_token")
    else:
        print(f"Error: {response.status_code}, {response.content.decode('utf-8')}")

    url_params = {
        "request": {
            "project_name": "TD",
            "xnat_url": "http://137.120.191.233",
            "xnat_username": "abhi",
            "xnat_password": "welcome2023",
            "vertebra": "L3"
        }
    }

    # Send the second request to start the data processing
    request_url = "http://127.0.0.1:8000/ProjectName"
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(request_url, headers=header, json=url_params)
    print(f"Response: {response.status_code}, {response.content.decode('utf-8')}")
    if not response.status_code == 202:
        exit(1)

    # Replace this URL with the actual URL of your FastAPI server
    get_url = "http://localhost:8000/isDataReady"
    # JSON payload for the POST request
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    while True:
        try:
            response = requests.post(get_url, headers=headers)
            if response.status_code == 200:
                # If you expect to receive a file response, you can save it to a file
                with open("slices.zip", "wb") as file:
                    file.write(response.content)
                print("Data is ready and saved as slices.zip")
                break
            else:
                print(f"{response.status_code} {response.content.decode('utf-8')}")
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        time.sleep(30)

if __name__ == "__main__":
    main()