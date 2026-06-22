from .Image_Classification import Image_Classification_Model
from .Text_Classification import Text_Classification_Model
from .Text_Content_Classification import Text_Content_Class
from .Image_Recommendation import Image_Recommendation_Model
from .Text_Recommendation import Text_Recommendation_Model
from .Tag_Recommendation import HashTagRecommender
from .Data_Visualization import DataVisulaizer

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
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
from .models import (
	UserProfile, UserFashionPreference, EventPlan,
	GalleryImage,
	ImagePredictionLog, ImageRecommendationLog,
	TextPredictionLog, TextRecommendationLog,
	TagRecommendationLog, ContentSimilarityLog,
)

from django.conf import settings
from keras.applications import vgg16
import datetime

from .ChatbotEngine import FashionChatbotEngine


def index1(request):
	dv = DataVisulaizer('graphs')

	# Graph 1: User growth by month
	ug_labels, ug_counts = dv.get_user_growth()
	# Graph 2: Image prediction label distribution
	pred_labels, pred_counts = dv.get_prediction_label_counts()
	# Graph 3: Event plan distribution
	ep_labels, ep_counts = dv.get_event_plan_distribution()
	# Graph 4: Plan source split (manual vs stylebot)
	ps_labels, ps_counts = dv.get_plan_source_split()
	# Graph 5: Fashion color preference
	fp_labels, fp_counts = dv.get_fashion_preferences()
	# Graph 6: StyleBot daily sessions
	sb_labels, sb_counts = dv.get_stylebot_activity()

	ctx = {
		'ug_labels': json.dumps(ug_labels),
		'ug_counts': json.dumps(ug_counts),
		'pred_labels': json.dumps(pred_labels),
		'pred_counts': json.dumps(pred_counts),
		'ep_labels': json.dumps(ep_labels),
		'ep_counts': json.dumps(ep_counts),
		'ps_labels': json.dumps(ps_labels),
		'ps_counts': json.dumps(ps_counts),
		'fp_labels': json.dumps(fp_labels),
		'fp_counts': json.dumps(fp_counts),
		'sb_labels': json.dumps(sb_labels),
		'sb_counts': json.dumps(sb_counts),
	}
	return render(request, 'Home.html', ctx)

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
	items = GalleryImage.objects.all().order_by('-created_at')
	data = [(item.image_url, item.predicted_label) for item in items]
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
			GalleryImage.objects.create(
				predicted_label=str(result),
				image_url=file_url,
				uploaded_by=request.user if request.user.is_authenticated else None,
			)
			ImagePredictionLog.objects.create(
				user=request.user if request.user.is_authenticated else None,
				image_path=file_url,
				predicted_label=str(result),
			)
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
		um = UserProfile.objects.create(user=cu, area=A, city=C, occupation=O, gender=G, education=E, age=a)
		return render(request,"UDetails.html",{"um":um, "A":A, "C":C, "G":G, "O":O, "E":E, "a":a })

	else:
		um = UserProfile.objects.all()
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

		fs = UserFashionPreference.objects.create(user=cu, fashion_conscious=F, brand_conscious=B, fav_color=FC, fav_dressing_type=FDT, fav_design=FD)

		return render(request,"FDetails.html",{"fs": fs, "F":F, "B":B, "FC":FC, "FDT":FDT, "FD":FD })  
	else:
		um = UserFashionPreference.objects.all()

		return render(request,"FDetails.html",{"um":um})

#...................................................................

def planDetails(request):
	todos = EventPlan.objects.all()
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

		    EventPlan.objects.create(user=cu, title=tt, due_date=d, time=t, event=e, priority=pt, content=content, source='manual')
		    # return redirect("/")

		if "taskDelete" in request.POST: #checking if there is a request to delete a todo
			checked = request.POST.get("checkedbox") #checked todos to be deleted
			# for u in checkedlist:
			todo = EventPlan.objects.get(id=int(checked))
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

			ImageRecommendationLog.objects.create(
				user=request.user if request.user.is_authenticated else None,
				input_image_id=int(f),
				recommended_item_ids=[s[0] for s in id_score_list] if id_score_list else [],
			)
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
				TextPredictionLog.objects.create(
					user=request.user if request.user.is_authenticated else None,
					prediction_type='dress_category',
					input_features=ud,
					predicted_label=str(target),
				)
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
				TextPredictionLog.objects.create(
					user=request.user if request.user.is_authenticated else None,
					prediction_type='event',
					input_features=ud,
					predicted_label=str(target2),
				)
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
				TextPredictionLog.objects.create(
					user=request.user if request.user.is_authenticated else None,
					prediction_type='dress',
					input_features=ud,
					predicted_label=str(target3),
				)
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
			TextRecommendationLog.objects.create(
				user=request.user if request.user.is_authenticated else None,
				query_category=f,
				recommendation_type='category_based',
				recommended_items=[r[0] for r in frr],
			)
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
			TagRecommendationLog.objects.create(
				user=request.user if request.user.is_authenticated else None,
				tag_input=input_tag,
				matched_fashion_choices=tag_brand_list[:20],
				total_count=int(tag_brand__total_counts),
			)
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
			ContentSimilarityLog.objects.create(
				user=request.user if request.user.is_authenticated else None,
				query_text=str(query),
				similar_items=[item[0] for item in rl] if rl else [],
			)
			return render(request, "Content_Classification.html", {'rl': rl})

	return render(request, "Content_Classification.html")


@login_required
def chatbot_page(request):
	if 'chat_history' not in request.session:
		request.session['chat_history'] = []
	request.session.modified = True
	return render(request, "Chatbot.html", {
		'welcome_message': "Hi! I am StyleBot. Ask me about outfits, events, colors, or planning your event.",
	})


@login_required
@require_POST
def chatbot_message(request):
	try:
		payload = json.loads(request.body.decode('utf-8'))
	except Exception:
		return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

	user_message = (payload.get('message') or '').strip()
	if not user_message:
		return JsonResponse({'error': 'Message is required.'}, status=400)

	history = request.session.get('chat_history', [])
	engine = FashionChatbotEngine()
	reply, updated_history, plan_save_result = engine.process_message(history, user_message, request.user)

	request.session['chat_history'] = updated_history
	request.session.modified = True

	return JsonResponse({
		'reply': reply,
		'plan_saved': bool(plan_save_result),
		'plan': plan_save_result,
	})


@login_required
@require_POST
def chatbot_reset(request):
	request.session['chat_history'] = []
	request.session.modified = True
	return JsonResponse({
		'message': "Chat reset complete. Hi! I am StyleBot. How can I help with your event outfit today?"
	})