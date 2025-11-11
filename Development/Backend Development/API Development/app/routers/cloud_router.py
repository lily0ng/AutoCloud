from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..services.aws_service import AWSService

router = APIRouter(
    prefix="/cloud",
    tags=["cloud"]
)

@router.get("/ec2/instances")
async def list_instances():
    try:
        aws_service = AWSService()
        instances = await aws_service.list_ec2_instances()
        return {
            "status": "success",
            "data": instances
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/s3/buckets")
async def list_buckets():
    try:
        aws_service = AWSService()
        buckets = await aws_service.list_s3_buckets()
        return {
            "status": "success",
            "data": buckets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backup/{resource_type}/{resource_id}")
async def create_backup(resource_type: str, resource_id: str):
    try:
        aws_service = AWSService()
        backup = await aws_service.create_backup(resource_id, resource_type)
        return {
            "status": "success",
            "data": backup
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

