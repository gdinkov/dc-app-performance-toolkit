import re
import time
from locustio.common_utils import init_logger, jira_measure

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
def app_specific_action(locust):
    # webSudoBody = {"webSudoPassword"="admin"}
    # r = locust.post('secure/admin/WebSudoAuthenticate.jspa', params=webSudoBody, catch_response=True)

    # CMJ stuff below
    r = locust.get('/secure/ConfigurationSnapshot.jspa', catch_response=True, auth=("admin", "admin"))
    content = r.content.decode('utf-8')   # decode response content

    if 'Configuration Snapshots' not in content:
        logger.error(f"'Configuration Snapshots' was not found in {content}")
    assert 'Configuration Snapshots' in content

    snapshotName = "testSnapshot" + str(int(time.time()*1000))
    snapshotCreateBody = {"type":"projectWithIssues","filter":"","includeAllIssues":"true","checkCustomFieldValues":"true","includeAttachmentFiles":"false","filters":[],"boards":[],"dashboards":[],"appsWithGlobalData":[],"includeAllFilters":"false","includeAllBoards":"false","includeAllDashboards":"false","includeGlobalAppData":"false","includeProjectFilters":"true","includeProjectBoards":"true","filterSelectionApplied":"false","boardSelectionApplied":"false","projectKeys":["CRUSR"],"hasValidAgileVersion":"true","name":snapshotName}
    headers = {'content-type': 'application/json'}
    r = locust.post('/rest/configuration-manager/1.0/snapshots', json=snapshotCreateBody, headers=headers, catch_response=True)

    content = r.content.decode('utf-8')
    progressID = content.split("/")[1]

    try:
        r = locust.get("/rest/configuration-manager/1.0/snapshots/progress/" + progressID, catch_response=True)
        logger.info(f"Successful GET for job {progressID}")

        content = r.content.decode('utf-8')
        if 'auditMaxSeverity' not in content:
            logger.error(f"'auditMaxSeverity' was not found in {content}")
        assert 'auditMaxSeverity' in content
    except:
        logger.info(f"Skipped due to running job {progressID}")
 
    r = locust.get('/secure/ConfigurationDeploy.jspa', catch_response=True, auth=("admin", "admin"))
    content = r.content.decode('utf-8')   # decode response content

    if 'Deploy Configuration Snapshot' not in content:
        logger.error(f"'Deploy Configuration Snapshot' was not found in {content}")
    assert 'Deploy Configuration Snapshot' in content

    r = locust.get('/secure/ManageAuditConfiguration.jspa', catch_response=True, auth=("admin", "admin"))
    content = r.content.decode('utf-8')   # decode response content

    if 'Audit Logs' not in content:
        logger.error(f"'Audit Logs' was not found in {content}")
    assert 'Audit Logs' in content

    r = locust.get('/secure/ManageAuditConfiguration.jspa#/details?id=1', catch_response=True, auth=("admin", "admin"))
    content = r.content.decode('utf-8')   # decode response content

    if 'Audit Logs' not in content:
        logger.error(f"'Audit Logs' was not found in {content}")
    assert 'Audit Logs' in content

    # PA stuff below
    # r = locust.get('/secure/PowerAdminSearch.jspa?query=&type=CUSTOM_FIELD', catch_response=True, auth=("admin", "admin"))

    # r = locust.get('/rest/power-admin/1.0/search/types', catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'Custom Field' not in content:
    #     logger.error(f"'Custom Field' was not found in {content}")
    # assert 'Custom Field' in content

    # r = locust.get('/rest/power-admin/1.0/search/customfieldtypes', catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'customfieldTypes' not in content:
    #     logger.error(f"'customfieldTypes' was not found in {content}")
    # assert 'customfieldTypes' in content

    # searchBody = {"searchString":"","objectType":"CUSTOM_FIELD","fieldTypes":[],"projectTypes":[],"projectCategories":{"includeNoCategory":"false","categories":[]},"projectLeadKeys":[],"searchRequestsFilter":{"ownersKeys":[],"accessModes":[]}}
    # headers = {'content-type': 'application/json'}
    # r = locust.post('/rest/power-admin/1.0/search', json=searchBody, headers=headers, catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'data' not in content:
    #     logger.error(f"'data' was not found in {content}")
    # assert 'data' in content

    # hLocation = r.headers['Location'].split("aws.com")[1]

    # r = locust.get(hLocation, catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'progress' not in content:
    #     logger.error(f"'progress' was not found in {content}")
    # assert 'progress' in content

    # r = locust.get('/rest/power-admin/1.0/usage/header?type=CUSTOM_FIELD&id=customfield_10727', catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'customfield_10727' not in content:
    #     logger.error(f"'customfield_10727' was not found in {content}")
    # assert 'customfield_10727' in content

    # usageBody = {"objectType":"CUSTOM_FIELD","id":"customfield_10727"}
    # r = locust.post('/rest/power-admin/1.0/usage', json=usageBody, headers=headers, catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'data' not in content:
    #     logger.error(f"'data' was not found in {content}")
    # assert 'data' in content

    # hLocation = r.headers['Location'].split("aws.com")[1]

    # r = locust.get(hLocation, catch_response=True)
    # content = r.content.decode('utf-8')

    # if 'progress' not in content:
    #     logger.error(f"'progress' was not found in {content}")
    # assert 'progress' in content

    # IM stuff below
    # r = locust.get('/browse/AAAA-6', catch_response=True, auth=("admin", "admin"))
    # content = r.content.decode('utf-8')
    # if 'Sub Tasks Matrix' not in content:
    #     logger.error(f"'Sub Tasks Matrix' was not found in {content}")
    # assert 'Sub Tasks Matrix' in content

    # r = locust.get('/browse/AAAA-5', catch_response=True, auth=("admin", "admin"))
    # content = r.content.decode('utf-8')
    # if 'Sub Tasks Matrix' not in content:
    #     logger.error(f"'Sub Tasks Matrix' was not found in {content}")
    # assert 'Sub Tasks Matrix' in content
    # if 'Link Matrix' not in content:
    #     logger.error(f"'Link Matrix' was not found in {content}")
    # assert 'Link Matrix' in content

    # r = locust.get('/rest/api/2/search?jql=issue%20in%20issueMatrix(%22AAAA-6%22%2C%20%22Sub%20Tasks%20Matrix%22)', catch_response=True, auth=("admin", "admin"))
    # content = r.content.decode('utf-8')
    # if 'AAAA-9' not in content:
    #     logger.error(f"'AAAA-9' was not found in {content}")
    # assert 'AAAA-9' in content
    # if 'AAAA-8' not in content:
    #     logger.error(f"'AAAA-8' was not found in {content}")
    # assert 'AAAA-8' in content
    # if 'AAAA-7' not in content:
    #     logger.error(f"'AAAA-7' was not found in {content}")
    # assert 'AAAA-7' in content

    # ICJ stuff below
    # r = locust.get('/secure/ConfigurationIntegrityCheck.jspa#system', catch_response=True, auth=("admin", "admin"))
    # content = r.content.decode('utf-8')   # decode response content

    # if 'Configuration Integrity Check' not in content:
    #     logger.error(f"'Configuration Integrity Check' was not found in {content}")
    # assert 'Configuration Integrity Check' in content

    # checkBody = {"name":"","projectKeys":"","description":"","type":"system","isScoped":"false","includeAllFilters":"false","includeAllBoards":"false","includeAllDashboards":"false","includeProjectFilters":"false","includeProjectBoards":"false"}
    # # ceckBody = {"scope" : "system"}
    # headers = {'content-type': 'application/json'}
    # r = locust.post('/rest/integrity-check/1.0/integrity', json=checkBody, headers=headers, catch_response=True)

    # hLocation = r.headers['Location'].split("aws.com")[1]

    # try:
    #     r = locust.get(hLocation, catch_response=True)
    #     logger.info(f"Successful GET for job {hLocation}")

    #     content = r.content.decode('utf-8')
    #     if 'Integrity' not in content:
    #         logger.error(f"'Integrity ' was not found in {content}")
    #     assert 'Integrity' in content
    # except:
    #     logger.info(f"Skipped GET due to running job")

    # example below
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
