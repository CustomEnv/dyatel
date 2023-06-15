import json
import time

from selenium.webdriver.chromium.webdriver import ChromiumDriver


class CDPManager:
    def __init__(self, driver: ChromiumDriver):
        self.driver = driver

    def enable_intercept(self, url_pattern):
        self.driver.execute_cdp_cmd('Fetch.enable', {'patterns': [{'urlPattern': f'*{url_pattern}'}]})

    def request_paused(self, url_path):
        data = self.get_request_data(url_path)['params']
        self.driver.execute_cdp_cmd('Fetch.requestPaused', {'requestId': data['requestId'], 'request': data['request'], 'frameId': data['frameId'], 'ResourceType': 'Document'})

    def mock_response(self, url_pattern):
        data = self.driver.get_log('performance')
        breakpoint()
        self.driver.execute_cdp_cmd('Fetch.continueRequest', {'requestId': '33DDEBAD4B0C4BF9F8F5A13169BD0759'})
        self.driver.execute_cdp_cmd('Fetch.fulfillRequest', {'requestId': self.get_request_id(url_pattern), 'responseCode': 200, 'body': 'data'})

    def get_response(self, url_pattern):
        return self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': self.get_request_id(url_pattern)})

    def get_logs(self, log_type='performance'):
        return [json.loads(x['message'])['message'] for x in self.driver.get_log(log_type)] if log_type in self.driver.log_types else []

    def get_request_data(self, url_pattern):
        time.sleep(3)
        data = self.get_logs()
        for request in data:
            if url_pattern in request['params'].get('request', {}).get('url', ''):
                return request

    def get_request_id(self, url_pattern):
        return self.get_request_data(url_pattern)["params"]["requestId"]
