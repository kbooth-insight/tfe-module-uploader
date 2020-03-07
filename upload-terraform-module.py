import json
import tarfile
import requests
import argparse

parser = argparse.ArgumentParser(description='Upload a terraform module to Terraform Enterprise or Cloud')
parser.add_argument('--organization', help='TFE/TFC organization')
parser.add_argument('--hostname', help='Custom hostname if not TFC', default='app.terraform.io')
parser.add_argument('--module-name', help='Module name')
parser.add_argument('--module-version', help='Module version i.e. v0.5.2, or with out the v 0.5.2')
parser.add_argument('--module-path', help='Path to module direction', default='/home/kbooth/hashi/is-terraform-azurerm-ptfe-v4')
parser.add_argument('--provider-name', help='Terraform provider')
parser.add_argument('--token', help='Terraform token from owner team or user in the owner team')

args = parser.parse_args()


module_name = args.module_name
provider_name = args.provider_name
module_path =args.module_path
module_version = args.module_version
hostname = args.hostname
organization = args.organization
tfe_token = args.token

headers = {'Authorization': f'Bearer {tfe_token}', 'Content-Type': "application/vnd.api+json"}
api_endpoint = f'https://{hostname}/api/v2/'

create_path = f'organizations/{organization}/registry-modules'
module_version_path = f'registry-modules/{organization}/{module_name}/{provider_name}/versions'

module_payload = {
    "data": {
        "type": "registry-modules",
        "attributes": {
            "name": module_name,
            "provider": provider_name
        }
    }
}

module_version_payload = {
    "data": {
        "type": "registry-module-versions",
        "attributes": {
            "version": module_version
        }
    }
}

data = json.dumps(module_payload)
path = api_endpoint + create_path

response = requests.post(path, headers=headers, data=data)
if response.status_code == 422:
    print(f'Module previously created, continuing')

path = api_endpoint + module_version_path


data = json.dumps(module_version_payload)
response = requests.post(path, headers=headers, data=data)
if response.status_code == 201:
    print(f'Module {module_name} version {module_version} created')
elif response.status_code == 422:
    print(f'Module version {module_version} already taken.')
    exit(-1)
else:
    print(f'Unknown status code {response.status_code} creating module version: {response.content}')
    exit(-1)

version_content = response.json()
archivist_uri = version_content['data']['links']['upload']

with tarfile.open('./module.tar.gz', mode='w:gz') as archive:
    archive.add(module_path, recursive=True, arcname='.')

headers['Content-Type'] = 'application/octet-stream'
data = open('./module.tar.gz', 'rb').read()
response = requests.put(archivist_uri, data=data, headers=headers)
if response.status_code == 200:
    print(f'Module {module_name} version: {module_version} for provider: {provider_name} added to registry.')
else:
    print(f'Unexpected status code {response.status_code} uploading tarball: {response.content}')
    exit(-1)
