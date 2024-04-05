# (c) Copyright 2023 NTT Data Thailand Ltd.
#
# This software is confidential and may contain trade secrets that are the
# property of NTT Data Thailand Ltd. No part of the software may be disclosed
# to other parties without the express written consent of NTT Data Thailand Ltd.
# It is against the law to copy the software. No part of the software may
# be reproduced, transmitted, or distributed in any form or by any means,
# electronic or mechanical, including photocopying, recording, or information
# storage and retrieval systems, for any purpose without the express written
# permission of NTT Data Thailand Ltd. our services are only available for legal
# users of the program, for instance in the event that we extend our services
# by offering the updating of files via the Internet.
#
# Created : Suppanut Ploywong
# Email : suppanut.ploywong@global.ntt

import requests
import json
import time
from datetime import datetime, timezone, timedelta
from os import path

# ignore invalid https certificate warning
requests.packages.urllib3.disable_warnings()

### CUSTOM RESULT FILE PATH HERE ###
output_file_path = "outputFile"

### CUSTOM ADDRESS OF APIC HERE ###
apic_url = ""

### CUSTOM YOUR APIC CREDENTIAL HERE ###
payload = {
    "aaaUser": {
        "attributes": {
        "name":"",
        "pwd":""
        }
    }
}
headers = {
    "Cache-Control": "no-cache",
    "Content-Type" : "application/json"
}
cookie = {}

# query class
apic_classes = [
    ('fvCEp', '?rsp-subtree=full&rsp-subtree-class=fvRsCEpToPathEp,fvIp'),
    ('fabricPathEp', '?query-target=self'),
    ('fvAEPg', '?rsp-subtree=children&rsp-subtree-class=fvCEp'),
    ('fvIp', '?rsp-subtree=full'),
    ('fvCtx', '?rsp-subtree=full'),
    ('fvATp', ''),
    ('fvL3Out', '?rsp-subtree=full'),
    ('fvL3SubInterface', '?rsp-subtree=full'),
]

# re-connect times in case error in connection
apic_api_send_limit_time = 3

## Logging function ##
def print_log(message):
    """ print timestamp in thailand time UTC+7 """
    output_message = datetime.now(timezone(timedelta(hours = 7))).strftime("[%d/%b/%Y:%H:%M:%S UTC+7] ") + message
    print(output_message)

## APIC API ##
def login_apic(recursive_count=1):
    """ APIC login and get authentication token """
    url = f"{apic_url}/api/aaaLogin.json"

    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

    if response.ok:
        cookie['APIC-cookie'] = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
        print_log(f"Login to APIC Success!")
    # After tries "apic_api_send_limit_time" time print error log and force exit program
    elif recursive_count >= apic_api_send_limit_time:
        print_log(f"Login (Last Try) Error: {response.json()['imdata'][0]['error']['attributes']['text']}. Status code: {response.status_code}")
        exit(1)
    # If there have error try to login again for "apic_api_send_limit_time" time
    else:
        print_log(f"Login ({recursive_count} Try) Error: {response.json()['imdata'][0]['error']['attributes']['text']}. Status code: {response.status_code}")
        login_apic()

def get_request_apic_api(apic_class, attr, recursive_count=1):
    """ Send GET request to APIC using RESTFUL API """
    print_log(f"Send {apic_class} class get request to {apic_url}")

    time.sleep(1)
    get_url = f"{apic_url}/api/node/class/{apic_class}.json" + attr
    response = requests.get(get_url, headers=headers, cookies=cookie, verify=False)

    if response.ok:
        print_log(f"Receive {apic_class} class success")
        return response.json()
    # If token time out send login to get new token
    elif response.status_code == 403:
        print_log(f"Session token timeout! Re-Sending login request to APIC")
        login_apic()
        return get_request_apic_api(get_url, recursive_count)
    # After tries "apic_api_send_limit_time" time print error log and force exit program
    elif recursive_count >= apic_api_send_limit_time:
        print_log(f"Get Request (Last Try) Error: {response.json()['imdata'][0]['error']['attributes']['text']}. Status code: {response.status_code}")
        exit(1)
    # If there have error try to send get request again for "apic_api_send_limit_time" time
    else:
        print_log(f"Get Request ({recursive_count} Try) Error: {response.json()['imdata'][0]['error']['attributes']['text']}. Status code: {response.status_code}")
        return get_request_apic_api(get_url, recursive_count+1)

def main():
    """ main function here """
    # get APIC API token
    login_apic()

    for index, apic_class in enumerate(apic_classes):
        output_json = get_request_apic_api(apic_class[0], apic_class[1])
        with open(f"{output_file_path}/{'%02d'%index}-{apic_class[0]}-TTB-APIC.json", "w", encoding="utf-8") as outputFile:
            json.dump(output_json, outputFile, indent=4)

    print_log(f"API json converted output file saved to {path.abspath(output_file_path)}")

if __name__ == "__main__":
    main()
