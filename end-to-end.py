import sys
sys.path.append('../code/')
import utils
import argparse
import audiofile as af
import os
parser = argparse.ArgumentParser(description='Audio Separation tool by GPA.')
parser.add_argument('model', type=str,
                    help='The model to be chosen. Must be one of the following: u_net_5_5, u_net_3_7, open_umx')
parser.add_argument('input', type=str,
                    help='The input audio path/filename. Must be .wav 44.1kHz.')
parser.add_argument('weights_file', type=str,
                    help='The weights path/filename.')

args = parser.parse_args()
print(args.model)
model = args.model
input_filename = args.input
weights_path = args.weights_file

if model== 'u_net_5_5':
    kernel_size=(5,5)
if model== 'u_net_3_7':
    kernel_size=(7,3)

model = utils.load_unet_spleeter(kernel_size,weights_path)
audio , fs = af.read(input_filename)
if fs!=44100:
    print("Audio must be 44.1 kHz. Exiting")
audio_vocal_pred = utils.separate_from_audio(audio,44100,model,wiener_filter=True)
audio_acc_pred = audio - audio_vocal_pred[0:len(audio)]
base_folder = './audio/'
basename = os.path.splitext(os.path.basename(input_filename))[0]

af.write(base_folder + basename + '_vocals_pred.wav',audio_vocal_pred,44100)
af.write(base_folder + basename + '_acc_pred.wav',audio_acc_pred,44100)
