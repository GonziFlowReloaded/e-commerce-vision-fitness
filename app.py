from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # Importa StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from routes import estadistica


app = FastAPI()


# Monta la carpeta static para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializa Jinja2 para FastAPI
templates = Jinja2Templates(directory="templates")

app.include_router(estadistica.router)
# Modelo de producto usando Pydantic
class Product(BaseModel):
    name: str
    description: str
    price: float
    image: str
    category: str

# Lista de productos de ejemplo
products = [
    Product(name="Mancuernas Ajustables", description="Perfectas para entrenar en casa o en el gimnasio.", price=50.00, image="https://via.placeholder.com/400x300", category="Fuerza"),
    Product(name="Banca para Pesas", description="Banca reclinable para entrenamientos de fuerza.", price=75.00, image="https://via.placeholder.com/400x300", category="Fuerza"),
    Product(name="Cuerda para Saltar", description="Accesorio ideal para mejorar tu resistencia cardiovascular.", price=30.00, image="https://via.placeholder.com/400x300", category="Cardio"),
    Product(name="Bicicleta Estática", description="Bicicleta para entrenamientos de resistencia en interiores.", price=200.00, image="https://via.placeholder.com/400x300", category="Cardio"),
    Product(name="Soga de Batalla", description="Herramienta ideal para entrenamientos de alta intensidad.", price=45.00, image="https://via.placeholder.com/400x300", category="HIIT")
]

@app.get("/")
async def index(
    request: Request,
    category: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    filtered_products = products
    categories = ["Fuerza", "Cardio", "HIIT"]
    # Filtrar por categoría
    if category:
        filtered_products = [p for p in filtered_products if p.category.lower() == category.lower()]

    # Filtrar por nombre
    if name:
        filtered_products = [p for p in filtered_products if name.lower() in p.name.lower()]

    # Filtrar por rango de precios
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.price >= min_price]
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.price <= max_price]

    return templates.TemplateResponse("index.html", {"request": request, "products": filtered_products, "categories": categories})
