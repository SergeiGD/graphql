from os import environ
from ariadne import gql, make_executable_schema, graphql_sync
from ariadne.types import GraphQLResolveInfo
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from modules.models.base import db
from modules.graphql.schema import type_defs
from modules.graphql.types import mutation, query, category, datetime_scalar, date_scalar

# TODO: корзина
# TODO: права
# TODO: поиск
# TODO: индексы прокинуть
# TODO: cron для очищения корзины и заказов
# TODO: dataclasses
# TODO: типизацию


checked_types = gql(type_defs)
schema = make_executable_schema(
    checked_types,
    [query, mutation, category, date_scalar, datetime_scalar],
    convert_names_case=True
)
explorer_html = ExplorerGraphiQL().html(None)
app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value={"request": request},
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    db_name = environ.get('DB_NAME', 'db_graphql')
    db_user = environ.get('DB_USER', 'db_user')
    db_password = environ.get('DB_PASSWORD', 'db_password')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_password}@db/{db_name}'

    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')



