from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class TrainResultRequest(BaseModel):
    # id: Optional[str] = None
    train_config_id: int
    model_path: Optional[str] = None
    train_start_time: str
    train_end_time: str
    train_error_msg: Optional[str] = None
    model_config = ConfigDict(
        protected_namespaces=()
    )


class InferEntity(BaseModel):
    time: str
    radiation: Optional[float] = None
    windspeed: Optional[float] = None
    power: Optional[float] = None


class InferResultRequest(BaseModel):
    infer_config_id: int
    model_id: int
    station_id: int
    infer_start_time: str
    infer_end_time: str
    infer_error_msg: Optional[str] = None
    items_len: Optional[int] = None
    items: List[InferEntity]
    model_config = ConfigDict(
        protected_namespaces=()
    )

class QueryInferRequest(BaseModel):
    query_type: int = Field(default=0, description="查询类型，0：基于场站查询，1：基于子场查询")
    ids: list[int] = Field(default=[], description="场站或子场id列表")
    algos: list[str] = Field(default=[], description="算法名称列表")
    start_time: str = Field(description="开始时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    end_time: str = Field(description="结束时间, 默认:utc, 若指定其它时区，如东八区时间:2024-02-01 15:00+08或2024-02-01T15:00+08:00")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=500, description="每页条数")