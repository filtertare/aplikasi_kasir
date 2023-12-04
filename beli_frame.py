import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

from riwayat_frame import RiwayatPembelianFrame

class beliFrame(tk.Frame):
    def __init__(self, master, cursor_barang, conn_barang, cursor_riwayat, conn_riwayat):
        super().__init__(master)

        self.cursor_barang = cursor_barang
        self.barang_dipilih = []
        self.total_harga = 0
        self.conn_barang = conn_barang
        
        # data khusus riwayat
        self.cursor_riwayat = cursor_riwayat
        self.conn_riwayat = conn_riwayat
        
        self.riwayat_frame = RiwayatPembelianFrame(master, self.cursor_riwayat, self.conn_riwayat)
        

        self.label_judul = ttk.Label(self, text="DAFTAR BELANJA")
        self.label_judul.grid(row=0, column=1, pady=15)

        # form scan
        self.label_scan = ttk.Label(self, text="Scan Barcode:")
        self.label_scan.grid(row=1, column=0, pady=20)
        self.form_scan = ttk.Entry(self, width=50)
        self.form_scan.grid(row=1, column=1, padx=1, pady=5)

        # Memanggil fungsi cari_barang_by_barcode saat teks pada form_scan berubah
        self.form_scan.bind("<KeyRelease>", lambda event: self.cari_barang_by_barcode(self.form_scan.get()))

        # form pilih manual
        self.label_pilih_manual = ttk.Label(self, text="Pilih Manual:")
        self.label_pilih_manual.grid(row=2, column=0)

        # Entry untuk memasukkan teks pencarian
        self.entry_cari_barang = ttk.Entry(self, width=50)
        self.entry_cari_barang.grid(row=2, column=1, padx=5, pady=5)

        # Listbox untuk menampilkan hasil pencarian
        self.listbox_hasil_cari = Listbox(self, height=3, width=50)
        self.listbox_hasil_cari.grid(row=3, column=1, padx=5, pady=5)
        
        # Memanggil fungsi cari_barang saat teks pada Entry berubah
        self.entry_cari_barang.bind("<KeyRelease>", lambda event: self.cari_barang())

        # Mengaitkan fungsi pilih_barang dengan event klik pada Listbox
        self.listbox_hasil_cari.bind("<ButtonRelease-1>", self.pilih_barang)

        # tambahkan variabel untuk menyimpan barang yang dipilih dan total keseluruhan harga

        # tambahkan kolom untuk menampilkan tabel barang yang dipilih
        self.tree_beli = ttk.Treeview(self, columns=("Barcode", "Nama Barang", "Harga", "Jumlah", "Total Harga"), show="headings", height=10)
        self.tree_beli.heading("#1", text="Barcode")
        self.tree_beli.heading("#2", text="Nama Barang")
        self.tree_beli.heading("#3", text="Harga")
        self.tree_beli.heading("#4", text="Jumlah")
        self.tree_beli.heading("#5", text="Total Harga")
        self.tree_beli.grid(row=4, column=0, columnspan=6, pady=10)

        # label untuk menampilkan total keseluruhan harga
        self.label_total_harga = ttk.Label(self, text="Total Keseluruhan Harga: 0")
        self.label_total_harga.grid(row=5, column=5, pady=10)

        # # Mengaitkan fungsi pilih_barang dengan event klik pada Listbox
        self.listbox_hasil_cari.bind("<ButtonRelease-1>", self.pilih_barang)

        # Hapus barang di treeview
        self.tombol_hapus_barang = ttk.Button(self, text="Hapus", command=self.hapus_barang)
        self.tombol_hapus_barang.grid(row=5, column=0, pady=10, padx=5)
        
        self.label_dibayar = ttk.Label(self, text="Jumlah uang yang dibayar:")
        self.label_dibayar.grid(row=6, column=4, pady=5)
        
        self.entry_dibayar = ttk.Entry(self, width=30)
        self.entry_dibayar.insert(0, "1")
        self.entry_dibayar.grid(row=6, column=5)

        # Checkout barang di treeview
        self.tombol_checkout_barang = ttk.Button(self, text="CHECKOUT",command=self.checkout_barang, width=30)
        self.tombol_checkout_barang.grid(row=7, column=5, pady=10, padx=5)

    def cari_barang(self):
        # Mengambil teks pencarian
        teks_pencarian = self.entry_cari_barang.get().lower()

        # Menghapus semua item di Listbox hasil pencarian
        self.listbox_hasil_cari.delete(0, END)

        # Mengambil data barang dari database
        self.cursor_barang.execute("SELECT nama_barang FROM barang WHERE LOWER(nama_barang) LIKE ?", ('%' + teks_pencarian + '%',))
        hasil_pencarian = self.cursor_barang.fetchall()

        # Menambahkan hasil pencarian ke Listbox
        for barang in hasil_pencarian:
            self.listbox_hasil_cari.insert(END, barang[0])

    # Fungsi untuk menanggapi pemilihan barang dari Listbox hasil pencarian
    def pilih_barang(self, event):
        # Memastikan ada item yang dipilih sebelum mengambil nilai dari Listbox
        if self.listbox_hasil_cari.curselection():
            # Mengambil nama barang dari item yang dipilih di Listbox
            nama_barang_terpilih = self.listbox_hasil_cari.get(self.listbox_hasil_cari.curselection())

            # mengambil informasi barang dari database berdasarkan nama barang
            self.cursor_barang.execute("SELECT * FROM barang WHERE nama_barang=?", (nama_barang_terpilih,))
            data_barang = self.cursor_barang.fetchone()

            if data_barang:
                barcode = data_barang[1]
                nama_barang = data_barang[2]
                harga_barang = data_barang[3]

                # meminta pengguna untuk memasukkan jumlah barang yang dibeli
                jumlah_barang = simpledialog.askinteger("Jumlah Barang", f"Masukkan jumlah barang yang dibeli untuk {nama_barang}:", minvalue=1)

                if jumlah_barang is not None:
                    
                    found = False
                    for barang in self.barang_dipilih:
                        if barang["barcode"] == barcode:
                            barang["jumlah_barang"] += jumlah_barang
                            barang["total_harga_barang"] += harga_barang * jumlah_barang
                            found = True
                            break

                # Jika barang belum ada, tambahkan ke dalam list
                    if not found:
                        self.barang_dipilih.append({
                            "barcode": barcode,
                            "nama_barang": nama_barang,
                            "harga_barang": harga_barang,
                            "jumlah_barang": jumlah_barang,
                            "total_harga_barang": harga_barang * jumlah_barang
                        })

                    # Memperbarui tampilan tabel dan total keseluruhan harga
                    self.update_tabel()

    def update_tabel(self):
        # Menghapus semua baris yang ada di treeview
        for row in self.tree_beli.get_children():
            self.tree_beli.delete(row)

        # Menambahkan data barang yang dipilih ke treeview
        for barang in self.barang_dipilih:
            self.tree_beli.insert("", tk.END, values=(barang["barcode"], barang["nama_barang"], barang["harga_barang"], barang["jumlah_barang"], barang["total_harga_barang"]))

        # Menghitung total keseluruhan harga
        self.total_harga = sum(data_barang["total_harga_barang"] for data_barang in self.barang_dipilih)

        # Memperbarui label total keseluruhan harga
        self.label_total_harga.config(text=f"Total Keseluruhan Harga: {self.total_harga}")

    def cari_barang_by_barcode(self, barcode):
        
        # Mengecek apakah barcode sudah ada di database
        self.cursor_barang.execute("SELECT * FROM barang WHERE barcode=?", (barcode,))
        data_barang = self.cursor_barang.fetchone()

        if data_barang:
            # jika barcode ditemukan, tampilkan informasi barang dan minta jumlah barang yang dibeli
            nama_barang = data_barang[2]
            harga_barang = data_barang[3]

            # jumlah_barang = simpledialog.askinteger("Jumlah Barang", f"Masukkan jumlah barang yang dibeli untuk {nama_barang}:", minvalue=1)
            jumlah_barang = 1
                    
            found = False
            for barang in self.barang_dipilih:
                if barang["barcode"] == barcode:
                    barang["jumlah_barang"] += jumlah_barang
                    barang["total_harga_barang"] += harga_barang * jumlah_barang
                    found = True
                    break

            # Jika barang belum ada, tambahkan ke dalam list
            if not found:
                self.barang_dipilih.append({
                    "barcode": barcode,
                    "nama_barang": nama_barang,
                    "harga_barang": harga_barang,
                    "jumlah_barang": jumlah_barang,
                    "total_harga_barang": harga_barang * jumlah_barang
                })

            # Memperbarui tampilan tabel dan total keseluruhan harga
            self.update_tabel()

            self.form_scan.delete(0, END)

        
    def hapus_barang(self):
        selected_item = self.tree_beli.selection()
        if selected_item:
            # Mengambil barcode dari barang
            selected_index = self.tree_beli.index(selected_item)

            # membuat konfirmasi untuk pengguna
            konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah anda yakin ingin menghapus barang ini?")
            if konfirmasi:
                # menghapus data dari treeview
                del self.barang_dipilih[selected_index]

                self.update_tabel()
                
    def checkout_barang(self):
        # Memastikan ada barang yang dipilih sebelum checkout
        if not self.barang_dipilih:
            messagebox.showwarning("Peringatan", "Belum ada barang yang dipilih untuk checkout.")
            return
    
        try:
            # Mengambil jumlah uang yang dibayar dari entry
            uang_dibayar = float(self.entry_dibayar.get())

            # Menghitung kembalian
            kembalian = uang_dibayar - self.total_harga

            # Menampilkan hasil kembalian
            messagebox.showinfo("Kembalian", f"Kembalian: {kembalian: .2f}")

            # Mengurangi jumlah stock dan mengosongkan treeview
            self.kurangi_stock()
            
            # insert pembelian ke riwayat
            self.insert_to_riwayat_pembelian()
            
            self.barang_dipilih = []
            self.update_tabel()
            self.entry_dibayar.delete(0, END)
            self.entry_dibayar.insert(0, "1")
            
            self.riwayat_frame.load_purchase_history()
            
            

        except ValueError:
            messagebox.showerror("Error", "Masukkan jumlah uang yang valid.")

        # Membuat tombol untuk menghitung kembalian
    def insert_to_riwayat_pembelian(self):
        # Insert purchased items into riwayat_pembelian table
        waktu_checkout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for barang in self.barang_dipilih:
            barcode = barang["barcode"]
            nama_barang = barang["nama_barang"]
            jumlah_barang = barang["jumlah_barang"]
            harga_satuan = barang["harga_barang"]
            harga_total = barang["total_harga_barang"]

            self.cursor_riwayat.execute("INSERT INTO riwayat_pembelian VALUES (?, ?, ?, ?, ?, ?)",
                                (waktu_checkout, barcode, nama_barang, jumlah_barang, harga_satuan, harga_total))

        # Commit the changes to the database
        self.conn_riwayat.commit()

    def kurangi_stock(self):
        # Mengurangi jumlah stock di database berdasarkan barang yang dibeli
        for barang in self.barang_dipilih:
            barcode = barang["barcode"]
            jumlah_barang = barang["jumlah_barang"]

            # Mengambil jumlah stock saat ini
            self.cursor_barang.execute("SELECT stock_barang FROM barang WHERE barcode=?", (barcode,))
            stock_sekarang = self.cursor_barang.fetchone()[0]

            # Mengurangi jumlah stock
            stock_baru = max(0,stock_sekarang - jumlah_barang)

            # Update jumlah stock di database
            self.cursor_barang.execute("UPDATE barang SET stock_barang=? WHERE barcode=?", (stock_baru, barcode))

        # Commit perubahan ke database
        self.conn_barang.commit()