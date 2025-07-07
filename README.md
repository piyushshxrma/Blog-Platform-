# Django Blog Platform with Commenting System

This is a Django-based blog platform I built to meet the following objectives:

- Allow users to create and manage blog posts
- Let visitors read articles and comment on them
- Include proper search, filtering, pagination, and user authentication
- Add clear comments in the code and provide basic API documentation

This project was developed as part of a task that required building a functional blog with all essential features, focusing on **learning Django deeply and structuring code properly**.

---

## Key Features

### 1. Database Design
- The database is designed from scratch with models for `User`, `Post`, `Comment`, and `Tag`.
- Relationships:
  - Each `Post` is linked to an `Author` (User).
  - Each `Comment` is linked to a `Post` and to the commenting `User`.
  - Posts can have multiple `Tags`.

### 2. CRUD Operations
- Full **Create, Read, Update, Delete** functionality for blog posts.
- Users (Authors) can manage their own posts.
- Readers can delete or edit their own comments.

### 3. Code Comments
- Each function and view in the project is properly commented, explaining what it does and why it’s needed.  
  (Makes it easier for anyone reading or maintaining the code.)

### 4. Data Filtering & Searching
- Users can:
  - Search posts by title, category (if extended), or author.
  - Filter posts by tags or by publication date.

### 5. Pagination
- Blog posts are paginated on the main listing page.
- Comment threads under each post are also paginated, so long discussions stay manageable.

### 6. Authentication & Roles
- Uses Django’s built-in authentication system for:
  - Registering, logging in, and logging out.
- Role-based logic:
  - Authors can create/edit/delete their own posts.
  - Readers can manage their profiles and comments.

### 7. API Docs
- The project includes simple API endpoints for managing posts and comments.
- API endpoints are documented in the project so it’s clear how to use them for integration or testing.

---

## How to run this project locally

### 1. Clone the repo and navigate into it
```bash
git clone <your-github-repo-url>
cd your-project-folder

### 2. Set up a virtual environment
python3 -m venv env
venv\Scripts\activate (Windows)
source env/bin/activate (MacOS)

### 3. Install dependencies
pip install django

### 4. Apply migrations
python manage.py migrate

### 5. Create a superuser(optional, for admin panel)
python manage.py createsuperuser

### 6. Run the development server
python manage.py runserver


