#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : oneapi_types
# @Time         : 2024/6/28 10:13
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.data.oneapi import NOTICE, FOOTER
from sqlmodel import Field, Session, SQLModel, create_engine, select, insert, update
from sqlalchemy import JSON

BASE_URL = "https://api.chatfire.cn"


class Tasks(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}  # includes this line

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[int] = Field(default=None)
    updated_at: Optional[int] = Field(default=time.time)
    task_id: Optional[str] = Field(default=None, max_length=50)
    platform: Optional[str] = Field(default=None, max_length=30)
    user_id: Optional[int] = Field(default=None)
    channel_id: Optional[int] = Field(default=None)
    quota: Optional[int] = Field(default=None)
    action: Optional[str] = Field(default=None, max_length=40)
    status: Optional[str] = Field(default=None, max_length=20)
    fail_reason: Optional[str] = Field(default=None)
    submit_time: Optional[int] = Field(default=None)
    start_time: Optional[int] = Field(default=None)
    finish_time: Optional[int] = Field(default=None)
    progress: Optional[str] = Field(default=None, max_length=20)
    properties: Optional[dict] = Field(default=None, sa_type=JSON)
    data: Optional[dict] = Field(default=None, sa_type=JSON)
    remote_task_id: Optional[str] = Field(default=None, max_length=50)

    class Config:
        arbitrary_types_allowed = True


class ModelGroupInfo(BaseModel):
    """注：信息JSON共有以下键值，均全为string类型：name（厂商名称）、desc（厂商介绍，支持MD）、icon（厂商图标链接，不定义则会自动匹配默认图标库）、notice（厂商使用公告说明，支持MD）"""
    name: str

    desc: Optional[str] = None

    icon: Optional[str] = None

    notice: Optional[str] = None


class ModelInfo(BaseModel):
    """note（模型说明，支持MD）、icon（模型图标链接，不定义则会自动匹配默认图标库）、tags（模型标签，多个｜分割）、group（模型归属分组，例如OpenAI，或与下方【模型厂商信息中的Key相对应】）"""
    note: Optional[str] = None

    icon: Optional[str] = None

    tags: Optional[str] = None

    """ModelGroupInfo.name"""
    group: Optional[str] = None


# https://oss.ffire.cc/images/qw.jpeg?x-oss-process=image/format,jpg/resize,w_512
if __name__ == '__main__':
    # print(','.join(REDIRECT_MODEL.keys()))

    from meutils.apis.oneapi import option, channel

    option()
    #
    arun(channel.edit_channel(MODEL_PRICE))
