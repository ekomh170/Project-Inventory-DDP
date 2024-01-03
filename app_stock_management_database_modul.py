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
                            harga_beli INTEGER NOT NULL,
                            harga_jual INTEGER,
                            supplier TEXT)''')
        # Menyimpan perubahan ke dalam database
        self.conn.commit()

    def add_item(self, nama_barang, jumlah_stok, harga_beli, harga_jual=None, supplier=None):
        # Mengeksekusi perintah SQL untuk menambahkan item baru ke dalam tabel
        self.cursor.execute('INSERT INTO data_barang (nama_barang, jumlah_stok, harga_beli, harga_jual, supplier) VALUES (?, ?, ?, ?, ?)',
                            (nama_barang, jumlah_stok, harga_beli, harga_jual, supplier))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()

    def get_all_items(self):
        # Mengeksekusi perintah SQL untuk mengambil semua item dari tabel
        self.cursor.execute('SELECT * FROM data_barang')
        # Mengembalikan hasil eksekusi (semua item) sebagai daftar
        return self.cursor.fetchall()

    # def update_item(self, item_id, edited_name, edited_quantity, edited_price):
    #     # Mengeksekusi perintah SQL untuk memperbarui item berdasarkan ID
    #     self.cursor.execute('UPDATE data_barang SET nama_barang=?, jumlah_stok=?, harga_beli=? WHERE id=?',
    #                         (edited_name, edited_quantity, edited_price, item_id))
    #     # Menyimpan perubahan ke dalam database
    #     self.conn.commit()

    def update_item(self, item_id, edited_name, edited_quantity, edited_price, edited_sell_price=None, edited_supplier=None):
        # Mengeksekusi perintah SQL untuk memperbarui item berdasarkan ID
        self.cursor.execute('UPDATE data_barang SET nama_barang=?, jumlah_stok=?, harga_beli=?, harga_jual=?, supplier=? WHERE id=?',
                            (edited_name, edited_quantity, edited_price, edited_sell_price, edited_supplier, item_id))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()
        
    def delete_item(self, item_id):
        # Mengeksekusi perintah SQL untuk menghapus item berdasarkan ID
        self.cursor.execute('DELETE FROM data_barang WHERE id=?', (item_id,))
        # Menyimpan perubahan ke dalam database
        self.conn.commit()
        
    def truncate_table(self):
        # Mengeksekusi perintah SQL untuk menghapus semua data dari tabel
        self.cursor.execute('DELETE FROM data_barang')
        # Mereset nilai autoincrement pada kolom id
        self.cursor.execute('DELETE FROM sqlite_sequence WHERE name="data_barang"')
        # Menyimpan perubahan ke dalam database
        self.conn.commit()
