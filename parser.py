import argparse

align_parser = argparse.ArgumentParser(description='Align_face')

align_parser.add_argument('-upload_dir', type=str, default='upload_dir', help='image uploaded will be stored in this directory')
align_parser.add_argument('-unprocessed_dir', type=str, default='unprocessed', help='directory with unprocessed images')
align_parser.add_argument('-output_dir', type=str, default='input/face', help='output directory')

align_parser.add_argument('-output_size', type=int, default=1024, help='size to downscale the input images to, must be power of 2')
align_parser.add_argument('-seed', type=int, help='manual seed to use')
align_parser.add_argument('-cache_dir', type=str, default='cache', help='cache directory for model weights')

###############
align_parser.add_argument('-inter_method', type=str, default='bicubic')


param_parser = argparse.ArgumentParser(description='hair-tryon')
# I/O arguments
param_parser.add_argument('--input_dir', type=str, default='input/face',
                    help='The directory of the images to be inverted')
param_parser.add_argument('--output_dir', type=str, default='output',
                    help='The directory to save the latent codes and inversion images')
param_parser.add_argument('--im_path1', type=str, default='16.png', help='Identity image')
param_parser.add_argument('--im_path2', type=str, default='15.png', help='Structure image')
param_parser.add_argument('--im_path3', type=str, default='117.png', help='Appearance image')
param_parser.add_argument('--sign', type=str, default='realistic', help='realistic or fidelity results')
param_parser.add_argument('--smooth', type=int, default=1, help='dilation and erosion parame')
# StyleGAN2 setting
param_parser.add_argument('--size', type=int, default=1024)
param_parser.add_argument('--ckpt', type=str, default="pretrained_models/ffhq.pt")
param_parser.add_argument('--channel_multiplier', type=int, default=2)
param_parser.add_argument('--latent', type=int, default=512)
param_parser.add_argument('--n_mlp', type=int, default=8)
# Arguments
param_parser.add_argument('--device', type=str, default='cuda')
param_parser.add_argument('--seed', type=int, default=None)
param_parser.add_argument('--tile_latent', action='store_true', help='Whether to forcibly tile the same latent N times')
param_parser.add_argument('--opt_name', type=str, default='adam', help='Optimizer to use in projected gradient descent')
param_parser.add_argument('--learning_rate', type=float, default=0.01, help='Learning rate to use during optimization')
param_parser.add_argument('--lr_schedule', type=str, default='fixed', help='fixed, linear1cycledrop, linear1cycle')
param_parser.add_argument('--save_intermediate', action='store_true',
                    help='Whether to store and save intermediate HR and LR images during optimization')
param_parser.add_argument('--save_interval', type=int, default=400, help='Latent checkpoint interval')
param_parser.add_argument('--verbose', action='store_true', help='Print loss information')
param_parser.add_argument('--seg_ckpt', type=str, default='pretrained_models/seg.pth')
# Embedding loss options
param_parser.add_argument('--percept_lambda', type=float, default=1.0, help='Perceptual loss multiplier factor')
param_parser.add_argument('--l2_lambda', type=float, default=1.0, help='L2 loss multiplier factor')
param_parser.add_argument('--p_norm_lambda', type=float, default=0.001, help='P-norm Regularizer multiplier factor')
param_parser.add_argument('--l_F_lambda', type=float, default=0.5, help='L_F loss multiplier factor')
param_parser.add_argument('--W_steps', type=int, default=10, help='Number of W space optimization steps')
param_parser.add_argument('--FS_steps', type=int, default=150, help='Number of FS space optimization st')
# Alignment loss options
param_parser.add_argument('--ce_lambda', type=float, default=1.0, help='cross entropy loss multiplier factor')
param_parser.add_argument('--style_lambda', type=str, default=4e4, help='style loss multiplier factor')
param_parser.add_argument('--align_steps1', type=int, default=140, help='')
param_parser.add_argument('--align_steps2', type=int, default=1, help='')
# Blend loss options
param_parser.add_argument('--face_lambda', type=float, default=1, help='')
param_parser.add_argument('--hair_lambda', type=str, default=1.0, help='')
param_parser.add_argument('--blend_steps', type=int, default=400, help='')


# args = param_parser.parse_args()
# args.blend_steps = 100
# print(args.blend_steps)