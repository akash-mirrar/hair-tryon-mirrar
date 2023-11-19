from flask import flask, request, jsonify
import os
from align_face import run_face_alignment
from parser import align_parser, param_parser
from main import *

app = Flask(__name__)

@app.route("/embed", methods=['POST'])
def embed():
    file = request.files['user_image']

    file.save(os.path.join('./upload_dir', file.filename.split('.')[0]+'.png'))

    #run face alignment
    align_args = align_parser.parse_args()
    run_face_alignment(align_args)

    #Generate embeddings
    param_args = param_parser.parse_args()
    generate_embeddings(param_args)

    return jsonify({
        "Success": "Embeddings generated successfully"
    })

@app.route("/tryon", methods=['POST'])
def tryon():
    user_image_id = request.args.get('user_image_id')
    style_img_path = request.args.get('hairstyle_img_path')
    color = request.args.get('color')

    pass

