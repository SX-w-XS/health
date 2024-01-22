# -*- coding: utf-8 -*- 
'''
# @Time : 2023/10/18 1:51 
# @Author : PVINCE
# @Project: fastapi-vue-admin
# @Path:
# @Software: PyCharm
# @File : mySQLAlchemyCRUDRouter.py 
#@desc:
'''

from typing import Any, Callable, List, Generator

from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_crudrouter.core._types import PAGINATION

try:
    from sqlalchemy.orm import Session
    from sqlalchemy.ext.declarative import DeclarativeMeta as Model
    from sqlalchemy.exc import IntegrityError
except ImportError:
    Model = None
    Session = None
    IntegrityError = None
    sqlalchemy_installed = False
else:
    sqlalchemy_installed = True
    Session = Callable[..., Generator[Session, Any, None]]

CALLABLE = Callable[..., Model]
CALLABLE_LIST = Callable[..., List[Model]]


class MYSQLAlchemyCRUDRouter(SQLAlchemyCRUDRouter):

    def _get_all(self, *args: Any, **kwargs: Any) -> CALLABLE_LIST:
        def route(
                db: Session = Depends(self.db_func),
                pagination: PAGINATION = self.pagination,
        ) -> List[Model]:
            skip, limit = pagination.get("skip"), pagination.get("limit")

            db_models: List[Model] = (
                db.query(self.db_model)
                .filter(self.db_model.is_delete == 0)
                .order_by(getattr(self.db_model, self._pk))
                .limit(limit)
                .offset(skip)
                .all()
            )
            return db_models

        return route
