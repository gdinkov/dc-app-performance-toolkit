import re
from locustio.common_utils import init_logger, jira_measure

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
def app_specific_action(locust):
    r = locust.get('/secure/ConfigurationIntegrityCheck.jspa#system', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    # token_pattern_example = '"token":"(.+?)"'
    # id_pattern_example = '"id":"(.+?)"'
    # token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    # id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    # logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jira.yml file
    # if 'Configuration Integrity Check' not in content:
    #     logger.error(f"'Configuration Integrity Check' was not found in {content}")
    # assert 'Configuration Integrity Check' in content  # assert specific string in response content

    # body = {"id": id, "token": token}  # include parsed variables to POST request body
    # checkBody = {"name":"","projectKeys":"","description":"","type":"system","isScoped":false,"includeAllFilters":false,"includeAllBoards":false,"includeAllDashboards":false,"includeProjectFilters":false,"includeProjectBoards":false}
    apiCheckBody = {"scope" : "system"}
    headers = {'content-type': 'application/json'}
    r = locust.post('/rest/integrity-check/1.0/integrity', apiCheckBody, headers, catch_response=True)  # call app-specific POST endpoint

    hLocation = r.headers['Location'].split("aws.com")[1]

    r = locust.get(hLocation, catch_response=True)
    # content = r.content.decode('utf-8')
    # if 'Integrity Check' not in content:
    #     logger.error(f"'Integrity Check ' was not found in {content}")
    # assert 'Integrity Check ' in content  # assertion after POST request
