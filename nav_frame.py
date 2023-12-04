import tkinter as tk
from tkinter import *
from tkinter import ttk


class navFrame(tk.Frame):
    def __init__(self, master, frame_data, frame_history, frame_beli):
        super().__init__(master)
        # Frame navigasi-------------------------------------------------------------------------------------------------------
        self.frame_data = frame_data
        self.frame_beli = frame_beli
        self.frame_history = frame_history

        self.tombol_data = ttk.Button(self, text="Database", command=self.tampilkan_data_frame)
        self.tombol_data.grid(row=0, column=0, pady=20, padx=5)

        self.tombol_beli = ttk.Button(self, text="Beli", command=self.tampilkan_beli_frame)
        self.tombol_beli.grid(row=0, column=1, pady=20, padx=5)

        self.tombol_custom = ttk.Button(self, text="History", command=self.tampilkan_custom_frame)
        self.tombol_custom.grid(row=0, column=2, pady=20, padx=5 )

    def tampilkan_beli_frame(self):
        self.frame_data.pack_forget()
        self.frame_history.pack_forget()
        self.frame_beli.pack()

    def tampilkan_data_frame(self):
        self.frame_beli.pack_forget()
        self.frame_history.pack_forget()
        self.frame_data.pack()

    def tampilkan_custom_frame(self):
        self.frame_beli.pack_forget()
        self.frame_data.pack_forget()
        self.frame_history.pack()