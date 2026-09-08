from fastapi import FastAPI

app = FastAPI(
    title="API Cafeteria",
    description="API REST for cafeteria order and inventory management",
    version="1.0.0"
)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "API of the cafeteria running correctly"}
