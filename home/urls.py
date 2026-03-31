from django.urls import include, path
from . import views


urlpatterns = [
	path('', views.index1, name='Home'),
	path('userDetails', views.userDetails, name='userDetails'),
	path('fashionDetails', views.fashionDetails, name='fashionDetails'),
	path('planDetails', views.planDetails, name='planDetails'),
	path('gallery', views.gallery, name='gallery'),
	path('imgPredictor', views.imgPredictor, name='imgPredictor'),
	path('imgRecommender', views.imgRecommender, name='imgRecommender'),
	path('textClassifier', views.textClassifier, name='textClassifier'),
	path('textRecommender', views.textRecommender, name='textRecommender'),
	path('tagRecommender', views.tagRecommender, name='tagRecommender'),
	path('contentClassify', views.contentClassify, name='contentClassify'),
]