from flask import Flask, request, jsonify
import os, pymongo
from align_face import run_face_alignment
from parser import align_parser, param_parser
from main import *
from dotenv import load_dotenv
import ssl, certifi
from uuid import uuid4
import jwt
from config import *
from swap import swap_face
from pathlib import Path

user_collection = db["user"]

app = Flask(__name__)
upload_dir = "./upload_dir"
unprocessed_dir = "./unprocessed"
input_dir = "./input/face"
output_dir = "./output"

def create_user_directory(phone_no):
    try:
        if not os.path.exists(os.path.join(upload_dir, phone_no)):
            os.mkdir(os.path.join(upload_dir, phone_no))
        
        if not os.path.exists(os.path.join(unprocessed_dir, phone_no)):
            os.mkdir(os.path.join(unprocessed_dir, phone_no))

        if not os.path.exists(os.path.join(output_dir, phone_no)):
            os.mkdir(os.path.join(output_dir, phone_no))
    except Exception as e:
        raise(e)

@app.route("/login", methods=['POST'])
def login():
    request_body = request.json

    token = jwt.encode({
        'phone_no': request_body["phone_no"],
    }, SECRET_KEY, "HS256")

    try:
        if not user_collection.find_one({"phone_no": request_body["phone_no"]}):
            create_user_directory(request_body['phone_no'])
            
            # add user to db
            user_data = {
                "phone_no": request_body["phone_no"],
                "token": token,
                "upload_dir": os.path.join(upload_dir, request_body["phone_no"]),
                "unprocessed_dir": os.path.join(unprocessed_dir, request_body["phone_no"]),
                "output_dir": os.path.join(output_dir, request_body["phone_no"])
            }
            user_collection.insert_one(user_data)
        else:
            user = user_collection.find_one({"phone_no": request_body["phone_no"]})

        return jsonify(message="user logged in successfully", token=token), 200
    except Exception as e:
        return jsonify(message=e), 403

def remove_files(current_user):
    if os.path.exists(os.path.join(upload_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(upload_dir, current_user["phone_no"])).glob("*") if f.is_file()] 

        # for f in os.listdir(os.path.join(upload_dir, current_user["phone_no"])):
        #     print(f)
        #     os.remove(f)


    if os.path.exists(os.path.join(unprocessed_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(unprocessed_dir, current_user["phone_no"])).glob("*") if f.is_file()]

    if os.path.exists(os.path.join(output_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(output_dir, current_user["phone_no"])).glob("*") if f.is_file()]

@app.route("/embed", methods=['POST'])
@token_required
def embed(current_user):
    f = request.files['file']
    ref_img_path = request.form.get('ref_img_path')
    remove_files(current_user)
    f.save(os.path.join('./upload_dir/'+current_user.get("phone_no")+"/", f.filename.split('.')[0]+'.png'))
    
    filter_criteria = {"phone_no": current_user["phone_no"]}  # Replace with the actual criteria to identify the document
    data_to_append = {"filename": f.filename.split('.')[0]+'.png'}
    update_operation = {"$set": data_to_append}
    user_collection.update_one(filter_criteria, update_operation)
    #run face alignment
    align_args = align_parser.parse_args()
    align_args.upload_dir = os.path.join("upload_dir", str(current_user.get("phone_no")))
    align_args.unprocessed_dir = os.path.join("unprocessed", str(current_user.get("phone_no")))
    align_args.output_dir = "./input/face"
    run_face_alignment(align_args)
    #Generate embeddings
    param_args = param_parser.parse_args()
    # param_args.input_dir = os.path.join("./input/face", current_user.phone_no)
    param_args.im_path1 = f.filename.split(".")[0]+".png"
    param_args.im_path2 = ref_img_path
    param_args.im_path3 = ref_img_path
    param_args.output_dir = os.path.join("./output", current_user.get("phone_no"))
    generate_embeddings(param_args)
    return jsonify({
        "Success": "Embeddings generated successfully"
    })
    # except Exception as e:
    #     return jsonify(message=str(e)), 403

@app.route("/tryon", methods=['POST'])
@token_required
def tryon(current_user):
    ref_img_path = request.form.get('ref_img_path')
    param_args = param_parser.parse_args()
    param_args.im_path1 = current_user["filename"]
    param_args.im_path2 = ref_img_path
    param_args.im_path3 = ref_img_path
    param_args.output_dir = os.path.join("./output", current_user.get("phone_no"))
    run_alignment(param_args)
    blend_images(param_args)
    swap_face(param_args, current_user)
    
    return jsonify(message="Alignment and Blending done successfully")
    # except Exception as e:
    #     return jsonify(message=str(e)), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)