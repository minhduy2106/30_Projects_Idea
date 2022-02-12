#import lib

from ast import Mod
import re
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model

from PIL import Image
import pickle
import numpy as np
import os

#Def create model

def get_extract_model():
    vgg16_model = VGG16(weights="imagenet")
    extract_model = Model(inputs=vgg16_model.inputs, outputs = vgg16_model.get_layer("fc1").output)
    return extract_model

#Def convert image to tensor
def image_processing(img):
    img = img.resize((224,224))
    img = img.convert("RGB")
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def extract_vector(model, image_path):
    print("Processing : ", image_path)
    img = Image.open(image_path)
    img_tensor = image_processing(img)

    #feature extract
    vector = model.predict(img_tensor)[0]
    #vector normalization
    vector = vector/np.linalg.norm(vector)
    return vector

#define folder data
data_folder = "dataset"

#create model
model = get_extract_model()

vectors = []
paths = []

for image_path in os.listdir(data_folder):
    # Noi full path
    image_path_full = os.path.join(data_folder, image_path)
    #Trich dac trung
    image_vector = extract_vector(model, image_path_full)
    #Add dac trung va fullpath vao list
    vectors.append(image_vector)
    paths.append(image_path_full)

#save file
vector_file = "vector.pkl"
path_file = "paths.pkl"

pickle.dump(vectors, open(vector_file, "wb"))
pickle.dump(paths, open(path_file, "wb"))