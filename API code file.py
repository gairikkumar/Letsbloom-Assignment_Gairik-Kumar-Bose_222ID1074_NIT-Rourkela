from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['library']

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def retrieve_all_books():
    try:
        books = list(db.books.find())
        return jsonify(books)
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        new_book = request.get_json()
        result = db.books.insert_one(new_book)
        return jsonify(db.books.find_one({'_id': result.inserted_id}))
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint 3: Update Book Details
@app.route('/api/books/<book_id>', methods=['PUT'])
def update_book_details(book_id):
    try:
        updated_details = request.get_json()
        result = db.books.update_one({'_id': book_id}, {'$set': updated_details})
        if result.matched_count == 0:
            return jsonify({'error': 'Book not found'}), 404
        else:
            return jsonify({'message': 'Book updated successfully'})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
