from flask import Flask
from flask_babel import Babel
from config import DevelopmentConfig, ProductionConfig
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene_file_upload.flask import FileUploadGraphQLView
from sqlalchemy.orm import scoped_session, sessionmaker
from middlewares.auth import AuthorizationMiddleware

app = Flask(__name__, static_folder='storage')
app.debug = True

babel = Babel(app)

# cors
CORS(app, resources={r'/*': {'origins': '*'}})

# environment config
if app.config["ENV"] == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

with app.app_context():
    from root_schema import schema
    from depot.manager import DepotManager
    from db import db
    app.db = db

    depot_name = 'podcast_audio_data'
    depot_config = {
        'depot.backend': 'depot.io.boto3.S3Storage',
        'depot.endpoint_url': 'https://storage.googleapis.com',
        'depot.access_key_id': app.config['GOOGLE_CLOUD_STORAGE_ACCESS_KEY'],
        'depot.secret_access_key': app.config['GOOGLE_CLOUD_STORAGE_SECRET_KEY'],
        'depot.bucket': app.config['GOOGLE_CLOUD_STORAGE_BUCKET']
    }

    DepotManager.configure(depot_name, depot_config)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

# graphql endpoint
app.add_url_rule('/graphql',
                 view_func=FileUploadGraphQLView.as_view(
                     'graphql',
                     schema=schema,
                     graphiql=False,
                     middleware=[AuthorizationMiddleware()]))


if __name__ == '__main__':
    app.run(
        port=5000,
        threaded=True,
        debug=True,
    )
