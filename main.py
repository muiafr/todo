from fastapi import FastAPI
from router.routes import router as tasks_router
app = FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)