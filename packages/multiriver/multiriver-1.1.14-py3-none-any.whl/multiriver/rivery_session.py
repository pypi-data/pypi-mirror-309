import logging
import zlib
from faulthandler import is_enabled

import requests
from bson import json_util
import json
from . import utils

MAX_PULL_TIME = 1800
SLEEP_PULL_TIME = 5
REQUEST_CONNECT_TIMEOUT = 20
REQUEST_READ_TIMEOUT = 180
DEFAULT_HOST = "https://console.rivery.io"

LOGIC_STEP_BODY = """
 {
                "nodes": [],
                "hash_key_init": "KiPr2SHvuIYNHUKB21Rjk",
                "container_running": "run_once",
                "isEnabled": true,
                "isParallel": false,
                "step_name": "{logic_step_name}",
                "content": {
                  "sql_query": "",
                  "connection_id": {},
                  "drop_after": false,
                  "target_type": "table",
                  "file_type": "csv",
                  "block_type": "river",
                  "block_primary_type": "river",
                  "block_db_type": "river",
                  "compression": "none",
                  "split_tables": "no",
                  "split_interval": "d",
                  "target_loading": "append",
                  "target_table": "",
                  "fields": [],
                  "river_id": {
                    "$oid": "{river_id}"
                  }
                }
              }

"""
LOGIC_RIVER_BODY =""" {
  "river_definitions": {
    "shared_params": {
      "notifications": {
        "on_failure": {
          "email": "{Mail_Alert_Group}"
        },
        "on_warning": {
          "email": "{Mail_Alert_Group}"
        },
        "on_run_threshold": {
          "email": "{Mail_Alert_Group}"
        }
      },
      "fz_connection": {}
    },
    "river_name": "{river_name}",
    "river_type": "logic",
    "group_id": {
      "_id": {
        "$oid": "{group_id}"
      }
    }
  },
  "tasks_definitions": [
    {
      "task_label": "logic",
      "task_config": {
        "logic_steps": [
          {
            "nodes": {logic_steps},
            "hash_key_init": "a-swFp3ZMc4G3rix41BqO",
            "container_running": "run_once",
            "isEnabled": true,
            "isParallel": true,
            "step_name": "Container 0"
          }
        ],
        "condition_name_counter": 0,
        "step_name_counter": 1,
        "variables": {},
        "fz_batched": true,
        "container_name_counter": 0,
        "datasource_id": "logic"
      },
      "task_type_id": "logic",
      "schedule": {
        "endDate": {},
        "isEnabled": {is_enabled},
        "sched": {
          "hour": 11,
          "min": 16,
          "showCrontab": false,
          "days": {
            "days": 1
          },
          "month": {
            "radioMon": 0,
            "months": 1,
            "days": 1,
            "month": 1
          },
          "hours": {
            "hours": 1,
            "radioHour": 0
          },
          "year": {
            "radioYear": 0,
            "days": 1
          },
          "minutes": 15
        },
        "cronExp": "{cron_schedule}"
      },
      "connection_id": {},
      "is_synchronized": true
    }
  ]
}"""


