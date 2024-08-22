# import httpx
# from app.config import settings
# from app.models import Customer
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.services.task_manager import task_manager
# import uuid
# import asyncio


# async def sync_crm_data(db: AsyncSession):
#     async with httpx.AsyncClient() as client:
#         task_id = str(uuid.uuid4())
#         task = asyncio.create_task(_sync_crm(client, db))
#         task_manager.add_task(task_id, task)

# async def _sync_crm(client, db: AsyncSession):
#     try:
#         response = await client.get(settings.CRM_API_URL, headers={"X-API-Key": settings.API_KEY})
#         response.raise_for_status()
#         data = response.json()
#         for customer_data in data:
#             customer = Customer(
#                 external_id=customer_data["id"],
#                 name=customer_data["name"],
#                 email=customer_data["email"]
#             )
#             db.add(customer)
#         await db.commit()
#     except Exception as e:
#         await db.rollback()
#         raise e


import httpx
from app.config import settings
from app.models import Customer
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_manager import task_manager
import uuid
import asyncio
from typing import List, Dict, Any

async def sync_crm_data(db: AsyncSession):
    task_id = str(uuid.uuid4())
    task = asyncio.create_task(_sync_crm(task_id, db))
    task_manager.add_task(task_id, task)

async def _sync_crm(task_id: str, db: AsyncSession):
    async with httpx.AsyncClient() as client:
        try:
            # Paginate through CRM API
            limit = 100
            offset = 0
            while True:
                response = await client.get(
                    f"{settings.CRM_API_URL}?limit={limit}&offset={offset}",
                    headers={"X-API-Key": settings.API_KEY}
                )
                response.raise_for_status()
                data = response.json()

                if not isinstance(data, list):
                    raise ValueError("Expected a list of customers, but received: " + str(type(data)))
                
                if not data:
                    break  # Exit loop if no more data

                # Process and save customers to the database
                customers = []
                for customer_data in data:
                    if not isinstance(customer_data, dict):
                        raise ValueError("Customer data should be a dictionary but received: " + str(type(customer_data)))
                    
                    customer = Customer(
                        external_id=customer_data.get("external_id"),
                        name=customer_data.get("name"),
                        email=customer_data.get("email")
                    )
                    customers.append(customer)

                db.add_all(customers)
                await db.commit()

                offset += limit  # Update offset for next page

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
