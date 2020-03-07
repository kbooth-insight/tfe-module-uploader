# tfe-module-uploader


Uploads a module using Terraform Cloud/Enterprise API

## example usage

```
python3 tfe-module-uploader.py --help
usage: tfe-module-uploader.py [-h] [--organization ORGANIZATION]
                              [--hostname HOSTNAME]
                              [--module-name MODULE_NAME]
                              [--module-version MODULE_VERSION]
                              [--module-path MODULE_PATH]
                              [--provider-name PROVIDER_NAME] [--token TOKEN]

Upload a terraform module to Terraform Enterprise or Cloud

optional arguments:
  -h, --help            show this help message and exit
  --organization ORGANIZATION
                        TFE/TFC organization (default: None)
  --hostname HOSTNAME   Custom hostname if not TFC (default: app.terraform.io)
  --module-name MODULE_NAME
                        Module name (default: None)
  --module-version MODULE_VERSION
                        Module version i.e. v0.5.2, or with out the v 0.5.2
                        (default: None)
  --module-path MODULE_PATH
                        Path to module direction (default: ./)
  --provider-name PROVIDER_NAME
                        Terraform provider (default: None)
  --token TOKEN         Terraform token from owner team or user in the owner
                        team (default: None)

```

Invoke on command line like this:
```
$python3 tfe-module-uploader.py --provider-name="azurerm" \
--module-version="0.0.4" \ 
--module-name="booth-api-test2" \
--organization="cardinalsolutions" \
--token="<tfetoken>"
```


Example output:

```
Module booth-api-test2 version 0.0.4 created
Module booth-api-test2 version: 0.0.4 for provider: azurerm added to registry.
```