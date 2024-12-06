import json
import sys
from sais.autotrain.dataservice import EnvVarCredentialsProvider, TrainInferHandler, TrainResultRequest, \
    InferResultRequest, QueryNWPHandler, ENDPOINT, QueryNWPRequest, QueryNWPBizRequest, QueryStationRelatedHandler, QueryStationRequest, \
    QueryObservationRequest, QueryInferRequest, QueryAreaRequest
import pandas as pd




# query_related = QueryStationRelatedHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_related.execute_query_area(QueryAreaRequest(
#     type=0,  # 0: wind, 1: solar
#     provinces=['Hainan'],
#     start_time='2024-01-31 16:00:00',
#     end_time='2024-12-10 15:00:00',
#     page=1,
#     page_size=sys.maxsize
# ))
# print(f"Query area result: {result.model_dump_json()}")

# query_station_result = query_station_related.execute_query_station(QueryStationRequest(
#     ids=["68"],
#     # provinces=["山东"],
#     page=1,
#     page_size=100,
#     query_type=0
# ))
# print(f"Query station result: {query_station_result.model_dump_json()}")

# result = query_related.execute_query_observation(QueryObservationRequest(
#     ids=["18"],
#     # provinces=["Hainan"],
#     start_time="2018-02-01 15:00:00",
#     end_time="2024-12-01 15:00:00",
#     page=1,
#     page_size=10,
#     query_type=0
# ))
# print(f"Query observation result: {result.model_dump_json()}")


# 全页遍历
# page = 1
# page_size = 1000
# while True:
#     query_observation_result_item = query_station_related.execute_query_observation(QueryObservationRequest(
#         ids=["1"],
#         # provinces=["山东"],
#         start_time="2023-01-01 00:00:05",
#         end_time="2024-07-01 00:00:05",
#         page=page,
#         page_size=page_size,
#         query_type=0
#     ))
#     if len(query_observation_result_item.records) == 0:
#         break
#     else:
#         print(f"Query observation result: {query_observation_result_item}")
#     page += 1

# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPRequest(
#     engine="mongo",
#     src="ec/hres_irr",
#     start_time="23080100",
#     period_interval=24,
#     period=1,
#     start_hour=28,
#     end_hour=51,
#     forecast_interval=1,
#     coords=[{"req_lat": 18.01, "req_lon": 96.61},{"req_lat": 18, "req_lon": 114},{"req_lat": 19, "req_lon": 119}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")





# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPRequest(
#     engine="mongo",
#     src="ec/hres",
#     start_time="24083000",
#     period_interval=24,
#     period=1,
#     start_hour=40,
#     end_hour=51,
#     forecast_interval=1,
#     coords=[{"req_lat": 38.44889, "req_lon": 111.4655}],
#     vars=[
#         "u100"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")


# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.query_nwp_meta(src="ec/hres")
# print(f"Query nwp meta: {result.model_dump_json()}")


# train_infer_handler = TrainInferHandler(endpoint="http://localhost:10115", auth_provider=EnvVarCredentialsProvider())
# train_result = train_infer_handler.execute_train_result_submit(TrainResultRequest(
#     train_config_id=62,
#     model_path="/path1/path2/model2.pkl",
#     train_start_time="2024-09-10 10:00:00",
#     train_end_time="2024-09-10 10:10:00",
#     train_error_msg="success"
# ))
# print(f"submit train result: {train_result}")

# infer_result = train_infer_handler.execute_infer_result_submit(InferResultRequest(
#     infer_config_id=1,
#     model_id=1,
#     station_id=1,
#     infer_start_time="2024-09-10 10:00:00",
#     infer_end_time="2024-09-10 10:10:00",
#     infer_status=2,  # 2：成功 3：失败
#     infer_error_msg="success",
#     items=[
#         {
#             "time": "2024-09-10 10:00:00",
#             "station_id": 1,
#             "radiation": 11.1,
#             "power": 9.8,
#         }
#     ]
# ))
# print(f"submit infer result: {infer_result}")


# train_infer_handler = TrainInferHandler(endpoint="http://fuxi-ai.cn:10115", auth_provider=EnvVarCredentialsProvider())
# query_infer_result = train_infer_handler.execute_query_infer(QueryInferRequest(
#     ids=[68],
#     algos=["tiapi-xgb_wind_short"],
#     start_time="2024-08-01 00:00:00",
#     end_time="2024-08-10 00:00:00",
#     page=1,
#     page_size=1000
# ))
# print(f"Query infer result: {query_infer_result.model_dump_json()}")
#
# train_infer_handler = TrainInferHandler(endpoint="http://fuxi-ai.cn:10115", auth_provider=EnvVarCredentialsProvider())
# query_infer_result = train_infer_handler.execute_query_infer(QueryInferRequest(
#     ids=[1],
#     algos=["tiapi-xgb_solar_short"],
#     start_time="2024-07-01 00:00:00",
#     end_time="2024-07-10 00:00:00",
#     page=1,
#     page_size=1000
# ))
# print(f"Query infer result: {query_infer_result.model_dump_json()}")


