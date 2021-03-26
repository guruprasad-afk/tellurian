# Tellurian

Provision cloud resources from Digital Ocean using just a simple yaml file.

---

### Requirements

1. Python >= 3.6 
2. Digital Ocean Account

---

### Setting up the environment variable

1. In order to interact with the DigitalOcean API, the application must be authenticated. This is done using an Personal Access Token (PAO) from Digital Ocean
2. You can generate an PAO token by visiting the [Apps & API](https://cloud.digitalocean.com/settings/applications) section of the DigitalOcean control panel for your account.
3. Copy the generated token and set it as the environment variable.**The variable name should be set exactly as `DO_PAO`**
For MacOS and Linux Distributions:
`export DO_PAO=Your_Digital_Ocean_PAO`
For Windows
`set DO_PAO=Your_Digital_Ocean_PAO`
**Note: `set` only sets the envs for the current instance of the terminal**

### Running the application

1. Clone the repository

2. Install the necessary modules using pip

`pip install -r requirements.txt`

3. Run the application using the command

`python app.py -f YAML_FILE_HERE`

4. To delete the resources that have been created, use

`python app.y -d`


### Yaml file for parsing

An [example yaml file](../examples/example1.yml) has been included for reference. It creates a single droplet with a basic nginx server and links it to the domain `example-domain.com`. After running the application with the yaml file, you should be able to see a simple web page at `example-domain.com`

**Replace `example-domain.com` with your own domain**

The application looks for a **tellurian.yml** file in the current working directory if no file is given as command-line argument

### Limitations

1. It is not possible to reference the values of one resource in another resource
2. Cannot create a droplet with the same name, image and size in the same region
3. Keyboard Interrupts can cause problems with the state file. Recommended to delete the created resources and start the command again
