import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
import random

class ECommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyShop - Python E-Commerce")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f5f7ff")
        
        # Initialize database
        self.db_file = "products.json"
        self.products = self.load_products()
        
        self.cart = []
        self.current_page = "home"
        
        # Create UI
        self.create_header()
        self.create_home_page()
        
    def load_products(self):
        """Load products from JSON file or create sample data"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    return json.load(f)
            except:
                return self.create_sample_products()
        else:
            return self.create_sample_products()
    
    def save_products(self):
        """Save products to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.products, f, indent=2)

    def create_sample_products(self):
        """Create sample products if JSON file doesn't exist"""
        products = [
            {"id": 1, "name": "Wireless Headphones", "price": 89.99, "category": "Electronics", 
             "description": "Premium sound with noise cancellation", "icon": "🎧"},
            {"id": 2, "name": "Smartphone Pro", "price": 699.99, "category": "Electronics", 
             "description": "Triple camera, all-day battery", "icon": "📱"},
            {"id": 3, "name": "UltraSlim Laptop", "price": 899.99, "category": "Electronics", 
             "description": "Powerful performance in sleek design", "icon": "💻"},
            {"id": 4, "name": "Smart Watch", "price": 249.99, "category": "Electronics", 
             "description": "Fitness tracking and notifications", "icon": "⌚"},
            {"id": 5, "name": "Cotton T-Shirt", "price": 24.99, "category": "Clothing", 
             "description": "Soft and comfortable", "icon": "👕"},
            {"id": 6, "name": "Running Shoes", "price": 89.99, "category": "Footwear", 
             "description": "Lightweight with extra cushioning", "icon": "👟"},
            {"id": 7, "name": "Coffee Maker", "price": 129.99, "category": "Home", 
             "description": "Brew perfect coffee every morning", "icon": "☕"},
            {"id": 8, "name": "Bluetooth Speaker", "price": 79.99, "category": "Electronics", 
             "description": "360° immersive sound experience", "icon": "🔊"},
        ]
        self.save_products()
        return products
    
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg="#4361ee", height=70)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Logo
        logo_frame = tk.Frame(header_frame, bg="#4361ee")
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(logo_frame, text="🛒", font=("Arial", 24), 
                bg="#4361ee", fg="white").pack(side=tk.LEFT)
        tk.Label(logo_frame, text="PyShop", font=("Arial", 20, "bold"), 
                fg="white", bg="#4361ee").pack(side=tk.LEFT, padx=10)
        
        # Search bar
        search_frame = tk.Frame(header_frame, bg="#4361ee")
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40,
                               font=("Arial", 10), bd=2, relief=tk.GROOVE)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        search_btn = tk.Button(search_frame, text="Search", bg="#4cc9f0", fg="white",
                              font=("Arial", 10), bd=0, command=self.search_products)
        search_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg="#4361ee")
        nav_frame.pack(side=tk.RIGHT, padx=20)
        
        home_btn = tk.Button(nav_frame, text="Home", font=("Arial", 10), 
                            bg="#4cc9f0", fg="white", bd=0, padx=10,
                            command=lambda: self.show_page("home"))
        home_btn.pack(side=tk.LEFT, padx=5)
        
        products_btn = tk.Button(nav_frame, text="Products", font=("Arial", 10), 
                                bg="#4cc9f0", fg="white", bd=0, padx=10,
                                command=lambda: self.show_page("products"))
        products_btn.pack(side=tk.LEFT, padx=5)
        
        cart_btn = tk.Button(nav_frame, text="Cart", font=("Arial", 10), 
                            bg="#4cc9f0", fg="white", bd=0, padx=10,
                            command=lambda: self.show_page("cart"))
        cart_btn.pack(side=tk.LEFT, padx=5)
        
        # Cart counter
        self.cart_counter = tk.Label(nav_frame, text="0", font=("Arial", 10, "bold"), 
                                    bg="#e91e63", fg="white", width=2, height=1)
        self.cart_counter.pack(side=tk.LEFT, padx=5)
    
    def create_home_page(self):
        # Create container frame
        self.home_frame = tk.Frame(self.root, bg="#f5f7ff")
        
        # Hero section
        hero_frame = tk.Frame(self.home_frame, bg="#4361ee", height=200)
        hero_frame.pack(fill=tk.X, padx=20, pady=20)
        
        hero_label = tk.Label(hero_frame, text="Welcome to PyShop", 
                             font=("Arial", 24, "bold"), fg="white", bg="#4361ee")
        hero_label.pack(pady=20)
        
        hero_desc = tk.Label(hero_frame, text="Quality products at affordable prices\nFree shipping on orders over $50!", 
                           font=("Arial", 12), fg="white", bg="#4361ee")
        hero_desc.pack()
        
        shop_btn = tk.Button(hero_frame, text="Shop Now", bg="#4cc9f0", fg="white",
                            font=("Arial", 12), bd=0, padx=20, pady=10,
                            command=lambda: self.show_page("products"))
        shop_btn.pack(pady=20)
        
        # Featured products
        featured_frame = tk.Frame(self.home_frame, bg="#f5f7ff")
        featured_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        tk.Label(featured_frame, text="Featured Products", 
                font=("Arial", 18, "bold"), bg="#f5f7ff", fg="#3f37c9").pack(anchor=tk.W)
        
        # Products grid
        products_frame = tk.Frame(featured_frame, bg="#f5f7ff")
        products_frame.pack(fill=tk.BOTH, pady=10, expand=True)
        
        # Create product cards
        for i, product in enumerate(random.sample(self.products, 4)):
            card = tk.Frame(products_frame, bg="white", bd=1, relief=tk.RAISED)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
            # Product image
            img_label = tk.Label(card, text=product["icon"], font=("Arial", 48), 
                               bg="#e0e7ff", width=8, height=3)
            img_label.pack(pady=10)
            
            # Product info
            tk.Label(card, text=product["name"], font=("Arial", 12, "bold"), 
                   bg="white").pack()
            
            tk.Label(card, text=product["category"], font=("Arial", 10), 
                   fg="#6c757d", bg="white").pack()
            
            tk.Label(card, text=f"${product['price']}", font=("Arial", 14, "bold"), 
                   fg="#4361ee", bg="white").pack(pady=5)
            
            # Add to cart button
            add_btn = tk.Button(card, text="Add to Cart", bg="#4361ee", fg="white",
                              command=lambda p=product: self.add_to_cart(p))
            add_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Categories section
        categories_frame = tk.Frame(self.home_frame, bg="#f5f7ff")
        categories_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(categories_frame, text="Shop by Category", 
                font=("Arial", 18, "bold"), bg="#f5f7ff", fg="#3f37c9").pack(anchor=tk.W)
        
        cat_btn_frame = tk.Frame(categories_frame, bg="#f5f7ff")
        cat_btn_frame.pack(fill=tk.X, pady=10)
        
        categories = list(set(p["category"] for p in self.products))
        for category in categories:
            btn = tk.Button(cat_btn_frame, text=category, bg="#4cc9f0", fg="white",
                          font=("Arial", 10), padx=15, pady=5,
                          command=lambda c=category: self.show_category(c))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Footer
        footer_frame = tk.Frame(self.home_frame, bg="#212529", height=60)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        tk.Label(footer_frame, text="© 2023 PyShop. All rights reserved.", 
                fg="white", bg="#212529", font=("Arial", 10)).pack(pady=20)
        
        # Show home page
        self.home_frame.pack(fill=tk.BOTH, expand=True)
    
    def create_products_page(self):
        self.products_frame = tk.Frame(self.root, bg="#f5f7ff")
        
        # Page title and filter
        top_frame = tk.Frame(self.products_frame, bg="#f5f7ff")
        top_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(top_frame, text="All Products", 
                font=("Arial", 18, "bold"), bg="#f5f7ff", fg="#3f37c9").pack(side=tk.LEFT)
        
        # Sort options
        sort_frame = tk.Frame(top_frame, bg="#f5f7ff")
        sort_frame.pack(side=tk.RIGHT)
        
        tk.Label(sort_frame, text="Sort by:", bg="#f5f7ff").pack(side=tk.LEFT)
        
        sort_var = tk.StringVar(value="name")
        ttk.Combobox(sort_frame, textvariable=sort_var, width=15,
                    values=["Name", "Price: Low to High", "Price: High to Low"]).pack(side=tk.LEFT, padx=5)
        
        # Products grid
        products_frame = tk.Frame(self.products_frame, bg="#f5f7ff")
        products_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Create product cards
        for i, product in enumerate(self.products):
            card = tk.Frame(products_frame, bg="white", bd=1, relief=tk.RAISED)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            # Product image
            img_label = tk.Label(card, text=product["icon"], font=("Arial", 48), 
                               bg="#e0e7ff", width=8, height=3)
            img_label.pack(pady=10)
            
            # Product info
            tk.Label(card, text=product["name"], font=("Arial", 12, "bold"), 
                   bg="white").pack()
            
            tk.Label(card, text=product["category"], font=("Arial", 10), 
                   fg="#6c757d", bg="white").pack()
            
            tk.Label(card, text=f"${product['price']}", font=("Arial", 14, "bold"), 
                   fg="#4361ee", bg="white").pack(pady=5)
            
            # Add to cart button
            add_btn = tk.Button(card, text="Add to Cart", bg="#4361ee", fg="white",
                              command=lambda p=product: self.add_to_cart(p))
            add_btn.pack(pady=10, padx=20, fill=tk.X)
    
    def create_cart_page(self):
        self.cart_frame = tk.Frame(self.root, bg="#f5f7ff")
        
        # Page title
        title_frame = tk.Frame(self.cart_frame, bg="#f5f7ff")
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(title_frame, text="Your Shopping Cart", 
                font=("Arial", 18, "bold"), bg="#f5f7ff", fg="#3f37c9").pack(side=tk.LEFT)
        
        # Cart items frame
        cart_items_frame = tk.Frame(self.cart_frame, bg="#f5f7ff")
        cart_items_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        if not self.cart:
            # Empty cart message
            empty_frame = tk.Frame(cart_items_frame, bg="#f5f7ff")
            empty_frame.pack(expand=True, pady=50)
            
            tk.Label(empty_frame, text="🛒", font=("Arial", 48), 
                    bg="#f5f7ff", fg="#6c757d").pack()
            
            tk.Label(empty_frame, text="Your cart is empty", 
                    font=("Arial", 16), bg="#f5f7ff", fg="#6c757d").pack(pady=10)
            
            shop_btn = tk.Button(empty_frame, text="Browse Products", 
                                bg="#4361ee", fg="white", font=("Arial", 12),
                                command=lambda: self.show_page("products"))
            shop_btn.pack(pady=20)
        else:
            # Create cart table
            columns = ("item", "price", "quantity", "total")
            self.cart_tree = ttk.Treeview(cart_items_frame, columns=columns, show="headings", height=8)
            
            # Configure columns
            self.cart_tree.heading("item", text="Product")
            self.cart_tree.heading("price", text="Price")
            self.cart_tree.heading("quantity", text="Quantity")
            self.cart_tree.heading("total", text="Total")
            
            self.cart_tree.column("item", width=300)
            self.cart_tree.column("price", width=150, anchor=tk.CENTER)
            self.cart_tree.column("quantity", width=150, anchor=tk.CENTER)
            self.cart_tree.column("total", width=150, anchor=tk.CENTER)
            
            # Add data to cart
            for item in self.cart:
                total = item["price"] * item["quantity"]
                self.cart_tree.insert("", tk.END, values=(
                    f"{item['icon']} {item['name']}",
                    f"${item['price']}",
                    item["quantity"],
                    f"${total:.2f}"
                ))
            
            self.cart_tree.pack(fill=tk.BOTH, expand=True)
            
            # Cart total
            cart_total = sum(item["price"] * item["quantity"] for item in self.cart)
            total_frame = tk.Frame(cart_items_frame, bg="#f5f7ff")
            total_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(total_frame, text="Subtotal:", font=("Arial", 14), 
                    bg="#f5f7ff").pack(side=tk.LEFT)
            
            tk.Label(total_frame, text=f"${cart_total:.2f}", font=("Arial", 16, "bold"), 
                    fg="#4361ee", bg="#f5f7ff").pack(side=tk.LEFT, padx=10)
            
            shipping = 0 if cart_total > 50 else 9.99
            tk.Label(total_frame, text="Shipping:", font=("Arial", 14), 
                    bg="#f5f7ff").pack(side=tk.LEFT, padx=(30, 0))
            
            tk.Label(total_frame, text=f"${shipping:.2f}", font=("Arial", 14), 
                    bg="#f5f7ff").pack(side=tk.LEFT, padx=10)
            
            tk.Label(total_frame, text="Total:", font=("Arial", 16, "bold"), 
                    bg="#f5f7ff").pack(side=tk.LEFT, padx=(30, 0))
            
            total_amount = cart_total + shipping
            tk.Label(total_frame, text=f"${total_amount:.2f}", font=("Arial", 16, "bold"), 
                    fg="#4361ee", bg="#f5f7ff").pack(side=tk.LEFT, padx=10)
            
            # Buttons
            btn_frame = tk.Frame(cart_items_frame, bg="#f5f7ff")
            btn_frame.pack(fill=tk.X, pady=20)
            
            tk.Button(btn_frame, text="Continue Shopping", bg="#6c757d", fg="white",
                     command=lambda: self.show_page("products")).pack(side=tk.LEFT, padx=5)
            
            tk.Button(btn_frame, text="Checkout", bg="#4caf50", fg="white",
                     command=self.show_checkout).pack(side=tk.RIGHT, padx=5)
    
    def create_checkout_page(self):
        self.checkout_frame = tk.Frame(self.root, bg="#f5f7ff")
        
        # Page title
        tk.Label(self.checkout_frame, text="Checkout", 
                font=("Arial", 18, "bold"), bg="#f5f7ff", fg="#3f37c9").pack(pady=20)
        
        # Checkout form
        form_frame = tk.Frame(self.checkout_frame, bg="#f5f7ff")
        form_frame.pack(fill=tk.BOTH, padx=50, pady=10, expand=True)
        
        # Left column - Form
        left_frame = tk.Frame(form_frame, bg="#f5f7ff")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Label(left_frame, text="Shipping Information", 
                font=("Arial", 14, "bold"), bg="#f5f7ff").pack(anchor=tk.W, pady=10)
        
        # Form fields
        fields = [
            ("Full Name", "entry"),
            ("Email", "entry"),
            ("Address", "entry"),
            ("City", "entry"),
            ("State", "entry"),
            ("ZIP Code", "entry"),
            ("Phone", "entry")
        ]
        
        self.form_entries = {}
        for label, field_type in fields:
            frame = tk.Frame(left_frame, bg="#f5f7ff")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, width=12, anchor=tk.W, 
                    bg="#f5f7ff").pack(side=tk.LEFT)
            
            if field_type == "entry":
                entry = tk.Entry(frame, width=30)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_entries[label] = entry
        
        # Payment method
        tk.Label(left_frame, text="Payment Method", 
                font=("Arial", 14, "bold"), bg="#f5f7ff").pack(anchor=tk.W, pady=10)
        
        payment_frame = tk.Frame(left_frame, bg="#f5f7ff")
        payment_frame.pack(fill=tk.X)
        
        payment_var = tk.StringVar(value="credit_card")
        
        tk.Radiobutton(payment_frame, text="Credit Card", variable=payment_var, 
                      value="credit_card", bg="#f5f7ff").pack(anchor=tk.W)
        
        tk.Radiobutton(payment_frame, text="PayPal", variable=payment_var, 
                      value="paypal", bg="#f5f7ff").pack(anchor=tk.W)
        
        tk.Radiobutton(payment_frame, text="Cash on Delivery", variable=payment_var, 
                      value="cod", bg="#f5f7ff").pack(anchor=tk.W)
        
        # Right column - Order summary
        right_frame = tk.Frame(form_frame, bg="white", bd=1, relief=tk.GROOVE)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        tk.Label(right_frame, text="Order Summary", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        
        # Order items
        items_frame = tk.Frame(right_frame, bg="white")
        items_frame.pack(fill=tk.X, padx=10, pady=5)
        
        cart_total = sum(item["price"] * item["quantity"] for item in self.cart)
        shipping = 0 if cart_total > 50 else 9.99
        total = cart_total + shipping
        
        # Display items
        for item in self.cart:
            item_frame = tk.Frame(items_frame, bg="white")
            item_frame.pack(fill=tk.X, pady=3)
            
            tk.Label(item_frame, text=f"{item['icon']} {item['name']} x{item['quantity']}", 
                    bg="white", anchor=tk.W).pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=f"${item['price'] * item['quantity']:.2f}", 
                    bg="white", anchor=tk.E).pack(side=tk.RIGHT)
        
        # Summary totals
        summary_frame = tk.Frame(right_frame, bg="white")
        summary_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Frame(summary_frame, height=1, bg="#e0e0e0").pack(fill=tk.X, pady=5)
        
        tk.Label(summary_frame, text="Subtotal:", bg="white").pack(anchor=tk.E)
        tk.Label(summary_frame, text=f"${cart_total:.2f}", bg="white").pack(anchor=tk.E)
        
        tk.Label(summary_frame, text="Shipping:", bg="white").pack(anchor=tk.E)
        tk.Label(summary_frame, text=f"${shipping:.2f}", bg="white").pack(anchor=tk.E)
        
        tk.Frame(summary_frame, height=1, bg="#e0e0e0").pack(fill=tk.X, pady=5)
        
        tk.Label(summary_frame, text="Total:", font=("Arial", 12, "bold"), bg="white").pack(anchor=tk.E)
        tk.Label(summary_frame, text=f"${total:.2f}", font=("Arial", 12, "bold"), 
                fg="#4361ee", bg="white").pack(anchor=tk.E)
        
        # Place order button
        place_order_btn = tk.Button(right_frame, text="Place Order", bg="#4caf50", fg="white",
                                  font=("Arial", 12), width=20,
                                  command=self.complete_order)
        place_order_btn.pack(pady=20)
    
    def create_confirmation_page(self):
        self.confirmation_frame = tk.Frame(self.root, bg="#f5f7ff")
        
        # Confirmation message
        tk.Label(self.confirmation_frame, text="✓", font=("Arial", 72), 
                fg="#4caf50", bg="#f5f7ff").pack(pady=30)
        
        tk.Label(self.confirmation_frame, text="Order Confirmed!", 
                font=("Arial", 24, "bold"), bg="#f5f7ff").pack(pady=10)
        
        tk.Label(self.confirmation_frame, text="Thank you for your order!", 
                font=("Arial", 14), bg="#f5f7ff").pack(pady=10)
        
        tk.Label(self.confirmation_frame, text="Your order has been placed successfully.", 
                font=("Arial", 12), bg="#f5f7ff").pack(pady=5)
        
        order_frame = tk.Frame(self.confirmation_frame, bg="#e8f5e9", bd=1, relief=tk.GROOVE)
        order_frame.pack(pady=20, padx=50, fill=tk.X)
        
        # Order details
        order_num = random.randint(100000, 999999)
        tk.Label(order_frame, text=f"Order #: {order_num}", 
                font=("Arial", 12), bg="#e8f5e9").pack(pady=5)
        
        cart_total = sum(item["price"] * item["quantity"] for item in self.cart)
        shipping = 0 if cart_total > 50 else 9.99
        total = cart_total + shipping
        
        tk.Label(order_frame, text=f"Total: ${total:.2f}", 
                font=("Arial", 12), bg="#e8f5e9").pack(pady=5)
        
        # Continue shopping button
        tk.Button(self.confirmation_frame, text="Continue Shopping", 
                 bg="#4361ee", fg="white", font=("Arial", 12),
                 command=lambda: self.show_page("home")).pack(pady=30)
    
    def add_to_cart(self, product):
        # Check if product already in cart
        for item in self.cart:
            if item["id"] == product["id"]:
                item["quantity"] += 1
                break
        else:
            self.cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "icon": product["icon"]
            })
        
        # Update cart counter
        total_items = sum(item["quantity"] for item in self.cart)
        self.cart_counter.config(text=str(total_items))
        
        messagebox.showinfo("Added to Cart", f"{product['name']} added to your cart!")
    
    def show_page(self, page_name):
        # Hide current page
        if self.current_page == "home":
            self.home_frame.pack_forget()
        elif self.current_page == "products":
            self.products_frame.pack_forget()
        elif self.current_page == "cart":
            self.cart_frame.pack_forget()
        elif self.current_page == "checkout":
            self.checkout_frame.pack_forget()
        elif self.current_page == "confirmation":
            self.confirmation_frame.pack_forget()
        
        # Show new page
        if page_name == "home":
            if not hasattr(self, "home_frame"):
                self.create_home_page()
            self.home_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "products":
            if not hasattr(self, "products_frame"):
                self.create_products_page()
            self.products_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "cart":
            if hasattr(self, "cart_frame"):
                self.cart_frame.destroy()
            self.create_cart_page()
            self.cart_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "checkout":
            if not hasattr(self, "checkout_frame"):
                self.create_checkout_page()
            self.checkout_frame.pack(fill=tk.BOTH, expand=True)
        elif page_name == "confirmation":
            if not hasattr(self, "confirmation_frame"):
                self.create_confirmation_page()
            self.confirmation_frame.pack(fill=tk.BOTH, expand=True)
        
        self.current_page = page_name
    
    def show_checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Your cart is empty. Add products before checkout.")
        else:
            self.show_page("checkout")
    
    def show_category(self, category):
        self.show_page("products")
        # In a full implementation, this would filter products by category
    
    def search_products(self):
        query = self.search_var.get().lower()
        if query:
            # In a full implementation, this would filter products by search query
            self.show_page("products")
            messagebox.showinfo("Search", f"Searching for: {query}")
    
    def complete_order(self):
        # Validate form
        for field, entry in self.form_entries.items():
            if not entry.get().strip():
                messagebox.showerror("Missing Information", f"Please fill in the {field} field")
                return
        
        # Process order
        self.show_page("confirmation")
        self.cart = []
        self.cart_counter.config(text="0")

if __name__ == "__main__":
    root = tk.Tk()
    app = ECommerceApp(root)
    root.mainloop()