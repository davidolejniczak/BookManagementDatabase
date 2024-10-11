# Book Inventory Management System

This project is a simple web-based Book Inventory Management System built using **Flask** as the web framework and **SQLite** as the database. It allows users to manage a collection of books by adding, filtering, exporting, and deleting entries from the inventory.

## Features
- Add new books with required fields like title, author, genre, publication date, and ISBN.
- Filter the list of books by title, author, genre, and publication date.
- Export the list of books in either CSV or JSON format.
- Delete all books from the inventory with a single button.
- Simple, user-friendly, and responsive design using **Bootstrap** for styling.

---

## Setup and Installation

### Prerequisites
- **Python 3.x**: Ensure you have Python 3.x installed. Download from the [official Python website](https://www.python.org/downloads/).
- **Flask**: Flask will be used to run the web server.

### Step 1: Clone the Repository
Clone this repository to your local machine and cd to:
```bash
cd BookManagementDatabase
```

### Step 2: Ensure Flask is installed 
Please ensure Flask is installed to run it. If not instead here is the command:
```bash 
pip install flask
```
### Step 3: Running the website
Run the application by typing in:
```Python
python app.py
``` 
The website will be available at: 
```arduino
http://127.0.0.1:5000/
```

## Usage

### Adding a New Book
1. Navigate to the homepage.
2. Fill out the form with the following fields:
   - **Title** (Required)
   - **Author** (Required)
   - **Genre** (Required)
   - **Publication Date** (Required, cannot be in the future)
   - **ISBN** (Required, must be 10 or 13 digits)
3. Click the **Add Book** button to add the book to the inventory.

### Filtering Books
- Use the filter form to search for books by title, author, genre, or publication date.
- Click the **Filter** button to display the filtered results.
- Use the **Clear** button to reset the filters and display all books.

### Exporting Data
- Click **Export as CSV** to download the book list as a CSV file.
- Click **Export as JSON** to download the book list as a JSON file.

### Clearing the Inventory
- Click the **Clear All Books** button to delete all books from the inventory. 
- **Warning**: This action cannot be undone.

## Design decisions or challenges
During development, I chose Flask as the web framework for its simplicity, which is ideal for a project like this. SQLite was selected as the database because it’s serverless, and easy to integrate with Flask, making it the perfect choice for this project. One challenge I faced was ensuring efficient database connections and properly handling validation, especially for the ISBN field. It took me a while to find a way but I used regular expressions to ensure only valid formats were accepted. For the front-end, I decided to use Bootstrap as it provides a clean, responsive design with minimal custom CSS. This really helped me as I do not have deep knowledge in front-end devoplement.