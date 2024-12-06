
# MongoAPI

**MongoAPI** is a Python package designed to simplify MongoDB operations. This tool provides an intuitive interface for interacting with MongoDB collections, including features like CRUD operations, TTL (Time-To-Live) indexing, and automatic expiration handling.

<br>

## Installation

To install MongoAPI, use pip:

```bash
pip install mongoapi
```

or install directly from the GitHub repository:

```bash
pip install git+https://github.com/rekcah-pavi/mongoapi
```

---

## Features

- **CRUD Operations:** Easily perform Create, Read, Update, and Delete actions on MongoDB documents.
- **Expiration Handling:** Automatically manage document expiration with the `__expires` field.
- **Indexing:** Supports unique key indexing and TTL indexing for automatic cleanup of expired documents.
- **Lightweight Dependency:** Built with `pymongo` for efficient database interaction.

---

## Usage

### Initialize the API

```python
from mongoapi import mongoapi,mongodb_url

url = mongodb_url("username","pass","dbname","host") #port=27017
# Initialize the MongoAPI
api = mongoapi(url,"mydb")

```

### Insert or Update a Document

```python
# Insert or update a document
import time
ex = time.time()+60 #expires in 60 seconds
api.put({"key": "item1", "value": "data", "__expires": ex})  # __expires is an optional expiry timestamp

#insert many at once
api.put([{"key": https://pypi.org/project/mongoapi/
### Retrieve a Document

```python
# Retrieve  by key
item = api.get("item1")
print(item)
```

### Update Specific Fields

```python
# Update specific fields by key
api.patch("item1", {"value": "updated_data"})
```

### Delete a Document

```python
# Delete a document by key
api.delete("item1")
```

### Retrieve All Documents

```python
# Retrieve all non-expired documents
all_items = api.get_all()
print(all_items)
```

### Delete All Documents

```python
# Delete all documents in the collection
api.delete_all()
```

---

## License

This package is licensed under the MIT License. See the LICENSE file for details.

---

## Author

Developed by Paviththanan (rkpavi06@gmail.com).  
GitHub Repository: [MongoAPI](https://github.com/rekcah-pavi/mongoapi)

