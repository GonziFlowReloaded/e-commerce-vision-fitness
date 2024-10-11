from fastapi import APIRouter, HTTPException, Query, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import math

router = APIRouter()

# Configurar Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Montar archivos estáticos
router.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo de datos para un item de inventario
class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    unit: str
    price_per_unit: float

# Simulación de una base de datos de inventario
inventory_db = [
    InventoryItem(id=1, name="Hierro", quantity=100, unit="kg", price_per_unit=2.5),
    InventoryItem(id=2, name="Carbón", quantity=50, unit="kg", price_per_unit=1.0),
    InventoryItem(id=3, name="Martillo", quantity=10, unit="unidad", price_per_unit=15.0),
]

# Rutas para el frontend
@router.get("/herreria")
async def home(request: Request):
    return templates.TemplateResponse("herreria/home.html", {"request": request})

@router.get("/inventory_management")
async def inventory_management(request: Request):
    return templates.TemplateResponse("herreria/inventory.html", {"request": request, "inventory": inventory_db})

@router.get("/calculations")
async def calculations(request: Request):
    return templates.TemplateResponse("herreria/calculations.html", {"request": request})

# Rutas de la API
@router.get("/api/inventory", response_model=List[InventoryItem])
async def get_inventory():
    return inventory_db

@router.post("/api/inventory")
async def add_inventory_item(request: Request):
    form_data = await request.form()
    new_item = InventoryItem(
        id=len(inventory_db) + 1,
        name=form_data.get("name"),
        quantity=int(form_data.get("quantity")),
        unit=form_data.get("unit"),
        price_per_unit=float(form_data.get("price_per_unit"))
    )
    inventory_db.append(new_item)
    return {"success": True, "message": "Item added successfully"}

@router.put("/api/inventory/{item_id}")
async def update_inventory_item(item_id: int, quantity: int):
    for item in inventory_db:
        if item.id == item_id:
            item.quantity = quantity
            return {"message": f"Cantidad actualizada para {item.name}"}
    raise HTTPException(status_code=404, detail="Item no encontrado")

@router.get("/api/calculate/sphere")
async def calculate_sphere_volume(radius: float = Query(..., description="Radio de la esfera en cm")):
    volume = (4/3) * math.pi * (radius ** 3)
    return {"volume": volume, "unit": "cm³"}

@router.get("/api/calculate/coal")
async def calculate_coal_needed(metal_weight: float = Query(..., description="Peso del metal a forjar en kg")):
    coal_needed = metal_weight * 0.25  # Asumimos que se necesita 1/4 de carbón por peso de metal
    return {"coal_needed": coal_needed, "unit": "kg"}

@router.get("/api/calculate/project_cost")
async def calculate_project_cost(
    metal_weight: float = Query(..., description="Peso del metal necesario en kg"),
    labor_hours: float = Query(..., description="Horas de trabajo estimadas")
):
    metal_cost = metal_weight * 2.5  # Asumimos un costo promedio de 2.5 por kg de metal
    labor_cost = labor_hours * 20  # Asumimos un costo de mano de obra de 20 por hora
    total_cost = metal_cost + labor_cost
    return {
        "metal_cost": metal_cost,
        "labor_cost": labor_cost,
        "total_cost": total_cost,
        "currency": "USD"
    }

@router.get("/api/check_stock")
async def check_stock(metal_needed: float = Query(..., description="Cantidad de metal necesario en kg")):
    total_metal = sum(item.quantity for item in inventory_db if item.name.lower() == "hierro")
    if total_metal >= metal_needed:
        return {"sufficient_stock": True, "available": total_metal, "needed": metal_needed}
    else:
        return {"sufficient_stock": False, "available": total_metal, "needed": metal_needed}
