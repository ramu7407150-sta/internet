from fastapi import FastAPI, Query, Path, Body, File, UploadFile, Depends
from pydantic import BaseModel

app = FastAPI()

# -----------------------------
# Зависимость (Depends)
# -----------------------------
def common_parameters(q: str = Query(None), limit: int = 10):
    return {"q": q, "limit": limit}

# -----------------------------
# Модель для Body
# -----------------------------
class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

# -----------------------------
# Path
# -----------------------------
@app.get("/items/{item_id}")
async def read_item(item_id: int = Path(..., description="ID товара"), commons: dict = Depends(common_parameters)):
    return {"item_id": item_id, "query": commons}

# -----------------------------
# Body
# -----------------------------
@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_description": item.description}

# -----------------------------
# Query
# -----------------------------
@app.get("/search/")
async def search_items(q: str = Query(..., min_length=3, max_length=50), limit: int = 10):
    return {"query": q, "limit": limit}

# -----------------------------
# File
# -----------------------------
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}

# -----------------------------
# Body + Query + Path + Depends вместе
# -----------------------------
@app.post("/full-example/{item_id}")
async def full_example(
    item_id: int = Path(..., description="ID товара"),
    item: Item = Body(...),
    q: str = Query(None),
    commons: dict = Depends(common_parameters),
):
    return {
        "item_id": item_id,
        "item": item,
        "query": q,
        "commons": commons
    }
