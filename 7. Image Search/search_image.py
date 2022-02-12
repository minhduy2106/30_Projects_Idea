#import lib

from ast import Mod
import re
from tkinter.tix import IMAGE
from turtle import distance
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

#define image to find
search_image = "dataset/4571.jpg"

#khoi tao model
model = get_extract_model()

#trich dac trung
search_vector = extract_vector(model, search_image)

#load 4700 vector from vector.pkl 
vectors = pickle.load(open("vector.pkl", "rb"))
paths = pickle.load(open("paths.pkl", "rb"))

#distance from search_vector to all vector
distance = np.linalg.norm(vectors - search_vector, axis=1)

#sap xep va lay ra K vector có khoảng cách ngắn nhất
K= 16
ids = np.argsort(distance)[:K]

#create output
nearest_image = [(paths[id], distance[id]) for id in ids]

#Draw to the screen that picture
import matplotlib.pyplot as plt
import math

axes = []
grid_size = int(math.sqrt(K))
fig = plt.figure(figsize=(10,5))

for id in range(K):
    draw_image = nearest_image[id]
    axes.append(fig.add_subplot(grid_size, grid_size, id+1))
    
    axes[-1].set_title(draw_image[1])
    plt.imshow(Image.open(draw_image[0]))

fig.tight_layout()
plt.show()