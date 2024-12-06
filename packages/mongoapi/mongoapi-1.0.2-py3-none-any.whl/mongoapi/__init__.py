from pymongo import MongoClient, ASCENDING
import datetime
from urllib.parse import urlparse,quote_plus


class mongoapi:
    def __init__(self, mongodb_url, name):
        self.name = name
        parsed_url = urlparse(mongodb_url)
        self.dbname = parsed_url.path.split('?')[0].lstrip('/')

        # MongoDB connection setup
        self.client = MongoClient(mongodb_url)

    def _get_collection(self):
        """Helper method to get the MongoDB collection."""
        return self.client[self.dbname][self.name]


    def put(self, items):
        """Insert or update items in the collection."""
        if isinstance(items, dict):
            items = [items]
        elif not isinstance(items, list):
            raise ValueError("Items must be a dictionary or a list of dictionaries")

        collection = self._get_collection()
        collection.create_index([("expireAt", ASCENDING)], expireAfterSeconds=0)
        collection.create_index([("key", ASCENDING)], unique=True)

        for item in items:

            if not isinstance(item, dict) or 'key' not in item:
                raise ValueError(f"Invalid item format: {item}")
            if '__expires' in item:
                item['expireAt'] = datetime.datetime.utcfromtimestamp(item['__expires'])

            collection.update_one(
                {'key': item['key']},  # Find item by key
                {'$set': item},        # Update the item
                upsert=True            # Insert if it doesn't exist
            )
        return True

    def get(self, key):
        """Retrieve an item by key."""
        collection = self._get_collection()
        current_time = datetime.datetime.now(datetime.UTC)

        item = collection.find_one({"key": key})
        if item:
            if 'expireAt' in item and item['expireAt'] < current_time:
                collection.delete_one({"key": key})
                return False  # Item expired and removed
            item.pop('_id', None)  # Remove MongoDB internal ID
            return item
        else:
            return False  # Item not found

    def patch(self, key, updates):
        """Update specific fields in an item."""
        collection = self._get_collection()
        result = collection.update_one({"key": key}, {'$set': updates})

        if result.matched_count:
            return True
        else:
            return False  # Item not found

    def delete(self, key):
        """Delete an item by key."""
        collection = self._get_collection()
        result = collection.delete_one({"key": key})

        if result.deleted_count:
            return True
        else:
            return False  # Item not found

    def get_all(self):
        """Retrieve all non-expired items."""
        collection = self._get_collection()
        current_time = datetime.datetime.now(datetime.UTC)

        # Remove expired items
        collection.delete_many({'expireAt': {'$lt': current_time}})

        items = collection.find({
            '$or': [
                {'expireAt': {'$exists': False}},  # No expiry
                {'expireAt': {'$gte': current_time}}  # Not expired
            ]
        })

        return [
            {key: value for key, value in item.items() if key != '_id'}
            for item in items
        ]

    def delete_all(self):
        """Delete all items in the collection."""
        collection = self._get_collection()
        result = collection.delete_many({})
        return f"Deleted {result.deleted_count} items"






def mongodb_url(username, password, dbname, host, port=27017):
    # Escape username and password
    username = quote_plus(username)
    password = quote_plus(password)
    
    return f"mongodb://{username}:{password}@{host}:{port}/{dbname}"




