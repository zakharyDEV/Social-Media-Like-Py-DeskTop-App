import customtkinter as ctk
import sqlite3
from tkinter import filedialog
from ttkthemes import ThemedStyle

# Step 2: Implement Posting System and User Interactions

# Create a SQLite database connection
conn = sqlite3.connect('social_media.db')
cursor = conn.cursor()

# Create a table for posts
cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  post_type TEXT,
                  content TEXT,
                  likes INTEGER,
                  comments INTEGER)''')

# Create a table for user-to-user conversations
cursor.execute('''CREATE TABLE IF NOT EXISTS conversations
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sender_id INTEGER,
                  receiver_id INTEGER,
                  message TEXT,
                  timestamp TEXT)''')

# Function to handle post submission
def submit_post(user_id, post_type, content):
    cursor.execute('''INSERT INTO posts (user_id, post_type, content, likes, comments)
                      VALUES (?, ?, ?, 0, 0)''', (user_id, post_type, content))
    conn.commit()

# Function to handle post liking
def like_post(post_id):
    cursor.execute('''UPDATE posts SET likes = likes + 1 WHERE id = ?''', (post_id,))
    conn.commit()

# Function to handle post commenting
def add_comment(post_id):
    cursor.execute('''UPDATE posts SET comments = comments + 1 WHERE id = ?''', (post_id,))
    conn.commit()

# Function to handle sending messages in conversations
def send_message(sender_id, receiver_id, message):
    cursor.execute('''INSERT INTO conversations (sender_id, receiver_id, message, timestamp)
                      VALUES (?, ?, ?, datetime('now'))''', (sender_id, receiver_id, message))
    conn.commit()

# Step 3: Design User Interface and Additional Features

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Social Media App")

        # Apply themes to the application
        style = ThemedStyle(self)
        style.set_theme("arc")

        # Create a navigation bar for buttons
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x")

        # Create buttons on the nav bar
        self.post_button = ctk.CTkButton(nav_frame, text="New Post", command=self.open_post_dialog)
        self.post_button.pack(side="left", padx=20, pady=10)

        self.conversation_button = ctk.CTkButton(nav_frame, text="Start a Conversation", command=self.open_conversation_dialog)
        self.conversation_button.pack(side="left", padx=20, pady=10)

        self.account_button = ctk.CTkButton(nav_frame, text="My Account", command=self.open_account_tab)
        self.account_button.pack(side="left", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(nav_frame)
        self.search_entry.pack(side="left", padx=20, pady=10)

        self.search_button = ctk.CTkButton(nav_frame, text="Search", command=self.search_users)
        self.search_button.pack(side="left", padx=20, pady=10)

        self.settings_button = ctk.CTkButton(nav_frame, text="Settings", command=self.open_settings_tab)
        self.settings_button.pack(side="left", padx=20, pady=10)

        # Additional Features
        self.selected_file_label = ctk.CTkLabel(self, text="No File Selected")
        self.selected_file_label.pack(pady=10)

        self.content_entry = ctk.CTkEntry(self)
        self.content_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_post)
        self.submit_button.pack(pady=10)

    def open_post_dialog(self):
        # Create a dialog for submitting a post
        post_dialog = ctk.CTkToplevel(self)
        post_dialog.title("New Post")

        file_button = ctk.CTkButton(post_dialog, text="Select File", command=self.open_file_dialog)
        file_button.pack(pady=10)

        self.selected_file_label = ctk.CTkLabel(post_dialog, text="No File Selected")
        self.selected_file_label.pack(pady=10)

        content_label = ctk.CTkLabel(post_dialog, text="Content:")
        content_label.pack(pady=10)

        self.content_entry = ctk.CTkEntry(post_dialog)
        self.content_entry.pack(pady=10)

        submit_button = ctk.CTkButton(post_dialog, text="Submit", command=self.submit_post)
        submit_button.pack(pady=10)

    def open_file_dialog(self):
        # Open a file dialog to select the file
        file_path = filedialog.askopenfilename()
        if file_path:
            # Display the selected file path in the label
            self.selected_file_label.config(text=file_path)

    def submit_post(self):
        # Implement the logic to submit a post
        # Get the user_id from the current logged in user
        user_id = 1  # Replace with the actual user_id
        # Get the post type based on the selected file
        post_type = self.get_file_type()
        content = self.content_entry.get()
        # Call the submit_post function with the user_id, post_type, and content
        submit_post(user_id, post_type, content)

    def get_file_type(self):
        # Check the extension of the selected file
        # Return "image" if the extension is .jpg or .png
        # Return "video" if the extension is .mp4
        # Return "text" otherwise
        file_path = self.selected_file_label.cget("text")
        if file_path.lower().endswith(('.jpg', '.png')):
            return "image"
        elif file_path.lower().endswith('.mp4'):
            return "video"
        else:
            return "text"

    def open_conversation_dialog(self):
        # Create a dialog for starting a conversation
        conversation_dialog = ctk.CTkToplevel(self)
        conversation_dialog.title("Start Conversation")

        receiver_label = ctk.CTkLabel(conversation_dialog, text="Receiver ID:")
        receiver_label.pack(pady=10)

        receiver_entry = ctk.CTkEntry(conversation_dialog)
        receiver_entry.pack(pady=10)

        message_label = ctk.CTkLabel(conversation_dialog, text="Message:")
        message_label.pack(pady=10)

        message_entry = ctk.CTkEntry(conversation_dialog)
        message_entry.pack(pady=10)

        send_button = ctk.CTkButton(conversation_dialog, text="Send", command=self.send_message)
        send_button.pack(pady=10)

    def send_message(self):
        # Implement the logic to send a message
        # Get the sender_id from the current logged in user
        sender_id = 1  # Replace with the actual sender_id
        receiver_id = receiver_entry.get()
        message = message_entry.get()
        # Call the send_message function with the sender_id, receiver_id, and message
        send_message(sender_id, receiver_id, message)

    def open_account_tab(self):
        # Create a tab for "My Account"
        account_tab = ctk.CTkToplevel(self)
        account_tab.title("My Account")

        # Display user account information, profile picture, and settings

    def search_users(self):
        search_query = self.search_entry.get()
        # Implement the logic to search for user accounts based on search_query
        # Display the search results in the UI

    def open_settings_tab(self):
        # Create a tab for app settings
        settings_tab = ctk.CTkToplevel(self)
        settings_tab.title("Settings")



app = App()
app.mainloop()