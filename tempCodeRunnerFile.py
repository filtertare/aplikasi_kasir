import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3

from nav_frame import navFrame
from beli_frame import beliFrame
from data_frame import dataFrame
from riwayat_frame import RiwayatPembelianFrame

class Aplikasi:
    def __init__(self, master):
        self.master = master
        self.master.title("TOKO ATMAJAYA")

        # Fungsi untuk beralih antara mode fullscreen dan mode jendela biasa
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.toggle_fullscreen)

        # Mengatur ukuran window dan menjalankan aplikasi
        self.master.geometry("800x600")

        # Inisialisasi koneksi SQlite
        self.conn_barang= sqlite3.connect("database_barang.db")
        self.cursor_barang = self.conn_barang.cursor()

        # membuat tabel jika belum ada
        self.cursor_barang.execute('''
            CREATE TABLE IF NOT EXISTS barang (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode INTEGER,
                nama_barang TEXT,
                harga_barang INTEGER,
                stock_barang INTEGER
            )
        ''')
        self.conn_barang.commit()
        
        # Inisialisasi koneksi SQlite untuk riwayat_pembelian.db
        self.conn_riwayat = sqlite3.connect("riwayat_pembelian.db")
        self.cursor_riwayat = self.conn_riwayat.cursor()

        # membuat tabel jika belum ada di riwayat_pembelian.db
        self.cursor_riwayat.execute('''
            CREATE TABLE IF NOT EXISTS riwayat_pembelian (
                waktu TEXT,
                barcode TEXT,
                nama_barang TEXT,
                jumlah INTEGER,
                harga_satuan REAL,
                harga_total REAL
            )
        ''')
        self.conn_riwayat.commit()

        # frame beli-------------------------------------------------------------------------------------------------------
        self.frame_beli = beliFrame(self.master, self.cursor_barang, self.conn_barang, self.cursor_riwayat, self.conn_riwayat)
        self.frame_beli.pack()

        # Frame Data-------------------------------------------------------------------------------------------------------
        self.frame_data = dataFrame(self.master, self.cursor_barang, self.conn_barang)
        self.frame_data.pack()
        self.frame_data.pack_forget()

        # frame Custom Data-------------------------------------------------------------------------------------------------------
        self.frame_history = RiwayatPembelianFrame(self.master, self.cursor_riwayat, self.conn_riwayat)
        self.frame_history.pack()
        self.frame_history.pack_forget()

        # Frame navigasi-------------------------------------------------------------------------------------------------------
        self.nav_frame = navFrame(self.master, self.frame_data, self.frame_history, self.frame_beli)
        self.nav_frame.pack(side="bottom")

        # Mengatur ukuran window sesuai dengan resolusi layar laptop
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        default_width = int(screen_width * 0.8)
        default_height = int(screen_height * 0.8)
        self.master.geometry(f"{default_width}x{default_height}+{int((screen_width - default_width) / 2)}+{int((screen_height - default_height) / 2)}")


    def toggle_fullscreen(self, event=None):
        state = not self.master.attributes('-fullscreen')
        self.master.attributes('-fullscreen', state)
        if state:
            self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        else:
            # Mengatur ukuran window sesuai dengan resolusi layar laptop saat keluar dari fullscreen
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            default_width = int(screen_width * 0.8)
            default_height = int(screen_height * 0.8)
            self.master.geometry(f"{default_width}x{default_height}+{int((screen_width - default_width) / 2)}+{int((screen_height - default_height) / 2)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikasi(root)
    root.mainloop()


