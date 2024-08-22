Project Overview
This project is a FastAPI application that acts as a data warehouse. It collects and synchronizes data from multiple external APIs, handles webhook inputs, and provides efficient data retrieval. The application manages background tasks for data synchronization using asyncio.

Setup Instructions

Prerequisites
-------------
Python 3.11

Local Setup
-----------
1.Clone the Repository:
    git clone https://github.com/SL70030662/fastapi-data-warehouse.git
    cd fastapi-data-warehouse
2.Create a Virtual Environment:
    python3 -m venv venv
    venv\Scripts\activate
3.Install Dependencies:
    pip install -r requirements.txt
4.Run the Application:
    uvicorn app.main:app --reload
5.Access the API:
    Open http://localhost:8000/docs to view the Swagger UI for API testing.

API Documentation
-----------------

Endpoints
1.POST /webhook:
    Receives data from a webhook and stores it in the database.
2.GET /data:
    Retrieves stored data with pagination.
    Query Parameters: offset, limit
3.GET /sync/{source}:
    Triggers synchronization for a specific data source (crm or marketing).
4.GET /tasks:
    Lists all running background tasks.
5.POST /tasks/cancel:
    Cancels a specific background task by task_id.

Example Requests
----------------
post request to /receive_webhook
{
    "customer": {
      "id": 1,
      "external_id": "cust_12345",
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
  }


{
  "campaign": {
    "id": 1,
    "external_id": "camp_67890",
    "name": "Winter Sale",
    "details": {
      "discount": "20%",
      "start_date": "2024-12-01",
      "end_date": "2024-12-31"
    }
  }
}

Data Modeling Decisions
-----------------------

1.Unified Schema
The application uses a unified data model to store information from both CRM and Marketing APIs, allowing for seamless querying across different data sources.

2.CRM Data:
Stored in the customers table with fields like id, name, email, etc.

3.Marketing Data:
Stored in the campaigns table with fields like id, campaign_name, budget, etc.

4.Indexing and Optimization
Indexes are created on frequently queried fields to enhance data retrieval speed. The use of SQLite's database is sufficient for this project scope, but it can be replaced with a more scalable solution if necessary.

5.Background Task Management
asyncio for Background Tasks
The application leverages asyncio for handling background tasks. When a sync operation is triggered, it runs asynchronously, allowing the API to respond immediately without blocking.

6.Task Tracking
Background tasks are tracked using an in-memory dictionary, enabling easy monitoring and cancellation through API endpoints.