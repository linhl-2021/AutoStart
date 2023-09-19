import enum
import json
import requests
import urllib3
import time
import unittest
import sys
from log_module import logger
from demo import login_web

instanceType = None
# ntos_page = f"https://172.28.247.83"
ntos_page = f"https://172.28.247.85"
login_api = f"{ntos_page}/api/v1/login/"
version_api = "/api/v1/feature_library/getData/"
upload_api = "/api/v1/upload/"
upgrade_api = "/api/v1/feature_library/localUpgrade/"
query_upgrade_api = "/api/v1/feature_library/localUpgradeRes/"
res=login_web(login_api,ntos_page)
sessionid=res["session_id"]
csrftoken=res["csrftoken"]
cookie = f"csrftoken={csrftoken};sessionid={sessionid}"
headers = {
    "cookie": cookie,
    "X-CSRFToken": csrftoken,
    "Referer": ntos_page
}


def get_page(api: str) -> requests.Response:
    return requests.get(ntos_page + api,
                        headers=headers,
                        verify=False)


def post_file(api: str, filename) -> requests.Response:
    with open(filename, "rb") as f:
        ret = requests.post(ntos_page + api,
                            headers=headers,
                            verify=False,
                            files={"file": f})
    return ret


def post_json(api: str, form_data: dict) -> requests.Response:
    return requests.post(ntos_page + api,
                         headers=headers,
                         verify=False,
                         json=form_data)



class UpdateTest:
    class UpdateType(enum.Enum):
        IPS = enum.auto()
        AppId = enum.auto()

    class UpdateState(enum.IntEnum):
        ing = 1

    def __init__(self, sig_type: UpdateType):
        urllib3.disable_warnings()
        self.update_id = 0
        self.current_version = 0
        self.sig_type = sig_type    
        self.upload_api = upload_api
        if sig_type == self.UpdateType.IPS:
            self.type_name = "ips"
            self.upload_api += "4/"

        if sig_type == self.UpdateType.AppId:
            self.type_name = "app-identify"
            self.upload_api += "6/"

    def _parse_version(self, resp):
        res_d = json.loads(resp.text)
        res_data = res_d['data']
        for i in res_data['list']:
            if i['type'] == self.type_name:
                return i['current-version']
        raise Exception(f"Cannot get {self.type_name} current version")

    def get_current_version(self):
        res = get_page(version_api)
        self.current_version = str(self._parse_version(res))
        return self.current_version

    def update(self, filepath, filename):
        print(f"{self.type_name} current version: {self.get_current_version()}")
        print(f"{self.type_name} upload {filename}")
        res = post_file(self.upload_api, filepath)
        try:
            res_json = json.loads(res.text)
            if int(res_json['code']) != 20000:
                raise Exception("ret code != 20000")
        except:
            raise Exception(f"Cannot upload file {filename}, res={res.text}")
        print(f"upload done")

        res = post_json(upgrade_api, {
            'type': self.type_name,
            'fileName': filename
        })
        try:
            res_json = json.loads(res.text)
            if int(res_json['code']) != 20000:
                raise Exception("ret code != 20000")
            self.update_id = int(res_json['data']['id'])
        except:
            raise Exception(f"Cannot do local upgrade, res={res.text}")
        print(f"start to do local update, id={self.update_id}")

    def get_update_state(self) -> int:
        res = post_json(query_upgrade_api, {
            'id': self.update_id,
            'type': self.type_name
        })
        print(res.json())
        try:
            res_json = json.loads(res.text)
            if int(res_json['code']) != 20000:
                raise Exception("ret code != 20000")
            return int(res_json['data']['errnum'])
        except:
            raise Exception(f"Cannot do local upgrade, res={res.text}")


class SigUpdateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = UpdateTest(instanceType)

    def test_update(self):
        print()
        filepath = str(sys.argv[2])    
        filename = str(filepath.split("/")[-1])
        self.instance.update(filepath, filename)
        while True:
            state = self.instance.get_update_state()
            if state == self.instance.UpdateState.ing.value:
                time.sleep(5)
                continue
            print(f"current version: {self.instance.get_current_version()}")
            break
        
 

class Test(SigUpdateTest):
    def __init__(self, a):
        super(Test, self).__init__(a)
        global instanceType
        L7_type = str(sys.argv[1]) 
        #L7_ipFile = str(sys.argv[3])
        #print(f"文件内容: {L7_ipFile}")
        if L7_type == "ips":
            instanceType = UpdateTest.UpdateType.IPS
        elif L7_type == "appid":
            instanceType = UpdateTest.UpdateType.AppId
        else:
            exit(0)


if __name__ == '__main__':
        logger.info("1111")
        ips_suite = unittest.TestSuite()
        logger.info("1111")

        ips_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test))
        logger.info("1111")
        ips_runner = unittest.TextTestRunner(verbosity=2)
        logger.info("1111")
        
        ips_res = ips_runner.run(ips_suite)
        logger.info("1111")
