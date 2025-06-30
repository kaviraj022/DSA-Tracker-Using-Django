# DSA Tracker

A full-stack Django web application for tracking Data Structures and Algorithms (DSA) problems, user progress, and resources. Deployed on Railway with PostgreSQL and static file support via Whitenoise.

---

## Features

- User authentication (sign up, sign in, password reset)
- Admin dashboard for managing users and problems
- Track DSA problems by topic, difficulty, and practice links
- User progress tracking and personal notes
- Responsive UI with custom CSS
- Super admin(add problems/delete any one), Admin(add problems, delete only users)

---

## Tech Stack

- **Backend:** Django 5.x
- **Frontend:** Django Templates, HTML, CSS
- **Database:** PostgreSQL (cloud, via Railway)
- **Deployment:** Railway
- **Static Files:** Whitenoise

---

## Project Structure

```
dsa_tracker/
├── dsa_tracker/           # Django project settings
├── tracker/               # Main app (models, views, templates, static)
├── staticfiles/           # Collected static files (created by collectstatic)
├── requirements.txt       # Python dependencies
├── Procfile               # For Railway/Gunicorn deployment
├── .env                   # Environment variables (not committed)
├── manage.py
└── README.md
```

---

## Getting Started (Local Development)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd dsa_tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     SECRET_KEY=your-local-secret-key
     DATABASE_URL=your-local-or-cloud-postgres-url
     ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Deployment on Railway

1. **Push your code to GitHub.**
2. **Create a new Railway project and link your GitHub repo.**
3. **Set environment variables in Railway:**
   - `SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DATABASE_URL` (your Railway PostgreSQL URL)
4. **Ensure your `Procfile` contains:**
   ```
   web: gunicorn dsa_tracker.wsgi
   ```
5. **Static files:**  
   Railway will serve static files using Whitenoise.  
   Make sure `STATIC_ROOT` and `STATICFILES_STORAGE` are set in `settings.py`.
6. **After deployment, migrations and static collection are run automatically if using a Dockerfile or Nixpacks.**

---

## Environment Variables

- `SECRET_KEY` – Django secret key (keep this secret!)
- `DATABASE_URL` – PostgreSQL connection string

---

## Static Files

- Place your static files in `tracker/static/tracker/`
- Run `python manage.py collectstatic --noinput` to gather all static files into `staticfiles/` for production

---

## Security & Production Settings

- Set `DEBUG = False` in production
- Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in `settings.py` to include your Railway domain:
  ```python
  ALLOWED_HOSTS = ['.railway.app']
  CSRF_TRUSTED_ORIGINS = ['https://your-app-name.up.railway.app']
  ```

---

## License

This project is for educational purposes. Feel free to use and modify as needed.
