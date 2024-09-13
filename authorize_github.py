import time
import requests


def device_flow_authorization():
    client_id = "Ov23ctcTOZYKketJP76s"
    json_setting = {"Accept": "application/json"}

    url = "https://github.com/login/device/code"
    params = {"client_id": client_id, "scope": "public_repo"}
    response = requests.post(url, params=params, headers=json_setting).json()

    code = response["user_code"]
    interval = response["interval"]
    device_code = response["device_code"]
    print("Enter the following code on https://github.com/login/device to verify your device with GitHub.")
    print(code)

    url2 = "https://github.com/login/oauth/access_token"
    params2 = {"client_id": client_id, "device_code": device_code, "grant_type": "urn:ietf:params:oauth:grant-type"
                                                                                 ":device_code"}
    while True:
        time.sleep(interval)
        response2 = requests.post(url2, params=params2, headers=json_setting).json()

        if response2.get("error") is None:
            access_token = response2["access_token"]
            break
        else:
            error = response2["error"]
            if error == "expired_token":
                print("Your authorization request has timed out please. Please run the authorization command again.")
                return None
            if error == "access_denied":
                print("Seems like you cancelled the authorization process. Please run the authorization command again "
                      "if you would like to retry.")
                return None

    print("Your device has successfully been authorized")
    return access_token
