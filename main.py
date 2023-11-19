import argparse

import torch
import numpy as np
import sys
import os
import dlib
from datetime import datetime

from PIL import Image

from models.Embedding import Embedding
from models.Alignment import Alignment
from models.Blending import Blending
from swap import swap_face

def generate_embeddings(args):
    embeddings = Embedding(args)

    im_path1 = os.path.join(args.input_dir, args.im_path1)
    im_path2 = os.path.join(args.input_dir, args.im_path2)
    im_path3 = os.path.join(args.input_dir, args.im_path3)

    im_set = {im_path1, im_path2, im_path3}

    embeddings.invert_images_in_W([*im_set])
    embeddings.invert_images_in_FS([*im_set])


def run_alignment(args):
    im_path1 = os.path.join(args.input_dir, args.im_path1)
    im_path2 = os.path.join(args.input_dir, args.im_path2)
    im_path3 = os.path.join(args.input_dir, args.im_path3)

    align = Alignment(args)
    align.align_images(im_path1, im_path2, sign=args.sign, align_more_region=False, smooth=args.smooth)

    if im_path2 != im_path3:
        align.align_images(im_path1,im_path3, sign=args.sign, align_more_region=False, smooth=args.smooth)

def blend_images(args):
    im_path1 = os.path.join(args.input_dir, args.im_path1)
    im_path2 = os.path.join(args.input_dir, args.im_path2)
    im_path3 = os.path.join(args.input_dir, args.im_path3)

    blend = Blending(args)

    blend.blend_images(im_path1, im_path2, im_path3, sign=args.sign)

# def main(args):
#     ii2_start_time = datetime.now()
#     print(f"### Starting II2S Embedding ###: {ii2_start_time}")
#     ii2s = Embedding(args)
#     ii2_end_time = datetime.now()
#     print(f"### Completed II2S Embedding ###: {ii2_end_time}")
#     print(f"Time taken for II2S embedding: {ii2_end_time-ii2_start_time}")
#     # print(f"Time taken: {}")
#     #
#     # ##### Option 1: input folder
#     # # ii2s.invert_images_in_W()
#     # # ii2s.invert_images_in_FS()

#     # ##### Option 2: image path
#     # # ii2s.invert_images_in_W('input/face/28.png')
#     # # ii2s.invert_images_in_FS('input/face/28.png')
#     #
#     ##### Option 3: image path list

#     # im_path1 = 'input/face/90.png'
#     # im_path2 = 'input/face/15.png'
#     # im_path3 = 'input/face/117.png'

#     im_path1 = os.path.join(args.input_dir, args.im_path1)
#     im_path2 = os.path.join(args.input_dir, args.im_path2)
#     im_path3 = os.path.join(args.input_dir, args.im_path3)

    
#     im_set = {im_path1, im_path2, im_path3}

#     wp_start_time = datetime.now()
#     print(f"### Starting W+ Embedding ###: {wp_start_time}")
#     ii2s.invert_images_in_W([*im_set])
#     wp_end_time = datetime.now()
#     print(f"### Ending W+ Embedding ###: {wp_end_time}")
#     print(f"Time taken for W+ embedding: {wp_end_time-wp_start_time}")

#     fs_start_time = datetime.now()
#     print(f"### Starting FS Embedding ###: {fs_start_time}")
#     ii2s.invert_images_in_FS([*im_set])
#     fs_end_time = datetime.now()
#     print(f"### Starting FS Embedding ###: {fs_end_time}")
#     print(f"Time taken for FS Embedding: {fs_end_time-fs_start_time}")

#     alignment_start_time = datetime.now()
#     print(f"### Starting Alignment ###: {alignment_start_time}")
#     align = Alignment(args)
#     align.align_images(im_path1, im_path2, sign=args.sign, align_more_region=False, smooth=args.smooth)
#     if im_path2 != im_path3:
#         align.align_images(im_path1, im_path3, sign=args.sign, align_more_region=False, smooth=args.smooth, save_intermediate=False)
    
#     alignment_end_time = datetime.now()
#     print(f"### Ending alignment: {alignment_end_time}")
#     print(f"Time taken for alignment: {alignment_end_time-alignment_start_time}")

#     blending_start_time = datetime.now()
#     print(f"### Starting Blending: {blending_start_time}")
#     blend = Blending(args)
#     blend.blend_images(im_path1, im_path2, im_path3, sign=args.sign)
    
