<!-- This should be the location of the title of the repository, normally the short name -->
# ibm-cloud-vpc-logs-2-qradar

## Scope

The purpose of this project is to provide a mechanism for ingesting IBM Cloud VPC Flow Logs into QRadar.

# Pre-Requisites

## IBM Cloud

IBM Cloud User account with privileges to:
1. Create and configure IBM Cloud Object Storage instances and buckets.
2. Create and configure IBM LogDNA
3. Create and configure IBM Cloud Functions

IBM Cloud Service Accounts
    When configuring IBM Cloud VPC Flow logs to use IBM Fucntions Triggers & Actions and Cloud Object Storage you will need to configure service IDs with the appropriate privileges. Refer to the [About IBM Cloud Flow Logs for VPC](https://cloud.ibm.com/docs/vpc?topic=vpc-flow-logs&locale=en) and integrating [Cloud Functions with Cloud Obeject Storage](https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-pkg_obstorage) for steps for creating the appropriate service IDs.

## QRadar
1. IBM QRadar 7.4 or higher
2. IBM QRadar user account with privileges to create/modify log sources and create/modify DSMs.

# Setup

## Sending IBM Cloud VPC Flow Logs to LogDNA
There are options for how to send the VPC Flow logs to Log DNA.
1. Use the instructions outlined at  https://github.com/IBM-Cloud/vpc-flowlogs-logdna.
2. Use the example action in this repo ibm-cloud-function/ibm-cloud-function-action.py. *Note the provided [Example QRadar DSM](https://github.com/IBM/ibm-cloud-vpc-logs-2-qradar/blob/master/IBM%20Cloud%20LogDNA%20for%20VPC%20Flow%20Logs-20210208104351.zip) was created based upon using this example.


## Setup QRadar using the Universal Cloud REST API

The parameters needed to configure the Univeral Cloud Rest API require information specific to the instance of IBM Cloud LogDNA. See below on how to get the required parameters. The two required parameters are Host Name and Service Key. There are optional parameters below that allow you to limit the LogDNA query results.

# Getting IBM Cloud LogDNA Hostname

To obtain the 'Host Name':
1. Log on to the IBM Cloud LogDNA
2. Navigate to "Installation Instructions"
3. Click 'REST API'
4. This will give you the URL for the LogDNA service in your region. Example: https://logs.us-south.logging.cloud.ibm.com
5. This URL is for log ingestion, so you will need to modify the URL for event export.
6. In the URL relpace 'logs' with 'api'. Example: https://api.us-south.logging.cloud.ibm.com 

# Getting IBM Cloud LogDNA Service Key

To obtain a 'Service Key':
1. Log on to the IBM Cloud LogDNA
2. Navigate to "Settings"
3. Click "Organization"
4. Click the 'API Keys'
7. Generate or choose and existing 'Service Key'

# QRadar Log Source Configuration

1. Log in to QRadar.
2. Click the _Admin_ tab.
3. To open the app, click the _QRadar Log Source Management_ app icon.
4. Click _New Log Source_ > Single Log Source.
5. On the Select a Log Source Type page, _Select a Log Source Type (Universal DSM)_ and click _Select Protocol Type (Universal Rest API)_.
6. On the Select a Protocol Type page, select a protocol and click _Configure Log Source Parameters_.
7. On the Configure the Log Source parameters page, configure the log source parameters and click _Configure Protocol
Parameters_.
8. On the Configure the Protocol Parameters page, configure the protocol-specific parameters (Workflow and Workflow
Parameter Values). 
9. In the Test protocol parameters window, click _Start Test_.
10. To fix any errors, click _Configure Protocol Parameters_. Configure the parameters and click Test Protocol Parameters.
11. Click _Finish_


# Optional IBM Cloud LogDNA Query Options

    There are 2 optional query options to limit the number of returns based upon LogDNA Log Source and LogDNA Application. These parameters are 'logsourcehosts' and 'logsourceapps' that can be configured in IBMCloud-LogDNA-Workflow-Parameter.xml. Additional query options can configured, see https://docs.logdna.com/reference#v1export-1.

    logsourcehosts: comma separated list of hosts to filter by
    logsourceapps:  comma separated list of apps to filter by

<!-- A notes section is useful for anything that isn't covered in the Usage or Scope. Like what we have below. -->
## Notes

If you have any questions or issues you can create a new [issue here][issues].

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1. Fork the repo
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License

All source files must include a Copyright and License header. 

If you would like to see the detailed LICENSE click [here](LICENSE).

```text
#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
```

