import torch
from torch import nn


class MatrixFactorization(nn.Module):
    def __init__(self, num_users: int, num_movies: int, embedding_dim: int = 50):
        super().__init__()

        self.user_embeddings = nn.Embedding(num_users, embedding_dim)
        self.movie_embeddings = nn.Embedding(num_movies, embedding_dim)

        self.user_biases = nn.Embedding(num_users, 1)
        self.movie_biases = nn.Embedding(num_movies, 1)

        self.global_bias = nn.Parameter(torch.zeros(1))

    def forward(self, user_ids, movie_ids):
        user_vecs = self.user_embeddings(user_ids)
        movie_vecs = self.movie_embeddings(movie_ids)

        dot = (user_vecs * movie_vecs).sum(dim=1)

        user_bias = self.user_biases(user_ids).squeeze()
        movie_bias = self.movie_biases(movie_ids).squeeze()

        return self.global_bias + user_bias + movie_bias + dot