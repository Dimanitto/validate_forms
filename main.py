from fastapi import FastAPI

from api.form import router
from db import forms_collection, create_data

app = FastAPI(
    title='Определение форм',
    description='Web-приложение для определения заполненных форм',
)

app.include_router(router)


@app.on_event("startup")
async def app_init() -> None:
    document_count = await forms_collection.count_documents({})

    if document_count > 0:
        return
    await create_data()
