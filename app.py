from os import name
from flask import Flask
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
from flask_restx import Api, Namespace, Resource, reqparse

from utils.predict import classify_using_bytes
from utils.maps import get_hospitals_near_location

app = Flask(__name__)
CORS(app)

api = Api(
    app=app,
    title="Eye Disease Classification API",
    description="3 models models are trained, combined them using ensemble technique to improve accuracy",
    doc="/",
    validate=True
)

classification_args = reqparse.RequestParser()
classification_args.add_argument(
    name="file",
    type=FileStorage,
    location="files",
    help="select the image for classification",
    required=True
)
classification_args.add_argument(
    name="model", 
    type=str, 
    location="form",
    help="select the model which you want to use for classification",
    required=True, 
    choices=[
        "VGG16", 
        "ResNet50", 
        "Ensemble",
        "InceptionV3",
        "WeightedEnsemble"
    ]
)

map_args = reqparse.RequestParser()
map_args.add_argument(
    name="lat",
    type=str,
    location="form",
    help="Enter latitude",
    required=True
)
map_args.add_argument(
    name="lon",
    type=str,
    location="form",
    help="Enter longutidue",
    required=True
)
map_args.add_argument(
    name="radius",
    type=str,
    location="form",
    help="Enter radius",
    required=True
)

model_path = {
    "VGG16" : "models/vgg16-5-epochs.h5",
    "ResNet50" : "models/resnet50-5-epochs.h5",
    "Ensemble" : "models/ensemble-5-epochs.h5",
    "InceptionV3" : "models/inceptionV3-5-epochs.h5",
    "WeightedEnsemble" : "models/weighted-ensemble-5-epochs.h5"
}
classification_controller = Namespace(name="Classification Controller", path="/classify")
map_controller = Namespace(name="map controller", description="Get nearest hospital", path="/map")

@classification_controller.route("/eye-disease")
class ClassificationClass(Resource):
    @classification_controller.expect(classification_args)
    def post(self):
        args = classification_args.parse_args()
        file = args['file']
        model = model_path.get(args['model'])

        result = classify_using_bytes(file.read(), model, 224)

        return result
    
@map_controller.route("/hospital")
class MapController(Resource):
    @map_controller.expect(map_args)
    def post(self):
        print("i am here")
        args = map_args.parse_args()
        print(args)
        result = get_hospitals_near_location(
                    lat=float(args['lat']),
                    lon=float(args['lon']),
                    radius=int(args['radius'])
                )
        
        return result

        

api.add_namespace(classification_controller)
api.add_namespace(map_controller)

if __name__ == "__main__":
    app.run(debug=True)
