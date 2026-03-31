
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import time
# from sklearn.externals import joblib
from . import Recommenders


class Text_Recommendation_Model:
	d = dict()
	ua = list()

	def __init__(self, r):
		print('Text_Recommendation')

	def read_data(self):

		tr_df = pd.read_csv('Saved_Models/Recommendation_Table.csv')
		return tr_df


	def pop_model(self):
		# load data
		tr_df = self.read_data()

		print(len(tr_df.user_id.unique().tolist()))
		print(len(tr_df.item_id.unique().tolist()))
		print(len(tr_df.Title.unique().tolist()))
		print(len(tr_df.Category.unique().tolist()))
 
		train_data, test_data = train_test_split(tr_df, test_size = 0.20, random_state=0)
		train_data.head(6)

		pm = Recommenders.popularity_recommender_py()
		pm.create(train_data, 'user_id', 'Category')
		
		users = tr_df['user_id'].unique()
		print(users)

		# for all users same category will display
		# so pick any user here i choosed 5th number user

		user_id = users[5]
		p_model = pm.recommend(user_id)
		t_items = p_model['Category'].tolist()[:6]
		t_scores = p_model['score'].tolist()[:6]
		t_ranks = p_model['Rank'].tolist()[:6]
		print(t_items, t_scores, t_ranks)
		p_model.head()

		return (t_items, t_scores, t_ranks)


	def user_model(self, u):
		# load data
		tr_df = self.read_data()

		train_data, test_data = train_test_split(tr_df, test_size = 0.30, random_state=80)
		train_data.head(6)

		is_model = Recommenders.item_similarity_recommender_py()
		is_model.create(train_data, 'user_id', 'Category')
		
		users = tr_df['user_id'].unique()

		user_id = users[u]
		# user_id = u

		print(u)
		user_items = is_model.get_user_items(user_id)
		print('\nuser_items: \n', user_items)

		print("------------------------------------------------------------------------------------")
		print(" Lets Training with fashion data  for the user userid: %s:" % user_id)
		print("------------------------------------------------------------------------------------")
				
		# By using user hostory (Past Interations with fashion) 

		u_hist = []
		for user_item in user_items:
			u_hist.append(user_item)

		print('\nuser_history: \n', len(u_hist), u_hist)

		uhr = []
		for i in user_items:
		    d = tr_df[ (tr_df['Category'] == i) & (tr_df['user_id'] == user_id) ] ['user_id']
		    r = d.shape
		    print(i, r[0])
		    uhr.append(r[0])

		u_hist, uhr = self.get_orderd_data(u_hist, uhr)

		print("----------------------------------------------------------------------")
		print("Recommendation process going on:")
		print("----------------------------------------------------------------------")
		    		
    	# print(user_item)
		#Recommend fashion for the user using personalized model

		u_model = is_model.recommend(user_id)
		t_items = u_model['Category'].tolist()[:6]
		t_scores = u_model['score'].tolist()[:6]
		t_ranks = u_model['rank'].tolist()[:6]
		t_scores_r = [ '%.2f' % elem for elem in t_scores ]
		print(t_items, t_scores_r, t_ranks)

		return (t_items, t_scores_r, t_ranks, u_hist, uhr)


	def get_orderd_data(self, n, r):
		tup = []
		for i, j in zip(n, r):
			t = (i, j)
			tup.append(t)
		print(tup)

	      
	    # getting length of list of tuples 
		lst = len(tup)  
		for i in range(0, lst):  
	          
			for j in range(0, lst-i-1):  
				if (tup[j][1] < tup[j + 1][1]):  
					temp = tup[j]  
					tup[j]= tup[j + 1]  
					tup[j + 1]= temp

		u_hist = []
		uhr = []
		for i in tup:
			
			u_hist.append(i[0])
			uhr.append(i[1])

		return (u_hist, uhr)


	def fashion_model(self, b):
		# load data
		tr_df = self.read_data()

		train_data, test_data = train_test_split(tr_df, test_size = 0.20, random_state=0)
		train_data.head(5)

		is_model = Recommenders.item_similarity_recommender_py()
		is_model.create(train_data, 'user_id', 'Category')

		b_name = b

		b_model = is_model.get_similar_items([b_name])
		print(b_name)
		#Recommend brands for the user selected brand using brand model
		t_items = b_model['Category'].tolist()[:6]
		t_scores = b_model['score'].tolist()[:6]
		t_ranks = b_model['rank'].tolist()[:6]
		
		t_scores_r = [ '%.2f' % elem for elem in t_scores ]
		print(t_items, t_scores_r, t_ranks)
		return (t_items, t_scores_r, t_ranks)


	def get_data(self):

		# load data

		tr_df = self.read_data()

		ubl = tr_df.Title.unique().tolist()
		bidl = tr_df.item_id.unique().tolist()

		itl = []
		for i, j in zip(ubl, bidl):
			bit = (i, j)
			itl.append(bit)

		ua = tr_df.Category.unique().tolist()
		d = dict()
		for i in ua:
		    iba = tr_df[tr_df['Category'] == i]['Title'].unique().tolist()
		    d[i] = iba
		    print(i, ": ", iba)
		
		print(d[ua[1]])

		
		self.ua = ua
		self.bidl = bidl  

		for i in bidl:

		    c = tr_df[tr_df['item_id'] == i]['Reaction_Count'].value_counts().tolist()
		    v = tr_df[tr_df['item_id'] == i]['Reaction_Count'].unique().tolist()
		    print(c, v)
		    d[i] = v

		self.d = d

		return (itl, d)


	# To make adaptive feed more liked brand user have
	def add_data(self, uid, sbl, sil):

		tr_df = self.read_data()

		for i, j in zip(sbl, sil):
			print(i, j)
			for k in range(len(self.ua)):
				if i in self.d[self.ua[k]]:
					ar = self.ua[k]

			cn = self.d[j][0]

			usd = {
			'user_id': str(uid), 'item_id': str(j), 'Reaction_Count': str(cn), 'Title': str(i), 'Category': str(ar),

			}

			# save the new update
			tr_df = tr_df.append(usd, ignore_index=True)

			print(usd)

		export_csv = tr_df.to_csv (r'Saved_Models/Recommendation_Table.csv', index = False, header=True)

		# dic = { 'user_id': 'U93', 'item_id': 'B21', 'Reaction_Count': '3', 'Title': 'Khaadi', 'Category': 'Formal' }
		# tr_df = tr_df.append(dic, ignore_index=True)




# if __name__ == '__main__':
# 	main()