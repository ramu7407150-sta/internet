# Body - Вложенные модели
# расчёт полной цены и русские названия полей

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="API Магазина", description="Расчёт полной стоимости товара с налогом")

# Модель товара
class Item(BaseModel):
    name: str = Field(..., title="Название товара")
    description: str | None = Field(None, title="Описание товара")
    price: float = Field(..., gt=0, title="Цена товара")
    tax: float | None = Field(None, ge=0, title="Налог на товар")
    tags: list = Field(default_factory=list, title="Теги товара")

# PUT эндпоинт
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    full_price = item.price + (item.tax or 0)  # Рассчёт полной цены
    result = {
        "item_id": item_id,
        "item": item,
        "full_price": full_price  # Добавили новое поле с полной ценой
    }
    return result
