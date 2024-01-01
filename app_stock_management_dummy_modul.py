from app_stock_management_database_modul import Database 

def insert_dummy_data():
    # Membuat objek Database
    db = Database()

    # Menambahkan data dummy ke dalam tabel
    dummy_data = [
        ('Laptop', 5, 1200),
        ('Printer', 10, 300),
        ('Mouse', 20, 25),
        ('Keyboard', 15, 50)
    ]
    db.cursor.executemany('INSERT INTO data_barang (nama_barang, jumlah_stok, harga_beli) VALUES (?, ?, ?)', dummy_data)

    # Menyimpan perubahan ke dalam database
    db.conn.commit()

    print("Data dummy berhasil ditambahkan.")

if __name__ == "__main__":
    insert_dummy_data()
