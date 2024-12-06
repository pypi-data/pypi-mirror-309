from decimal import Decimal
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class Coordinate(BaseModel):
    req_lat: float
    req_lon: float


class QueryNWPRequest(BaseModel):
    """
    Query request model
    src: str - 数据源，如：ec、gfs
    start_time: str - 数据源发布起始时间，如：24010100，24年01月01号00点
    period_interval: int - 相邻两次的发布时间，如：24，单位：小时
    period: int - 从发布起始时间往后取的发布时次长度，如：365
    start_hour: int - 单次发布时间点往后取的时间点起点，如：0，单位：小时
    end_hour: int - 单次发布时间点往后取的时间点起点，如：24，单位：小时
    forecast_interval: int - 数据点的时间间隔，如：1，单位：hour
    req_lat: float - 请求的纬度，如：35.0
    req_lon: float - 请求的经度，如：109.9
    vars: List[str] - 变量列表，如：['t2m']
    levels: List[str] - 层列表，如：['100']
    workers:int - mongo方式时生效，并发查询线程数量，默认3
    """
    engine: str = "mongo"
    src: str
    start_time: str
    period_interval: int
    period: int
    start_hour: int
    end_hour: int
    forecast_interval: int
    coords: List[Coordinate]
    vars: List[str]
    levels: Optional[List[str]] = None
    workers: int = 3

    @field_validator("engine")
    def color_must_be_valid(cls, v):
        valid_engines = ["bigdata", "mongo"]
        if v not in valid_engines:
            raise ValueError("engine must be one of bigdata, mongo")
        return v

class QueryNWPBizRequest(BaseModel):
    """
    Query request model
    src: str - 数据源，如：ec/hres
    start_time: str - 数据起始时间(不一定是真正的起报时间，要逻辑计算向前获取最近的起报时间)，如：24010100，24年01月01号00点
    ndays: int - 从匹配到的最近的起报时间开始，往后n天的数据
    hours: int - 输入时刻算起的预报小时数，如24 即传入的start_time + 24小时之间的预报数据
    vars: List[str] - 变量列表，如：['t2m']
    workers:int - mongo方式时生效，并发查询线程数量，默认3
    """
    engine: str = "mongo"
    src: str
    start_time: str
    ndays: int
    hours: int
    coords: List[Coordinate]
    vars: List[str]
    workers: int = 3

class QueryAreaRequest(BaseModel):
    provinces: list[str] = Field(default=[], description="省份或区域id列表", min_items=1)
    type: int = Field(default=0, description="场站类型，0：wind，1：solar")
    start_time: str = Field(description="开始时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    end_time: str = Field(description="结束时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")

class QueryStationRequest(BaseModel):
    query_type: int = Field(default=0, description="查询类型，0：基于场站查询，1：基于子场查询 ")
    ids: list[int] = Field(default=[], description="场站或子场id列表")
    provinces: list[str] = Field(default=[], description="省份列表")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")


class QueryObservationRequest(BaseModel):
    query_type: int = Field(default=0, description="查询类型，0：基于场站查询，1：基于子场查询")
    ids: list[int] = Field(default=[], description="场站或子场id列表")
    provinces: list[str] = Field(default=[], description="省份或区域id列表")
    type: int = Field(default=None, description="场站类型，0：wind，1：solar")
    start_time: str = Field(description="开始时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    end_time: str = Field(description="结束时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


class Task(BaseModel):
    task_id: str
    status: StatusEnum
    file_path: Optional[str] = None
    start_time: Optional[str] = None  # YYYY-MM-DD HH:MM:SS

class AreasDto(BaseModel):
    area_id: Optional[str] = None
    province: Optional[str] = None
    types: Optional[int] = None
    capacity: Optional[float] = None
    time: Optional[str] = None

class StationsDto(BaseModel):
    id: int = Field(default=None, description="场站id")
    code: Optional[str] = None
    types: str
    capacity: Optional[float] = None
    province: Optional[str] = None
    longitude: Decimal
    latitude: Decimal
    altitude: Optional[float] = None
    hub_height: Optional[float] = None


class ObservationsDto(BaseModel):
    time: str
    station_id: int
    sub_station_id: Optional[int] = None
    radiation: Optional[float] = None
    windspeed: Optional[float] = None
    power: Optional[float] = None
    label_status: Optional[int] = None


class BaseRsp(BaseModel):
    page: int = 0
    page_size: int = 0
    records: Union[List[StationsDto], List[ObservationsDto], List[AreasDto], None] = None


class BizResponse(BaseModel):
    code: int = 0  # 0: success !0: fail
    msg: str = 'ok'
    data: object = None
