import sqlite3

class Database:
    def __init__(self):
        # Membuat koneksi ke database 'inventory.db' dan kursor
        self.conn = sqlite3.connect('db/db_stock_management.db')
        self.cursor = self.conn.cursor()
        # Memanggil metode untuk menginisialisasi database
        self.init_database()

    def init_database(self):
        # Mengeksekusi perintah SQL untuk membuat tabel 'data_barang' jika belum ada
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data_barang
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nama_barang TEXT NOT NULL,
                            jumlah_stok INTEGER NOT NULL,
                            harga_beli INTEGER NOT NULL)''')
        # Menyimpan perubahan ke dalam database
        self.conn.commit()

    def add_item(self, nama_barang, jumlah_stok, harga_beli):
        # Mengeksekusi perintah SQL untuk menambahkan item baru ke dalam tabel
        self.cursor.execute('INSERT INTO data_barang (nama_barang, jumlah_stok, harga_beli) VALUES (?, ?, ?)',
                            (nama_barang, jumlah_stok, harga_beli))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()

    def get_all_items(self):
        # Mengeksekusi perintah SQL untuk mengambil semua item dari tabel
        self.cursor.execute('SELECT * FROM data_barang')
        # Mengembalikan hasil eksekusi (semua item) sebagai daftar
        return self.cursor.fetchall()

    def update_item(self, item_id, edited_name, edited_quantity, edited_price):
        # Mengeksekusi perintah SQL untuk memperbarui item berdasarkan ID
        self.cursor.execute('UPDATE data_barang SET nama_barang=?, jumlah_stok=?, harga_beli=? WHERE id=?',
                            (edited_name, edited_quantity, edited_price, item_id))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()

    def delete_item(self, item_id):
        # Mengeksekusi perintah SQL untuk menghapus item berdasarkan ID
        self.cursor.execute('DELETE FROM data_barang WHERE id=?', (item_id,))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()
