# Skillvine_Python

Skillvine_Python is a Django-based version of **Skillvine**, an online learning platform concept that connects **students** and **teachers** in one system.  
This project is a rebuild of the original Skillvine idea using **Python**, **Django**, **HTML**, **CSS**, and **JavaScript**.

The goal of this version is to create a cleaner, easier-to-maintain, and more scalable web application while continuing the original vision of Skillvine.

---

## Overview

Skillvine is designed as a platform where users can:

- create accounts
- choose a role such as **Student** or **Teacher**
- explore a learning platform interface
- log in and access protected areas
- later use dashboards, features, and teacher-student interactions

At the current stage, the project already includes a working Django foundation, landing page UI, login and signup pages, custom user roles, and a JSON-based authentication flow.

---

## Current Features

### Completed
- Django project setup
- Organized app structure
- Landing page
- Base template system
- Responsive navigation
- About / Services / Contact popup tabs
- Hero section
- Image slider
- Features section
- Login page
- Signup page
- Custom user model
- Role selection during signup
- JSON-based signup flow
- JSON-based login flow
- Auto-login after signup
- Temporary dashboard redirect
- Static file integration for CSS, JS, and images
- Git repository setup
- GitHub repository push completed

### In Progress
- Dashboard improvements
- Role-based dashboard logic
- Better protected routes
- Backend feature expansion

### Planned
- Real dashboard UI
- Logout functionality
- Authentication protection on pages
- Student dashboard
- Teacher dashboard
- Profile page
- Notifications system
- Coins / credits system
- Teacher credibility / ratings
- Session booking features
- Admin controls
- Database improvements
- Better form validation
- Deployment

---

## Tech Stack

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite (development)

### Version Control
- Git
- GitHub

---

## Project Structure

```text
skillvine/
├── config/
├── core/
├── users/
├── dashboard/
├── notifications/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   └── users/
├── media/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main folders
- `config/` → Django project settings and root URL configuration
- `core/` → Main landing page and core views
- `users/` → Login, signup, and user-related logic
- `dashboard/` → Dashboard routes and views
- `notifications/` → Future notification system
- `static/` → CSS, JavaScript, and image assets
- `templates/` → HTML templates
- `media/` → Uploaded media files
- `manage.py` → Django management entry point

---

## Authentication System

This project currently uses:

- custom Django user model
- email-based login logic
- role-based signup
- frontend JavaScript `fetch()` requests
- JSON responses from Django views

### Current roles
- Student
- Teacher

The current auth flow includes:
- user registration
- login request handling
- auto-login after signup
- redirect to dashboard

---

## Frontend Pages

### Landing Page
The landing page currently includes:
- navbar
- popup tabs for About, Services, and Contact
- hero section
- image slider
- features section
- footer

### Login Page
The login page includes:
- email input
- password input
- password visibility toggle
- frontend error messages
- JSON login request handling

### Signup Page
The signup page includes:
- full name
- email
- password
- confirm password
- password strength indicator
- password match checker
- role selector
- password visibility toggles
- frontend validation
- auto-login flow after signup

---

## Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/JezCruz/Skillvine_Python.git
cd Skillvine_Python
```

### 2. Create a virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

### 6. Open in browser

```text
http://127.0.0.1:8000/
```

---

## Requirements

Make sure you have:
- Python installed
- pip installed
- Git installed

Recommended:
- VS Code
- Django latest stable version
- virtual environment for project isolation

---

## Development Notes

This project started as a Python/Django rebuild of the original Skillvine concept.

The purpose of rebuilding it in Django is to:
- make backend development easier to maintain
- improve project structure
- simplify authentication handling
- use Django's built-in strengths for web apps
- allow the project to grow into a more complete platform

---

## Current Progress Summary

At this point, the project already has:

- working Django structure
- working home page
- base layout setup
- working login page
- working signup page
- working custom user model
- working JSON auth requests
- working redirect flow after authentication
- GitHub repository already initialized and pushed

This means the project now has a solid starting foundation for future features.

---

## Next Development Goals

The next major steps planned are:

1. Build a real dashboard page  
2. Add proper dashboard template and styling  
3. Add route protection for authenticated users  
4. Add logout  
5. Separate student and teacher views  
6. Add profile system  
7. Add notification features  
8. Expand the platform logic for learning sessions and user interactions  

---

## .gitignore Notes

The project uses a `.gitignore` file to avoid pushing unnecessary and sensitive files such as:

- `__pycache__/`
- `db.sqlite3`
- `.env`
- virtual environments
- editor-specific folders
- logs
- temporary files

This helps keep the repository clean and secure.

---

## Example Commands Used During Setup

### Run the server
```bash
python manage.py runserver
```

### Create migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Create superuser
```bash
python manage.py createsuperuser
```

---

## Future Improvements

Some possible future improvements for Skillvine_Python include:

- better UI/UX polish
- improved dashboard cards and stats
- real database-backed user data display
- role-based permissions
- teacher verification system
- booking logic
- payment or coin system
- ratings and feedback system
- notifications and reminders
- deployment to a live server
- mobile responsiveness improvements
- cleaner reusable components

---

## Learning Purpose

This project is also part of a learning journey in:

- Python
- Django
- authentication systems
- project structure
- frontend and backend integration
- Git and GitHub workflow
- rebuilding and improving an existing concept using a new stack

---

## Author

**JezCruz**

GitHub: [JezCruz](https://github.com/JezCruz)

---

## Repository

GitHub Repository:  
[Skillvine_Python](https://github.com/JezCruz/Skillvine_Python)

---

## License

This project is currently for learning and development purposes.

You may add a license later depending on how you want to publish or share the project.

---

## Final Note

Skillvine_Python is still under active development, but the foundation is already working well.  
The project now has a clean Django setup, frontend pages, authentication flow, and room to grow into a more complete learning platform.
