from pydantic import Field
from pydantic.generics import GenericModel
from typing import Generic, TypeVar


DataT = TypeVar('DataT')


class CustomResponse(GenericModel, Generic[DataT]):
    status: str = Field(..., description='状态', example='success')
    data: DataT


def success_response(data):
    return {'status': 'success', 'data': data}
