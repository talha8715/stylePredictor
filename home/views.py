from .Image_Classification import Image_Classification_Model
from .Text_Classification import Text_Classification_Model
from .Text_Content_Classification import Text_Content_Class
from .Image_Recommendation import Image_Recommendation_Model
from .Text_Recommendation import Text_Recommendation_Model
from .Tag_Recommendation import HashTagRecommender
from .Data_Visualization import DataVisulaizer

from django.shortcuts import render, redirect
import numpy as np
from numpy import asarray
import pandas as pd
import json

from keras.preprocessing import image
from keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import default_storage
import os
from PIL import Image

from django.contrib.auth.models import User
from .models import UserModal, FashionModel, PlanModel

from django.conf import settings
from keras.applications import vgg16
import datetime


def index1(request):
	dv = DataVisulaizer('To visualize the data!')
	bn, bc, bm = dv.get_mc_rating()

	bns = json.dumps(bn)
	bcs = json.dumps(bc)
	bms = json.dumps(bm)

	uid = request.user.id
	r = Text_Recommendation_Model('My Brand recommender!')
	x, y = dv.get_data()
	a, b, c, d, e = r.user_model(uid)

	ubn = json.dumps(d)
	uhr = json.dumps(e)

	if request.method == 'POST':
		for i, j in x:
			h = request.POST.get(j)
			if h is not None:
				pass

		return render(request, 'visuals1.html', {
			'bn': bns,
			'bc': bcs,
			'bm': bms,
			'ubn': ubn,
			'uhr': uhr,
		})
	else:
		x, y = dv.get_data()

	return render(request, 'Home.html', {
		'bn': bns,
		'bc': bcs,
		'bm': bms,
		'ubn': ubn,
		'uhr': uhr,
	})

# def add_data(request):
#     # if request.session['u_type']:
#     #     del request.session['u_type']
# # take user ID selection of one user out of all users
#     u_type = request.POST.get("choice", None)
#     print("....user type value: ", 'U' + str(u_type))
#     request.session['u_type'] = u_type
#     request.session['uid'] = request.user.id
#     return redirect('ind')


def gallery(request):
	df1 = pd.read_csv('Saved_Models/gallery.csv')
	data = []
	u = df1.URL.tolist()
	r = df1.RESULT.tolist()
	for i,j in zip(u, r):
		tup = (i, j)
		data.append(tup)
	return render(request, "Gallery.html", {"data": data} )

#..................................................................

def imgPredictor(request):

	if request.method == "POST":
		up = request.POST.get('upload_img')

		if up is not None:

			f = request.FILES.get('user_image')

			obj = Image_Classification_Model("Image Classifier")

			file_name = "pic.jpg"
			file_name_2 = default_storage.save(file_name, f)
			file_url = default_storage.url(file_name_2)
			furl = '.'+ file_url

			result = obj.predict_img(furl)
			obj.gallery(furl, result)

			return render(request,"Image_Classification.html",{"result": result, 'img_url': file_url})
	else:
		return render(request,"Image_Classification.html") 

# ...............................................................

def userDetails(request):

	r = request.user.id

	cu = User.objects.only('id').get(id = r)

	if request.method == 'POST':
		A = request.POST.get('area')
		C = request.POST.get('city')
		O = request.POST.get('occupation')

		G = request.POST.get('gender')
		E = request.POST.get('education')
		a = request.POST.get('age')

		print(A,C,O,G,E,a)

		um = UserModal.objects.create(user = cu, area = A, city = C, occupation = O, gender = G, education = E, age = a)
		um.save()
		return render(request,"UDetails.html",{"um":um, "A":A, "C":C, "G":G, "O":O, "E":E, "a":a })

	else:
		um = UserModal.objects.all()
		return render(request,"UDetails.html",{"um":um})

#...................................................................

