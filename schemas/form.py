from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class ExampleForm(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "example": {
                "field_name_1": "phone",
                "field_name_2": "date",
            }
        },
    )


class Form(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "example": {
                "name": "Form template name",
                "field_name_1": "email",
                "field_name_2": "phone"
            }
        },
    )
