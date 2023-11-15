from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette import status

from datatools.validate_form import find_matching_form, check_fields_type
from db import forms_collection
from schemas import ExampleForm
from schemas.form import Form

router = APIRouter()


@router.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")


@router.post(
    "/get_form",
    summary="Поиск среди шаблонов форм",
    description="Если найдется шаблон response = {'name': 'Myform'}, "
                "если нет то = {'f_name1': FIELD_TYPE, ...}"
)
async def get_form(data: ExampleForm) -> dict:
    """
    Поддерживаются типы:
    - **email**
    - **телефон**
    - **дата**
    - **текст**
    """
    data = data.model_dump()
    or_conditions = []
    for field_name in data.keys():
        or_conditions.append(
            {field_name: {'$exists': True}}
        )
    # Ищем все совпадения по названиям полей
    cursor = forms_collection.find(
        {
            "$or": or_conditions
        }
    )
    results = [obj async for obj in cursor]
    data = await find_matching_form(results, data)
    return data


@router.get(
    "/forms",
    summary='Список всех шаблонов форм'
)
async def get_all_forms() -> list[dict]:
    cursor = forms_collection.find()
    forms = await cursor.to_list(length=None)
    forms_without_id = [
        {k: v for k, v in form.items() if k != '_id'} for form in forms
    ]
    return forms_without_id


@router.post(
    "/forms",
    summary="Создание шаблона формы",
    status_code=status.HTTP_201_CREATED,
    response_model=Form
)
async def create_form(data: Form) -> dict:
    is_valid = await check_fields_type(
        data.model_dump(exclude={"name", "id"})
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Некорректные данные в форме',
        )
    new_form = await forms_collection.insert_one(data.model_dump())
    created_form = await forms_collection.find_one(
        {"_id": new_form.inserted_id}
    )
    return created_form


@router.delete(
    "/forms",
    summary="Удаление шаблона формы",
    status_code=status.HTTP_200_OK,
    response_model=Form
)
async def delete_form(name: str) -> dict:
    form = await forms_collection.find_one_and_delete(
        {"name": name}
    )
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Форма с именем '{name}' не найдена."
        )
    return form
