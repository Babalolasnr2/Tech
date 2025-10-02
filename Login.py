import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

class AuthSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login System")
        self.root.geometry("400x300")
        
        # Initialize database
        self.init_database()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=50)
        
        self.show_login_page()
    
    def init_database(self):
        """Initialize SQLite database and create users table"""
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def hash_password(self, password):
        """Simple password hashing using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_frame(self):
        """Clear all widgets from the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_login_page(self):
        """Display the login page"""
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text="Login", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Username
        tk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.login_username = tk.Entry(self.main_frame)
        self.login_username.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(self.main_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.login_password = tk.Entry(self.main_frame, show="*")
        self.login_password.grid(row=2, column=1, padx=5, pady=5)
        
        # Login button
        tk.Button(self.main_frame, text="Login", command=self.login, 
                 bg="lightblue", width=15).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Signup link
        tk.Button(self.main_frame, text="Don't have an account? Sign up", 
                 command=self.show_signup_page, border=0, fg="blue", 
                 cursor="hand2").grid(row=4, column=0, columnspan=2, pady=5)
    
    def show_signup_page(self):
        """Display the signup page"""
        self.clear_frame()
        
        # Title
        tk.Label(self.main_frame, text="Sign Up", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Username
        tk.Label(self.main_frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.signup_username = tk.Entry(self.main_frame)
        self.signup_username.grid(row=1, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(self.main_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.signup_password = tk.Entry(self.main_frame, show="*")
        self.signup_password.grid(row=2, column=1, padx=5, pady=5)
        
        # Confirm Password
        tk.Label(self.main_frame, text="Confirm Password:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.signup_confirm_password = tk.Entry(self.main_frame, show="*")
        self.signup_confirm_password.grid(row=3, column=1, padx=5, pady=5)
        
        # Signup button
        tk.Button(self.main_frame, text="Sign Up", command=self.signup, 
                 bg="lightgreen", width=15).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Login link
        tk.Button(self.main_frame, text="Already have an account? Login", 
                 command=self.show_login_page, border=0, fg="blue", 
                 cursor="hand2").grid(row=5, column=0, columnspan=2, pady=5)
    
    def login(self):
        """Handle login process"""
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        hashed_password = self.hash_password(password)
        
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                           (username, hashed_password))
        user = self.cursor.fetchone()
        
        if user:
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.show_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def signup(self):
        """Handle signup process"""
        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm_password = self.signup_confirm_password.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters long")
            return
        
        hashed_password = self.hash_password(password)
        
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                               (username, hashed_password))
            self.conn.commit()
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.show_login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
    
    def show_dashboard(self, username):
        """Show dashboard after successful login"""
        self.clear_frame()
        
        tk.Label(self.main_frame, text=f"Welcome, {username}!", 
                font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self.main_frame, text="You have successfully logged in!", 
                font=("Arial", 12)).pack(pady=10)
        
        tk.Button(self.main_frame, text="Logout", command=self.show_login_page,
                 bg="lightcoral", width=15).pack(pady=20)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Run the application
if __name__ == "__main__":
    app = AuthSystem()
    app.run()
