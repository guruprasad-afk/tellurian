import requests
import os
import sys
import yaml
import argparse
from apis import actions

def parse_yaml_file(filename):
   """
   Takes a yaml file and parses its contents

   Parameters:
      filename(str): Name of the yaml file

   Returns:
      parsed_data(dict): Parsed Dictionary from the yaml file
   """

   with open(filename) as stream:
      try:
         parsed_data = yaml.safe_load(stream)
      except yaml.YAMLError as e:
         print(e)

   return parsed_data

def get_personal_access_token():
   """
   Checks whether the environment variable 'DO_PAO' is set.  
   If it is not set, exit the application

   Parameters:
      None

   Returns:
      DO_PAO: Personal Access Token
   """

   try:  
      return os.environ["DO_PAO"]
   except KeyError: 
      print("Please set the environment variable DO_PAO")
      sys.exit(1)

# INFO Get an input file from the user to parse

def main():
   parser = argparse.ArgumentParser()

   parser.add_argument("-d","--delete",action="store_true", help="delete the resources based on the current state file")

   parser.add_argument("-f","--file",type=str, help="Specify a path to the yaml file to read as input")

   args = parser.parse_args()

   DO_PAO = get_personal_access_token()

   if args.file:
      parse_file = args.file
   else:
      parse_file = "tellurian.yml"

   if args.delete:
      actions.delete_resources()
   else:
      try:
         print(f'Reading {parse_file}')
         parsed_data = parse_yaml_file(parse_file)
         print(f'{parse_file} read successfully')
         actions.create_resources(parsed_data)
      except yaml.YAMLError as e:
         print('Errors Detected in Yaml File.')



if __name__ == '__main__':
   main()
