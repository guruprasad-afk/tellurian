from apis import domain
from apis import dns
from apis import droplets
from apis import state
import sys
import json

def domain_handler(properties):
    """
    Passes the properties of domain to be created to a handler function in the domain module
    """
    return domain.create_handler(properties)
    
def dns_handler(properties):
    """
    Passes the properties of droplet to be created to a handler function in the droplet module
    """
    return dns.create_handler(properties)

def droplet_handler(properties):
    """
    Passes the properties of dns record to be created to a handler function in the dns module
    """
    return droplets.create_handler(properties)


def resource_switcher(resource, properties):
    """
    Calls the approriate handler function based on the resource type

    Parameters:
        resource(str): Type of resource to be created
        properties(dict): Properties of the resource
    """

    switcher = {
        'DO_DOMAIN': domain_handler,
        'DO_DNS_RECORD': dns_handler,
        'DO_DROPLET': droplet_handler
    }

    func = switcher.get(resource, 0)
    if func == 0:
        return {
            'status': "FAILURE",
            'error': f'No such resource: {resource}'
        }

    return func(properties)


def create_resources(parsed_yaml_data):
    """
    Performs function calls to check, refresh and write the state before calling the appropriate handler functions 
    to create the resource.

    Parameters:
        parsed_yaml_data(dict): Data parsed from YAML file
    """

    curr_state = state.load_state()

    if parsed_yaml_data.get('actions', 0) == 0:
        print('Error with YAML specification')
        print("actions attribute is required")
        return

    for action in parsed_yaml_data['actions']:

        # INFO Get attributes for each action
        identifier = action.get('identifier', '')
        properties = action.get('properties', {})

        if identifier == '' or properties == {}:
            print('Error with YAML specification')
            print("identifier attribute is required")
            return

        print(f'Starting Task: {identifier}\n\n')

        if state.check_state(curr_state, action['resource'], properties):

            # INFO Function to call the appropriate handler function based on the resource
            created_resource = resource_switcher(action['resource'], properties)

            if created_resource['status']  == 'SUCCESS':
                state_data = {}
                state_data['identifier'] = identifier
                state_data['resource'] = action['resource']
                state_data['data'] = created_resource['data']

                curr_state = state.refresh_state(state_data, curr_state)
                curr_state.append(state_data)
            else:
                print(created_resource)


            print(f'\nFinished Task: {identifier}\n')
        else:
            print(f'\n Skipping Task: {identifier}\n')

    with open('tellurian.tlstate', 'w') as f:
        json.dump(curr_state, f)


def delete_resources():
    """
    Deletes the resources and clears the state file when the -d flag is set.
    """

    curr_state = state.load_state()

    domains_in_state = [r['data']['domain']['name'] for r in curr_state if r['resource'] == 'DO_DOMAIN']

    for rsrc in curr_state:

        if rsrc['resource'] == 'DO_DOMAIN':
            domain.delete_handler(rsrc['data'])
            
        if rsrc['resource'] == 'DO_DNS_RECORD':
            dns.delete_handler(rsrc['data'], domains_in_state)

        if rsrc['resource'] == 'DO_DROPLET':
            droplets.delete_handler(rsrc['data'])

    with open('tellurian.tlstate', 'w') as f:
        f.write('')