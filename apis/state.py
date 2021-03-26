import json
from apis import domain
from apis import droplets
from apis import dns

def load_state():
    """
    Function to load the current state from the state file. Returns empty array if the current state is null

    Parameters:
        None
    
    Returns:
        state(array): current state
    """
    try:
        return json.load(open('tellurian.tlstate'))
    except FileNotFoundError as e:
        return []
    except json.decoder.JSONDecodeError as e:
        return []


def check_state(state, resource, properties):
    """
    Checks the properties of the resource to be created with the already existing resources in state

    Parameters:
        state(dict): current state object
        resource(str): Type of resource being created
        properties(dict): Properties of the resource
    """

    if resource == 'DO_DOMAIN':
        if domain.compare_domains(properties):
            return False

    if resource == 'DO_DROPLET':
        existing_droplet_ids = [s['data']['id'] for s in state if s['resource'] == 'DO_DROPLET']
        if droplets.compare_droplets(properties, existing_droplet_ids):
            return False

    if resource == 'DO_DNS_RECORD':
        existing_record_ids = [s['data']['domain_record']['id'] for s in state if s['resource'] == 'DO_DNS_RECORD']
        if dns.compare_domains(properties, existing_record_ids):
            return False

    return True
            
def refresh_state(state_data, curr_state):
    """
    Deletes the unnecessary resources if the resource in the current state has to be deleted and replaced

    Parameters:
        state_data: Newly created resource's state details
        curr_state: Current state object
    """
    to_remove = None
    for resource in curr_state:
        if resource['identifier'] == state_data['identifier']:
            to_remove = resource

    if to_remove != None:
        if to_remove['resource'] == 'DO_DROPLET':
            droplets.delete_handler(to_remove['data'])

        if to_remove['resource'] == 'DO_DOMAIN':
            domain.delete_handler(to_remove['data'])

        if to_remove['resource'] == 'DO_DNS_RECORD':
            dns.delete_handler(to_remove['data'])
        curr_state.remove(to_remove)


    return curr_state
