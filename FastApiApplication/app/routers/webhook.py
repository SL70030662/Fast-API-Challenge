from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import CustomerSchema, CampaignSchema
from app.models import Customer, Campaign

router = APIRouter()

@router.post("/webhook")
async def receive_webhook(data: dict, db: AsyncSession = Depends(get_db)):
    # Process webhook data and save it to the database
    try:
        if "customer" in data:
            customer_data = CustomerSchema(**data["customer"])
            customer = Customer(external_id=customer_data.external_id, name=customer_data.name, email=customer_data.email)
            db.add(customer)
        elif "campaign" in data:
            campaign_data = CampaignSchema(**data["campaign"])
            campaign = Campaign(external_id=campaign_data.external_id, name=campaign_data.name, details=campaign_data.details)
            db.add(campaign)

        await db.commit()
        return {"message": "Webhook data received successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
