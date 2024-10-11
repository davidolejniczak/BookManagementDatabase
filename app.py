from flask import Flask, render_template, request, redirect, make_response
import sqlite3
import csv
import json
import re
from datetime import datetime

app = Flask(__name__)

#SQLite connection
def getDbConnection():
    conn = sqlite3.connect('books_inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

#Makes Database
def initializeDatabase():
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            publication_date TEXT,
            isbn TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

initializeDatabase()

#ISBN check
def isValidIsbn(isbn):
    return re.match(r'^\d{10}(\d{3})?$', isbn)

#Home of webpage
@app.route('/')
def index():
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Inventory')
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

#Add book
@app.route('/add', methods=['POST'])
def addBook():
    title = request.form['title']
    author = request.form['author']
    genre = request.form['genre']
    publicationDate = request.form['publication_date']
    isbn = request.form['isbn']

    #Input validation
    if not title or not author or not genre or not publicationDate or not isbn:
        return "Error: All fields are required."

    if not isValidIsbn(isbn):
        return "Error: Invalid ISBN. It must be 10 or 13 digits."
    try:
        pubDate = datetime.strptime(publicationDate, '%Y-%m-%d')
        if pubDate > datetime.now():
            return "Error: The publication date cannot be in the future."
    except ValueError:
        return "Error: Invalid date format."
    
    #New book
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Inventory (title, author, genre, publication_date, isbn) VALUES (?, ?, ?, ?, ?)',
                   (title, author, genre, publicationDate, isbn))
    conn.commit()
    conn.close()
    return redirect('/')

#Filter
@app.route('/filter', methods=['GET'])
def filterBooks():
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    genre = request.args.get('genre', '')
    publicationDate = request.args.get('publication_date', '')

    query = "SELECT * FROM Inventory WHERE 1=1"
    params = []

    #Filter logic
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if author:
        query += " AND author LIKE ?"
        params.append(f"%{author}%")
    if genre:
        query += " AND genre LIKE ?"
        params.append(f"%{genre}%")
    if publicationDate:
        query += " AND publication_date = ?"
        params.append(publicationDate)

    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

#Delete
@app.route('/clearBooks', methods=['POST'])
def clearBooks():
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Inventory')
    conn.commit()
    conn.close()
    return redirect('/')

#Export CSV
@app.route('/export/csv')
def exportToCsv():
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Inventory')
    books = cursor.fetchall()
    conn.close()
    csvOutput = []
    csvOutput.append(['ID', 'Title', 'Author', 'Genre', 'Publication Date', 'ISBN'])
    for book in books:
        csvOutput.append([book['id'], book['title'], book['author'], book['genre'], book['publication_date'], book['isbn']])
    csvString = "\n".join([",".join(map(str, row)) for row in csvOutput])
    response = make_response(csvString)
    response.headers['Content-Disposition'] = 'attachment; filename=books_inventory.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response

#Export JSON
@app.route('/export/json')
def exportToJson():
    conn = getDbConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Inventory')
    books = cursor.fetchall()
    conn.close()
    booksList = []
    for book in books:
        bookDict = {
            'id': book['id'],
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'publication_date': book['publication_date'],
            'isbn': book['isbn']
        }
        booksList.append(bookDict)
    response = make_response(json.dumps(booksList, indent=4))
    response.headers['Content-Disposition'] = 'attachment; filename=books_inventory.json'
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
