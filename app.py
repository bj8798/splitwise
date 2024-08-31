import uvicorn
from fastapi import FastAPI
from pathlib import Path
from src.api.main import app_router
from src.utils.db_ops import create_schema, add_seed_data

create_schema()
add_seed_data()

app = FastAPI()
app.include_router(app_router)


if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app",
                host="0.0.0.0",
                port=8000,
                log_config='config/logging/logging.conf')
