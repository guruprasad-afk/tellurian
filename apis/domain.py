import requests
import os
import json


def create_new_domain(auth_token, domain_name, ip_address):
    """
    Creates a new domain using the Digital Ocean API
    """

    url = "https://api.digitalocean.com/v2/domains"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    } 

    params = {
        "name": domain_name,
    }

    request_body = json.dumps(params)

    if ip_address != None:
        params["ip_address"] = ip_address

    response = requests.post(url, headers=headers, data=request_body)

    return {
        'status': response.status_code,
        'data': response.json()
    }


def delete_existing_domain(auth_token, domain_name):
    """
    Deletes an existing domain based on the name
    """
    
    url = f"https://api.digitalocean.com/v2/domains/{domain_name}"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {
            'status': response.status_code,
        }

    return {
        'status': response.status_code,
        'data': response.json()
    }

# INFO List all existing domains or list a specific domain

def list_domains(auth_token, domain_name):
    """
    List all existing domains or list a specific domain
    """
    
    if domain_name != '':
        url = f"https://api.digitalocean.com/v2/domains/{domain_name}"
    else:
        url = f"https://api.digitalocean.com/v2/domains"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    response = requests.get(url, headers=headers)

    return {
        'status': response.status_code,
        'data': response.json()
    }

def create_handler(properties):
    """
    Handler function for creating a new Domain

    Parameters:
        properties(dict): An dictionary containing the properties of the Domain

    Returns:
        state(dict): Details of the Domain to store in state if create is sucessful 
    """
    
    auth_token = os.environ['DO_PAO']
    
    domain_name = properties.get('name', -1)
    ip_address = properties.get('ip_address', None)

    if domain_name == -1:
        print('Domain name is required')
        return

    result = create_new_domain(auth_token, domain_name, ip_address)

    if result['status'] == 201:
        return {
            'status': 'SUCCESS',
            'data': result['data']
        }
    else:
        return {
            'status': 'FAILURE',
            'error': result['data']
        }

def delete_handler(properties):
    """
    Handler Function to delete the domains in the current state

    Parameters:
        properties(dict): Properties of the DNS domain
    """

    auth_token = os.environ['DO_PAO']

    domain_name = properties['domain']['name']

    result = delete_existing_domain(auth_token, domain_name)

    if result['status'] == 204:
        print({
            'status': 'SUCCESS',
            'data': f'{domain_name} deleted successfully'
        })
    else:
        print({
            'status': 'FAILURE',
            'error': result['data']
        })

def compare_domains(properties):
    """
    Checks whether a domain already exists in the Digital Ocean System
    """

    auth_token = os.environ['DO_PAO']

    existing_domains = list_domains(auth_token, properties['name'])

    if existing_domains['status'] == 200:
        return True

    return False
