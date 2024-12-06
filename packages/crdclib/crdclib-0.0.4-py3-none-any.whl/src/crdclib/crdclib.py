# A collection of random routines I use frequently
import yaml
import requests
import json
import re
import os


def readYAML(yamlfile):

    """
    This method reads a YAML file and returns a JSON object
    :param yamlfile: A full path to the yaml file to be parsed
    :type yamlfile: String
    :return: A JSON object/dictionary representing the YAML file content
    :rtype: dictionary
    """

    with open(yamlfile) as f:
        yamljson = yaml.load(f, Loader=yaml.FullLoader)
    return yamljson


def writeYAML(filename, jsonobj):

    """
    Takes a filename and JSON object/dictionary and writes out a basic yaml file
    :param filename: A full path to the output file
    :type filename: String
    :param jsonobj: A dictionary to be written as YAML
    :type jsonobj: Dictionary
    """

    with open(filename, 'w') as f:
        yaml.dump(jsonobj, f)
    f.close()


def getCDERecord(cde_id, cde_version=None, verbose=False):

    """
    Queries the caDSR API with a CDE identifier and optional version, returns the full JSON object
    #If no version is given, returns whatever the latest version is.
    :param cde_id: CDE Public identifier
    :type cde_id: Integer
    :param cde_version: The version of the CDE to be queried.  If not supplied the latest version will be returned
    :type cde_version: String, optional
    :return: If status_code == 200, a JSON object that is the full CDE record
    :rtype: dictionary
    :return: If status_code != 200, a string with error code and message
    :rtype: string
    :return: If HTTP error, the requests.HTTPError object
    :rtype: request.HTTPError
    """

    if verbose:
        print(f"CDE ID:\t{cde_id}\tVersion:\t{cde_version}")
    if cde_version is None:
        url = "https://cadsrapi.cancer.gov/rad/NCIAPI/1.0/api/DataElement/"+str(cde_id)
    else:
        url = "https://cadsrapi.cancer.gov/rad/NCIAPI/1.0/api/DataElement/"+str(cde_id)+"?version="+str(cde_version)
    headers = {'accept': 'application/json'}
    try:
        results = requests.get(url, headers=headers)
    except requests.exceptions.HTTPError as e:
        return (f"HTTPError:\n{e}")
    if results.status_code == 200:
        results = json.loads(results.content.decode())
        return results
    else:
        return (f"Error Code: {results.status_code}\n{results.content}")


def cleanString(inputstring, leavewhitespace=False):

    """
    Removes non-printing characters and whitespaces from strings
    :param inputstring: The string to be processed
    :type intputstring: String
    :param leavewhitespace: Boolean, if True, uses regex [\n\r\t?]+.  If False, uses regex [\W]+
    :type leavewhitespace: Boolean, optional, default False
    :return: Processed string
    :rtype: String
    """

    if leavewhitespace:
        outputstring = re.sub(r'[\n\r\t?]+', '', inputstring)
        outputstring.rstrip()
    else:
        outputstring = re.sub(r'[\W]+', '', inputstring)
    return outputstring


def dhApiQuery(url, apitoken, query, variables=None):

    """
    Runs queries against the Data Hub Submission Portal API
    :param url: URL of the Submission Portal API
    :type url: URL
    :param apitoken: API Access token obtained from the Submission Portal
    :type apitoken: String
    :param query: A valid GraphQL query
    :type query: String
    :param variables: a JSON object containing any variables for the provided query
    :type variables: dictionary, optional
    :return: If status_code == 200, a JSON object that is the full query response
    :rtype: dictionary
    :return: If status_code != 200, a string with error code and message
    :rtype: string
    :return: If HTTP error, the requests.HTTPError object
    :rtype: request.HTTPError
    """

    headers = {"Authorization": f"Bearer {apitoken}"}
    try:
        if variables is None:
            result = requests.post(url=url, headers=headers, json={"query": query})
        else:
            result = requests.post(url=url, headers=headers, json={"query": query, "variables": variables})
        if result.status_code == 200:
            return result.json()
        else:
            return (f"Status Code: {result.status_code}\n{result.content}")
    except requests.exceptions.HTTPError as e:
        return (f"HTTPError: {e}")
 

def dhAPICreds(tier):

    """
    A simple way to retrieve the Data Hub submission URLs and API tokens
    :param tier: A string for the tier to return.  Must be one of prod, stage, qa, qa2, dev, dev2
    :type tier: String
    :return url: The URL for the requested tier
    :rtype url: string
    :return token: The API access token for the tier.
    :rtype token: dictionary
    """

    url = None
    token = None
    if tier == 'prod':
        url = 'https://hub.datacommons.cancer.gov/api/graphql'
        token = os.getenv('PRODAPI')
    elif tier == 'stage':
        url = 'https://hub-stage.datacommons.cancer.gov/api/graphql'
        token = os.getenv('STAGEAPI')
    elif tier == 'qa':
        url = 'https://hub-qa.datacommons.cancer.gov/api/graphql'
        token = os.getenv('QAAPI')
    elif tier == 'qa2':
        url = 'https://hub-qa2.datacommons.cancer.gov/api/graphql'
        token = os.getenv('QA2API')
    elif tier == 'dev':
        url = 'https://hub-dev.datacommons.cancer.gov/api/graphql'
        token = os.getenv('DEVAPI')
    elif tier == 'dev2':
        url = 'https://hub-dev2.datacommons.cancer.gov/api/graphql'
        token = os.getenv('DEV2API')
    elif tier == 'localtest':
        url = 'https://this.is.a.test/url/graphql'
        token = os.getenv('LOCALTESTAPI')
    return {'url': url, 'token': token}
