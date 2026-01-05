import tkinter as tk
from tkinter import ttk, messagebox
from user import UserDAO


class LoginDialog(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login stranka")
        self.geometry("400x260")
        self.resizable(False, False)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.user_dao = None
        self.logged_user = None

        self.create_widgets()

        self.bind('<Return>', lambda e: self.login())

        self.username_entry.focus()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Evidence výroby",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=10)

        ttk.Label(form_frame, text="Uzivatelské jmeno:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text="Heslo:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        login_btn = ttk.Button(
            button_frame,
            text="Login",
            command=self.login,
            width=15
        )
        login_btn.pack(side="left", padx=5)

        register_btn = ttk.Button(
            button_frame,
            text="Register",
            command=self.show_register_dialog,
            width=15
        )
        register_btn.pack(side="left", padx=5)

        cancel_btn = ttk.Button(
            button_frame,
            text="Storno",
            command=self.cancel,
            width=15
        )
        cancel_btn.pack(side="left", padx=5)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Chyba", "Vypln uzivatelske jmeno a heslo")
            return

        try:
            if not self.user_dao:
                self.user_dao = UserDAO()

            user = self.user_dao.authenticate(username, password)

            if user:
                self.logged_user = {
                    'user_id': user[0],
                    'username': user[1]
                }
                messagebox.showinfo(
                    "Úspěch",
                    f"Vítej, {self.logged_user['username']}!"
                )
                self.destroy()
            else:
                messagebox.showerror(
                    "Chyba",
                    "Nesprávné uživatelské jméno nebo heslo"
                )
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()

        except Exception as e:
            messagebox.showerror(
                "Chyba připojení",
                f"Nepodařilo se připojit k databázi:\n{str(e)}\n\n"
                "Zkontroluj, zda existuje tabulka Users:"
            )
            self.logged_user = None

    def show_register_dialog(self):
        register_window = tk.Toplevel(self)
        register_window.title("Registrace nového uživatele")
        register_window.geometry("400x250")
        register_window.resizable(False, False)

        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f'{width}x{height}+{x}+{y}')

        main_frame = ttk.Frame(register_window, padding="30")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Vytvoření nového účtu",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Formulář
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="x", pady=10)

        ttk.Label(form_frame, text="Uživatelské jméno:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        new_username = ttk.Entry(form_frame, width=25)
        new_username.grid(row=0, column=1, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text="Heslo:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        new_password = ttk.Entry(form_frame, width=25, show="*")
        new_password.grid(row=1, column=1, pady=5, padx=(10, 0))

        ttk.Label(form_frame, text="Potvrzení hesla:").grid(
            row=2, column=0, sticky="w", pady=5
        )
        confirm_password = ttk.Entry(form_frame, width=25, show="*")
        confirm_password.grid(row=2, column=1, pady=5, padx=(10, 0))

        def register():
            username = new_username.get().strip()
            password = new_password.get()
            confirm = confirm_password.get()

            if not username or not password:
                messagebox.showerror("Chyba", "Vyplň všechna pole")
                return

            if len(username) < 3:
                messagebox.showerror("Chyba", "Uživatelské jméno musí mít alespoň 3 znaky")
                return

            if len(password) < 6:
                messagebox.showerror("Chyba", "Heslo musí mít alespoň 6 znaků")
                return

            if password != confirm:
                messagebox.showerror("Chyba", "Hesla se neshodují")
                return

            try:
                if not self.user_dao:
                    self.user_dao = UserDAO()

                self.user_dao.insert(username, password)
                messagebox.showinfo(
                    "Úspěch",
                    f"Uživatel '{username}' byl úspěšně vytvořen!\n\n"
                    "Nyní se můžeš přihlásit."
                )
                register_window.destroy()

                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, username)
                self.password_entry.focus()

            except Exception as e:
                error_msg = str(e)
                if "UNIQUE" in error_msg or "unique" in error_msg.lower():
                    messagebox.showerror(
                        "Chyba",
                        f"Uživatelské jméno '{username}' již existuje.\n"
                        "Zvol jiné jméno."
                    )
                else:
                    messagebox.showerror(
                        "Chyba při registraci",
                        f"Nepodařilo se vytvořit uživatele:\n{error_msg}"
                    )

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="Vytvořit účet",
            command=register,
            width=15
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Zrušit",
            command=register_window.destroy,
            width=15
        ).pack(side="left", padx=5)

        new_username.focus()

        register_window.bind('<Return>', lambda e: register())

    def cancel(self):
        self.logged_user = None
        self.destroy()

    def get_logged_user(self):
        return self.logged_user

def show_login():
    login = LoginDialog()
    login.mainloop()
    return login.get_logged_user()

if __name__ == "__main__":
    user = show_login()
    if user:
        print(f"Přihlášený uživatel: {user}")
    else:
        print("Přihlášení zrušeno")