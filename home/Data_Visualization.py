import pandas as pd


# Show graphs and feed user like

class DataVisulaizer:
	data = pd.DataFrame()
    
	d = dict()
	ua = list()

	def __init__(self, s):
		print(s)

	def read_data(self):
		users_r = pd.read_csv('Saved_Models/Recommendation_Table.csv')
		# users_r = pd.read_csv('ui.csv')
		print(users_r.head(5))
		print(users_r.shape)
		print(users_r.dtypes)

		self.data = users_r

		return users_r

	def get_mc_rating(self):

		users_r = self.read_data()
		ul = users_r.Title.unique().tolist()
		
		bmrl = users_r.groupby(['Title'])['Reaction_Count'].mean()
		bcrl = users_r.groupby(['Title'])['Reaction_Count'].count()

		bnl = bmrl.index.tolist()
		print(bnl)
		
		mrl = []
		for i in bmrl.tolist():
			mrl.append(round(i,2))

		print(mrl)
		bcl = bcrl.tolist()
		print(bcl)


		return (bnl[:], bcl[:], mrl[:])

#     ..........................................

####################################################################

# for add data in csv file every time user like various fashion articles

	def get_data(self):

		# load data

		ubi_df = self.read_data()

		ubl = ubi_df.Title.unique().tolist()
		bidl = ubi_df.item_id.unique().tolist()

		itl = []
		for i, j in zip(ubl, bidl):
			bit = (i, j)
			itl.append(bit)

		ua = ubi_df.Category.unique().tolist()
		d = dict()
		for i in ua:
		    iba = ubi_df[ubi_df['Category'] == i]['Title'].unique().tolist()
		    d[i] = iba
		    print(i, ": ", iba)
		
		print(d[ua[1]])

		
		self.ua = ua
		self.bidl = bidl  

		for i in bidl:

		    c = ubi_df[ubi_df['item_id'] == i]['Reaction_Count'].value_counts().tolist()
		    v = ubi_df[ubi_df['item_id'] == i]['Reaction_Count'].unique().tolist()
		    print(c, v)
		    d[i] = v

		self.d = d

		return (itl, d)


# To make adaptive feed more liked brand user have
	def add_data(self, uid, sbl, sil, cn):

		ubi_df = self.read_data()

# 		for i, j in zip(sbl, sil):
# 			print(i, j)
# 			for k in range(len(self.ua)):
# 				if i in self.d[self.ua[k]]:
# 					ar = self.ua[k]

# 			cn = self.d[j][0]
            

		usd = {
		'user_id': str(uid), 'item_id': str(sbl), 'Reaction_Count': str(cn), 'Title': str(sil)

		}

		# save the new update
		ubi_df = ubi_df.append(usd, ignore_index=True)

		print(usd)

		export_csv = ubi_df.to_csv (r'Saved_Models/Recommendation_Table.csv', index = False, header=True)

# dv = DataVisulaizer("To Visulaize the data!")
# dv.read_data()
# dv.get_mc_rating()
# dv.get_data()
# dv.add_data(1, 2, 'Formal', 4)