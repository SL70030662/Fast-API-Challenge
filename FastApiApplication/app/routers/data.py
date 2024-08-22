from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Customer, Campaign
from app.schemas import CustomerSchema, CampaignSchema
from typing import List
# from app.services.crm_service import fetch_customers
# from app.services.marketing_service import fetch_campaigns


router = APIRouter()

@router.get("/data/customers", response_model=List[CustomerSchema])
async def get_customers(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).offset(offset).limit(limit))
    customers = result.scalars().all()
    return customers

# @router.get("/data/customers", response_model=List[CustomerSchema])
# async def get_customers(limit: int = Query(100, le=1000), offset: int = Query(0)):
#     try:
#         customers = await fetch_customers(limit=limit, offset=offset)
#         return customers
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/campaigns", response_model=List[CampaignSchema])
async def get_campaigns(offset: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Campaign).offset(offset).limit(limit))
    campaigns = result.scalars().all()
    return campaigns

# @router.get("/data/campaigns", response_model=List[CampaignSchema])
# async def get_campaigns():
#     try:
#         campaigns = await fetch_campaigns()
#         return campaigns
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
