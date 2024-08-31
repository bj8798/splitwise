import uvicorn
from fastapi import FastAPI
from pathlib import Path
from src.api.main import app_router
from src.db.db_ops import create_schema

create_schema()
app = FastAPI()
app.include_router(app_router)

if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app",
                host="localhost",
                port=8000,
                log_config='config/logging/logging.conf')
