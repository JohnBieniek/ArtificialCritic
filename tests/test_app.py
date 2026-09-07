import unittest

from fastapi.testclient import TestClient

from app.main import app, service


class AppIntegrationTests(unittest.TestCase):
    def setUp(self):
        service.ratings.clear()
        self.client = TestClient(app, base_url="http://localhost")
        self.addCleanup(self.client.close)
        self.addCleanup(service.ratings.clear)

    def test_django_catalogue(self):
        response = self.client.get("/django/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        for movie in service.list_movies():
            self.assertIn(movie.title, response.text)
        self.assertEqual(self.client.get("/django").status_code, 200)

    def test_django_rejects_unconfigured_host(self):
        response = self.client.get("/django/", headers={"host": "invalid.example"})
        self.assertEqual(response.status_code, 400)

    def test_api_routes_and_recommendations(self):
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})
        self.assertEqual(self.client.get("/docs").status_code, 200)
        self.assertEqual(len(self.client.get("/movies").json()), 10)
        rating = {"user_id": "test-user", "movie_id": 1, "rating": 5.0}
        response = self.client.post("/ratings", json=rating)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), rating)
        self.assertEqual(
            self.client.get("/users/test-user/ratings").json(), [rating]
        )
        recommendations = self.client.get(
            "/users/test-user/recommendations?limit=3"
        ).json()
        self.assertEqual(len(recommendations), 3)
        self.assertNotIn(1, [movie["movie_id"] for movie in recommendations])

    def test_api_validation(self):
        response = self.client.post(
            "/ratings", json={"user_id": "test-user", "movie_id": 1, "rating": 6}
        )
        self.assertEqual(response.status_code, 422)
