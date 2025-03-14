import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import datetime
import re
import os
import random as rd
from PIL import Image, ImageDraw, ImageTk
import threading
import base64
from io import BytesIO
import time
import sys

plt.close("all")
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 24})
plt.rcParams['lines.linewidth'] = 1

def resource_path(relative_path):
    """Retorna o caminho absoluto para o recurso, considerando execução como executável."""
    if hasattr(sys, '_MEIPASS'):
        # Quando executado como executável
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # Quando executado como script Python
        return os.path.abspath(relative_path)

# Caminho para a figura
image_path = resource_path("logo_smit.png")

def principal():
    j0.destroy()
    #----------------------------------JANELA 1------------------------------#
    j1 = tk.Tk()
    j1.option_add("*Font", ("Segoe UI", 11))
    j1.title("SMIT")
    #j1.geometry("1050x500")
    #j1.geometry("+%d+%d" % ((j1.winfo_screenwidth()-1050 ) / 2,
    #(j1.winfo_screenheight()-500 ) / 2))
    j1.state("zoomed")

    def on_close():
        for window in j1.winfo_children():  # Fecha todas as janelas secundárias
            if isinstance(window, tk.Toplevel):
                window.destroy()
        j1.destroy()
        j1.quit()

    j1.protocol("WM_DELETE_WINDOW", on_close)

    #---------------Frame da barra superior--------------------
    barra_superior = tk.Frame(j1, height=30, relief=tk.RAISED, bd=2)
    barra_superior.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
    # Impedir que o tamanho do frame da barra superior seja alterado automaticamente
    barra_superior.pack_propagate(False)
    def criar_icone_play(tamanho=20):
        image = Image.new("RGBA", (tamanho, tamanho), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        pontos = [(tamanho//4, tamanho//4), (tamanho//4, 3*tamanho//4), (3*tamanho//4, tamanho//2)]
        draw.polygon(pontos, fill="green")
        return ImageTk.PhotoImage(image)
    icone_play = criar_icone_play(tamanho=20)

    def criar_icone_stop(tamanho=20):
        image = Image.new("RGBA", (tamanho, tamanho), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        draw.rectangle([0, 0, tamanho, tamanho], fill="red")
        return ImageTk.PhotoImage(image)
    icone_stop = criar_icone_stop(tamanho=20)

    frame_entradas = tk.Frame(j1)
    frame_entradas.pack()

    # img_org = Image.open(r"logo_smit.png")
    img_org = Image.open(image_path)
    escala_im = 0.2
    img_l = int(img_org.width * escala_im)
    img_h = int(img_org.height * escala_im)
    img_red = img_org.resize((img_l, img_h), Image.LANCZOS)

    tk_image = ImageTk.PhotoImage(img_red)
    label_logosmit = tk.Label(frame_entradas, image=tk_image)
    label_logosmit.place(relx=1.02, rely=-0.1, anchor='ne')
    label_logosmit.image = tk_image

    #----------------------------------Tempo------------------------------#
    label_tempo = tk.Label(frame_entradas, text="\n\nSimulation Variables", font=("Segoe UI", 12, "bold"))
    label_tempo.grid(row=2, columnspan=8,sticky=tk.W)

    label_spacecolumn1=tk.Label(frame_entradas,text="       ")
    label_spacecolumn1.grid(row=2,column=2)
    label_spacecolumn2=tk.Label(frame_entradas,text="       ")
    label_spacecolumn2.grid(row=2,column=5)

    label_dt = tk.Label(frame_entradas, text="Sampling Frequency (Hz):")
    label_dt.grid(row=3, column=0, sticky=tk.W)

    def dt_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Frequency that defines the time interval between iterations.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    def destroy(event):
        popup.destroy()


    label_dt.bind("<Enter>", dt_message)
    label_dt.bind("<Leave>", destroy)
    entry_dt = tk.Entry(frame_entradas)
    entry_dt.insert(0, 1e4)
    entry_dt.grid(row=3, column=1, sticky=tk.W + tk.E)

    label_tt = tk.Label(frame_entradas, text="Simulation time (s):")
    label_tt.grid(row=3, column=3, sticky=tk.W)


    def tt_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Total simulated time (Large values may slow down the simulation)", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_tt.bind("<Enter>", tt_message)
    label_tt.bind("<Leave>", destroy)
    entry_tt = tk.Entry(frame_entradas)
    entry_tt.insert(0, 5)
    entry_tt.grid(row=3, column=4, sticky=tk.W + tk.E)

    #----------------------------------Alimentação------------------------------#
    # label_tempo = tk.Label(frame_entradas, text="Configuração da Alimentação", font=("Segoe UI", 12, "bold"))
    # label_tempo.grid(row=4, columnspan=8, sticky=tk.W)
    #
    # label_alim = tk.Label(frame_entradas, text="Tipo de alimentação:")
    # label_alim.grid(row=5, column=0, sticky=tk.W)
    # def alim_message(event):
    #     global popup
    #     popup = tk.Toplevel(j1)
    #     popup.geometry("+100+50")
    #     message = tk.Label(popup,
    #                        text="Indica a forma de alimentação do motor")
    #     message.place(relx=0, rely=0)
    #     message.pack()
    #
    #
    # label_alim.bind("<Enter>", alim_message)
    # label_alim.bind("<Leave>", destroy)
    # selected_alim = tk.StringVar(frame_entradas)
    # options_alim = ["Senoidal", "PWM"]
    # entry_alim = ttk.Combobox(frame_entradas, values=list(options_alim), textvariable=selected_alim)
    # entry_alim.grid(row=5, column=1, sticky=tk.W + tk.E)
    # entry_alim.set(options_alim[0])

    label_V = tk.Label(frame_entradas, text="Line RMS voltage (V):")
    label_V.grid(row=5, column=0, sticky=tk.W)

    def V_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Nominal line voltage that powers the motor.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_V.bind("<Enter>", V_message)
    label_V.bind("<Leave>", destroy)
    entry_V = tk.Entry(frame_entradas)
    entry_V.insert(0, 460)
    entry_V.grid(row=5, column=1, sticky=tk.W + tk.E)

    label_f = tk.Label(frame_entradas, text="Supply frequency:")
    label_f.grid(row=5, column=3, sticky=tk.W)


    def f_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Frequency of the machine's supply signal.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_f.bind("<Enter>", f_message)
    label_f.bind("<Leave>", destroy)
    entry_f = tk.Entry(frame_entradas)
    entry_f.insert(0, 60)
    entry_f.grid(row=5, column=4, sticky=tk.W + tk.E)

    # label_fpwm = tk.Label(frame_entradas, text="Frequência do inversor:")
    # label_fpwm.grid(row=6, column=0, sticky=tk.W)
    #
    #
    # def fpwm_message(event):
    #     global popup
    #     popup = tk.Toplevel(j1)
    #     popup.geometry("+100+50")
    #     message = tk.Label(popup, text="Frequência da onda triangular do PWM")
    #     message.place(relx=0, rely=0)
    #     message.pack()
    #
    #
    # label_fpwm.bind("<Enter>", fpwm_message)
    # label_fpwm.bind("<Leave>", destroy)
    # entry_fpwm = tk.Entry(frame_entradas)
    # label_fpwm.config(state='disabled')
    # entry_fpwm.config(state='disabled')
    # entry_fpwm.grid(row=6, column=1, sticky=tk.W + tk.E)
    #
    #
    # def pwm_select(event):
    #     if entry_alim.get() == options_alim[0]:
    #         label_fpwm.config(state='disabled')
    #         entry_fpwm.config(state='disabled')
    #         box_des.grid(row=20, columnspan=6)
    #     elif entry_alim.get() == options_alim[1]:
    #         label_fpwm.config(state='normal')
    #         entry_fpwm.config(state='normal')
    #         entry_fpwm.delete(0, tk.END)
    #         entry_fpwm.insert(0, 5000)
    #         estado_des.set(False)
    #         box_des.grid_remove()
    #
    #
    # entry_alim.bind("<<ComboboxSelected>>", pwm_select)


    #----------------------------------Dados Nominais------------------------------#
    label_tempo = tk.Label(frame_entradas, text="Machine Nominal Data", font=("Segoe UI", 12, "bold"))
    label_tempo.grid(row=4, columnspan=8, sticky=tk.W)

    label_P = tk.Label(frame_entradas, text="Number of Poles:")
    label_P.grid(row=5, column=6, sticky=tk.W)


    def P_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Number of poles in the machine.", wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()


    label_P.bind("<Enter>", P_message)
    label_P.bind("<Leave>", destroy)
    entry_P = tk.Entry(frame_entradas)
    entry_P.insert(0, 4)
    entry_P.grid(row=5, column=7, sticky=tk.W + tk.E)

    label_vnom = tk.Label(frame_entradas, text="Nominal speed (RPM):")
    label_vnom.grid(row=6, column=0, sticky=tk.W)


    def vnom_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Speed reached by the motor under nominal operating conditions.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_vnom.bind("<Enter>", vnom_message)
    label_vnom.bind("<Leave>", destroy)
    entry_vnom = tk.Entry(frame_entradas)
    entry_vnom.insert(0, 1705)
    entry_vnom.grid(row=6, column=1, sticky=tk.W + tk.E)

    label_Tload = tk.Label(frame_entradas, text="Nominal load (Nm):")
    label_Tload.grid(row=7, column=0, sticky=tk.W)


    def Tload_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Load supported by the machine under nominal conditions.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_Tload.bind("<Enter>", Tload_message)
    label_Tload.bind("<Leave>", destroy)
    entry_Tload = tk.Entry(frame_entradas)
    entry_Tload.insert(0, 198)
    entry_Tload.grid(row=7, column=1, sticky=tk.W + tk.E)

    label_j = tk.Label(frame_entradas, text="Moment of inertia (kgm²):")
    label_j.grid(row=6, column=6, sticky=tk.W)


    def j_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Motor's moment of inertia, equivalent to the difficulty in accelerating the machine.", wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()


    label_j.bind("<Enter>", j_message)
    label_j.bind("<Leave>", destroy)
    entry_j = tk.Entry(frame_entradas)
    entry_j.insert(0, 1.662)
    entry_j.grid(row=6, column=7, sticky=tk.W + tk.E)

    label_In = tk.Label(frame_entradas, text="Line RMS current (A):")
    label_In.grid(row=6, column=3, sticky=tk.W)

    def In_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Nominal line current that powers the motor.",
                           wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()

    label_In.bind("<Enter>", In_message)
    label_In.bind("<Leave>", destroy)
    entry_In = tk.Entry(frame_entradas)
    entry_In.insert(0, 46.8)
    entry_In.grid(row=6, column=4, sticky=tk.W + tk.E)

    #----------------------------------Circuito equivalente------------------------------#
    label_tempo = tk.Label(frame_entradas, text="Circuit Parameters (Y)", font=("Segoe UI", 12, "bold"))
    label_tempo.grid(row=10, columnspan=8, sticky=tk.W)

    label_rs = tk.Label(frame_entradas, text="Stator resistance (ohms):")
    label_rs.grid(row=11, column=0, sticky=tk.W)

    def rs_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Stator resistance, from the equivalent circuit.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_rs.bind("<Enter>", rs_message)
    label_rs.bind("<Leave>", destroy)
    entry_rs = tk.Entry(frame_entradas)
    entry_rs.insert(0, 0.087)
    entry_rs.grid(row=11, column=1, sticky=tk.W + tk.E)

    label_rr = tk.Label(frame_entradas, text="Rotor resistance (ohms):")
    label_rr.grid(row=11, column=3, sticky=tk.W)


    def rr_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Rotor resistance, from the equivalent circuit.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_rr.bind("<Enter>", rr_message)
    label_rr.bind("<Leave>", destroy)
    entry_rr = tk.Entry(frame_entradas)
    entry_rr.insert(0, 0.228)
    entry_rr.grid(row=11, column=4, sticky=tk.W + tk.E)

    label_xs = tk.Label(frame_entradas, text="Stator reactance (ohms):")
    label_xs.grid(row=11, column=6, sticky=tk.W)


    def xs_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Stator leakage reactance, from the equivalent circuit.", wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()


    label_xs.bind("<Enter>", xs_message)
    label_xs.bind("<Leave>", destroy)
    entry_xs = tk.Entry(frame_entradas)
    entry_xs.insert(0, 0.302)
    entry_xs.grid(row=11, column=7, sticky=tk.W + tk.E)

    label_xm = tk.Label(frame_entradas, text="Mutual reactance (ohms):")
    label_xm.grid(row=12, column=0, sticky=tk.W)


    def xm_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Machine mutual reactance, from the equivalent circuit.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_xm.bind("<Enter>", xm_message)
    label_xm.bind("<Leave>", destroy)
    entry_xm = tk.Entry(frame_entradas)
    entry_xm.insert(0, 13.08)
    entry_xm.grid(row=12, column=1, sticky=tk.W + tk.E)

    label_xr = tk.Label(frame_entradas, text="Rotor reactance (ohms):")
    label_xr.grid(row=12, column=3, sticky=tk.W)


    def xr_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Rotor leakage reactance, from the equivalent circuit.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_xr.bind("<Enter>", xr_message)
    label_xr.bind("<Leave>", destroy)
    entry_xr = tk.Entry(frame_entradas)
    entry_xr.insert(0, 0.302)
    entry_xr.grid(row=12, column=4, sticky=tk.W + tk.E)

    #----------------------------------Carga------------------------------#
    label_cargaconfig = tk.Label(frame_entradas, text="Load Configurations", font=("Segoe UI", 12,"bold"))
    label_cargaconfig.grid(row=13, columnspan=8, sticky=tk.W)

    label_part = tk.Label(frame_entradas, text="Starting Type:")
    label_part.grid(row=14, column=0, sticky=tk.W)


    def part_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Select whether the motor will start with or without load.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_part.bind("<Enter>", part_message)
    label_part.bind("<Leave>", destroy)


    def carga_select(event):
        if entry_part.get() == options_part[0]:
            label_carga.config(state='disabled')
            entry_carga.config(state='disabled')
            label_tp.config(state='normal')
            entry_tp.config(state='normal')
            entry_tp.delete(0, tk.END)
            balde_tp = round(float(entry_tt.get()) / 3, 4)
            entry_tp.insert(0, balde_tp)
        elif entry_part.get() == options_part[1]:
            label_carga.config(state='normal')
            entry_carga.config(state='normal')
            label_tp.config(state='disabled')
            entry_tp.config(state='disabled')


    selected_part = tk.StringVar(frame_entradas)
    options_part = ["Without Load", "With Load"]
    entry_part = ttk.Combobox(frame_entradas, values=list(options_part), textvariable=selected_part)
    entry_part.bind("<<ComboboxSelected>>", carga_select)
    entry_part.grid(row=14, column=1, sticky=tk.W + tk.E)
    entry_part.set(options_part[0])

    label_carga = tk.Label(frame_entradas, text="Load Type:", state='disabled')
    label_carga.grid(row=14, column=3, sticky=tk.W)


    def carga_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Select the type of load applied at startup.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_carga.bind("<Enter>", carga_message)
    label_carga.bind("<Leave>", destroy)
    selected_carga = tk.StringVar(frame_entradas)
    options_carga = ["Constant", "Linear", "Quadratic"]
    entry_carga = ttk.Combobox(frame_entradas, values=list(options_carga), textvariable=selected_carga, state='disabled')
    entry_carga.grid(row=14, column=4, sticky=tk.W + tk.E)
    entry_carga.set(options_carga[0])

    label_tp = tk.Label(frame_entradas, text="Startup time (s):")
    label_tp.grid(row=15, column=0, sticky=tk.W)


    def tp_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Motor startup time, during which no loads or faults will be applied.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_tp.bind("<Enter>", tp_message)
    label_tp.bind("<Leave>", destroy)
    entry_tp = tk.Entry(frame_entradas)
    balde_tp = round(float(entry_tt.get()) / 3, 4)
    entry_tp.insert(0, balde_tp)
    entry_tp.grid(row=15, column=1, sticky=tk.W + tk.E)

    label_pcarga = tk.Label(frame_entradas, text="Applied load (%)::")
    label_pcarga.grid(row=15, column=3, sticky=tk.W)


    def pcarga_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Percentage of applied load, relative to the nominal load.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_pcarga.bind("<Enter>", pcarga_message)
    label_pcarga.bind("<Leave>", destroy)
    entry_pcarga = tk.Entry(frame_entradas)
    entry_pcarga.insert(0, 100)
    entry_pcarga.grid(row=15, column=4, sticky=tk.W + tk.E)

    label_jload = tk.Label(frame_entradas, text="Moment of inertia (kgm²)::")
    label_jload.grid(row=15, column=6, sticky=tk.W)


    def jload_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Load moment of inertia, equivalent to the difficulty in accelerating the load.", wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()


    label_jload.bind("<Enter>", jload_message)
    label_jload.bind("<Leave>", destroy)
    entry_jload = tk.Entry(frame_entradas)
    entry_jload.insert(0, 0.831)
    entry_jload.grid(row=15, column=7, sticky=tk.W + tk.E)

    #----------------------------------Desequilíbrio------------------------------#
    estado_des = tk.BooleanVar()
    box_des = tk.Checkbutton(frame_entradas, text="Voltage Imbalance", font=("Segoe UI", 12,"bold"), variable=estado_des)
    box_des.grid(row=20, columnspan=8, sticky=tk.W)


    def atualizar_estado_des():
        if estado_des.get():
            entry_desamp.grid(row=21, column=1, sticky=tk.W + tk.E)
            entry_desamp.delete(0, tk.END)
            entry_desamp.insert(0, 100)
            entry_desang.grid(row=21, column=4, sticky=tk.W + tk.E)
            entry_desang.delete(0, tk.END)
            entry_desang.insert(0, 0)
            label_desamp.grid(row=21, column=0, sticky=tk.W)
            label_desang.grid(row=21, column=3, sticky=tk.W)
        else:
            entry_desamp.grid_remove()
            entry_desang.grid_remove()
            label_desamp.grid_remove()
            label_desang.grid_remove()


    label_desamp = tk.Label(frame_entradas, text="Imbalance percentage (%):")

    def desamp_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="This value will be multiplied by the amplitude of the phase A supply voltage.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_desamp.bind("<Enter>", desamp_message)
    label_desamp.bind("<Leave>", destroy)
    entry_desamp = tk.Entry(frame_entradas)

    label_desang = tk.Label(frame_entradas, text="Angular imbalance (°):")


    def desang_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Value, in degrees, that will be added to the phase A phase shift (recommended between -30° to 30°).", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_desang.bind("<Enter>", desang_message)
    label_desang.bind("<Leave>", destroy)
    entry_desang = tk.Entry(frame_entradas)

    box_des.config(command=atualizar_estado_des)

    #----------------------------------Curto------------------------------#
    estado_curto = tk.BooleanVar()
    box_curto = tk.Checkbutton(frame_entradas, text="Short Circuit in the Stator Windings", font=("Segoe UI", 12,"bold"),
                               variable=estado_curto)
    box_curto.grid(row=22, columnspan=8, sticky=tk.W)


    def atualizar_estado_curto():
        if estado_curto.get():
            entry_mi.grid(row=23, column=1, sticky=tk.W + tk.E)
            entry_mi.delete(0, tk.END)
            entry_mi.insert(0, 1)
            entry_rf.grid(row=23, column=4, sticky=tk.W + tk.E)
            entry_rf.delete(0, tk.END)
            entry_rf.insert(0, 1)
            label_mi.grid(row=23, column=0, sticky=tk.W)
            label_rf.grid(row=23, column=3, sticky=tk.W)
        else:
            entry_mi.grid_remove()
            entry_rf.grid_remove()
            label_mi.grid_remove()
            label_rf.grid_remove()


    label_mi = tk.Label(frame_entradas, text="Winding short circuit ratio (%):")

    def mi_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Ratio between the number of short-circuited windings and the total (recommended value between 0 and 5%).", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_mi.bind("<Enter>", mi_message)
    label_mi.bind("<Leave>", destroy)
    entry_mi = tk.Entry(frame_entradas)

    label_rf = tk.Label(frame_entradas, text="Multiplier:")


    def rf_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="This variable directly impacts the amplitude of the motor fault current, and its value represents the ratio between the short-circuit current and the motor's nominal current.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_rf.bind("<Enter>", rf_message)
    label_rf.bind("<Leave>", destroy)
    entry_rf = tk.Entry(frame_entradas)
    box_curto.config(command=atualizar_estado_curto)

    #----------------------------------Barras Quebradas------------------------------#
    estado_barra = tk.BooleanVar()
    box_barra = tk.Checkbutton(frame_entradas, text="Broken Bars in the Rotor", font=("Segoe UI", 12,"bold"),
                               variable=estado_barra)
    box_barra.grid(row=24, columnspan=6, sticky=tk.W)


    def atualizar_estado_barra():
        if estado_barra.get():
            entry_n.grid(row=25, column=1, sticky=tk.W + tk.E)
            entry_n.delete(0, tk.END)
            entry_n.insert(0, 28)
            entry_nbq.grid(row=25, column=4, sticky=tk.W + tk.E)
            entry_nbq.delete(0, tk.END)
            entry_nbq.insert(0, 1)
            entry_nivelbq.grid(row=25, column=7, sticky=tk.W + tk.E)
            balde_nivelbq = entry_nivelbq.get()
            if balde_nivelbq == "":
                entry_nivelbq.delete(0, tk.END)
                entry_nivelbq.set(options_nivelbq[2])
            else:
                entry_nivelbq.delete(0, tk.END)
                entry_nivelbq.set(balde_nivelbq)
            label_n.grid(row=25, column=0, sticky=tk.W)
            label_nbq.grid(row=25, column=3, sticky=tk.W)
            label_nivelbq.grid(row=25, column=6, sticky=tk.W)

        else:
            entry_n.grid_remove()
            entry_nbq.grid_remove()
            entry_nivelbq.grid_remove()
            label_n.grid_remove()
            label_nbq.grid_remove()
            label_nivelbq.grid_remove()


    label_n = tk.Label(frame_entradas, text="Total number of bars:")


    def n_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup, text="Total number of bars present in the rotor construction.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_n.bind("<Enter>", n_message)
    label_n.bind("<Leave>", destroy)
    entry_n = tk.Entry(frame_entradas)

    label_nbq = tk.Label(frame_entradas, text="Number of broken bars:")


    def nbq_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Number of broken bars in the rotor (it is recommended to have a maximum of 3 bars, and this value should never exceed the total number of bars, as it would cause a code error).)", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_nbq.bind("<Enter>", nbq_message)
    label_nbq.bind("<Leave>", destroy)
    entry_nbq = tk.Entry(frame_entradas)

    label_nivelbq = tk.Label(frame_entradas, text="Failure level:")


    def nivelbq_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Indicates the failure level, with the number in parentheses representing the percentage of current reduction in the bar.", wraplength=300)
        message.place(relx=0, rely=0)
        message.pack()

    label_nivelbq.bind("<Enter>", nivelbq_message)
    label_nivelbq.bind("<Leave>", destroy)
    selected_nivelbq = tk.StringVar(frame_entradas)
    options_nivelbq = ["Crack (10%)", "Fracture (50%)", "Break (100%)"]
    entry_nivelbq = ttk.Combobox(frame_entradas, values=list(options_nivelbq), textvariable=selected_nivelbq)
    #entry_nivelbq=tk.Entry(frame_entradas, state="disabled")
    #entry_nivelbq.grid(row=14,column=5,sticky=tk.W+tk.E)

    box_barra.config(command=atualizar_estado_barra)

    #----------------------------------Falhas Mecânicas------------------------------#
    estado_mec = tk.BooleanVar()
    box_mec = tk.Checkbutton(frame_entradas, text="Mechanical Failures", font=("Segoe UI", 12,"bold"), variable=estado_mec)
    box_mec.grid(row=26, columnspan=6, sticky=tk.W)


    def atualizar_estado_mec():
        if estado_mec.get():
            entry_Tfalha.grid(row=27, column=1, sticky=tk.W + tk.E)
            entry_Tfalha.delete(0, tk.END)
            entry_Tfalha.insert(0, 1)
            label_Tfalha.grid(row=27, column=0, sticky=tk.W)
        else:
            entry_Tfalha.grid_remove()
            label_Tfalha.grid_remove()

    label_Tfalha = tk.Label(frame_entradas, text="Failure torque (%)::")


    def Tfalha_message(event):
        global popup
        popup = tk.Toplevel(j1)
        x = j1.winfo_pointerx()
        y = j1.winfo_pointery()
        popup.geometry(f"+{x}+{y}")
        message = tk.Label(popup,
                           text="Mechanical failures are simulated by adding a variable torque to the load torque, and the magnitude of this torque is obtained from a percentage of the nominal torque.", wraplength=400)
        message.place(relx=0, rely=0)
        message.pack()


    label_Tfalha.bind("<Enter>", Tfalha_message)
    label_Tfalha.bind("<Leave>", destroy)
    entry_Tfalha = tk.Entry(frame_entradas)

    box_mec.config(command=atualizar_estado_mec)


    #----------------------------------Botão de Simulação------------------------------#
    # thread = None
    executando = False
    def iniciar_simu():
        # global thread
        # if not thread or not thread.is_alive():
        thread = threading.Thread(target=validar)
        thread.start()

    def validar():
        a = 0
        b = 0

        def adicionar_mensagem(mensagem):
            texto.config(state=tk.NORMAL)
            texto.insert(tk.END, mensagem + "\n")
            texto.config(state=tk.DISABLED)
            texto.see(tk.END)

        jerro = tk.Toplevel()
        jerro.title("Errors")
        texto = tk.Text(jerro, wrap="word", state=tk.DISABLED)
        texto.pack(fill=tk.BOTH, expand=True)
        try:
            valor = (entry_dt.get())
            valor = valor.replace(",", ".")
            entry_dt.delete(0, tk.END)
            entry_dt.insert(0, valor)
            valor = float(entry_dt.get())
            entry_dt.config(bg="white")
            if valor<1000:
                entry_dt.config(bg="red")
                adicionar_mensagem("Sampling frequency lower than the minimum accepted: 1000 Hz.")
                a+=1
        except ValueError:
            entry_dt.config(bg="red")
            adicionar_mensagem(label_dt.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_tt.get())
            valor = valor.replace(",", ".")
            entry_tt.delete(0, tk.END)
            entry_tt.insert(0, valor)
            valor = float(entry_tt.get())
            entry_tt.config(bg="white")
            if valor<=0:
                entry_tt.config(bg="red")
                adicionar_mensagem(label_tt.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_tt.config(bg="red")
            adicionar_mensagem(label_tt.cget("text") + " INVALID INPUT!")
            a += 1

        # try:
        #     valor = (entry_fnom.get())
        #     valor = valor.replace(",", ".")
        #     entry_fnom.delete(0, tk.END)
        #     entry_fnom.insert(0, valor)
        #     valor = float(entry_fnom.get())
        #     entry_fnom.config(bg="white")
        # except ValueError:
        #     entry_fnom.config(bg="red")
        #     adicionar_mensagem(label_fnom.cget("text") + " ENTRADA INVALIDA!")
        #     a += 1

        try:
            valor = (entry_P.get())
            valor = valor.replace(",", ".")
            entry_P.delete(0, tk.END)
            entry_P.insert(0, valor)
            valor = float(entry_P.get())
            entry_P.config(bg="white")
            if valor<=0:
                entry_P.config(bg="red")
                adicionar_mensagem(label_P.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_P.config(bg="red")
            adicionar_mensagem(label_P.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_V.get())
            valor = valor.replace(",", ".")
            entry_V.delete(0, tk.END)
            entry_V.insert(0, valor)
            valor = float(entry_V.get())
            entry_V.config(bg="white")
            if valor<=0:
                entry_V.config(bg="red")
                adicionar_mensagem(label_V.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_V.config(bg="red")
            adicionar_mensagem(label_V.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_In.get())
            valor = valor.replace(",", ".")
            entry_In.delete(0, tk.END)
            entry_In.insert(0, valor)
            valor = float(entry_In.get())
            entry_In.config(bg="white")
            if valor<=0:
                entry_In.config(bg="red")
                adicionar_mensagem(label_In.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_In.config(bg="red")
            adicionar_mensagem(label_In.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_vnom.get())
            valor = valor.replace(",", ".")
            entry_vnom.delete(0, tk.END)
            entry_vnom.insert(0, valor)
            valor = float(entry_vnom.get())
            entry_vnom.config(bg="white")
            if valor<=0:
                entry_vnom.config(bg="red")
                adicionar_mensagem(label_vnom.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_vnom.config(bg="red")
            adicionar_mensagem(label_vnom.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_Tload.get())
            valor = valor.replace(",", ".")
            entry_Tload.delete(0, tk.END)
            entry_Tload.insert(0, valor)
            valor = float(entry_Tload.get())
            entry_Tload.config(bg="white")
            if valor<=0:
                entry_Tload.config(bg="red")
                adicionar_mensagem(label_Tload.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_Tload.config(bg="red")
            adicionar_mensagem(label_Tload.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_rs.get())
            valor = valor.replace(",", ".")
            entry_rs.delete(0, tk.END)
            entry_rs.insert(0, valor)
            valor = float(entry_rs.get())
            entry_rs.config(bg="white")
            if valor<=0:
                entry_rs.config(bg="red")
                adicionar_mensagem(label_rs.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_rs.config(bg="red")
            adicionar_mensagem(label_rs.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_xs.get())
            valor = valor.replace(",", ".")
            entry_xs.delete(0, tk.END)
            entry_xs.insert(0, valor)
            valor = float(entry_xs.get())
            entry_xs.config(bg="white")
            if valor<=0:
                entry_xs.config(bg="red")
                adicionar_mensagem(label_xs.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_xs.config(bg="red")
            adicionar_mensagem(label_xs.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_xm.get())
            valor = valor.replace(",", ".")
            entry_xm.delete(0, tk.END)
            entry_xm.insert(0, valor)
            valor = float(entry_xm.get())
            entry_xm.config(bg="white")
            if valor<=0:
                entry_xm.config(bg="red")
                adicionar_mensagem(label_xm.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_xm.config(bg="red")
            adicionar_mensagem(label_xm.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_xr.get())
            valor = valor.replace(",", ".")
            entry_xr.delete(0, tk.END)
            entry_xr.insert(0, valor)
            valor = float(entry_xr.get())
            entry_xr.config(bg="white")
            if valor<=0:
                entry_xr.config(bg="red")
                adicionar_mensagem(label_xr.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_xr.config(bg="red")
            adicionar_mensagem(label_xr.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_rr.get())
            valor = valor.replace(",", ".")
            entry_rr.delete(0, tk.END)
            entry_rr.insert(0, valor)
            valor = float(entry_rr.get())
            entry_rr.config(bg="white")
            if valor<=0:
                entry_rr.config(bg="red")
                adicionar_mensagem(label_rr.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_rr.config(bg="red")
            adicionar_mensagem(label_rr.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_j.get())
            valor = valor.replace(",", ".")
            entry_j.delete(0, tk.END)
            entry_j.insert(0, valor)
            valor = float(entry_j.get())
            entry_j.config(bg="white")
            if valor<=0:
                entry_j.config(bg="red")
                adicionar_mensagem(label_j.cget("text") + "Variable cannot be equal to or less than 0.")
                a += 1
        except ValueError:
            entry_j.config(bg="red")
            adicionar_mensagem(label_j.cget("text") + " INVALID INPUT!")
            a += 1

        if entry_part.get() != options_part[0] and entry_part.get() != options_part[1]:
            entry_part.set("ERRO")
            adicionar_mensagem("Starting type not accepted.")
            a += 1

        if entry_carga.get() != options_carga[0] and entry_carga.get() != options_carga[1] and entry_carga.get() != \
                options_carga[2]:
            entry_carga.set("ERRO")
            adicionar_mensagem("Load type not accepted.")
            a += 1

        if entry_part.get()==options_part[0]:
            try:
                valor = (entry_tp.get())
                valor = valor.replace(",", ".")
                entry_tp.delete(0, tk.END)
                entry_tp.insert(0, valor)
                valor = float(entry_tp.get())
                entry_tp.config(bg="white")
                if valor >= float(entry_tt.get()):
                    entry_tp.config(bg="yellow")
                    entry_tt.config(bg="yellow")
                    adicionar_mensagem(
                        "Since the startup time is equal to or greater than the total simulation time, the load and faults will not be applied.")
                    b += 1
                if valor<0:
                    entry_tp.delete(0, tk.END)
                    entry_tp.insert(0, 0)
                    entry_tp.config(bg="yellow")
                    adicionar_mensagem("Negative startup time changed to zero.")
                    b += 1
            except ValueError:
                entry_tp.config(bg="red")
                adicionar_mensagem(label_tp.cget("text") + " INVALID INPUT!")
                a += 1

        try:
            valor = (entry_pcarga.get())
            valor = valor.replace(",", ".")
            entry_pcarga.delete(0, tk.END)
            entry_pcarga.insert(0, valor)
            valor = float(entry_pcarga.get())
            entry_pcarga.config(bg="white")
            if not 0 <= valor <= 110:
                entry_pcarga.config(bg="red")
                adicionar_mensagem(label_pcarga.cget("text") + " Input out of the allowed range (between 0 and 110%).")
                a += 1
        except ValueError:
            entry_pcarga.config(bg="red")
            adicionar_mensagem(label_pcarga.cget("text") + " INVALID INPUT!")
            a += 1

        try:
            valor = (entry_jload.get())
            valor = valor.replace(",", ".")
            entry_jload.delete(0, tk.END)
            entry_jload.insert(0, valor)
            valor = float(entry_jload.get())
            entry_jload.config(bg="white")
            if valor<0:
                entry_jload.config(bg="red")
                adicionar_mensagem(label_jload.cget("text") + "Variable cannot be negative.")
                a += 1
        except ValueError:
            entry_jload.config(bg="red")
            adicionar_mensagem(label_jload.cget("text") + " INVALID INPUT!")
            a += 1

        # if entry_alim.get() != options_alim[0] and entry_alim.get() != options_alim[1]:
        #     entry_alim.set("ERRO")
        #     adicionar_mensagem("Tipo de alimentação não aceita")
        #     a += 1

        try:
            valor = (entry_f.get())
            valor = valor.replace(",", ".")
            entry_f.delete(0, tk.END)
            entry_f.insert(0, valor)
            valor = float(entry_f.get())
            entry_f.config(bg="white")
            if valor<=0:
                entry_f.config(bg="red")
                adicionar_mensagem(label_f.cget("text") + "Variable cannot be null or negative.")
                a += 1
        except ValueError:
            entry_f.config(bg="red")
            adicionar_mensagem(label_f.cget("text") + " INVALID INPUT!")
            a += 1
        # if entry_fpwm.cget("state") == "normal":
        #     try:
        #         valor = (entry_fpwm.get())
        #         valor = valor.replace(",", ".")
        #         entry_fpwm.delete(0, tk.END)
        #         entry_fpwm.insert(0, valor)
        #         valor = float(entry_fpwm.get())
        #         entry_fpwm.config(bg="white")
        #         if valor * 20 > float(entry_dt.get()):
        #             entry_fpwm.config(bg="yellow")
        #             entry_dt.config(bg="yellow")
        #             entry_dt.delete(0, tk.END)
        #             entry_dt.insert(0, str(valor * 20))
        #             adicionar_mensagem(
        #                 "Para o funcionamento correto do PWM, a frequência de amostragem precisa ser, no mínimo, 20 vezes maior que a frequência do inversor. A amostragem foi atualizada automaticamente. ")
        #             b += 1
        #     except ValueError:
        #         entry_fpwm.config(bg="red")
        #         adicionar_mensagem(label_fpwm.cget("text") + " ENTRADA INVALIDA!")
        #         a += 1

        if estado_des.get():
            try:
                valor = (entry_desamp.get())
                valor = valor.replace(",", ".")
                entry_desamp.delete(0, tk.END)
                entry_desamp.insert(0, valor)
                valor = float(entry_desamp.get())
                entry_desamp.config(bg="white")
                if valor <= 0:
                    entry_desamp.config(bg="red")
                    adicionar_mensagem(label_desamp.cget("text") + " Variable cannot be null or negative.")
                    a+=1
                if 90 > valor > 110:
                    entry_desamp.config(bg="red")
                    adicionar_mensagem(label_desamp.cget("text") + " Variable out of limit (±10%).")
                    a+=1
            except ValueError:
                entry_desamp.config(bg="red")
                adicionar_mensagem(label_desamp.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_desang.get())
                valor = valor.replace(",", ".")
                entry_desang.delete(0, tk.END)
                entry_desang.insert(0, valor)
                valor = float(entry_desang.get())
                entry_desang.config(bg="white")
                if -30 > valor > 30:
                    entry_desang.config(bg="red")
                    adicionar_mensagem(label_desang.cget("text") + " Variable out of limit (±30º]).")
                    a += 1
            except ValueError:
                entry_desang.config(bg="red")
                adicionar_mensagem(label_desang.cget("text") + " INVALID INPUT!")
                a += 1

        if estado_curto.get():
            try:
                valor = (entry_mi.get())
                valor = valor.replace(",", ".")
                entry_mi.delete(0, tk.END)
                entry_mi.insert(0, valor)
                valor = float(entry_mi.get())
                entry_mi.config(bg="white")
                if not 0 <= valor <= 100:
                    entry_mi.config(bg="red")
                    adicionar_mensagem(label_mi.cget("text") + " Input out of the allowed range (between 0 and 100%).")
                    a += 1
            except ValueError:
                entry_mi.config(bg="red")
                adicionar_mensagem(label_mi.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_rf.get())
                valor = valor.replace(",", ".")
                entry_rf.delete(0, tk.END)
                entry_rf.insert(0, valor)
                valor = float(entry_rf.get())
                entry_rf.config(bg="white")
                if valor < 0.5:
                    entry_rf.config(bg="red")
                    adicionar_mensagem(label_rf.cget("text") + " Input out of the allowed range (greater than 0.5).")
                    a += 1
            except ValueError:
                entry_rf.config(bg="red")
                adicionar_mensagem(label_rf.cget("text") + " INVALID INPUT!")
                a += 1

        if estado_barra.get():
            try:
                valor = (entry_n.get())
                valor = valor.replace(",", ".")
                entry_n.delete(0, tk.END)
                entry_n.insert(0, valor)
                valor = float(entry_n.get())
                valor = int(valor)
                entry_n.delete(0, tk.END)
                entry_n.insert(0, str(valor))
                entry_n.config(bg="white")
                if valor <= 0:
                    entry_n.config(bg="red")
                    adicionar_mensagem(label_n.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_n.config(bg="red")
                adicionar_mensagem(label_n.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_nbq.get())
                valor = valor.replace(",", ".")
                entry_nbq.delete(0, tk.END)
                entry_nbq.insert(0, valor)
                valor = float(entry_nbq.get())
                valor = int(valor)
                entry_nbq.delete(0, tk.END)
                entry_nbq.insert(0, str(valor))
                entry_nbq.config(bg="white")
                if int(entry_nbq.get()) >= int(entry_n.get()):
                    entry_nbq.config(bg="red")
                    entry_n.config(bg="red")
                    adicionar_mensagem(label_nbq.cget("text") + " greater than or equal to. " + label_n.cget("text"))
                    a += 1
                if valor < 0:
                    entry_nbq.config(bg="red")
                    adicionar_mensagem(label_nbq.cget("text") + "Variable cannot be negative.")
                    a += 1
            except ValueError:
                entry_nbq.config(bg="red")
                adicionar_mensagem(label_nbq.cget("text") + " INVALID INPUT!")
                a += 1

            if entry_nivelbq.get() != options_nivelbq[0] and entry_nivelbq.get() != options_nivelbq[1] and entry_nivelbq.get() != \
                    options_nivelbq[2]:
                entry_nivelbq.set("ERRO")
                adicionar_mensagem("Bar breakage level not accepted.")
                a += 1

        if estado_mec.get():
            try:
                valor = (entry_Tfalha.get())
                valor = valor.replace(",", ".")
                entry_Tfalha.delete(0, tk.END)
                entry_Tfalha.insert(0, valor)
                valor = float(entry_Tfalha.get())
                entry_Tfalha.config(bg="white")
                if not 0 <= valor <= 100:
                    entry_Tfalha.config(bg="red")
                    adicionar_mensagem(label_Tfalha.cget("text") + " Input out of the allowed range (between 0 and 100%).")
                    a += 1
            except ValueError:
                entry_Tfalha.config(bg="red")
                adicionar_mensagem(label_Tfalha.cget("text") + " INVALID INPUT!")
                a += 1

        if a == 0 and b == 0:
            jerro.destroy()
            selectvar()
            return
        elif b != 0:
            selectvar()
            return
        else:
            return

    # ----------------------------------Seletor de Variáveis------------------------------#
    def selectvar():  #Essa função tem que chamar a simulador, depois
        def varesc():
            var = np.zeros(7, dtype=bool)
            if select_V.get():
                var[0] = True
            if select_Is.get():
                var[1] = True
            if select_Ir.get():
                var[2] = True
            if select_Fs.get():
                var[3] = True
            if select_Fr.get():
                var[4] = True
            if select_Te.get():
                var[5] = True
            if select_vel.get():
                var[6] = True
            jvar.destroy()
            simulador(var)
            return

        def manter_marcado():
            var.set(1)

        var = tk.IntVar(value=1)

        jvar = tk.Toplevel(j1)
        jvar.title("Variables")

        frame_var = tk.Frame(jvar)
        frame_var.pack()

        label_var = tk.Label(frame_var, text="Select the variables that should be saved.", font=("Segoe UI", 14, "bold"))
        label_var.grid(row=1, columnspan=2)

        select_V = var
        box_V = tk.Checkbutton(frame_var, text="Supply voltage", variable=select_V, command=manter_marcado)
        box_V.select()
        box_V.grid(row=2, columnspan=2)

        select_Is = var
        box_Is = tk.Checkbutton(frame_var, text="Stator current", variable=select_Is, command=manter_marcado)
        box_Is.grid(row=3, columnspan=2)
        box_Is.select()

        select_Ir = tk.BooleanVar()
        box_Ir = tk.Checkbutton(frame_var, text="Rotor current", variable=select_Ir)
        box_Ir.grid(row=4, columnspan=2)

        select_Fs = tk.BooleanVar()
        box_Fs = tk.Checkbutton(frame_var, text="Stator electromagnetic flux", variable=select_Fs)
        box_Fs.grid(row=5, columnspan=2)

        select_Fr = tk.BooleanVar()
        box_Fr = tk.Checkbutton(frame_var, text="Rotor electromagnetic flux", variable=select_Fr)
        box_Fr.grid(row=6, columnspan=2)

        select_Te = tk.BooleanVar()
        box_Te = tk.Checkbutton(frame_var, text="Electromagnetic torque", variable=select_Te)
        box_Te.grid(row=7, columnspan=2)
        box_Te.select()

        select_vel = tk.BooleanVar()
        box_vel = tk.Checkbutton(frame_var, text="Motor speed", variable=select_vel)
        box_vel.grid(row=8, columnspan=2)
        box_vel.select()

        var_botao = tk.Button(frame_var, text="Select", command=varesc, font=("Segoe UI", 12), width=8)
        var_botao.grid(row=15, columnspan=2)


    def simulador(var):
        global executando
        executando=True
        plt.close("all")
        #Pasta para salvar os resultados
        botao_play.pack_forget()
        botao_stop.pack(side=tk.LEFT, padx=10, pady=5)
        diretorio = filedialog.askdirectory()
        if diretorio == '':
            botao_stop.pack_forget()
            botao_play.pack(side=tk.LEFT, padx=10, pady=5)
            return
        # ----------------------------------Barra de Progresso------------------------------#
        progresso = ttk.Progressbar(frame_entradas, orient="horizontal", length=200, mode="determinate")
        progresso.grid(row=31, columnspan=8)
        agora = datetime.datetime.now()
        agora = str(agora)
        agora = re.sub(r"\s|\W+", "_", agora)[:-7]

        # diretorio = diretorio + "/MITSimulador_" + agora
        # os.makedirs(diretorio)

        #SIMULADOR
        #-------------------- FUNÇÃO ABC2DQ --------------------#
        def abc2dq(fa, fb, fc, teta):
            Fabc = np.array([[fa], [fb], [fc]])
            K = c23 * np.array([[np.cos(teta), np.cos(teta - ang120), np.cos(teta + ang120)],
                                [np.sin(teta), np.sin(teta - ang120), np.sin(teta + ang120)],
                                [0.5, 0.5, 0.5]])
            Fdq = K @ Fabc
            return (Fdq)

        #-------------------- FUNÇÃO DQ2ABC --------------------#
        def dq2abc(fq, fd, f0, teta):
            Fdq = np.array([[fq], [fd], [f0]])
            K = np.array([[np.cos(teta), np.sin(teta), 1],
                          [np.cos(teta - ang120), np.sin(teta - ang120), 1],
                          [np.cos(teta + ang120), np.sin(teta + ang120), 1]])
            Fabc = K @ Fdq
            return (Fabc)

        #-------------------- FUNÇÃO MATRIZ --------------------#
        def matriz(n, P):
            Tdq = np.zeros([n, n], dtype=float)
            Tdq[0, 0] = 1
            for i in range(1, n):
                Tdq[0, i] = np.cos(P / 2 * (-2 * np.pi * i / n))
                Tdq[1, i] = np.sin(P / 2 * (-2 * np.pi * i / n))
            T_aux = np.linalg.inv(Tdq[:2, :2]) @ (-Tdq[:2, 2:n])
            for i in range(2, n):
                Tdq[i, 0] = T_aux[0, i - 2]
                Tdq[i, 1] = T_aux[1, i - 2]
            Tdq[2:, 2:] = np.identity(n - 2)
            Tdq = (n - 1) * Tdq / n
            return Tdq

        #-------------------- FUNÇÃO RUNGE-KUTTA --------------------#
        def RK(u):
            du = np.zeros(7, dtype=float)
            Fqs = u[0]
            Fds = u[1]
            Fqr = u[2]
            Fdr = u[3]
            wr = u[4]
            F0s = u[5]
            Fas2 = u[6]

            du[0] = dt * (vq - rs * (a1 * Fqs - a2 * Fqr + c23mi * i_f) + c23mirs * i_f)
            du[1] = dt * (vd - rs * (a1 * Fds - a2 * Fdr))
            du[2] = dt * (-rr * (a4 * Fqr - a2 * Fqs) + wr * Fdr)
            du[3] = dt * (-rr * (a4 * Fdr - a2 * Fds) - wr * Fqr)
            du[4] = dt * ((Te - Tload) / J)
            du[5] = dt * (mirs3 * i_f)
            du[6] = dt * (vas2 - mirs * ((a1 * Fqs - a2 * Fqr + c23mi * i_f) - i_f))

            return (du)

        # -------------------- FUNÇÃO INVERSOR --------------------#
        # def IF(Va_ref, Vb_ref, Vc_ref, y):
        #     if Va_ref >= y:
        #         Sa = True
        #     else:
        #         Sa = False
        #     if Vb_ref >= y:
        #         Sb = True
        #     else:
        #         Sb = False
        #     if Vc_ref >= y:
        #         Sc = True
        #     else:
        #         Sc = False
        #     Va_teta = VDC * (Sa - (1 - Sa))
        #     Vb_teta = VDC * (Sb - (1 - Sb))
        #     Vc_teta = VDC * (Sc - (1 - Sc))
        #     M = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])
        #     M = M / 3
        #     V_teta = np.array([[Va_teta], [Vb_teta], [Vc_teta]])
        #     V = M @ V_teta
        #     Va = V[0, 0]
        #     Vb = V[1, 0]
        #     Vc = V[2, 0]
        #     return Va, Vb, Vc

        #-------------------- FUNÇÃO DBFFT --------------------#
        def dbfft(x, fs, win=None, ref=1):
            """
            Calculate spectrum in dB scale
            Args:
                x: input signal
                fs: sampling frequency
                win: vector containing window samples (same length as x).
                     If not provided, then rectangular window is used by default.
                ref: reference value used for dBFS scale. 32768 for int16 and 1 for float
            Returns:
                freq: frequency vector
                s_db: spectrum in dB scale
            """
            N = len(x)  # Length of input sequence
            if win is None:
                win = np.ones(N)
            if len(x) != len(win):
                raise ValueError('Signal and window must be of the same length')
            x = x * win
            # Calculate real FFT and frequency vector
            sp = np.fft.rfft(x)
            freq = np.arange((N / 2) + 1) / (float(N) / fs)

            # Scale the magnitude of FFT by window and factor of 2,
            # because we are using half of FFT spectrum.
            s_mag = np.abs(sp) * 2 / np.sum(win)

            # Convert to dBFS
            s_dbfs = 20 * np.log10(s_mag / ref)
            # s_dbfs = s_mag/ref

            if len(freq) > len(s_dbfs):
                freq = freq[:len(s_dbfs)]
            if len(s_dbfs) > len(freq):
                s_dbfs = s_dbfs[:len(freq)]

            return freq, s_dbfs

        #-------------------- ENTRADAS --------------------#
        #TEMPO
        famos = float(entry_dt.get())
        dt = 1 / famos  #Passo
        tfinal = float(entry_tt.get())  #Tempo de simulação

        #DADOS DO MOTOR
        # fnom = float(entry_fnom.get())  #Frequência da rede
        P = float(entry_P.get())  #Número de polos
        V = float(entry_V.get())  #Tensão de linha nominal
        v_nom = float(entry_vnom.get())  #Velocidade nominal
        Tload_max = float(entry_Tload.get())  #Carga nominal
        rs = float(entry_rs.get())  #Resistência do estator
        Lls = float(entry_xs.get())  #Reatância do estator
        Lm = float(entry_xm.get())  #Reatância mútua
        Llr = float(entry_xr.get())  #Reatância do rotor
        rr = float(entry_rr.get())  #Resistência do rotor
        J_nom = float(entry_j.get())  #Momento de inércia do motor
        In= float(entry_In.get()) #Corrente nominal

        #CARGA
        if entry_part.get() == options_part[0]:
            tp = float(entry_tp.get())  # Tempo de partida
            tipo_part = 0
        elif entry_part.get() == options_part[1]:
            tipo_part = 1
            tp = 0
            if entry_carga.get() == options_carga[0]:
                tipo_carga = 0
            elif entry_carga.get() == options_carga[1]:
                tipo_carga = 1
            elif entry_carga.get() == options_carga[2]:
                tipo_carga = 2
        pcarga = float(entry_pcarga.get()) / 100  # Porcentagem de carga
        J_load = float(entry_jload.get())  # Momento de inércia da carga

        #ALIMENTAÇÃO
        # if entry_alim.get() == options_alim[0]:
        #     tipo_alim = 0
        # elif entry_alim.get() == options_alim[1]:
        #     tipo_alim = 1
        #     f_triang = float(entry_fpwm.get())
        tipo_alim = 0
        f = float(entry_f.get())

        #DESEQUELÍBRIO DE FASES
        if estado_des.get():
            deseqamp = float(entry_desamp.get()) / 100
            deseqang = float(entry_desang.get())
        else:
            deseqamp = 1  #Desequilíbrio do módulo da fase a
            deseqang = 0  #Desequilíbrio do ângulo da fase a
        deseqang = deseqang * np.pi / 180

        #CURTO NAS ESPIRAS
        if estado_curto.get():
            mi_ = float(entry_mi.get()) / 100
            nrf = float(entry_rf.get())
        else:
            mi_ = 0
            rf=0

        #BARRAS QUEBRADAS
        if estado_barra.get():
            n = int(entry_n.get())
            nbq_ = int(entry_nbq.get())
            nivelbq = entry_nivelbq.get()
        else:
            n = 28  #Número de barras (Aproximado)
            nbq_ = 0  #Número de barras quebradas
            nivelbq = 3  #Nível do rompimento (1- rachadura (10%), 2- metade(50%), 3- completa(100%))
        if nivelbq == "Crack (10%)":
            nivelbq = 1
        elif nivelbq == "Fracture (50%)":
            nivelbq = 2
        elif nivelbq == "Break (100%)":
            nivelbq = 3

        #FALHAS MECÂNICAS
        if estado_mec.get():
            T_falha_nom = float(entry_Tfalha.get())/100 * Tload_max * pcarga
        else:
            T_falha_nom = 0.0  #Falhas mecânicas

        # -------------------- CÁLCULOS --------------------#
        t = np.arange(dt, tfinal, dt)
        Vmax = V * np.sqrt(2)/np.sqrt(3)
        J_nom = J_nom * 2 / P
        we = 2 * np.pi * f
        baldefnom=v_nom*P/120
        if baldefnom>50:
            fnom=60
        else:
            fnom=50
        v_nom = f * v_nom / fnom

        # Cálculo de Rf
        if estado_curto.get():
            In =nrf * In * np.sqrt(2)
            Zeq=mi_*Vmax/In
            Rquad=Zeq**2-(mi_*Lls)**2
            if Rquad<0:
                rf=0
            else:
                Req=np.sqrt(Rquad)
                rf = Req - mi_ * rs
                if rf<0:
                    rf=0
            # print(In)
            # print(rf)

        Lls = Lls / we
        Llr = Llr / we
        Lm = Lm / we
        Ls = Lls + Lm
        Lr = Llr + Lm
        a1 = Lr / (Ls * Lr - Lm ** 2)
        a2 = Lm / (Ls * Lr - Lm ** 2)
        a4 = Ls / (Ls * Lr - Lm ** 2)
        Kvel = 60 * (2 / P) / (2 * np.pi)
        K_linear = pcarga * Tload_max * 2 / (v_nom * 2 * np.pi * P / 60)
        K_quad = pcarga * Tload_max * 4 / (v_nom * 2 * np.pi * P / 60) ** 2

        # IF
        # if tipo_alim == 1:
        #     VDC = 1.35 * V * np.sqrt(3) / 2
        #     triang = 2 * np.abs(2 * (t * f_triang - np.floor(0.5 + t * f_triang))) - 1
        #     triang = VDC * triang

        # COORDENADAS DQ
        # wplano=0;
        teta = 0

        # CONSTANTES
        ang120 = np.pi * 2 / 3
        c23 = 2 / 3
        aux_mec = v_nom * 2 * np.pi / 60
        auxT = 3 * P * Lm / 4
        aux_Tv = 3 * P / 4
        aux_Tc = 3 * P * Lm / (4 * Lr)

        # INICIANDO VALORES
        j = 1
        # header = "t,Ias,Ibs,Ics,Iar,Ibr,Icr,Te,Vel,Va,Vb,Vc,If"
        header = "t"
        if var[0]:
            V_index = j
            header += ",Va,Vb,Vc"
            j += 3
        if var[1]:
            Is_index = j
            header += ",Ias,Ibs,Ics"
            j += 3
        if var[2]:
            Ir_index = j
            header += ",Iar,Ibr,Icr"
            j += 3
        if var[3]:
            Fs_index = j
            header += ",Fas,Fbs,Fcs"
            j += 3
        if var[4]:
            Fr_index = j
            header += ",Far,Fbr,Fcr"
            j += 3
        if var[5]:
            Te_index = j
            header += ",Te"
            j += 1
        if var[6]:
            vel_index = j
            header += ",Vel"
            j += 1
        if mi_ > 0:
            If_index = j
            header += ",If"
            j += 1
        Z = np.zeros([j, t.shape[0]], dtype=float)
        Tv = np.zeros(len(t), dtype=float)
        Tc = np.zeros(len(t), dtype=float)
        tetar = 0
        Te = 0
        u = np.zeros(7, dtype=float)
        k = 0
        c_t = 0
        i_f = 0
        pos = 0
        pos_ant = 0
        w_ant = 0
        wr = 0
        aux_barra = np.zeros([n - 2, 1])
        Tdq = matriz(n, P)

        vas2 = 0
        # -------------------- SIMULAÇÃO --------------------#
        for i in t:
            if not executando:
                progresso.destroy()
                return
            if tipo_part == 0:
                if i < tp and c_t == 0:
                    Tload = 0
                    J = J_nom
                    mi = 0
                    nbq = 0
                    T_falha = 0
                    c_t = 1

                    c23mi = c23 * mi
                    c23mirs = c23 * mi * rs
                    mirs = mi * rs
                    mirs3 = mi * rs / 3
                    auxT_mi = P * mi * Lm / 2
                elif i >= tp and c_t == 1:
                    Tload = pcarga * Tload_max
                    J = J_nom + J_load
                    mi = mi_
                    nbq = nbq_
                    c_t = 2

                    c23mi = c23 * mi
                    c23mirs = c23 * mi * rs
                    mirs = mi * rs
                    mirs3 = mi * rs / 3
                    auxT_mi = P * mi * Lm / 2
                    if mi > 0:
                        miLs_if = mi * Ls
                        miLm_if = mi * Lm
                        den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
            elif tipo_part == 1:
                if tipo_carga == 0 and c_t == 0:
                    Tload = pcarga * Tload_max
                    J = J_nom + J_load
                    mi = mi_
                    nbq = nbq_
                    c_t = 2

                    c23mi = c23 * mi
                    c23mirs = c23 * mi * rs
                    mirs = mi * rs
                    mirs3 = mi * rs / 3
                    auxT_mi = P * mi * Lm / 2
                    if mi > 0:
                        miLs_if = mi * Ls
                        miLm_if = mi * Lm
                        den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
                elif tipo_carga == 1:
                    Tload = K_linear * wr
                    if c_t == 0:
                        J = J_nom + J_load
                        mi = mi_
                        nbq = nbq_
                        c_t = 2

                        c23mi = c23 * mi
                        c23mirs = c23 * mi * rs
                        mirs = mi * rs
                        mirs3 = mi * rs / 3
                        auxT_mi = P * mi * Lm / 2
                        if mi > 0:
                            miLs_if = mi * Ls
                            miLm_if = mi * Lm
                            den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
                elif tipo_carga == 2:
                    Tload = K_quad * wr ** 2
                    if c_t == 0:
                        J = J_nom + J_load
                        mi = mi_
                        nbq = nbq_
                        c_t = 2

                        c23mi = c23 * mi
                        c23mirs = c23 * mi * rs
                        mirs = mi * rs
                        mirs3 = mi * rs / 3
                        auxT_mi = P * mi * Lm / 2
                        if mi > 0:
                            miLs_if = mi * Ls
                            miLm_if = mi * Lm
                            den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)

            # FALHA MECÂNICA
            if T_falha_nom > 0 and c_t == 2:
                T_falha = T_falha_nom * np.sin(aux_mec * i)
                Tload = Tload_max + T_falha

            # SINAIS DE TENSÃO
            if tipo_alim == 0:
                va = deseqamp * Vmax * np.cos(we * i + deseqang)
                vb = Vmax * np.cos(we * i - ang120)
                vc = (-(va + vb))
                # vc = Vmax * np.cos(we * i + ang120)
            # elif tipo_alim == 1:
            #     va_ref = deseqamp * Vmax * np.cos(we * i + deseqang)
            #     vb_ref = Vmax * np.cos(we * i - ang120)
            #     vc_ref = (-(va_ref + vb_ref))
            #     vaux = [va_ref, vb_ref, vc_ref]
            #     v0 = -0.5 * (max(vaux) + min(vaux))
            #     va_ref += v0
            #     vb_ref += v0
            #     vc_ref += v0
            #     va, vb, vc = IF(va_ref, vb_ref, vc_ref, triang[k])

            Vqd = abc2dq(va, vb, vc, teta)
            vq = Vqd[0, 0]
            vd = Vqd[1, 0]
            # v0=Vqd[2,0]
            vas2 = rf * i_f

            # RUNGE-KUTTA
            du1 = RK(u)
            du2 = RK(u + du1 / 2)
            du3 = RK(u + du2 / 2)
            du4 = RK(u + du3)
            u = u + (du1 + 2 * du2 + 2 * du3 + du4) / 6
            Fqs = u[0]
            Fds = u[1]
            Fqr = u[2]
            Fdr = u[3]
            wr = u[4]
            # F0s=u[5]
            Fas2 = u[6]

            # CORRENTES
            iqs = a1 * Fqs - a2 * Fqr + c23mi * i_f
            ids = a1 * Fds - a2 * Fdr
            # ids=a1*Fds-a2*Fdr
            iqr = a4 * Fqr - a2 * Fqs
            idr = a4 * Fdr - a2 * Fds
            if mi > 0:
                i_f = (-Fas2 + miLs_if * (iqs) + miLm_if * ((iqr))) / den_if

            # BARRAS QUEBRADAS
            tetar = (tetar + wr * dt) % (2 * np.pi)
            aux1 = np.cos(tetar)
            aux2 = np.sin(tetar)
            iqs_r = iqs * aux1 - ids * aux2
            ids_r = iqs * aux2 + ids * aux1
            # aux1 = np.cos(-tetar)
            # aux2 = np.sin(-tetar)
            Fqr_r = Fqr * aux1 - Fdr * aux2
            Fdr_r = Fqr * aux2 + Fdr * aux1
            if nbq > 0:
                iqr_r = iqr * aux1 - idr * aux2
                idr_r = iqr * aux2 + idr * aux1
                Irn = np.linalg.inv(Tdq) @ np.concatenate((np.array([[iqr_r], [idr_r]]), aux_barra))
                media = sum(Irn[2:nbq + 3, 0]) / (nbq + 1)
                dif = media - Irn[2:nbq + 3, 0]
                if nivelbq == 1:  # 10%
                    Irn[2:nbq + 3, 0] += dif * 0.1
                if nivelbq == 2:  # 50%
                    Irn[2:nbq + 3, 0] += dif * 0.5
                if nivelbq == 3:  # 100%
                    Irn[2:nbq + 3, 0] = np.ones(nbq + 1) * media

                Ir = Tdq @ Irn
                idr_r = Ir[1, 0]
                iqr_r = Ir[0, 0]
                iqr = iqr_r * aux1 + idr_r * aux2
                idr = -iqr_r * aux2 + idr_r * aux1

            # pos = (w_ant + wr) * dt / 2 + pos_ant
            # w_ant = wr
            # pos_ant = pos

            # TRANSFORMAÇÂO DAS CORRENTES
            Iabcs = dq2abc(iqs, ids, 0, teta)
            if var[2]:
                Iabcr = dq2abc(iqr, idr, 0, teta - tetar)

            # Transformação dos Fluxos
            if var[3]:
                Fabcs = dq2abc(Fqs, Fds, 0, teta)
            if var[4]:
                Fabcr = dq2abc(Fqr, Fdr, 0, teta)

            # VELOCIDADE DO MOTOR
            vel = wr * Kvel

            # TORQUE ELETROMAGNÉTICO
            Te = auxT * (iqs * idr - ids * iqr) - auxT_mi * i_f * idr
            Tv[k] = aux_Tv * (Fds * iqs - Fqs * ids)
            # Tc[k] = aux_Tc*(Fdr_r * iqs_r - Fqr_r * ids_r)
            Tc[k] = Te

            # ARMAZENAMENTO
            j = 1
            Z[0, k] = i
            if var[0]:
                Z[j, k] = va
                Z[j + 1, k] = vb
                Z[j + 2, k] = vc
                j += 3
            if var[1]:
                Z[j, k] = float(Iabcs[0, 0])
                Z[j + 1, k] = float(Iabcs[1, 0])
                Z[j + 2, k] = float(Iabcs[2, 0])
                j += 3
            if var[2]:
                Z[j, k] = float(Iabcr[0, 0])
                Z[j + 1, k] = float(Iabcr[1, 0])
                Z[j + 2, k] = float(Iabcr[2, 0])
                j += 3
            if var[3]:
                Z[j, k] = float(Fabcs[0, 0])
                Z[j + 1, k] = float(Fabcs[1, 0])
                Z[j + 2, k] = float(Fabcs[2, 0])
                j += 3
            if var[4]:
                Z[j, k] = float(Fabcr[0, 0])
                Z[j + 1, k] = float(Fabcr[1, 0])
                Z[j + 2, k] = float(Fabcr[2, 0])
                j += 3
            if var[5]:
                Z[j, k] = Te
                j += 1
            if var[6]:
                Z[j, k] = vel
                j += 1
            if mi_ > 0:
                Z[j, k] = i_f

            # Z[0,k]=Iabcs[0]
            # Z[1,k]=Iabcs[1]
            # Z[2,k]=Iabcs[2]
            # Z[3,k]=Iabcr[0]
            # Z[4,k]=Iabcr[1]
            # Z[5,k]=Iabcr[2]
            # Z[6,k]=Te
            # Z[7,k]=vel
            # Z[8,k]=va
            # Z[9,k]=vb
            # Z[10,k]=vc
            # Z[11,k]=i_f
            k = k + 1

            barra = i / tfinal * 100
            progresso["value"] = barra
            frame_entradas.update()

        plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 24})
        plt.rcParams['lines.linewidth'] = 1
        plt.rcParams.update({
            'axes.grid': True,  # Ativa a grade principal
            'grid.color': 'gray',  # Cor da grade
            'grid.linestyle': '--',  # Estilo da linha da grade
            'grid.alpha': 0.7,  # Transparência da grade
            'grid.linewidth': 0.8,  # Largura da linha da grade
        })
        if var[6]:
            plt.figure(1)
            plt.plot(t, Z[vel_index, :])
            plt.title("Motor speed")
            plt.ylabel("Speed (rpm)")
            plt.xlabel("Time (s)")

        if var[5]:
            plt.figure(2)
            plt.plot(t, Z[Te_index, :])
            plt.title("Electromagnetic torque")
            plt.ylabel("Electromagnetic torque (Nm)")
            plt.xlabel("Time (s)")

        if var[5] and var[6]:
            plt.figure(3)
            plt.plot(Z[vel_index, :], Z[Te_index, :])
            plt.title("Electromagnetic torque as a function of speed")
            plt.ylabel("Electromagnetic torque (Nm)")
            plt.xlabel("Speed (rpm)")

        if var[4]:
            plt.figure(4)
            plt.plot(t, Z[Fr_index, :], t, Z[Fr_index + 1, :], t, Z[Fr_index + 2, :])
            plt.title("Rotor electromagnetic flux")
            plt.ylabel("Flux")
            plt.xlabel("Time (s)")
            plt.legend(["Phase A", "Phase B", "Phase C"])

        if var[3]:
            plt.figure(5)
            plt.plot(t, Z[Fs_index, :], t, Z[Fs_index + 1, :], t, Z[Fs_index + 2, :])
            plt.title("Stator electromagnetic flux")
            plt.ylabel("Flux")
            plt.xlabel("Time (s)")
            plt.legend(["Phase A", "Phase B", "Phase C"])

        if var[2]:
            plt.figure(6)
            plt.plot(t, Z[Ir_index, :], t, Z[Ir_index + 1, :], t, Z[Ir_index + 2, :])
            plt.title("Rotor Currents")
            plt.ylabel("Current (A)")
            plt.xlabel("Time (s)")
            plt.legend(["Phase A", "Phase B", "Phase C"])

        if tp <= 0.75 * tfinal:
            if tp==0:
                tp=tfinal/3
            contador = 0
            Ip_ant = 0
            global aux_fft
            for i in range(int(tp / dt), np.size(t)):
                if i == np.size(t) - 1:
                    aux_fft = 0
                    break
                if Z[Is_index, i - 1] < Z[Is_index, i] and Z[Is_index, i + 1] < Z[Is_index, i]:
                    if Z[Is_index, i] > Ip_ant * 0.99 and Z[Is_index, i] < Ip_ant * 1.01:
                        contador += 1
                        Ip_ant = Z[Is_index, i]
                    else:
                        Ip_ant = Z[Is_index, i]
                    if contador == 10:
                        aux_fft = i
                        break

            if aux_fft > 0:
                # plt.figure(5, figsize=(19.2, 10.8))
                plt.figure(7)
                y = Z[Is_index, aux_fft:]
                N = y.shape[0]
                win = np.hanning(N)
                [freq, y] = dbfft(y, 1 / (dt), win=win)
                plt.plot(freq, y)
                plt.xlim(0, 200)
                plt.ylim(-70, 45)
                plt.title("FFT of the stator phase A current")
                plt.ylabel("Current (dB)")
                plt.xlabel("Frequency (Hz)")

                # jfalha = tk.Toplevel()
                # jfalha.title("Indicadores de Falha")
                # texto = tk.Text(jfalha, wrap="word", state=tk.DISABLED)
                # texto.pack(fill=tk.BOTH, expand=True)
                #
                # def adicionar_mensagem(mensagem):
                #     texto.config(state=tk.NORMAL)
                #     texto.insert(tk.END, mensagem + "\n")
                #     texto.config(state=tk.DISABLED)
                #     texto.see(tk.END)
                #
                # # -------------------Detecção de Falha Mecânica-------------------#
                # freq_mec = f - vel / f
                # mec_db = -99999
                # for i in range(len(y)):
                #     if y[i] > mec_db and (freq_mec - 10) < freq[i] < (freq_mec + 10):
                #         mec_db = y[i]
                # adicionar_mensagem("Componente da Falha Mecânica: " + str(round(mec_db, 4)) + " dB")
                #
                # # -------------------Detecção de Curto Circuito-------------------#
                # if deseqang != 0 or deseqamp != 1:
                #     wplano = -f * 2 * np.pi
                #     teta = 0
                #     Va = Z[V_index, :]
                #     Vb = Z[V_index + 1, :]
                #     Vc = Z[V_index + 2, :]
                #     Ia = Z[Is_index, :]
                #     Ib = Z[Is_index + 1, :]
                #     Ic = Z[Is_index + 2, :]
                #     Vqd = np.zeros([2, len(Va)], dtype=float)
                #     Iqd = np.zeros([2, len(Ia)], dtype=float)
                #     for i in range(len(Ia)):
                #         Iq, Id, I0 = abc2dq(Ia[i], Ib[i], Ic[i], teta)
                #         Vq, Vd, V0 = abc2dq(Va[i], Vb[i], Vc[i], teta)
                #         teta = (teta + wplano * dt) % (2 * np.pi)
                #         Iqd[0, i] = Iq[0]
                #         Iqd[1, i] = Id[0]
                #         Vqd[0, i] = Vq[0]
                #         Vqd[1, i] = Vd[0]
                #     Iq = np.mean(Iqd[0, :])
                #     Id = np.mean(Iqd[1, :])
                #     Vq = np.mean(Vqd[0, :])
                #     Vd = np.mean(Vqd[1, :])
                #     Is = np.sqrt(Iq ** 2 + Id ** 2)
                #     Vs = np.sqrt(Vq ** 2 + Vd ** 2)
                #     Zn = Vs / Is
                #     adicionar_mensagem("Impedância Negativa: " + str(round(Zn, 4)) + " Ohms")
                #
                # # -------------------Detecção de Barras Quebradas-------------------#
                # f_amos = 1 / dt
                # cutoff = 12
                # ordem = 5
                # nyq = 0.5 * f_amos
                # normal_cutoff = cutoff / nyq
                # b, a = butter(ordem, normal_cutoff, btype='low', analog=False)
                # dT = Tv[aux_fft:] - Tc[aux_fft:]
                # dT = filtfilt(b, a, dT)
                # dT_aux = int(len(dT) * 0.1)
                # dT = dT[dT_aux:-dT_aux]
                # # plt.figure(21)
                # # plt.plot(Tv[aux_fft:])
                # # plt.plot(Tc[aux_fft:])
                # # plt.plot(dT)
                # # plt.figure(22)
                # # y = dT
                # # N = y.shape[0]
                # # win = np.hanning(N)
                # # [freq, y] = dbfft(y, 1 / (dt), win=win)
                # # plt.plot(freq, y)
                # # plt.xlim(0, 200)
                # # plt.ylim(-70, 45)
                # # plt.title("FFT do resíduo do conjugado")
                # # plt.ylabel("Conjugado (dB)")
                # # plt.xlabel("Frequência (Hz)")
                # rc = (max(dT) - min(dT)) / 2
                # adicionar_mensagem("Resíduo do Conjugado: " + str(round(rc, 4)) + " Nm")

        if mi_ > 0:
            plt.figure(8)
            plt.plot(t, Z[If_index, :])
            plt.title("Fault current")
            plt.ylabel("Current (A)")
            plt.xlabel("Time (s)")

        if var[1]:
            plt.figure(9)
            plt.plot(t, Z[Is_index, :], t, Z[Is_index + 1, :], t, Z[Is_index + 2, :])
            plt.title("Stator current")
            plt.ylabel("Current (A)")
            plt.xlabel("Time (s)")
            plt.legend(["Phase A", "Phase B", "Phase C"])

        if var[0]:
            plt.figure(10)
            plt.plot(t, Z[V_index, :], t, Z[V_index + 1, :], t, Z[V_index + 2, :])
            plt.title("Supply voltage")
            plt.ylabel("Voltage (V)")
            plt.xlabel("Time (s)")
            plt.legend(["Phase A", "Phase B", "Phase C"])

        plt.show(block=False)

        dados = np.transpose(Z)
        #header="t,Ias,Ibs,Ics,Iar,Ibr,Icr,Te,Vel,Va,Vb,Vc,If"
        np.savetxt(diretorio + "/" + agora + "_Output.txt", dados, delimiter=',', header=header)

        progresso.destroy()
        botao_stop.pack_forget()
        botao_play.pack(side=tk.LEFT, padx=10, pady=5)
        executando=False

    def parar_simu():
        global executando
        botao_stop.pack_forget()
        botao_play.pack(side=tk.LEFT, padx=10, pady=5)
        executando=False

    #----------------------------------Botão de Abrir------------------------------#
    def open_data():
        diretorio = filedialog.askopenfilename()
        if diretorio == "":
            return
        with open(diretorio, "r") as arquivo:
            abrir = arquivo.readlines()
        for i in range(abrir.__len__()):
            abrir[i] = abrir[i][:-1]

        entry_dt.delete(0, tk.END)
        entry_dt.insert(0, float(abrir[0]))
        entry_tt.delete(0, tk.END)
        entry_tt.insert(0, float(abrir[1]))

        entry_f.delete(0, tk.END)
        entry_f.insert(0, float(abrir[2]))
        entry_P.delete(0, tk.END)
        entry_P.insert(0, float(abrir[3]))
        entry_V.delete(0, tk.END)
        entry_V.insert(0, float(abrir[4]))
        entry_vnom.delete(0, tk.END)
        entry_vnom.insert(0, float(abrir[5]))
        entry_Tload.delete(0, tk.END)
        entry_Tload.insert(0, float(abrir[6]))
        entry_rs.delete(0, tk.END)
        entry_rs.insert(0, float(abrir[7]))
        entry_xs.delete(0, tk.END)
        entry_xs.insert(0, float(abrir[8]))
        entry_xm.delete(0, tk.END)
        entry_xm.insert(0, float(abrir[9]))
        entry_xr.delete(0, tk.END)
        entry_xr.insert(0, float(abrir[10]))
        entry_rr.delete(0, tk.END)
        entry_rr.insert(0, float(abrir[11]))
        entry_j.delete(0, tk.END)
        entry_j.insert(0, float(abrir[12]))
        entry_jload.delete(0, tk.END)
        entry_jload.insert(0, float(abrir[13]))
        entry_In.delete(0, tk.END)
        entry_In.insert(0, float(abrir[14]))

    #----------------------------------Botão de Salvar------------------------------#
    def save_data():
        diretorio = tk.filedialog.asksaveasfilename(defaultextension=".txt")
        if diretorio == '':
            return
        salvar = []
        #TEMPO
        salvar.append(str(entry_dt.get()))
        salvar.append(str(entry_tt.get()))
        #DADOS DO MOTOR
        salvar.append(str(entry_f.get()))
        salvar.append(str(entry_P.get()))
        salvar.append(str(entry_V.get()))
        salvar.append(str(entry_vnom.get()))
        salvar.append(str(entry_Tload.get()))
        salvar.append(str(entry_rs.get()))
        salvar.append(str(entry_xs.get()))
        salvar.append(str(entry_xm.get()))
        salvar.append(str(entry_xr.get()))
        salvar.append(str(entry_rr.get()))
        salvar.append(str(entry_j.get()))
        salvar.append(str(entry_jload.get()))
        salvar.append(str(entry_In.get()))
        for i in range(salvar.__len__()):
            if salvar[i] == '':
                salvar[i] = "0"

        with open(diretorio, "w") as arquivo:
            for elemento in salvar:
                arquivo.write(str(elemento) + "\n")

    # ----------------------------------Estimador de Parâmetros------------------------------#
    def estimparamcat():
        # ----------------------------------JANELA 2------------------------------#
        j2 = tk.Toplevel(j1)
        j2.title("Parameter Estimator")
        j2.option_add("*Font", ("Segoe UI", 11))

        frame_estim = tk.Frame(j2)
        frame_estim.pack()

        # label_estim = tk.Label(frame_estim, text="Estimador de Parâmetros do MIT", font=("Segoe UI", 18, "bold"))
        # label_estim.grid(row=1, columnspan=4)

        # ----------------------------------DADOS DE CATÁLOGO------------------------------#
        label_dados = tk.Label(frame_estim, text="Motor Data ", font=("Segoe UI", 12, "bold"))
        label_dados.grid(row=2, columnspan=4, sticky=tk.W)

        label_Potn = tk.Label(frame_estim, text="Nominal power (HP):")
        label_Potn.grid(row=3, column=0, sticky=tk.W)
        entry_Potn = tk.Entry(frame_estim)
        entry_Potn.grid(row=3, column=1, sticky=tk.W + tk.E)

        label_Vn = tk.Label(frame_estim, text="  Nominal line voltage (V):")
        label_Vn.grid(row=3, column=2, sticky=tk.W)
        entry_Vn = tk.Entry(frame_estim)
        entry_Vn.grid(row=3, column=3, sticky=tk.W + tk.E)

        label_fn = tk.Label(frame_estim, text="Nominal frequency (Hz):")
        label_fn.grid(row=4, column=0, sticky=tk.W)
        entry_fn = tk.Entry(frame_estim)
        entry_fn.grid(row=4, column=1, sticky=tk.W + tk.E)

        label_Inc = tk.Label(frame_estim, text="  Nominal current (A):")
        label_Inc.grid(row=4, column=2, sticky=tk.W)
        entry_Inc = tk.Entry(frame_estim)
        entry_Inc.grid(row=4, column=3, sticky=tk.W + tk.E)

        label_Polos = tk.Label(frame_estim, text="Number of poles:")
        label_Polos.grid(row=5, column=0, sticky=tk.W)
        entry_Polos = tk.Entry(frame_estim)
        entry_Polos.grid(row=5, column=1, sticky=tk.W + tk.E)

        label_veln = tk.Label(frame_estim, text="  Nominal speed (rpm):")
        label_veln.grid(row=5, column=2, sticky=tk.W)
        entry_veln = tk.Entry(frame_estim)
        entry_veln.grid(row=5, column=3, sticky=tk.W + tk.E)

        def cat_select(event):
            selected_norma = entry_norma.get()
            entry_cat.config(values=options_cat[selected_norma])
            entry_cat.set(options_cat[selected_norma][0])

        options_cat = {
            "NEMA": ["A", "B", "C", "D"],
            "NBR": ["D", "N", "H"]}
        label_cat = tk.Label(frame_estim, text="Motor category:")
        label_cat.grid(row=6, column=0, sticky=tk.W)
        selected_norma = tk.StringVar(frame_estim)
        selected_cat = tk.StringVar(frame_estim)
        entry_norma = ttk.Combobox(frame_estim, values=list(options_cat.keys()), textvariable=selected_norma)
        entry_norma.bind("<<ComboboxSelected>>", cat_select)
        entry_norma.grid(row=6, column=1)
        entry_cat = ttk.Combobox(frame_estim, textvariable=selected_cat)
        entry_cat.grid(row=6, column=2,columnspan=2,sticky=tk.W)

        label_espaco = tk.Label(frame_estim, text=" ")
        label_espaco.grid(row=7, columnspan=4)

        label_carga = tk.Label(frame_estim, text="Load:")
        label_carga.grid(row=8, column=0, sticky=tk.W)
        label_50 = tk.Label(frame_estim, text="50%")
        label_50.grid(row=8, column=1)
        label_75 = tk.Label(frame_estim, text="75%")
        label_75.grid(row=8, column=2)
        label_100 = tk.Label(frame_estim, text="100%")
        label_100.grid(row=8, column=3)

        label_eff = tk.Label(frame_estim, text="Efficiency (%):")
        label_eff.grid(row=9, column=0, sticky=tk.W)
        entry_eff_50 = tk.Entry(frame_estim)
        entry_eff_50.grid(row=9, column=1, sticky=tk.W + tk.E)
        entry_eff_75 = tk.Entry(frame_estim)
        entry_eff_75.grid(row=9, column=2, sticky=tk.W + tk.E)
        entry_eff_100 = tk.Entry(frame_estim)
        entry_eff_100.grid(row=9, column=3, sticky=tk.W + tk.E)

        label_fp = tk.Label(frame_estim, text="Power Factor")
        label_fp.grid(row=10, column=0, sticky=tk.W)
        entry_fp_50 = tk.Entry(frame_estim)
        entry_fp_50.grid(row=10, column=1, sticky=tk.W + tk.E)
        entry_fp_75 = tk.Entry(frame_estim)
        entry_fp_75.grid(row=10, column=2, sticky=tk.W + tk.E)
        entry_fp_100 = tk.Entry(frame_estim)
        entry_fp_100.grid(row=10, column=3, sticky=tk.W + tk.E)

        def validarparam():
            a = 0

            def adicionar_mensagem(mensagem):
                texto.config(state=tk.NORMAL)
                texto.insert(tk.END, mensagem + "\n")
                texto.config(state=tk.DISABLED)
                texto.see(tk.END)

            jerro = tk.Toplevel()
            jerro.title("Errors")
            texto = tk.Text(jerro, wrap="word", state=tk.DISABLED)
            texto.pack(fill=tk.BOTH, expand=True)
            try:
                valor = (entry_Potn.get())
                valor = valor.replace(",", ".")
                entry_Potn.delete(0, tk.END)
                entry_Potn.insert(0, valor)
                valor = float(entry_Potn.get())
                entry_Potn.config(bg="white")
                if valor<=0:
                    entry_Potn.config(bg="red")
                    adicionar_mensagem(label_Potn.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_Potn.config(bg="red")
                adicionar_mensagem(label_Potn.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_Vn.get())
                valor = valor.replace(",", ".")
                entry_Vn.delete(0, tk.END)
                entry_Vn.insert(0, valor)
                valor = float(entry_Vn.get())
                entry_Vn.config(bg="white")
                if valor<=0:
                    entry_Vn.config(bg="red")
                    adicionar_mensagem(label_Vn.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_Vn.config(bg="red")
                adicionar_mensagem(label_Vn.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_fn.get())
                valor = valor.replace(",", ".")
                entry_fn.delete(0, tk.END)
                entry_fn.insert(0, valor)
                valor = float(entry_fn.get())
                entry_fn.config(bg="white")
                if valor<=0:
                    entry_fn.config(bg="red")
                    adicionar_mensagem(label_fn.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_fn.config(bg="red")
                adicionar_mensagem(label_fn.cget("text") + " INVALID INPUT!")
                a += 1

            # try:
            #     valor = (entry_In.get())
            #     valor = valor.replace(",", ".")
            #     entry_In.delete(0, tk.END)
            #     entry_In.insert(0, valor)
            #     valor = float(entry_In.get())
            #     entry_In.config(bg="white")
            # except ValueError:
            #     entry_In.config(bg="red")
            #     adicionar_mensagem(label_In.cget("text") + " ENTRADA INVALIDA!")
            #     a += 1

            try:
                valor = (entry_Polos.get())
                valor = valor.replace(",", ".")
                entry_Polos.delete(0, tk.END)
                entry_Polos.insert(0, valor)
                valor = float(entry_Polos.get())
                entry_Polos.config(bg="white")
                if valor<=0:
                    entry_Polos.config(bg="red")
                    adicionar_mensagem(label_Polos.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_Polos.config(bg="red")
                adicionar_mensagem(label_Polos.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_veln.get())
                valor = valor.replace(",", ".")
                entry_veln.delete(0, tk.END)
                entry_veln.insert(0, valor)
                valor = float(entry_veln.get())
                entry_veln.config(bg="white")
                if valor<=0:
                    entry_veln.config(bg="red")
                    adicionar_mensagem(label_veln.cget("text") +"Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_veln.config(bg="red")
                adicionar_mensagem(label_veln.cget("text") + " INVALID INPUT!")
                a += 1

            if entry_norma.get() == '':
                entry_norma.set("ERRO")
                adicionar_mensagem("Standard not selected.")
                a += 1

            if entry_cat.get() == '':
                entry_cat.set("ERRO")
                adicionar_mensagem("Category not selected.")
                a += 1

            try:
                valor = (entry_eff_50.get())
                valor = valor.replace(",", ".")
                entry_eff_50.delete(0, tk.END)
                entry_eff_50.insert(0, valor)
                valor = float(entry_eff_50.get())
                entry_eff_50.config(bg="white")
                if not (0 <= float(entry_eff_50.get()) <= 100):
                    entry_eff_50.config(bg="red")
                    adicionar_mensagem("Efficiency at 50% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_eff_50.config(bg="red")
                adicionar_mensagem("Efficiency at 50% load: INVALID INPUT!")
                a += 1

            try:
                valor = (entry_eff_75.get())
                valor = valor.replace(",", ".")
                entry_eff_75.delete(0, tk.END)
                entry_eff_75.insert(0, valor)
                valor = float(entry_eff_75.get())
                entry_eff_75.config(bg="white")
                if not (0 <= float(entry_eff_75.get()) <= 100):
                    entry_eff_75.config(bg="red")
                    adicionar_mensagem("Efficiency at 75% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_eff_75.config(bg="red")
                adicionar_mensagem("Efficiency at 75% load: INVALID INPUT!")
                a += 1

            try:
                valor = (entry_eff_100.get())
                valor = valor.replace(",", ".")
                entry_eff_100.delete(0, tk.END)
                entry_eff_100.insert(0, valor)
                valor = float(entry_eff_100.get())
                entry_eff_100.config(bg="white")
                if not (0 <= float(entry_eff_100.get()) <= 100):
                    entry_eff_100.config(bg="red")
                    adicionar_mensagem("Efficiency at 100% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_eff_100.config(bg="red")
                adicionar_mensagem("Efficiency at 100% load: INVALID INPUT!")
                a += 1

            try:
                valor = (entry_fp_50.get())
                valor = valor.replace(",", ".")
                entry_fp_50.delete(0, tk.END)
                entry_fp_50.insert(0, valor)
                valor = float(entry_fp_50.get())
                entry_fp_50.config(bg="white")
                if not (0 <= float(entry_fp_50.get()) <= 1):
                    entry_fp_50.config(bg="red")
                    adicionar_mensagem("Power factor at 50% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_fp_50.config(bg="red")
                adicionar_mensagem("Power factor at 50% load: INVALID INPUT!")
                a += 1

            try:
                valor = (entry_fp_75.get())
                valor = valor.replace(",", ".")
                entry_fp_75.delete(0, tk.END)
                entry_fp_75.insert(0, valor)
                valor = float(entry_fp_75.get())
                entry_fp_75.config(bg="white")
                if not (0 <= float(entry_fp_75.get()) <= 1):
                    entry_fp_75.config(bg="red")
                    adicionar_mensagem("Power factor at 75% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_fp_75.config(bg="red")
                adicionar_mensagem("Power factor at 75% load: INVALID INPUT!")
                a += 1

            try:
                valor = (entry_fp_100.get())
                valor = valor.replace(",", ".")
                entry_fp_100.delete(0, tk.END)
                entry_fp_100.insert(0, valor)
                valor = float(entry_fp_100.get())
                entry_fp_100.config(bg="white")
                if not (0 <= float(entry_fp_100.get()) <= 1):
                    entry_fp_100.config(bg="red")
                    adicionar_mensagem("Power factor at 100% load: Out of the allowed range (0 to 100%).")
                    a += 1
            except ValueError:
                entry_fp_100.config(bg="red")
                adicionar_mensagem("Power factor at 100% load: INVALID INPUT!")
                a += 1

            if a == 0:
                jerro.destroy()
                estimparam()
            else:
                return

        def estimparam():
            global r1, x1, xm, x2, r2
            diretorio = filedialog.askdirectory()
            agora = datetime.datetime.now()
            agora = str(agora)
            agora = re.sub(r"\s|\W+", "_", agora)[:-7]
            Pot_n = float(entry_Potn.get()) * 745.69872
            V_n = float(entry_Vn.get()) / np.sqrt(3)
            f_n = float(entry_fn.get())
            # I_n = float(entry_In.get())
            P = float(entry_Polos.get())
            vel_n = float(entry_veln.get())
            eff = np.array([float(entry_eff_50.get()), float(entry_eff_75.get()), float(entry_eff_100.get())]) / 100
            fp = np.array([float(entry_fp_50.get()), float(entry_fp_75.get()), float(entry_fp_100.get())])
            cat = entry_cat.get()
            if entry_norma.get() == "NEMA":
                norma = "0"
            elif entry_norma.get() == "NBR":
                norma = "1"
            cat = cat + norma

            ############################## r1 e Prot ####################################
            Pout = np.array([0.5, 0.75, 1]) * Pot_n
            P1 = Pout / eff
            vel_sin = 120 * f_n / P  # Velocidade síncrona
            s_n = (vel_sin - vel_n) / vel_sin  # Escorregamento nominal
            s = np.array([0.5, 0.75, 1]) * s_n
            Y = Pout - (1 - s) * P1

            I1 = P1 / (3 * V_n * fp)
            sup1 = -(1 - s) * 3 * I1 ** 2
            sup2 = -np.ones(3)
            PSI = np.stack((sup1, sup2), axis=1)

            TETA = np.dot(np.linalg.inv(np.dot(np.transpose(PSI), PSI)), np.dot(np.transpose(PSI), Y))
            r1 = TETA[0]
            Prot = TETA[1]

            ############################## r2 e k ####################################
            Y = s * (Pout + Prot) / (1 - s)

            sup1 = 3 * I1 ** 2
            sup2 = np.ones(3)
            PSI = np.stack((sup1, sup2), axis=1)

            TETA = np.dot(np.linalg.inv(np.dot(np.transpose(PSI), PSI)), np.dot(np.transpose(PSI), Y))
            r2 = TETA[0]
            k = TETA[1]

            ############################## x1, x2 e xm ####################################
            x1_x2 = {"A0": 1, "B0": 0.67, "C0": 0.43, "D0": 1,
                     "D1": 0.78, "N1": 0.68, "H1": 0.58}
            a = x1_x2[cat]

            Q = P1[2] * np.sin(np.arccos(fp[2])) / fp[2]
            I0 = np.sqrt((3 * r2 * I1[2] ** 2 - (Pout[2] + Prot) * s_n / (1 - s_n)) / (3 * r2))
            I1 = I1[2]

            A = 9 * (I0 ** 4 - I0 ** 2 * I1 ** 2 + (I1 ** 2 * a - I0 ** 2 + I1 ** 2) ** 2) / a ** 2
            B = -6 * Q * (I1 ** 2 * a - I0 ** 2 + I1 ** 2) / a  # Teve diferenças entre o trabalho e o artigo/código
            C = (9 * I0 ** 4 * r2 ** 2 - 9 * I0 ** 2 * I1 ** 2 * r2 ** 2 + Q ** 2 * s_n ** 2) / s_n ** 2

            x1 = (-B - np.sqrt(B ** 2 - 4 * A * C)) / (2 * A)  # Teve diferenças entre o trabalho e o artigo/código
            x2 = x1 / a
            xm = np.sqrt(((I1 ** 2 - I0 ** 2) / I0 ** 2) * ((r2 / s_n) ** 2 + (x1 / a) ** 2))

            dados_param = np.array([[r1, x1, xm, x2, r2]])
            header_param = "r1,x1,xm,x2,r2"
            np.savetxt(diretorio + "/" + agora + "_EstimParam.txt", dados_param, delimiter=',', header=header_param)

            ############################## Circuito ####################################
            if estado_graph_estimparam.get():
                plt.close("all")
                s = np.arange(1e-5, s_n * 1.2, 1e-5)
                dados_graph = np.zeros([len(s), 3], dtype=float)

                Z = 1j * x2 + r2 / s
                Z = (1j * xm * Z) / (1j * xm + Z)
                Z = Z + r1 + 1j * x1  # Calculo da impedância total do motor
                Z_abs = abs(Z)
                Z_angle = np.angle(Z)
                FP = np.cos(Z_angle)
                Is = V_n / Z_abs
                Pin = 3 * V_n * Is * FP
                Pcus = 3 * r1 * Is ** 2
                Pout = (Pin - Pcus) * (1 - s) - Prot
                Eff = Pout / Pin * 100

                Peixo = Pout * 100 / Pot_n
                dados_graph[:, 0] = Peixo
                dados_graph[:, 1] = Eff
                dados_graph[:, 2] = FP
                header_graph = "Power,Eff,FP"
                np.savetxt(diretorio + "/" + agora + "_Graph_EffPF.txt", dados_graph, delimiter=',', header=header_graph)

                plt.figure(1)
                plt.plot(Peixo, Eff)
                plt.title("Efficiency")
                plt.ylabel("Efficiency (%)")
                plt.xlabel("Power supplied relative to the nominal (%).")
                plt.ylim([0, 101])
                plt.xlim([0, 121])
                plt.grid()
                plt.figure(2)
                plt.plot(Peixo, FP)
                plt.title("Power Factor")
                plt.ylabel("Power Factor")
                plt.xlabel("Power supplied relative to the nominal (%).")
                plt.ylim([0, 1.1])
                plt.xlim([0, 121])
                plt.grid()
                plt.show(block=False)

            entry_V.delete(0, tk.END)
            entry_V.insert(0, str(entry_Vn.get()))
            entry_In.delete(0, tk.END)
            entry_In.insert(0, str(entry_Inc.get()))
            entry_f.delete(0, tk.END)
            entry_f.insert(0, entry_fn.get())
            entry_P.delete(0, tk.END)
            entry_P.insert(0, entry_Polos.get())
            entry_vnom.delete(0, tk.END)
            entry_vnom.insert(0, entry_veln.get())
            entry_rs.delete(0, tk.END)
            entry_rs.insert(0, str(round(r1, 4)))
            entry_xs.delete(0, tk.END)
            entry_xs.insert(0, str(round(x1, 4)))
            entry_xm.delete(0, tk.END)
            entry_xm.insert(0, str(round(xm, 4)))
            entry_xr.delete(0, tk.END)
            entry_xr.insert(0, str(round(x2, 4)))
            entry_rr.delete(0, tk.END)
            entry_rr.insert(0, str(round(r2, 4)))
            entry_Tload.delete(0, tk.END)
            entry_j.delete(0, tk.END)
            entry_jload.delete(0, tk.END)

            j2.destroy()

        label_espaco1 = tk.Label(frame_estim, text=' ')
        label_espaco1.grid(row=11, columnspan=4)
        botao_estim = tk.Button(frame_estim, text="ESTIMATE", command=validarparam, font=("Segoe UI", 11))
        botao_estim.grid(row=14, column=1, columnspan=2)

        estado_graph_estimparam = tk.BooleanVar()
        box_graph_estimparam = tk.Checkbutton(frame_estim, text="Show Graphs", variable=estado_graph_estimparam)
        box_graph_estimparam.grid(row=14, column=0)

        j2.update_idletasks()
        jan_l = j2.winfo_width()
        jan_h = j2.winfo_height()
        tela_l = j2.winfo_screenwidth()
        tela_h = j2.winfo_screenheight()
        x = (tela_l // 2) - (jan_l // 2)
        y = (tela_h // 2) - (jan_h // 2)
        j2.geometry(f"{jan_l}x{jan_h}+{x}+{y}")

    # ----------------------------------Banco de Dados------------------------------#
    def bdcreator():
        j1.withdraw()
        j3 = tk.Toplevel(j1)
        j3.option_add("*Font", ("Segoe UI", 11))
        # j1_l = j1.winfo_width()
        # j1_h = j1.winfo_height()
        # print(j1_l)
        # j3.geometry(f"{j1_l}x{j1_h}")
        j3.state("zoomed")
        j3.title("Database Generator")

        # ---------------Frame da barra superior--------------------
        barra_superiorbd = tk.Frame(j3, height=30, relief=tk.RAISED, bd=2)
        barra_superiorbd.pack(fill=tk.X, side=tk.TOP, padx=0, pady=0)
        # Impedir que o tamanho do frame da barra superior seja alterado automaticamente
        barra_superiorbd.pack_propagate(False)

        frame_bd = tk.Frame(j3)
        frame_bd.pack()

        # img_org = Image.open(r"logo_smit.png")
        img_org = Image.open(image_path)
        escala_im = 0.2
        img_l = int(img_org.width * escala_im)
        img_h = int(img_org.height * escala_im)
        img_red = img_org.resize((img_l, img_h), Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(img_red)
        label_logosmit = tk.Label(frame_bd, image=tk_image)
        label_logosmit.place(relx=1.02, rely=-0.1, anchor='ne')
        label_logosmit.image = tk_image

        label_estim = tk.Label(frame_bd, text="      ", font=("Segoe UI", 18, "bold"))
        label_estim.grid(row=11, column=8)

        # ----------------------------------Motor------------------------------#
        label_motorsel = tk.Label(frame_bd, text="\n\nMotor Selection", font=("Segoe UI", 12,"bold"))
        label_motorsel.grid(row=1, columnspan=6, sticky=tk.W)

        label_motor = tk.Label(frame_bd, text="Motor:")
        label_motor.grid(row=2, column=0, sticky=tk.W)
        diretorio_motor=''
        def selecionar_arquivo():
            global diretorio_motor
            diretorio_motor = filedialog.askopenfilename(parent=j3)
            if diretorio_motor == '':
                return
            botao_motor.config(text=diretorio_motor.split('/')[-1][:-4])
        botao_motor=tk.Button(frame_bd,text="Select File", command=selecionar_arquivo)
        botao_motor.grid(row=2,column=1, sticky=tk.W + tk.E)

        label_nsimu=tk.Label(frame_bd,text="  Number of simulations:")
        label_nsimu.grid(row=2,column=2, sticky=tk.W)
        entry_nsimu=tk.Entry(frame_bd)
        entry_nsimu.grid(row=2, column=3, sticky=tk.W + tk.E)

        # ----------------------------------Carga------------------------------#
        label_loadsel = tk.Label(frame_bd, text="Load settings", font=("Segoe UI", 12,"bold"))
        label_loadsel.grid(row=10, columnspan=6, sticky=tk.W)

        label_partbd = tk.Label(frame_bd, text="Starting type:")
        label_partbd.grid(row=11, column=0, sticky=tk.W)

        def cargabd_select(event):
            if entry_partbd.get() == options_part[0]:
                label_cargabd.config(state='disabled')
                entry_cargabd.config(state='disabled')
                label_tpbd.config(state='normal')
                entry_tpbd.config(state='normal')
            elif entry_partbd.get() == options_part[1]:
                label_cargabd.config(state='normal')
                entry_cargabd.config(state='normal')
                label_tpbd.config(state='disabled')
                entry_tpbd.config(state='disabled')

        selected_partbd = tk.StringVar(frame_bd)
        options_partbd = ["Without Load", "With Load"]
        entry_partbd = ttk.Combobox(frame_bd, values=list(options_partbd), textvariable=selected_partbd)
        entry_partbd.bind("<<ComboboxSelected>>", cargabd_select)
        entry_partbd.grid(row=11, column=1, sticky=tk.W + tk.E)
        selected_partbd.set("Without Load")

        label_tpbd = tk.Label(frame_bd, text="  Startup time (s):")
        label_tpbd.grid(row=11, column=2, sticky=tk.W)
        entry_tpbd = tk.Entry(frame_bd)
        entry_tpbd.grid(row=11, column=3, sticky=tk.W + tk.E)

        label_cargabd = tk.Label(frame_bd, text="  Load Type:", state='disabled')
        label_cargabd.grid(row=11, column=4, sticky=tk.W)
        selected_cargabd = tk.StringVar(frame_bd)
        options_cargabd = ["Constant", "Linear", "Quadratic"]
        entry_cargabd = ttk.Combobox(frame_bd, values=list(options_cargabd), textvariable=selected_cargabd, state='disabled')
        entry_cargabd.grid(row=11, column=5, sticky=tk.W + tk.E)
        entry_cargabd.set(options_cargabd[0])

        label_intercarga=tk.Label(frame_bd,text="Range")
        label_intercarga.grid(row=14, column=0, sticky=tk.W)
        label_mincarga=tk.Label(frame_bd,text="Minimum")
        label_mincarga.grid(row=14,column=1)
        label_maxcarga = tk.Label(frame_bd, text="Maximum")
        label_maxcarga.grid(row=14, column=2)

        label_pcargabd=tk.Label(frame_bd,text="Applied load (%):")
        label_pcargabd.grid(row=15,column=0,sticky=tk.W)
        entry_pcargabdmin=tk.Entry(frame_bd)
        entry_pcargabdmin.grid(row=15,column=1, sticky=tk.W + tk.E)
        entry_pcargabdmax=tk.Entry(frame_bd)
        entry_pcargabdmax.grid(row=15,column=2, sticky=tk.W + tk.E)

        label_jloadbd = tk.Label(frame_bd, text="Moment of inertia (kg·m²):")
        label_jloadbd.grid(row=16, column=0, sticky=tk.W)
        entry_jloadbdmin = tk.Entry(frame_bd)
        entry_jloadbdmin.grid(row=16, column=1, sticky=tk.W + tk.E)
        entry_jloadbdmax = tk.Entry(frame_bd)
        entry_jloadbdmax.grid(row=16, column=2, sticky=tk.W + tk.E)

        #----------------------------------Alimentação------------------------------#
        # label_alimconfigbd = tk.Label(frame_bd, text="Inversor de Frequência", font=("Segoe UI", 12))
        # label_alimconfigbd.grid(row=20, columnspan=6)
        #
        # label_alimbd = tk.Label(frame_bd, text="Tipo de alimentação:")
        # label_alimbd.grid(row=21, column=0, sticky=tk.W)
        # selected_alimbd = tk.StringVar(frame_bd)
        # options_alimbd = ["Senoidal", "PWM"]
        # entry_alimbd = ttk.Combobox(frame_bd, values=list(options_alimbd), textvariable=selected_alimbd)
        # entry_alimbd.grid(row=21, column=1, sticky=tk.W + tk.E)
        # entry_alimbd.insert(0,"Senoidal")
        #
        # label_fbd = tk.Label(frame_bd, text="Frequência da alimentação:")
        # label_fbd.grid(row=21, column=2, sticky=tk.W)
        # entry_fbd = tk.Entry(frame_bd)
        # # entry_fbd.insert(0, 60)
        # entry_fbd.grid(row=21, column=3, sticky=tk.W + tk.E)
        #
        # label_fpwmbd = tk.Label(frame_bd, text="Frequência do inversor:")
        # label_fpwmbd.grid(row=21, column=4, sticky=tk.W)
        # entry_fpwmbd = tk.Entry(frame_bd)
        # label_fpwmbd.config(state='disabled')
        # entry_fpwmbd.config(state='disabled')
        # entry_fpwmbd.grid(row=21, column=5, sticky=tk.W + tk.E)
        #
        # def pwmbd_select(event):
        #     if entry_alimbd.get() == options_alimbd[0]:
        #         label_fpwmbd.config(state='disabled')
        #         entry_fpwmbd.config(state='disabled')
        #     elif entry_alimbd.get() == options_alimbd[1]:
        #         label_fpwmbd.config(state='normal')
        #         entry_fpwmbd.config(state='normal')
        #
        # entry_alimbd.bind("<<ComboboxSelected>>", pwmbd_select)

        #----------------------------------Desequilíbrio------------------------------#
        estado_desbd = tk.BooleanVar()
        box_desbd = tk.Checkbutton(frame_bd, text="Voltage Imbalance", font=("Segoe UI", 12, "bold"), variable=estado_desbd)
        box_desbd.grid(row=30, columnspan=3, sticky=tk.W)
        def atualizar_estado_desbd():
            if estado_desbd.get():
                label_interdes.grid(row=31, column=0, sticky=tk.W)
                label_mindes.grid(row=31, column=1)
                label_maxdes.grid(row=31, column=2)
                label_desampbd.grid(row=32,column=0,sticky=tk.W)
                entry_desampbdmin.grid(row=32, column=1, sticky=tk.W + tk.E)
                entry_desampbdmax.grid(row=32, column=2, sticky=tk.W + tk.E)
                label_desangbd.grid(row=33, column=0, sticky=tk.W)
                entry_desangbdmin.grid(row=33, column=1, sticky=tk.W + tk.E)
                entry_desangbdmax.grid(row=33, column=2, sticky=tk.W + tk.E)
            else:
                label_interdes.grid_remove()
                label_mindes.grid_remove()
                label_maxdes.grid_remove()
                label_desampbd.grid_remove()
                entry_desampbdmin.grid_remove()
                entry_desampbdmax.grid_remove()
                label_desangbd.grid_remove()
                entry_desangbdmin.grid_remove()
                entry_desangbdmax.grid_remove()

        box_desbd.config(command=atualizar_estado_desbd)

        label_interdes = tk.Label(frame_bd, text="Range:")
        label_mindes = tk.Label(frame_bd, text="Minimum")
        label_maxdes = tk.Label(frame_bd, text="Maximum")

        label_desampbd=tk.Label(frame_bd,text="Imbalance percentage (%):")
        entry_desampbdmin=tk.Entry(frame_bd)
        entry_desampbdmax = tk.Entry(frame_bd)

        label_desangbd = tk.Label(frame_bd, text="Angular imbalance (%):")
        entry_desangbdmin = tk.Entry(frame_bd)
        entry_desangbdmax = tk.Entry(frame_bd)

        # ----------------------------------Curto------------------------------#
        estado_curtobd = tk.BooleanVar()
        box_curtobd = tk.Checkbutton(frame_bd, text="Short Circuit in the Stator Windings", font=("Segoe UI", 12,"bold"), variable=estado_curtobd)
        box_curtobd.grid(row=30, column=3, columnspan=3, sticky=tk.W)

        def atualizar_estado_curtobd():
            if estado_curtobd.get():
                label_intercurto.grid(row=31, column=3, sticky=tk.W)
                label_mincurto.grid(row=31, column=4)
                label_maxcurto.grid(row=31, column=5)
                label_mibd.grid(row=32, column=3, sticky=tk.W)
                entry_mibdmin.grid(row=32, column=4, sticky=tk.W + tk.E)
                entry_mibdmax.grid(row=32, column=5, sticky=tk.W + tk.E)
                label_rfbd.grid(row=33, column=3, sticky=tk.W)
                entry_rfbdmin.grid(row=33, column=4, sticky=tk.W + tk.E)
                entry_rfbdmax.grid(row=33, column=5, sticky=tk.W + tk.E)
            else:
                label_intercurto.grid_remove()
                label_mincurto.grid_remove()
                label_maxcurto.grid_remove()
                label_mibd.grid_remove()
                entry_mibdmin.grid_remove()
                entry_mibdmax.grid_remove()
                label_rfbd.grid_remove()
                entry_rfbdmin.grid_remove()
                entry_rfbdmax.grid_remove()

        box_curtobd.config(command=atualizar_estado_curtobd)

        label_intercurto = tk.Label(frame_bd, text="  Range:")
        label_mincurto = tk.Label(frame_bd, text="Minimum")
        label_maxcurto = tk.Label(frame_bd, text="Maximum")

        label_mibd = tk.Label(frame_bd, text="  Short-circuit winding ratio (%):")
        entry_mibdmin = tk.Entry(frame_bd)
        entry_mibdmax = tk.Entry(frame_bd)

        label_rfbd = tk.Label(frame_bd, text="  Multiplier:")
        entry_rfbdmin = tk.Entry(frame_bd)
        entry_rfbdmax = tk.Entry(frame_bd)


        # ----------------------------------Barras Quebradas------------------------------#
        estado_barrabd = tk.BooleanVar()
        box_barrabd = tk.Checkbutton(frame_bd, text="Broken Bars in the Rotor", font=("Segoe UI", 12, "bold"),
                                   variable=estado_barrabd)
        box_barrabd.grid(row=50, columnspan=6, sticky=tk.W)

        def atualizar_estado_barrabd():
            if estado_barrabd.get():
                label_nbd.grid(row=51, column=0, sticky=tk.W)
                entry_nbd.grid(row=51, column=1, sticky=tk.W + tk.E)
                label_nivelbqbd.grid(row=51, column=2, sticky=tk.W)
                entry_nivelbqbd.grid(row=51, column=3, sticky=tk.W + tk.E)
                label_interbarra.grid(row=52, column=0, sticky=tk.W)
                label_minbarra.grid(row=52, column=1)
                label_maxbarra.grid(row=52, column=2)
                label_nbqbd.grid(row=53, column=0, sticky=tk.W)
                entry_nbqbdmin.grid(row=53, column=1, sticky=tk.W + tk.E)
                entry_nbqbdmax.grid(row=53, column=2, sticky=tk.W + tk.E)

            else:
                label_nbd.grid_remove()
                entry_nbd.grid_remove()
                label_nivelbqbd.grid_remove()
                entry_nivelbqbd.grid_remove()
                label_interbarra.grid_remove()
                label_minbarra.grid_remove()
                label_maxbarra.grid_remove()
                label_nbqbd.grid_remove()
                entry_nbqbdmin.grid_remove()
                entry_nbqbdmax.grid_remove()

        box_barrabd.config(command=atualizar_estado_barrabd)
        label_nbd = tk.Label(frame_bd, text="Total number of bars:")
        entry_nbd = tk.Entry(frame_bd)

        label_nivelbqbd = tk.Label(frame_bd, text="  Failure level:")
        selected_nivelbqbd = tk.StringVar(frame_bd)
        options_nivelbqbd = ["Crack (10%)", "Fracture (50%)", "Break (100%)"]
        entry_nivelbqbd = ttk.Combobox(frame_bd, values=list(options_nivelbqbd), textvariable=selected_nivelbqbd)

        label_interbarra = tk.Label(frame_bd, text="Range:")
        label_minbarra = tk.Label(frame_bd, text="Minimum")
        label_maxbarra = tk.Label(frame_bd, text="Maximum")

        label_nbqbd = tk.Label(frame_bd, text="Number of broken bars:")
        entry_nbqbdmin = tk.Entry(frame_bd)
        entry_nbqbdmax = tk.Entry(frame_bd)

        # ----------------------------------Falhas Mecânicas------------------------------#
        estado_mecbd = tk.BooleanVar()
        box_mecbd = tk.Checkbutton(frame_bd, text="Mechanical Failures", font=("Segoe UI", 12, "bold"), variable=estado_mecbd)
        box_mecbd.grid(row=60, columnspan=6, sticky=tk.W)

        def atualizar_estado_mecbd():
            if estado_mecbd.get():
                label_intermec.grid(row=61, column=0, sticky=tk.W)
                label_minmec.grid(row=61, column=1)
                label_maxmec.grid(row=61, column=2)
                label_Tfalhabd.grid(row=62, column=0, sticky=tk.W)
                entry_Tfalhabdmin.grid(row=62, column=1, sticky=tk.W + tk.E)
                entry_Tfalhabdmax.grid(row=62, column=2, sticky=tk.W + tk.E)

            else:
                label_Tfalhabd.grid_remove()
                entry_Tfalhabdmin.grid_remove()
                entry_Tfalhabdmax.grid_remove()
                label_intermec.grid_remove()
                label_minmec.grid_remove()
                label_maxmec.grid_remove()

        box_mecbd.config(command=atualizar_estado_mecbd)

        label_intermec = tk.Label(frame_bd, text="Range:")
        label_minmec = tk.Label(frame_bd, text="Minimum")
        label_maxmec = tk.Label(frame_bd, text="Maximum")

        label_Tfalhabd = tk.Label(frame_bd, text="Failure torque (%):")
        entry_Tfalhabdmin = tk.Entry(frame_bd)
        entry_Tfalhabdmax = tk.Entry(frame_bd)

        executando = False
        def iniciar_simubd():
            # global thread
            # if not thread or not thread.is_alive():
            thread = threading.Thread(target=validarbd)
            thread.start()

        def validarbd():
            a = 0
            pmax=0
            pmin=0

            def adicionar_mensagem(mensagem):
                texto.config(state=tk.NORMAL)
                texto.insert(tk.END, mensagem + "\n")
                texto.config(state=tk.DISABLED)
                texto.see(tk.END)

            jerro = tk.Toplevel()
            jerro.title("Errors")
            texto = tk.Text(jerro, wrap="word", state=tk.DISABLED)
            texto.pack(fill=tk.BOTH, expand=True)

            if diretorio_motor=='':
                adicionar_mensagem("Motor not selected")
                a+=1

            try:
                valor = (entry_nsimu.get())
                valor = valor.replace(",", ".")
                entry_nsimu.delete(0, tk.END)
                entry_nsimu.insert(0, valor)
                valor = float(entry_nsimu.get())
                valor = int(valor)
                entry_nsimu.delete(0, tk.END)
                entry_nsimu.insert(0, str(valor))
                entry_nsimu.config(bg="white")
                if valor <= 0:
                    entry_nsimu.config(bg="red")
                    adicionar_mensagem(label_nsimu.cget("text")[2:] + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_nsimu.config(bg="red")
                adicionar_mensagem(label_nsimu.cget("text")[2:] + " INVALID INPUT!")
                a += 1

            if entry_partbd.get() != options_partbd[0] and entry_partbd.get() != options_partbd[1]:
                entry_partbd.set("ERRO")
                adicionar_mensagem("Starting type not accepted.")
                a += 1

            if entry_cargabd.get() != options_cargabd[0] and entry_cargabd.get() != options_cargabd[1] and entry_cargabd.get() != \
                    options_cargabd[2]:
                entry_cargabd.set("ERRO")
                adicionar_mensagem("Load type not accepted.")
                a += 1

            try:
                valor = (entry_tpbd.get())
                valor = valor.replace(",", ".")
                entry_tpbd.delete(0, tk.END)
                entry_tpbd.insert(0, valor)
                valor = float(entry_tpbd.get())
                entry_tpbd.config(bg="white")
            except ValueError:
                entry_tpbd.config(bg="red")
                adicionar_mensagem(label_tpbd.cget("text")[2:] + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_pcargabdmin.get())
                valor = valor.replace(",", ".")
                entry_pcargabdmin.delete(0, tk.END)
                entry_pcargabdmin.insert(0, valor)
                valor = float(entry_pcargabdmin.get())
                entry_pcargabdmin.config(bg="white")
                pmin=valor
                if valor <= 0:
                    entry_pcargabdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of "+ label_pcargabd.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_pcargabdmin.config(bg="red")
                adicionar_mensagem("Minimum point of "+ label_pcargabd.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_pcargabdmax.get())
                valor = valor.replace(",", ".")
                entry_pcargabdmax.delete(0, tk.END)
                entry_pcargabdmax.insert(0, valor)
                valor = float(entry_pcargabdmax.get())
                entry_pcargabdmax.config(bg="white")
                pmax=valor
                if valor <= 0:
                    entry_pcargabdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of "+label_pcargabd.cget("text") + "Variable cannot be null or negative.")
                    a += 1
            except ValueError:
                entry_pcargabdmax.config(bg="red")
                adicionar_mensagem("Maximum point of "+label_pcargabd.cget("text") + " INVALID INPUT!")
                a += 1

            if pmax<pmin:
                entry_pcargabdmin.config(bg="red")
                entry_pcargabdmax.config(bg="red")
                adicionar_mensagem("Maximum point of the applied load interval is greater than the minimum.")
                a+=1

            try:
                valor = (entry_jloadbdmin.get())
                valor = valor.replace(",", ".")
                entry_jloadbdmin.delete(0, tk.END)
                entry_jloadbdmin.insert(0, valor)
                valor = float(entry_jloadbdmin.get())
                entry_jloadbdmin.config(bg="white")
                pmin=valor
                if valor < 0:
                    entry_jloadbdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of "+label_jloadbd.cget("text") +  "Variable cannot be negative.")
                    a += 1
            except ValueError:
                entry_jloadbdmin.config(bg="red")
                adicionar_mensagem("Minimum point of "+label_jloadbd.cget("text") + " INVALID INPUT!")
                a += 1

            try:
                valor = (entry_jloadbdmax.get())
                valor = valor.replace(",", ".")
                entry_jloadbdmax.delete(0, tk.END)
                entry_jloadbdmax.insert(0, valor)
                valor = float(entry_jloadbdmax.get())
                entry_jloadbdmax.config(bg="white")
                pmax=valor
                if valor < 0:
                    entry_pcargabdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of "+label_jloadbd.cget("text") + "Variable cannot be negative.")
                    a += 1
            except ValueError:
                entry_jloadbdmax.config(bg="red")
                adicionar_mensagem("Maximum point of "+label_jloadbd.cget("text") + " INVALID INPUT!")
                a += 1

            if pmax < pmin:
                entry_jloadbdmin.config(bg="red")
                entry_jloadbdmax.config(bg="red")
                adicionar_mensagem("Maximum point of the load moment of inertia interval is greater than the minimum.")
                a += 1

            if estado_desbd.get():
                try:
                    valor = (entry_desampbdmin.get())
                    valor = valor.replace(",", ".")
                    entry_desampbdmin.delete(0, tk.END)
                    entry_desampbdmin.insert(0, valor)
                    valor = float(entry_desampbdmin.get())
                    entry_desampbdmin.config(bg="white")
                    pmin = valor
                    if valor <= 0:
                        entry_desampbdmin.config(bg="red")
                        adicionar_mensagem("Minimum point of " + label_desampbd.cget("text") + "Variable cannot be null or negative.")
                        a += 1
                except ValueError:
                    entry_desampbdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of " + label_desampbd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_desampbdmax.get())
                    valor = valor.replace(",", ".")
                    entry_desampbdmax.delete(0, tk.END)
                    entry_desampbdmax.insert(0, valor)
                    valor = float(entry_desampbdmax.get())
                    entry_desampbdmax.config(bg="white")
                    pmax = valor
                    if valor <= 0:
                        entry_desampbdmax.config(bg="red")
                        adicionar_mensagem("Maximum point of " + label_desampbd.cget("text") + "Variable cannot be null or negative.")
                        a += 1
                except ValueError:
                    entry_desampbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of " + label_desampbd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmax < pmin:
                    entry_desampbdmin.config(bg="red")
                    entry_desampbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of the imbalance percentage interval is greater than the minimum.")
                    a += 1

                try:
                    valor = (entry_desangbdmin.get())
                    valor = valor.replace(",", ".")
                    entry_desangbdmin.delete(0, tk.END)
                    entry_desangbdmin.insert(0, valor)
                    valor = float(entry_desangbdmin.get())
                    entry_desangbdmin.config(bg="white")
                    pmin = valor
                except ValueError:
                    entry_desangbdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of " + label_desangbd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_desangbdmax.get())
                    valor = valor.replace(",", ".")
                    entry_desangbdmax.delete(0, tk.END)
                    entry_desangbdmax.insert(0, valor)
                    valor = float(entry_desangbdmax.get())
                    entry_desangbdmax.config(bg="white")
                    pmax = valor
                except ValueError:
                    entry_desangbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of " + label_desangbd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmax < pmin:
                    entry_desangbdmin.config(bg="red")
                    entry_desangbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of the angular phase shift interval is greater than the minimum.")
                    a += 1

            if estado_curtobd.get():
                try:
                    valor = (entry_mibdmin.get())
                    valor = valor.replace(",", ".")
                    entry_mibdmin.delete(0, tk.END)
                    entry_mibdmin.insert(0, valor)
                    valor = float(entry_mibdmin.get())
                    entry_mibdmin.config(bg="white")
                    pmin = valor
                    if 0 > valor > 100:
                        entry_mibdmin.config(bg="red")
                        adicionar_mensagem("Minimum point of " + label_mibd.cget("text") + "Input out of the allowed range (between 0 and 100%).")
                        a += 1
                except ValueError:
                    entry_mibdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of " + label_mibd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_mibdmax.get())
                    valor = valor.replace(",", ".")
                    entry_mibdmax.delete(0, tk.END)
                    entry_mibdmax.insert(0, valor)
                    valor = float(entry_mibdmax.get())
                    entry_mibdmax.config(bg="white")
                    pmax = valor
                    if 0 > valor > 100:
                        entry_mibdmax.config(bg="red")
                        adicionar_mensagem("Maximum point of " + label_mibd.cget("text") + "Input out of the allowed range (between 0 and 100%).")
                        a += 1
                except ValueError:
                    entry_mibdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of " + label_mibd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmax < pmin:
                    entry_mibdmin.config(bg="red")
                    entry_mibdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of the short-circuit winding percentage interval is greater than the minimum.")
                    a += 1

                try:
                    valor = (entry_rfbdmin.get())
                    valor = valor.replace(",", ".")
                    entry_rfbdmin.delete(0, tk.END)
                    entry_rfbdmin.insert(0, valor)
                    valor = float(entry_rfbdmin.get())
                    entry_rfbdmin.config(bg="white")
                    pmin = valor
                    if 0>valor>1:
                        entry_rfbdmin.config(bg="red")
                        adicionar_mensagem("Minimum point of " + label_rfbd.cget("text") + "Variable out of the allowed range (greater than 0).")
                        a += 1
                except ValueError:
                    entry_rfbdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of " + label_rfbd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_rfbdmax.get())
                    valor = valor.replace(",", ".")
                    entry_rfbdmax.delete(0, tk.END)
                    entry_rfbdmax.insert(0, valor)
                    valor = float(entry_rfbdmax.get())
                    entry_rfbdmax.config(bg="white")
                    pmax = valor
                    if 0>valor>1:
                        entry_rfbdmax.config(bg="red")
                        adicionar_mensagem("Maximum point of " + label_rfbd.cget("text") + "Variable out of the allowed range (greater than 0).")
                        a += 1
                except ValueError:
                    entry_rfbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of " + label_rfbd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmax < pmin:
                    entry_rfbdmin.config(bg="red")
                    entry_rfbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of the failure resistance multiplier interval is greater than the minimum.")
                    a += 1

            if estado_barrabd.get():
                try:
                    valor = (entry_nbd.get())
                    valor = valor.replace(",", ".")
                    entry_nbd.delete(0, tk.END)
                    entry_nbd.insert(0, valor)
                    valor = float(entry_nbd.get())
                    valor = int(valor)
                    entry_nbd.delete(0, tk.END)
                    entry_nbd.insert(0, str(valor))
                    entry_nbd.config(bg="white")
                    if valor <= 0:
                        entry_nbd.config(bg="red")
                        adicionar_mensagem(label_nbd.cget("text") + "Variable cannot be null or negative.")
                        a += 1
                except ValueError:
                    entry_nbd.config(bg="red")
                    adicionar_mensagem(label_nbd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_nbqbdmin.get())
                    valor = valor.replace(",", ".")
                    entry_nbqbdmin.delete(0, tk.END)
                    entry_nbqbdmin.insert(0, valor)
                    valor = float(entry_nbqbdmin.get())
                    valor = int(valor)
                    entry_nbqbdmin.delete(0, tk.END)
                    entry_nbqbdmin.insert(0, str(valor))
                    entry_nbqbdmin.config(bg="white")
                    pmin=valor
                    if int(entry_nbqbdmin.get()) >= int(entry_nbd.get()):
                        entry_nbqbdmin.config(bg="red")
                        entry_nbd.config(bg="red")
                        adicionar_mensagem(label_nbqbd.cget("text") + " Greater than or equal to " + label_nbd.cget("text"))
                        a += 1
                    if valor < 0:
                        entry_nbqbdmin.config(bg="red")
                        adicionar_mensagem("Minimum point of" + label_nbqbd.cget("text") + "Variable cannot be negative.")
                        a += 1
                except ValueError:
                    entry_nbqbdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of" + label_nbqbd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_nbqbdmax.get())
                    valor = valor.replace(",", ".")
                    entry_nbqbdmax.delete(0, tk.END)
                    entry_nbqbdmax.insert(0, valor)
                    valor = float(entry_nbqbdmax.get())
                    valor = int(valor)
                    entry_nbqbdmax.delete(0, tk.END)
                    entry_nbqbdmax.insert(0, str(valor))
                    entry_nbqbdmax.config(bg="white")
                    pmax=valor
                    if int(entry_nbqbdmax.get()) >= int(entry_nbd.get()):
                        entry_nbqbdmax.config(bg="red")
                        entry_nbd.config(bg="red")
                        adicionar_mensagem(label_nbqbd.cget("text") + " Greater than or equal to " + label_nbd.cget("text"))
                        a += 1
                    if valor < 0:
                        entry_nbqbdmax.config(bg="red")
                        adicionar_mensagem("Maximum point of" + label_nbqbd.cget("text") + "Variable cannot be negative.")
                        a += 1
                except ValueError:
                    entry_nbqbdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of" + label_nbqbd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmin>pmax:
                    entry_nbqbdmin.config(bg="red")
                    entry_nbqbdmax.config(bg="red")
                    adicionar_mensagem(
                        "Maximum point of the broken bars interval is greater than the minimum.")
                    a += 1

                if entry_nivelbqbd.get() != options_nivelbqbd[0] and entry_nivelbqbd.get() != options_nivelbqbd[
                    1] and entry_nivelbqbd.get() != \
                        options_nivelbqbd[2]:
                    entry_nivelbqbd.set("ERROR")
                    adicionar_mensagem("Bar breakage level not accepted.")
                    a += 1

            if estado_mecbd.get():
                try:
                    valor = (entry_Tfalhabdmin.get())
                    valor = valor.replace(",", ".")
                    entry_Tfalhabdmin.delete(0, tk.END)
                    entry_Tfalhabdmin.insert(0, valor)
                    valor = float(entry_Tfalhabdmin.get())
                    entry_Tfalhabdmin.config(bg="white")
                    pmin=valor
                    if not 0 <= valor <= 100:
                        entry_Tfalhabdmin.config(bg="red")
                        adicionar_mensagem("Minimum point of" +
                            label_Tfalhabd.cget("text") + " Input out of the allowed range (between 0 and 100%).")
                        a += 1
                except ValueError:
                    entry_Tfalhabdmin.config(bg="red")
                    adicionar_mensagem("Minimum point of" + label_Tfalhabd.cget("text") + " INVALID INPUT!")
                    a += 1

                try:
                    valor = (entry_Tfalhabdmax.get())
                    valor = valor.replace(",", ".")
                    entry_Tfalhabdmax.delete(0, tk.END)
                    entry_Tfalhabdmax.insert(0, valor)
                    valor = float(entry_Tfalhabdmax.get())
                    entry_Tfalhabdmax.config(bg="white")
                    pmax=valor
                    if not 0 <= valor <= 100:
                        entry_Tfalhabdmax.config(bg="red")
                        adicionar_mensagem("Maximum point of" +
                            label_Tfalhabd.cget("text") + " Input out of the allowed range (between 0 and 100%).")
                        a += 1
                except ValueError:
                    entry_Tfalhabdmax.config(bg="red")
                    adicionar_mensagem("Maximum point of" + label_Tfalhabd.cget("text") + " INVALID INPUT!")
                    a += 1

                if pmin>pmax:
                    entry_Tfalhabdmin.config(bg="red")
                    entry_Tfalhabdmax.config(bg="red")
                    adicionar_mensagem(
                        "Maximum point of the failure torque interval is greater than the minimum.")
                    a += 1

            if a == 0:
                jerro.destroy()
                selectvarbd()
            else:
                return

        def selectvarbd():  # Essa função tem que chamar a simulador, depois
            def varesc():
                var = np.zeros(7, dtype=bool)
                if select_V.get():
                    var[0] = True
                if select_Is.get():
                    var[1] = True
                if select_Ir.get():
                    var[2] = True
                if select_Fs.get():
                    var[3] = True
                if select_Fr.get():
                    var[4] = True
                if select_Te.get():
                    var[5] = True
                if select_vel.get():
                    var[6] = True
                jvar.destroy()
                simularbd(var)
                return

            def manter_marcado():
                var.set(1)

            var = tk.IntVar(value=1)

            jvar = tk.Toplevel(j1)
            jvar.title("Variables")

            frame_var = tk.Frame(jvar)
            frame_var.pack()

            label_var = tk.Label(frame_var, text="Select the variables that should be saved.",
                                 font=("Segoe UI", 14, "bold"))
            label_var.grid(row=1, columnspan=2)

            select_V = var
            box_V = tk.Checkbutton(frame_var, text="Supply voltage", variable=select_V, command=manter_marcado)
            box_V.select()
            box_V.grid(row=2, columnspan=2)

            select_Is = var
            box_Is = tk.Checkbutton(frame_var, text="Stator current", variable=select_Is, command=manter_marcado)
            box_Is.grid(row=3, columnspan=2)
            box_Is.select()

            select_Ir = tk.BooleanVar()
            box_Ir = tk.Checkbutton(frame_var, text="Rotor current", variable=select_Ir)
            box_Ir.grid(row=4, columnspan=2)

            select_Fs = tk.BooleanVar()
            box_Fs = tk.Checkbutton(frame_var, text="Stator electromagnetic flux", variable=select_Fs)
            box_Fs.grid(row=5, columnspan=2)

            select_Fr = tk.BooleanVar()
            box_Fr = tk.Checkbutton(frame_var, text="Rotor electromagnetic flux", variable=select_Fr)
            box_Fr.grid(row=6, columnspan=2)

            select_Te = tk.BooleanVar()
            box_Te = tk.Checkbutton(frame_var, text="Electromagnetic torque", variable=select_Te)
            box_Te.grid(row=7, columnspan=2)
            box_Te.select()

            select_vel = tk.BooleanVar()
            box_vel = tk.Checkbutton(frame_var, text="Motor speed", variable=select_vel)
            box_vel.grid(row=8, columnspan=2)
            box_vel.select()

            var_botao = tk.Button(frame_var, text="Select", command=varesc, font=("Segoe UI", 12), width=8)
            var_botao.grid(row=15, columnspan=2)

        def simularbd(var):
            global executando
            executando = True
            plt.close("all")
            botao_playbd.pack_forget()
            botao_stopbd.pack(side=tk.LEFT, padx=10, pady=5)
            diretorio_savebd=filedialog.askdirectory()
            if diretorio_savebd=='':
                botao_stopbd.pack_forget()
                botao_playbd.pack(side=tk.LEFT, padx=10, pady=5)
                return

            # ----------------------------------Barra de Progresso------------------------------#
            progressobd=ttk.Progressbar(frame_bd,orient='horizontal',length=200, mode="determinate")
            progressobd.grid(row=71,columnspan=6)

            agora=datetime.datetime.now()
            agora=str(agora)
            agora = re.sub(r"\s|\W+", "_", agora)[:-7]
            diretorio_savebd=diretorio_savebd+ "/MITSimulador_" + agora
            os.makedirs(diretorio_savebd)

            # ----------------------------------Simulador------------------------------#
            # -------------------- FUNÇÃO ABC2DQ --------------------#
            def abc2dq(fa, fb, fc, teta):
                Fabc = np.array([[fa], [fb], [fc]])
                K = c23 * np.array([[np.cos(teta), np.cos(teta - ang120), np.cos(teta + ang120)],
                                    [np.sin(teta), np.sin(teta - ang120), np.sin(teta + ang120)],
                                    [0.5, 0.5, 0.5]])
                Fdq = K @ Fabc
                return (Fdq)

            # -------------------- FUNÇÃO DQ2ABC --------------------#
            def dq2abc(fq, fd, f0, teta):
                Fdq = np.array([[fq], [fd], [f0]])
                K = np.array([[np.cos(teta), np.sin(teta), 1],
                              [np.cos(teta - ang120), np.sin(teta - ang120), 1],
                              [np.cos(teta + ang120), np.sin(teta + ang120), 1]])
                Fabc = K @ Fdq
                return (Fabc)

            # -------------------- FUNÇÃO MATRIZ --------------------#
            def matriz(n, P):
                Tdq = np.zeros([n, n], dtype=float)
                Tdq[0, 0] = 1
                for i in range(1, n):
                    Tdq[0, i] = np.cos(P / 2 * (-2 * np.pi * i / n))
                    Tdq[1, i] = np.sin(P / 2 * (-2 * np.pi * i / n))
                T_aux = np.linalg.inv(Tdq[:2, :2]) @ (-Tdq[:2, 2:n])
                for i in range(2, n):
                    Tdq[i, 0] = T_aux[0, i - 2]
                    Tdq[i, 1] = T_aux[1, i - 2]
                Tdq[2:, 2:] = np.identity(n - 2)
                Tdq = (n - 1) * Tdq / n
                return Tdq

            # -------------------- FUNÇÃO RUNGE-KUTTA --------------------#
            def RK(u):
                du = np.zeros(7, dtype=float)
                Fqs = u[0]
                Fds = u[1]
                Fqr = u[2]
                Fdr = u[3]
                wr = u[4]
                F0s = u[5]
                Fas2 = u[6]

                du[0] = dt * (vq - rs * (a1 * Fqs - a2 * Fqr + c23mi * i_f) + c23mirs * i_f)
                du[1] = dt * (vd - rs * (a1 * Fds - a2 * Fdr))
                du[2] = dt * (-rr * (a4 * Fqr - a2 * Fqs) + wr * Fdr)
                du[3] = dt * (-rr * (a4 * Fdr - a2 * Fds) - wr * Fqr)
                du[4] = dt * ((Te - Tload) / J)
                du[5] = dt * (mirs3 * i_f)
                du[6] = dt * (vas2 - mirs * ((a1 * Fqs - a2 * Fqr + c23mi * i_f) - i_f))

                return (du)

            # -------------------- ENTRADAS --------------------#
            with open(diretorio_motor, "r") as arquivo:
                abrir = arquivo.readlines()
            for i in range(abrir.__len__()):
                abrir[i] = abrir[i][:-1]

            # TEMPO
            famos=float(abrir[0])
            dt=1/famos
            tfinal=float(abrir[1])

            # DADOS DO MOTOR
            f=float(abrir[2]) #Frequência da rede
            P=int(float(abrir[3])) #Número de polos
            V = float(abrir[4]) # Tensão de linha nominal
            v_nom = float(abrir[5])  # Velocidade nominal
            Tload_max = float(abrir[6])  # Carga nominal
            rs = float(abrir[7])  # Resistência do estator
            Lls = float(abrir[8])  # Reatância do estator
            Xs=Lls
            Lm = float(abrir[9])  # Reatância mútua
            Llr = float(abrir[10])  # Reatância do rotor
            rr = float(abrir[11])  # Resistência do rotor
            J_nom = float(abrir[12])  # Momento de inércia do motor
            In = float(abrir[14])  # Momento de inércia do motor

            # CONFIGURAÇÃO DO BD
            nsimu=int(entry_nsimu.get()) #Quantidade de simulações

            # CARGA
            if entry_partbd.get() == options_partbd[0]:
                tp = float(entry_tpbd.get())  # Tempo de partida
                tipo_part = 0
            elif entry_partbd.get() == options_partbd[1]:
                tipo_part = 1
                tp = 0
                if entry_cargabd.get() == options_cargabd[0]:
                    tipo_carga = 0
                elif entry_cargabd.get() == options_cargabd[1]:
                    tipo_carga = 1
                elif entry_cargabd.get() == options_cargabd[2]:
                    tipo_carga = 2
            pcargamin = float(entry_pcargabdmin.get())
            pcargamax = float(entry_pcargabdmax.get())
            J_loadmin = float(entry_jloadbdmin.get())
            J_loadmax = float(entry_jloadbdmax.get())

            # ALIMENTAÇÃO
            # if entry_alimbd.get() == options_alimbd[0]:
            #     tipo_alim = 0
            # elif entry_alimbd.get() == options_alimbd[1]:
            #     tipo_alim = 1
            #     f_triang = float(entry_fpwmbd.get())
            # f = float(entry_fbd.get())

            # DESEQUELÍBRIO DE FASES
            if estado_desbd.get():
                deseqampmin = float(entry_desampbdmin.get())
                deseqampmax = float(entry_desampbdmax.get())
                deseqangmin = float(entry_desangbdmin.get())
                deseqangmax = float(entry_desangbdmax.get())
            else:
                deseqampmin = 100  # Desequilíbrio do módulo da fase a
                deseqampmax = 100  # Desequilíbrio do módulo da fase a
                deseqangmin = 0  # Desequilíbrio do ângulo da fase a
                deseqangmax = 0  # Desequilíbrio do ângulo da fase a

            # CURTO
            if estado_curtobd.get():
                mimin = float(entry_mibdmin.get())
                mimax = float(entry_mibdmax.get())
                nrfmin = float(entry_rfbdmin.get())
                nrfmax = float(entry_rfbdmax.get())
            else:
                mimin = 0
                mimax = 0
                nrfmin = 0
                nrfmax = 0

            # BARRAS QUEBRADAS
            if estado_barrabd.get():
                n = int(entry_nbd.get())
                aux_barra = np.zeros([n - 2, 1])
                Tdq = matriz(n, P)
                nbqmin = int(entry_nbqbdmin.get())
                nbqmax = int(entry_nbqbdmax.get())
                nivelbq = entry_nivelbqbd.get()
            else:
                n = 0  # Número de barras (Aproximado)
                nbqmin = 0  # Número de barras quebradas
                nbqmax = 0  # Número de barras quebradas
                nivelbq = 0  # Nível do rompimento (1- rachadura (10%), 2- metade(50%), 3- completa(100%))
            if nivelbq == options_nivelbqbd[0]:
                nivelbq = 1
            elif nivelbq == options_nivelbqbd[1]:
                nivelbq = 2
            elif nivelbq == options_nivelbqbd[2]:
                nivelbq = 3

            # FALHAS MECÂNICAS
            if estado_mecbd.get():
                T_falha_nommin = float(entry_Tfalhabdmin.get())
                T_falha_nommax = float(entry_Tfalhabdmax.get())
            else:
                T_falha_nommin = 0.0  # Falhas mecânicas
                T_falha_nommax = 0.0  # Falhas mecânicas

            t = np.arange(0, tfinal + dt, dt)
            Vmax = V * np.sqrt(2)/np.sqrt(3)
            J_nom = J_nom * 2 / P
            we = 2 * np.pi * f
            baldefnom = v_nom * P / 120
            if 60 - baldefnom > 50:
                fnom = 60
            else:
                fnom = 50
            v_nom = f * v_nom / fnom
            Lls = Lls / we
            Llr = Llr / we
            Lm = Lm / we
            Ls = Lls + Lm
            Lr = Llr + Lm
            a1 = Lr / (Ls * Lr - Lm ** 2)
            a2 = Lm / (Ls * Lr - Lm ** 2)
            a4 = Ls / (Ls * Lr - Lm ** 2)
            Kvel = 60 * (2 / P) / (2 * np.pi)

            # IF
            # Vmax = f * Vmax / fnom
            # if tipo_alim == 1:
            #     VDC = 1.35 * V * np.sqrt(3) / 2
            #     triang = 2 * np.abs(2 * (t * f_triang - np.floor(0.5 + t * f_triang))) - 1
            #     triang = VDC * triang

            # COORDENADAS DQ
            # wplano=0;
            teta = 0

            # CONSTANTES
            ang120 = np.pi * 2 / 3
            c23 = 2 / 3
            aux_mec = v_nom * 2 * np.pi / 60
            auxT = 3 * P * Lm / 4
            aux_Tv = 3 * P / 4
            aux_Tc = 3 * P * Lm / (4 * Lr)

            # INICIANDO VALORES
            j = 1
            # header = "t,Ias,Ibs,Ics,Iar,Ibr,Icr,Te,Vel,Va,Vb,Vc,If"
            header_output = "t"
            if var[0]:
                V_index = j
                header_output += ",Va,Vb,Vc"
                j += 3
            if var[1]:
                Is_index = j
                header_output += ",Ias,Ibs,Ics"
                j += 3
            if var[2]:
                Ir_index = j
                header_output += ",Iar,Ibr,Icr"
                j += 3
            if var[3]:
                Fs_index = j
                header_output += ",Fas,Fbs,Fcs"
                j += 3
            if var[4]:
                Fr_index = j
                header_output += ",Far,Fbr,Fcr"
                j += 3
            if var[5]:
                Te_index = j
                header_output += ",Te"
                j += 1
            if var[6]:
                vel_index = j
                header_output += ",Vel"
                j += 1

            simu=1
            label_simu=tk.Label(frame_bd,text="Simulations: "+str(simu)+"/"+str(nsimu),font=("Segoe UI", 12))
            label_simu.grid(row=72,columnspan=6)
            header_input="%_load,J_load,ImbalAmp,ImbalAng,mi,nrf,Nºbq,T_fault"
            while simu<=nsimu:
                #ENTRADAS ALEATÓRIAS
                pcarga=round(rd.uniform(pcargamin,pcargamax),2)/100
                J_load=rd.uniform(J_loadmin,J_loadmax)
                deseqamp=round(rd.uniform(deseqampmin,deseqampmax),2)/100
                deseqang = round(rd.uniform(deseqangmin, deseqangmax), 2)*np.pi/180
                mi_=round(rd.uniform(mimin,mimax),2)/100
                nrf=rd.uniform(nrfmin,nrfmax)
                nbq_=rd.randint(nbqmin,nbqmax)
                T_falha_nom=round(rd.uniform(T_falha_nommin,T_falha_nommax),2)/100*Tload_max*pcarga

                # -------------------- CÁLCULOS --------------------#
                K_linear = pcarga * Tload_max * 2 / (v_nom * 2 * np.pi * P / 60)
                K_quad = pcarga * Tload_max * 4 / (v_nom * 2 * np.pi * P / 60) ** 2

                # Cálculo de Rf
                if estado_curto.get():
                    In = nrf * In * np.sqrt(2)
                    Zeq = mi_ * Vmax / In
                    Rquad = Zeq ** 2 - (mi_ * Lls) ** 2
                    if Rquad < 0:
                        rf = 0
                    else:
                        Req = np.sqrt(Rquad)
                        rf = Req - mi_ * rs
                        if rf < 0:
                            rf = 0
                else:
                    rf=0

                # INICIANDO VALORES
                # j-=1
                # if (mi_) > 0:
                #     If_index = j
                #     header_output += ",If"
                #     j += 1
                # print(j)
                Z = np.zeros([j, t.shape[0]], dtype=float)
                tetar = 0
                Te = 0
                u = np.zeros(7, dtype=float)
                k = 0
                c_t = 0
                i_f = 0
                pos = 0
                pos_ant = 0
                w_ant = 0
                wr = 0

                # -------------------- SIMULAÇÃO --------------------#
                for i in t:
                    if not executando:
                        progressobd.destroy()
                        label_simu.destroy()
                        return
                    if tipo_part == 0:
                        if i < tp and c_t == 0:
                            Tload = 0
                            J = J_nom
                            mi = 0
                            nbq = 0
                            T_falha = 0
                            c_t = 1

                            c23mi = c23 * mi
                            c23mirs = c23 * mi * rs
                            mirs = mi * rs
                            mirs3 = mi * rs / 3
                            auxT_mi = P * mi * Lm / 2
                        elif i >= tp and c_t == 1:
                            Tload = pcarga * Tload_max
                            J = J_nom + J_load
                            mi = mi_
                            nbq = nbq_
                            c_t = 2

                            c23mi = c23 * mi
                            c23mirs = c23 * mi * rs
                            mirs = mi * rs
                            mirs3 = mi * rs / 3
                            auxT_mi = P * mi * Lm / 2
                            if mi > 0:
                                miLs_if = mi * Ls
                                miLm_if = mi * Lm
                                den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
                    elif tipo_part == 1:
                        if tipo_carga == 0 and c_t == 0:
                            Tload = pcarga * Tload_max
                            J = J_nom + J_load
                            mi = mi_
                            nbq = nbq_
                            c_t = 2

                            c23mi = c23 * mi
                            c23mirs = c23 * mi * rs
                            mirs = mi * rs
                            mirs3 = mi * rs / 3
                            auxT_mi = P * mi * Lm / 2
                            if mi > 0:
                                miLs_if = mi * Ls
                                miLm_if = mi * Lm
                                den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
                        elif tipo_carga == 1:
                            Tload = K_linear * wr
                            if c_t == 0:
                                J = J_nom + J_load
                                mi = mi_
                                nbq = nbq_
                                c_t = 2

                                c23mi = c23 * mi
                                c23mirs = c23 * mi * rs
                                mirs = mi * rs
                                mirs3 = mi * rs / 3
                                auxT_mi = P * mi * Lm / 2
                                if mi > 0:
                                    miLs_if = mi * Ls
                                    miLm_if = mi * Lm
                                    den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)
                        elif tipo_carga == 2:
                            Tload = K_quad * wr ** 2
                            if c_t == 0:
                                J = J_nom + J_load
                                mi = mi_
                                nbq = nbq_
                                c_t = 2

                                c23mi = c23 * mi
                                c23mirs = c23 * mi * rs
                                mirs = mi * rs
                                mirs3 = mi * rs / 3
                                auxT_mi = P * mi * Lm / 2
                                if mi > 0:
                                    miLs_if = mi * Ls
                                    miLm_if = mi * Lm
                                    den_if = (mi * Lls + 2 * mi ** 2 * Lm / 3)

                    # FALHA MECÂNICA
                    if T_falha_nom > 0 and c_t == 2:
                        T_falha = T_falha_nom * np.cos(aux_mec * i)
                        Tload = Tload_max + T_falha

                    # SINAIS DE TENSÃO
                    va = deseqamp * Vmax * np.cos(we * i + deseqang)
                    vb = Vmax * np.cos(we * i - ang120)
                    vc = (-(va + vb))
                    Vqd = abc2dq(va, vb, vc, teta)
                    vq = Vqd[0, 0]
                    vd = Vqd[1, 0]
                    # v0=Vqd[2,0]
                    vas2 = rf * i_f

                    # RUNGE-KUTTA
                    du1 = RK(u)
                    du2 = RK(u + du1 / 2)
                    du3 = RK(u + du2 / 2)
                    du4 = RK(u + du3)
                    u = u + (du1 + 2 * du2 + 2 * du3 + du4) / 6
                    Fqs = u[0]
                    Fds = u[1]
                    Fqr = u[2]
                    Fdr = u[3]
                    wr = u[4]
                    # F0s=u[5]
                    Fas2 = u[6]

                    # CORRENTES
                    iqs = a1 * Fqs - a2 * Fqr + c23mi * i_f
                    ids = a1 * Fds - a2 * Fdr
                    # ids=a1*Fds-a2*Fdr
                    iqr = a4 * Fqr - a2 * Fqs
                    idr = a4 * Fdr - a2 * Fds
                    if mi > 0:
                        i_f = (-Fas2 + miLs_if * (iqs) + miLm_if * ((iqr))) / den_if

                    # BARRAS QUEBRADAS
                    tetar = (tetar + wr * dt) % (2 * np.pi)
                    aux1 = np.cos(tetar)
                    aux2 = np.sin(tetar)
                    if nbq > 0:
                        iqr_r = iqr * aux1 - idr * aux2
                        idr_r = iqr * aux2 + idr * aux1
                        Irn = np.linalg.inv(Tdq) @ np.concatenate((np.array([[iqr_r], [idr_r]]), aux_barra))
                        media = sum(Irn[2:nbq + 3, 0]) / (nbq + 1)
                        dif = media - Irn[2:nbq + 3, 0]
                        if nivelbq == 1:  # 10%
                            Irn[2:nbq + 3, 0] += dif * 0.1
                        if nivelbq == 2:  # 50%
                            Irn[2:nbq + 3, 0] += dif * 0.5
                        if nivelbq == 3:  # 100%
                            Irn[2:nbq + 3, 0] = np.ones(nbq + 1) * media

                        Ir = Tdq @ Irn
                        idr_r = Ir[1, 0]
                        iqr_r = Ir[0, 0]
                        iqr = iqr_r * aux1 + idr_r * aux2
                        idr = -iqr_r * aux2 + idr_r * aux1

                    # TRANSFORMAÇÂO DAS CORRENTES
                    Iabcs = dq2abc(iqs, ids, 0, teta)
                    if var[2]:
                        Iabcr = dq2abc(iqr, idr, 0, teta - tetar)

                    # Transformação dos Fluxos
                    if var[3]:
                        Fabcs = dq2abc(Fqs, Fds, 0, teta)
                    if var[4]:
                        Fabcr = dq2abc(Fqr, Fdr, 0, teta)

                    # VELOCIDADE DO MOTOR
                    vel = wr * Kvel

                    # TORQUE ELETROMAGNÉTICO
                    Te = auxT * (iqs * idr - ids * iqr) - auxT_mi * i_f * idr

                    # ARMAZENAMENTO
                    p = 1
                    Z[0, k] = i
                    if var[0]:
                        Z[p, k] = va
                        Z[p + 1, k] = vb
                        Z[p + 2, k] = vc
                        p += 3
                    if var[1]:
                        Z[p, k] = float(Iabcs[0, 0])
                        Z[p + 1, k] = float(Iabcs[1, 0])
                        Z[p + 2, k] = float(Iabcs[2, 0])
                        p += 3
                    if var[2]:
                        Z[p, k] = float(Iabcr[0, 0])
                        Z[p + 1, k] = float(Iabcr[1, 0])
                        Z[p + 2, k] = float(Iabcr[2, 0])
                        p += 3
                    if var[3]:
                        Z[p, k] = float(Fabcs[0, 0])
                        Z[p + 1, k] = float(Fabcs[1, 0])
                        Z[p + 2, k] = float(Fabcs[2, 0])
                        p += 3
                    if var[4]:
                        Z[p, k] = float(Fabcr[0, 0])
                        Z[p + 1, k] = float(Fabcr[1, 0])
                        Z[p + 2, k] = float(Fabcr[2, 0])
                        p += 3
                    if var[5]:
                        Z[p, k] = Te
                        p += 1
                    if var[6]:
                        Z[p, k] = vel
                        p += 1
                    # if mi_ > 0:
                    #     Z[p, k] = i_f

                    k = k + 1
                    barra = i / tfinal * 100
                    progressobd["value"] = barra
                    frame_bd.update()

                dados = np.transpose(Z)
                np.savetxt(diretorio_savebd + "/Simu" + str(simu) + "_Output.txt", dados, delimiter=',',
                           header=header_output)
                dados_input=np.array([[pcarga,J_load,deseqamp,deseqang,mi_,nrf,nbq_,T_falha_nom]])
                np.savetxt(diretorio_savebd + "/Simu" + str(simu) + "_Input.txt", dados_input, delimiter=',',
                           header=header_input)
                simu+=1

                progressobd["value"]=0
                label_simu["text"]="Simulations: "+str(simu)+"/"+str(nsimu)
            progressobd.destroy()
            label_simu.destroy()
            botao_stop.pack_forget()
            botao_play.pack(side=tk.LEFT, padx=10, pady=5)

        def parar_simubd():
            global executando
            botao_stopbd.pack_forget()
            botao_playbd.pack(side=tk.LEFT, padx=10, pady=5)
            executando = False

        # ----------------------------------Botão Voltar------------------------------#
        def voltar_princ():
            j3.destroy()
            j1.deiconify()
            j1.state("zoomed")
        botao_voltar = tk.Button(barra_superiorbd, text="Back",font=("Segoe UI", 10), command=voltar_princ, relief=tk.FLAT,
                                  highlightthickness=0, bd=0)
        botao_voltar.pack(side=tk.LEFT, padx=10, pady=5)
        botao_playbd = tk.Button(barra_superiorbd, image=icone_play, command=iniciar_simubd, relief=tk.FLAT)
        botao_playbd.pack(side=tk.LEFT, padx=10, pady=5)
        botao_stopbd = tk.Button(barra_superiorbd, image=icone_stop, command=parar_simubd, relief=tk.FLAT)

        j3.protocol("WM_DELETE_WINDOW",j1.quit)

    # ----------------------------------Configurações da barra superior------------------------------#
    def abrir_menu_arquivo(event):
        menu_arquivo.post(event.x_root, event.y_root)
    menu_arquivo = tk.Menu(barra_superior, tearoff=0)
    menu_arquivo.add_command(label="Open",font=("Segoe UI", 10), command=open_data)
    menu_arquivo.add_command(label="Save",font=("Segoe UI", 10), command=save_data)
    menu_arquivo.add_separator()
    menu_arquivo.add_command(label="Exit",font=("Segoe UI", 10), command=j1.quit)
    botao_arquivo = tk.Button(barra_superior, text="Archive",font=("Segoe UI", 10), relief=tk.FLAT, highlightthickness=0, bd=0)
    botao_arquivo.pack(side=tk.LEFT, padx=10, pady=5)
    botao_arquivo.bind("<Button-1>", abrir_menu_arquivo)
    botao_barraestim = tk.Button(barra_superior, text="Parameter Estimator",font=("Segoe UI", 10), command=estimparamcat, relief=tk.FLAT, highlightthickness=0, bd=0)
    botao_barraestim.pack(side=tk.LEFT, padx=10, pady=5)
    botao_barrabd = tk.Button(barra_superior, text="Database",font=("Segoe UI", 10), command=bdcreator, relief=tk.FLAT, highlightthickness=0, bd=0)
    botao_barrabd.pack(side=tk.LEFT, padx=10, pady=5)

    botao_play = tk.Button(barra_superior, image=icone_play, command=iniciar_simu, relief=tk.FLAT)
    botao_play.pack(side=tk.LEFT, padx=10, pady=5)
    botao_stop = tk.Button(barra_superior, image=icone_stop, command=parar_simu, relief=tk.FLAT)


    # label_tit = tk.Label(frame_entradas, text="Desenvolvedores: Lucas Henrique Gonçalves Ribeiro (lucash.gribeiro@gmail.com), Lane Maria Rabelo (rabelo@ufsj.edu.br)",
    #                      font=("Segoe UI", 8))
    # label_tit.grid(row=50, columnspan=6, sticky='sw')

    j1.mainloop()

#----------------------------------JANELA 0------------------------------#
j0=tk.Tk()
j0.title("MIT-Simulator")
jan_l=800
jan_h=600
tela_l = j0.winfo_screenwidth()
tela_h = j0.winfo_screenheight()
x=(tela_l//2)-(jan_l//2)
y=(tela_h//2)-(jan_h//2)
j0.geometry(f"{jan_l}x{jan_h}+{x}+{y}")

# img_org=Image.open(r"logo_smit.png")
img_org = Image.open(image_path)
escala_im=0.2
img_l=int(img_org.width*escala_im)
img_h=int(img_org.height*escala_im)
img_red=img_org.resize((img_l,img_h),Image.LANCZOS)

tk_image=ImageTk.PhotoImage(img_red)

label_image=tk.Label(j0,image=tk_image)
label_image.place(relx=1.0, rely=-0.05, anchor='ne')
label_image.image = tk_image

label_sigla = tk.Label(j0, text="SMIT", font=("Segoe UI", 36, "bold"))
label_sigla.place(relx=0.5,rely=0.4, anchor='center')

label_tit = tk.Label(j0, text="Simulador do Motor de Indução Trifásico", font=("Segoe UI", 24, "bold"))
label_tit.place(relx=0.5,rely=0.5, anchor='center')

label_tit = tk.Label(j0, text="Three-Phase Induction Motor Simulator", font=("Segoe UI", 18, "bold"))
label_tit.place(relx=0.5,rely=0.6, anchor='center')

label_desen=tk.Label(j0, text="Developed by: Lucas Henrique Gonçalves Ribeiro e Lane Maria Rabelo", font=("Segoe UI",12, "bold"))
label_desen.place(x=0,rely=1.0,anchor='sw')

j0.after(5000,principal)

j0.mainloop()