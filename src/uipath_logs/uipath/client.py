import requests
import json
import sys
import pytz


class AuthenticationError(Exception):
    pass


class UiPathBaseClient:
    def get_jobs(self, from_datetime, to_datetime=None):
        self.headers.pop('X-UIPATH-OrganizationUnitId', None)
        print(self.headers)
        return self.get_data_from_uipath('Jobs', from_datetime, to_datetime)

    def get_processes_schedules(self, folder_id):
        self.headers['X-UIPATH-OrganizationUnitId'] = str(folder_id)
        return self.get_data_from_uipath('ProcessSchedules', None)

    def get_folders(self):
        return self.get_data_from_uipath('Folders', None)

    def get_data_from_uipath(self, type, from_datetime, to_datetime=None):
        url = f'{self.base_url}odata/{type}'
        if self.base_url[-1] != '/':
            url = f'{self.base_url}/odata/{type}'
        params = {}

        if from_datetime:
            from_datetime_iso = str(from_datetime.astimezone(
                tz=pytz.utc)).replace('+00:00', 'Z').replace(' ', 'T')
            filter = f'StartTime gt {from_datetime_iso}'
            if to_datetime != None:
                to_datetime_iso = str(to_datetime.astimezone(tz=pytz.utc)).replace(
                    '+00:00', 'Z').replace(' ', 'T')
                filter += f' and StartTime lt {to_datetime_iso}'

            params = {
                '$filter': filter,
                '$orderby': 'StartTime',
            }

        r = requests.get(url, headers=self.headers,
                         params=params, verify=True)
        print(r, url, params)
        return r


class OnPremisseClient(UiPathBaseClient):
    def __init__(self, config):
        # commom
        self.base_url = config['url']

        try:
            self.tenant_name = config['tenant_name']
        except KeyError:
            self.tenant_name = 'Default'

        self.credentials = {
            "tenancyName": self.tenant_name,
            "usernameOrEmailAddress": config['usernameOrEmailAddress'],
            "password": config['password'],
        }

    def authenticate(self):
        print("Authenticating...")
        url = '%s/api/Account/Authenticate' % self.base_url

        headers = {
            'Content-Type':       'application/json',
            'X-UIPATH-TenantName': self.tenant_name,
        }

        try:
            r = requests.post(url,
                              headers=headers,
                              data=json.dumps(self.credentials),
                              verify=True)
        except requests.ConnectionError:
            print('Connection error with orchestrator, verify your network')
            return sys.exit(2)

        if r.status_code == 200:
            token = r.json()['result']
            self.headers = {'Content-Type': 'application/json',
                            'Authorization': 'Bearer %s' % token}
            return
        raise AuthenticationError


class CloudClient(UiPathBaseClient):
    def __init__(self, config):
        # commom
        self.base_url = config['url']
        self.tenant_name = config['tenant_name']

        self.credentials = {
            "grant_type": 'refresh_token',
            "refresh_token": config['refresh_token'],
            "client_id": config['client_id'],
        }

    def authenticate(self):
        print("Authenticating...")

        url = 'https://account.uipath.com/oauth/token'

        headers = {
            'Content-Type':       'application/json',
            'X-UIPATH-TenantName': self.tenant_name,
        }

        try:
            r = requests.post(url,
                              headers=headers,
                              data=json.dumps(self.credentials),
                              verify=True
                              )
        except requests.ConnectionError:
            print('Connection error with orchestrator, verify your network')
            return sys.exit(2)

        if r.status_code == 200:
            print('AUTHENTICATED')
            token = r.json()['access_token']
            self.headers = {'Content-Type': 'application/json',
                            'X-UIPATH-TenantName': self.tenant_name,
                            'Authorization': 'Bearer %s' % token}
            return
        raise AuthenticationError(r)
