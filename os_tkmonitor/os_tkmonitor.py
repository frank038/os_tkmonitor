#!/usr/bin/env python3

"""
 by frank38
 V. 0.9
"""
import tkinter as tk
import tkinter.ttk as ttk
import os
import sys
import shutil
import subprocess
from collections import deque
import psutil

######### the followings to personalize the dimensions of the level indicators in the CPU tab
# left pad in canvas
rx1 = 10
# top pad in canvas
ry1 = 25
# width of the background rectangle
rx1_width = 80
# height of the background rectangle
ry1_height = 200
# the pad between the background rectangle
rrpad = 10
# inner rectangles
# width
rx1_in_width = 60
# height
ry1_in_height = 180

###################

# loop interval
LOOP_INTERVAL = 1000
# gpu vendor
GPU_VENDOR = ""
# vendor list
vendor_list = ["nvidia", "nouveau", "amdpro", "radeon", "intel"]

# arguments are passed to the program 
if len(sys.argv) > 1:
    if sys.argv[1].isdigit():
        if int(sys.argv[1]) > 0:
            LOOP_INTERVAL = int(sys.argv[1]) * 1000
        #
        if len(sys.argv) > 2:
            if sys.argv[2] in vendor_list:
                GPU_VENDOR = sys.argv[2]
    # if help
    if sys.argv[1] == "-help":
       print("Usage: os_tkmonitor or os_tkmonitor interval or os_tkmonitor interval gpu_maker")
       sys.exit()

# psutil version
PSUTIL_V = psutil.version_info
if PSUTIL_V < (5,1,0):
    print("Version >= 5.1.0 is required.")
    sys.exit()

# application name
app_name = "OS tkmonitor"
# application width
app_width = 1200
# application height
app_height = 700
# base font size
font_size = 18
# font size for cpu usage level
font_size2 = 18
# alternate text color
frg_color = "gray40"
# background color of diagram
dia_color = "gray70"
# background color of sensors
dia_color2 = "gray80"
# width of the line
dia_width = 2

# number of points in the diagram, one per time defined by LOOP_INTERVAL
deque_size = 30
dcpu = deque('', deque_size)
for i in range(deque_size):
    dcpu.append('0')

