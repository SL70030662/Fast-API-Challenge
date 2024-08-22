from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Customer, Campaign
from app.schemas import CustomerSchema, CampaignSchema
from sqlalchemy.orm import sessionmaker
from app.database import engine


async def get_customers(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[CustomerSchema]:
    async with db() as session:
        result = await session.execute(select(Customer).offset(skip).limit(limit))
        customers = result.scalars().all()
        return [CustomerSchema.from_orm(customer) for customer in customers]

async def get_customer_by_id(db: AsyncSession, customer_id: int) -> Optional[CustomerSchema]:
    async with db() as session:
        result = await session.execute(select(Customer).filter(Customer.id == customer_id))
        customer = result.scalar_one_or_none()
        return CustomerSchema.from_orm(customer) if customer else None

async def create_customer(db: AsyncSession, customer_data: CustomerSchema) -> CustomerSchema:
    new_customer = Customer(**customer_data.dict())
    async with db() as session:
        session.add(new_customer)
        await session.commit()
        await session.refresh(new_customer)
        return CustomerSchema.from_orm(new_customer)

async def update_customer(db: AsyncSession, customer_id: int, customer_data: CustomerSchema) -> Optional[CustomerSchema]:
    async with db() as session:
        result = await session.execute(select(Customer).filter(Customer.id == customer_id))
        customer = result.scalar_one_or_none()
        if customer:
            for key, value in customer_data.dict().items():
                setattr(customer, key, value)
            await session.commit()
            await session.refresh(customer)
            return CustomerSchema.from_orm(customer)
        return None

async def delete_customer(db: AsyncSession, customer_id: int) -> bool:
    async with db() as session:
        result = await session.execute(select(Customer).filter(Customer.id == customer_id))
        customer = result.scalar_one_or_none()
        if customer:
            await session.delete(customer)
            await session.commit()
            return True
        return False

async def get_campaigns(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[CampaignSchema]:
    async with db() as session:
        result = await session.execute(select(Campaign).offset(skip).limit(limit))
        campaigns = result.scalars().all()
        return [CampaignSchema.from_orm(campaign) for campaign in campaigns]

async def get_campaign_by_id(db: AsyncSession, campaign_id: int) -> Optional[CampaignSchema]:
    async with db() as session:
        result = await session.execute(select(Campaign).filter(Campaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        return CampaignSchema.from_orm(campaign) if campaign else None

async def create_campaign(db: AsyncSession, campaign_data: CampaignSchema) -> CampaignSchema:
    new_campaign = Campaign(**campaign_data.dict())
    async with db() as session:
        session.add(new_campaign)
        await session.commit()
        await session.refresh(new_campaign)
        return CampaignSchema.from_orm(new_campaign)

async def update_campaign(db: AsyncSession, campaign_id: int, campaign_data: CampaignSchema) -> Optional[CampaignSchema]:
    async with db() as session:
        result = await session.execute(select(Campaign).filter(Campaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        if campaign:
            for key, value in campaign_data.dict().items():
                setattr(campaign, key, value)
            await session.commit()
            await session.refresh(campaign)
            return CampaignSchema.from_orm(campaign)
        return None

async def delete_campaign(db: AsyncSession, campaign_id: int) -> bool:
    async with db() as session:
        result = await session.execute(select(Campaign).filter(Campaign.id == campaign_id))
        campaign = result.scalar_one_or_none()
        if campaign:
            await session.delete(campaign)
            await session.commit()
            return True
        return False

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async def get_all_customers():
    async with async_session() as session:
        result = await session.execute(select(Customer))
        return result.scalars().all()

async def get_all_campaigns():
    async with async_session() as session:
        result = await session.execute(select(Campaign))
        return result.scalars().all()