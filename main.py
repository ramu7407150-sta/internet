from fastapi import FastAPI

app = FastAPI(title="Мой FastAPI сервер")

@app.get("/")
def read_root():
    return {"message": "Здесь — главная страница!"}

@app.get("/hello")
def say_hello():
    return {"message": "Саломат бошед! Это доп. страница."}
