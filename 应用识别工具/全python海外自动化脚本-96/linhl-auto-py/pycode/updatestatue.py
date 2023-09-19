
import enum
import json
import os
import requests
import urllib3
import time
import sys
from log_module import logger
from demo import login_web



def run_update_test(sig_type: str, filepath: str,config):
    urllib3.disable_warnings()
    type_name=""
    filename = filepath.split("/")[-1]
    sig_type = sig_type    
    ntos_page = f"https://{config.firewalld_ip}"
    login_api = f"{ntos_page}/api/v1/login/"
    version_api = "/api/v1/feature_library/getData/"
    upload_api = "/api/v1/upload/"
    upgrade_api = "/api/v1/feature_library/localUpgrade/"
    query_upgrade_api = "/api/v1/feature_library/localUpgradeRes/"
    res = login_web(login_api,ntos_page,config.firewalld_web_user,config.firewalld_web_passwd)
    sessionid=res["session_id"]
    csrftoken=res["csrftoken"]
    cookie = f"csrftoken={csrftoken};sessionid={sessionid}"
    headers = {
        "cookie": cookie,
        "X-CSRFToken": csrftoken,
        "Referer": ntos_page
    }
    if sig_type == "ips":
        type_name = "ips"
        upload_api += "4/"
        instanceType=0
    elif sig_type == "appid":
        type_name = "app-identify"
        upload_api += "6/"
        instanceType=1

    # update_test = UpdateTest(instanceType)

    def _parse_version(resp):
        res_d = json.loads(resp.text)
        res_data = res_d['data']
        for i in res_data['list']:
            if i['type'] == type_name:
                return i['current-version']
        logger.debug(f"Cannot get {type_name} current version")

    def get_update_state(update_id):
        try:
            while True:
                res = requests.post(ntos_page + query_upgrade_api,
                                    headers=headers,
                                    verify=False,
                                    json={
                                        'id': update_id,
                                        'type': type_name
                                    })
                logger.debug(res.json())
                res_json = json.loads(res.text)
                if int(res_json['code']) != 20000:
                    logger.debug("ret code != 20000")
                if int(res_json['data']['errnum']) ==1:
                    time.sleep(5)
                    continue
                logger.debug(f"current version: {get_current_version()}")
                return   
                
        except:
            logger.debug(f"Cannot do local upgrade, res={res.text}")

    def get_current_version():
            res = requests.get(ntos_page + version_api,
                                headers=headers,
                                verify=False)
            current_version = str(_parse_version(res))
            return current_version

    def update():
            logger.debug(f"{type_name} current version: {get_current_version()}")
            logger.debug(f"{type_name} upload {filename}")
            with open(filepath, "rb") as f:
                ret = requests.post(ntos_page + upload_api,
                                    headers=headers,
                                    verify=False,
                                    files={"file": f})
                logger.debug(f"返回类型为： {type(ret)}")
            try:
                res_json = json.loads(ret.text)
                if int(res_json['code']) != 20000:
                    logger.debug("ret code != 20000")
            except:
                logger.debug(f"Cannot upload file {filename}, res={ret.text}")
            logger.debug(f"upload done")

            res = requests.post(ntos_page + upgrade_api,
                                headers=headers,
                                verify=False,
                                json={
                                    'type': type_name,
                                    'fileName': filename
                                })
            try:
                res_json = json.loads(res.text)
                if int(res_json['code']) != 20000:
                    logger.debug("ret code != 20000")
                update_id = int(res_json['data']['id'])
            except:
                logger.debug(f"Cannot do local upgrade, res={res.text}")
            logger.debug(f"start to do local update, id={update_id}")
            get_update_state(update_id)






    # while True:
    #     state = update_test.get_update_state()
    #     logger.debug("state: "+str(state))
    #     if state == update_test.UpdateState.ing.value:
    #         time.sleep(5)
    #         continue
    #     logger.debug(f"current version: {update_test.get_current_version()}")
    #     break
       


    msg=update()
    logger.debug("更新结束")
    return msg



    