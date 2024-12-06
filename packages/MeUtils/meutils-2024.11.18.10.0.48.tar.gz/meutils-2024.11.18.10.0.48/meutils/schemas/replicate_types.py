#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : replicate_types
# @Time         : 2024/11/15 18:32
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


class ReplicateRequest(BaseModel):
    input: Optional[Any] = None
    version: str = ""


class ReplicateResponse(BaseModel):
    id: str = Field(default_factory=shortuuid.random)
    status: str = "starting"  # succeeded

    input: Optional[Any] = None  # 兼容任意结构体
    output: Optional[Any] = None

    logs: Optional[str] = None
    error: Optional[str] = None
    metrics: Optional[Any] = None

    created_at: str = Field(default_factory=lambda: datetime.datetime.today().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    """
    {
    "get": "https://api.replicate.com/v1/predictions/pab8srw8jhrm20cj1e7s0d8kf4",
    "cancel": "https://api.replicate.com/v1/predictions/pab8srw8jhrm20cj1e7s0d8kf4/cancel"
    }
    """
    urls: Optional[Dict[str, str]] = None

    data_removed: bool = False  # 移除任务
    version: Optional[str] = None

    # token
    system_fingerprint: Optional[str] = None

    class Config:
        # 允许额外字段，增加灵活性
        extra = 'allow'


class ReplicateSDKRequest(BaseModel):
    ref: str = ""
    input: Optional[Dict[str, Any]] = None  # {"prompt": "A majestic lion", "num_outputs": 2}


if __name__ == '__main__':
    from meutils.db.redis_db import redis_client

    r = ReplicateRequest(
        input=ReplicateSDKRequest(
            ref="stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
            input={"prompt": "A majestic lion", "num_outputs": 2}
        )
    )

    # print(r.model_dump_json(indent=4))

    # print(ReplicateResponse())

    url = "https://oss.ffire.cc/files/kling_watermark.png"

    response = ReplicateResponse(output=[url])
    print(response.model_dump_json(indent=4))

    redis_client.set(response.id, response.model_dump_json(indent=4), ex=3600)

    # redis_client.set(response.id, response, ex=3600)
