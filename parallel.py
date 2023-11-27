from flask import Flask, request, jsonify
import os, pymongo
from align_face import run_face_alignment
# from parser import align_parser, param_parser
from main import *
from dotenv import load_dotenv
import ssl, certifi
from uuid import uuid4
import jwt
from config import *
from utils.file_ops import *
from swap import swap_face
from pathlib import Path
import torch
from parser import align_parser, param_parser
from datetime import datetime
import torch
import torch.multiprocessing as mp
from multiprocessing import freeze_support
import base64
from io import BytesIO
from PIL import Image

# manager = mp.Manager()
# processing_dict = manager.dict()
processing_dict = {}
embedding_status = {}
reconstruction_status = {}
# lock = manager.Lock()

user_collection = db["user"]

def process_embedding_endpoint(current_user_phone, filename, ref_img_path):
    # with lock:
    # embedding_status[current_user_phone] = {}
    start_time = datetime.now()
    # print(f"Starting Embedding for User - {current_user_phone} --> {start_time}")
    # embedding_status[current_user_phone]["status"] = "processing"
    # embedding_status[current_user_phone]["start_time"] = str(start_time)
    filter_criteria = {"phone_no": current_user_phone}  # Replace with the actual criteria to identify the document
    data_to_append = {"filename": filename.split('.')[0]+'.png'}
    update_operation = {"$set": data_to_append}
    user_collection.update_one(filter_criteria, update_operation)
    #run face alignment
    align_args = align_parser.parse_args()
    align_args.upload_dir = os.path.join("upload_dir", str(current_user_phone))
    align_args.unprocessed_dir = os.path.join("unprocessed", str(current_user_phone))
    align_args.output_dir = "./input/face"
    run_face_alignment(align_args)

    #Generate embeddings
    param_args = param_parser.parse_args()
    # param_args.input_dir = os.path.join("./input/face", current_user.phone_no)
    param_args.im_path1 = filename.split(".")[0]+".png"
    param_args.im_path2 = ref_img_path
    param_args.im_path3 = ref_img_path
    param_args.output_dir = os.path.join("./output", current_user_phone)
    generate_embeddings(param_args)

    # processing_dict[current_user_phone] = "Completed"

    end_time = datetime.now()
    duration = end_time-start_time
    # print(f"Starting Embedding for User: {current_user_phone} : {end_time}")
    # embedding_status[current_user_phone]["status"] = "completed"
    print(f"Time taken in Embedding - {current_user_phone} --> {end_time-start_time}")
    # print(embedding_status)
    # embedding_status[current_user_phone]["end_time"] = str(end_time)
    # embedding_status[current_user_phone]["duration"] = str(duration)

    update_data = {
        "$set": {
            "embedding": {
                "status": "completed",
                "start_time": str(start_time),
                "end_time": str(end_time),
                "duration": str(duration)
            }
        }
    }

    user_collection.update_one({"phone_no": current_user_phone}, update_data)
    # print("Embedding status \n", embedding_status)


def process_reconstruction_endpoint(current_user_phone, filename, ref_img_path):
    # reconstruction_status[current_user_phone] = {}
    # reconstruction_status[current_user_phone]["status"] = "processing"
    
    start_time = datetime.now()
    print(f"Starting Reconstruction for User - {current_user_phone} ---> {start_time}")
    # reconstruction_status[current_user_phone]["start_time"] = str(start_time)
    param_args = param_parser.parse_args()
    param_args.im_path1 = filename
    param_args.im_path2 = ref_img_path
    param_args.im_path3 = ref_img_path
    param_args.output_dir = os.path.join("./output", current_user_phone)
    run_alignment(param_args)
    
    blend_images(param_args)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Ending Reconstruction for User - {current_user_phone} - {end_time}")
    # reconstruction_status[current_user_phone]["status"] = "completed"
    
    print(f"Time taken in Reconstruction for User {current_user_phone}--> {end_time-start_time}")
    # reconstruction_status[current_user_phone]["end_time"] = str(end_time)
    # embedding_status[current_user_phone]["duration"] = str(duration)

    print("Reconstruction status \n", reconstruction_status)

    update_data = {
        "$set": {
            "reconstruction": {
                "status": "completed",
                "start_time": str(start_time),
                "end_time": str(end_time),
                "duration": str(duration)
            }
        }
    }

    user_collection.update_one({"phone_no": current_user_phone}, update_data)
    # swap_face(param_args, current_user)
    
    # return jsonify(message="Alignment and Blending done successfully")


def create_app(align_parser, param_parser):

    app = Flask(__name__)

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


    @app.route("/embed", methods=['POST'])
    @token_required
    def embed(current_user):
        data = request.json
        base64_img = data["base_64_image"]
        image_data = base64.b64decode(base64_img)
        remove_files(current_user)
        filename = current_user["phone_no"]+".png"
        with open("./upload_dir/"+current_user["phone_no"]+"/"+filename, "wb") as f:
            f.write(image_data)

        ref_img_path = data['ref_img_path']
        # f = request.files['file']
        # ref_img_path = request.form.get('ref_img_path')
        
        # f.save(os.path.join('./upload_dir/'+current_user.get("phone_no")+"/", current_user["phone_no"]+'.png'))
        
        # with lock:
        if current_user["phone_no"] in embedding_status:
            phone_no = current_user["phone_no"]
            return jsonify(message=f"User with {phone_no}'s request is already processing"), 403
        
        mp.Process(
            target=process_embedding_endpoint,
            args=(current_user["phone_no"], filename, ref_img_path)
        ).start()
        
        return jsonify({
            "Success": "Embeddings generated successfully"
        })
        # except Exception as e:
        #     return jsonify(message=str(e)), 403

    @app.route("/tryon", methods=['POST'])
    @token_required
    def tryon(current_user):
        ref_img_path = request.form.get('ref_img_path')
        
        if current_user["phone_no"] is reconstruction_status:
            phone_no = current_user["phone_no"]
            return jsonify(message="User with {phone_no}'s request is already processing"), 403

        mp.Process(
            target=process_reconstruction_endpoint,
            args=(current_user["phone_no"], current_user["filename"], ref_img_path)
        ).start()

        # print()

        return jsonify({
            "Success": "Embeddings generated successfully"
        })
    return app


if __name__ == '__main__':
    import pycuda.driver as cuda
    cuda.init()
    # from parser import align_parser, param_parser
    mp.set_start_method('spawn', force=True)
    # freeze_support()
    print(cuda.Device(0).name())
    app = create_app(align_parser, param_parser)
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)