"""
Inventory Management System (Desktop App)

This project began as a real solution for my family's retail shop.
Managing inventory manually was confusing and slow, so I built this tool to
organize stock, search items quickly, and reduce human errors.

Working on this project made me realize how technology can simplify everyday
business tasks and inspired me to build accessible tools for small shops
like ours in the future.

Future Goals:
- Android version
- Customer order & feedback system
- Digital credit book / billing system
- Customer notifications and pre-paid order support
"""


import customtkinter as ctk
import json
import os

PRODUCTS_FILE = "products.json"
products = []

# Demo login for testing purpose (admin + user roles)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "rahul": {"password": "user123", "role": "user"}
}

# ----------------------------
# Product Data Functions
# ----------------------------

def load_products():
    """Load products from file."""
    global products
    try:
        if os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "r") as f:
                products = json.load(f)
        else:
            products = []
    except json.JSONDecodeError:
        products = []

def save_products():
    """Save product data to file."""
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)


def add_product(name, category, stock, price):
    """Add product to list and update file."""
    try:
        stock = int(stock)
        price = float(price)
    except ValueError:
        return  # Invalid input, skip adding

    product = {"name": name, "category": category, "stock": stock, "price": price}
    products.append(product)
    save_products()

def remove_product(name):
    """Remove product by name."""
    global products
    products = [p for p in products if p['name'].lower() != name.lower()]
    save_products()

# ----------------------------
# Login Page
# ----------------------------

class LoginPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        title = ctk.CTkLabel(self, text="Inventory Login", font=("Arial Rounded MT Bold", 28))
        title.pack(pady=40)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=300, height=40)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300, height=40)
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login, width=200, height=40)

        self.username_entry.pack(pady=10)
        self.password_entry.pack(pady=10)
        self.login_button.pack(pady=25)

        self.message_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.message_label.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = USERS.get(username)
        if user and user["password"] == password:
            if user["role"] == "admin":
                self.master.switch_frame(AdminPage)
            else:
                self.master.switch_frame(UserPage)
        else:
            self.message_label.configure(text="Invalid credentials", text_color="red")

# ----------------------------
# User Page
# ----------------------------

class UserPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        load_products()

        ctk.CTkLabel(self, text="User Dashboard", font=("Arial Rounded MT Bold", 26)).pack(pady=20)

        # Search bar for customers to find products quickly
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search product...", width=280)
        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_products, width=100)
        self.search_entry.pack(side="left", padx=5)
        self.search_button.pack(side="left", padx=5)

        # Display available products
        self.products_box = ctk.CTkTextbox(self, width=450, height=300)
        self.products_box.pack(pady=20)
        self.refresh_products()

        ctk.CTkButton(self, text="Logout", command=lambda: master.switch_frame(LoginPage), width=150).pack(pady=20)

    def refresh_products(self):
        self.products_box.delete("1.0", "end")
        for p in products:
            self.products_box.insert("end", f"{p['name']} | ₹{p['price']} | Stock: {p['stock']} | {p['category']}\n")

    def search_products(self):
        query = self.search_entry.get().lower()
        self.products_box.delete("1.0", "end")
        for p in products:
            if query in p["name"].lower() or query in p["category"].lower():
                self.products_box.insert("end", f"{p['name']} | ₹{p['price']} | Stock: {p['stock']} | {p['category']}\n")

# ----------------------------
# Admin Page (Shopkeeper)
# ----------------------------

class AdminPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        load_products()

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial Rounded MT Bold", 26)).pack(pady=10)
        content = ctk.CTkScrollableFrame(self)
        content.pack(fill="both", expand=True, padx=10, pady=10)

        # Add product section
        box = ctk.CTkFrame(content)
        box.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(box, text="Add Product", font=("Arial Rounded MT Bold", 18)).pack(pady=5)

        form = ctk.CTkFrame(box)
        form.pack(pady=5)

        self.name_entry = ctk.CTkEntry(form, placeholder_text="Product Name", width=200)
        self.category_entry = ctk.CTkEntry(form, placeholder_text="Category", width=200)
        self.stock_entry = ctk.CTkEntry(form, placeholder_text="Stock", width=200)
        self.price_entry = ctk.CTkEntry(form, placeholder_text="Price", width=200)

        self.name_entry.grid(row=0, column=0, padx=10, pady=5)
        self.category_entry.grid(row=0, column=1, padx=10, pady=5)
        self.stock_entry.grid(row=1, column=0, padx=10, pady=5)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkButton(form, text="Add", command=self.add_product).grid(row=2, column=0, columnspan=2, pady=10)

        # Product list display
        self.products_box = ctk.CTkTextbox(content, width=450, height=250)
        self.products_box.pack(pady=10)
        self.refresh_products()

        # Remove product section
        remove_frame = ctk.CTkFrame(content)
        remove_frame.pack(pady=10, padx=10, fill="x")

        self.remove_entry = ctk.CTkEntry(remove_frame, placeholder_text="Product name to remove", width=250)
        ctk.CTkButton(remove_frame, text="Remove", command=self.remove_product, width=100).pack(side="right", padx=5)
        self.remove_entry.pack(side="left", padx=5)

        ctk.CTkButton(content, text="Logout", command=lambda: master.switch_frame(LoginPage)).pack(side="right", pady=15)

    def refresh_products(self):
        self.products_box.delete("1.0", "end")
        for p in products:
            self.products_box.insert("end", f"{p['name']} | ₹{p['price']} | Stock: {p['stock']} | {p['category']}\n")

    def add_product(self):
        add_product(self.name_entry.get(), self.category_entry.get(), self.stock_entry.get(), self.price_entry.get())
        self.refresh_products()
        self.name_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.stock_entry.delete(0, "end")
        self.price_entry.delete(0, "end")

    def remove_product(self):
        remove_product(self.remove_entry.get())
        self.refresh_products()
        self.remove_entry.delete(0, "end")

# ----------------------------
# App Launcher
# ----------------------------

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("1000x700")
        self.current_frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, new_frame):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame(self)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    load_products()
    app = InventoryApp()
    app.mainloop()