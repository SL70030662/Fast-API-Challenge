from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.crm_sync import sync_crm_data
from app.services.marketing_sync import sync_marketing_data

router = APIRouter()

@router.get("/sync/{source}")
async def sync_data(source: str, db: AsyncSession = Depends(get_db)):
    if source == "crm":
        await sync_crm_data(db)
    elif source == "marketing":
        await sync_marketing_data(db)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data source")
    return {"message": f"Data synchronized successfully for {source}"}
