from flask import Flask, render_template, request, redirect
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Connect to MongoDB Atlas using connection string stored in .env
MONGO_URI = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
db = client["notes_db"]  # Database name
collection = db["notes"]  # Collection name

# Route: Home page - Shows form and list of notes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        content = request.form.get('content')

        # Insert into MongoDB if data is present
        if title and content:
            collection.insert_one({'title': title, 'content': content})
            return redirect('/')
    
    # Fetch all notes from MongoDB
    notes = collection.find()
    return render_template('index.html', notes=notes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
