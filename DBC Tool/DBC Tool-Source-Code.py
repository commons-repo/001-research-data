"""
=========================================================
 Developed and written by: Angkush Kumar Ghosh
 Contact: ghosh-ak@mail.kitami-it.ac.jp
=========================================================
 Related Work:
 https://www.preprints.org/manuscript/202507.0713/v1
=========================================================
 Description:
 This script was developed as part of research on
 bioinspired computing (DBC + ANN) for pattern recognition
 in smart manufacturing applications.
=========================================================
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import json
import tkinter.font as tkFont
import matplotlib as mpl
mpl.rcParams["font.family"] = "serif"
mpl.rcParams["font.serif"] = ["Times New Roman"]
mpl.rcParams["mathtext.fontset"] = "custom"
mpl.rcParams["mathtext.rm"] = "Times New Roman"
mpl.rcParams["mathtext.it"] = "Times New Roman:italic"
mpl.rcParams["mathtext.bf"] = "Times New Roman:bold"

# Global Variables
canvas = None
hyp_set = False
conv_canvas = None
loaded_data = None
dataset_id = None

# Hyperparameter globals:
mu = sigma = 0
R1 = R2 = R3 = 0
a = b = c = d = 0
A_R1 = A_R2 = A_R3 = 0
B_R1 = B_R2 = B_R3 = 0
C_R1 = C_R2 = C_R3 = 0
D_R1 = D_R2 = D_R3 = 0

# Functions
def init_empty_canvas():
    global canvas
    fig = Figure(figsize=(6, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, "No data Loaded", ha="center", va="center", color="gray", fontsize=11)
    ax.axis('off')
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().configure(borderwidth=0.5, relief="solid")
    canvas.get_tk_widget().pack()

def init_empty_conv_canvas():
    global conv_canvas
    fig = Figure(figsize=(6, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, "No data Loaded", ha="center", va="center", color="gray", fontsize=11)
    ax.axis('off')
    conv_canvas = FigureCanvasTkAgg(fig, master=conv_plot_frame)
    conv_canvas.get_tk_widget().configure(borderwidth=0.5, relief="solid")
    conv_canvas.get_tk_widget().pack()

def update_reference_lines():    
    if loaded_data is None:
        return
    fig = canvas.figure
    ax = fig.axes[0]
    ax.clear()
    ax.plot(loaded_data, linewidth=0.7, color="black") 
    ax.set_xlabel(r"$\it{i}$", fontdict={"fontname": "Times New Roman", "fontsize": 11, "color": "gray"})
    ax.set_ylabel(r"$\it{x}$($\it{i}$)", fontdict={"fontname": "Times New Roman", "fontsize": 11, "color": "gray"})
    ax.tick_params(axis='both', labelsize=8, colors="gray")
    ax.grid(False)
    fig.tight_layout()
    canvas.draw()

def load_data():
    global loaded_data, dataset_id, canvas
    filename = filedialog.askopenfilename(
        title="Select a Data File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not filename:
        return    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        if len(lines) < 4:
            messagebox.showerror("Error", "The file does not have the required structure.")
            return        
        common_metadata = {}
        try:
            common_metadata["Data Type"] = lines[0].strip().split(": ")[1]
        except IndexError:
            common_metadata["Data Type"] = "N/A"
        try:
            common_metadata["Condition"] = lines[1].strip().split(": ")[1]
        except IndexError:
            common_metadata["Condition"] = "N/A"
        try:
            dataset_id = lines[2].strip().split(": ")[1]
        except IndexError:
            dataset_id = "Unknown"
        numerical_data = []
        for line in lines[3:]:
            try:
                numerical_data.append(float(line.strip()))
            except ValueError:
                continue
        if not numerical_data:
            messagebox.showerror("Error", "No numerical data found in the file.")
            return
        loaded_data = numerical_data
        fig = Figure(figsize=(6, 2.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(numerical_data, linewidth=0.7, color="black")
        ax.set_xlabel(r"$\it{i}$", fontdict={"fontname": "Times New Roman","fontsize": 11,"color": "gray"})
        ax.set_ylabel(r"$\it{x}$($\it{i}$)",fontdict={"fontname": "Times New Roman","fontsize": 11,"color": "gray"})        
        ax.tick_params(axis='both', labelsize=8, colors="gray")
        ax.grid(False)
        fig.tight_layout()
        if canvas is None:
            canvas = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas.get_tk_widget().configure(borderwidth=0.5, relief="solid")
            canvas.get_tk_widget().pack()
        else:
            canvas.figure = fig
            canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_param():
    global mu, sigma, R1, R2, R3, a, b, c, d
    global A_R1, A_R2, A_R3, B_R1, B_R2, B_R3, C_R1, C_R2, C_R3, D_R1, D_R2, D_R3
    return (f"R1 = {R1:.3f}, R2 = {R2:.3f}, R3 = {R3:.3f}\n\n"
            f"∀R ∈{{R1, R2, R3}}\n\n"
            f"a = {{{A_R1:.3f}, {A_R2:.3f}, {A_R3:.3f}}}\n"
            f"b = {{{B_R1:.3f}, {B_R2:.3f}, {B_R3:.3f}}}\n"
            f"c = {{{C_R1:.3f}, {C_R2:.3f}, {C_R3:.3f}}}\n"
            f"d = {{{D_R1:.3f}, {D_R2:.3f}, {D_R3:.3f}}}")

def show_parameters_popup(event=None):
    param_text = display_param()
    param_popup = tk.Toplevel(root)
    param_popup.iconbitmap("icon-png.ico")
    param_popup.title("Parameters")
    param_popup.geometry("400x250")    
    text_frame = tk.Frame(param_popup)
    text_frame.pack(fill="both", expand=True, padx=10, pady=10)    
    text_area = tk.Text(text_frame, wrap="word", font=("Courier New", 9))
    text_area.pack(side="left", fill="both", expand=True)    
    scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)    
    text_area.insert("1.0", param_text)
    text_area.config(state="disabled")

def set_parameters_popup():
    popup = tk.Toplevel(root)
    popup.iconbitmap("icon-png.ico")
    popup.title("Set Parameters")
    popup.geometry("450x450")
        
    def update_mode(mode_var, container, def_frame, mod_frame, dir_frame):
        for widget in container.winfo_children():
            widget.pack_forget()
        mode = mode_var.get()
        if mode == "default":
            def_frame.pack(fill="both", expand=True)
        elif mode == "modify":
            mod_frame.pack(fill="both", expand=True)
        elif mode == "direct":
            dir_frame.pack(fill="both", expand=True)
        
    def update_direct_mode():
        if direct_option_var.get() == "same":
            same_frame.pack(fill="x", pady=5)
            different_frame.pack_forget()
        else:
            same_frame.pack_forget()
            different_frame.pack(fill="x", pady=5)
        
    top_mode_frame = tk.Frame(popup)
    top_mode_frame.pack(fill="x", pady=10)
    mode_var = tk.StringVar(value="default")
    tk.Label(top_mode_frame, text="Select Mode:").pack(side="left", padx=5)
    tk.Radiobutton(top_mode_frame, text="Default", variable=mode_var, value="default",
                   command=lambda: update_mode(mode_var, input_container, default_frame, modify_frame, direct_frame)
                  ).pack(side="left", padx=5)
    tk.Radiobutton(top_mode_frame, text="Modify Equation", variable=mode_var, value="modify",
                   command=lambda: update_mode(mode_var, input_container, default_frame, modify_frame, direct_frame)
                  ).pack(side="left", padx=5)
    tk.Radiobutton(top_mode_frame, text="Direct Input", variable=mode_var, value="direct",
                   command=lambda: update_mode(mode_var, input_container, default_frame, modify_frame, direct_frame)
                  ).pack(side="left", padx=5)
        
    input_container = tk.Frame(popup)
    input_container.pack(fill="both", expand=True, padx=10)
    
    default_frame = tk.Frame(input_container)
    tk.Label(default_frame, text="μ:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    default_mu_entry = tk.Entry(default_frame, width=10)
    default_mu_entry.grid(row=0, column=1, padx=5, pady=5)
    if mu != 0:
        default_mu_entry.insert(0, str(mu))
    tk.Label(default_frame, text="σ:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    default_sigma_entry = tk.Entry(default_frame, width=10)
    default_sigma_entry.grid(row=1, column=1, padx=5, pady=5)
    if sigma != 0:
        default_sigma_entry.insert(0, str(sigma))
    tk.Label(default_frame, text="Default Equations:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="R1 = μ").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="R2 = μ + 4σ").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="R3 = μ - 4σ").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="a = 2.5σ").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="b = 1.5σ").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="c = −1.5σ").grid(row=8, column=0, sticky="e", padx=5, pady=5)
    tk.Label(default_frame, text="d = −2.5σ").grid(row=9, column=0, sticky="e", padx=5, pady=5)
    
    modify_frame = tk.Frame(input_container)
    tk.Label(modify_frame, text="μ ( = R1):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    mod_mu_entry = tk.Entry(modify_frame, width=10)
    mod_mu_entry.grid(row=0, column=1, padx=5, pady=5)
    if mu != 0:
        mod_mu_entry.insert(0, str(mu))
    tk.Label(modify_frame, text="σ:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    mod_sigma_entry = tk.Entry(modify_frame, width=10)
    mod_sigma_entry.grid(row=1, column=1, padx=5, pady=5)
    if sigma != 0:
        mod_sigma_entry.insert(0, str(sigma))
    tk.Label(modify_frame, text="R2 ( = μ + m·σ). Insert 'm':").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    r2_mult_entry = tk.Entry(modify_frame, width=10)
    r2_mult_entry.grid(row=2, column=1, padx=5, pady=5)
    if sigma != 0:
        m = (R2 - mu) / sigma if R2 != 0 else 4
        r2_mult_entry.insert(0, str(m))
    else:
        r2_mult_entry.insert(0, "4")
    tk.Label(modify_frame, text="R3 ( = μ − n·σ). Insert 'n':").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    r3_mult_entry = tk.Entry(modify_frame, width=10)
    r3_mult_entry.grid(row=3, column=1, padx=5, pady=5)
    if sigma != 0:
        n = (mu - R3) / sigma if R3 != 0 else 4
        r3_mult_entry.insert(0, str(n))
    else:
        r3_mult_entry.insert(0, "4")
    tk.Label(modify_frame, text="a ( = α·σ). Insert 'α':").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    a_mult_entry = tk.Entry(modify_frame, width=10)
    a_mult_entry.grid(row=4, column=1, padx=5, pady=5)
    if sigma != 0 and A_R1 != 0:
        a_mult_entry.insert(0, str(A_R1 / sigma))
    else:
        a_mult_entry.insert(0, "2.5")
    tk.Label(modify_frame, text="b ( = β·σ). Insert 'β':").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    b_mult_entry = tk.Entry(modify_frame, width=10)
    b_mult_entry.grid(row=5, column=1, padx=5, pady=5)
    if sigma != 0 and B_R1 != 0:
        b_mult_entry.insert(0, str(B_R1 / sigma))
    else:
        b_mult_entry.insert(0, "1.5")
    tk.Label(modify_frame, text="c ( = γ·σ). Insert 'γ':").grid(row=6, column=0, sticky="e", padx=5, pady=5)
    c_mult_entry = tk.Entry(modify_frame, width=10)
    c_mult_entry.grid(row=6, column=1, padx=5, pady=5)
    if sigma != 0 and C_R1 != 0:
        c_mult_entry.insert(0, str(C_R1 / sigma))
    else:
        c_mult_entry.insert(0, "-1.5")
    tk.Label(modify_frame, text="d ( = δ·σ). Insert 'δ':").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    d_mult_entry = tk.Entry(modify_frame, width=10)
    d_mult_entry.grid(row=7, column=1, padx=5, pady=5)
    if sigma != 0 and D_R1 != 0:
        d_mult_entry.insert(0, str(D_R1 / sigma))
    else:
        d_mult_entry.insert(0, "-2.5")
        
    direct_frame = tk.Frame(input_container)    
    direct_option_var = tk.StringVar(value="same")
    option_frame = tk.Frame(direct_frame)
    option_frame.pack(fill="x", pady=5)
    tk.Label(option_frame, text="Direct Input Sub‑Mode:", font=custom_font).pack(side="left", padx=5)
    tk.Radiobutton(option_frame, text="Same Values", variable=direct_option_var, value="same", font=custom_font,
                   command=update_direct_mode).pack(side="left", padx=5)
    tk.Radiobutton(option_frame, text="Different Values", variable=direct_option_var, value="different", font=custom_font,
                   command=update_direct_mode).pack(side="left", padx=5)    
    same_frame = tk.Frame(direct_frame)
    different_frame = tk.Frame(direct_frame)
    
    tk.Label(same_frame, text="R:", font=custom_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    r_entry = tk.Entry(same_frame, width=10)
    r_entry.grid(row=0, column=1, padx=5, pady=5)
    if R1 != 0:
        r_entry.insert(0, str(R1))
    tk.Label(same_frame, text="a:", font=custom_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    a_same_entry = tk.Entry(same_frame, width=10)
    a_same_entry.grid(row=1, column=1, padx=5, pady=5)
    if A_R1 != 0:
        a_same_entry.insert(0, str(A_R1))
    tk.Label(same_frame, text="b:", font=custom_font).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    b_same_entry = tk.Entry(same_frame, width=10)
    b_same_entry.grid(row=2, column=1, padx=5, pady=5)
    if B_R1 != 0:
        b_same_entry.insert(0, str(B_R1))
    tk.Label(same_frame, text="c:", font=custom_font).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    c_same_entry = tk.Entry(same_frame, width=10)
    c_same_entry.grid(row=3, column=1, padx=5, pady=5)
    if C_R1 != 0:
        c_same_entry.insert(0, str(C_R1))
    tk.Label(same_frame, text="d:", font=custom_font).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    d_same_entry = tk.Entry(same_frame, width=10)
    d_same_entry.grid(row=4, column=1, padx=5, pady=5)
    if D_R1 != 0:
        d_same_entry.insert(0, str(D_R1))
    
    r1_frame = tk.Frame(different_frame, borderwidth=1, relief="solid", padx=5, pady=5)
    r2_frame = tk.Frame(different_frame, borderwidth=1, relief="solid", padx=5, pady=5)
    r3_frame = tk.Frame(different_frame, borderwidth=1, relief="solid", padx=5, pady=5)

    r1_frame.grid(row=0, column=0, padx=5, sticky="n")
    r2_frame.grid(row=0, column=1, padx=5, sticky="n")
    r3_frame.grid(row=0, column=2, padx=5, sticky="n")
    
    tk.Label(r1_frame, text="R1:", font=custom_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    r1_entryD = tk.Entry(r1_frame, width=10)
    r1_entryD.grid(row=0, column=1, padx=5, pady=5)
    if R1 != 0:
        r1_entryD.insert(0, str(R1))
    tk.Label(r1_frame, text="a:", font=custom_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    a_entryD = tk.Entry(r1_frame, width=10)
    a_entryD.grid(row=1, column=1, padx=5, pady=5)
    if A_R1 != 0:
        a_entryD.insert(0, str(A_R1))
    tk.Label(r1_frame, text="b:", font=custom_font).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    b_entryD = tk.Entry(r1_frame, width=10)
    b_entryD.grid(row=2, column=1, padx=5, pady=5)
    if B_R1 != 0:
        b_entryD.insert(0, str(B_R1))
    tk.Label(r1_frame, text="c:", font=custom_font).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    c_entryD = tk.Entry(r1_frame, width=10)
    c_entryD.grid(row=3, column=1, padx=5, pady=5)
    if C_R1 != 0:
        c_entryD.insert(0, str(C_R1))
    tk.Label(r1_frame, text="d:", font=custom_font).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    d_entryD = tk.Entry(r1_frame, width=10)
    d_entryD.grid(row=4, column=1, padx=5, pady=5)
    if D_R1 != 0:
        d_entryD.insert(0, str(D_R1))
    
    tk.Label(r2_frame, text="R2:", font=custom_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    r2_entryD = tk.Entry(r2_frame, width=10)
    r2_entryD.grid(row=0, column=1, padx=5, pady=5)
    if R2 != 0:
        r2_entryD.insert(0, str(R2))
    tk.Label(r2_frame, text="a:", font=custom_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    a_entryD2 = tk.Entry(r2_frame, width=10)
    a_entryD2.grid(row=1, column=1, padx=5, pady=5)
    if A_R2 != 0:
        a_entryD2.insert(0, str(A_R2))
    tk.Label(r2_frame, text="b:", font=custom_font).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    b_entryD2 = tk.Entry(r2_frame, width=10)
    b_entryD2.grid(row=2, column=1, padx=5, pady=5)
    if B_R2 != 0:
        b_entryD2.insert(0, str(B_R2))
    tk.Label(r2_frame, text="c:", font=custom_font).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    c_entryD2 = tk.Entry(r2_frame, width=10)
    c_entryD2.grid(row=3, column=1, padx=5, pady=5)
    if C_R2 != 0:
        c_entryD2.insert(0, str(C_R2))
    tk.Label(r2_frame, text="d:", font=custom_font).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    d_entryD2 = tk.Entry(r2_frame, width=10)
    d_entryD2.grid(row=4, column=1, padx=5, pady=5)
    if D_R2 != 0:
        d_entryD2.insert(0, str(D_R2))
    
    tk.Label(r3_frame, text="R3:", font=custom_font).grid(row=0, column=0, sticky="e", padx=5, pady=5)
    r3_entryD = tk.Entry(r3_frame, width=10)
    r3_entryD.grid(row=0, column=1, padx=5, pady=5)
    if R3 != 0:
        r3_entryD.insert(0, str(R3))
    tk.Label(r3_frame, text="a:", font=custom_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    a_entryD3 = tk.Entry(r3_frame, width=10)
    a_entryD3.grid(row=1, column=1, padx=5, pady=5)
    if A_R3 != 0:
        a_entryD3.insert(0, str(A_R3))
    tk.Label(r3_frame, text="b:", font=custom_font).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    b_entryD3 = tk.Entry(r3_frame, width=10)
    b_entryD3.grid(row=2, column=1, padx=5, pady=5)
    if B_R3 != 0:
        b_entryD3.insert(0, str(B_R3))
    tk.Label(r3_frame, text="c:", font=custom_font).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    c_entryD3 = tk.Entry(r3_frame, width=10)  
    c_entryD3.grid(row=3, column=1, padx=5, pady=5)
    if C_R3 != 0:
        c_entryD3.insert(0, str(C_R3))
    tk.Label(r3_frame, text="d:", font=custom_font).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    d_entryD3 = tk.Entry(r3_frame, width=10)
    d_entryD3.grid(row=4, column=1, padx=5, pady=5)
    if D_R3 != 0:
        d_entryD3.insert(0, str(D_R3))
    
    update_direct_mode()
    
    direct_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    bottom_frame = tk.Frame(popup)
    bottom_frame.pack(side="bottom", fill="x", pady=10)
    
    update_mode(mode_var, input_container, default_frame, modify_frame, direct_frame)
    
    def calculate_and_set_params():
        global mu, sigma, R1, R2, R3, a, b, c, d
        global A_R1, A_R2, A_R3, B_R1, B_R2, B_R3, C_R1, C_R2, C_R3, D_R1, D_R2, D_R3, hyp_set
        mode = mode_var.get()
        if mode == "default":
            if default_mu_entry.get() == "" or default_sigma_entry.get() == "":
                messagebox.showinfo("Missing", "Please enter values for μ and σ.")
                return
            try:
                mu = float(default_mu_entry.get())
                sigma = float(default_sigma_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid numerical values for μ or σ.")
                return
            if mu == 0 or sigma == 0:
                messagebox.showinfo("Missing", "Please enter nonzero values for μ and σ.")
                return
            R1 = mu
            R2 = mu + 4 * sigma
            R3 = mu - 4 * sigma
            a = 2.5 * sigma
            b = 1.5 * sigma
            c = -1.5 * sigma
            d = -2.5 * sigma
            
            if not (a > 0 and b > 0 and c < 0 and d < 0 and a > b and c > d):
                messagebox.showerror("Error", "Conversion boundaries must satisfy:\n"
                                    "a and b > 0 with a > b,\n"
                                    "c and d < 0 with c > d.")
                return
        elif mode == "modify":
            if mod_mu_entry.get() == "" or mod_sigma_entry.get() == "":
                messagebox.showinfo("Missing", "Please enter base values for μ and σ.")
                return
            try:
                mu = float(mod_mu_entry.get())
                sigma = float(mod_sigma_entry.get())
                r2_mult = float(r2_mult_entry.get())
                r3_mult = float(r3_mult_entry.get())
                a_mult = float(a_mult_entry.get())
                b_mult = float(b_mult_entry.get())
                c_mult = float(c_mult_entry.get())
                d_mult = float(d_mult_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid values in Modify Equation mode.")
                return
            R1 = mu
            R2 = mu + r2_mult * sigma
            R3 = mu - r3_mult * sigma
            a = a_mult * sigma
            b = b_mult * sigma
            c = c_mult * sigma
            d = d_mult * sigma
            
            if not (a > 0 and b > 0 and c < 0 and d < 0 and a > b and c > d):
                messagebox.showerror("Error", "Conversion boundaries must satisfy:\n"
                                    "a and b > 0 with a > b,\n"
                                    "c and d < 0 with c > d.")
                return
        elif mode == "direct":
            if direct_option_var.get() == "same":
                try:
                    common_R = float(r_entry.get())
                    common_a = float(a_same_entry.get())
                    common_b = float(b_same_entry.get())
                    common_c = float(c_same_entry.get())
                    common_d = float(d_same_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid input in 'Same Values' Direct mode.")
                    return
                
                if not (common_a > 0 and common_b > 0 and common_a > common_b and
                        common_c < 0 and common_d < 0 and common_c > common_d):
                    messagebox.showerror("Error", "Conversion boundaries must satisfy:\n"
                                        "  a and b > 0 with a > b,\n"
                                        "  c and d < 0 with c > d.")
                    return
                R1 = R2 = R3 = common_R
                A_R1 = A_R2 = A_R3 = common_a
                B_R1 = B_R2 = B_R3 = common_b
                C_R1 = C_R2 = C_R3 = common_c
                D_R1 = D_R2 = D_R3 = common_d
            else:
                try:
                    R1 = float(r1_entryD.get())
                    R2 = float(r2_entryD.get())
                    R3 = float(r3_entryD.get())
                    a1 = float(a_entryD.get())
                    b1 = float(b_entryD.get())
                    c1 = float(c_entryD.get())
                    d1 = float(d_entryD.get())
                    a2 = float(a_entryD2.get())
                    b2 = float(b_entryD2.get())
                    c2 = float(c_entryD2.get())
                    d2 = float(d_entryD2.get())
                    a3 = float(a_entryD3.get())
                    b3 = float(b_entryD3.get())
                    c3 = float(c_entryD3.get())
                    d3 = float(d_entryD3.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid values in Direct Input mode.")
                    return
                                
                if not (a1 > 0 and b1 > 0 and a1 > b1 and c1 < 0 and d1 < 0 and c1 > d1):
                    messagebox.showerror("Error", "For R1, conversion boundaries must satisfy:\n"
                                        "  a and b > 0 with a > b,\n"
                                        "  c and d < 0 with c > d.")
                    return
                if not (a2 > 0 and b2 > 0 and a2 > b2 and c2 < 0 and d2 < 0 and c2 > d2):
                    messagebox.showerror("Error", "For R2, conversion boundaries must satisfy:\n"
                                        "  a and b > 0 with a > b,\n"
                                        "  c and d < 0 with c > d.")
                    return
                if not (a3 > 0 and b3 > 0 and a3 > b3 and c3 < 0 and d3 < 0 and c3 > d3):
                    messagebox.showerror("Error", "For R3, conversion boundaries must satisfy:\n"
                                        "  a and b > 0 with a > b,\n"
                                        "  c and d < 0 with c > d.")
                    return             

                A_R1, A_R2, A_R3 = a1, a2, a3
                B_R1, B_R2, B_R3 = b1, b2, b3
                C_R1, C_R2, C_R3 = c1, c2, c3
                D_R1, D_R2, D_R3 = d1, d2, d3
        if mode in ["default", "modify"]:
            A_R1 = A_R2 = A_R3 = a
            B_R1 = B_R2 = B_R3 = b
            C_R1 = C_R2 = C_R3 = c
            D_R1 = D_R2 = D_R3 = d
        hyp_set = True
        messagebox.showinfo("Success", "Parameters have been set.")
        popup.destroy()
        update_reference_lines()
    
    tk.Button(bottom_frame, text="Calculate & Set", font=custom_font, command=calculate_and_set_params).pack(pady=10)

def show_dna_forming_rules_popup():
    popup = tk.Toplevel(root)
    popup.iconbitmap("icon-png.ico")
    popup.title("DNA-Forming Rules")
    popup.geometry("600x700")    
    explanation_frame = tk.Frame(popup)
    explanation_frame.pack(fill="both", expand=True, padx=10, pady=10)
    explanation_text = tk.Text(explanation_frame, wrap="word", font=("Courier New", 9))
    explanation_text.pack(side="left", fill="both", expand=True)    
    scrollbar = tk.Scrollbar(explanation_frame, command=explanation_text.yview)
    scrollbar.pack(side="right", fill="y")
    explanation_text.config(yscrollcommand=scrollbar.set)
    explanation = (
        "Calculating DNA-Forming Rules from User-Defined Parameters:\n\n"
        "1. User-Defined Parameters:\n\n"
        "   a. Default Mode:\n"
        "      - The values for μ (the mean) and σ (the standard deviation) are provided.\n"
        "      - The system then calculates the following parameters:\n"
        "           R₁ = μ\n"
        "           R₂ = μ + 4σ\n"
        "           R₃ = μ − 4σ\n"
        "           a = 2.5σ,  b = 1.5σ,  c = −1.5σ,  d = −2.5σ\n"
        "      - These computed values serve as the final parameters for data conversion.\n\n"
        "   b. Modify Equation Mode:\n"
        "      - Base values for μ and σ are provided, along with multipliers:\n"
        "           R₁ = μ\n"
        "           For R₂: a multiplier m, so that R₂ = μ + m·σ\n"
        "           For R₃: a multiplier n, so that R₃ = μ − n·σ\n"
        "           For the conversion boundaries: multipliers α, β, γ, δ such that\n"
        "                 a = α·σ,  b = β·σ,  c = γ·σ,  d = δ·σ\n"
        "      - These calculations yield the final parameters in this mode.\n\n"
        "   c. Direct Input Mode:\n"
        "      - The values for R₁, R₂, R₃ and for the boundaries a, b, c, d are entered directly,without further calculation.\n\n"
        "In all modes, the final set of parameters used are:\n"
        "   - The reference values: R₁, R₂, R₃\n"
        "   - Their respective conversion boundaries: a, b, c, and d\n"
        "   - Note that conversion boundaries must satisfy: (1) a and b > 0 with a > b. (2) c and d < 0 with c > d.\n\n"
        "2. DNA-Forming Rules:\n\n"
        "   - For each data point in the loaded dataset, the difference between the data point and a selected reference value (R) is computed.\n\n"
        "   - Each difference is then converted into a DNA nucleotide according to the following rules:\n"
        "         • If c < Difference < b, then assign 'A'.\n"
        "         • If b ≤ Difference ≤ a, then assign 'C'.\n"
        "         • If d ≤ Difference ≤ c, then assign 'G'.\n"
        "         • If Difference > a or Difference < d, then assign 'T'.\n\n"
        "   - This conversion transforms the entire array of differences into a strand (a string of nucleotides) for each reference (R₁, R₂, and R₃).\n\n"
    )
    explanation_text.insert("1.0", explanation)
    explanation_text.config(state="disabled")

def visualize_conversion_rules_embedded(selected):
    global conv_canvas, conv_plot_frame, loaded_data
    if loaded_data is None:
        messagebox.showerror("Error", "No data loaded. Please load data first.")
        return
    
    if selected == "R1":
        R = R1; A_val = A_R1; B_val = B_R1; C_val = C_R1; D_val = D_R1
    elif selected == "R2":
        R = R2; A_val = A_R2; B_val = B_R2; C_val = C_R2; D_val = D_R2
    elif selected == "R3":
        R = R3; A_val = A_R3; B_val = B_R3; C_val = C_R3; D_val = D_R3
    else:
        messagebox.showerror("Error", "Invalid reference selection.")
        return

    diff_data = np.array(loaded_data) - R

    fig = Figure(figsize=(6, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(diff_data, linewidth=0.7)
    ax.set_xlabel(r"$\it{i}$", fontdict={"fontname": "Times New Roman","fontsize": 11,"color": "gray"})
    ax.set_ylabel("Difference", fontdict={"fontname": "Times New Roman","fontsize": 11,"color": "gray"})
    ax.tick_params(axis='both', labelsize=8, colors="gray")
    ax.grid(False)
    fig.tight_layout()

    ax.axhline(y=A_val, color='black', linestyle='--', lw=0.5)
    ax.annotate(f'a', xy=(0.01, A_val), xycoords=('axes fraction','data'),
                xytext=(0, 5), textcoords='offset points', ha='left', va='center', fontsize=11)
    ax.axhline(y=B_val, color='black', linestyle='--', lw=0.5)
    ax.annotate(f'b', xy=(0.01, B_val), xycoords=('axes fraction','data'),
                xytext=(0, 5), textcoords='offset points', ha='left', va='center', fontsize=11)
    ax.axhline(y=C_val, color='black', linestyle='--', lw=0.5)
    ax.annotate(f'c', xy=(0.01, C_val), xycoords=('axes fraction','data'),
                xytext=(0, 5), textcoords='offset points', ha='left', va='center', fontsize=11)
    ax.axhline(y=D_val, color='black', linestyle='--', lw=0.5)
    ax.annotate(f'd', xy=(0.01, D_val), xycoords=('axes fraction','data'),
                xytext=(0, 5), textcoords='offset points', ha='left', va='center', fontsize=11)

    xmin, xmax = ax.get_xlim()
    shading_start = xmax - 0.05*(xmax - xmin)
    shading_end = xmax
    ax.fill_between([shading_start, shading_end], C_val, B_val, color='purple', alpha=0.3)
    ax.text((shading_start+xmax)/2, (C_val+B_val)/2, 'A', ha='center', va='center', fontsize=11)
    ax.fill_between([shading_start, shading_end], B_val, A_val, color='green', alpha=0.3)
    ax.text((shading_start+xmax)/2, (B_val+A_val)/2, 'C', ha='center', va='center', fontsize=11)
    ax.fill_between([shading_start, shading_end], D_val, C_val, color='blue', alpha=0.3)
    ax.text((shading_start+xmax)/2, (D_val+C_val)/2, 'G', ha='center', va='center', fontsize=11)
    y_bottom = ax.get_ylim()[0]
    ax.fill_between([shading_start, shading_end], y_bottom, D_val, color='red', alpha=0.3)
    ax.text((shading_start+xmax)/2, (y_bottom+D_val)/2, 'T', ha='center', va='center', fontsize=11)
    y_top = ax.get_ylim()[1]
    ax.fill_between([shading_start, shading_end], A_val, y_top, color='red', alpha=0.3)
    ax.text((shading_start+xmax)/2, (A_val+y_top)/2, 'T', ha='center', va='center', fontsize=11)  

    global conv_canvas
    if conv_canvas is not None:
        conv_canvas.get_tk_widget().destroy()
    conv_canvas = FigureCanvasTkAgg(fig, master=conv_plot_frame)
    conv_canvas.get_tk_widget().configure(borderwidth=0.5, relief="solid")
    conv_canvas.get_tk_widget().pack()

def create_difference_data(final_individual_file_data, R_values):    
    difference_data = {}
    dataset = final_individual_file_data[0]  # our only dataset
    for key in R_values:
        R_value = R_values[key]
        differences = [x - R_value for x in dataset['Numerical Data']]
        difference_data[key] = differences
    return difference_data

def create_strand_data(difference_data, A_values, B_values, C_values, D_values):    
    strand_data = {}
    for key in difference_data:
        diffs = difference_data[key]
        strand = ""
        for diff in diffs:
            if C_values[key] < diff < B_values[key]:
                strand += 'A'
            elif B_values[key] <= diff <= A_values[key]:
                strand += 'C'
            elif D_values[key] <= diff <= C_values[key]:
                strand += 'G'
            elif diff > A_values[key] or diff < D_values[key]:
                strand += 'T'
        strand_data[key] = strand
    return strand_data

def create_dna_strand(strand_R1, strand_R2, strand_R3):    
    dna_strand = ""
    length = len(strand_R1)
    for i in range(length):
        dna_strand += strand_R1[i] + strand_R2[i] + strand_R3[i]
    return dna_strand

def compute_DNA_strand():    
    global hyp_set, loaded_data, R1, R2, R3
    global A_R1, A_R2, A_R3, B_R1, B_R2, B_R3, C_R1, C_R2, C_R3, D_R1, D_R2, D_R3

    if loaded_data is None:
        print("Error: No data loaded. Please load data first.")
        return None
    if not hyp_set:
        print("Error: Hyperparameters not set. Please set parameters before computing DNA strands.")
        return None

    final_individual_file_data = [{'Dataset ID': dataset_id, 'Numerical Data': loaded_data}]

    R_values = {'R1': R1, 'R2': R2, 'R3': R3}
    A_values = {'R1': A_R1, 'R2': A_R2, 'R3': A_R3}
    B_values = {'R1': B_R1, 'R2': B_R2, 'R3': B_R3}
    C_values = {'R1': C_R1, 'R2': C_R2, 'R3': C_R3}
    D_values = {'R1': D_R1, 'R2': D_R2, 'R3': D_R3}

    diff_data = create_difference_data(final_individual_file_data, R_values)
   
    strand_data = create_strand_data(diff_data, A_values, B_values, C_values, D_values)
   
    strand_R1 = strand_data['R1']
    strand_R2 = strand_data['R2']
    strand_R3 = strand_data['R3']
    
    dna_strand = create_dna_strand(strand_R1, strand_R2, strand_R3)    
    
    print("Final DNA Strand:", dna_strand)
    return {"DNA(R1)": strand_R1, "DNA(R2)": strand_R2, "DNA(R3)": strand_R3, "DNA": dna_strand}

def form_dna():
    result = compute_DNA_strand()
    dna_text_area.config(state="normal")
    if result is None:
        return
    dna_text_area.delete("1.0", tk.END)

    def truncate_strand(s):
        return s if len(s) <= 200 else s[:200] + "..."
    
    dna1_display = truncate_strand(result['DNA(R1)'])
    dna2_display = truncate_strand(result['DNA(R2)'])
    dna3_display = truncate_strand(result['DNA(R3)'])
    
    dna_text_area.insert(tk.END, f"DNA1: {dna1_display}\n\n", "R1")
    dna_text_area.insert(tk.END, f"DNA2: {dna2_display}\n\n", "R2")
    dna_text_area.insert(tk.END, f"DNA3: {dna3_display}\n\n", "R3")

    dna_text_area.config(state="disabled")

def form_mrna():    
    result = compute_DNA_strand()
    if result is None:
        return
    mrna_text_area.config(state="normal")
    mrna_text_area.delete("1.0", tk.END)
    mrna_text_area.insert(tk.END, "mRNA: ")
    final_strand = result["DNA"]

    if len(final_strand) > 600:
        display_strand = final_strand[:600] + "..."
    else:
        display_strand = final_strand

    for i, ch in enumerate(display_strand):
        if i % 3 == 0:
            tag = "R1"
        elif i % 3 == 1:
            tag = "R2"
        else:
            tag = "R3"
        mrna_text_area.insert(tk.END, ch, tag)
    
    mrna_text_area.insert(tk.END, "\n")
    mrna_text_area.config(state="disabled")

def show_mrna_rule():
    rule_popup = tk.Toplevel(root)
    rule_popup.iconbitmap("icon-png.ico")
    rule_popup.title("mRNA-Forming Rule")
    rule_popup.geometry("600x300")
    
    rule_frame = tk.Frame(rule_popup)
    rule_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    rule_text = tk.Text(rule_frame, wrap="word", font=("Courier New", 9))
    rule_text.pack(side="left", fill="both", expand=True)
    
    rule_scrollbar = tk.Scrollbar(rule_frame, command=rule_text.yview)
    rule_scrollbar.pack(side="right", fill="y")
    rule_text.config(yscrollcommand=rule_scrollbar.set)
    
    explanation = (
        "mRNA-Forming Rule:\n\n"
        "Let DNA1, DNA2, and DNA3 be the individual strands computed for references R1, R2, and R3, respectively.\n\n"
        "For each sample index i, the final mRNA is constructed by concatenating the corresponding characters:\n"
        "    mRNA[i] = DNA1[i] + DNA2[i] + DNA3[i]\n\n"
        "Thus, if DNA1 = A₁A₂A₃…, DNA2 = B₁B₂B₃…, and DNA3 = C₁C₂C₃…, then:\n"
        "    mRNA = A₁B₁C₁ A₂B₂C₂ A₃B₃C₃ …\n\n"
        "In mathematical notation, if we denote D₁ = DNA1, D₂ = DNA2, and D₃ = DNA3, then:\n"
        "    mRNA = ∏₍ᵢ₌₁₎ⁿ (D₁[i] + D₂[i] + D₃[i])\n\n"
        "This means that each triplet of nucleotides (one from each strand) is concatenated to form the final mRNA."
    )
    rule_text.insert("1.0", explanation)
    rule_text.config(state="disabled")

def generate_protein():    
    result = compute_DNA_strand()  
    if result is None:
        return
    final_strand = result["DNA"]    
    
    codon_to_amino_acid = {
        "ATT": "I", "ATC": "I", "ATA": "I",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L", "TTA": "L", "TTG": "L",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "TTT": "F", "TTC": "F",
        "ATG": "M",
        "TGT": "C", "TGC": "C",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
        "TAT": "Y", "TAC": "Y",
        "TGG": "W",
        "CAA": "Q", "CAG": "Q",
        "AAT": "N", "AAC": "N",
        "CAT": "H", "CAC": "H",
        "GAA": "E", "GAG": "E",
        "GAT": "D", "GAC": "D",
        "AAA": "K", "AAG": "K",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
        "TAA": "X", "TAG": "X", "TGA": "X"
    }
    
    protein_seq = ""
    
    for i in range(0, len(final_strand), 3):
        codon = final_strand[i:i+3]
        if len(codon) < 3:
            break  
        protein_seq += codon_to_amino_acid.get(codon, "-")  
        
    protein_text_area.config(state="normal")
    protein_text_area.delete("1.0", tk.END)
    
    if len(protein_seq) > 200:
        display_protein = protein_seq[:200] + "..."
    else:
        display_protein = protein_seq

    protein_text_area.insert(tk.END, f"Protein (Amino Acids Sequence): {display_protein}\n")
    protein_text_area.config(state="disabled")

def show_genetic_rules():    
    rule_popup = tk.Toplevel(root)
    rule_popup.iconbitmap("icon-png.ico")
    rule_popup.title("Genetic Rules")
    rule_popup.geometry("600x500")
    
    rule_frame = tk.Frame(rule_popup)
    rule_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    rule_text = tk.Text(rule_frame, wrap="word", font=("Courier New", 9))
    rule_text.pack(side="left", fill="both", expand=True)
    
    rule_scrollbar = tk.Scrollbar(rule_frame, command=rule_text.yview)
    rule_scrollbar.pack(side="right", fill="y")
    rule_text.config(yscrollcommand=rule_scrollbar.set)
    
    explanation = (
        "Genetic Rules (Codon-to-Amino-Acid Mapping):\n\n"
        "Each codon/triplet (a group of 3 nucleotides) in the mRNA is translated into an amino acid.\n\n"
        "For example:\n"
        "  • ATT, ATC, ATA  → Isoleucine (I)\n"
        "  • CTT, CTC, CTA, CTG, TTA, TTG  → Leucine (L)\n"
        "  • GTT, GTC, GTA, GTG  → Valine (V)\n"
        "  • TTT, TTC  → Phenylalanine (F)\n"
        "  • ATG  → Methionine (M)\n"
        "  • TGT, TGC  → Cysteine (C)\n"
        "  • GCT, GCC, GCA, GCG  → Alanine (A)\n"
        "  • GGT, GGC, GGA, GGG  → Glycine (G)\n"
        "  • CCT, CCC, CCA, CCG  → Proline (P)\n"
        "  • ACT, ACC, ACA, ACG  → Threonine (T)\n"
        "  • TCT, TCC, TCA, TCG, AGT, AGC  → Serine (S)\n"
        "  • TAT, TAC  → Tyrosine (Y)\n"
        "  • TGG  → Tryptophan (W)\n"
        "  • CAA, CAG  → Glutamine (Q)\n"
        "  • AAT, AAC  → Asparagine (N)\n"
        "  • CAT, CAC  → Histidine (H)\n"
        "  • GAA, GAG  → Glutamic Acid (E)\n"
        "  • GAT, GAC  → Aspartic Acid (D)\n"
        "  • AAA, AAG  → Lysine (K)\n"
        "  • CGT, CGC, CGA, CGG, AGA, AGG  → Arginine (R)\n"
        "  • TAA, TAG, TGA  → Stop Codon (X)\n\n"
        "The final protein sequence is generated by reading the mRNA in successive triplets (codons) and mapping each codon to its corresponding amino acid as listed above."
    )
    rule_text.insert("1.0", explanation)
    rule_text.config(state="disabled")

def generate_protein_seq(final_strand):
    codon_to_amino_acid = {
        "ATT": "I", "ATC": "I", "ATA": "I",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L", "TTA": "L", "TTG": "L",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "TTT": "F", "TTC": "F",
        "ATG": "M",
        "TGT": "C", "TGC": "C",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
        "TAT": "Y", "TAC": "Y",
        "TGG": "W",
        "CAA": "Q", "CAG": "Q",
        "AAT": "N", "AAC": "N",
        "CAT": "H", "CAC": "H",
        "GAA": "E", "GAG": "E",
        "GAT": "D", "GAC": "D",
        "AAA": "K", "AAG": "K",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
        "TAA": "X", "TAG": "X", "TGA": "X"
    }
    protein_seq = ""
    for i in range(0, len(final_strand), 3):
        codon = final_strand[i:i+3]
        if len(codon) < 3:
            break
        protein_seq += codon_to_amino_acid.get(codon, "-")
    return protein_seq

def export_results():
    global dataset_id  
    result = compute_DNA_strand()
    if result is None:
        messagebox.showerror("Error", "No results available. Make sure data is loaded and parameters are set.")
        return
    protein_seq = generate_protein_seq(result["DNA"])
    export_data = [{
        "Dataset ID": dataset_id,
        "DNA1": result["DNA(R1)"],
        "DNA2": result["DNA(R2)"],
        "DNA3": result["DNA(R3)"],
        "mRNA": result["DNA"],
        "Protein (Amino Acids Sequence)": protein_seq
    }]
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, "w") as f:
                json.dump(export_data, f, indent=4)
            messagebox.showinfo("Export", "Results exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

# Main Window Setup
root = tk.Tk()
root.title("DNA-Based Computing (DBC) Tool for Time Series Data")
root.iconbitmap("icon-png.ico")
root.geometry("1200x720")

custom_font = tkFont.Font(family="Arial", size=10)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)

left_frame = tk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

right_frame = tk.Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


top_left = tk.Frame(left_frame)
top_left.pack(pady=10)
load_button = tk.Button(top_left, text="Load Data", font=custom_font, command=load_data)
load_button.pack(side="left")

plot_frame = tk.Frame(left_frame)
plot_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

init_empty_canvas()

button_frame = tk.Frame(left_frame)
button_frame.pack(pady=10)

dna_rules_button = tk.Label(button_frame, text="DNA-Forming Rules", fg="grey",
                      cursor="hand2", font=("Arial", 10, "underline"))
dna_rules_button.bind("<Button-1>", lambda event: show_dna_forming_rules_popup())
dna_rules_button.pack(side="left", padx=5)

param_button = tk.Button(button_frame, text="Set Parameters", font=custom_font, command=set_parameters_popup)
param_button.pack(side="left", padx=5)

param_link = tk.Label(button_frame, text="Parameters", fg="grey",
                      cursor="hand2", font=("Arial", 10, "underline"))
param_link.bind("<Button-1>", show_parameters_popup)
param_link.pack(side="left", padx=5)

rule_selection_frame = tk.Frame(left_frame)
rule_selection_frame.pack(pady=5)

tk.Label(rule_selection_frame, text="Select Reference (R):", font=custom_font).pack(side="left", padx=5)

rule_reference_var = tk.StringVar(value="R1")
tk.Radiobutton(rule_selection_frame, text="R1", variable=rule_reference_var, value="R1", font=custom_font).pack(side="left", padx=5)
tk.Radiobutton(rule_selection_frame, text="R2", variable=rule_reference_var, value="R2", font=custom_font).pack(side="left", padx=5)
tk.Radiobutton(rule_selection_frame, text="R3", variable=rule_reference_var, value="R3", font=custom_font).pack(side="left", padx=5)

rule_ok_button = tk.Button(rule_selection_frame, text="Show DNA-Forming Rules", font=custom_font,
                            command=lambda: visualize_conversion_rules_embedded(rule_reference_var.get()))
rule_ok_button.pack(side="left", padx=5)

conv_plot_frame = tk.Frame(left_frame)
conv_plot_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)

init_empty_conv_canvas()

dna_button = tk.Button(right_frame, text="DNA", font=custom_font, command=form_dna)
dna_button.pack(pady=10)

dna_text_frame = tk.Frame(right_frame)
dna_text_frame.pack(pady=10)  
dna_text_area = tk.Text(dna_text_frame, wrap="word", width=70, height=15, font=("Courier New", 9),
                         borderwidth=0.5, relief="solid")
dna_text_area.pack(side="left", fill="y")

dna_scrollbar = tk.Scrollbar(dna_text_frame, command=dna_text_area.yview)
dna_scrollbar.pack(side="right", fill="y")
dna_text_area.config(yscrollcommand=dna_scrollbar.set)

dna_text_area.tag_config("R1", foreground="blue")
dna_text_area.tag_config("R2", foreground="green")
dna_text_area.tag_config("R3", foreground="red")

mrna_button_frame = tk.Frame(right_frame)
mrna_button_frame.pack(pady=10)

mrna_rule_label = tk.Label(mrna_button_frame, text="mRNA-Forming Rule", fg="grey",
                           cursor="hand2", font=("Arial", 10, "underline"))
mrna_rule_label.bind("<Button-1>", lambda event: show_mrna_rule())
mrna_rule_label.pack(side="left", padx=5)

mrna_button = tk.Button(mrna_button_frame, text="mRNA", font=custom_font, command=form_mrna)
mrna_button.pack(side="left", padx=5)

mrna_text_frame = tk.Frame(right_frame)
mrna_text_frame.pack(pady=10)

mrna_text_area = tk.Text(mrna_text_frame, wrap="word", width=70, height=8, font=("Courier New", 9),
                          borderwidth=0.5, relief="solid")
mrna_text_area.pack(side="left", fill="y")
mrna_scrollbar = tk.Scrollbar(mrna_text_frame, command=mrna_text_area.yview)
mrna_scrollbar.pack(side="right", fill="y")
mrna_text_area.config(yscrollcommand=mrna_scrollbar.set)

mrna_text_area.tag_config("R1", foreground="blue")
mrna_text_area.tag_config("R2", foreground="green")
mrna_text_area.tag_config("R3", foreground="red")

protein_button_frame = tk.Frame(right_frame)
protein_button_frame.pack(pady=10)

genetic_rule_label = tk.Label(protein_button_frame, text="Genetic Rules", fg="grey",
                              cursor="hand2", font=("Arial", 10, "underline"))
genetic_rule_label.bind("<Button-1>", lambda event: show_genetic_rules())
genetic_rule_label.pack(side="left", padx=5)

protein_button = tk.Button(protein_button_frame, text="Protein", font=custom_font, command=generate_protein)
protein_button.pack(side="left", padx=5)

protein_text_frame = tk.Frame(right_frame)
protein_text_frame.pack(pady=10)

protein_text_area = tk.Text(protein_text_frame, wrap="word", width=70, height=5,
                            font=("Courier New", 9), borderwidth=0.5, relief="solid")
protein_text_area.pack(side="left", fill="y")
protein_scrollbar = tk.Scrollbar(protein_text_frame, command=protein_text_area.yview)
protein_scrollbar.pack(side="right", fill="y")
protein_text_area.config(yscrollcommand=protein_scrollbar.set)

export_button = tk.Button(right_frame, text="Export Results", font=custom_font, command=export_results)
export_button.pack(pady=10)


root.mainloop()
