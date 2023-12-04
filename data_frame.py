import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class dataFrame(tk.Frame):
    def __init__(self,master, cursor, conn):
        super().__init__(master)

        self.conn = conn
        self.cursor = cursor

        self.label_data = ttk.Label(self, text="DATA BARANG")
        self.label_data.pack(pady=15)


        # membuat treeview untuk menampilkan tabel
        self.frame_trv = tk.Frame(self)
        self.frame_trv.pack()

        self.tombol_refresh = ttk.Button(self.frame_trv, text="Refresh", command=self.reset_pencarian)
        self.tombol_refresh.grid(row=0, column=0, pady=5)

        # Entry untuk memasukkan teks pencarian
        self.entry_cari = ttk.Entry(self.frame_trv, width=30)
        self.entry_cari.grid(row=0, column=17, padx=1, pady=5)

        # Tombol untuk memulai pencarian
        self.tombol_cari = ttk.Button(self.frame_trv, text="Cari", command=self.cari_data)
        self.tombol_cari.grid(row=0, column=18, padx=1, pady=5)

        # Tombol untuk reset hasil cari
        self.tombol_sort = ttk.Button(self.frame_trv, text="Sort", command=self.urut_stock)
        self.tombol_sort.grid(row=0, column=19, padx=1, pady=5)

        self.tree = ttk.Treeview(self.frame_trv, columns=("No","Barcode", "Nama Barang", "Harga Barang", "Stock Barang"), show="headings", height=20)
        self.tree.column("#1", anchor=E, stretch=NO, width=100)
        self.tree.heading("#1", text="No")
        self.tree.column("#2", anchor=E, stretch=NO)
        self.tree.heading("#2", text="Barcode")
        self.tree.column("#3", anchor=E, stretch=NO)
        self.tree.heading("#3", text="Nama Barang")
        self.tree.column("#4", anchor=E, stretch=NO, width=100)
        self.tree.heading("#4", text="Harga Barang")
        self.tree.column("#5", anchor=E, stretch=NO, width=100)
        self.tree.heading("#5", text="Stock Barang")
        self.tree.grid(row=1,columnspan=20)

        # Mengisi treeview dengan data dari database
        self.tampilkan_data()

        # tombol input data, hapus data, dan edit data
        self.frame_nav_data = tk.Frame(self)
        self.frame_nav_data.pack()

        self.tombol_input_data = ttk.Button(self.frame_trv, text="INPUT DATA", command=self.tampilkan_jendela_input)
        self.tombol_input_data.grid(row=2, column=0, padx=5, pady=20)
        
        self.tombol_hapus_data = ttk.Button(self.frame_trv, text="HAPUS DATA", command=self.hapus_data)
        self.tombol_hapus_data.grid(row=2, column=18, padx=1, pady=20)
        
        self.tombol_edit_data = ttk.Button(self.frame_trv, text="EDIT DATA", command=self.tampilkan_jendela_edit)
        self.tombol_edit_data.grid(row=2, column=19, pady=20)

    def tampilkan_data(self):
        # Menghapus semua baris yang ada di treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # mengambil data dari database dan menampilkannya di treeview
        self.cursor.execute("SELECT * FROM barang")
        data_barang = self.cursor.fetchall()

        # Menambah kolom "Nomor Urut"
        nomor_urut = 1

        for data in data_barang:
            self.tree.insert("", data[0], iid=data[0], values=(nomor_urut, data[1], data[2], data[3], data[4]))
            nomor_urut += 1

    def tampilkan_jendela_input(self):
        # fungsi untuk menampilkan jendela kecil untuk input data baru
        jendela_input = tk.Toplevel(self.master)
        jendela_input.title("Input Data Baru")

        # antarmuka pengguna untuk memasukkan data baru
        label_barcode = ttk.Label(jendela_input, text="Barcode:")
        label_barcode.grid(row=0, column=0, padx=5, pady=5)
        entry_barcode = ttk.Entry(jendela_input)
        entry_barcode.grid(row=0, column=1, padx=5,pady=5)

        label_nama_barang = ttk.Label(jendela_input, text="Nama Barang:")
        label_nama_barang.grid(row=1, column=0, padx=5, pady=5)
        entry_nama_barang = ttk.Entry(jendela_input)
        entry_nama_barang.grid(row=1, column=1, padx=5, pady=5)

        label_harga_barang = ttk.Label(jendela_input, text="Harga Barang:")
        label_harga_barang.grid(row=2, column=0, padx=5, pady=5)
        entry_harga_barang = ttk.Entry(jendela_input)
        entry_harga_barang.grid(row=2, column=1, padx=5, pady=5)

        label_stock_barang = ttk.Label(jendela_input, text="Stock Barang:")
        label_stock_barang.grid(row=3, column=0, padx=5, pady=5)
        entry_stock_barang = ttk.Entry(jendela_input)
        entry_stock_barang.grid(row=3, column=1, padx=5, pady=5)

        tombol_simpan = ttk.Button(jendela_input, text="Simpan", command=lambda: self.simpan_data(entry_barcode.get(), entry_nama_barang.get(), entry_harga_barang.get(), entry_stock_barang.get(), jendela_input))
        tombol_simpan.grid(row=4, column=0, columnspan=2, pady=10)

    # fungsi tombol simpan pada input data
    def simpan_data(self, barcode, nama_barang, harga_barang, stock_barang, jendela_input):
        # Pemeriksaan apakah barcode sudah ada di database
        self.cursor.execute("SELECT * FROM barang Where barcode=?", (barcode,))
        existing_data = self.cursor.fetchone()
        
        if existing_data:
            messagebox.showerror("Duplikasi Barcode", "Data sudah ada di database. Silahkan update pada menu edit.")
            jendela_input.destroy()
        else:
            # perintah SQL untuk menyimpan data ke database
            sql = "INSERT INTO barang (barcode, nama_barang, harga_barang, stock_barang) VALUES (?, ?, ?, ?)"
            values = (barcode, nama_barang, harga_barang, stock_barang)

            try:
                # Eksekusi perintah SQL
                self.cursor.execute(sql, values)
                self.conn.commit()

                # menampilkan kembali data setelah penyimpanan
                self.tampilkan_data()

                # menutup jendela input setelah berhasil menyimpan
                jendela_input.destroy()
            except Exception as e:
                # menampilkan pesan kesalahan jika terjadi
                messagebox.showerror("Error", f"Error: {e}")

    def hapus_data(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Mengambil Barcode dari data terpilih
            barcode_barang = self.tree.item(selected_item, "values")[1]

            # membuat konfirmasi untuk pengguna
            konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah anda yakin ingin menghapus data ini?")
            if konfirmasi:
                # menghapus data dari database
                self.cursor.execute("DELETE FROM barang WHERE barcode=?", (barcode_barang,))
                self.conn.commit()

                # menampilkan kembali data setelah penghapusan
                self.tampilkan_data()

    def tampilkan_jendela_edit(self):
    # fungsi untuk menampilkan jendela kecil untuk edit data
        selected_item = self.tree.selection()
        if selected_item:
            barcode = self.tree.item(selected_item, "values")[1]  # Mengambil nilai barcode dari data terpilih
            data_barang = self.cursor.execute("SELECT * FROM barang WHERE barcode=?", (barcode,)).fetchone()

            if data_barang:
                jendela_edit = tk.Toplevel(self.master)
                jendela_edit.title("Edit Data")

                # Antarmuka pengguna untuk mengedit data
                label_barcode = ttk.Label(jendela_edit, text="Barcode:")
                label_barcode.grid(row=0, column=0, padx=5, pady=5)
                entry_barcode = ttk.Entry(jendela_edit)
                entry_barcode.insert(0, data_barang[1])
                entry_barcode.grid(row=0, column=1, padx=5, pady=5)

                label_nama_barang = ttk.Label(jendela_edit, text="Nama Barang:")
                label_nama_barang.grid(row=1, column=0, padx=5, pady=5)
                entry_nama_barang = ttk.Entry(jendela_edit)
                entry_nama_barang.insert(0, data_barang[2])
                entry_nama_barang.grid(row=1, column=1, padx=5, pady=5)

                label_harga_barang = ttk.Label(jendela_edit, text="Harga Barang:")
                label_harga_barang.grid(row=2, column=0, padx=5, pady=5)
                entry_harga_barang = ttk.Entry(jendela_edit)
                entry_harga_barang.insert(0, data_barang[3])
                entry_harga_barang.grid(row=2, column=1, padx=5, pady=5)

                label_stock_barang = ttk.Label(jendela_edit, text="Stock Barang:")
                label_stock_barang.grid(row=3, column=0, padx=5, pady=5)
                entry_stock_barang = ttk.Entry(jendela_edit)
                entry_stock_barang.insert(0, data_barang[4])
                entry_stock_barang.grid(row=3, column=1, padx=5, pady=5)

                tombol_simpan = ttk.Button(jendela_edit, text="Simpan", command=lambda: self.simpan_edit_data(data_barang[0], entry_barcode.get(), entry_nama_barang.get(), entry_harga_barang.get(), entry_stock_barang.get(), jendela_edit))
                tombol_simpan.grid(row=4, column=0, columnspan=2, pady=10)
            else:
                messagebox.showwarning("Data tidak ditemukan", f"Tidak ada data dengan barcode {barcode}")
    
    def simpan_edit_data(self, id_barang, barcode, nama_barang, harga_barang, stock_barang, jendela_edit):
        # perintah SQL untuk menyimpan perubahan pada data
        sql = "UPDATE barang SET barcode=?, nama_barang=?, harga_barang=?, stock_barang=? WHERE id=?"
        values = (barcode, nama_barang, harga_barang, stock_barang, id_barang)

        try:
            # Eksekusi perintah SQL
            self.cursor.execute(sql, values)
            self.conn.commit()

            # menampilkan kembali data setelah penyimpanan
            self.tampilkan_data()

            # menutup jendela edit setelah berhasil menyimpan
            jendela_edit.destroy()
        except Exception as e:
            # menampilkan pesan kesalahan jika terjadi
            messagebox.showerror("Error", f"Error: {e}")

    def cari_data(self):
        # Mengambil teks pencarian
        teks_pencarian = self.entry_cari.get().lower()

        # Menghapus semua item di treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Mengambil data barang dari database yang sesuai dengan pencarian
        self.cursor.execute("SELECT * FROM barang WHERE LOWER(nama_barang) LIKE ? OR barcode=?", ('%' + teks_pencarian + '%', teks_pencarian))
        data_barang = self.cursor.fetchall()

        # Menambahkan hasil pencarian ke treeview
        nomor_urut = 1
        for data in data_barang:
            self.tree.insert("", data[0], iid=data[0], values=(nomor_urut, data[1], data[2], data[3], data[4]))
            nomor_urut += 1

    def reset_pencarian(self):
        self.entry_cari.delete(0, END)
        self.tampilkan_data()

    def urut_stock(self):
        # Menghapus semua item di treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Mengambil data barang dari database dan mengurutkannya berdasarkan stock barang terkecil
        self.cursor.execute("SELECT * FROM barang ORDER BY stock_barang ASC")
        data_barang = self.cursor.fetchall()

        # Menambahkan hasil pengurutan ke treeview
        nomor_urut = 1
        for data in data_barang:
            self.tree.insert("", data[0], iid=data[0], values=(nomor_urut, data[1], data[2], data[3], data[4]))
            nomor_urut += 1