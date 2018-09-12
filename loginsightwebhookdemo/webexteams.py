#!/usr/bin/env python

from loginsightwebhookdemo import app, parse, callapi
from flask import request, json
import logging
from datetime import datetime


__author__ = "Jason Cantrell"
__license__ = "Apache v2"
__email__ = "cantrell.jm@gmail.com"
__version__ = "1.0"


# Spark/Webex Teams incoming webhook URL. For more information see these links:
# https://apphub.webex.com/integrations/incoming-webhooks-cisco-systems
# https://developer.webex.com/webhooks-explained.html
WXTEAMS = ''

@app.route("/endpoint/wxteams", methods=['POST'])
@app.route("/endpoint/wxteams/<HOOKID>", methods=['POST','PUT'])
def wxteams(HOOKID=None):
    """
    Send messages to Spark/Webex Teams. If HOOKID is not present, requires WXTEAMS defined as 'https://api.ciscospark.com/v1/webooks/incoming/<HOOKID>
    """
    # Prefer URL parameters to WXTEAMS
    if HOOKID is not None:
        URL = 'https://api.ciscospark.com/v1/webhooks/incoming/' + HOOKID
    elif not WXTEAMS or not 'https://api.ciscospark.com/v1/webhooks/incoming' in WXTEAMS:
        return ("WXTEAMS parameter must be set properly, please edit the shim!", 500, None)
    else:
        URL = WXTEAMS

    a = parse(request)

    try:
        if ('alertId' in a):
            alertTime = (datetime.fromtimestamp(a.startDate)).strftime('%Y-%m-%d %H:%M:%S')
            message = 'Resource Name: {resourceName}\nTimestamp: {alertTime}\nStatus: {status}\nInfo: {info}'.format(
                resourceName=a.resourceName,alertTime=alertTime,status=a.status,info=a.info)
            payload = {
                "text": message
            }
    except:
        logging.exception("Can't create new payload. Check code and try again.")
        raise

    return callapi(URL, 'post', json.dumps(payload))