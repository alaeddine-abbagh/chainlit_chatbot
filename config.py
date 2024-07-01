import os

# Flask settings
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

# Babel settings
LANGUAGES = ['en', 'fr']
