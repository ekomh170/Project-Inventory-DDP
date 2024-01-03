import tkinter as tk
import os
import tkinter.font as tkFont

from datetime import datetime
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
from ttkthemes import ThemedStyle 

# Komponen Buat PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# Komponen Buat PDF

import app_stock_management_database_modul as database_module
import app_stock_management_dummy_modul as dummy_module

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
        
        # Menu Bar untuk navigasi cepat
        navigasi_cepat = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Navigasi Cepat", menu=navigasi_cepat)
        navigasi_cepat.add_command(label="Halaman Utama", command=self.show_home_page)
        navigasi_cepat.add_command(label="Tambah Barang", command=self.show_add_item_page)
        navigasi_cepat.add_command(label="Lihat Stok", command=self.show_view_stock_page)

        # Menu Bar untuk ekspor PDF
        menu_bar.add_command(label="Ekspor PDF", command=self.create_pdf)
        
        # Menu Bar untuk fitur tambahan
        fitur_tambahan = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Fitur Tambahan", menu=fitur_tambahan)
        fitur_tambahan.add_command(label="Reset Database", command=self.reset_item)
        fitur_tambahan.add_command(label="Tambah Data Dummy", command=self.dummy_item)

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
        self.label_title.grid(row=1, column=0, columnspan=3, pady=20)

        ttk.Button(self.main_frame, text="Halaman Utama", command=self.show_home_page, style="TButton").grid(
            row=2, column=0, columnspan=3, pady=5)

        ttk.Button(self.main_frame, text="Tambah Barang", command=self.show_add_item_page, style="TButton").grid(
            row=3, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Lihat Stok", command=self.show_view_stock_page, style="TButton").grid(
            row=4, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Ekspor PDF", command=self.create_pdf, style="TButton").grid(
            row=5, column=0, columnspan=3, pady=5) 
        
        ttk.Button(self.main_frame, text="Reset Database", command=self.reset_item, style="TButton").grid(
            row=6, column=0, columnspan=3, pady=5) 
        ttk.Button(self.main_frame, text="Tambah Data Dummy", command=self.dummy_item, style="TButton").grid(
            row=7, column=0, columnspan=3, pady=5)
        
    def create_add_item_frame(self):
        # Membuat frame untuk menambahkan barang baru
        self.add_item_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.create_add_item_frame_content()

    def create_view_stock_frame(self):
        # Membuat frame untuk melihat stok barang
        self.view_stock_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.create_view_stock_frame_content()

    def create_view_stock_frame_content(self):
            # Membuat frame untuk melihat stok barang
        self.view_stock_frame = ttk.Frame(self.paned_window, style="TFrame")
        self.view_stock_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Membuat Treeview dengan style "Treeview.columns" agar dapat meresize kolom
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 10))

        columns = ("Nomer Urut", "Nama Barang", "Jumlah Barang", "Harga Beli", "Harga Jual", "Supplier")
        self.treeview_stock = ttk.Treeview(self.view_stock_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            self.treeview_stock.heading(col, text=col)

        self.treeview_stock.grid(row=0, column=0, pady=5, padx=5, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Menambahkan binding untuk fungsi edit dan delete
        self.treeview_stock.bind("<Double-1>", lambda event: self.edit_item())
        ttk.Button(self.view_stock_frame, text="Delete", command=self.delete_item).grid(row=1, column=0, pady=5)

        # Konfigurasi untuk membuat Treeview responsive
        self.view_stock_frame.columnconfigure(0, weight=1)
        self.view_stock_frame.rowconfigure(0, weight=1)

        for col in columns:
            self.treeview_stock.column(col, anchor="center", width=tkFont.Font().measure(col))
            self.treeview_stock.column("#0", stretch=tk.NO)

        # Membuat scrollbar untuk Treeview
        scrollbar = ttk.Scrollbar(self.view_stock_frame, orient="vertical", command=self.treeview_stock.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.treeview_stock.configure(yscrollcommand=scrollbar.set)

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

        # List Anggota Kelompok
        ttk.Label(self.home_frame, text="Anggota Kelompok:", font=("Arial", 14), background='#333333',
                foreground='#FFFFFF').grid(row=2, column=0, pady=10)

        # Nama-nama anggota kelompok
        anggota_kelompok = ["Ketua Kelompok : Eko Muchamad Haryono", "Nama Anggota : Najwa Nur Salimah", "Nama Anggota : Nurhayati", "Nama Anggota : Muhammad Sayyid Fadil"]  # Ganti dengan nama anggota kelompok Anda

        # Menambahkan label untuk setiap anggota kelompok
        for index, anggota in enumerate(anggota_kelompok, start=3):
            ttk.Label(self.home_frame, text=f"{index-2}. {anggota}", font=("Arial", 12), background='#333333',
                    foreground='#FFFFFF').grid(row=index, column=0, pady=5)

    def center_window(self):
        # Menengahkan jendela aplikasi di tengah layar
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        frame_width, frame_height = 800, 600
        x_position, y_position = (screen_width - frame_width) // 2, (screen_height - frame_height) // 2
        self.root.geometry(f"{frame_width}x{frame_height}+{x_position}+{y_position}")

    def init_database(self):
        # Inisialisasi kelas Database dari modul database_module
        self.database = database_module.Database()
        self.dbdummy = dummy_module.Dummy()

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
        
    def show_home_page(self):
        # Menampilkan halaman utama
        self.label_title.config(text="Halaman Utama")
        self.home_frame.grid(row=0, column=1, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.add_item_frame.grid_forget()
        self.view_stock_frame.grid_forget()
        
    def create_add_item_frame_content(self):
        # Membuat konten di dalam frame untuk menambahkan barang baru
        ttk.Label(self.add_item_frame, text="Nama Barang:").grid(row=0, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_name = ttk.Entry(self.add_item_frame)
        self.entry_item_name.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Stock Barang:").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_quantity = ttk.Entry(self.add_item_frame)
        self.entry_item_quantity.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Harga Beli:").grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_price = ttk.Entry(self.add_item_frame)
        self.entry_item_price.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Harga Jual:").grid(row=3, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_harga_jual = ttk.Entry(self.add_item_frame)
        self.entry_item_harga_jual.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Label(self.add_item_frame, text="Supplier:").grid(row=4, column=0, pady=5, padx=10, sticky=tk.W)
        self.entry_item_supplier = ttk.Entry(self.add_item_frame)
        self.entry_item_supplier.grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)

        ttk.Button(self.add_item_frame, text="Tambah Barang", command=self.add_item).grid(
            row=5, column=0, columnspan=2, pady=10) 

    def add_item(self):
        # Menambahkan barang baru ke dalam database
        item_name, item_quantity, item_price, harga_jual, supplier = self.entry_item_name.get(), self.entry_item_quantity.get(), self.entry_item_price.get(), self.entry_item_harga_jual.get(), self.entry_item_supplier.get()
        self.database.add_item(item_name, item_quantity, item_price, harga_jual, supplier)
        print(f"Nama Barang: {item_name}\nJumlah: {item_quantity}\nHarga: {item_price}\nHarga Jual: {harga_jual}\nSupplier: {supplier}")
        
        # Menampilkan notifikasi berhasil
        messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")

        self.update_stock_data()

    def update_stock_data(self):
    # Memperbarui data stok yang ditampilkan di Treeview
        for item in self.treeview_stock.get_children():
            self.treeview_stock.delete(item)

        # Mendapatkan data dari database
        data_barang = self.database.get_all_items()

        # Menambahkan data ke Treeview dengan item_id sebagai ID
        for item_id, barang in enumerate(data_barang, start=1):
            
            # Masukkan data ke dalam Treeview tanpa menampilkan barang[0] secara langsung
            self.treeview_stock.insert("", tk.END, text=item_id, values=(item_id, barang[1], barang[2], barang[3], barang[4], barang[5]))

            # Dapatkan ID item Treeview yang baru saja ditambahkan
            item_id_treeview = self.treeview_stock.get_children()[-1]

            # Atur nilai barang[0] sebagai tag pada item Treeview
            self.treeview_stock.item(item_id_treeview, tags=(barang[0],))
            
            # Atur lebar dan anchor untuk semua kolom
            for col_index in range(len(data_barang[0])):
                self.treeview_stock.column(f"#{col_index}", anchor="center")

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

            ttk.Label(self.edit_dialog, text="Stock Barang:").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_quantity = ttk.Entry(self.edit_dialog)
            entry_edit_quantity.insert(0, item_values[2])
            entry_edit_quantity.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Label(self.edit_dialog, text="Harga Beli:").grid(row=2, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_price = ttk.Entry(self.edit_dialog)
            entry_edit_price.insert(0, item_values[3])
            entry_edit_price.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Label(self.edit_dialog, text="Harga Jual:").grid(row=3, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_harga_jual = ttk.Entry(self.edit_dialog)
            entry_edit_harga_jual.insert(0, item_values[4])  # Ganti indeks ke-4
            entry_edit_harga_jual.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)

            ttk.Label(self.edit_dialog, text="Supplier:").grid(row=4, column=0, pady=5, padx=10, sticky=tk.W)
            entry_edit_supplier = ttk.Entry(self.edit_dialog)
            entry_edit_supplier.insert(0, item_values[5])  # Ganti indeks ke-5
            entry_edit_supplier.grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)

            # Memperbaiki pemanggilan fungsi dan menambahkan parameter yang diperlukan
            ttk.Button(self.edit_dialog, text="Simpan", command=lambda: self.save_edit(selected_item, entry_edit_name.get(), entry_edit_quantity.get(), entry_edit_price.get(), entry_edit_harga_jual.get(), entry_edit_supplier.get())).grid(row=5, column=0, columnspan=2, pady=10)

    def save_edit(self, selected_item, edited_name, edited_quantity, edited_price, edited_harga_jual, edited_supplier):
        # Metode untuk menyimpan perubahan pada item yang diedit
        if selected_item:
            # Memeriksa apakah item yang dipilih memiliki atribut 'text'
            # Dapatkan ID dari item yang terpilih di Treeview
            item_id_treeview = selected_item

            # Dapatkan nilai barang[0] dari tag pada item Treeview
            item_id = self.treeview_stock.item(item_id_treeview, "tags")[0]
            
            if item_id:
                self.database.update_item(item_id, edited_name, edited_quantity, edited_price, edited_harga_jual, edited_supplier)

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
            try:
                # Dapatkan ID dari item yang terpilih di Treeview
                item_id_treeview = selected_item

                # Dapatkan nilai barang[0] dari tag pada item Treeview
                item_id = self.treeview_stock.item(item_id_treeview, "tags")[0]

                # Konfirmasi hapus
                confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus barang ini?")
                
                if confirmation:
                    # Menghapus data di database
                    self.database.delete_item(item_id)

                    # Memperbarui tampilan Treeview
                    self.update_stock_data()

                    # Notifikasi berhasil
                    messagebox.showinfo("Sukses", "Data berhasil dihapus.")
                    print(f"Data dengan ID {item_id} berhasil dihapus.")

            except Exception as e:
                # Tangani kesalahan (misalnya, jika ID tidak ditemukan)
                messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
                print(f"Terjadi kesalahan: {str(e)}")
        else:
            # Jika tidak ada item yang dipilih
            messagebox.showwarning("Peringatan", "Pilih item terlebih dahulu untuk dihapus.")
            
    def reset_item(self):
        # Menampilkan konfirmasi kepada pengguna
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mereset data? Semua data akan dihapus.")
        
        if confirmation:
            # Jika pengguna mengonfirmasi, panggil fungsi truncate_table
            self.database.truncate_table()

            # Memperbarui tampilan Treeview
            self.update_stock_data()

            messagebox.showinfo("Sukses", "Data di Penyimpanan Database Berhasil di Reset.")
        else:
            messagebox.showinfo("Sukses", "Perintah Reset Database Dibatalkan")
            
    def dummy_item(self):
        # Membuat Data Secara Otomatis
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mengisi data secara otomatis?")
        
        if confirmation:
            # Jika pengguna mengonfirmasi, panggil fungsi insert_dummy_data
            self.dbdummy.insert_dummy_data()

            # Memperbarui tampilan Treeview
            self.update_stock_data()

            messagebox.showinfo("Sukses", "Penambahan data otomatis berhasil di tambahkan.")
        else:
            messagebox.showinfo("Sukses", "Penambahan data otomatis dibatalkan.")
            
    # Fungsi untuk membuat dan menyimpan file PDF
    def create_pdf(self):
        # Mendapatkan data stok barang dari database
        data_barang = self.database.get_all_items()

        # Membuat objek PDF dengan menentukan nama file dan ukuran halaman
        current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_filename = f"assets/export/Stok_Management_Barang_{current_date}.pdf"
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # List untuk menyimpan data tabel
        table_data = [["Nomer Urut", "Nama Barang", "Jumlah Barang", "Harga Barang", "Harga Jual", "Supplier"]]

        # Menambahkan baris tabel untuk setiap barang
        for row, barang in enumerate(data_barang, start=1):
            table_data.append([row, barang[1], barang[2], barang[3], barang[4], barang[5]])

        # Membuat objek tabel
        table = Table(table_data)

        # Mengatur gaya tabel
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)

        # Membuat objek Story untuk menambahkan elemen ke PDF
        story = []
        story.append(table)

        # Menyimpan file PDF
        pdf.build(story)

        # Menampilkan messagebox yang memberi tahu pengguna bahwa ekspor PDF berhasil
        messagebox.showinfo("Export PDF", f"Data stok barang telah diekspor ke {pdf_filename}.")

        # Menampilkan file PDF di browser
        self.open_pdf_in_browser(pdf_filename)

    # Fungsi untuk membuka file PDF di browser
    def open_pdf_in_browser(self, pdf_filename):
        try:
            os.system(f'start {pdf_filename}')  # Membuka file PDF di program default
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")