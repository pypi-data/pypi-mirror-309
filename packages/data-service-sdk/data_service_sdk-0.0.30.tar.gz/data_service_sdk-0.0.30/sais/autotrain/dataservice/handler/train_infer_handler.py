import json
import logging
import os
import time

import requests

from sais.autotrain.dataservice.auth.auth_info import EnvVarCredentialsProvider
from sais.autotrain.dataservice.config.const import LOGGER_NAME, ENDPOINT
from loguru import logger
from sais.autotrain.dataservice.model.data_model import Task, StatusEnum, QueryNWPRequest, QueryStationRequest, \
    QueryObservationRequest, BaseRsp, BizResponse
from sais.autotrain.dataservice.model.train_infer_model import TrainResultRequest, InferResultRequest, QueryInferRequest
from sais.autotrain.dataservice.types.biz_exception import BizException


class TrainInferHandler(object):
    def __init__(self, endpoint=ENDPOINT, auth_provider: EnvVarCredentialsProvider = None):
        self.endpoint = endpoint
        self.auth_provider = auth_provider

    def execute_train_result_submit(self, result):
        """执行训练结果提交"""
        submit_result = self.submit_train_result(result)
        return submit_result

    def execute_infer_result_submit(self, result):
        """执行推理结果提交"""
        submit_result = self.submit_infer_result(result)
        return submit_result

    def submit_train_result(self, result: TrainResultRequest):
        """提交场站结果"""
        url = f"{self.endpoint}/api/v1/train/result"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=result.model_dump(by_alias=True, exclude_none=True), headers=headers)
        result_json = response.json()
        if result_json.get('success'):
            logger.info(f"Submit train result successfully.")
            return True
        else:
            logger.error(f"Failed to submit train result. Response: {result_json}")
            return False

    def submit_infer_result(self, result: InferResultRequest) -> bool:
        """提交推理结果"""
        url = f"{self.endpoint}/api/v1/infer/result"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=result.model_dump(by_alias=True, exclude_none=True), headers=headers)
        result_json = response.json()
        if result_json.get('success'):
            logger.info(f"Submit infer result successfully.")
            return True
        else:
            logger.error(f"Failed to submit infer result. Response: {result_json}")
            return False

    def execute_query_infer(self, query_params):
        """查询推理结果"""
        try:
            observation_data = self.submit_query_infer(query_params)
            result = BizResponse(code=0, data=observation_data)
        except BizException as biz_err:
            result = BizResponse(code=biz_err.code, msg=biz_err.msg)
        except Exception as e:
            result = BizResponse(code=1, msg=str(e))
        return result

    def submit_query_infer(self, query: QueryInferRequest):
        """提交观测查询"""
        url = f"{self.endpoint}/api/v1/infer/query"
        headers = {
            # "Authorization": f"Bearer {self.auth_provider.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=query.model_dump(by_alias=True, exclude_none=True), headers=headers)
        query_result_json = response.json()
        if query_result_json.get('success'):
            return BaseRsp(**query_result_json.get('data'))
        else:
            logger.error(f"Failed to submit query infer. Response: {query_result_json}")
            raise ValueError(f"Failed to submit query infer.{query_result_json.get('msg')}")