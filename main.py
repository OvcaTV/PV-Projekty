import tkinter as tk
from tkinter import ttk, messagebox

from DAO.productionEnd import ProductionEnd
from DAO.productionOverviewVW import ProductionOverviewVW
from DAO.machineUsageVW import MachineUsageVW
from DAO.Pristroje import MachineDAO
from DAO.produktManagement import Product
from DAO.objednaniProdukce import ProductionOrder
from DAO.report import ReportsDAO


class ProductionApp(tk.Tk):
    def __init__(self, logged_user=None):
        super().__init__()
        self.logged_user = logged_user

        self.title("Evidence výroby")
        self.geometry("1500x650")

        self.service_dao = ProductionEnd()
        self.order_view_dao = ProductionOverviewVW()
        self.machine_view_dao = MachineUsageVW()
        self.machine_dao = MachineDAO()
        self.product_dao = Product()
        self.order_dao = ProductionOrder()
        self.reports_dao = ReportsDAO()

        self.create_widgets()
        self.refresh_all()
        self.check_database_schema()
        self.create_menu()

#UI
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Soubor", menu=file_menu)
        file_menu.add_command(label="Odhlásit se", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Ukončit", command=self.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Nápověda", menu=help_menu)
        help_menu.add_command(label="O aplikaci", command=self.show_about)

    def logout(self):
        if messagebox.askyesno("Odhlášení", "Opravdu se chceš odhlásit?"):
            self.destroy()
            from UI.login import show_login
            logged_user = show_login()
            if logged_user:
                app = ProductionApp(logged_user)
                app.mainloop()

    def show_about(self):
        messagebox.showinfo(
            "O aplikaci",
            f"Evidence výroby\n"
            f"Verze 1.0\n\n"
            f"Přihlášený uživatel: {self.logged_user['username']}"
        )

#Tvorvba UI aplikace
    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.tab_orders = ttk.Frame(notebook)
        self.tab_machines = ttk.Frame(notebook)
        self.tab_products = ttk.Frame(notebook)
        self.tab_machine_mgmt = ttk.Frame(notebook)
        self.tab_reports = ttk.Frame(notebook)

        notebook.add(self.tab_orders, text="Zakázky")
        notebook.add(self.tab_machines, text="Běžící stroje")
        notebook.add(self.tab_products, text="Produkty")
        notebook.add(self.tab_machine_mgmt, text="Správa strojů")
        notebook.add(self.tab_reports, text="Reporty")

        self.create_orders_tab()
        self.create_machines_tab()
        self.create_products_tab()
        self.create_machine_mgmt_tab()
        self.create_reports_tab()

