import requests
import os
import json
import time


def create_new_droplet(auth_token, droplet_name, region, size, image, ssh_keys, backups, ipv6, vpc_uuid, user_data, monitoring, volumes, tags):
    """
    Creates a new droplet in Digital Ocean
    """
    
    url = "https://api.digitalocean.com/v2/droplets"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json"
    }

    params = {
        "name": droplet_name,
        "region": region,
        "size": size,
        "image": image,
        "ssh_keys": ssh_keys,
        "backups": backups,
        "ipv6": ipv6,
        "user_data": user_data,
        "monitoring": monitoring,
        "volumes": volumes,
        "tags": tags
    }

    request_body = json.dumps(params)

    if vpc_uuid != '':
        params['vpc_uuid'] = vpc_uuid

    response = requests.post(url, data=request_body, headers=headers)

    json_data = response.json()

    if response.status_code == 202:

        action_links = json_data['links']

        create_action_url = action_links['actions'][0]['href']

        action_status = None

        timer = 0
        print('Creating Droplet')
        while True:

            time.sleep(10)
            timer += 10

            action_response = requests.get(create_action_url, headers=headers)

            json_action_response = action_response.json()

            action_status = json_action_response['action']['status']


            if action_status == 'completed':
                droplet_properties = list_droplets(auth_token, droplet_id=json_action_response['action']['resource_id'])

                return {
                    'status': action_status,
                    'data': {
                        'id': droplet_properties['data']['droplet']['id'],
                        'name': droplet_properties['data']['droplet']['name'],
                        'image': droplet_properties['data']['droplet']['image']['slug'],
                        'size': droplet_properties['data']['droplet']['size']['slug'],
                        'public_ip_address': droplet_properties['data']['droplet']['networks']['v4'][1]['ip_address'],
                        'region': droplet_properties['data']['droplet']['region']['slug'],
                        'tags': droplet_properties['data']['droplet']['tags']
                    }
                }

            if action_status == 'errored':
                return {
                    'status': action_status,
                    'data': {
                        "error": "Failed to create droplet"
                    }
                }

            if timer > 120:
                print('Timed Out')
                break

            print('Still Creating... ' + str(timer) + 'secs')
    else:
        return {
            'status': 400,
            'data': {
                "error": "Bad properties for droplet. Please check the values of the properties in the docs",
                "response": response.json()
            }
        }


def list_droplets(auth_token, droplet_id=None):
    """
    Lists all the droplets or droplets of a specific ID
    """

    if droplet_id != None:
        url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
    else:
        url = "https://api.digitalocean.com/v2/droplets"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    response = requests.get(url, headers=headers)

    return {
        'status': response.status_code,
        'data': response.json()
    }

def delete_droplet(auth_token, droplet_id):
    """
    Delete a droplet with a given ID
    """

    url = "https://api.digitalocean.com/v2/droplets"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    url = url + f"/{droplet_id}"

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {
            'status': response.status_code,
        }

    return {
        'status': response.status_code,
        'data': response.json()
    }

def update_droplet_image(auth_token, droplet_id, image):
    """
    Rebuild a droplet with the given image
    """

    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}/actions"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    body = {
        'type': 'rebuild',
        'image': image
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    json_data = response.json()

    if json_data['action']['status'] != 'errored':
        print('Updated Image Successfully')
    else:
        print('Update for Droplet Image Failed')

def update_droplet_ipv6(auth_token, droplet_id):
    """
    Enable ipv6 for a droplet if it is disabled
    """

    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}/actions"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    body = {
        'type': 'enable_ipv6',
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    json_data = response.json()

    if json_data['action']['status'] != 'errored':
        print('Enabled ipv6 successfully')
    else:
        print("ipv6 couldn't be enabled")

def update_droplet_size(auth_token, droplet_id, size):
    """
    Resize the droplet
    """

    url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}/actions"

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json" 
    }

    body = {
        'type': 'resize',
        'size': size
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    json_data = response.json()

    if json_data['action']['status'] != 'errored':
        print('Updated Droplet Size Successfully')
    else:
        print('Update for Droplet Size Failed')


def create_handler(properties):
    """
    Handler function for creating a new droplet 

    Parameters:
        properties(dict): An dictionary containing the properties of the droplet

    Returns:
        state(dict): Details of the droplet to store in state if create is sucessful 
    """

    auth_token = os.environ['DO_PAO']
    

    droplet_name = properties.get('name', -1)
    region = properties.get('region', -1)
    size = properties.get('size', -1)
    image = properties.get('image', -1)
    ssh_keys = properties.get('ssh_keys', [])
    backups = properties.get('backups', False)
    ipv6 = properties.get('ipv6', False)
    user_data = properties.get('user_data', None)
    vpc_uuid = properties.get('vpc_uuid', '')
    monitoring = properties.get('monitoring', False)
    volumes = properties.get('volumes', None)
    tags = properties.get('tags', [])

    if droplet_name == -1:
        print('Droplet name is required')
        return
    if region == -1:
        print('Droplet region is required')
        return
    if size == -1:
        print('Droplet size is required')
        return
    if image == -1:
        print('Droplet image is required')
        return

    result = create_new_droplet(auth_token, droplet_name, region, size, image, ssh_keys, backups, ipv6, vpc_uuid, user_data, monitoring, volumes, tags)

    if result['status'] == 'completed':
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
    Handler Function to delete the droplet

    Parameters:
        properties(dict): Properties of the DNS record
    """

    auth_token = os.environ['DO_PAO']

    droplet_id = properties['id']

    result = delete_droplet(auth_token, droplet_id)

    if result['status'] == 204:
        print({
            'status': 'SUCCESS',
            'data': f'Droplet with the id {droplet_id} was deleted successfully'
        })
    else:
        print({
            'status': 'FAILURE',
            'error': result['data']
        })

def compare_droplets(properties, existing_droplet_ids):
    """
    Checks whether a droplet already exists in the Digital Ocean System
    """

    auth_token = os.environ['DO_PAO']

    existing_droplets = list_droplets(auth_token)

    for droplet in existing_droplets['data']['droplets']:
        if droplet['name'] == properties['name'] and droplet['id'] in existing_droplet_ids:
            if not update_droplet_properties(auth_token, droplet, properties):
                return True

    return False


def update_droplet_properties(auth_token, droplet, properties):
    """
    Compares the properties of the droplet namely image, size and region
    """

    if droplet['region']['slug'] != properties['region']:
        return True

    if droplet['image']['slug'] != properties['image']:
        update_droplet_image(auth_token, droplet['id'], properties['image'])

    if droplet['size']['slug'] != properties['size']:
        update_droplet_size(auth_token, droplet['id'], properties['size'])

    ipv6 = properties.get('ipv6', False)
    if droplet['networks']['v6'] == [] and ipv6 == True:
        update_droplet_ipv6(auth_token, droplet['id'])

    return False