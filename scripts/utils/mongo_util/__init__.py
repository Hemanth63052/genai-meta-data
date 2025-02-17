from pymongo import MongoClient
from scripts.config import MongoDBConfig
from scripts.logging import logger


class MongoConnectionBaseClass:
    def __init__(self, database_name=None, collection_name=None):
        self.database_name = database_name  # Initialize here
        self.collection_name = collection_name  # Initialize here
        self.client = None # Add client attribute
        self.db = None # Add db attribute
        self.collection = None # Add collection attribute
        self.connect() # Call connect on initialization

    def connect(self):
        """Establishes the MongoDB connection."""
        try:
            self.client = MongoClient(MongoDBConfig.MONGODB_URI)
            self.db = self.client[f"{self.database_name}"]
            self.collection = self.db[self.collection_name]
        except Exception as e:
            logger.exception(f"Could not connect to MongoDB: {e}")

    def reconnect(self):
        """Re-establishes the MongoDB connection when project_id changes."""
        self.close()
        self.connect()

    def close(self):
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")


    def find_one(self, query, filters=None):
        return self.collection.find_one(query, filters)

    def find(self, query, filters=None):
        return self.collection.find(query, filters)

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def insert_many(self, data):
        return self.collection.insert_many(data)

    def update_one(self, query, data):
        return self.collection.update_one(query, data)

    def update_many(self, query, data):
        return self.collection.update_many(query, data)

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_many(self, query):
         return self.collection.delete_many(query)


    def __del__(self):
        self.close()


class MongoUtilConstants:
    configurations = "configurations"
    users = "users"
    user_details = "user_details"