###############

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        
        self.pack(fill="both", expand=True)
        self.master.update_idletasks()
        
        self.create_widgets()
        
    # the name of the distro
    def name_distro(self):
        try:
            with open("/etc/os-release") as f:
                lline = f.readline().split("=")[1].replace('"',"").strip()
                return lline
        except:
            try:
                with open("/etc/issue") as f:
                    return f.read().replace("\n","").replace("\l","").strip()
            except:
                return ""
     
    def create_widgets(self):
        # font family and size
        self.s = ttk.Style(self.master)
        self.s.configure('.', font=('', font_size))
        
        # the notebook
        self.wnb = ttk.Notebook(self)
        self.wnb.pack(expand=True, fill="both")
        
        ### Summary
        frame0 = ttk.Frame(self)
        self.wnb.add(frame0, text="Summary")
        
        # Linux Logo
        self.llogo = tk.PhotoImage(file="Tux.png")
        lab_logo = ttk.Label(frame0, image=self.llogo)
        lab_logo.pack(side="left", anchor="nw")
        
        ## some system data
        uname_list = os.uname()
        mem = psutil.virtual_memory()
        mswap = psutil.swap_memory()
        tnet = psutil.net_io_counters()
        
        ## labels
        frame_grid = ttk.Frame(frame0)
        frame_grid.pack(side="left", anchor="n")
        # empty label
        lab_empty = ttk.Label(frame_grid, text="").grid(column=0, row=0)
        # user name
        lab_un = ttk.Label(frame_grid, text="User Name  ", foreground=frg_color).grid(column=0, row=1, sticky="NE")
        u_username = psutil.Process().username()
        lab_un2 = ttk.Label(frame_grid, text=u_username).grid(column=1, row=1, sticky="NW")
        # Network PC name
        lab_netnm = ttk.Label(frame_grid, text="Network PC name  ", foreground=frg_color).grid(column=0, row=2, sticky="NE")
        lab_netnm2 = ttk.Label(frame_grid, text=uname_list.nodename).grid(column=1, row=2, sticky="NW")
        # Distro
        lab_distronm = ttk.Label(frame_grid, text="Distro  ", foreground=frg_color).grid(column=0, row=3, sticky="NE")
        lab_distronm2 = ttk.Label(frame_grid, text=(self.name_distro() or uname_list.sysname or "None")).grid(column=1, row=3, sticky="NW")
        
        # kernel version
        lab_kernel = ttk.Label(frame_grid, text="Kernel Version  ", foreground=frg_color).grid(column=0, row=4, sticky="NE")
        kernel_release = uname_list.release
        lab_kernel2 = ttk.Label(frame_grid, text=kernel_release).grid(column=1, row=4, sticky="NW")
        
        # desktop
        lab_desktop = ttk.Label(frame_grid, text="Desktop Manager  ", foreground=frg_color).grid(column=0, row=5, sticky="NE")
        u_dmname = os.environ['XDG_CURRENT_DESKTOP']
        lab_desktop2 = ttk.Label(frame_grid, text=u_dmname).grid(column=1, row=5, sticky="NW")
        
        # processor
        lab_cpu = ttk.Label(frame_grid, text="Processor  ", foreground=frg_color).grid(column=0, row=6, sticky="NE")
        # processor
        u_proc_num = psutil.cpu_count()
        u_proc_num_real = psutil.cpu_count(logical=False)
        u_proc_model_name = ""
        u_proc_model = ""
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line.rstrip('\n').startswith('model name'):
                    u_proc_model_name = line.rstrip('\n').split(':')[1].strip()
                    break;
            f.close()
        except:
            u_proc_model_name("#")
        if u_proc_num_real == u_proc_num:
            u_proc_model = u_proc_model_name+" x "+str(u_proc_num_real)
        else:
            u_proc_model = u_proc_model_name+" x ("+str(u_proc_num_real)+"+"+str(u_proc_num)+")"
        lab_processor2 = ttk.Label(frame_grid, text=u_proc_model).grid(column=1, row=6, sticky="NW")
        
        # Gpu
        lab_gpu = ttk.Label(frame_grid, text="Gpu  ", foreground=frg_color).grid(column=0, row=7, sticky="NE")
        # gpu name
        gpu_name = "#"
        try:
            # check whether nvidia-smi is in the system
            if shutil.which("nvidia-smi"):
                gpu_name = subprocess.check_output("nvidia-smi --query-gpu=gpu_name --format=csv,noheader",shell=True).decode().strip()
            # alternate method
            else:
                # the first 50 chars only
                gpu_name = subprocess.check_output('lspci | grep VGA | cut -d ":" -f3', shell=True).decode().strip()[0:50]
        except:
            pass
        lab_gpu2 = ttk.Label(frame_grid, text=gpu_name).grid(column=1, row=7, sticky="NW")
        
        # installed memory
        lab_inst_mem = ttk.Label(frame_grid, text="Installed Memory  ", foreground=frg_color).grid(column=0, row=8, sticky="NE")
        lab_inst_mem2 = ttk.Label(frame_grid, text=self.el_size(mem.total)).grid(column=1, row=8, sticky="NW")
        
        # swap
        lab_swap = ttk.Label(frame_grid, text="Swap  ", foreground=frg_color).grid(column=0, row=9, sticky="NE")
        
        u_swapmem = 0
        try:
            u_swapmem = mswap.total
            if u_swapmem == None:
                u_swapmem = 0
        except:
            u_swapmem = 0
        
        lab_swap2 = ttk.Label(frame_grid, text=self.el_size(u_swapmem)).grid(column=1, row=9, sticky="NW")
        
        # root or home disk size
        # partitions
        partitions = psutil.disk_partitions(all=False)
        num_partitions = len(partitions)
        # check the moutpoint
        home_partition = ""
        for i in range(num_partitions):
            if partitions[i].mountpoint == "/":
                root_partition = partitions[i].device
                root_fstype = partitions[i].fstype
                root_disk_usage = psutil.disk_usage('/')
                root_disk_total = self.el_size(root_disk_usage.total)
            if partitions[i].mountpoint == "/home":
                home_partition = partitions[i].device
                home_fstype = partitions[i].fstype
                home_disk_usage = psutil.disk_usage('/home')
                home_disk_total = self.el_size(home_disk_usage.total)
        # root disk size
        lab_root_disk_size = ttk.Label(frame_grid, text="Disk Size  ", foreground=frg_color).grid(column=0, row=10, sticky="NE")
        lab_root_disk_size2 = ttk.Label(frame_grid, text=root_disk_total).grid(column=1, row=10, sticky="NW")
        # root device and type
        lab_root_disk_type = ttk.Label(frame_grid, text="Root Device and Type  ", foreground=frg_color).grid(column=0, row=11, sticky="NE")
        root_dev_type = root_partition + " - " + root_fstype
        lab_root_disk_type2 = ttk.Label(frame_grid, text=root_dev_type).grid(column=1, row=11, sticky="NW")
        
        # if the home partition is present
        if home_partition != "":
            # home disk size
            lab_home_disk_size = ttk.Label(frame_grid, text="Home Size  ", foreground=frg_color).grid(column=0, row=12, sticky="NE")
            lab_home_disk_size2 = ttk.Label(frame_grid, text=home_disk_total).grid(column=1, row=12, sticky="NW")
        
            # home device and type
            lab_home_disk_type = ttk.Label(frame_grid, text="Home Device and Type  ", foreground=frg_color).grid(column=0, row=13, sticky="NE")
            home_dev_type = home_partition + " - " + home_fstype
            lab_home_disk_type2 = ttk.Label(frame_grid, text=root_dev_type).grid(column=1, row=13, sticky="NW")
        
        # battery - static info : not tested
        if PSUTIL_V > (5,1,0):
            battery = psutil.sensors_battery()
            if battery != None:
                lab_battery = ttk.Label(frame_grid, text="Battery  ", foreground=frg_color).grid(column=0, row=5, sticky="NE")
                #
                bsec = int(battery.secsleft)
                stbsec = "very very low"
                if bsec/60/60 > 1:
                    # hours 
                    tbsec = bsec/60/60
                    stbsec = str(round(tbsec, 2))+" hours"
                elif bsec/60 > 1:
                    # minutes
                    tbsec = bsec/60
                    stbsec = str(round(tbsec, 2))+" minutes"
                label12 = str(battery.percent)+"% - "+stbsec
                #
                lab_battery2 = ttk.Label(frame_grid, text=label12).grid(column=1, row=5, sticky="NW")
        
        ###### tab 1 Memory and Network ######
        frame1 = ttk.Frame(self)
        self.wnb.add(frame1, text="Memory and Network")
        
        lab_memory = ttk.Label(frame1, text="\n Memory").grid(column=0, row=0, sticky="NW")
        # installed memory
        lab_inst_memory = ttk.Label(frame1, text="Installed Memory  ", foreground=frg_color).grid(column=1, row=1, sticky="NE")
        inst_mem = self.el_size(mem.total)
        lab_inst_memory2 = ttk.Label(frame1, text=inst_mem).grid(column=2, row=1, sticky="NW")
        # memory available
        lab_avail_memory = ttk.Label(frame1, text="Available Memory  ", foreground=frg_color).grid(column=1, row=2, sticky="NE")
        avail_mem = self.el_size(mem.available)
        lab_avail_memory2 = ttk.Label(frame1, text=avail_mem).grid(column=2, row=2, sticky="NW")
        # used memory
        lab_used_memory = ttk.Label(frame1, text="Used Memory  ", foreground=frg_color).grid(column=1, row=3, sticky="NE")
        used_mem = self.el_size(mem.used)+" ("+str(mem.percent)+"%)"
        lab_used_memory2 = ttk.Label(frame1, text=used_mem).grid(column=2, row=3, sticky="NW")
        # freee memory
        lab_free_memory = ttk.Label(frame1, text="Free Memory  ", foreground=frg_color).grid(column=1, row=4, sticky="NE")
        free_mem = self.el_size(mem.free)
        lab_free_memory2 = ttk.Label(frame1, text=free_mem).grid(column=2, row=4, sticky="NW")
        # buffer/cache
        lab_buff_memory = ttk.Label(frame1, text="Buff/Cached Memory  ", foreground=frg_color).grid(column=1, row=5, sticky="NE")
        buff_mem = self.el_size(mem.buffers+mem.cached)
        lab_buff_memory2 = ttk.Label(frame1, text=buff_mem).grid(column=2, row=5, sticky="NW")
        # shared memory
        lab_shared_memory = ttk.Label(frame1, text="Shared Memory  ", foreground=frg_color).grid(column=1, row=6, sticky="NE")
        shared_mem = self.el_size(mem.shared)
        lab_shared_memory2 = ttk.Label(frame1, text=shared_mem).grid(column=2, row=6, sticky="NW")
        
        ## Swap
        lab_swap = ttk.Label(frame1, text="\n Swap").grid(column=0, row=7, sticky="NW")
        # total
        lab_total_swap = ttk.Label(frame1, text="Total  ", foreground=frg_color).grid(column=1, row=8, sticky="NE")
        total_swap = self.el_size(mswap.total) or ""
        lab_total_swap2 = ttk.Label(frame1, text=total_swap).grid(column=2, row=8, sticky="NW")
        # used - if it exists
        if u_swapmem > 0:
            lab_used_swap = ttk.Label(frame1, text="Used  ", foreground=frg_color).grid(column=1, row=9, sticky="NE")
            used_swap = self.el_size(mswap.used)+" ("+str(mswap.percent)+"%)"
            lab_used_swap2 = ttk.Label(frame1, text=used_swap).grid(column=2, row=9, sticky="NW")
        
        ## net
        lab_net = ttk.Label(frame1, text="\n Net").grid(column=0, row=10, sticky="NW")
        # bytes/packets received
        lab_bytes_recv = ttk.Label(frame1, text="bytes/packets received  ", foreground=frg_color).grid(column=1, row=11, sticky="NE")
        bytes_recv = str(self.el_size(tnet.bytes_recv))+" - "+str(tnet.packets_recv)
        lab_bytes_recv2 = ttk.Label(frame1, text=bytes_recv).grid(column=2, row=11, sticky="NW")
        # bytes/packets sent
        lab_bytes_sent = ttk.Label(frame1, text="bytes/packets sent  ", foreground=frg_color).grid(column=1, row=12, sticky="NE")
        bytes_sent = str(self.el_size(tnet.bytes_sent))+" - "+str(tnet.packets_sent)
        lab_bytes_sent2 = ttk.Label(frame1, text=bytes_sent).grid(column=2, row=12, sticky="NW")
        # errin/dropin
        lab_errin = ttk.Label(frame1, text="errin/dropin  ", foreground=frg_color).grid(column=1, row=13, sticky="NE")
        errin = str(tnet.errin)+" - "+str(tnet.dropin)
        lab_errin2 = ttk.Label(frame1, text=errin).grid(column=2, row=13, sticky="NW")
        # errout/dropout
        lab_errout = ttk.Label(frame1, text="errout/dropout  ", foreground=frg_color).grid(column=1, row=14, sticky="NE")
        errout = str(tnet.errout)+" - "+str(tnet.dropout)
        lab_errout2 = ttk.Label(frame1, text=errout).grid(column=2, row=14, sticky="NW")
        
        ###### tab 2 Disks ######
        frame2 = ttk.Frame(self)
        self.wnb.add(frame2, text="Disks")
        ## Disks
        lab_disks = ttk.Label(frame2, text="\n Disks").grid(column=0, row=0, sticky="NW")
        # 
        # how many partitions
        tpartitions = psutil.disk_partitions(all=False)
        npartitions = len(tpartitions)
        for i in range(npartitions):
            part_mount_p = tpartitions[i].mountpoint
            # the efi partition is dropped
            if part_mount_p not in ["/boot/efi"]:
                # mount point
                ppart = ttk.Label(frame2, text="Mount Point  ", foreground=frg_color).grid(column=1, row=(i*4)+1, sticky="NE")
                tppart = ttk.Label(frame2, text=part_mount_p).grid(column=2, row=(i*4)+1, sticky="NW")
                # type
                ptype = ttk.Label(frame2, text="Type  ", foreground=frg_color).grid(column=1, row=(i*4)+2, sticky="NE")
                pfstype = tpartitions[i].fstype
                tptype = ttk.Label(frame2, text=pfstype).grid(column=2, row=(i*4)+2, sticky="NW")
                # used - free
                pused = ttk.Label(frame2, text="Total/Used  ", foreground=frg_color).grid(column=1, row=(i*4)+3, sticky="NE")
                ptot_used = self.el_size(psutil.disk_usage(psutil.disk_partitions()[i].mountpoint).total)+" - "+self.el_size(psutil.disk_usage(psutil.disk_partitions()[i].mountpoint).used)
                tpused = ttk.Label(frame2, text=ptot_used).grid(column=2, row=(i*4)+3, sticky="NW")
                # blank line
                ttk.Label(frame2, text=" ").grid(column=1, row=(i*4)+4)
        
        ###### tab 3 Cpu ######
        frame3 = ttk.Frame(self)
        self.wnb.add(frame3, text="Cpu")
        
        # top frame
        frame3a = ttk.Frame(frame3, height=290)
        frame3a.pack(side="top", fill="both", expand=True)
        frame3a.pack_propagate(0)
        
        ## first canvas
        self.canvas = tk.Canvas(frame3a, height=290)
        self.canvas.configure(bg=dia_color)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.master.update_idletasks()
        
        ## second canvas
        self.canvas2 = tk.Canvas(frame3a, width=200, height=290)
        self.canvas2.configure(bg=dia_color2)
        self.canvas2.pack(side="right", fill="both", expand=False)

        self.master.update_idletasks()
        
        ############# the level widgets
        ####### global level
        # background
        self.canvas2.create_rectangle(50, 25, 150, 250, fill="black")
        #
        self.canvas2.create_rectangle(64, 40, 136, 236, fill="#000bbb000")
        #
        canvas_id = self.canvas2.create_rectangle(64, 40, 136, 236, fill="#000222000")
        # the text
        id_text = self.canvas2.create_text(100,250, text="0.0", font=("", font_size+2), justify="center", anchor="n")

        ###### per cpu levels
        # frame
        frame3b = ttk.Frame(frame3)
        frame3b.pack(side="bottom", fill="both", expand=True)
        # canvas
        self.canvas3 = tk.Canvas(frame3b)
        self.canvas3.configure(bg=dia_color2)
        self.canvas3.pack(fill="both", expand=True)
        
        # how many physical cores (no virtual ones)
        self.c2_num_cpu = psutil.cpu_count(logical=True)
        # canvas2 width and height
        c2_width = self.canvas3.winfo_width()
        c2_height = self.canvas3.winfo_height()

        # how many widgets (one per core)
        c2_num_rect = c2_width / self.c2_num_cpu
        
        # needed to draw the widgets
        # the background rectangle
        self.x1 = rx1
        self.y1 = ry1
        self.x1_width = rx1_width
        self.y1_height = ry1_height
        self.rpad = rrpad
        # inner rectangles
        self.x1_in_width = rx1_in_width
        self.y1_in_height = ry1_in_height
        #
        self.rxinpad = (self.x1_width - self.x1_in_width)/2
        self.ryinpad = (self.y1_height - self.y1_in_height)/2
        
        #
        for i in range(int(self.c2_num_cpu)):
            a1 = (self.rpad + self.x1_width)*i
            
            self.canvas3.create_rectangle(self.x1+a1, self.y1, self.x1+self.x1_width+a1, self.y1+self.y1_height, fill="black")
            
            self.canvas3.create_rectangle(self.x1+a1+self.rxinpad, self.y1+self.ryinpad, self.x1+a1+self.rxinpad+self.x1_in_width, self.y1+self.ryinpad+self.y1_in_height, fill="#000bbb000")
            
            self.canvas3.create_rectangle(self.x1+a1+self.rxinpad, self.y1+self.ryinpad, self.x1+a1+self.rxinpad+self.x1_in_width, self.y1+self.ryinpad+self.y1_in_height, fill="#000222000", tags=("c2r_"+str(i),))
            
            self.canvas3.create_text(self.x1+self.x1_width/2+a1, self.y1+self.y1_height+3, text="0.0", font=("", font_size2), justify="center", anchor="n", tags=("c2t_"+str(i),))
        
        #
        self.pop_deque(canvas_id, id_text)
        
        
        ###### aggiungo tab 4 Gpu ######
        if GPU_VENDOR:
            self.frame4 = ttk.Frame(self)
            self.wnb.add(self.frame4, text="Gpu")
            #
            # nvidia
            if GPU_VENDOR == "nvidia":
                try:
                    import os_tkmonitor_nvidia
                    fr_nv = os_tkmonitor_nvidia.FNV(self.frame4, self.master, frg_color)
                except:
                    pass
            # nouveau
            elif GPU_VENDOR == "nouveau":
                try:
                    import os_tkmonitor_nouveau
                    fr_nv = os_tkmonitor_nouveau.FNV(self.frame4, self.master, frg_color)
                except Exception as E:
                    pass
            # amdpro
            elif GPU_VENDOR == "amdpro":
                try:
                    import os_tkmonitor_amdpro
                    fr_nv = os_tkmonitor_amdpro.FNV(self.frame4, self.master, frg_color)
                except:
                    pass
            # radeon
            elif GPU_VENDOR == "radeon":
                try:
                    import os_tkmonitor_radeon
                    fr_nv = os_tkmonitor_radeon.FNV(self.frame4, self.master, frg_color)
                except:
                    pass
            # intel
            elif GPU_VENDOR == "intel":
                try:
                    import os_tkmonitor_intel
                    fr_nv = os_tkmonitor_intel.FNV(self.frame4, self.master, frg_color)
                except:
                    pass

    #
    def pop_deque(self, canvas_id, id_text):
        self.canvas.delete(tk.ALL)
        #
        ii = 0
        #
        c_width = self.canvas.winfo_width()
        # 
        c_height = self.canvas.winfo_height()
        # min 2 
        p_pad = 2
        #
        p_space = (c_width-(p_pad*2))/(deque_size-1)
        
        self.canvas.create_line(0,c_height/4,c_width,c_height/4,width=1,fill="black")
        
        self.canvas.create_line(0,c_height/2,c_width,c_height/2,width=1,fill="black")
        
        self.canvas.create_line(0,c_height/4*3,c_width,c_height/4*3,width=1,fill="black")
        
        #
        list_point = []
        x_point = []
    
        for item in dcpu:
            line_h = ((100-float(item))*(c_height-(p_pad*2)))/100
            
            list_point.append(line_h or p_pad)
            
            x_space = p_space*(ii)+p_pad
            x_point.append(x_space)
            
            ii += 1
        
        list_line = []
        for x,y in zip(x_point, list_point):
            list_line.append(x)
            list_line.append(y)
        
        #
        self.canvas.create_line(list_line, width=dia_width, fill="red", smooth=True)
        
        cpu_pc = psutil.cpu_percent()
        
        dcpu.append(cpu_pc)
        
        ### global level
        if cpu_pc !=0 :
            h_lev_rel = (cpu_pc * 175) / 100
        else:
            h_lev_rel = 0
        
        self.canvas2.coords(canvas_id, 64, 40, 136, 236 - h_lev_rel)
        
        self.canvas2.itemconfigure(id_text, text=str(cpu_pc))
        
        ################## per core level
        #
        c2_us_cpu = psutil.cpu_percent(percpu=True)
        #
        for nn in range(self.c2_num_cpu):
            #
            if c2_us_cpu[nn] !=0 :
                h_lev_rel2 = (c2_us_cpu[nn] * self.y1_in_height) / 100
            else:
                h_lev_rel2 = 0
        
            a1 = (self.rpad + self.x1_width)*nn
            self.canvas3.coords("c2r_"+str(nn), self.x1+a1+self.rxinpad, self.y1+self.ryinpad, self.x1+a1+self.rxinpad+self.x1_in_width, self.y1+self.ryinpad+self.y1_in_height - h_lev_rel2)
    
            ### the label of each level indicator
            # frequencies
            all_core_freq = psutil.cpu_freq(percpu=True)
            core_freq = int(all_core_freq[nn].current)
            # temperatures
            all_core_temp = psutil.sensors_temperatures()['coretemp']
            core_temp = int(psutil.sensors_temperatures()['coretemp'][nn].current)
            #
            self.canvas3.itemconfigure("c2t_"+str(nn), text=str(c2_us_cpu[nn])+"\n"+str(core_freq)+"\n"+str(core_temp))
        
        #
        self.master.after(LOOP_INTERVAL, lambda:self.pop_deque(canvas_id, id_text))

    
    #  size in the readable format
    def el_size(self, esize):
        if esize == 0 or esize == 1:
            oesize = str(esize)+" byte"
        elif esize//1024 == 0:
            oesize = str(esize)+" bytes"
        elif esize//1048576 == 0:
            oesize = str(round(esize/1024, 3))+" KB"
        elif esize//1073741824 == 0:
            oesize = str(round(esize/1048576, 3))+" MB"
        elif esize//1099511627776 == 0:
            oesize = str(round(esize/1073741824, 1))+" GiB"
        else:
            oesize = str(round(esize/1099511627776, 1))+" GiB"
        
        return oesize

###########
def main():
    root = tk.Tk()
    root.title(app_name)
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    width = app_width
    height = app_height
    root.geometry('{}x{}'.format(width, height))
    
    # style
    s = ttk.Style()
    s.theme_use("clam")
    
    app = Application(master=root)
    app.mainloop()
    
if __name__ == "__main__":
    main()
