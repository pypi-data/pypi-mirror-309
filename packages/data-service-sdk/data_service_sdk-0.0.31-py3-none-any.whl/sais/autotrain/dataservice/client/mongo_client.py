import concurrent
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from loguru import logger
from pymongo import MongoClient

from sais.autotrain.dataservice.config.const import DEBUG
from sais.autotrain.dataservice.model.data_model import Coordinate
from sais.autotrain.dataservice.types.biz_exception import BizException
from sais.autotrain.dataservice.config.mongo_config import mongo_config

import json

def query_nwp_mongo_biz(src: str, start_time: str, ndays: int, hours: int, coords: list[Coordinate], vars: list[str], workers: int):
    nwp_meta = query_nwp_meta_info(src)
    real_start_time = get_nearest_start_time(start_time, nwp_meta['times'].split(','))
    period_interval = 24
    period = ndays
    start_hour = calculate_hours_between(real_start_time, start_time)
    end_hour = (start_hour + hours) -1
    forecast_interval = 1
    return query_nwp_mongo(src, real_start_time, period_interval, period, start_hour, end_hour,
                           forecast_interval, coords, vars, workers, nwp_meta)
def query_nwp_mongo(src: str, start_time: str, period_interval: int, period: int, start_hour: int, end_hour: int,
                    forecast_interval: int, coords: list[Coordinate], vars: list[str], workers: int, nwp_meta: dict=None):
    if DEBUG:
        logger.debug(f'params: src: {src}, start_time: {start_time}, period_interval: {period_interval}, period: {period}, start_hour: {start_hour}, '
                     f'end_hour: {end_hour}, forecast_interval: {forecast_interval}, coords: {coords}, vars: {vars}, workers: {workers}')
    # 记录查询开始时间
    query_start_time = time.time()
    # 查询气象源元信息
    if not nwp_meta:
        nwp_meta = query_nwp_meta_info(src)
    # 解析请求参数
    start_time_dt = datetime.strptime(start_time, "%y%m%d%H")
    # 所有起报时间点
    forcast_start_times = []
    # 所有预报时间点
    forcast_times = []
    # 预报步长
    steps = []
    # forcast_time 按月分组
    month_groups = {}
    # 发布时次
    for i in range(period):
        forcast_start_time = start_time_dt + timedelta(hours=i * period_interval)
        # logger.info(f'forcast_start_time: {forcast_start_time}')
        forcast_start_time_str = forcast_start_time.strftime("%Y-%m-%d %H:%M:%S")
        forcast_start_times.append(forcast_start_time_str)
        # 记录到月分组中
        month_key = forcast_start_time.strftime('%Y%m')
        if month_key not in month_groups:
            month_groups[month_key] = []
        month_groups[month_key].append(forcast_start_time_str)

        for hour in range(start_hour, end_hour + 1, forecast_interval):
            current_step = timedelta(hours=hour)
            forcast_time = forcast_start_time + current_step
            # logger.info(f'forcast_time: {forcast_time}')
            forcast_times.append(forcast_time.strftime("%Y-%m-%d %H:%M:%S"))

            # 格式化时间步长
            formatted_step = f"P{current_step.days}DT{current_step.seconds // 3600}H{(current_step.seconds // 60) % 60}M{current_step.seconds % 60}S"
            steps.append(formatted_step)
    # logger.info(f'forcast_times: {forcast_times}')
    # logger.info(f'forcast_start_times: {forcast_start_times}')

    # 获取实际查询的格点
    mapping_coords = approximate_coordinates(coords, nwp_meta['grid'])
    support_steps = json.loads(nwp_meta['steps'])
    valid_steps = [step for step in steps if step in support_steps]
    # 查询气象源数据
    result = query_mongo_multi_thread(workers, nwp_meta, month_groups, valid_steps, vars, mapping_coords)
    current = time.time()  # 记录查询结束时间
    query_time = current - query_start_time
    logger.info(f"查询耗时: {query_time:.2f} 秒")
    # 结果后处理
    result = handle_result(src, start_time, period_interval, period, start_hour, end_hour,
                           forecast_interval, mapping_coords, vars, result)
    all_end_time = time.time()  # 记录查询结束时间
    all_execution_time = all_end_time - query_start_time
    check_result(vars, forcast_start_times, valid_steps, result, nwp_meta)
    logger.info(f"总耗时: {all_execution_time:.2f} 秒")
    return result


