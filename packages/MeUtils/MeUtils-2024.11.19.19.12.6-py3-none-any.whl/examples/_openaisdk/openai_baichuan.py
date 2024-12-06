#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: assistants
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError
from meutils.schemas.oneapi_types.models import BAICHUAN

client = OpenAI(
    api_key=os.getenv("BAICHUAN_API_KEY"),
    base_url=os.getenv("BAICHUAN_BASE_URL")
)

for model in BAICHUAN:
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是个画图工具"},
                {"role": "user", "content": "你是谁"}
            ],
            # top_p=0.7,
            top_p=None,
            temperature=None,
            stream=True,
            max_tokens=6000
        )
    except APIStatusError as e:
        print(e.status_code)

        print(e.response)
        print(e.message)
        print(e.code)

    for chunk in completion:
        print(chunk.choices[0].delta.content)

