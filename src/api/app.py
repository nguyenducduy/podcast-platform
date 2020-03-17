from db import db_session
from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from root_schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView
from middleware.auth import AuthorizationMiddleware
from depot.manager import DepotManager
from config import config_by_name

app = Flask(__name__, static_folder='storage')
app.debug = True
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

depot_name = 'podcast_audio_data'
depot_config = {
    'depot.backend': 'depot.io.boto3.S3Storage',
    'depot.endpoint_url': 'https://storage.googleapis.com',
    'depot.access_key_id': config_by_name['prod'].GOOGLE_CLOUD_STORAGE_ACCESS_KEY,
    'depot.secret_access_key': config_by_name['prod'].GOOGLE_CLOUD_STORAGE_SECRET_KEY,
    'depot.bucket': config_by_name['prod'].GOOGLE_CLOUD_STORAGE_BUCKET
}

DepotManager.configure(depot_name, depot_config)

app.add_url_rule(
    '/graphql',
    view_func=FileUploadGraphQLView.as_view(
        'graphql', schema=schema, graphiql=True, middleware=[AuthorizationMiddleware()])
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(port=9000, threaded=True, debug=True,)
