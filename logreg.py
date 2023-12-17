import customtkinter as ctk
import sqlite3
import bcrypt
import re

# Create database and user table
connection = sqlite3.connect("social_media.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT)")
connection.commit()

# Create login and register system
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        # Verify the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user[2]):
            login_message_label.configure(text="Login successful", fg="green")
        else:
            login_message_label.configure(text="Invalid username or password", fg="red")
    else:
        login_message_label.configure(text="Invalid username or password", fg="red")

def register():
    username = register_username_entry.get()
    password = register_password_entry.get()

    # Validate the password
    if len(password) < 6 or not re.search(r'\d', password):
        register_message_label.configure(text="Password must be at least 6 characters long and contain at least 1 number", fg="red")
        return 

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        register_message_label.configure(text="Username already taken", fg="red")
    else:
        # Generate a unique user ID
        cursor.execute("SELECT MAX(userID) FROM users")
        max_id = cursor.fetchone()[0]
        new_user_id = max_id + 1 if max_id is not None else 1

        # Insert the new user into the database with the hashed password and the generated user ID
        cursor.execute("INSERT INTO users (userID, username, password) VALUES (?, ?, ?)", (new_user_id, username, hashed_password))
        connection.commit()

        # Display registration success message
        register_message_label.configure(text="Registration successful", fg="green")

        # Clear the entry fields
        register_username_entry.delete(0, ctk.END)
        register_password_entry.delete(0, ctk.END)



# Create main app window
app = ctk.CTk()
app.geometry("400x300")
app.resizable(False, False) 
app.title("Social Media - Login/Register")

toggle_button = ctk.CTkButton(app, text="Register/Login", width=10, command=lambda: toggle_register())
toggle_button.pack(pady=10, side=ctk.BOTTOM) 


# Create login frame
login_frame = ctk.CTkFrame(app)
login_frame.pack(pady=20, padx=20, fill=ctk.BOTH, expand=True)


# Create a password visibility toggle

login_label = ctk.CTkLabel(login_frame, text="Login", font=("Arial", 20))
login_label.pack(pady=10)

login_form_frame = ctk.CTkFrame(login_frame)
login_form_frame.pack(pady=10)

login_username_label = ctk.CTkLabel(login_form_frame, text="Username:")
login_username_label.grid(row=0, column=0, sticky="w")

login_username_entry = ctk.CTkEntry(login_form_frame)
login_username_entry.grid(row=0, column=1, padx=5)

login_password_label = ctk.CTkLabel(login_form_frame, text="Password:")
login_password_label.grid(row=1, column=0, sticky="w")

login_password_entry = ctk.CTkEntry(login_form_frame)
login_password_entry.grid(row=1, column=1, padx=5)

login_button = ctk.CTkButton(login_frame, text="Login", width=10, command=login)
login_button.pack(pady=10)

login_message_label = ctk.CTkLabel(login_frame, text="")
login_message_label.pack()




# Create register frame
register_frame = ctk.CTkFrame(app)
register_frame.pack(pady=20, padx=20, fill=ctk.BOTH, expand=True)

register_label = ctk.CTkLabel(register_frame, text="Register", font=("Arial", 20))
register_label.pack(pady=10)

register_form_frame = ctk.CTkFrame(register_frame)
register_form_frame.pack(pady=10)

register_username_label = ctk.CTkLabel(register_form_frame, text="Username:")
register_username_label.grid(row=0, column=0, sticky="w")

register_username_entry = ctk.CTkEntry(register_form_frame)
register_username_entry.grid(row=0, column=1, padx=5)

register_password_label = ctk.CTkLabel(register_form_frame, text="Password:")
register_password_label.grid(row=1, column=0, sticky="w")

register_password_entry = ctk.CTkEntry(register_form_frame)
register_password_entry.grid(row=1, column=1, padx=5)

register_button = ctk.CTkButton(register_frame, text="Register", width=10, command=register)
register_button.pack(pady=10)

register_message_label = ctk.CTkLabel(register_frame, text="")
register_message_label.pack()

# After creating the register frame, add the following code to hide it initially
# After creating the register frame, add the following code to hide it initially
register_frame.pack_forget()

# Create a button to toggle the register form
register_frame.place(in_=login_frame, relx=0.5, rely=0.5, anchor="center")
# Define the toggle_register function
def toggle_register():
    if str(register_frame.winfo_ismapped()) == "0":
        register_frame.place_configure(rely=1.0)  # Set the initial position below the login frame
        register_frame.place(in_=login_frame, relx=0.5, rely=0.5, anchor="center")  # Position the register frame over the login frame
        register_frame.lift()  # Raise the register frame to appear over the login frame
    else:
        register_frame.place_forget()

# Configure grid layout to scale properly
app.grid_columnconfigure(0, weight=1)
login_frame.grid_columnconfigure(0, weight=1)
register_frame.grid_columnconfigure(0, weight=1)

app.mainloop()