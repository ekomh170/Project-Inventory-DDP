from app_stock_management_database_modul import Database

class Dummy:
    def __init__(self):
        # Membuat objek Database
        self.db = Database()

    def insert_dummy_data(self):
        # Menambahkan data dummy ke dalam tabel
        dummy_data = [
            ('Laptop', 5, 1200, 1500, 'TechMasters Inc.'),
            ('Printer', 10, 300, 400, 'OfficeSolutions Ltd.'),
            ('Mouse', 20, 25, 30, 'ElectroGadgets Co.'),
            ('Keyboard', 15, 50, 60, 'Accessories Unlimited')
        ]

        for data in dummy_data:
            # Cek apakah data dengan nama barang yang sama sudah ada
            existing_data = self.db.cursor.execute(
                'SELECT * FROM data_barang WHERE nama_barang = ?', (data[0],)
            ).fetchone()

            if not existing_data:
                # Data belum ada, lakukan penyisipan ke dalam tabel
                self.db.cursor.execute(
                    'INSERT INTO data_barang (nama_barang, jumlah_stok, harga_beli, harga_jual, supplier) VALUES (?, ?, ?, ?, ?)',
                    data
                )

        # Menyimpan perubahan ke dalam database
        self.db.conn.commit()

        print("Data dummy berhasil ditambahkan.")