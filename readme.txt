This project trains a movie recommendation model using PyTorch and the MovieLens dataset.

The first model is matrix factorization. It learns an embedding vector for each user and each movie, then predicts ratings from the interaction between those vectors.

The demo supports:
- training a recommender model
- evaluating rating prediction accuracy
- generating top-N recommendations
- adding new user ratings
- recommending movies for a new user profile