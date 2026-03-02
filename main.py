from unittest import result
from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from resources import Entry, EntryManager
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [
  "https://wexler.io",  # адрес на котором работает фронт-энд
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)

class Settings(BaseSettings):
    data_folder: str = '/Users/anastasia/PycharmProjects/PythonProject' #'/Users/anastasia/Downloads/test.json'

settings = Settings()

@app.get("/api/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/api/entries/")
async def get_entries():
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()
    result = []
    for entry in entry_manager.entries:
        result.append(entry.json())
    return result
@app.post('/api/save_entries/')
async def save_entries(data: list[dict]):
    entry_manager = EntryManager(settings.data_folder)
    entry_manager.load()
    for item in data:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)