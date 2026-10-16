import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
from tkinter import filedialog

# =========================================================
# DATABASE
# =========================================================

db = sqlite3.connect("ecommerce.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    name TEXT,
    phone TEXT,
    city TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    selling REAL,
    cost REAL,
    stock INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    total REAL,
    profit REAL,
    status TEXT DEFAULT 'Ordered'
)
""")

db.commit()

# =========================================================
# COLORS
# =========================================================

BG = "#eef2ff"
DARK = "#172554"
BLUE = "#4f46e5"
PURPLE = "#7c3aed"
GREEN = "#16a34a"
RED = "#dc2626"
ORANGE = "#f59e0b"
WHITE = "#ffffff"
GRAY = "#64748b"

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("E-Commerce Management System")
root.geometry("1050x680")
root.configure(bg=BG)
root.resizable(False, False)

def clear():
    for widget in root.winfo_children():
        widget.destroy()

def title(text, color=DARK):

    tk.Label(
        root,
        text=text,
        font=("Arial", 23, "bold"),
        bg=color,
        fg=WHITE
    ).pack(fill="x", pady=22)

# =========================================================
# HOME / LOGIN
# =========================================================

def home():

    clear()

    title("🛒 E-COMMERCE MANAGEMENT SYSTEM")

    tk.Label(
        root,
        text="Choose how you want to continue",
        font=("Arial", 14),
        bg=BG,
        fg=GRAY
    ).pack(pady=25)

    box = tk.Frame(root, bg=BG)
    box.pack()

    # ADMIN
    admin = tk.Frame(
        box, bg=WHITE, padx=35, pady=30
    )
    admin.grid(row=0, column=0, padx=15)

    tk.Label(
        admin,
        text="🔐 ADMIN",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=PURPLE
    ).pack()

    tk.Label(
        admin,
        text="Manage products, customers\nand orders",
        bg=WHITE,
        fg=GRAY
    ).pack(pady=12)

    tk.Button(
        admin,
        text="ADMIN LOGIN",
        command=admin_login,
        bg=PURPLE,
        fg=WHITE,
        width=22,
        font=("Arial", 10, "bold")
    ).pack(pady=5, ipady=7)

    tk.Button(
        admin,
        text="REGISTER ADMIN",
        command=admin_register,
        width=22
    ).pack(pady=5, ipady=5)

    # USER
    user = tk.Frame(
        box, bg=WHITE, padx=35, pady=30
    )
    user.grid(row=0, column=1, padx=15)

    tk.Label(
        user,
        text="👤 CUSTOMER",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack()

    tk.Label(
        user,
        text="Browse products and\nplace orders",
        bg=WHITE,
        fg=GRAY
    ).pack(pady=12)

    tk.Button(
        user,
        text="CUSTOMER LOGIN",
        command=user_login,
        bg=BLUE,
        fg=WHITE,
        width=22,
        font=("Arial", 10, "bold")
    ).pack(pady=5, ipady=7)

    tk.Button(
        user,
        text="CREATE ACCOUNT",
        command=user_register,
        width=22
    ).pack(pady=5, ipady=5)

# =========================================================
# ADMIN REGISTER
# =========================================================

def admin_register():

    clear()
    title("🔐 ADMIN REGISTRATION", PURPLE)

    box = tk.Frame(root, bg=WHITE, padx=40, pady=30)
    box.pack(pady=20)

    fields = {}

    for name in ["Username", "Email", "Password"]:

        tk.Label(
            box,
            text=name,
            bg=WHITE,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        e = tk.Entry(
            box,
            width=32,
            show="*" if name == "Password" else ""
        )
        e.pack(pady=7, ipady=5)

        fields[name] = e

    def save():

        try:

            cur.execute("""
            INSERT INTO admins(username,email,password)
            VALUES(?,?,?)
            """, (
                fields["Username"].get(),
                fields["Email"].get(),
                fields["Password"].get()
            ))

            db.commit()

            messagebox.showinfo(
                "Success",
                "Admin account created!"
            )

            home()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Username or email already exists."
            )

    tk.Button(
        box,
        text="CREATE ADMIN ACCOUNT",
        command=save,
        bg=GREEN,
        fg=WHITE,
        width=28,
        font=("Arial", 10, "bold")
    ).pack(pady=15, ipady=7)

    tk.Button(
        box,
        text="BACK",
        command=home,
        width=28
    ).pack(ipady=5)

# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login():

    clear()
    title("🔐 ADMIN LOGIN", PURPLE)

    box = tk.Frame(root, bg=WHITE, padx=40, pady=30)
    box.pack(pady=30)

    tk.Label(box, text="Username", bg=WHITE).pack(anchor="w")
    username = tk.Entry(box, width=32)
    username.pack(pady=7, ipady=5)

    tk.Label(box, text="Password", bg=WHITE).pack(anchor="w")
    password = tk.Entry(box, width=32, show="*")
    password.pack(pady=7, ipady=5)

    def check():

        cur.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username.get(), password.get())
        )

        if cur.fetchone():
            admin_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )

    tk.Button(
        box,
        text="LOGIN",
        command=check,
        bg=PURPLE,
        fg=WHITE,
        width=28,
        font=("Arial", 10, "bold")
    ).pack(pady=15, ipady=7)

    tk.Button(
        box,
        text="BACK",
        command=home,
        width=28
    ).pack(ipady=5)

# =========================================================
# USER REGISTER
# =========================================================

def user_register():

    clear()
    title("👤 CUSTOMER REGISTRATION", BLUE)

    box = tk.Frame(root, bg=WHITE, padx=35, pady=20)
    box.pack(pady=10)

    fields = {}

    for name in [
        "Name", "Username", "Email",
        "Phone", "City", "Password"
    ]:

        tk.Label(
            box,
            text=name,
            bg=WHITE
        ).pack(anchor="w")

        e = tk.Entry(
            box,
            width=32,
            show="*" if name == "Password" else ""
        )
        e.pack(pady=4, ipady=4)

        fields[name] = e

    def save():

        try:

            cur.execute("""
            INSERT INTO users
            (username,email,password,name,phone,city)
            VALUES(?,?,?,?,?,?)
            """, (
                fields["Username"].get(),
                fields["Email"].get(),
                fields["Password"].get(),
                fields["Name"].get(),
                fields["Phone"].get(),
                fields["City"].get()
            ))

            db.commit()

            messagebox.showinfo(
                "Success",
                "Customer account created!"
            )

            user_login()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Username or email already exists."
            )

    tk.Button(
        box,
        text="CREATE CUSTOMER ACCOUNT",
        command=save,
        bg=GREEN,
        fg=WHITE,
        width=28,
        font=("Arial", 10, "bold")
    ).pack(pady=12, ipady=6)

    tk.Button(
        box,
        text="BACK",
        command=home,
        width=28
    ).pack(ipady=5)

# =========================================================
# USER LOGIN
# =========================================================

def user_login():

    clear()
    title("👤 CUSTOMER LOGIN", BLUE)

    box = tk.Frame(root, bg=WHITE, padx=40, pady=30)
    box.pack(pady=30)

    tk.Label(box, text="Username", bg=WHITE).pack(anchor="w")
    username = tk.Entry(box, width=32)
    username.pack(pady=7, ipady=5)

    tk.Label(box, text="Password", bg=WHITE).pack(anchor="w")
    password = tk.Entry(box, width=32, show="*")
    password.pack(pady=7, ipady=5)

    def check():

        cur.execute("""
        SELECT id,name
        FROM users
        WHERE username=? AND password=?
        """, (
            username.get(),
            password.get()
        ))

        user = cur.fetchone()

        if user:
            customer_dashboard(user[0], user[1])
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password"
            )

    tk.Button(
        box,
        text="LOGIN",
        command=check,
        bg=BLUE,
        fg=WHITE,
        width=28,
        font=("Arial", 10, "bold")
    ).pack(pady=15, ipady=7)

    tk.Button(
        box,
        text="CREATE ACCOUNT",
        command=user_register,
        width=28
    ).pack(ipady=5)

# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_dashboard():

    clear()
    title("📊 ADMIN DASHBOARD", DARK)

    tk.Label(
        root,
        text="Manage your e-commerce business",
        font=("Arial", 13),
        bg=BG,
        fg=GRAY
    ).pack(pady=15)

    frame = tk.Frame(root, bg=BG)
    frame.pack()

    # PRODUCTS
    card1 = tk.Frame(frame, bg=WHITE, padx=25, pady=25)
    card1.grid(row=0, column=0, padx=10)

    tk.Label(
        card1,
        text="📦 PRODUCTS",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack()

    tk.Label(
        card1,
        text="Add and manage products",
        bg=WHITE
    ).pack(pady=8)

    tk.Button(
        card1,
        text="PRODUCT MANAGEMENT",
        command=admin_products,
        bg=BLUE,
        fg=WHITE,
        width=22
    ).pack(ipady=6)

    # CUSTOMERS
    card2 = tk.Frame(frame, bg=WHITE, padx=25, pady=25)
    card2.grid(row=0, column=1, padx=10)

    tk.Label(
        card2,
        text="👥 CUSTOMERS",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=GREEN
    ).pack()

    tk.Label(
        card2,
        text="View registered customers",
        bg=WHITE
    ).pack(pady=8)

    tk.Button(
        card2,
        text="CUSTOMER MANAGEMENT",
        command=admin_customers,
        bg=GREEN,
        fg=WHITE,
        width=22
    ).pack(ipady=6)

    # ORDERS
    card3 = tk.Frame(frame, bg=WHITE, padx=25, pady=25)
    card3.grid(row=0, column=2, padx=10)

    tk.Label(
        card3,
        text="🛍 ORDERS",
        font=("Arial", 16, "bold"),
        bg=WHITE,
        fg=ORANGE
    ).pack()

    tk.Label(
        card3,
        text="View customer orders",
        bg=WHITE
    ).pack(pady=8)

    tk.Button(
        card3,
        text="ORDER MANAGEMENT",
        command=admin_orders,
        bg=ORANGE,
        fg=WHITE,
        width=22
    ).pack(ipady=6)

    tk.Button(
        root,
        text="📥 DOWNLOAD CSV DATASET",
        command=download_csv,
        bg=GREEN,
        fg=WHITE,
        width=25,
        font=("Arial", 10, "bold")
    ).pack(pady=10, ipady=7)

    tk.Button(
        root,
        text="🚪 LOGOUT",
        command=home,
        bg=RED,
        fg=WHITE,
        width=25
    ).pack(pady=10, ipady=7)


# =========================================================
# DOWNLOAD DATABASE AS CSV
# =========================================================

def download_csv():
    try:
        cur.execute("""
        SELECT
            orders.id AS order_id,
            users.name AS customer_name,
            users.username,
            users.email,
            users.phone,
            users.city,
            products.name AS product,
            products.category,
            products.selling AS selling_price,
            products.cost AS cost_price,
            orders.quantity,
            orders.total,
            orders.profit,
            orders.status
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN products ON orders.product_id = products.id
        ORDER BY orders.id DESC
        """)

        rows = cur.fetchall()

        file_path = filedialog.asksaveasfilename(
            title="Save CSV Dataset",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="ecommerce_dataset.csv"
        )

        if not file_path:
            return

        headers = [
            "Order ID", "Customer Name", "Username", "Email",
            "Phone", "City", "Product", "Category",
            "Selling Price", "Cost Price", "Quantity",
            "Total", "Profit", "Status"
        ]

        with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

        messagebox.showinfo(
            "CSV Downloaded",
            f"Dataset saved successfully!\n\nLocation:\n{file_path}"
        )

    except Exception as e:
        messagebox.showerror(
            "Download Error",
            f"Could not create CSV file.\n\n{e}"
        )


# =========================================================
# ADMIN PRODUCT MANAGEMENT
# =========================================================

def admin_products():

    clear()
    title("📦 PRODUCT MANAGEMENT", BLUE)

    form = tk.Frame(root, bg=WHITE, padx=15, pady=15)
    form.pack(fill="x", padx=20)

    fields = [
        "Product", "Category",
        "Selling Price", "Cost Price", "Stock"
    ]

    entries = {}

    for i, field in enumerate(fields):

        tk.Label(
            form,
            text=field,
            bg=WHITE
        ).grid(row=0, column=i, padx=5)

        e = tk.Entry(form, width=16)
        e.grid(row=1, column=i, padx=5, pady=5)

        entries[field] = e

    def add():

        try:

            if not entries["Product"].get():
                raise ValueError

            cur.execute("""
            INSERT INTO products
            (name,category,selling,cost,stock)
            VALUES(?,?,?,?,?)
            """, (
                entries["Product"].get(),
                entries["Category"].get(),
                float(entries["Selling Price"].get()),
                float(entries["Cost Price"].get()),
                int(entries["Stock"].get())
            ))

            db.commit()
            load()

            for e in entries.values():
                e.delete(0, tk.END)

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter valid product details."
            )

    tk.Button(
        form,
        text="➕ ADD PRODUCT",
        command=add,
        bg=GREEN,
        fg=WHITE
    ).grid(row=1, column=5, padx=10, ipady=5)

    cols = (
        "ID", "Product", "Category",
        "Selling", "Cost", "Profit", "Stock"
    )

    table = ttk.Treeview(
        root,
        columns=cols,
        show="headings",
        height=11
    )

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=130)

    table.pack(fill="both", padx=20, pady=15)

    def load():

        for x in table.get_children():
            table.delete(x)

        cur.execute("SELECT * FROM products")

        for p in cur.fetchall():

            profit = p[3] - p[4]

            table.insert(
                "",
                tk.END,
                values=(
                    p[0], p[1], p[2],
                    f"₹{p[3]:,.2f}",
                    f"₹{p[4]:,.2f}",
                    f"₹{profit:,.2f}",
                    p[5]
                )
            )

    def delete():

        selected = table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a product."
            )
            return

        pid = table.item(
            selected[0]
        )["values"][0]

        cur.execute(
            "DELETE FROM products WHERE id=?",
            (pid,)
        )

        db.commit()
        load()

    tk.Button(
        root,
        text="🗑 DELETE",
        command=delete,
        bg=RED,
        fg=WHITE,
        width=15
    ).pack(side="left", padx=20)

    tk.Button(
        root,
        text="← DASHBOARD",
        command=admin_dashboard,
        width=15
    ).pack(side="right", padx=20)

    load()


# =========================================================
# ADMIN CUSTOMERS
# =========================================================

def admin_customers():

    clear()
    title("👥 CUSTOMER MANAGEMENT", GREEN)

    cols = (
        "ID", "Name", "Username",
        "Email", "Phone", "City"
    )

    table = ttk.Treeview(
        root,
        columns=cols,
        show="headings",
        height=16
    )

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=145)

    table.pack(fill="both", padx=25, pady=25)

    cur.execute("""
    SELECT id,name,username,email,phone,city
    FROM users
    """)

    for row in cur.fetchall():
        table.insert("", tk.END, values=row)

    tk.Button(
        root,
        text="← DASHBOARD",
        command=admin_dashboard,
        width=20
    ).pack(pady=10)


# =========================================================
# ADMIN ORDERS
# =========================================================

def admin_orders():

    clear()
    title("🛍 CUSTOMER ORDERS", ORANGE)

    cols = (
        "Order ID",
        "Customer",
        "Product",
        "Quantity",
        "Total",
        "Profit",
        "Status"
    )

    table = ttk.Treeview(
        root,
        columns=cols,
        show="headings",
        height=16
    )

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=130)

    table.pack(fill="both", padx=25, pady=25)

    cur.execute("""
    SELECT
        orders.id,
        users.name,
        products.name,
        orders.quantity,
        orders.total,
        orders.profit,
        orders.status
    FROM orders
    JOIN users ON orders.user_id = users.id
    JOIN products ON orders.product_id = products.id
    ORDER BY orders.id DESC
    """)

    for row in cur.fetchall():

        row = list(row)

        row[4] = f"₹{row[4]:,.2f}"
        row[5] = f"₹{row[5]:,.2f}"

        table.insert("", tk.END, values=row)

    tk.Button(
        root,
        text="← DASHBOARD",
        command=admin_dashboard,
        width=20
    ).pack(pady=10)


# =========================================================
# CUSTOMER DASHBOARD
# =========================================================

def customer_dashboard(user_id, name):

    clear()

    title(f"🛒 CUSTOMER STORE", BLUE)

    tk.Label(
        root,
        text=f"Welcome, {name}!",
        font=("Arial", 15, "bold"),
        bg=BG,
        fg=DARK
    ).pack(pady=10)

    tk.Button(
        root,
        text="🛍 MY ORDERS",
        command=lambda: my_orders(user_id, name),
        bg=PURPLE,
        fg=WHITE,
        width=18
    ).pack(pady=5)

    tk.Label(
        root,
        text="Available Products",
        font=("Arial", 17, "bold"),
        bg=BG,
        fg=DARK
    ).pack(pady=15)

    cols = (
        "ID",
        "Product",
        "Category",
        "Price",
        "Stock"
    )

    table = ttk.Treeview(
        root,
        columns=cols,
        show="headings",
        height=12
    )

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=150)

    table.pack(fill="both", padx=25)

    cur.execute("""
    SELECT id,name,category,selling,stock
    FROM products
    WHERE stock > 0
    """)

    for p in cur.fetchall():

        table.insert(
            "",
            tk.END,
            values=(
                p[0],
                p[1],
                p[2],
                f"₹{p[3]:,.2f}",
                p[4]
            )
        )

    # Quantity
    order_frame = tk.Frame(root, bg=BG)
    order_frame.pack(pady=15)

    tk.Label(
        order_frame,
        text="Quantity:",
        bg=BG,
        font=("Arial", 10, "bold")
    ).pack(side="left")

    quantity = tk.Entry(
        order_frame,
        width=8
    )
    quantity.pack(side="left", padx=10)

    def order():

        selected = table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Product",
                "Please select a product."
            )

            return

        try:
            qty = int(quantity.get())

            if qty <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid quantity."
            )

            return

        product_id = table.item(
            selected[0]
        )["values"][0]

        cur.execute(
            "SELECT selling,cost,stock,name FROM products WHERE id=?",
            (product_id,)
        )

        product = cur.fetchone()

        if qty > product[2]:

            messagebox.showerror(
                "Stock Error",
                f"Only {product[2]} items available."
            )

            return

        total = product[0] * qty
        profit = (product[0] - product[1]) * qty

        cur.execute("""
        INSERT INTO orders
        (user_id,product_id,quantity,total,profit)
        VALUES(?,?,?,?,?)
        """, (
            user_id,
            product_id,
            qty,
            total,
            profit
        ))

        cur.execute("""
        UPDATE products
        SET stock = stock - ?
        WHERE id=?
        """, (
            qty,
            product_id
        ))

        db.commit()

        messagebox.showinfo(
            "Order Successful",
            f"Product: {product[3]}\n"
            f"Quantity: {qty}\n"
            f"Total: ₹{total:,.2f}\n\n"
            "Order placed successfully!"
        )

        customer_dashboard(user_id, name)

    tk.Button(
        order_frame,
        text="🛒 PLACE ORDER",
        command=order,
        bg=GREEN,
        fg=WHITE,
        width=18,
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=10, ipady=5)

    tk.Button(
        root,
        text="🚪 LOGOUT",
        command=home,
        bg=RED,
        fg=WHITE,
        width=20
    ).pack(pady=12)


# =========================================================
# CUSTOMER ORDERS
# =========================================================

def my_orders(user_id, name):

    clear()

    title("🧾 MY ORDERS", PURPLE)

    cols = (
        "Order ID",
        "Product",
        "Quantity",
        "Total",
        "Profit",
        "Status"
    )

    table = ttk.Treeview(
        root,
        columns=cols,
        show="headings",
        height=15
    )

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=145)

    table.pack(fill="both", padx=25, pady=25)

    cur.execute("""
    SELECT
        orders.id,
        products.name,
        orders.quantity,
        orders.total,
        orders.profit,
        orders.status
    FROM orders
    JOIN products
    ON orders.product_id = products.id
    WHERE orders.user_id=?
    ORDER BY orders.id DESC
    """, (user_id,))

    for row in cur.fetchall():

        row = list(row)

        row[3] = f"₹{row[3]:,.2f}"
        row[4] = f"₹{row[4]:,.2f}"

        table.insert("", tk.END, values=row)

    tk.Button(
        root,
        text="← BACK TO STORE",
        command=lambda: customer_dashboard(user_id, name),
        width=20
    ).pack(pady=10)


# =========================================================
# START
# =========================================================

home()
root.mainloop()