def fashionDetails(request):

	sp = request.POST.get('Submit_p')

	if sp is not None:

		r = request.user.id

		cu = User.objects.only('id').get(id = r)

		F = request.POST.get('fashion_consious')
		B = request.POST.get('brand_consious')
		FC = request.POST.get('fav_color')

		FDT = request.POST.get('fav_dressing_type')
		FD = request.POST.get('fav_design')

		print(F,B,FC,FDT,FD)

		fs = FashionModel.objects.create(user = cu, fashion_consious = F, brand_consious = B, fav_color = FC, fav_dressing_type = FDT, fav_design = FD)
		fs.save()

		return render(request,"FDetails.html",{"fs": fs, "F":F, "B":B, "FC":FC, "FDT":FDT, "FD":FD })  
	else:
		um = FashionModel.objects.all() 

		return render(request,"FDetails.html",{"um":um})

#...................................................................

def planDetails(request):
	todos = PlanModel.objects.all()
	if request.POST:
		if "taskAdd" in request.POST:

		    r = request.user.id

		    cu = User.objects.only('id').get(id = r)

		    tt = request.POST.get('title')

		    d = request.POST.get('date')
		    t = request.POST.get('time')
		    e = request.POST.get('event')
		    pt = request.POST.get('priority')

		    content = tt + " -- " + t + " " + e

		    pp = PlanModel.objects.create(user = cu,title = tt, due_date = d, time = t, event = e,priority = pt, content=content)
		    pp.save()
		    # return redirect("/")

		if "taskDelete" in request.POST: #checking if there is a request to delete a todo
			checked = request.POST.get("checkedbox") #checked todos to be deleted
			# for u in checkedlist:
			todo = PlanModel.objects.get(id=int(checked)) #getting todo id
			todo.delete() #deleting todo
		return render(request,"PDetails.html",{"todos": todos})
	else:

		pp = User.objects.all()
		return render(request,"PDetails.html",{"pp":pp, "todos": todos})

#...................................................................

def imgRecommender(request):
	if request.method == "POST":
		up = request.POST.get('Submit')

		if up is not None:
			print("submitted")

			f = request.POST['user_image']
			# 
			print('\n\n\n\t\trec image: ', f)

			recom = Image_Recommendation_Model('Recommend Images')
			print('\n\n\n\nget images\n')
			id_score_list = recom.rec_process(int(f))

			print(id_score_list)

			return render(request,"Image_Recommendation.html", {'id_score_list': id_score_list })
	else:
		return render(request,"Image_Recommendation.html")


#...................................................................

def textClassifier(request):

		if request.POST:

			# Fashion Prediction
			if request.POST.get('Submit_1'):

				g = request.POST.get('gender')
				a = request.POST.get('age')
				f = request.POST.get('fabric')
				c = request.POST.get('color')
				q = request.POST.get('quality')
				cm = request.POST.get('comfort')
				b = request.POST.get('brand')

				a = int(a)
				f = int(f)
				c = int(c)
				q = int(q)
				cm = int(cm)
				b = int(b)

				if g =="Male":
					g = 1
				else:
					g = 0


				ud = [g, a, f, c, q, cm, b]

				fp = Text_Classification_Model(" Dress predictor module object!")
				target = fp.predict_fashion_style(ud)

				return render(request,"Text_Classification.html",{"target":target})


			# Event Prediction
			if request.POST.get('Submit_2'):

				g = request.POST.get('gender')
				a = request.POST.get('age')
				f = request.POST.get('profession')
				c = request.POST.get('education')
				q = request.POST.get('weather')
				cm = request.POST.get('culture')
				b = request.POST.get('style')

				a = int(a)
				f = int(f)
				c = int(c)
				q = int(q)
				cm = int(cm)
				b = int(b)

				if g =="Male":
					g = 1
				else:
					g = 0


				ud = [g, a, f, c, q, cm, b]

				fp = Text_Classification_Model(" Dress predictor module object!")
				target2 = fp.predict_fashion_style_event(ud)

				return render(request,"Text_Classification.html",{"target2":target2})


			# Dress Prediction
			if request.POST.get('Submit_3'):

				g = request.POST.get('gender')
				a = request.POST.get('age')
				f = request.POST.get('comfort')
				c = request.POST.get('color')
				q = request.POST.get('quality')
				cm = request.POST.get('etype')
				b = request.POST.get('epriority')

				a = int(a)
				f = int(f)
				c = int(c)
				q = int(q)
				cm = int(cm)
				b = int(b)

				if g =="Male":
					g = 1
				else:
					g = 0


				ud = [g, a, f, c, q, cm, b]

				fp = Text_Classification_Model(" Dress predictor module object!")
				target3 = fp.predict_fashion_style_dress(ud)

				return render(request,"Text_Classification.html",{"target3":target3})

		else:
			return render(request,"Text_Classification.html")

