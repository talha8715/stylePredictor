import numpy as np
import pandas as pd
from PIL import Image
from PIL import ImageOps
import sys
import os
import requests
from io import BytesIO

from keras.models import load_model
from tensorflow.keras.models import model_from_json
import h5py



class Image_Classification_Model:
    def __init__(self, arg):
        print(arg)

    def gallery(self, url, result):
        df1 = pd.read_csv('Saved_Models/gallery.csv')
        a = {"URL": str(url), "RESULT": str(result)}
        df2 = pd.concat([df1, pd.DataFrame([a])], ignore_index=True)
        df2.to_csv('Saved_Models/gallery.csv', index=False)



    def resize(self, image_path):

        print("desired path: ", image_path)
        """
        Pick a basic color (Black) and pad the images that do not have a 1:1 aspect ratio.
        Reshape without stretching to a 128x128 pixel array shape
        """
        
        im = Image.open(image_path)

            
        desired_size = 128
        old_size = im.size  # old_size[0] is in (width, height) format

        ratio = float(desired_size)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])

        im = im.resize(new_size)
        
        # create a new image and paste the resized on it
        new_im = Image.new("RGB", (desired_size, desired_size))
        new_im.paste(im, ((desired_size-new_size[0])//2,
                            (desired_size-new_size[1])//2))

        delta_w = desired_size - new_size[0]
        delta_h = desired_size - new_size[1]
        padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
        new_im = ImageOps.expand(im, padding)

        filename, file_extension = os.path.splitext(image_path)
        new_filename = filename + "_resized.jpeg"
        new_im.save(new_filename, "JPEG")
        
        return new_filename


    def equalize_image(self, image_path): #"imagename_resized.JPEG"
        """
        Ensure for each image that the pixel range is [0,255] (constrast stretching)
        by applying the equalise method (normalise works also)
        """
        im = Image.open(image_path)

        # Equalize image
        im_out = ImageOps.equalize(im)
        
        # Save equalized image
        filename, file_extension = os.path.splitext(image_path) 
        new_filename = filename + "_equalized.jpeg"
        im_out.save(new_filename, "JPEG")
        
        return new_filename



    def image_to_array(self, image_path):
        """
        Input: Image path
        Output: Flatten array of 3x128x128 image pixels in range[0,255]
        """
        im = Image.open(image_path)
        return np.array(im, dtype=float)



    def label_decoder(self, key):
        label_mapping = {
            "1" : "Bagpack",
            "2" : "Jacket",
            "3" : "Kurti",
            "4" : "Pent",
            "5" : "Saree",
            "6" : "Shirt",
            "7" : "Shoes",
            "8" : "Sweater",
            "9" : "Watch",
        }
        return label_mapping[key]



    def run_model(self, data):

        # load json and create model
        json_file = open('Saved_Models/Classification_using_CNN.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("Saved_Models/Classification_using_CNN.h5")
        print("Loaded model from disk")


        result_array = loaded_model.predict(data).tolist()[0]
        
        # Get the position of the element 1.0 within the array
        index = result_array.index(max(result_array)) + 1
        
        # Decode results
        predicted_label = self.label_decoder(str(index))
        
        return predicted_label



    def predict_img(self, image_path):
        # Pre-process image
        print('Image :', image_path.split('/')[1])
        resized_image_path = self.resize(image_path)
        preprocessed_img_path = self.equalize_image(resized_image_path)

        # Converting image to Numpy array
        numpy_data = self.image_to_array(preprocessed_img_path)
        numpy_data = numpy_data.reshape(1, 3, 128, 128)

        # Predict label using Keras Mutli-Class model
        result_label = self.run_model(numpy_data)

        print('Predicted : ' + result_label + '\n')

        # Cleaning up
        os.remove(resized_image_path)
        os.remove(preprocessed_img_path)
        return result_label
