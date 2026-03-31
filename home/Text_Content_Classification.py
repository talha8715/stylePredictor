import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Text_Content_Class:
	"""docstring for Classrecommend"""
	inputdata=pd.DataFrame()
	data=pd.DataFrame()
	tfidf_matrix=pd.DataFrame()
	cosine_similarities=pd.DataFrame()
	results=pd.DataFrame()
	lost=pd.DataFrame()
	idl = []
	list_r = dict()
	# reslt=pd.dictionary
 
	def __init__(self, arg):
		self.arg = arg

	def read_file(self):

		ds = pd.read_csv("Saved_Models/Text_Similarity.csv")
		self.data = ds
		self.idl = ds.idl.tolist()
		return ds
# 		td = pd.DataFrame()
	def get_data(self, ds):

		td = ds.copy()
		tdata = td[:15000]
		tdata['combined'] = tdata['masterCategory'] + ' ' + tdata['gender'] + ' ' + tdata['articleType'] + ' ' + tdata['season'] + ' ' + tdata['usage'] + ' ' + tdata['productDisplayName'] + ' ' + tdata['baseColour']

		self.inputdata=tdata

	def find_tfidf(self):
		tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0.01, max_df=0.3, stop_words='english')
		tfidf_matrix = tf.fit_transform(self.inputdata['combined'])
		self.tfidf_matrix=tfidf_matrix

	def find_cosinesimilarity(self):
		cosine_similarities = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
		results = {}
		for idx, row in self.inputdata.iterrows():
		    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
		    similar_items = [(cosine_similarities[idx][i], self.inputdata.index[i]) for i in similar_indices]
		    results[row['idl']] = similar_items[1:]
		    self.results=results
    
		self.cosine_similarities=cosine_similarities
		print(type(results), results[0])
		with open("Saved_Models/results.json", "w") as fp:
			json.dump(results , fp) 
		# json_result = json.dumps(results.to_dict('records'))

        
	# matching record
	# [0] store value does not create list within list
	def item(self,id):
		 return self.inputdata.loc[self.inputdata['idl'] == id]['combined'].tolist()[0].split(' - ')[0]
	

	def recommend_fashion(self,item_id, num):
	    #print("Recommending " + str(num) + " products similar to " + self.item(item_id) + "...")
	    # print("-------")

	    list_r = self.list_r
	    print(type(list_r))

	    # if list_r is None:
	    	# load from file again
	    	# ..


	    with open("Saved_Models/Similarity.json", "r") as fp:
	    	list_r = json.load(fp)
	    	self.list_r = list_r
	    	print(type(list_r))
	    	# print(list_r)

    	# else:
    		# use existing loaded
    		# .. 
	    #alist_r = list_r["0"][:]
	    recs = list_r[item_id][:num]


	# recs = self.results[item_id][:num]
	# print(recs)
	    lst=[]
	    ids_list=[]
	    for rec in recs:
	    	ids_list.append(rec[1])
	    	print("Recommended: " + self.item(rec[1]) + " (score:" + str(rec[0]))
	    	p=(self.item(rec[1])  , str(rec[0]))
	    	lst.append(p)


	    return lst


	def filter_prepare(self):
# remove this category
		# dfv = dfs[dfs.subCategory == 'Innerwear']
		# dfvl = dfv.index.tolist()
		# print(dfvl[:10])
		# print(dfv.shape[0])
		rfl = []
		for i in self.idl:
			# for j in dfvl:
			# 	if i == j:
			# 		pass
			# 	else:
			# 		rfl.append(i)

			rfl.append(self.ds.iloc[i]['id'])

		return rfl

	def rec_pipeline(self):
		ds = self.read_file()
		self.get_data(ds)
		# self.find_tfidf()
		# self.find_cosinesimilarity()

# .......................................

# def main():
# 	r = Text_Content_Class('r')
# 	# r.rec_pipeline()
# 	rl = r.recommend_fashion(11975, 5)
# 	print(rl)

# if __name__ == '__main__':
# 	main()