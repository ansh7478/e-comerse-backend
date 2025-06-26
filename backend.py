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
        