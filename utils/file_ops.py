import os
from pathlib import Path

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

def remove_files(current_user):
    if os.path.exists(os.path.join(upload_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(upload_dir, current_user["phone_no"])).glob("*") if f.is_file()] 

    if os.path.exists(os.path.join(unprocessed_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(unprocessed_dir, current_user["phone_no"])).glob("*") if f.is_file()]

    if os.path.exists(os.path.join(output_dir, current_user["phone_no"])):
        [os.remove(f) for f in Path(os.path.join(output_dir, current_user["phone_no"])).glob("*") if f.is_file()]
