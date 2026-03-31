import pandas as pd
from numpy import *
import pickle as pkl
import numpy as np
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import neighbors

class Text_Classification_Model:
    def __init__(self, arg):
        print("Text Based Classfier: ", arg)

    df = pd.DataFrame()

    # load data 

    def load_txt_model(self):
        Pkl_Filename = "Saved_Models/fp_lr.pkl"
        with open(Pkl_Filename, 'rb') as file:
            fp = pkl.load(file)

        return fp


    def predict_fashion_style(self, ud):

        f = self.load_txt_model()
        
        udx = np.array([ud])
        r = f.predict(udx)
        usY = r[0]

        print("Predicted Fashion Style: ", usY)
        return usY


    def load_txt_model_event(self):
        Pkl_Filename = "Saved_Models/fp_lr_event.pkl"
        with open(Pkl_Filename, 'rb') as file:
            fp = pkl.load(file)

        return fp


    def predict_fashion_style_event(self, ud):

        f = self.load_txt_model_event()
        
        udx = np.array([ud])
        r = f.predict(udx)
        usY = r[0]

        print("predicted Event: ", usY)
        return usY


    def load_txt_model_dress(self):
        Pkl_Filename = "Saved_Models/fp_lr_dress.pkl"
        with open(Pkl_Filename, 'rb') as file:
            fp = pkl.load(file)

        return fp


    def predict_fashion_style_dress(self, ud):

        f = self.load_txt_model_dress()
        
        udx = np.array([ud])
        r = f.predict(udx)
        usY = r[0]

        print("predicted Dress: ", usY)
        return usY



# def main():
# 	fp = predict_dress(" Dress predictor module object!")
# 	fp.laod_txt_model()
#     ud = [0, 22, 3, 2, 7, 8, 3]
#     fp.predict_fashion_style(ud)

# if __name__ == '__main__':
# 	main()
