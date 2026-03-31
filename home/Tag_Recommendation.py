import pandas as pd
from apyori import apriori




class HashTagRecommender:
	data = pd.DataFrame()
	def __init__(self, s):
		print(s)

	def read_data(self):
		users_r = pd.read_csv('Saved_Models/Fashion_Tags_rec.csv')
		print(users_r.shape)
		print(users_r.dtypes)

		return users_r

	def get_all_tags(self):
		fd = self.read_data()
		all_tags = fd.Fashion_Tag.unique().tolist()
		return all_tags

	def tag_segmentation(self):
		fd = self.read_data()
		gbt = fd.groupby('Fashion_Tag')

		return gbt

	def get_tagger_brand(self, TagName):
		gbt = self.tag_segmentation()
		tag_input = TagName
		# Finding the values contained in the "Boston Celtics" group 
		in_tag_group = gbt.get_group(tag_input)
		
		return in_tag_group

	def get_tagger_brands(self, tags_input):
		# brand name filtered by tags name
		fd = self.read_data()
		tag_filter_list = fd[fd['Fashion_Tag'] == tags_input]['Fashion_Choice'][:].unique().tolist()
		return tag_filter_list

	def get_tagger_brand_counts(self, tags_input):
		# brand name count by tags name overall
		fd = self.read_data()
		tag_filter_list_counter = fd[fd['Fashion_Tag'] == tags_input]['Fashion_Choice'].count()
		return tag_filter_list_counter

	def get_tagger_brand_distribution(self, tags_input):
		# brand name count individual by tags name 
		fd = self.read_data()
		tag_filter_list_counter_i = fd[fd['Fashion_Tag'] == tags_input]['Fashion_Choice'].value_counts()
		tag_filter_brands_list = tag_filter_list_counter_i.index.values.tolist()
		tag_filter_counter_list = tag_filter_list_counter_i.tolist()
		ncl = []
		for i, j in zip(tag_filter_brands_list, tag_filter_counter_list):
			nct = (i, j)
			ncl.append(nct)
		return (ncl, tag_filter_brands_list, tag_filter_counter_list)
