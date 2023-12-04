import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd

class RiwayatPembelianFrame(tk.Frame):
    def __init__(self, master, cursor, conn):
        super().__init__(master)

        self.conn = conn
        self.cursor = cursor
        

        self.label_judul = ttk.Label(self, text="RIWAYAT PEMBELIAN")
        self.label_judul.grid(row=0, column=1, pady=15)
        
        self.tombol_refresh = ttk.Button(self, text="Refresh", command=self.load_purchase_history)
        self.tombol_refresh.grid(row=1, column=0)
        
        # fitur sortir riwayat
        self.label_pilih_bulan = ttk.Label(self, text="Pilih Bulan & Tahun:")
        self.label_pilih_bulan.grid(row=1, column=16, padx=1)
        
        self.combobox_bulan = ttk.Combobox(self, values=("Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"))
        self.combobox_bulan.grid(row=1, column=17, padx=1)
        
        self.combobox_tahun = ttk.Combobox(self, values=[str(tahun) for tahun in range(2023, 2050)])
        self.combobox_tahun.grid(row=1, column=18, padx=1)
        self.combobox_tahun.set("2023")
        
        self.tombol_sortir = ttk.Button(self, text="Sort", command=self.sortir_riwayat)
        self.tombol_sortir.grid(row=1, column=19)

        # Add a Treeview to display purchase history
        self.tree_riwayat = ttk.Treeview(self, columns=("Waktu", "Barcode", "Nama Barang", "Jumlah", "Harga Satuan", "Harga Total"), show="headings", height=10)
        self.tree_riwayat.heading("#1", text="Waktu")
        self.tree_riwayat.heading("#2", text="Barcode")
        self.tree_riwayat.heading("#3", text="Nama Barang")
        self.tree_riwayat.heading("#4", text="Jumlah")
        self.tree_riwayat.heading("#5", text="Harga Satuan")
        self.tree_riwayat.heading("#6", text="Harga Total")
        self.tree_riwayat.grid(row=2, column=0, columnspan=20, pady=10)
        
        self.tombol_hapus_riwayat = ttk.Button(self, text="Hapus", command=self.hapus_riwayat)
        self.tombol_hapus_riwayat.grid(row=3, column=19, pady=10, padx=5)


        # Load purchase history data
        self.load_purchase_history()

        # Export button to export data to Excel
        self.tombol_export_excel = ttk.Button(self, text="Export to Excel", command=self.export_to_excel, width=30)
        self.tombol_export_excel.grid(row=3, column=0, pady=10)

    def load_purchase_history(self):
        # Clear existing rows in the Treeview
        for row in self.tree_riwayat.get_children():
            self.tree_riwayat.delete(row)

        # Retrieve purchase history data from the database
        self.cursor.execute("SELECT * FROM riwayat_pembelian")
        purchase_history = self.cursor.fetchall()

        # Populate the Treeview with purchase history data
        for purchase in purchase_history:
            self.tree_riwayat.insert("", tk.END, values=purchase)

    def export_to_excel(self):
        # Retrieve purchase history data from the database
        self.cursor.execute("SELECT * FROM riwayat_pembelian")
        purchase_history = self.cursor.fetchall()

        # Create a DataFrame from the purchase history data
        df = pd.DataFrame(purchase_history, columns=["Waktu", "Barcode", "Nama Barang", "Jumlah", "Harga Satuan", "Harga Total"])

        # Export DataFrame to Excel file
        excel_file_path = "riwayat_pembelian.xlsx"
        df.to_excel(excel_file_path, index=False)

        messagebox.showinfo("Export Success", f"Data has been exported to {excel_file_path}")
        
    def convert_month_name_to_number(self, month_name):
        # Dict untuk menonversi nama bulan menjadi angka
        month_dict = {
            'Januari': '01',
            'Februari': '02',
            'Maret': '03',
            'April': '04',
            'Mei': '05',
            'Juni': '06',
            'Juli': '07',
            'Agustus': '08',
            'September': '09',
            'Oktober': '10',
            'November': '11',
            'Desember': '12'
        }
        
        return month_dict.get(month_name, '01')
        
    def sortir_riwayat(self):
        selected_month = self.convert_month_name_to_number(self.combobox_bulan.get())
        selected_year = self.combobox_tahun.get()
        
        # Mengambil data riwayat dari database
        self.cursor.execute("SELECT * FROM riwayat_pembelian WHERE strftime('%m', waktu) = ? AND strftime('%Y', waktu) = ?", (selected_month, selected_year))
        data_pembelian = self.cursor.fetchall()
        
        # Menghapus semua baris di treeview
        for row in self.tree_riwayat.get_children():
            self.tree_riwayat.delete(row)
            
        # Menambahkan data pembelian ke treeview
        for pembelian in data_pembelian:
            self.tree_riwayat.insert("", tk.END, values=pembelian)
            
    def hapus_riwayat(self):
    # Memastikan ada riwayat yang dipilih sebelum menghapus
        if not self.tree_riwayat.selection():
            messagebox.showwarning("Peringatan", "Belum ada riwayat yang dipilih untuk dihapus.")
            return

        selected_item = self.tree_riwayat.selection()
        # Mengambil waktu_checkout dari riwayat yang dipilih
        waktu_checkout = self.tree_riwayat.item(selected_item, 'values')[0]

        # Membuat konfirmasi untuk pengguna
        konfirmasi = messagebox.askyesno("Konfirmasi", "Apakah anda yakin ingin menghapus riwayat ini?")
        if konfirmasi:
            # Menghapus data dari riwayat_pembelian
            self.cursor.execute("DELETE FROM riwayat_pembelian WHERE waktu=?", (waktu_checkout,))
            
            # Commit perubahan ke database
            self.conn.commit()

            # Memperbarui tampilan riwayat
            self.load_purchase_history()


