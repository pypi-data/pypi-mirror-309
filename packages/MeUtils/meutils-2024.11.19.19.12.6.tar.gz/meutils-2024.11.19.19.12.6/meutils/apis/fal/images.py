#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : images
# @Time         : 2024/11/13 15:44
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.config_utils.lark_utils import get_next_token_for_polling
from meutils.pipe import *
from meutils.schemas.image_types import ImageRequest, FluxImageRequest, SDImageRequest, ImagesResponse
from meutils.schemas.fal_types import FEISHU_URL

import fal_client
from fal_client import AsyncClient, SyncClient

DEFAULT_MODEL = "fal-ai/flux-pro/v1.1-ultra"
MODELS = {
    "flux-1.1-pro-ultra": "fal-ai/flux-pro/v1.1-ultra"
}

# client = AsyncClient(key=os.getenv("FAL_KEY"))
client = SyncClient(key=os.getenv("FAL_KEY"))

application = "fal-ai/recraft-v3"

import asyncio
import fal_client


async def submit():
    result = await fal_client.run_async(
        "fal-ai/flux/dev",
        arguments={
            "prompt": "a cat",
            "seed": 6252023,
            "image_size": "landscape_4_3",
            "num_images": 4
        },
    )

    print(result)


async def generate(request: ImageRequest, token: Optional[str] = None):
    """https://fal.ai/models/fal-ai/flux-pro/v1.1-ultra/api#api-call-submit-request
    """
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    request.model = MODELS.get(request.model, DEFAULT_MODEL)
    logger.debug(request)

    data = await AsyncClient(key=token).run(
        application=request.model,
        arguments={
            "prompt": request.prompt,
            "num_images": request.n,

            "aspect_ratio": "16:9",

            "enable_safety_checker": True,
            "safety_tolerance": "6",
            "output_format": "png",
        }
    )

    return ImagesResponse(data=data.get("images", data))


handler = client.submit(
    application=application,
    arguments={
        "prompt": "a red panda eating a bamboo in front of a poster that says \"recraft V3 now available at fal\""
    },
)

# 任务id
request_id = handler.request_id
client.get_handle(application, request_id)
client.get_handle(application, request_id).get()

from openai import AsyncClient, Client

resp = Client().images.generate(
    model="dall-e-3",
    prompt="a red panda eating a bamboo in front of a poster that says \"recraft V3 now available at fal\"",
    size="1024x1024",
    quality="standard",
    n=1,
)  # {"data": [{"url": '...'}]}

# /replicate/ {

#     openai
#
# }

#
# from
#
# import replicate
#
# output = replicate.run(
#     "black-forest-labs/flux-schnell",
#     input={"prompt": "an iguana on the beach, pointillism"}
# )
#
# # Save the generated image
# with open('output.png', 'wb') as f:
#     f.write(output[0].read())
#
# print(f"Image saved as output.png")
