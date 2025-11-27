import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk


#  DATABASE CONNECTION

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="newsblock"
    )


#  MAIN APPLICATION CLASS

class NewsBlockApp:

    def __init__(self, root):
        self.root = root
        self.root.title("NewsBlock - DBMS Project")
        self.root.geometry("750x500")

        title = tk.Label(root, text="NewsBlock Management System", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=15)

        # Buttons Frame
        frame = tk.Frame(root)
        frame.pack(pady=10)

        btn1 = tk.Button(frame, text="Add Users", width=20, command=self.add_users_window)
        btn2 = tk.Button(frame, text="Add News", width=20, command=self.add_news_window)
        btn3 = tk.Button(frame, text="View Users", width=20, command=self.view_users)
        btn4 = tk.Button(frame, text="View News", width=20, command=self.view_news)
        btn5 = tk.Button(frame, text="Update Users", width=20, command=self.update_users_window)
        btn6 = tk.Button(frame, text="Delete Users", width=20, command=self.delete_users_window)

        btn1.grid(row=0, column=0, padx=10, pady=5)
        btn2.grid(row=0, column=1, padx=10, pady=5)
        btn3.grid(row=1, column=0, padx=10, pady=5)
        btn4.grid(row=1, column=1, padx=10, pady=5)
        btn5.grid(row=2, column=0, padx=10, pady=5)
        btn6.grid(row=2, column=1, padx=10, pady=5)


    # ADD USER 

    def add_users_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add Users")
        win.geometry("350x300")

        tk.Label(win, text="Name").pack()
        name = tk.Entry(win)
        name.pack()

        tk.Label(win, text="Email").pack()
        email = tk.Entry(win)
        email.pack()

        tk.Label(win, text="Age").pack()
        age = tk.Entry(win)
        age.pack()

        def save_users():
            db = connect()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO user(u_name, u_email, u_age) VALUES (%s,%s,%s)",
                (name.get(), email.get(), age.get())
            )
            db.commit()
            messagebox.showinfo("Success", "User added!")
            db.close()

        tk.Button(win, text="Save", command=save_users).pack(pady=10)


    # ADD NEWS

    def add_news_window(self):
        win = tk.Toplevel(self.root)
        win.title("Add News")
        win.geometry("400x350")

        tk.Label(win, text="User ID").pack()
        uid = tk.Entry(win)
        uid.pack()

        tk.Label(win, text="News Title").pack()
        title = tk.Entry(win)
        title.pack()

        tk.Label(win, text="News Body").pack()
        body = tk.Text(win, height=6)
        body.pack()

        def save_news():
            db = connect()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO news(u_id, n_title, n_body) VALUES (%s,%s,%s)",
                (uid.get(), title.get(), body.get("1.0", tk.END))
            )
            db.commit()
            messagebox.showinfo("Success", "News added!")
            db.close()

        tk.Button(win, text="Save", command=save_news).pack(pady=10)

    
    # VIEW USERS
    
    def view_users(self):
        win = tk.Toplevel(self.root)
        win.title("All Users")
        win.geometry("600x400")

        table = ttk.Treeview(win, columns=("id","name","email","age"), show="headings")
        table.heading("id", text="User ID")
        table.heading("name", text="Name")
        table.heading("email", text="Email")
        table.heading("age", text="Age")
        table.pack(fill=tk.BOTH, expand=True)

        db = connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM users")
        for row in cur.fetchall():
            table.insert("", tk.END, values=row)
        db.close()

    
    # VIEW NEWS
    
    def view_news(self):
        win = tk.Toplevel(self.root)
        win.title("All News")
        win.geometry("700x400")

        table = ttk.Treeview(win, columns=("nid","uid","title","body","time"), show="headings")
        table.heading("nid", text="News ID")
        table.heading("uid", text="User ID")
        table.heading("title", text="Title")
        table.heading("body", text="Body")
        table.heading("time", text="Created At")
        table.pack(fill=tk.BOTH, expand=True)

        db = connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM news")
        for row in cur.fetchall():
            table.insert("", tk.END, values=row)
        db.close()

    
    # UPDATE 
    
    def update_users_window(self):
        win = tk.Toplevel(self.root)
        win.title("Update User")
        win.geometry("350x300")

        tk.Label(win, text="User ID to Update").pack()
        uid = tk.Entry(win)
        uid.pack()

        tk.Label(win, text="New Name").pack()
        name = tk.Entry(win)
        name.pack()

        tk.Label(win, text="New Email").pack()
        email = tk.Entry(win)
        email.pack()

        tk.Label(win, text="New Age").pack()
        age = tk.Entry(win)
        age.pack()

        def update_users():
            db = connect()
            cur = db.cursor()
            cur.execute(
                "UPDATE user SET u_name=%s, u_email=%s, u_age=%s WHERE u_id=%s",
                (name.get(), email.get(), age.get(), uid.get())
            )
            db.commit()
            messagebox.showinfo("Success", "User updated!")
            db.close()

        tk.Button(win, text="Update", command=update_users).pack(pady=10)

    
    # DELETE
    
    def delete_users_window(self):
        win = tk.Toplevel(self.root)
        win.title("Delete User")
        win.geometry("300x200")

        tk.Label(win, text="User ID").pack()
        uid = tk.Entry(win)
        uid.pack()

        def delete_users():
            db = connect()
            cur = db.cursor()
            cur.execute("DELETE FROM user WHERE u_id=%s", (uid.get(),))
            db.commit()
            messagebox.showinfo("Success", "User deleted!")
            db.close()

        tk.Button(win, text="Delete", command=delete_users).pack(pady=10)


#  RUN APP

root = tk.Tk()
app = NewsBlockApp(root)
root.mainloop()
