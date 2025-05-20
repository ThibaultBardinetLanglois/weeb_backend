# weeb_backend

Projet Django pour gérer l'API du site web **Weeb**.

## 🚀 Prérequis

- Python 3.8+ recommandé
- Git
- Virtualenv (ou `python -m venv`)

## 🛠️ Installation

1. **Cloner le dépôt**

```bash
git clone git@github.com:ThibaultBardinetLanglois/weeb_backend.git
cd weeb_backend
```

2. **Créer un environnement virtuel**
   python -m venv venv
   source venv/bin/activate # Sur Windows : venv\Scripts\activate

3. **Installer les dépendances**
   pip install -r requirements.txt

4. (optionnel) **Installer les dépendances**
   python manage.py migrate

5. **Lancer le serveur**
   python manage.py runserver
