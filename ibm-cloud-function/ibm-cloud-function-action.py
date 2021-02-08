#
# Copyright 2020- IBM Inc. All rights reserved
# SPDX-License-Identifier: Apache2.0
#
import logging
import requests
import json
import ibm_boto3
import gzip

from datetime import datetime
from datetime import timezone
from time import time
from ibm_botocore.client import Config, ClientError



def main(params):
    #validate params
    logging.info("Validating parameters")
    validationResult = validateParams(params)
    if validationResult[0] != True:
        return {'Error': validationResult[1]}
    else:
        validatedParams = validationResult[1]

    #download COS file
    cos = ibm_boto3.client("s3",ibm_api_key_id=params['cos_api_key'],ibm_service_instance_id=params['cos_instance_crn'],config=Config(signature_version="oauth"),endpoint_url=params['cos_endpoint'])
    file = cos.get_object(Bucket=params['bucket'], Key=params['key'])
    data_body = file['Body']
    
    #Unzip and get JSON logs
    event_data = []
    with gzip.open(data_body, 'rt') as flow_data:
            for lines in flow_data:
                for flow_entry in (json.loads(lines)["flow_logs"]):                    
                    if flow_entry['start_time']:
                        #Gather Events
                        event_data.append(buildEventLine(flow_entry))

    post_data = ({"lines":event_data})
    if sendToLogDna(post_data,params):
        return {"Success":"Flow logs successfully sent to LogDNA"}        
    else:
        return {"Error":"Failed to send logs to LogDNA"}
        

                        
def buildEventLine(flow_entry):
    flow_info = {
                "LogSourceTime":flow_entry["start_time"],
                "Accessallowed":flow_entry["action"],
                "SourceIP":flow_entry["initiator_ip"],
                "DestinationIP":flow_entry["target_ip"],
                "SourcePort":flow_entry["initiator_port"],
                "DestinationPort":flow_entry["target_port"],
                "Protocol":flow_entry["transport_protocol"],
                "BytesFromClient":flow_entry["bytes_from_initiator"],
                "BytesFromServer":flow_entry["bytes_from_target"],
                "PacketsFromClient":flow_entry["packets_from_initiator"],
                "PacketsFromServer":flow_entry["packets_from_target"]
                }
    log_line = {
                "line":json.dumps(flow_info),
                "eventTime": str(datetime.now(timezone.utc)), 
                "app":"vpc-flow-logs",
                "level":"info"                       
    }
    return log_line
            


def validateParams(params):
    validatedParams = params.copy()
    requiredParams = ['cos_endpoint', 'cos_api_key', 'cos_instance_crn', 'logdna_host', 'logdna_injest_key']
    missingParams = []    

    for requiredParam in requiredParams:
        if requiredParam not in params:
            missingParams.append(requiredParam)

    if len(missingParams) > 0:
        return (False, "You must supply all of the following parameters: {}".format(', '.join(missingParams)))
        
    return (True,"Validated Params")
    
 
def sendToLogDna(post_data, params):
    #Build Headers
    time_stamp = str( round(time()*1000))
    date_stamp = str(datetime.now(timezone.utc))
    url_params = {'hostname':'ibm-cloud-vpc-flow-logs','now':time_stamp, 'apikey':params['logdna_injest_key']}
    url = params['logdna_host']
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    
    #Make Request
    r = requests.post(url, headers=headers, params=url_params, data=json.dumps(post_data))
    if (r.status_code == 200):
        return True
    else:
        logging.error("Error Posting to LogDNA: " + r.text)
        return False