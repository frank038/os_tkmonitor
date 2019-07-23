#!/usr/bin/env python3

"""
intel gpu module
"""

import tkinter as tk
import tkinter.ttk as ttk
import os
import sys
import shutil
import subprocess


class FNV(ttk.Frame):
    def __init__(self, master, root, frg_color):
        super().__init__(master)
        self.master = master
        self.root = root
        #
        self.pack()
        
        # blank line
        ttk.Label(self, text=" ").grid(column=0, row=0)
        
        # logo
        self.nv_logo = tk.PhotoImage(file="IntelLogo.png")
        self.lab_logo = ttk.Label(self, text="logo", image=self.nv_logo)
        self.lab_logo.grid(column=0, row=1, sticky="NW", rowspan=8)
        
        ## gpu name
        tgpu_name = ""
        gpu_name = ttk.Label(self, text="Product Name  ", foreground=frg_color).grid(column=1, row=2, sticky="NE")
        gpu_name2 = ttk.Label(self, text=tgpu_name).grid(column=2, row=2, sticky="NW")
        ## driver version
        gpu_driver_version = ""
        gpu_drv_ver = ttk.Label(self, text="Driver Version  ", foreground=frg_color).grid(column=1, row=3, sticky="NE")
        gpu_drv_ver2 = ttk.Label(self, text=gpu_driver_version).grid(column=2, row=3, sticky="NW")
        ## total memory
        gpu_totmem = ""
        gpu_tot_mem = ttk.Label(self, text="Total Memory  ", foreground=frg_color).grid(column=1, row=4, sticky="NE")
        gpu_tot_mem2 = ttk.Label(self, text=gpu_totmem).grid(column=2, row=4, sticky="NW")
        ## memory used
        gpu_usedmem = ""
        gpu_used_mem = ttk.Label(self, text="Memory Used  ", foreground=frg_color).grid(column=1, row=5, sticky="NE")
        gpu_used_mem2 = ttk.Label(self, text=gpu_usedmem).grid(column=2, row=5, sticky="NW")
        ## clock
        self.gpu_clock = tk.StringVar()
        self.gpu_clock.set("")
        gpu_clock = ttk.Label(self, text="Clock  ", foreground=frg_color).grid(column=1, row=6, sticky="NE")
        gpu_clock2 = ttk.Label(self, textvariable=self.gpu_clock).grid(column=2, row=6, sticky="NW")
        ## temperature
        self.gpu_temperature = tk.StringVar()
        self.gpu_temperature.set("")
        gpu_temp = ttk.Label(self, text="Temperature  ", foreground=frg_color).grid(column=1, row=7, sticky="NE")
        gpu_temp2 = ttk.Label(self, textvariable=self.gpu_temperature).grid(column=2, row=7, sticky="NW")
        ## gpu usage
        self.gpu_usage = tk.StringVar()
        self.gpu_usage.set("")
        gpu_usage = ttk.Label(self, text="Usage  ", foreground=frg_color).grid(column=1, row=8, sticky="NE")
        gpu_usage2 = ttk.Label(self, textvariable=self.gpu_usage).grid(column=2, row=8, sticky="NW")
        
        self.fupdate()
        
    def fupdate(self):
        # clock
        self.gpu_clock.set("")
        
        # temperature
        self.gpu_temperature.set("")
        
        # usage
        self.gpu_usage.set("")
        
        self.root.after(1000, self.fupdate)
