import re
from locustio.common_utils import init_logger, jira_measure

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
def app_specific_action(locust):
    # webSudoBody = {"webSudoPassword"="admin"}
    # r = locust.post('secure/admin/WebSudoAuthenticate.jspa', params=webSudoBody, catch_response=True)
 
    r = locust.get('/secure/ConfigurationIntegrityCheck.jspa#system', catch_response=True, auth=("admin", "admin"))  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    if 'Configuration Integrity Check' not in content:
        logger.error(f"'Configuration Integrity Check' was not found in {content}")
    assert 'Configuration Integrity Check' in content

    checkBody = {"name":"","projectKeys":"","description":"","type":"system","isScoped":"false","includeAllFilters":"false","includeAllBoards":"false","includeAllDashboards":"false","includeProjectFilters":"false","includeProjectBoards":"false"}
    # ceckBody = {"scope" : "system"}
    headers = {'content-type': 'application/json'}
    r = locust.post('/rest/integrity-check/1.0/integrity', json=checkBody, headers=headers, catch_response=True)

    hLocation = r.headers['Location'].split("aws.com")[1]

    try:
        r = locust.get(hLocation, catch_response=True)
        logger.info(f"Successful GET for job {hLocation}")

        content = r.content.decode('utf-8')
        if 'Integrity' not in content:
            logger.error(f"'Integrity ' was not found in {content}")
        assert 'Integrity' in content
    except:
        logger.info(f"Skipped GET due to running job")


    # r = locust.get('/app/get_endpoint', catch_response=True)  # call app-specific GET endpoint
    # content = r.content.decode('utf-8')   # decode response content

    # token_pattern_example = '"token":"(.+?)"'
    # id_pattern_example = '"id":"(.+?)"'
    # token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    # id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    # logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jira.yml file
    # if 'assertion string' not in content:
    #     logger.error(f"'assertion string' was not found in {content}")
    # assert 'assertion string' in content  # assert specific string in response content

    # body = {"id": id, "token": token}  # include parsed variables to POST request body
    # headers = {'content-type': 'application/json'}
    # r = locust.post('/app/post_endpoint', body, headers, catch_response=True)  # call app-specific POST endpoint
    # content = r.content.decode('utf-8')
    # if 'assertion string after successful POST request' not in content:
    #     logger.error(f"'assertion string after successful POST request' was not found in {content}")
    # assert 'assertion string after successful POST request' in content  # assertion after POST request