#Zakazky
    def create_orders_tab(self):
        create_frame = ttk.LabelFrame(self.tab_orders, text="Správa zakázek", padding=10)
        create_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(create_frame, text="+ Nová zakázka", command=self.add_order_window).pack(side="left")
        ttk.Button(create_frame, text="x Smazat zakázku", command=self.delete_order).pack(side="left", padx=5)


        control_frame = ttk.LabelFrame(self.tab_orders, text="Správa výroby", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(control_frame, text="Zakázka:").pack(side="left")

        self.order_combo = ttk.Combobox(control_frame, state="readonly", width=30)
        self.order_combo.pack(side="left", padx=5)

        ttk.Label(control_frame, text="Stroje:").pack(side="left", padx=(20, 0))

        self.machine_listbox = tk.Listbox(control_frame, selectmode=tk.MULTIPLE, height=5)
        self.machine_listbox.pack(side="left", padx=5)

        ttk.Button(control_frame, text="Spustit výrobu", command=self.start_production).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Ukončit výrobu", command=self.finish_production).pack(side="left")

        self.orders_tree = ttk.Treeview(
            self.tab_orders,
            columns=("id", "product", "qty", "status", "start", "end"),
            show="headings"
        )

        for col, txt, width in [
            ("id", "ID", 50),
            ("product", "Produkt", 200),
            ("qty", "Množství", 100),
            ("status", "Stav", 100),
            ("start", "Začátek", 150),
            ("end", "Konec", 150),
        ]:
            self.orders_tree.heading(col, text=txt)
            self.orders_tree.column(col, width=width)

        self.orders_tree.pack(fill="both", expand=True, padx=10, pady=10)

#Vuuziti stroju
    def create_machines_tab(self):
        self.machines_tree = ttk.Treeview(
            self.tab_machines,
            columns=("id", "name", "type", "order", "product", "status"),
            show="headings"
        )

        for col, txt, width in [
            ("id", "ID stroje", 80),
            ("name", "Název", 150),
            ("type", "Typ", 120),
            ("order", "Zakázka", 80),
            ("product", "Produkt", 200),
            ("status", "Stav zakázky", 120),
        ]:
            self.machines_tree.heading(col, text=txt)
            self.machines_tree.column(col, width=width)

        self.machines_tree.pack(fill="both", expand=True, padx=10, pady=10)

#Produkty
    def create_products_tab(self):
        top = ttk.Frame(self.tab_products)
        top.pack(fill="x", padx=10, pady=5)

        ttk.Button(top, text="+ Přidat produkt", command=self.add_product_window).pack(side="left")
        ttk.Button(top, text="x Smazat produkt", command=self.delete_product).pack(side="left", padx=5)

        self.products_tree = ttk.Treeview(
            self.tab_products,
            columns=("id", "name", "weight", "active"),
            show="headings"
        )

        for col, txt, width in [
            ("id", "ID", 50),
            ("name", "Název", 300),
            ("weight", "Hmotnost", 100),
            ("active", "Aktivní", 100),
        ]:
            self.products_tree.heading(col, text=txt)
            self.products_tree.column(col, width=width)

        self.products_tree.pack(fill="both", expand=True, padx=10, pady=10)

#Sprava stroju
    def create_machine_mgmt_tab(self):
        top = ttk.Frame(self.tab_machine_mgmt)
        top.pack(fill="x", padx=10, pady=5)

        ttk.Button(top, text="+ Přidat stroj", command=self.add_machine_window).pack(side="left")
        ttk.Button(top, text="x Smazat stroj", command=self.delete_machine).pack(side="left", padx=5)
        ttk.Button(top, text="Aktivovat stroj", command=self.activate_machine).pack(side="left", padx=5)
        ttk.Button(top, text="Deaktivovat stroj", command=self.deactivate_machine).pack(side="left")

        self.machine_mgmt_tree = ttk.Treeview(
            self.tab_machine_mgmt,
            columns=("id", "name", "type", "occupied", "active"),
            show="headings"
        )

        for col, txt, width in [
            ("id", "ID", 50),
            ("name", "Název", 220),
            ("type", "Typ stroje", 150),
            ("occupied", "Obsazeno", 100),
            ("active", "Aktivní", 100),
        ]:
            self.machine_mgmt_tree.heading(col, text=txt)
            self.machine_mgmt_tree.column(col, width=width)

        self.machine_mgmt_tree.pack(fill="both", expand=True, padx=10, pady=10)

#Sprava
    def create_reports_tab(self):
        reports_notebook = ttk.Notebook(self.tab_reports)
        reports_notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Prehled
        tab_overview = ttk.Frame(reports_notebook)
        reports_notebook.add(tab_overview, text="Celkový přehled")
        self.create_overview_report(tab_overview)

        # Tab 2: Vyrabi se neco?
        tab_production = ttk.Frame(reports_notebook)
        reports_notebook.add(tab_production, text="Výroba podle stavu")
        self.create_production_report(tab_production)

        # Tab 3: Vyuzití stroju
        tab_machines = ttk.Frame(reports_notebook)
        reports_notebook.add(tab_machines, text="Běžící stroje")
        self.create_machine_report(tab_machines)

        # Tab 4: Statistiky produktu
        tab_products = ttk.Frame(reports_notebook)
        reports_notebook.add(tab_products, text="Produkty")
        self.create_product_report(tab_products)

        # Tab 5: Vytízení stroju
        tab_workload = ttk.Frame(reports_notebook)
        reports_notebook.add(tab_workload, text="Vytížení strojů")
        self.create_workload_report(tab_workload)

    def create_overview_report(self, parent):
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(top_frame, text="Obnovit data", command=self.load_overview_report).pack(side="left")

        stats_frame = ttk.LabelFrame(parent, text="Klíčové metriky", padding=20)
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.overview_labels = {}
        labels = [
            ("total_orders", "Celkem zakázek:"),
            ("running_orders", "Běžící zakázky:"),
            ("completed_orders", "Dokončené zakázky:"),
            ("active_products", "Aktivních produktů:"),
            ("total_machines", "Celkem strojů:"),
            ("occupied_machines", "Obsazených strojů:"),
            ("total_quantity", "Celkové množství:"),
            ("total_weight", "Celková hmotnost (kg):"),
        ]

        for i, (key, label_text) in enumerate(labels):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(stats_frame, text=label_text, font=("Arial", 10)).grid(
                row=row, column=col, sticky="w", padx=10, pady=10
            )
            value_label = ttk.Label(stats_frame, text="0", font=("Arial", 12, "bold"))
            value_label.grid(row=row, column=col + 1, sticky="w", padx=10, pady=10)
            self.overview_labels[key] = value_label

    def create_production_report(self, parent):
        ttk.Button(parent, text="Obnovit data", command=self.load_production_report).pack(padx=10, pady=10,
                                                                                            anchor="w")

        self.production_tree = ttk.Treeview(
            parent,
            columns=("status", "count", "quantity", "products"),
            show="headings"
        )

        for col, txt, width in [
            ("status", "Stav: ", 150),
            ("count", "Počet zakázek: ", 120),
            ("quantity", "Celkové množství: ", 150),
            ("products", "Různé produkty: ", 150),
        ]:
            self.production_tree.heading(col, text=txt)
            self.production_tree.column(col, width=width)

        self.production_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_machine_report(self, parent):
        ttk.Button(parent, text="Obnovit data", command=self.load_machine_report).pack(padx=10, pady=10, anchor="w")

        self.machine_util_tree = ttk.Treeview(
            parent,
            columns=("type", "total", "occupied", "orders"),
            show="headings"
        )

        for col, txt, width in [
            ("type", "Typ stroje", 200),
            ("total", "Celkem strojů", 120),
            ("occupied", "Obsazeno", 120),
            ("orders", "Počet zakázek", 150),
        ]:
            self.machine_util_tree.heading(col, text=txt)
            self.machine_util_tree.column(col, width=width)

        self.machine_util_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_product_report(self, parent):
        ttk.Button(parent, text="Obnovit data", command=self.load_product_report).pack(padx=10, pady=10, anchor="w")

        self.product_stats_tree = ttk.Treeview(
            parent,
            columns=("product", "weight", "orders", "quantity", "total_weight", "avg"),
            show="headings"
        )

        for col, txt, width in [
            ("product", "Produkt", 200),
            ("weight", "Hmotnost (kg)", 100),
            ("orders", "Počet zakázek", 100),
            ("quantity", "Celk. množství", 100),
            ("total_weight", "Celk. hmotnost", 120),
            ("avg", "Prům. množství", 120),
        ]:
            self.product_stats_tree.heading(col, text=txt)
            self.product_stats_tree.column(col, width=width)

        self.product_stats_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def create_workload_report(self, parent):
        ttk.Button(parent, text="Obnovit data", command=self.load_workload_report).pack(padx=10, pady=10, anchor="w")

        self.workload_tree = ttk.Treeview(
            parent,
            columns=("machine", "type", "orders", "quantity", "occupied"),
            show="headings"
        )

        for col, txt, width in [
            ("machine", "Stroj", 200),
            ("type", "Typ", 150),
            ("orders", "Počet zakázek", 120),
            ("quantity", "Celk. množství", 120),
            ("occupied", "Obsazeno", 100),
        ]:
            self.workload_tree.heading(col, text=txt)
            self.workload_tree.column(col, width=width)

        self.workload_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Načítání dat pro reporty
    def load_overview_report(self):
        try:
            stats = self.reports_dao.get_overall_statistics()
            if stats:
                self.overview_labels["total_orders"].config(text=str(stats[0] or 0))
                self.overview_labels["running_orders"].config(text=str(stats[1] or 0))
                self.overview_labels["completed_orders"].config(text=str(stats[2] or 0))
                self.overview_labels["active_products"].config(text=str(stats[3] or 0))
                self.overview_labels["total_machines"].config(text=str(stats[4] or 0))
                self.overview_labels["occupied_machines"].config(text=str(stats[5] or 0))
                self.overview_labels["total_quantity"].config(text=str(stats[6] or 0))
                self.overview_labels["total_weight"].config(text=f"{stats[7]:.2f}" if stats[7] else "0.00")
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst přehled:\n{str(e)}")

    def load_production_report(self):
        try:
            self.production_tree.delete(*self.production_tree.get_children())
            data = self.reports_dao.get_production_summary()
            for row in data:
                self.production_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst report výroby:\n{str(e)}")

    def load_machine_report(self):
        try:
            self.machine_util_tree.delete(*self.machine_util_tree.get_children())
            data = self.reports_dao.get_machine_utilization()
            for row in data:
                self.machine_util_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst report strojů:\n{str(e)}")

    def load_product_report(self):
        try:
            self.product_stats_tree.delete(*self.product_stats_tree.get_children())
            data = self.reports_dao.get_product_statistics()
            for row in data:
                formatted_row = (
                    row[0], #Produkt
                    f"{row[1]:.2f}",  #Hmotnost
                    row[2],  #Počet zakázek
                    row[3],  #Celkové množství
                    f"{row[4]:.2f}" if row[4] else "0.00", #Celkem hmotnost
                    f"{row[5]:.2f}" if row[5] else "0.00" #Prumer mnozstiv
                )
                self.product_stats_tree.insert("", "end", values=formatted_row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst report produktů:\n{str(e)}")

    def load_workload_report(self):
        try:
            self.workload_tree.delete(*self.workload_tree.get_children())
            data = self.reports_dao.get_machine_workload()
            for row in data:
                formatted_row = (
                    row[0],  #Stroj
                    row[1],  #Typ
                    row[2] or 0,  #Pocet zakazek
                    row[3] or 0,  #Celkové mnozstvi
                    "Ano" if row[4] else "Ne"  #Obsazeno
                )
                self.workload_tree.insert("", "end", values=formatted_row)
        except Exception as e:
            messagebox.showerror("Chyba", f"Nepodařilo se načíst report vytížení:\n{str(e)}")

#Data loading
    def check_database_schema(self):
        try:
            self.machine_dao.cursor.execute(
                "SELECT TOP 1 IsActive FROM Machine"
            )
        except Exception:
            msg = (
                "UPOZORNĚNÍ: Databáze nemá sloupec IsActive v tabulce Machine.\n\n"
                "Funkce aktivace/deaktivace strojů nebude fungovat.\n\n"
                "Pro přidání sloupce spusť v SQL Server Management Studio:\n"
                "ALTER TABLE Machine ADD IsActive BIT NOT NULL DEFAULT 1;\n\n"
                "Aplikace bude fungovat i bez tohoto sloupce, ale s omezenou funkcionalitou."
            )
            messagebox.showwarning("Chybějící sloupec v databázi", msg)


    def refresh_all(self):
        self.load_orders()
        self.load_free_machines()
        self.load_machine_usage()
        self.load_products()
        self.load_all_machines()

    def load_orders(self):
        self.orders_tree.delete(*self.orders_tree.get_children())
        orders = self.order_view_dao.get_all()

        self.order_map = {}
        combo_values = []

        for o in orders:
            values = (
                o[0],  #OrderId
                o[1],  #ProductName
                o[2],  #Quantity
                o[3],  #Status
                o[4] if o[4] else "",
                o[5] if o[5] else ""
            )
            self.orders_tree.insert("", "end", values=values)
            label = f"{o[0]} - {o[1]} ({o[3]})"
            combo_values.append(label)
            self.order_map[label] = o[0]

        self.order_combo["values"] = combo_values

    def load_free_machines(self):
        self.machine_listbox.delete(0, tk.END)
        machines = self.machine_dao.get_free_machines()

        self.machine_map = {}
        for m in machines:
            label = f"{m[0]} - {m[1]} ({m[2]})"
            self.machine_listbox.insert(tk.END, label)
            self.machine_map[label] = m[0]

    def load_machine_usage(self):
        self.machines_tree.delete(*self.machines_tree.get_children())
        for m in self.machine_view_dao.get_all():
            self.machines_tree.insert("", "end", values=m)

    def load_products(self):
        self.products_tree.delete(*self.products_tree.get_children())
        for p in self.product_dao.get_all():
            self.products_tree.insert("", "end", values=(
                p[0],  #ID
                p[1],  #Nazev
                p[2],  #Hmotnost
                p[3]  #Aktivta
            ))

    def load_all_machines(self):
        self.machine_mgmt_tree.delete(*self.machine_mgmt_tree.get_children())
        machines = self.machine_dao.get_all()
        for m in machines:
            if len(m) >= 5:
                is_active = m[4]
            else:
                is_active = True

            item_id = self.machine_mgmt_tree.insert("", "end", values=(
                m[0],  #MachineId
                m[1],  #Name
                m[2],  #MachineType
                "Ano" if m[3] else "Ne",
                "Ano" if is_active else "Ne"
            ))

            if not is_active:
                self.machine_mgmt_tree.item(item_id, tags=('inactive',))

        self.machine_mgmt_tree.tag_configure('inactive', foreground='gray')

#Produkce
    def start_production(self):
        if not self.order_combo.get():
            messagebox.showerror("Chyba", "Vyber zakázku")
            return

        selected = self.machine_listbox.curselection()
        if not selected:
            messagebox.showerror("Chyba", "Vyber alespoň jeden stroj")
            return

        order_id = self.order_map[self.order_combo.get()]
        machine_ids = [self.machine_map[self.machine_listbox.get(i)] for i in selected]

        try:
            self.service_dao.start_production(order_id, machine_ids)
            messagebox.showinfo("OK", "Výroba spuštěna")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def finish_production(self):
        if not self.order_combo.get():
            messagebox.showerror("Chyba", "Vyber zakázku")
            return

        order_id = self.order_map[self.order_combo.get()]

        try:
            self.service_dao.finish_production(order_id)
            messagebox.showinfo("OK", "Výroba ukončena")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

#Zakazky
    def add_order_window(self):
        win = tk.Toplevel(self)
        win.title("Nová zakázka")
        win.geometry("350x200")

        ttk.Label(win, text="Produkt:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

        product_combo = ttk.Combobox(win, state="readonly", width=30)
        product_combo.grid(row=0, column=1, padx=5, pady=5)

        products = self.product_dao.get_all()
        product_map = {}
        product_values = []

        for p in products:
            label = f"{p[0]} - {p[1]}"
            product_values.append(label)
            product_map[label] = p[0]

        product_combo["values"] = product_values
        if product_values:
            product_combo.current(0)

        ttk.Label(win, text="Množství:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        quantity_entry = ttk.Entry(win, width=32)
        quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        def save():
            if not product_combo.get():
                messagebox.showerror("Chyba", "Vyber produkt")
                return

            try:
                quantity = int(quantity_entry.get())
                if quantity <= 0:
                    messagebox.showerror("Chyba", "Množství musí být kladné číslo")
                    return

                product_id = product_map[product_combo.get()]
                self.order_dao.insert(product_id, quantity)
                messagebox.showinfo("OK", "Zakázka vytvořena")
                win.destroy()
                self.refresh_all()
            except ValueError:
                messagebox.showerror("Chyba", "Množství musí být celé číslo")
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        button_frame = ttk.Frame(win)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Uložit", command=save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Zrušit", command=win.destroy).pack(side="left", padx=5)

#Mazani zakazky
    def delete_order(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber zakázku ke smazání")
            return

        order_data = self.orders_tree.item(selected[0])["values"]

        try:
            order_id = int(str(order_data[0]).strip())
        except (ValueError, IndexError) as e:
            messagebox.showerror("Chyba", f"Nepodařilo se získat ID zakázky: {e}")
            return

        order_status = str(order_data[3]) if len(order_data) > 3 else ""

        if order_status == "Running":
            messagebox.showerror("Chyba", "Nelze smazat běžící zakázku. Nejprve ji ukonči.")
            return

        if messagebox.askyesno("Potvrzení", f"Opravdu chceš smazat zakázku č. {order_id}?"):
            try:
                self.order_dao.delete(order_id)
                messagebox.showinfo("OK", "Zakázka smazána")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

#Pridani produktu
    def add_product_window(self):
        win = tk.Toplevel(self)
        win.title("Nový produkt")
        win.geometry("300x150")

        ttk.Label(win, text="Název:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name = ttk.Entry(win, width=25)
        name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(win, text="Hmotnost:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        weight = ttk.Entry(win, width=25)
        weight.grid(row=1, column=1, padx=5, pady=5)

        def save():
            try:
                if not name.get():
                    messagebox.showerror("Chyba", "Zadej název produktu")
                    return

                weight_val = float(weight.get())
                self.product_dao.insert(name.get(), weight_val)
                messagebox.showinfo("OK", "Produkt přidán")
                win.destroy()
                self.load_products()
            except ValueError:
                messagebox.showerror("Chyba", "Hmotnost musí být číslo")
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        button_frame = ttk.Frame(win)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Uložit", command=save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Zrušit", command=win.destroy).pack(side="left", padx=5)

# Mazani produktu
    def delete_product(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber produkt ke smazání")
            return

        product_id = int(self.products_tree.item(selected[0])["values"][0])

        if messagebox.askyesno("Potvrzení", "Opravdu chceš smazat tento produkt?"):
            try:
                self.product_dao.delete(product_id)
                messagebox.showinfo("OK", "Produkt smazán")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

#Pridani stroje
    def add_machine_window(self):
        win = tk.Toplevel(self)
        win.title("Nový stroj")
        win.geometry("350x200")

        ttk.Label(win, text="Název:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(win, width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(win, text="Typ stroje:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        type_combo = ttk.Combobox(win, state="readonly", width=28)
        type_combo.grid(row=1, column=1, padx=5, pady=5)

        machine_types = self.machine_dao.get_machine_types()
        type_map = {}
        type_values = []

        for mt in machine_types:
            label = f"{mt[0]} - {mt[1]}"
            type_values.append(label)
            type_map[label] = mt[0]

        type_combo["values"] = type_values
        if type_values:
            type_combo.current(0)

        def save():
            try:
                if not name_entry.get():
                    messagebox.showerror("Chyba", "Zadej název stroje")
                    return

                if not type_combo.get():
                    messagebox.showerror("Chyba", "Vyber typ stroje")
                    return

                machine_type_id = type_map[type_combo.get()]
                self.machine_dao.insert(name_entry.get(), machine_type_id)
                messagebox.showinfo("OK", "Stroj přidán")
                win.destroy()
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

        button_frame = ttk.Frame(win)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Uložit", command=save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Zrušit", command=win.destroy).pack(side="left", padx=5)

#Mazani stroje
    def delete_machine(self):
        selected = self.machine_mgmt_tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber stroj ke smazání")
            return

        machine_data = self.machine_mgmt_tree.item(selected[0])["values"]

        try:
            machine_id = int(str(machine_data[0]).strip())
        except (ValueError, IndexError) as e:
            messagebox.showerror("Chyba", f"Nepodařilo se získat ID stroje: {e}")
            return

        is_occupied = machine_data[3] == "Ano"

        if is_occupied:
            messagebox.showerror("Chyba", "Nelze smazat obsazený stroj. Nejprve ukonči výrobu.")
            return

        if messagebox.askyesno("Potvrzení", f"Opravdu chceš smazat stroj č. {machine_id}?"):
            try:
                self.machine_dao.delete(machine_id)
                messagebox.showinfo("OK", "Stroj smazán")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Chyba", str(e))

    def activate_machine(self):
        selected = self.machine_mgmt_tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber stroj k aktivaci")
            return

        machine_data = self.machine_mgmt_tree.item(selected[0])["values"]

        try:
            machine_id = int(str(machine_data[0]).strip())
        except (ValueError, IndexError) as e:
            messagebox.showerror("Chyba", f"Nepodařilo se získat ID stroje: {e}")
            return

        if len(machine_data) < 5:
            messagebox.showerror("Chyba",
                                 "Databáze nemá sloupec IsActive. Spusť SQL příkaz:\nALTER TABLE Machine ADD IsActive BIT NOT NULL DEFAULT 1;")
            return

        is_active = machine_data[4] == "Ano"

        if is_active:
            messagebox.showinfo("Info", "Tento stroj je již aktivní")
            return

        try:
            self.machine_dao.set_active(machine_id, True)
            messagebox.showinfo("OK", "Stroj aktivován")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

    def deactivate_machine(self):
        selected = self.machine_mgmt_tree.selection()
        if not selected:
            messagebox.showwarning("Upozornění", "Vyber stroj k deaktivaci")
            return

        machine_data = self.machine_mgmt_tree.item(selected[0])["values"]

        try:
            machine_id = int(str(machine_data[0]).strip())
        except (ValueError, IndexError) as e:
            messagebox.showerror("Chyba", f"Nepodařilo se získat ID stroje: {e}")
            return

        if len(machine_data) < 5:
            messagebox.showerror("Chyba", "Databáze nemá sloupec IsActive. Spusť SQL příkaz:\nALTER TABLE Machine ADD IsActive BIT NOT NULL DEFAULT 1;")
            return

        is_occupied = machine_data[3] == "Ano"
        is_active = machine_data[4] == "Ano"

        if not is_active:
            messagebox.showinfo("Info", "Tento stroj je již deaktivován")
            return

        # Kontrola, zda není stroj obsazený
        if is_occupied:
            messagebox.showerror("Chyba", "Nelze deaktivovat obsazený stroj. Nejprve ukonči výrobu.")
            return

        try:
            self.machine_dao.set_active(machine_id, False)
            messagebox.showinfo("OK", "Stroj deaktivován")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Chyba", str(e))

if __name__ == "__main__":
    from UI.login import show_login

    logged_user = show_login()

    if logged_user:
        app = ProductionApp(logged_user)
        app.mainloop()