#.........................................................................

def textRecommender(request):

	df = pd.read_csv('Saved_Models/Recommendation_Table.csv')
	cat = df.Category.unique()
	cat = cat.tolist()
	cat = cat[:40]
	r = Text_Recommendation_Model('My Fashion Recommender!')

	a, b, c = r.pop_model()
	arr = []
	for i,j,k in zip(a,b,c):
		tup = (i,j,k)
		arr.append(tup)

	ui = request.user.id
	d, e, f, hs, hr = r.user_model(int(ui))
	urr = []
	for i,j,k in zip(d,e,f):
		tup = (i,j,k)
		urr.append(tup)
	urr = urr[:3]

	if request.method == "POST":
		# up = request.POST.get('Submit2')
		up3 = request.POST.get('Submit3')

		if up3 is not None:
			print("submitted")

			f = request.POST['skills']
			u_item = f
			# 
			print('\n\n\n\t\tCategory: ', f)
			g, h, i = r.fashion_model(f)
			frr = []
			for i,j,k in zip(g,h,i):
				tup = (i,j,k)
				frr.append(tup)
			print(frr)
			return render(request, "Text_Recommendation.html",{"u_item": u_item, "arr": arr, "cat": cat, "frr": frr, "urr": urr})
	else:
		return render(request, "Text_Recommendation.html",{"arr": arr, "cat": cat, "urr": urr})

#.......................................................................

def tagRecommender(request):

	df = pd.read_csv('Saved_Models/fashions_tags.csv')
	t = df.Fashion_Tags.unique()
	t = t.tolist()
	# cat = cat[:40]
	tag_based = HashTagRecommender("Hash Tag Recommender")

	if request.method == "POST":
		# up = request.POST.get('Submit2')
		up = request.POST.get('Submit')

		if up is not None:
			print("submitted")

			f = request.POST['skills']

			all_tags = tag_based.get_all_tags()

			input_tag = f

			print('\n\n\n\tTag: ', f)
			tag_brand_list = tag_based.get_tagger_brands(input_tag)
			tag_brand__total_counts = tag_based.get_tagger_brand_counts(input_tag)

			ncl, fashion_names, fashion_tag_counts = tag_based.get_tagger_brand_distribution(input_tag)
			
			ncl = ncl[:6]
			# print(fashion_names[:5])
			# print(fashion_tag_counts[:5])
			return render(request, "Tag_Recommendation.html",{"t": t, "ncl": ncl})
	else:
		return render(request, "Tag_Recommendation.html",{"t": t})

#.......................................................................

def contentClassify(request):

	df = pd.read_csv('Saved_Models/Text_Similarity.csv')

	if request.method == "POST":
		tp = request.POST.get('type')
		up = request.POST.get('cat')
		query = up or tp
		if query:
			r = Text_Content_Class('r')
			r.rec_pipeline()
			rl = r.recommend_fashion(str(query), 5)
			return render(request, "Content_Classification.html", {'rl': rl})

	return render(request, "Content_Classification.html")