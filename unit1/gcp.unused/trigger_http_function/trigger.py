import sys
import os
import requests


def request_identity_token():
    stream = os.popen('gcloud auth print-identity-token')
    token = stream.read()

    return token.strip()


def send_test_request(cloud_function_url):
    content = {'None': 'None'}
    token = request_identity_token()
    headers = { 'content-type': 'application/json', 'authorization': f'bearer {token}' }

    print(f'Sending request to {cloud_function_url}. Waiting for response...')
    response = requests.post(cloud_function_url, json=content, headers = headers)
    print(f'Response: {response.text}.')


def main():
    if len(sys.argv) < 2:
        print('Please provide the URL of the cloud function to call.')
        print('Example: python trigger.py https://<gcp generated url>')
        return

    send_test_request(sys.argv[1])


if __name__ == "__main__":
    main()
