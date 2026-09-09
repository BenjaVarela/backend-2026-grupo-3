from fastapi import FastAPI

app = FastAPI(
    title="API Cafeteria",
    description="API REST para la gestión de pedidos e inventario de la cafetería",
    version="1.0.0"
)

@app.get("/", tags=["Health Check"])
def root():
    return {"mensaje": "de que la cafetería funcione correctamente"}
