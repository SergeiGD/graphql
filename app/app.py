from ariadne import gql, make_executable_schema, upload_scalar, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi.handlers import GraphQLHTTPHandler
from ariadne.asgi import GraphQL
from modules.session.session import engine
from modules.graphql.types import (
    mutation, query, datetime_scalar, date_scalar, user_union, base_order_union,
    category, group, order, purchase, worker, client,
)
from sqlalchemy import inspect
from modules.session.session import get_session
from modules.models.base import Base
import uvicorn


# TODO: миграции БД
# TODO: поиск везде
# TODO: измение личной информации


type_defs = load_schema_from_path('./modules/graphql/schema ')
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
        with get_session() as db:
            db.add(obj)
            value = resolver(obj, info, **args)
            return value
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
    uvicorn.run(app, host="0.0.0.0", port=5000)
