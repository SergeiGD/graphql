from ariadne import gql, make_executable_schema, upload_scalar, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi.handlers import GraphQLHTTPHandler
from ariadne.asgi import GraphQL
from hotel_business_module.session.session import engine
from ariadne_graphql.types import (
    mutation, query, datetime_scalar, date_scalar, user_union, base_order_union,
    category, group, order, purchase, worker, client,
)
from sqlalchemy import inspect
from hotel_business_module.session.session import get_session
from hotel_business_module.models.base import Base
import uvicorn


type_defs = load_schema_from_path('ariadne_graphql/schema ')
checked_types = gql(type_defs)
schema = make_executable_schema(
    checked_types,
    [
        query, mutation, category, date_scalar, datetime_scalar, upload_scalar, user_union, base_order_union,
        group, order, purchase, worker, client,
     ],
    convert_names_case=True
)
explorer_html = ExplorerGraphiQL().html(None)


def session_middleware(resolver, obj, info, **args):
    # middleware для добавления объекта к сесси при вложенных запросах
    if isinstance(obj, Base) and inspect(obj).detached:
        # если объект является моделью sqlalchemy и он не заатачен к сессии, то добалвяем его
        with get_session() as db:
            db.add(obj)
            value = resolver(obj, info, **args)
    else:
        value = resolver(obj, info, **args)
    return value


app = GraphQL(
    schema,
    http_handler=GraphQLHTTPHandler(
        middleware=[session_middleware],
    ),
)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