#     blending_end_time = datetime.now()
#     print(f"### Completing blending: {blending_end_time}")
#     print(f"Time taken for Bledning: {blending_end_time-blending_start_time}")





# if __name__ == "__main__":

#     parser = argparse.ArgumentParser(description='Barbershop')

#     # I/O arguments
#     parser.add_argument('--input_dir', type=str, default='input/face',
#                         help='The directory of the images to be inverted')
#     parser.add_argument('--output_dir', type=str, default='output',
#                         help='The directory to save the latent codes and inversion images')
#     parser.add_argument('--im_path1', type=str, default='16.png', help='Identity image')
#     parser.add_argument('--im_path2', type=str, default='15.png', help='Structure image')
#     parser.add_argument('--im_path3', type=str, default='117.png', help='Appearance image')
#     parser.add_argument('--sign', type=str, default='realistic', help='realistic or fidelity results')
#     parser.add_argument('--smooth', type=int, default=1, help='dilation and erosion parameter')

#     # StyleGAN2 setting
#     parser.add_argument('--size', type=int, default=1024)
#     parser.add_argument('--ckpt', type=str, default="pretrained_models/ffhq.pt")
#     parser.add_argument('--channel_multiplier', type=int, default=2)
#     parser.add_argument('--latent', type=int, default=512)
#     parser.add_argument('--n_mlp', type=int, default=8)

#     # Arguments
#     parser.add_argument('--device', type=str, default='cuda')
#     parser.add_argument('--seed', type=int, default=None)
#     parser.add_argument('--tile_latent', action='store_true', help='Whether to forcibly tile the same latent N times')
#     parser.add_argument('--opt_name', type=str, default='adam', help='Optimizer to use in projected gradient descent')
#     parser.add_argument('--learning_rate', type=float, default=0.01, help='Learning rate to use during optimization')
#     parser.add_argument('--lr_schedule', type=str, default='fixed', help='fixed, linear1cycledrop, linear1cycle')
#     parser.add_argument('--save_intermediate', action='store_true',
#                         help='Whether to store and save intermediate HR and LR images during optimization')
#     parser.add_argument('--save_interval', type=int, default=400, help='Latent checkpoint interval')
#     parser.add_argument('--verbose', action='store_true', help='Print loss information')
#     parser.add_argument('--seg_ckpt', type=str, default='pretrained_models/seg.pth')


#     # Embedding loss options
#     parser.add_argument('--percept_lambda', type=float, default=1.0, help='Perceptual loss multiplier factor')
#     parser.add_argument('--l2_lambda', type=float, default=1.0, help='L2 loss multiplier factor')
#     parser.add_argument('--p_norm_lambda', type=float, default=0.001, help='P-norm Regularizer multiplier factor')
#     parser.add_argument('--l_F_lambda', type=float, default=0.5, help='L_F loss multiplier factor')
#     parser.add_argument('--W_steps', type=int, default=10, help='Number of W space optimization steps')
#     parser.add_argument('--FS_steps', type=int, default=150, help='Number of FS space optimization steps')



#     # Alignment loss options
#     parser.add_argument('--ce_lambda', type=float, default=1.0, help='cross entropy loss multiplier factor')
#     parser.add_argument('--style_lambda', type=str, default=4e4, help='style loss multiplier factor')
#     parser.add_argument('--align_steps1', type=int, default=140, help='')
#     parser.add_argument('--align_steps2', type=int, default=1, help='')


#     # Blend loss options
#     parser.add_argument('--face_lambda', type=float, default=1, help='')
#     parser.add_argument('--hair_lambda', type=str, default=1.0, help='')
#     parser.add_argument('--blend_steps', type=int, default=400, help='')




#     args = parser.parse_args()
#     start_time = datetime.now()
#     main(args)

#     swap_face(src_img=args.input_dir+"/"+args.im_path1, dest_img=args.output_dir+"/"+args.im_path1.split('.')[0]+"_"+args.im_path2.split('.')[0]+"_"+args.im_path3.split('.')[0]+"_"+"realistic.png")
#     end_time = datetime.now()
    
#     print("Process starts: ", start_time)
#     print("Process ends: ", end_time)
#     print("Time takes to generate: ", end_time - start_time)