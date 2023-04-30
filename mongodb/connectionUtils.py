from pymongo import MongoClient, DESCENDING

class ConnectionUtils:

	"""
	A class contating a set of functionalities to 
	connect Mongo database

	...

	Attributes:
		None
	"""

	def __init__(self):

		pass

	def select_collection(self, connection, db_name: str, db_collection: str):
		"""
		Select and initiate a Mongo collection object to work with.

		Args:
			connection: A MongoClient connection object 
			db_name: Name of the Mongo database to select or create in case of absence
			db_collection: Name of the Mongo collection to select or create in case of absence

		Returns:
			MongoClient collection object
		"""

		db = connection[db_name]

		collection = db[db_collection]

		return collection

	def connect(self, db_user: str, db_pass: str, db_host: str, db_port: str, db_name: str):
		"""
		Initiate a connection to Mongo database.

		Args:
			db_user: Mongo database username
			db_pass: Mongo database password
			db_host: Mongo database host
			db_port: Mongo database port
			db_name: Mongo database name

		Returns:
			MongoClient connection object	
		"""

		uri = f"mongodb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

		connection = MongoClient(uri)

		return connection
