from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import route modules
from routes.vc_test_routes import router as vc_test_router
from routes.payment_routes import router as payment_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'app_db')]

# Create the main app without a prefix
app = FastAPI(title="VC Investor Test API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "VC Investor Test API", "status": "operational"}

@api_router.get("/health")
async def health():
    return {"status": "healthy", "database": "connected", "services": "operational"}

# Include sub-routers
api_router.include_router(vc_test_router)
api_router.include_router(payment_router)

# Include the main router in the app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    """Create database indexes and initialize services."""
    try:
        # Create indexes for better performance
        await db.vc_evaluations.create_index("id")
        await db.vc_evaluations.create_index("user_uuid")
        await db.vc_evaluations.create_index("created_at")
        await db.payment_records.create_index("evaluation_id")
        await db.payment_records.create_index("stripe_payment_intent_id")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database indexes: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection."""
    client.close()
    logger.info("Database connection closed")