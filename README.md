# weeb_backend

Django project to manage the website API **Weeb**.

## 🚀 Prerequisites

- Python 3.8+ recommandé
- Git
- Virtualenv (ou `python -m venv`)

## 🛠️ Installation

1. **Clone the repository**

```bash
git clone git@github.com:ThibaultBardinetLanglois/weeb_backend.git
cd weeb_backend
```

2. **Create a virtual environment**
   python -m venv venv
   source venv/bin/activate # Sur Windows : venv\Scripts\activate

3. **Install dependencies**
   pip install -r requirements.txt

4. (optional) **Generate new migration files if the models have evolved**
   python manage.py migrate

5. (optional) **Applies changes to the database if new migration files have been generated**
   python manage.py migrate

6. **If you want to train the machine learning model dedicated to sentiment analysis**
   python .\train_model.py

7. **Start the server**
   python manage.py runserver