def handle_result(src: str, start_time: str, period_interval: int, period: int, start_hour: int, end_hour: int,
                  forecast_interval: int, mapping_coords: dict[tuple[float, float], Coordinate], vars: list[str], result):
    if not result or len(result) == 0:
        return result
    df = pd.DataFrame(result)
    df = df.drop_duplicates()
    df = df.sort_values(by=['src', 'time', 'valid_time']).reset_index(drop=True)
    # 按经纬度分组
    grouped = df.groupby(['latitude', 'longitude'])
    # 构建结果列表
    result_list = []
    for (lat, lon), group_df in grouped:
        coor = mapping_coords.get((lat, lon))
        meta = {
            'src': src,
            'start_time': start_time,
            'period_interval': period_interval,
            'period': period,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'forecast_interval': forecast_interval,
            'latitude': lat,
            'longitude': lon,
            'req_lat': coor.req_lat,
            'req_lon': coor.req_lon
        }
        # 构建 data 字典
        var_list_dict = {var: group_df[var].tolist() for var in vars}
        data = {
            # 'step': group_df['step'].tolist(),
            **var_list_dict
        }
        result_list.append({
            'meta': meta,
            'data': data
        })

    return result_list


def check_result(vars, forcast_start_times, steps, result, nwp_meta):
    """
    :param vars: 所有气候变量
    :param forcast_start_times: 所有预报开始时间点
    :param steps 所有steps未去重
    :param result: 预报结果
    :param nwp_meta: 气象源元信息
    :return:
    """
    start_time = datetime.strptime(nwp_meta['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(nwp_meta['end_time'], "%Y-%m-%d %H:%M:%S")

    # 筛选出在指定时间范围内的所有起报时间
    filtered_fc_start_times = [
        ft for ft in forcast_start_times
        if start_time <= datetime.strptime(ft, "%Y-%m-%d %H:%M:%S") <= end_time
    ]
    # 去重步长
    unique_steps = list(set(steps))
    if not result or len(result) == 0:
        raise BizException(code=1, msg="查询结果为空")
    for index, item_result in enumerate(result):
        if not item_result['data']:
            raise BizException(code=2, msg="预报数据为空")
        for var in vars:
            # 检查是否存在该变量的预报数据
            if var not in result[index]['data']:
                raise BizException(code=3, msg=f"预报数据不存在于查询结果中")
            # 检查是否存在该预报时间点的预报数据
            expect_len = len(filtered_fc_start_times) * len(unique_steps)
            real_len = len(result[index]['data'][var])
            if expect_len != real_len:
                raise BizException(code=4, msg=f"{var} 预报数据长度与预报时间点长度不一致, expect_len: {str(expect_len)}, real_len:{str(real_len)}")


def run_query(db: MongoClient, nwp_meta: dict, month_item: dict, forcast_times: list[str], steps: list[str], vars: list[str],
              mapping_coords: dict[tuple[float, float], Coordinate]):
    query_conditions = []

    # 获取近似经纬度
    rounded_coords = [
        {"req_lat": key[0], "req_lon": key[1]}
        for key in mapping_coords.keys()
    ]
    query_conditions.append({
        "src": nwp_meta['src'],
        "time": {"$in": forcast_times},
        "$or": [
            {"$and": [{"latitude": loc['req_lat']}, {"longitude": loc['req_lon']}]} for loc in rounded_coords
        ],
        "step": {"$in": steps},
        "$and": [{var: {"$exists": True}} for var in vars]
    })
    collection = get_collection(db, nwp_meta["prefix"], month_item)
    vars_dict = {key: 1 for key in vars}
    query = {"$and": query_conditions}
    if DEBUG:
        logger.info(f'query: {query_conditions}')
    # logger.info(f'query: {query_conditions}')
    query_results = collection.find(query, {
        "_id": 0,
        "src": 1,
        "time": 1,
        "valid_time": 1,
        "step": 1,
        "latitude": 1,
        "longitude": 1,
        **vars_dict
    }).sort({
        "time": 1,
        "step": 1
    })
    return list(query_results)


def query_mongo_multi_thread(workers, nwp_meta: dict, month_group: dict, steps: list[str], vars: list[str],
                             mapping_coords: dict[tuple[float, float], Coordinate]):
    # 并发查询
    all_results = []
    client = mongo_config.get_client()
    db = client[os.getenv("MONGO_DB", "auto_train")]
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_month = {
            executor.submit(run_query, db, nwp_meta, month_key, month_group[month_key], steps, vars, mapping_coords): month_key
            for month_key in month_group
        }
        for future in concurrent.futures.as_completed(future_to_month):
            month_key = future_to_month[future]
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as exc:
                print(f'Error for month {month_key}: {exc}')
    return all_results


def query_nwp_meta_info(src):
    """
    查询气象源元数据
    :param src: 气象源
    :return:
    """
    client = mongo_config.get_client()
    db = client[os.getenv("MONGO_DB", "auto_train")]
    meta_info = db["nwp_infos"].find_one({"src": src})
    if not meta_info:
        raise BizException(code=6, msg=f"未查询到{src}气象源元信息")
    meta_info['_id'] = str(meta_info['_id'])
    return meta_info


def get_collection(db, prefix, year_month):
    cname = f"{prefix}_{year_month}"
    if DEBUG:
        logger.info(f'collection name: {cname}')
    return db[cname]


def get_year_month(dt):
    year_month = dt.strftime("%Y%m")
    return year_month


def get_nearest_start_time(input_time_str, supported_hours):
    """
    获取与给定时刻最近（向前）的起报时间。

    参数:
    input_time_str (str): 输入的时间字符串，格式为 "YYMMDDHH"。
    supported_hours (list): 支持的小时时刻列表，如 ["00", "12"]。

    返回:
    str: 最近的起报时间字符串，格式为 "YYMMDDHH"。
    """
    # 解析输入的时间字符串
    input_time = datetime.strptime(input_time_str, "%y%m%d%H")

    # 找到最近的支持时刻
    nearest_hour = None
    min_diff = None
    for hour in supported_hours:
        # 构建当前支持时刻的时间
        test_time = datetime.strptime(input_time_str[:-2] + hour, "%y%m%d%H")

        # 计算差异
        diff = (input_time - test_time).total_seconds()

        # 只考虑过去的时间
        if diff >= 0 and (min_diff is None or diff < min_diff):
            nearest_hour = hour
            min_diff = diff

    if nearest_hour is None:
        raise ValueError("无法找到最近的支持时刻")

    # 返回最近的起报时间
    return input_time_str[:-2] + nearest_hour


def calculate_hours_between(start_time_str, end_time_str):
    """
    计算两个时间点之间的小时数。

    参数:
    start_time_str (str): 开始时间字符串，格式为 "YYMMDDHH"。
    end_time_str (str): 结束时间字符串，格式为 "YYMMDDHH"。

    返回:
    int: 两个时间点之间的小时数。
    """
    # 解析时间字符串为 datetime 对象
    start_time = datetime.strptime(start_time_str, "%y%m%d%H")
    end_time = datetime.strptime(end_time_str, "%y%m%d%H")

    # 计算时间差
    delta = end_time - start_time

    # 将时间差转换为小时数
    hours = int(delta.total_seconds() / 3600)
    if hours == 0:
        hours = 1
    return hours


def approximate_coordinates(coords, grid):
    """
    根据传入的分辨率对经纬度列表进行取舍，并存储在字典中。

    :param coords: 经纬度对象列表，每个对象包含 req_lat 和 req_lon 属性
    :param grid: 分辨率，单位为度
    :return: 存储近似后坐标的字典
    """
    if grid <= 0:
        raise ValueError("分辨率必须大于0")

    factor = 1 / grid
    mapping_coords = {}

    for coord in coords:
        approx_lon = round(coord.req_lon * factor) / factor
        approx_lat = round(coord.req_lat * factor) / factor
        key = (approx_lat, approx_lon)
        if key not in mapping_coords:
            mapping_coords[key] = coord

    return mapping_coords