# train_infer_handler = TrainInferHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# query_infer_result = train_infer_handler.execute_query_infer(QueryInferRequest(
#     ids=[3],
#     algos=["tiapi-xgb_wind_ultra_points"],
#     start_time="2024-01-28 00:00:00",
#     end_time="2024-02-10 00:00:00",
#     page=1,
#     page_size=9223372036854775807
# ))
# dicts = query_infer_result.model_dump()
# print(f"Query infer result: {dicts}")



# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPRequest(
#     engine="mongo",
#     src="ec/hres_irr",
#     start_time="24080100",
#     period_interval=24,
#     period=1,
#     start_hour=0,
#     end_hour=245,
#     forecast_interval=1,
#     coords=[{"req_lat": 18, "req_lon": 96.6}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")

# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#         src='ec/hres',
#         start_time='23092116',
#         ndays=160,
#         hours=24,
#         coords=[{"req_lat": 35.56544828, "req_lon": 113.21735880}],
#         vars=['u100', 'v100', 'u10', 'v10', 'msl', 't2m', 'tp']))
# print(f"Query nwp result: {result.model_dump_json()}")

#
# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#     src="ec/hres_irr",
#     start_time="24082816",
#     ndays=1,
#     hours=24,
#     coords=[{"req_lat": 19, "req_lon": 109}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")


# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#     src="ec/hres_irr",
#     start_time="23090101",
#     ndays=4,
#     hours=24,
#     coords=[{"req_lat": 18.01, "req_lon": 96.61},{"req_lat": 18, "req_lon": 114},{"req_lat": 19, "req_lon": 119}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")

# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, auth_provider=EnvVarCredentialsProvider())
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#     src="fuxi_irr",
#     start_time="23090101",
#     ndays=4,
#     hours=24,
#     coords=[{"req_lat": 18, "req_lon": 96}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")


# 定义数据
# data = {
#     'time': ['2023-01-01 00:00:00+08'], # 带时区的字符串
#     'station_id': [18],
#     'radiation': [0.0],
#     'windspeed': [None],
#     'power': [0.02],
#     'label_status': [10]
# }
# df = pd.DataFrame(data)
#
# update_obs_related = QueryStationRelatedHandler(endpoint="http://fuxi-ai.cn:10115", auth_provider=EnvVarCredentialsProvider())
# update_obs_result = update_obs_related.execute_label_observation(df)
# print(update_obs_result)


# query_nwp = QueryNWPHandler(endpoint=ENDPOINT, mongo_host="fuxi-ai.cn", mongo_port=28087, mongo_user="root", mongo_password="yourPassword")
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#     src="fuxi_irr",
#     start_time="23090101",
#     ndays=4,
#     hours=24,
#     coords=[{"req_lat": 18, "req_lon": 96}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")


query_nwp = QueryNWPHandler(endpoint=ENDPOINT, mongo_host="fuxi-ai.cn", mongo_port=28087, mongo_user="root", mongo_password="yourPassword")
# result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
#     src="fuxi_irr",
#     start_time="23090101",
#     ndays=4,
#     hours=24,
#     coords=[{"req_lat": 18, "req_lon": 96}],
#     vars=[
#         "ssrgrd"
#     ]))
# print(f"Query nwp result: {result.model_dump_json()}")

result = query_nwp.execute_query(query_params=QueryNWPBizRequest(
        src='ec/hres',
        start_time='24070102',
        ndays=1,
        hours=96,
        coords=[{'req_lat': 18.66933828300006, 'req_lon': 109.11524498800003}, {'req_lat': 18.66933828300006, 'req_lon': 109.61524498800003}, {'req_lat': 18.66933828300006, 'req_lon': 110.11524498800003}, {'req_lat': 19.16933828300006, 'req_lon': 109.11524498800003}, {'req_lat': 19.16933828300006, 'req_lon': 109.61524498800003}, {'req_lat': 19.16933828300006, 'req_lon': 110.11524498800003}, {'req_lat': 19.66933828300006, 'req_lon': 109.61524498800003}, {'req_lat': 19.66933828300006, 'req_lon': 110.11524498800003}, {'req_lat': 19.66933828300006, 'req_lon': 110.61524498800003}],
        vars=['u100', 'v100', 'u10', 'v10', 'msl', 't2m', 'tp']))
        # vars=['u100m', 'v100m', 'u10m', 'v10m', 'msl', 't2m', 'tp']))
print(f"Query nwp result: {result.model_dump_json()}")