class RiverySession:
    """
    Support class to work with the Rivery API
    """

    CONNECTION_TYPES = set()

    def __init__(self, *args, **kwargs):
        self.session = requests.session()
        self.access_token = kwargs.get('token') or kwargs.get('access_token')
        self.account_id = None
        self.env_id = None
        self.host = kwargs.get("host") or DEFAULT_HOST
        print(f'Host: {self.host}')
        self.api_host =  self.host + "/api"

    def __repr__(self):
        return f"<RiverySession host:{self.api_host}>"

    def __str__(self):
        return f"<RiverySession host:{self.api_host}>"

    @property
    def headers(self):
        return {"Authorization": f'Bearer {self.access_token}'}

    def connect(self):
        """ Make a connection test """
        url = '/me'
        resp = self.handle_request(url=url)
        self.account_id = resp.get('account_id')
        self.env_id = resp.get('environment_id')

    @property
    def account(self):
        """ Set the account id in cli for the session, as come from the token """
        return self.account_id

    @property
    def environment_id(self):
        return self.env_id

    def send_request(self, url, method=None, params=None, headers=None, data=None, **kwargs):
        logging.debug("Send request started")
        logging.debug(f"sending {method} request to {url} with params {params}, headers: {headers} and data: {data}")
        headers.update(self.headers)
        try:
            timeout = (REQUEST_CONNECT_TIMEOUT, REQUEST_READ_TIMEOUT)
            if data:
                data = zlib.compress(json_util.dumps(data).encode("utf-8")) if headers.get("Content-Encoding",
                                                                                           "") == "gzip" else \
                    json_util.dumps(data)
            if method.lower() == "post":
                response = self.session.post(url=url, params=params, timeout=timeout, data=data, headers=headers)
                return response

            if method.lower() == "get":
                response = self.session.get(url=url, params=params, headers=headers, timeout=timeout)
                return response

            if method.lower() == "delete":
                response = self.session.delete(url=url, params=params, data=data, headers=headers, timeout=timeout)
                return response

            if method.lower() == "patch":
                response = self.session.patch(url=url, data=data, params=params, headers=headers, timeout=timeout)
                return response

            if method.lower() == "put":
                response = self.session.put(url=url, data=data, params=params, headers=headers, timeout=timeout)
                return response

        except Exception as e:
            logging.error("Got an error from the API with: {}".format(str(e)))
            raise e

    def handle_request(self, url, method='get', params=None, headers=None, **kwargs):
        if headers is None:
            headers = {}
        logging.debug('handle_request started')

        resp = self.send_request(url=self.api_host + url, method=method, params=params, headers=headers, **kwargs)
        if resp.ok:
            if kwargs.get("return_full_response", False):
                return resp
            else:
                try:
                    return json_util.loads(resp.content)
                except Exception as e:
                    raise requests.HTTPError("Failed")

        elif not resp.ok and resp.content:
            try:
                error_msg = json_util.loads(resp.content)
            except Exception as e:
                error_msg = resp.content
                pass
            logging.error("Error from Rivery API: {}-{}".format(resp.status_code, error_msg))
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", "")
            if 400 <= resp.status_code < 500:
                raise Exception(
                    "Permissions Error in Rivery API "
                    "Please check your credentials and permissions. API Error: {}".format(error_msg))
            elif resp.status_code >= 500:
                raise requests.HTTPError("Internal server error, "
                                         "see following error and try again later. API Error: {}".format(error_msg))
            else:
                raise Exception(
                    "Unknown error from Rivery API")
        else:
            logging.error("Received an error from Rivery API")
            raise Exception("Received an error from Rivery API")

    def list_rivers(self, **params):
        """ List the rivers """
        url_ = '/rivers'
        river_id = params.pop('river_id', None)
        if river_id:
            url_ = f'/rivers/{river_id}'
        return self.handle_request(url=url_, method='get', params=params)

    def get_river(self, **kwargs):
        """ Get specific river data """
        url = '/rivers/list'
        data = {"_id": kwargs.get('river_id') or kwargs.get('_id')}
        method = 'post'
        return self.handle_request(url=url, data=data, method=method)

    def get_river_groups(self):
        """ Get specific river data """
        url = '/river_groups'
        method = 'get'
        return self.handle_request(url=url, method=method)

    def generate_mapping(self, river_id, **kwargs):
        data = kwargs.get('data', {})

        payload = {
            "river_definitions": data.get("river_definitions"),
            "tasks_definitions": data.get("tasks_definitions"),
            "cross_id": {"$oid": river_id},
            "_id": {"$oid": river_id}
        }
        url = "/mapping"

        start_mapping_response =self.handle_request(url=url, data=payload, method="put")
        start_mapping_response = utils.process_data(start_mapping_response, convert_to_oi=['_id'], to_delete=['request_status'])
        return start_mapping_response


    def pull_river_mapping(self, mapping_data):
        url = "/mapping"

        response =self.handle_request(url=url, data=mapping_data, method="post")

        # payload['tasks_definitions'][1]['task_config']["file_columns"] = response['mapping']['target']
        # payload['tasks_definitions'][1]['task_config']["source_mapping"] = response['mapping']['source']
        # river = self.save_river(river_id=river_id, data=payload)
        return response.get('mapping'), response.get('errors') or response.get('error_msg')

    def save_river(self, **kwargs):
        """ Save a new river, or update one
            :param create_new: Force new river with the specification of the data.
            :param river_definition: The River's definition
            :param files_to_upload: A list of files to upload to S3 (code scripts for Logic steps)
        """
        data = kwargs.get('data', {})

        payload = data

        url = "/rivers/modify"
        if kwargs.get("create_new", False) or not data.get('cross_id'):
            logging.debug('Creating New River: {}({})'.format(
                data.get('river_definitions', {}).get('river_name'), data.get('cross_id')))
            method = "put"
        else:
            method = "patch"
            logging.debug('Checking out if the river {}({}) exists in the account and environment'.format(
                data.get('river_definitions', {}).get('river_name'), data.get('cross_id')
            ))
            exists = self.handle_request(url='/rivers/list', data={"_id": data.get('cross_id')},
                                         method='post')
            if not exists:
                logging.debug('river {}({}) does not exist. Create it. '.format(
                    data.get('river_definitions', {}).get('river_name'), data.get('cross_id')
                ))
                method = 'put'

        files_to_upload = kwargs.get('files_to_upload')
        if files_to_upload:
            logging.debug("Uploading all code script to S3")
            for file in files_to_upload:
                for file_name, full_file_path in file.items():
                    self.upload_file_to_pre_signed_url(python_file_name=file_name, full_file_path=full_file_path)

        logging.debug(
            'Saving River {}({}). Creating New? {}'.format(data.get('river_definitions', {}).get('river_name'),
                                                           data.get('cross_id'),
                                                           True if method == 'put' else False))
        return self.handle_request(url=url, method=method, data=payload)

    def delete_river(self, **kwargs):
        """ Delete a river"""
        data = kwargs.get("data")
        params = kwargs.get("params")
        url = "/rivers/modify"
        method = "delete"
        return self.handle_request(url=url, method=method, data=data, params=params)

    def create_logic_river(self, river_ids, group_id, logic_river_name, cron_schedule=None, **kwargs):
        """ Create a logic river """
        url = "/rivers/modify"
        method = "put"
        logs_steps = []
        for river_id in river_ids:
            logs_steps.append(
                json.loads(utils.liberal_format(LOGIC_STEP_BODY, logic_step_name=logic_river_name, river_id=river_id))
            )

        logic_river_body = utils.liberal_format(LOGIC_RIVER_BODY, river_name=f"Logic River {group_id}",
                                                group_id=group_id, logic_steps=json.dumps(logs_steps),
                                                is_enabled="true" if cron_schedule else "false",
                                                cron_schedule=cron_schedule or "0 0/5 * * * * *")

        return self.handle_request(url=url, method=method, data=json.loads(logic_river_body))


