# Объявление примеров данных запроса
# добавим расчёт полной цены с налогом и немного улучшим

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="API Магазина", description="Обновление товара и расчёт полной цены с налогом")

# Модель товара
class Item(BaseModel):
    name: str = Field(..., title="Название товара")
    description: str | None = Field(None, title="Описание товара")
    price: float = Field(..., gt=0, title="Цена товара")
    tax: float | None = Field(0, ge=0, title="Налог на товар")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ноутбук",
                    "description": "Высокопроизводительный ноутбук",
                    "price": 1000.0,
                    "tax": 100.0,
                }
            ]
        }
    }

# PUT-эндпоинт
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    full_price = item.price + (item.tax or 0)  # Рассчёт полной цены
    results = {
        "item_id": item_id,
        "item": item,
        "full_price": full_price
    }
    return results
 