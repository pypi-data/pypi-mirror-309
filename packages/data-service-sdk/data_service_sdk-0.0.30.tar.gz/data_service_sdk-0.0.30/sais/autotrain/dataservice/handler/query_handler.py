import json
import os
import time

import pandas as pd
import requests
from loguru import logger
from typing import Union
from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
from sais.autotrain.dataservice.client.mongo_client import query_nwp_mongo, query_nwp_meta_info, query_nwp_mongo_biz
from sais.autotrain.dataservice.config.const import ENDPOINT
from sais.autotrain.dataservice.model.data_model import Task, StatusEnum, QueryNWPRequest, QueryNWPBizRequest, \
    QueryStationRequest, \
    QueryObservationRequest, BaseRsp, BizResponse, QueryAreaRequest
from sais.autotrain.dataservice.types.biz_exception import BizException
from sais.autotrain.dataservice.config.mongo_config import mongo_config


class QueryNWPHandler(object):
    def __init__(self, endpoint=os.getenv("ENDPOINT", ENDPOINT), auth_provider: EnvVarCredentialsProvider = None,
                 mongo_host=None, mongo_port=None, mongo_user=None, mongo_password=None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider
        if mongo_host and mongo_port and mongo_user and mongo_password:
            mongo_config.set_config(host=mongo_host, port=mongo_port, user=mongo_user, password=mongo_password)

    def submit_query_task(self, query: QueryNWPRequest):
        """提交查询任务并返回任务ID"""
        url = f"{self.endpoint}/api/v1/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query task submitted successfully. Task ID: {query_result_json.get('data').get('task_id')}")
            return query_result_json.get('data').get('task_id')
        else:
            logger.error(f"Failed to submit query task. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query task.")

    def query_task_status(self, task_id):
        """通过任务ID查询任务状态"""
        url = f"{self.endpoint}/api/v1/query/{task_id}"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}"
        }
        response = requests.get(url, headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            logger.info(f"Query task status: {query_result_json.get('data')}")
            return Task(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to query task status. Response: {query_result_json}")
            raise ValueError(f"Failed to query task status.{query_result_json.get('msg')}")

    def wait_for_task_completion(self, task_id, poll_interval=5):
        """
        轮询查询任务状态直到任务完成
        状态：
            - PENDING: 等待执行
            - RUNNING: 执行中
            - FINISHED: 完成（已成功生成json文件）
            - FAILED: 失败
        """
        while True:
            task = self.query_task_status(task_id)
            if task.status == StatusEnum.FINISHED:
                if os.path.exists(task.file_path):
                    with open(task.file_path, 'r') as file:
                        return json.load(file)
                else:
                    return None
            elif task.status == StatusEnum.FAILED:
                raise Exception(f"Query task failed. Task ID: {task.task_id}")
            time.sleep(poll_interval)  # 轮询间隔

    def execute_query_mongo(self, query_params: Union[QueryNWPRequest, QueryNWPBizRequest]):
        if isinstance(query_params, QueryNWPRequest):
            return query_nwp_mongo(query_params.src, query_params.start_time, query_params.period_interval,
                                   query_params.period,
                                   query_params.start_hour,
                                   query_params.end_hour,
                                   query_params.forecast_interval,
                                   query_params.coords,
                                   query_params.vars,
                                   query_params.workers)
        elif isinstance(query_params, QueryNWPBizRequest):
            return query_nwp_mongo_biz(query_params.src, query_params.start_time, query_params.ndays,
                                       query_params.hours,
                                       query_params.coords,
                                       query_params.vars,
                                       query_params.workers)
        else:
            raise TypeError("Unsupported query parameters type")

    def execute_query(self, query_params: Union[QueryNWPRequest, QueryNWPBizRequest]):
        if query_params.engine == "mongo":
            try:
                result = BizResponse(data=self.execute_query_mongo(query_params))
            except BizException as biz_err:
                result = BizResponse(code=biz_err.code, msg=biz_err.msg)
            except Exception as e:
                result = BizResponse(code=1, msg=str(e))
            return result
        else:
            """封装的查询功能函数，提交查询任务并轮询直到返回任务状态结果"""
            task_id = self.submit_query_task(query_params)
            print(f"Query task submitted with task ID: {task_id}")
            return self.wait_for_task_completion(task_id)

    def query_nwp_meta(self, src):
        """获取nwp数据源的元数据"""
        try:
            result = BizResponse(data=query_nwp_meta_info(src))
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result


class QueryStationRelatedHandler(object):
    def __init__(self, endpoint=ENDPOINT, auth_provider: EnvVarCredentialsProvider = None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def execute_query_area(self, query_params):
        """场站查询"""
        try:
            area_data = self.submit_query_area(query_params)
            result = BizResponse(code=0, data=area_data)
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result

    def execute_query_station(self, query_params):
        """场站查询"""
        try:
            station_data = self.submit_query_station(query_params)
            result = BizResponse(code=0, data=station_data)
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result

    def execute_query_observation(self, query_params):
        """观测查询"""
        try:
            observation_data = self.submit_query_observation(query_params)
            result = BizResponse(code=0, data=observation_data)
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result

    def execute_label_observation(self, df: pd.DataFrame):
        """标记观测查询"""
        try:
            update_result = self.submit_label_observation(df)
            result = BizResponse(code=0, data=update_result)
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result

    def submit_query_observation(self, query: QueryObservationRequest):
        """提交观测查询"""
        url = f"{self.endpoint}/api/v1/observation/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query observation. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query observation.{query_result_json.get('msg')}")

    def submit_query_area(self, query: QueryAreaRequest):
        """提交省份或区域查询"""
        url = f"{self.endpoint}/api/v1/area/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query area. Response: {query_result_json}")
            raise ValueError(f"Failed to submit area station.{query_result_json.get('msg')}")

    def submit_query_station(self, query: QueryStationRequest):
        """提交场站查询"""
        url = f"{self.endpoint}/api/v1/station/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query station. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query station.{query_result_json.get('msg')}")

    def submit_label_observation(self, df: pd.DataFrame):
        """提交标记观测数据"""
        url = f"{self.endpoint}/api/v1/observation/label"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        data = {
            "observations": df.to_dict(orient='records')
        }
        response = requests.post(url, json=data, headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            return True
        else:
            logger.error(f"Failed to submit label observation. Response: {query_result_json}")
            return False
