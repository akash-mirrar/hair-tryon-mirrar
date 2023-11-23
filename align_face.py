import dlib
from pathlib import Path
import argparse
import torchvision
from utils.drive import open_url
from utils.shape_predictor import align_face
import PIL, os, cv2
from align import crop_image
from datetime import datetime
from rembg import remove

parser = argparse.ArgumentParser(description='Align_face')
parser.add_argument('-upload_dir', type=str, default='upload_dir', help='image uploaded will be stored in this directory')
parser.add_argument('-unprocessed_dir', type=str, default='unprocessed', help='directory with unprocessed images')
parser.add_argument('-output_dir', type=str, default='input/face', help='output directory')

parser.add_argument('-output_size', type=int, default=1024, help='size to downscale the input images to, must be power of 2')
parser.add_argument('-seed', type=int, help='manual seed to use')
parser.add_argument('-cache_dir', type=str, default='cache', help='cache directory for model weights')

###############
parser.add_argument('-inter_method', type=str, default='bicubic')



args = parser.parse_args()

cache_dir = Path(args.cache_dir)
cache_dir.mkdir(parents=True, exist_ok=True)

output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True,exist_ok=True)

# print("Downloading Shape Predictor")
# f=open_url("https://drive.google.com/uc?id=1huhv8PYpNNKbGCLOaYUjOgR1pY5pmbJx", cache_dir=cache_dir, return_path=True)
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def orientation_check(args):
    upload_path = os.path.join("./", args.upload_dir)
    unprocessed_path = os.path.join("./", args.unprocessed_dir)
    print(unprocessed_path)
    for filename in os.listdir(upload_path):
        img = cv2.imread(os.path.join(upload_path, filename))
        rembg = remove(img)
        # img = blur_face(img)
        img = crop_image(img)
        img = cv2.resize(img, (1024, 1024))
        cv2.imwrite(unprocessed_path + '/' +filename.split(".")[0]+".png", img)

def run_face_alignment(args):
    face_align_start_time = datetime.now()
    print(f"Face alignment start time: {face_align_start_time}")

    orientation_check(args)
    for im in Path(args.unprocessed_dir).glob("*.*"):
        faces = align_face(str(im),predictor)

        for i,face in enumerate(faces):
            if(args.output_size):
                factor = 1024//args.output_size
                assert args.output_size*factor == 1024
                face_tensor = torchvision.transforms.ToTensor()(face).unsqueeze(0).cuda()
                face_tensor_lr = face_tensor[0].cuda().detach().clamp(0, 1)
                face = torchvision.transforms.ToPILImage()(face_tensor_lr)
                if factor != 1:
                    face = face.resize((args.output_size, args.output_size), PIL.Image.LANCZOS)
            if len(faces) > 1:
                face.save(Path(args.output_dir) / (im.stem+f"_{i}.png"))
            else:
                face.save(Path(args.output_dir) / (im.stem + f".png"))

    face_align_end_time = datetime.now()
    print(f"Face alignment start time: {face_align_end_time}")
    print(f"Time taken for Bledning: {face_align_end_time-face_align_start_time}")
# run_face_alignment(args)