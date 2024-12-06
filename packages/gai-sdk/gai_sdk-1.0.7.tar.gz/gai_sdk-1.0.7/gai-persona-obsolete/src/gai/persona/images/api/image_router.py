import uuid
import base64
from io import BytesIO

# fastapi
from fastapi import APIRouter, Body, HTTPException, Header, Depends, Request
from gai.lib.common.errors import InternalException
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.persona.images.pydantic.GenerateImagePydantic import GenerateImagePydantic
from gai.tti.client.tti_client import TTIClient
from gai.persona.images.system_images_mgr import SystemImagesMgr
from gai.lib.common.image_utils import bytes_to_imageurl

# Implementations Below
image_router = APIRouter()

### POST /api/v1/persona/image
@image_router.post("/api/v1/persona/image")
async def post_persona_image(req: GenerateImagePydantic=Body(...)):
    try:
        mgr = SystemImagesMgr(
            tti_client=TTIClient(config={
                "type":"tti",
                "url":"http://localhost:12035/sdapi/v1/txt2img"
            })
        )
        if not req.AgentId:
            req.AgentId = "00000000-0000-0000-0000-000000000000"
        agent_image = mgr.generate_image(
            agent_id=req.AgentId,
            agent_name=req.Name,
            agent_traits=req.AgentTraits,
            image_styles=req.AgentImageStyles,
            description=req.AgentDescription
        )
        mgr.export_image(agent_image)
        image_bytes = mgr.get_agent_image(agent_id=req.AgentId,size="256x256")
        dataUrl = bytes_to_imageurl(image_bytes)["url"]
        return {"data_url":dataUrl}

    except Exception as e:
        id = str(uuid.uuid4())
        logger.error(str(e)+" "+id)
        raise InternalException(id)
    

### GET /api/v1/persona/profile
@image_router.get("/api/v1/persona/image/{size}/{persona_id}")
async def get_persona_image(size:str,persona_id:str):
    mgr = SystemImagesMgr(
        tti_client=TTIClient(config={
            "type":"tti",
            "url":"http://localhost:12035/sdapi/v1/txt2img"
        })
    )
    try:
        image_bytes = mgr.get_agent_image(agent_id=persona_id,size=size)
    except FileNotFoundError:
        return None
    image_base64 = convert_image_to_base64(image_bytes=image_bytes)
    imageType = 'image/png'
    dataUrl = f'data:{imageType};base64,{image_base64}'
    return {"data_url":dataUrl}
