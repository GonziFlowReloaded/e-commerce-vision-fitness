from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random

router = APIRouter()

# Configurar Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Montar archivos estáticos (si los necesitas en el futuro)
router.mount("/static", StaticFiles(directory="static"), name="static")

# Función auxiliar para generar datos de ejemplo
def generate_sample_data(n):
    return {
        'labels': [f'Día {i+1}' for i in range(n)],
        'values': [random.randint(1, 100) for _ in range(n)]
    }

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Generar datos de ejemplo (en una aplicación real, estos vendrían de una base de datos o API)
    compras_data = generate_sample_data(7)  # Datos para una semana
    clicks_data = generate_sample_data(7)
    productos_data = {
        'labels': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E'],
        'values': [random.randint(50, 200) for _ in range(5)]
    }
    conversion_data = {
        'conversiones': random.randint(50, 100),
        'no_conversiones': random.randint(100, 200)
    }

    # Renderizar la plantilla con los datos
    return templates.TemplateResponse("estadisticas.html", {
        "request": request,
        "compras_data": compras_data,
        "clicks_data": clicks_data,
        "productos_data": productos_data,
        "conversion_data": conversion_data
    })