# Path-параметры и валидация числовых данных
# Добавим описание, пример данных, обработку ошибок и возврат понятного ответа.



from typing import Annotated
from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI(title="Item API", description="Пример FastAPI проекта с параметрами пути и запросов", version="1.0")

# Эндпоинт получения товара по ID
@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="ID товара", ge=1, description="Идентификатор товара (целое число >= 1)")],
    q: Annotated[str | None, Query(max_length=50, description="Необязательный параметр поиска")] = None,
):
    # Простая имитация базы данных
    fake_db = {1: "Ноутбук", 2: "Мышь", 3: "Клавиатура"}

    # Проверка, есть ли товар
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"Товар с ID {item_id} не найден")

    result = {"id": item_id, "name": fake_db[item_id]}
    if q:
        result.update({"query": q})

    return {"status": "ok", "data": result}
