from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config import settings
from infra.logger import logger
from infra.oss import OSSConfigurationError

app = FastAPI(title="CapCut API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "output": None, "error": str(exc), "error_code": "INTERNAL_ERROR"}
    )

@app.exception_handler(OSSConfigurationError)
async def oss_config_exception_handler(request: Request, exc: OSSConfigurationError):
    return JSONResponse(
        status_code=500,
        content={"success": False, "output": None, "error": str(exc), "error_code": "CONFIG_ERROR"}
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port {settings.PORT}")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
