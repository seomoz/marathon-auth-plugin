#!/usr/bin/python

from __future__ import print_function
import unittest
import os
import socket
import argparse
import json
import sys
import httplib
import urllib
import requests
import base64
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "cli"))

def post_data(url,headers,payload):
    result = requests.post(url, data=json.dumps(payload), headers=headers)
    return (result.status_code)

def get_data(url,headers,payload):
    url = url+payload['id']
    result = requests.get(url,data=payload,headers=headers)
    return result.status_code

def put_data(url,headers,payload):
    url = url+payload['id']
    result = requests.put(url, data=json.dumps(payload), headers=headers)
    return (result.status_code)

def delete_data(url,headers,payload):
    url = url+payload['id']
    result = requests.delete(url, data=json.dumps(payload), headers=headers)
    return (result.status_code)

def test_create_app_with_no_headers(environment):

    app_url = 'http://'+environment+':8080/v2/apps'

    with open("auth-poc-prod-test-app.json") as json_file:
         json_data = json.load(json_file)
    headers = { "Content-Type": "application/json" }

    # Create App
    result_code = post_data(app_url,headers,json_data)
    assert (result_code != '201')
    print("Create Test: Pass")

    # Read App
    result_code = get_data(app_url,headers,json_data)
    assert(result_code != 200)
    print("Read Test: Pass")

    # Update App
    result_code = put_data(app_url,headers,json_data)
    assert(result_code != 200)
    print("Update Test: Pass")

    # Delete App
    result_code = delete_data(app_url,headers,json_data)
    assert(result_code != 200)
    print("Delete Test: Pass\n")

def test_user_crud_on_root(environment):

    app_url = 'http://'+environment+':8080/v2/apps'

    with open("auth-poc-prod-test-app.json") as json_file:
         json_data = json.load(json_file)

    # Creating Authorization for header using Base64 encoding (username:password)
    encoded = base64.b64encode(b'admin:admin')
    encoded = "Basic " + encoded
    headers = { "Content-Type": "application/json", "Authorization" : encoded }

    # Create App
    result_code = post_data(app_url,headers,json_data)
    assert(result_code == 201)
    print("Create Test: Pass")

    # Read App
    result_code = get_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Read Test: Pass")

    # Update App
    result_code = put_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Update Test: Pass")

    # Delete App
    result_code = delete_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Delete Test: Pass\n")

def test_user_ben_on_dev(environment):

    app_url = 'http://'+environment+':8080/v2/apps'

    with open("auth-poc-dev-test-app.json") as json_file:
         json_data = json.load(json_file)

    # Creating Authorization for header using Base64 encoding (username:password)
    encoded = base64.b64encode(b'ben:ben')
    encoded = "Basic " + encoded
    headers = { "Content-Type": "application/json", "Authorization" : encoded }

    # Create App
    result_code = post_data(app_url,headers,json_data)
    assert(result_code == 201)
    print("Create Test: Pass")

    # Read App
    result_code = get_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Read Test: Pass")

    # Update App
    result_code = put_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Update Test: Pass")

    # Delete App
    result_code = delete_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Delete Test: Pass\n")

def test_user_mac_dev_shared_with_ben(environment):

    app_url = 'http://'+environment+':8080/v2/apps'

    with open("auth-poc-dev-shared-test-app.json") as json_file:
         json_data = json.load(json_file)

    # Creating Authorization for header using Base64 encoding (username:password)
    encoded = base64.b64encode(b'mac:mac')
    encoded = "Basic " + encoded
    headers = { "Content-Type": "application/json", "Authorization" : encoded }

    # Create App
    result_code = post_data(app_url,headers,json_data)
    assert(result_code == 201)
    print("Create Test: Pass")

    # Read App
    result_code = get_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Read Test: Pass")

    # Update App
    result_code = put_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Update Test: Pass")

    # Delete App
    result_code = delete_data(app_url,headers,json_data)
    assert(result_code == 200)
    print("Delete Test: Pass\n")

def test_user_crud_in_unauthorized_environment(environment):

    app_url = 'http://'+environment+':8080/v2/apps'

    with open("auth-poc-prod-test-app.json") as json_file:
         json_data = json.load(json_file)

    # Creating Authorization for header using Base64 encoding (username:password)
    encoded = base64.b64encode(b'mac:mac')
    encoded = "Basic " + encoded
    headers = { "Content-Type": "application/json", "Authorization" : encoded }

    # Create App
    result_code = post_data(app_url,headers,json_data)
    assert(result_code != 201)
    print("Create Test: Not Allowed to Create -- Result: Pass")

    # Read App
    result_code = get_data(app_url,headers,json_data)
    assert(result_code != 200)
    print("Read Test: Not Allowed to Read -- Result: Pass")

    # Update App
    result_code = put_data(app_url,headers,json_data)
    assert(result_code != 200)
    print("Update Test: Not Allowed to Update -- Result: Pass")

    # Delete App
    result_code = delete_data(app_url,headers,json_data)
    print("Delete Test: Not Allowed to Delete -- Result: Pass\n")

def main(args):

    if len(args) < 2:
        print("Please provide list of machines and retry.\nExiting...")
        sys.exit(0)

    # Iterate through all the environments and execute all the tests
    for i in range(1,len(args)):

        port = 8080
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((args[i], port))
        sock.settimeout(1)
        if result == 0:
            sock.close()
        else:
            print ("\nEnvironment {}: Unreachable".format(args[i]))
            sock.close()
            continue

        print ("\nExecuting Tests for environemnt :",args[i])

        print("\nExecuting Test: User with Root Access:\n")
        test_user_crud_on_root(args[i])
        print("\nExecuting Test: User with No Access:\n")
        test_create_app_with_no_headers(args[i])
        print("\nExecuting Test: User with Dev Access:\n")
        test_user_ben_on_dev(args[i])
        print("\nExecuting Test: User with Shared Directory Access:\n")
        test_user_mac_dev_shared_with_ben(args[i])
        print("\nExecuting Test: CRUD on Unauthorized Environment:\n")
        test_user_crud_in_unauthorized_environment(args[i])

if __name__ == "__main__":
    main(sys.argv)
