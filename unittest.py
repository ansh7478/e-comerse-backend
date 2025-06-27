import unittest
from unittest.mock import Mock, patch

class CartService:
    def __init__(self):
        self.cart = []
    
    def add_to_cart(self, product_id, quantity=1):
        """Add product to cart or update quantity if exists"""
        if not product_id or quantity <= 0:
            raise ValueError("Invalid product ID or quantity")
        
        if quantity > 10:
            raise ValueError("Maximum 10 items per product")
        
        # Find existing item
        for item in self.cart:
            if item["product_id"] == product_id:
                new_qty = item["quantity"] + quantity
                if new_qty > 10:
                    raise ValueError("Cart limit exceeded")
                item["quantity"] = new_qty
                return {"message": "Quantity updated", "total_items": sum(i["quantity"] for i in self.cart)}
        
        # Add new item
        self.cart.append({"product_id": product_id, "quantity": quantity})
        return {"message": "Item added", "total_items": sum(i["quantity"] for i in self.cart)}

class TestCartService(unittest.TestCase):
    
    def setUp(self):
        self.cart_service = CartService()
    
    def test_add_new_item_success(self):
        """Test adding new item to empty cart"""
        result = self.cart_service.add_to_cart(1, 2)
        self.assertEqual(result["message"], "Item added")
        self.assertEqual(result["total_items"], 2)
        self.assertEqual(len(self.cart_service.cart), 1)
    
    def test_update_existing_item_quantity(self):
        """Test updating quantity of existing item"""
        self.cart_service.add_to_cart(1, 2)
        result = self.cart_service.add_to_cart(1, 3)
        self.assertEqual(result["message"], "Quantity updated")
        self.assertEqual(result["total_items"], 5)
    
    def test_invalid_product_id_none(self):
        """Test adding item with None product ID"""
        with self.assertRaises(ValueError) as context:
            self.cart_service.add_to_cart(None, 1)
        self.assertIn("Invalid product ID", str(context.exception))
    
    def test_invalid_product_id_empty(self):
        """Test adding item with empty product ID"""
        with self.assertRaises(ValueError):
            self.cart_service.add_to_cart("", 1)
    
    def test_invalid_quantity_zero(self):
        """Test adding item with zero quantity"""
        with self.assertRaises(ValueError) as context:
            self.cart_service.add_to_cart(1, 0)
        self.assertIn("Invalid product ID or quantity", str(context.exception))
    
    def test_invalid_quantity_negative(self):
        """Test adding item with negative quantity"""
        with self.assertRaises(ValueError):
            self.cart_service.add_to_cart(1, -5)
    
    def test_quantity_exceeds_limit_new_item(self):
        """Test adding new item with quantity > 10"""
        with self.assertRaises(ValueError) as context:
            self.cart_service.add_to_cart(1, 15)
        self.assertIn("Maximum 10 items", str(context.exception))
    
    def test_quantity_exceeds_limit_existing_item(self):
        """Test updating existing item beyond limit"""
        self.cart_service.add_to_cart(1, 8)
        with self.assertRaises(ValueError) as context:
            self.cart_service.add_to_cart(1, 5)
        self.assertIn("Cart limit exceeded", str(context.exception))
    
    def test_default_quantity_parameter(self):
        """Test default quantity when not specified"""
        result = self.cart_service.add_to_cart(1)
        self.assertEqual(result["total_items"], 1)
        self.assertEqual(self.cart_service.cart[0]["quantity"], 1)
    
    def test_multiple_different_products(self):
        """Test adding multiple different products"""
        self.cart_service.add_to_cart(1, 2)
        self.cart_service.add_to_cart(2, 3)
        result = self.cart_service.add_to_cart(3, 1)
        self.assertEqual(result["total_items"], 6)
        self.assertEqual(len(self.cart_service.cart), 3)

if __name__ == "__main__":
    unittest.main()