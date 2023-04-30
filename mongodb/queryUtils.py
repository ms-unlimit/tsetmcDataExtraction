from pymongo import DESCENDING, errors

class QueryUtils:

	"""
	pass
	"""

	def __init__(self, collection):
		self.collection = collection

	def fetch_docs(self, num_docs: int):
		response = list(self.collection.find({"Panel Code": "5"}).limit(num_docs))
		return response

	def inserertDF(self, df):
		response = self.collection.insert_many(df.to_dict('records'))
		return response

	def StockLastData(self, stock):
		response = list(self.collection.find({"Ticker": stock}).sort('Date', -1).limit(1))
		return response