if __name__ == '__main__':
    api_token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MjA0NjcyMTA2MSwiaWF0IjoxNzMxMzYxMDYxfQ.eyJhY2MiOiI2MmIwNzVkMjRjODZiMTAwMTBkZGY0NzAiLCJzY29wZXMiOnsiNjJiMDc1ZDM0Yzg2YjEwMDEwZGRmNDczIjpbInJpdmVyOmV4ZWN1dGUiLCJyaXZlcjpsaXN0IiwibWU6bGlzdCIsImRhdGFzb3VyY2U6bGlzdCIsImFjdGl2aXR5Omxpc3QiLCJhY3Rpdml0eTpsb2ciLCJkYXRhZnJhbWU6bGlzdCIsImRhdGFmcmFtZTp3cml0ZSIsImRhdGFmcmFtZTpkZWxldGUiLCJkYXRhX3F1YWxpdHlfdGVzdDpsaXN0IiwiZGF0YV9xdWFsaXR5X3Rlc3Q6d3JpdGUiLCJsb2dpY29kZTpsaXN0Iiwib3BlcmF0aW9uczpsaXN0IiwiZW52aXJvbm1lbnQ6bGlzdCIsImFjY291bnQ6bGlzdCIsImNvbm5lY3Rpb246bGlzdCIsImNvbm5lY3Rpb246ZWRpdCIsImNvbm5lY3Rpb246ZGVsZXRlIiwiY29ubmVjdGlvbjp0ZXN0Iiwicml2ZXI6ZWRpdCIsInJpdmVyOmRlbGV0ZSIsImZpbGU6ZWRpdCIsInJpdmVyOndyaXRlIiwicGxhbjpsaXN0IiwiYXVkaXQ6bGlzdCIsInVzZXI6bGlzdCIsInVzZXI6ZWRpdCIsInRlYW06bGlzdCIsInRlYW06d3JpdGUiLCJ2YXJpYWJsZXM6ZWRpdCIsInZhcmlhYmxlczpsaXN0IiwiYWNjb3VudDp3cml0ZSIsImdyb3VwOmxpc3QiXX0sInRva2VuX25hbWUiOiJuZXciLCJpc3MiOiI2MTVjMDdiYzczYjRlMTAwMWRkYWExNjkiLCJqdGkiOiIwOTZhNDZmOTQ2N2U0MGEzYTRhMWU2OTI4NTAxODY2MSIsImVudiI6IjYyYjA3NWQzNGM4NmIxMDAxMGRkZjQ3MyIsInN1YiI6IlJpdmVyeSBBUEkifQ.rcRwBAJfRDEDWnw2yndxGvblDES7xOlWKRPdxRPMPls'
    rivery_session = RiverySession(token=api_token)
    # value = rivery_session.get_river(
    #     **{"river_id": "672382b667752a2ed39a46ac"})
    # rivery_session.delete_river(data={"_id":"672b78809c783e0778ed32dd"})
    # value = utils.process_data(
    #     value,
    #     convert_to_oi=['connection_id', 'fz_connection', 'env_id', 'cross_id', 'account', 'created_by', 'env_id', 'version_id', 'updated_by'],
    #     to_date=['start_date', 'task_date_updated'],
    # )
    # rivery_session.generate_mapping(river_id="672382b667752a2ed39a46ac", data=value)

    # group_id = '63580e783a26fa000fd90c50'
    # [g for g in all_groups.get('groups') if g['_id'] == '672b58759c783e0778ed318f']
    # rivery_session.list_rivers(group_id='672b58759c783e0778ed318f')
    rivery_session.create_logic_river(group_id='6720e1592f775cb9fcdbf026', river_ids=[
        '67327c56563c1a406a6f8671',
        '67327c53563c1a406a6f8662'
    ],
    cron_schedule="0 0/5 * 1/1 * ? *"
)
    pass