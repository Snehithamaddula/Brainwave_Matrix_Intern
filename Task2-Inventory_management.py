import tkinter as tk
from tkinter import messagebox, ttk


class InventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")

        # User credentials for authentication
        self.users = {"admin": "password"}  # Default user

        # Inventory data (stored as a dictionary)
        self.inventory = {}

        # Authentication Screen
        self.auth_frame = tk.Frame(self.root)
        self.auth_frame.pack(pady=20)

        tk.Label(self.auth_frame, text="Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.auth_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.auth_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.auth_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.auth_frame, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.auth_frame, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.users.get(username) == password:
            messagebox.showinfo("Login Success", "Welcome to the Inventory Manager!")
            self.auth_frame.destroy()
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def show_main_menu(self):
        # Main Menu Frame
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Inventory Management System", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Add Product", width=20, command=self.add_product).pack(pady=5)
        tk.Button(self.menu_frame, text="Edit Product", width=20, command=self.edit_product).pack(pady=5)
        tk.Button(self.menu_frame, text="Delete Product", width=20, command=self.delete_product).pack(pady=5)
        tk.Button(self.menu_frame, text="View Inventory", width=20, command=self.view_inventory).pack(pady=5)
        tk.Button(self.menu_frame, text="Low Stock Report", width=20, command=self.low_stock_report).pack(pady=5)
        tk.Button(self.menu_frame, text="Logout", width=20, command=self.logout).pack(pady=5)

    def add_product(self):
        self.open_product_window("Add Product", self.perform_add_product)

    def edit_product(self):
        product_id = self.get_product_id("Edit Product")
        if product_id:
            if product_id in self.inventory:
                # Open a new window to edit product details
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Edit Product")

                # Display current values for reference
                current_product = self.inventory[product_id]
                tk.Label(edit_window, text=f"Editing Product ID: {product_id}", font=("Arial", 14)).pack(pady=10)

                tk.Label(edit_window, text="Current Name:").pack()
                tk.Label(edit_window, text=current_product["name"]).pack()

                tk.Label(edit_window, text="New Name (leave blank to keep current):").pack()
                name_entry = tk.Entry(edit_window)
                name_entry.pack(pady=5)

                tk.Label(edit_window, text="Current Quantity:").pack()
                tk.Label(edit_window, text=current_product["quantity"]).pack()

                tk.Label(edit_window, text="New Quantity (leave blank to keep current):").pack()
                quantity_entry = tk.Entry(edit_window)
                quantity_entry.pack(pady=5)

                tk.Label(edit_window, text="Current Price:").pack()
                tk.Label(edit_window, text=current_product["price"]).pack()

                tk.Label(edit_window, text="New Price (leave blank to keep current):").pack()
                price_entry = tk.Entry(edit_window)
                price_entry.pack(pady=5)

                def update_product():
                    # Get updated details from user inputs
                    new_name = name_entry.get().strip()
                    new_quantity = quantity_entry.get().strip()
                    new_price = price_entry.get().strip()

                    # Update only if the field is not empty
                    if new_name:
                        current_product["name"] = new_name
                    if new_quantity:
                        try:
                            current_product["quantity"] = int(new_quantity)
                        except ValueError:
                            messagebox.showerror("Error", "Quantity must be a numeric value!")
                            return
                    if new_price:
                        try:
                            current_product["price"] = float(new_price)
                        except ValueError:
                            messagebox.showerror("Error", "Price must be a numeric value!")
                            return

                    # Notify the user and close the edit window
                    self.inventory[product_id] = current_product
                    messagebox.showinfo("Success", "Product updated successfully!")
                    edit_window.destroy()

                tk.Button(edit_window, text="Update Product", command=update_product).pack(pady=10)
            else:
                messagebox.showerror("Error", f"Product ID {product_id} not found!")

    def delete_product(self):
        product_id = self.get_product_id("Delete Product")
        if product_id:
            if product_id in self.inventory:
                del self.inventory[product_id]
                messagebox.showinfo("Success", f"Product ID {product_id} deleted successfully!")
            else:
                messagebox.showerror("Error", f"Product ID {product_id} not found!")

    def view_inventory(self):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventory Report")

        columns = ("ID", "Name", "Quantity", "Price")
        tree = ttk.Treeview(inventory_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill="both", expand=True)

        for product_id, details in self.inventory.items():
            tree.insert("", "end", values=(product_id, details["name"], details["quantity"], details["price"]))

    def low_stock_report(self):
        low_stock_window = tk.Toplevel(self.root)
        low_stock_window.title("Low Stock Report")

        columns = ("ID", "Name", "Quantity")
        tree = ttk.Treeview(low_stock_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill="both", expand=True)

        for product_id, details in self.inventory.items():
            if details["quantity"] < 5:  # Threshold for low stock
                tree.insert("", "end", values=(product_id, details["name"], details["quantity"]))

    def logout(self):
        self.menu_frame.destroy()
        self.__init__(self.root)  # Restart the application

    def open_product_window(self, title, command, edit=False):
        product_window = tk.Toplevel(self.root)
        product_window.title(title)

        tk.Label(product_window, text="Product ID:").pack(pady=5)
        product_id_entry = tk.Entry(product_window)
        product_id_entry.pack(pady=5)

        if not edit:
            tk.Label(product_window, text="Product Name:").pack(pady=5)
            product_name_entry = tk.Entry(product_window)
            product_name_entry.pack(pady=5)

            tk.Label(product_window, text="Quantity:").pack(pady=5)
            quantity_entry = tk.Entry(product_window)
            quantity_entry.pack(pady=5)

            tk.Label(product_window, text="Price:").pack(pady=5)
            price_entry = tk.Entry(product_window)
            price_entry.pack(pady=5)
        else:
            product_name_entry, quantity_entry, price_entry = None, None, None

        def perform_transaction():
            product_id = product_id_entry.get()
            if not product_id:
                messagebox.showerror("Error", "Product ID cannot be empty!")
                return

            if not edit:
                product_name = product_name_entry.get()
                try:
                    quantity = int(quantity_entry.get())
                    price = float(price_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Price must be numeric values!")
                    return

                if product_id in self.inventory:
                    messagebox.showerror("Error", "Product ID already exists!")
                else:
                    self.inventory[product_id] = {"name": product_name, "quantity": quantity, "price": price}
                    messagebox.showinfo("Success", "Product added successfully!")
            else:
                if product_id in self.inventory:
                    new_name = product_name_entry.get() if product_name_entry else self.inventory[product_id]["name"]
                    try:
                        new_quantity = int(quantity_entry.get()) if quantity_entry else self.inventory[product_id][
                            "quantity"]
                        new_price = float(price_entry.get()) if price_entry else self.inventory[product_id]["price"]
                    except ValueError:
                        messagebox.showerror("Error", "Quantity and Price must be numeric values!")
                        return

                    self.inventory[product_id] = {"name": new_name, "quantity": new_quantity, "price": new_price}
                    messagebox.showinfo("Success", "Product updated successfully!")
                else:
                    messagebox.showerror("Error", "Product ID not found!")

            product_window.destroy()

        tk.Button(product_window, text="Submit", command=perform_transaction).pack(pady=10)

    def perform_add_product(self, product_id, name, quantity, price):
        self.inventory[product_id] = {"name": name, "quantity": quantity, "price": price}
        messagebox.showinfo("Success", "Product added successfully!")

    def perform_edit_product(self, product_id, name=None, quantity=None, price=None):
        if product_id in self.inventory:
            if name:
                self.inventory[product_id]["name"] = name
            if quantity:
                self.inventory[product_id]["quantity"] = quantity
            if price:
                self.inventory[product_id]["price"] = price
            messagebox.showinfo("Success", "Product updated successfully!")
        else:
            messagebox.showerror("Error", "Product ID not found!")

    def get_product_id(self, title):
        product_id_window = tk.Toplevel(self.root)
        product_id_window.title(title)

        # Create a StringVar to capture input
        product_id_var = tk.StringVar()

        tk.Label(product_id_window, text="Enter Product ID:").pack(pady=10)
        product_id_entry = tk.Entry(product_id_window, textvariable=product_id_var)
        product_id_entry.pack(pady=5)

        def submit():
            # Close the window on submit
            product_id_window.destroy()

        tk.Button(product_id_window, text="Submit", command=submit).pack(pady=10)

        # Wait for the user to close the Toplevel window
        product_id_window.grab_set()
        product_id_window.wait_window()

        # Return the entered product ID
        return product_id_var.get()


# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManager(root)
    root.mainloop()
