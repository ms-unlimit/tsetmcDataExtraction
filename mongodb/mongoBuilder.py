import os
from mongodb.connectionUtils import ConnectionUtils


class MongoBuilder:

	"""
	A class to build mongo instance.

	...

	Attributes
	----------
	None
	"""

	def __init__(self):
		
		self.connection_utils = ConnectionUtils()

	@staticmethod
	def get_mongodb_config():
		"""
		Get Mongodb connection configuration to work 
		with data base.

		Args:
			None

		Returns:
			A Mongodb connection dict.
		"""

		mongodb_config = {

			"host": os.environ.get("MONGO_HOST") or "127.0.0.1",
			"port": os.environ.get("MONGO_PORT") or "27020",
			"user": os.environ.get("MONGO_USERNAME") or "test1",
			"pass": os.environ.get("MONGO_PASSWORD") or "test1",
			"name": os.environ.get("MONGO_NAME") or "testdb"
		}

		return mongodb_config

	def get_mongodb_collection(self, collection_name):
		"""
		Connect to Mongo database and select collection with
		predefined config variables and provided name.

		Args:
			collection_name: name of the desired collection

		Returns:
			A MongoClient collection object.
		"""

		config = self.get_mongodb_config()

		connection = self.connection_utils.connect(
			db_user=config["user"],
			db_pass=config["pass"],
			db_host=config["host"],
			db_port=config["port"],
			db_name=config["name"])

		collection = self.connection_utils.select_collection(
			connection=connection,
			db_name=config["name"],
			db_collection=collection_name)

		return collection
