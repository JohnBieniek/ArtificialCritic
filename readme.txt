This project trains a movie recommendation model using PyTorch and the MovieLens dataset.

The first model is matrix factorization. It learns an embedding vector for each user and each movie, then predicts ratings from the interaction between those vectors.

The demo supports:
- training a recommender model
- evaluating rating prediction accuracy
- generating top-N recommendations
- adding new user ratings
- recommending movies for a new user profile

Running the app (Python 3.10+; deployments use Python 3.11)
--------------------------------------------------------
Install dependencies: python -m pip install -r requirements.txt
Start both frameworks: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

The existing FastAPI endpoints and interactive docs at /docs remain available.
The Django movie catalogue is at /django/. App Runner uses the same entry point.
The catalogue reads the demo movie list; API ratings still live in memory.

Django settings are in django_site/settings.py. Set DJANGO_ALLOWED_HOSTS to a
comma-separated list of hostnames for deployment (for example, your App Runner
hostname). The default permits localhost only. DJANGO_DEBUG defaults to false.
Set DJANGO_SECRET_KEY to a stable random secret in the deployment environment
before adding features that use signed data, such as sessions.

Django management: python manage.py check
Django-only development server: python manage.py runserver (catalogue at /)
The Django site currently has no database, authentication, or admin dependency.

Verification
------------
python -m pip install -r requirements-dev.txt
python manage.py check
python -m unittest discover -s tests
