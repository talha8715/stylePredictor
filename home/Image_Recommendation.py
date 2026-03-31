from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import matplotlib.image as mpimg
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os # accessing directory structure
import cv2
import PIL.Image
import pickle as pkl

import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
import keras
from keras import Model
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.preprocessing.image import load_img,img_to_array
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.layers import GlobalMaxPooling2D

from csv import writer
from csv import DictWriter

class Image_Recommendation_Model:
	def __init__(self, arg):
		print(arg)

	DATASET_PATH = "media/Recommender_Dataset"
	filenames = []


	def get_data(self):
		DATASET_PATH = self.DATASET_PATH

		df = pd.read_csv(DATASET_PATH + "/styles.csv", nrows=5000)
		df['image'] = df.apply(lambda row: str(row['id']) + ".jpg", axis=1)
		df = df.reset_index(drop=True)
		return df


	def img_path(self, img):
		return self.DATASET_PATH+"/images/"+img


	def load_images_from_folder(self):
	    images = []
	    folder = self.DATASET_PATH+"/images/"

	    for filename in os.listdir(folder):
	    	self.filenames.append(filename)


	def load_image(self, img, resized_fac = 0.1):
		img     = cv2.imread(self.img_path(img))
		w, h, _ = img.shape
		resized = cv2.resize(img, (int(h*resized_fac), int(w*resized_fac)), interpolation = cv2.INTER_AREA)
		return resized


	def load(self):
		with open('Saved_Models/Recommender_using_cnn.pkl', 'rb') as file:
			arr = pkl.load(file)
			return arr

	
	def get_recommender(self, idx, df, top_n = 6):
		arr = self.load()
		indices = pd.Series(range(len(df)), index=df.index)

		sim_idx    = indices[idx]
		sim_scores = list(enumerate(arr[sim_idx]))
		sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
		sim_scores = sim_scores[1:top_n+1]
		idx_rec    = [i[0] for i in sim_scores]
		idx_sim    = [i[1] for i in sim_scores]

		print("idx_rec: ", idx_rec)
		print("\n\nidx_sim: ", idx_sim)

		return (idx_rec, idx_sim)



	def rec_process(self, idx_ref):
		# idx_ref = 2994

		df = self.get_data()
		# print(df.head())
		# Recommendations
		idu = df.id.tolist()
		rfindl = []
		rfidl = []
		ind = ""
		iid = ""
		iurl = ""
		art = ""

		# field_names = ['index', 'id', 'img_url', 'articleType']
  #   # Open file in append mode
		# with open('C:/Users/Talha Javaid/Python/Python_Modules/django2/FYP/Saved_Models/input_rec_images.csv', 'a', newline='') as write_obj:
  #       # Create a writer object from csv module
		# 	dict_writer = DictWriter(write_obj, fieldnames=field_names)
  #       # Add dictionary as wor in the csv
			

		# 	# df1 = pd.read_csv('C:/Users/Talha Javaid/Python/Python_Modules/django2/FYP/Saved_Models/input_rec_images.csv', 'a')
		# 	for i in idu[:20000]:
		# 		# print(type(df[df['id'] == i]), df[df['id'] == i])
		# 		if not df[df['id'] == i].empty:
		# 			# rfindl.append(list(df[df['id'] == i].index))
		# 			ind = list(df[df['id'] == i].index)
		# 			ind = ind.pop()
		# 			iid = list(df[df['id'] == i].id)
		# 			print(iid)
		# 			iid = iid.pop()
		# 			iurl = list(df[df['id'] == i].image)

		# 			iurl = iurl.pop()
		# 			art = list(df[df['id'] == i].articleType)
		# 			art = art.pop()
		# 			# rfidl.append(list(df[df['id'] == i].id))
		# 			a = {'index': str(ind),'id': str(iid), 'img_url': str(iurl), 'articleType': str(art)}
		# 			# df2 = df1.append(a, ignore_index = True)
		# 			# print(a)
		# 			# print(df2)

		# 			dict_writer.writerow(a)


		# b = df2.to_csv(r'C:/Users/Talha Javaid/Python/Python_Modules/django2/FYP/Saved_Models/input_rec_images.csv', index = False)


		idx_refe = list(df[df['id'] == idx_ref].index)
		# idx_refe = [317]
		print(type(idx_refe), idx_refe)
		idx_refe = idx_refe.pop()
		idx_rec, idx_sim = self.get_recommender(idx_refe, df, top_n = 6)

		idx_rece = []

		for i in idx_rec:
			idx_rece.append(df.iloc[i].image)
		rec_im_sc_list = []

		for i, j in zip(idx_rece, idx_sim):
			t = (str(i), j)
			rec_im_sc_list.append(t)

		return rec_im_sc_list

