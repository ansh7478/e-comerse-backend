import unittest
from app import app


class ProductAPITest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_products(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)

    def test_product_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_add_product_without_data(self):
        response = self.client.post("/products", json={})
        self.assertEqual(response.status_code, 400)

    def test_add_product_missing_name(self):
        response = self.client.post("/products", json={
            "category": "Electronics",
            "price": 100,
            "stock": 5
        })
        self.assertEqual(response.status_code, 400)

    def test_add_product_negative_price(self):
        response = self.client.post("/products", json={
            "name": "Phone",
            "category": "Electronics",
            "price": -10,
            "stock": 5
        })
        self.assertEqual(response.status_code, 400)

    def test_add_product_negative_stock(self):
        response = self.client.post("/products", json={
            "name": "Phone",
            "category": "Electronics",
            "price": 100,
            "stock": -5
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_unknown_product(self):
        response = self.client.delete("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_update_unknown_product(self):
        response = self.client.put("/products/999", json={
            "name": "Phone",
            "category": "Electronics",
            "price": 100,
            "stock": 5
        })
        self.assertEqual(response.status_code, 404)

    def test_get_cart(self):
        response = self.client.get("/cart")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()