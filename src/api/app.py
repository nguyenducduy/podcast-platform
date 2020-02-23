from db import db_session
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from root_schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView
from middleware.auth import AuthorizationMiddleware

app = Flask(__name__, static_folder='storage')
app.debug = True
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
        'graphql', schema=schema, graphiql=True, middleware=[AuthorizationMiddleware()])
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
