from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Flask module takes name of current module
app = Flask(__name__)
api = Api(app)
# Relative path (creates based on current path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Model for DB storage
class VideoModel(db.Model):
    # Defining the columns of our DB
    id = db.Column(db.Integer, primary_key=True)
    
    # Max characters 100, and can never be null
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # Re-defining the functionality of repr() (Returns a printable representation of the object)
    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

# Only run once - re-initializing this will overwrite the data in the tables that we have
# Commenting out after running
# db.create_all()

# Creating a RequestParser object 
video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='name parameter is required', required=True)
video_put_args.add_argument('views', type=str, help='views parameter is required', required=True)
video_put_args.add_argument('likes', type=str, help='likes parameter is required', required=True)

# Defining the fields from instance of VideoModel that will be returned when queried
resource_fields = {
    'id' : fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='name parameter is required')
video_update_args.add_argument('views', type=str, help='views parameter is required')
video_update_args.add_argument('likes', type=str, help='likes parameter is required')

class Video(Resource):
    # Decorating returning json serialised info
    @marshal_with(resource_fields)
    def get(self, video_id):
        # Query the database for result 
        # Will return an instance of VideoModel; must be serialized in order to be returned
        # Done using Resource fields and marshal_with
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='could not find video with that id')
        return result
    
    # Add info about a new video 
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken")
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        # DB video object serialized by the @marshal_with decorator
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='video doesn\'t exist')
        
        # RequestParser fills in fields with the value 'None' if nothing is passed. 
        # This means that name, views and likes will always EXIST, even if they don't have a real value
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        # Committ result object changes to the database
        db.session.commit()

        return result




api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    # Server will reload itself with any changes in the code
    app.run(debug=True)