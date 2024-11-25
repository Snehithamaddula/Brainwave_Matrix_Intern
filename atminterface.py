import tkinter as tk
from tkinter import messagebox

class ATM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.dummy_account = "12345678"  # Dummy account number
        self.dummy_pin = "1234"  # Dummy PIN
        self.balance = 500  # Initial balance

        # Authentication Frame
        self.auth_frame = tk.Frame(self.root)
        self.auth_frame.pack(pady=20)

        tk.Label(self.auth_frame, text="ATM Login", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.auth_frame, text="Account Number:").pack()
        self.account_entry = tk.Entry(self.auth_frame, width=25)
        self.account_entry.pack(pady=5)

        tk.Label(self.auth_frame, text="PIN:").pack()
        self.pin_entry = tk.Entry(self.auth_frame, show="*", width=25)
        self.pin_entry.pack(pady=5)

        tk.Button(self.auth_frame, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        account = self.account_entry.get()
        pin = self.pin_entry.get()

        if account == self.dummy_account and pin == self.dummy_pin:
            messagebox.showinfo("Login Success", "Authentication Successful!")
            self.auth_frame.destroy()
            self.show_main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid account number or PIN!")

    def show_main_menu(self):
        # Main Menu Frame
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Welcome to ATM", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Balance Inquiry", width=20, command=self.check_balance).pack(pady=5)
        tk.Button(self.menu_frame, text="Deposit Money", width=20, command=self.deposit_money).pack(pady=5)
        tk.Button(self.menu_frame, text="Withdraw Money", width=20, command=self.withdraw_money).pack(pady=5)
        tk.Button(self.menu_frame, text="Exit", width=20, command=self.root.quit).pack(pady=5)

    def check_balance(self):
        messagebox.showinfo("Balance Inquiry", f"Your current balance is: Rs.{self.balance:.2f}")

    def deposit_money(self):
        # Open Deposit Window
        self.show_transaction_window("Deposit Money", self.perform_deposit)

    def withdraw_money(self):
        # Open Withdraw Window
        self.show_transaction_window("Withdraw Money", self.perform_withdrawal)

    def show_transaction_window(self, title, command):
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title(title)

        tk.Label(transaction_window, text=f"Enter amount to {title.lower()}:").pack(pady=10)
        amount_entry = tk.Entry(transaction_window, width=20)
        amount_entry.pack(pady=5)

        def perform_transaction():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Invalid amount! Please enter a positive value.")
                else:
                    transaction_window.destroy()
                    command(amount)
            except ValueError:
                messagebox.showerror("Error", "Invalid input! Please enter a numeric value.")

        tk.Button(transaction_window, text="Submit", command=perform_transaction).pack(pady=10)

    def perform_deposit(self, amount):
        self.balance += amount
        messagebox.showinfo("Success", f"Rs.{amount:.2f} deposited successfully!. Now your total balance is Rs.{self.balance:.2f}")

    def perform_withdrawal(self, amount):
        if amount > self.balance:
            messagebox.showerror("Error", "Insufficient balance!")
        else:
            self.balance -= amount
            messagebox.showinfo("Success", f"Rs.{amount:.2f} withdrawn successfully!")

# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = ATM_GUI(root)
    root.mainloop()
