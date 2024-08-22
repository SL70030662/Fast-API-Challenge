# import httpx
# from app.config import settings
# from app.models import Campaign
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.services.task_manager import task_manager
# import uuid
# import asyncio


# async def sync_marketing_data(db: AsyncSession):
#     async with httpx.AsyncClient() as client:
#         task_id = str(uuid.uuid4())
#         task = asyncio.create_task(_sync_marketing(client, db))
#         task_manager.add_task(task_id, task)

# async def _sync_marketing(client, db: AsyncSession):
#     try:
#         response = await client.get(settings.MARKETING_API_URL, headers={"X-API-Key": settings.API_KEY})
#         response.raise_for_status()
#         data = response.json()
#         for campaign_data in data:
#             campaign = Campaign(
#                 external_id=campaign_data["id"],
#                 name=campaign_data["name"],
#                 details=campaign_data.get("details")
#             )
#             db.add(campaign)
#         await db.commit()
#     except Exception as e:
#         await db.rollback()
#         raise e

import httpx
from app.config import settings
from app.models import Campaign
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_manager import task_manager
import uuid
import asyncio
from typing import List, Dict, Any

async def sync_marketing_data(db: AsyncSession):
    task_id = str(uuid.uuid4())
    task = asyncio.create_task(_sync_marketing(task_id, db))
    task_manager.add_task(task_id, task)

async def _sync_marketing(task_id: str, db: AsyncSession):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings.MARKETING_API_URL, headers={"X-API-Key": settings.API_KEY})
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, list):
                raise ValueError("Expected a list of campaigns, but received: " + str(type(data)))

            # Process and save campaigns to the database
            campaigns = []
            for campaign_data in data:
                if not isinstance(campaign_data, dict):
                    raise ValueError("Campaign data should be a dictionary but received: " + str(type(campaign_data)))
                
                campaign = Campaign(
                    external_id=campaign_data.get("id"),
                    name=campaign_data.get("name"),
                    details=campaign_data.get("details")
                )
                campaigns.append(campaign)

            db.add_all(campaigns)
            await db.commit()

        except httpx.HTTPStatusError as e:
            # Log HTTP errors
            await db.rollback()
            raise RuntimeError(f"HTTP error occurred: {e}")

        except httpx.RequestError as e:
            # Log request errors
            await db.rollback()
            raise RuntimeError(f"Request error occurred: {e}")

        except ValueError as e:
            # Log value errors (e.g., unexpected data format)
            await db.rollback()
            raise RuntimeError(f"Value error occurred: {e}")

        except Exception as e:
            # Log any other unexpected errors
            await db.rollback()
            raise RuntimeError(f"An unexpected error occurred: {e}")

        finally:
            # Optionally, you can handle any cleanup here if needed
            pass

