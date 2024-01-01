import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
from ttkthemes import ThemedStyle 
import app_stock_management_database_modul as database_module

class StockManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Manajemen Stok Barang")
        self.root.iconbitmap('assets/favicon/logo_icon.ico')  # Ganti dengan path ke ikon Anda
        self.setup_styles()
        self.create_menu_bar()
        self.create_paned_window()
        self.init_database()  # Inisialisasi database dan membaca data awal
        self.update_stock_data()    
        self.edit_dialog = None  

    def setup_styles(self):
        # Menggunakan ttkthemes
        themed_style = ThemedStyle(self.root)
        themed_style.set_theme("clearlooks")  # Ganti dengan tema yang kamu inginkan dari ttkthemes
        
       # Menggunakan ttkbootstrap
        style = Style('superhero')  # Anda dapat memilih tema yang berbeda
        style.configure("TButton", padding=10, relief="flat", font=('Arial', 12))

    def create_menu_bar(self):
        # Membuat menu bar untuk aplikasi
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # menu_bar.add_command(label="Halaman Utama", command=self.create_home_page)

        # Menu Bar untuk Aplikasi Manajemen Stok Barang
        stock_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Stok", menu=stock_menu)
        stock_menu.add_command(label="Tambah Barang", command=self.show_add_item_page)
        stock_menu.add_command(label="Lihat Stok", command=self.show_view_stock_page)

        # Keluar dari aplikasi
        menu_bar.add_command(label="Exit", command=self.root.destroy)

    def create_paned_window(self):
        # Membuat PanedWindow sebagai dasar layout
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.create_main_frame()
        self.create_add_item_frame()
        self.create_view_stock_frame()
        self.create_home_page()  # Tambahkan halaman utama
        ttk.Sizegrip(self.root).grid(column=1, row=1, sticky=(tk.S, tk.E))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.update_idletasks()
        self.center_window()
        self.paned_window.grid_columnconfigure(0, weight=1)
        self.paned_window.grid_columnconfigure(1, weight=1)
        self.paned_window.grid_rowconfigure(0, weight=1)

    def create_main_frame(self):
        # Membuat frame utama aplikasi
        self.main_frame = ttk.Frame(self.paned_window, padding="10", style="TFrame")
        self.paned_window.add(self.main_frame)
        self.create_main_frame_content()

    def create_main_frame_content(self):
        # Membuat konten di dalam frame utama
        self.create_logo_canvas()
        self.create_labels_and_buttons()

    def create_logo_canvas(self):
        # Membuat canvas untuk menampilkan logo
        logo_path = "assets/img/logo.png"
        logo = Image.open(logo_path).resize((300, 300))
        self.logo_image = ImageTk.PhotoImage(logo)

        canvas_width, canvas_height = 300, 300
        canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height, bg='#333333')
        canvas.grid(row=0, column=0, columnspan=3, pady=10)
        image_position_x = (canvas_width - self.logo_image.width()) / 2
        image_position_y = (canvas_height - self.logo_image.height()) / 2
        canvas.create_image(image_position_x, image_position_y, anchor=tk.NW, image=self.logo_image)

    def create_labels_and_buttons(self):
        # Membuat label dan tombol di frame utama
        self.label_title = ttk.Label(self.main_frame, text="Manajemen Stok Barang", font=("Arial", 16),
                                    background='#333333', foreground='#FFFFFF')
        self.label_title.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(self.main_frame, text="Tambah Barang", command=self.show_add_item_page, style="TButton").grid(
            row=2, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Lihat Stok", command=self.show_view_stock_page, style="TButton").grid(
            row=3, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Fitur Baru", command=self.show_feature_page, style="TButton").grid(
            row=4, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Halaman Utama", command=self.show_home_page, style="TButton").grid(
            row=5, column=0, columnspan=3, pady=5) 

    def create_add_item_frame(self):
        # Membuat frame untuk menambahkan barang baru
        self.add_item_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.create_add_item_frame_content()

    def create_add_item_frame_content(self):
        # Membuat konten di dalam frame untuk menambahkan barang baru
        ttk.Label(self.add_item_frame, text="Nama Barang:").grid(row=0, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_name = ttk.Entry(self.add_item_frame)
        self.entry_item_name.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Jumlah:").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_quantity = ttk.Entry(self.add_item_frame)
        self.entry_item_quantity.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Harga:").grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_price = ttk.Entry(self.add_item_frame)
        self.entry_item_price.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Button(self.add_item_frame, text="Tambah Barang", command=self.add_item).grid(
            row=3, column=0, columnspan=2, pady=10)

    def create_view_stock_frame(self):
        # Membuat frame untuk melihat stok barang
        self.view_stock_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.create_view_stock_frame_content()

    def create_view_stock_frame_content(self):
        # Membuat konten di dalam frame untuk melihat stok barang
        columns = ("Nomer Urut", "Nama Barang", "Jumlah Barang", "Harga Barang")
        self.treeview_stock = ttk.Treeview(self.view_stock_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.treeview_stock.heading(col, text=col)
        self.treeview_stock.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Menambahkan binding untuk fungsi edit dan delete
        self.treeview_stock.bind("<Double-1>", lambda event: self.edit_item())
        ttk.Button(self.view_stock_frame, text="Delete", command=self.delete_item).grid(row=1, column=0, pady=5)

        # Menengahkan Treeview di tengah frame
        self.view_stock_frame.columnconfigure(0, weight=1)
        self.view_stock_frame.rowconfigure(0, weight=1)

        # Membuat konten di dalam frame untuk melihat stok barang
        columns = ("Nomer Urut", "Nama Barang", "Jumlah Barang", "Harga Barang")
        self.treeview_stock = ttk.Treeview(self.view_stock_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.treeview_stock.heading(col, text=col)
        self.treeview_stock.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))

            # Menambahkan binding untuk fungsi edit dan delete
        self.treeview_stock.bind("<Double-1>", lambda event: self.edit_item())
        ttk.Button(self.view_stock_frame, text="Delete", command=self.delete_item).grid(row=1, column=0, pady=5)

    def create_home_page(self):
        # Membuat halaman utama
        self.home_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.home_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Deskripsi Aplikasi
        ttk.Label(self.home_frame, text="Deskripsi Aplikasi", font=("Arial", 16), background='#333333',
                  foreground='#FFFFFF').grid(row=0, column=0, pady=10)
        ttk.Label(self.home_frame,
                  text="Aplikasi Manajemen Stok Barang ini memungkinkan Anda untuk "
                       "mengelola stok barang, menambahkan barang baru, dan melihat stok "
                       "barang yang sudah ada. Gunakan fitur-fitur yang disediakan untuk "
                       "mempermudah pengelolaan stok barang di toko atau bisnis Anda.",
                  background='#333333', foreground='#FFFFFF', wraplength=400, justify=tk.LEFT).grid(row=1, column=0, pady=10)

    def center_window(self):
        # Menengahkan jendela aplikasi di tengah layar
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        frame_width, frame_height = 800, 600
        x_position, y_position = (screen_width - frame_width) // 2, (screen_height - frame_height) // 2
        self.root.geometry(f"{frame_width}x{frame_height}+{x_position}+{y_position}")

    def init_database(self):
        # Inisialisasi kelas Database dari modul database_module
        self.database = database_module.Database()

    def show_add_item_page(self):
        # Menampilkan halaman tambah barang baru
        self.label_title.config(text="Tambah Barang")
        self.add_item_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.view_stock_frame.grid_forget()
        self.home_frame.grid_forget()

    def show_view_stock_page(self):
        # Menampilkan halaman melihat stok barang
        self.label_title.config(text="Lihat Stok")
        self.view_stock_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.add_item_frame.grid_forget()
        self.home_frame.grid_forget()
        self.update_stock_data()

    def show_feature_page(self):
        # Menampilkan halaman fitur baru (dapat diimplementasikan lebih lanjut)
        self.label_title.config(text="Fitur Baru")
        self.add_item_frame.grid_forget()
        self.view_stock_frame.grid_forget()
        self.home_frame.grid_forget()

    def show_home_page(self):
        # Menampilkan halaman utama
        self.label_title.config(text="Halaman Utama")
        self.home_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.add_item_frame.grid_forget()
        self.view_stock_frame.grid_forget()

    def add_item(self):
        # Menambahkan barang baru ke dalam database
        item_name, item_quantity, item_price = self.entry_item_name.get(), self.entry_item_quantity.get(), self.entry_item_price.get()
        self.database.add_item(item_name, item_quantity, item_price)
        print(f"Nama Barang: {item_name}\nJumlah: {item_quantity}\nHarga: {item_price}")
        
        # Menampilkan notifikasi berhasil
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")

        self.update_stock_data()

    def update_stock_data(self):
    # Memperbarui data stok yang ditampilkan di Treeview
        for item in self.treeview_stock.get_children():
            self.treeview_stock.delete(item)

        # Mendapatkan data dari database
        data_barang = self.database.get_all_items()

        # Menambahkan data ke Treeview dengan nomor urut sebagai ID
        for index, barang in enumerate(data_barang, start=1):
            self.treeview_stock.insert("", tk.END, text=index, values=(index, barang[1], barang[2], barang[3]))

    def destroy_edit_dialog(self):
        # Menghancurkan dialog edit jika sudah ada
        if self.edit_dialog:
            self.edit_dialog.destroy()

    def edit_item(self):
        # Menampilkan dialog edit untuk item yang terpilih
        self.destroy_edit_dialog()
        selected_item = self.treeview_stock.focus()
        if selected_item:
            # Menampilkan dialog edit
            self.edit_dialog = tk.Toplevel(self.root)
            self.edit_dialog.title("Edit Barang")
            self.edit_dialog.iconbitmap('assets/favicon/logo_icon.ico')  # Ganti dengan path ke ikon Anda

            # Mendapatkan nilai item terpilih
            item_values = self.treeview_stock.item(selected_item, 'values')

            # Menampilkan elemen-elemen yang dapat diubah
            ttk.Label(self.edit_dialog, text="Nama Barang:").grid(row=0, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_name = ttk.Entry(self.edit_dialog)
            entry_edit_name.insert(0, item_values[1])
            entry_edit_name.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Label(self.edit_dialog, text="Jumlah:").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_quantity = ttk.Entry(self.edit_dialog)
            entry_edit_quantity.insert(0, item_values[2])
            entry_edit_quantity.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Label(self.edit_dialog, text="Harga:").grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_price = ttk.Entry(self.edit_dialog)
            entry_edit_price.insert(0, item_values[3])
            entry_edit_price.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Button(self.edit_dialog, text="Simpan", command=lambda: self.save_edit(selected_item, entry_edit_name.get(), entry_edit_quantity.get(), entry_edit_price.get())).grid(row=3, column=0, columnspan=2, pady=10)
    
    def save_edit(self, selected_item, edited_name, edited_quantity, edited_price):
        # Metode untuk menyimpan perubahan pada item yang diedit
        if selected_item:
            # Memeriksa apakah item yang dipilih memiliki atribut 'text'
            if 'text' in self.treeview_stock.item(selected_item):
                item_id = self.treeview_stock.item(selected_item, 'text')
                if item_id:
                    self.database.update_item(item_id, edited_name, edited_quantity, edited_price)

                    # Update tampilan Treeview
                    self.update_stock_data()

                    # Notifikasi berhasil
                    messagebox.showinfo("Sukses", "Data berhasil diedit.")

                    # Menutup dialog edit
                    self.destroy_edit_dialog()
                else:
                    print("Error: Item ID not found.")

    def delete_item(self):
        # Metode untuk menghapus item yang dipilih
        selected_item = self.treeview_stock.focus()
        if selected_item:
            # Mendapatkan nilai ID dari item yang terpilih
            item_id = self.treeview_stock.item(selected_item, 'text')

            # Konfirmasi hapus
            confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus barang ini?")
            if confirmation:
                # Menghapus data di database
                self.database.delete_item(item_id)

                # Memperbarui tampilan Treeview
                self.update_stock_data()

                # Notifikasi berhasil
                messagebox.showinfo("Sukses", "Data berhasil dihapus.")