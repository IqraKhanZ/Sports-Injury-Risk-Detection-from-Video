from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import logging

logger = logging.getLogger("sird.db")

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        if not settings.MONGODB_URL:
            logger.error("MONGODB_URL is not set in environment!")
            raise ValueError(
                "MONGODB_URL is missing. Set it in SIRD/backend/.env "
                "and ensure the file is loaded before startup."
            )
        if not settings.JWT_SECRET_KEY:
            logger.error("JWT_SECRET_KEY is not set in environment!")
            raise ValueError("JWT_SECRET_KEY is missing from environment variables.")

        logger.info("Connecting to MongoDB Atlas cluster...")
        # serverSelectionTimeoutMS=5000 ensures we fail fast if the cluster is unreachable
        cls.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000
        )
        # Verify connectivity with a lightweight ping before accepting requests
        await cls.client.admin.command("ping")
        cls.db = cls.client[settings.DB_NAME]
        logger.info(f"Connected to MongoDB Atlas → database: '{settings.DB_NAME}'")

    @classmethod
    async def close_db(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")

# Dependency helper
async def get_db():
    return Database.db

async def seed_demo_accounts():
    from app.auth import hash_password
    from datetime import datetime
    
    db = Database.db
    if db is None:
        return
        
    demo_coaches = [
        {"email": "coach.alex@sird.com", "fullname": "Alex Ferguson", "role": "Coach"},
        {"email": "coach.pep@sird.com", "fullname": "Pep Guardiola", "role": "Coach"},
        {"email": "coach.jurgen@sird.com", "fullname": "Jurgen Klopp", "role": "Coach"},
        {"email": "coach.carlo@sird.com", "fullname": "Carlo Ancelotti", "role": "Coach"},
        {"email": "coach.jose@sird.com", "fullname": "Jose Mourinho", "role": "Coach"}
    ]
    
    demo_physios = [
        {"email": "physio.john@sird.com", "fullname": "John Carter", "role": "Physiotherapist"},
        {"email": "physio.sarah@sird.com", "fullname": "Sarah Connor", "role": "Physiotherapist"},
        {"email": "physio.emma@sird.com", "fullname": "Emma Watson", "role": "Physiotherapist"},
        {"email": "physio.robert@sird.com", "fullname": "Robert Bruce", "role": "Physiotherapist"},
        {"email": "physio.alice@sird.com", "fullname": "Alice Vance", "role": "Physiotherapist"}
    ]
    
    demo_scientists = [
        {"email": "scientist.newton@sird.com", "fullname": "Newton Galileo", "role": "Sports Scientist"},
        {"email": "scientist.marie@sird.com", "fullname": "Marie Curie", "role": "Sports Scientist"}
    ]
    
    all_demos = demo_coaches + demo_physios + demo_scientists
    
    for demo in all_demos:
        existing = await db.users.find_one({"email": demo["email"]})
        if not existing:
            new_user = {
                "email": demo["email"],
                "fullname": demo["fullname"],
                "role": demo["role"],
                "password": hash_password("password123"),
                "auth_provider": "local",
                "created_at": datetime.utcnow()
            }
            await db.users.insert_one(new_user)
            logger.info(f"Seeded demo account: {demo['fullname']} ({demo['role']})")
