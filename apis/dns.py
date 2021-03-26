import requests
import json
import os

def create_new_dns_record(auth_token, domain_name, record_type, record_name, record_data):
    """
    Creates a new dns record for the given domain
    """
    url = f"https://api.digitalocean.com/v2/domains/{domain_name}/records"

    params = {
        "type": record_type,
        "name": record_name,
        "data": record_data,
    }

    request_body = json.dumps(params)

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    response = requests.post(url, data=request_body, headers=headers)

    return {
        'status': response.status_code,
        'data': response.json()
    }

def list_existing_records(auth_token, domain_name, record_type, record_name):
    """
    Lists all the dns records of the given type for a domain in the Digital Ocean DNS management systems
    """

    if record_name == '@':
        full_domain = domain_name
    else:
        full_domain = f'{record_name}.{domain_name}'

    url = f"https://api.digitalocean.com/v2/domains/{domain_name}/records?type={record_type}&name={full_domain}"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    response = requests.get(url, headers=headers)

    return {
        'status': response.status_code,
        'data': response.json()
    }

def update_existing_record(auth_token, domain_name, record_id, record_data):
    """
    Update an existing record with new record data
    """

    url = f"https://api.digitalocean.com/v2/domains/{domain_name}/records{record_id}"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    body = {
        'data': record_data
    }

    response = requests.put(url, data=json.dumps(body), headers=headers)


def delete_existing_record(auth_token, domain_name, record_id):
    """
    Delete a dns record using its ID
    """

    url = f"https://api.digitalocean.com/v2/domains/{domain_name}/records/{record_id}"

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

def create_handler(properties):
    """
    Handler function for creating a DNS record

    Parameters:
        properties(dict): An dictionary containing the properties of the DNS record

    Returns:
        state(dict): Details of the dns record to store in state if create is sucessful 
    """

    auth_token = os.environ['DO_PAO']

    domain_name = properties.get('domain', -1)
    record_type = properties.get('type', -1)
    record_data = properties.get('data', -1)
    record_name = properties.get('name', -1)


    if domain_name == -1:
        print('Domain Name is required')
        return
    if record_type == -1:
        print('Please specify the type of record')
        return
    if record_data == -1:
        print('Please specify the appropriate data for the record type')
        return
    if record_name == -1:
        print('Please specify a name for the record')
        return

    if record_type not in ['A', 'AAAA', 'CNAME']:
        print('Only A, AAAA and CNAME records can be created')
        return

    result = create_new_dns_record(auth_token, domain_name, record_type, record_name, record_data)

    if result['status'] == 201:
        result['data']['domain_name'] = domain_name
        return {
            'status': 'SUCCESS',
            'data': result['data']
        }
    else:
        return {
            'status': 'FAILURE',
            'error': result['data']
        }

def delete_handler(properties, domains_in_state):
    """
    Handler Function to delete the dns records in the current state
    If the domain is being deleted, then no need to delete individual records

    Parameters:
        properties(dict): Properties of the DNS record
        domains_in_state(array): An array of already existing domains in state
    """

    record_id = properties['domain_record']['id']

    if properties['domain_name'] in domains_in_state:
        print(f"Skipping Delete of record: {record_id}" )
    else:
        auth_token = os.environ['DO_PAO']

        result = delete_existing_record(auth_token, properties['domain_name'], record_id)

        if result['status'] == 204:
            print ({
                'status': 'SUCCESS',
                'data': f'The DNS record of id: {record_id} was deleted successfully'
            })
        else:
            print ({
                'status': 'FAILURE',
                'error': result['data']
            })

def compare_domains(properties, existing_record_ids):
    """
    Checks whether a dns record already exists in the Digital Ocean System
    """

    auth_token = os.environ['DO_PAO']

    existing_records = list_existing_records(auth_token, properties['domain'], properties['type'], properties['name'])

    if existing_records['status'] == 200:
        record = existing_records['data']['domain_records']

        if len(record) > 0:
            if record[0]['data'] != properties['data']:
                update_existing_record(auth_token, properties['domain'], properties['type'], properties['data'])
                print('Updated the DNS Records')
            return True

    return False