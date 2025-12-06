# Body - Множество параметров
#Улучшенная версия кода
#1/ Добавить валидацию полей цены и налога (не отрицательные).
#2/ Сделать вывод более структурированным.

from typing import Annotated
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="API Магазина", description="Пример PUT-запроса с валидацией")

class Товар(BaseModel):
    название: str = Field(..., title="Название товара")
    описание: str | None = Field(None, title="Описание товара")
    цена: float = Field(..., ge=0, title="Цена товара")
    налог: float | None = Field(None, ge=0, title="Налог")

@app.put("/товары/{id_товара}")
async def обновить_товар(
    id_товара: Annotated[int, Path(title="ID товара", ge=0, le=1000)],
    запрос: str | None = None,
    товар: Товар | None = None,
):
    # Проверка максимального ID
    if id_товара > 500:
        raise HTTPException(status_code=400, detail="ID товара слишком большой")

    результат = {"ID товара": id_товара, "Статус": "Обновлено"}

    if запрос:
        результат.update({"Запрос": запрос})
    if товар:
        результат.update({"Товар": товар})

    return результат
