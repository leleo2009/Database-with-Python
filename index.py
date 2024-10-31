import sqlite3
import tkinter as tk
from tkinter import messagebox
import re

conn = sqlite3.connect('aulaDB.db')
cursor = conn.cursor()

def criar_tabela():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplier (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT,
        cpf TEXT UNIQUE NOT NULL,
        father_name TEXT NOT NULL,
        mother_name TEXT NOT NULL,
        address TEXT NOT NULL,
        zip_code TEXT
    )""")
    conn.commit()

def cadastrar_supplier():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    cpf = entry_cpf.get()
    father_name = entry_father_name.get()
    mother_name = entry_mother_name.get()
    address = entry_address.get()
    zip_code = entry_zip_code.get()

    if not all([first_name, address, father_name, mother_name, cpf]):
        messagebox.showerror("Erro", "Todos os campos obrigatórios devem ser preenchidos!")
        return

    if not all(re.match("^[A-Za-zÀ-ÿ ]+$", name) for name in [first_name, last_name, father_name, mother_name]):
        messagebox.showerror("Erro", "Nomes e sobrenomes devem conter apenas letras.")
        return

    if not re.match(r"^\d{11}$", cpf):
        messagebox.showerror("Erro", "CPF deve conter exatamente 11 dígitos numéricos.")
        return

    if zip_code and not re.match(r"^\d{8}$", zip_code):
        messagebox.showerror("Erro", "CEP deve conter exatamente 8 dígitos numéricos.")
        return

    if len(address) > 40:
        messagebox.showerror("Erro", "Endereço deve ter no máximo 40 caracteres.")
        return

    cursor.execute("SELECT * FROM supplier WHERE cpf = ?", (cpf,))
    if cursor.fetchone():
        messagebox.showerror("Erro", "CPF já cadastrado!")
        return

    try:
        cursor.execute("""
        INSERT INTO supplier (
            first_name, last_name, cpf, father_name, mother_name, address, zip_code
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (first_name, last_name, cpf, father_name, mother_name, address, zip_code))
        
        conn.commit()
        messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Erro ao cadastrar fornecedor.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def consultar_supplier_por_id():
    cpf = entry_cpf.get()
    if not re.match(r"^\d{11}$", cpf):
        messagebox.showerror("Erro", "Por favor, insira um CPF válido para consulta.")
        return

    cursor.execute("SELECT * FROM supplier WHERE cpf = ?", (cpf,))
    supplier = cursor.fetchone()

    if supplier:
        result = f"ID: {supplier[0]}\nNome: {supplier[1]} {supplier[2]}\nCPF: {supplier[3]}\n" \
                 f"Nome do Pai: {supplier[4]}\nNome da Mãe: {supplier[5]}\nEndereço: {supplier[6]}"
        messagebox.showinfo("Fornecedor Encontrado", result)
    else:
        messagebox.showinfo("Fornecedor Não Encontrado", "Nenhum fornecedor encontrado com este CPF.")

def consultar_todos_suppliers():
    cursor.execute("SELECT id FROM supplier")
    suppliers = cursor.fetchall()

    if suppliers:
        result = "\n".join([f"ID: {supplier[0]}" for supplier in suppliers])
        messagebox.showinfo("Fornecedores Cadastrados", result)
    else:
        messagebox.showinfo("Fornecedores Cadastrados", "Nenhum fornecedor cadastrado.")

def excluir_supplier():
    cpf = entry_cpf.get()
    if not re.match(r"^\d{11}$", cpf):
        messagebox.showerror("Erro", "Por favor, insira um CPF válido para exclusão.")
        return

    cursor.execute("DELETE FROM supplier WHERE cpf = ?", (cpf,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso!")
    limpar_campos()

def excluir_todos_suppliers():
    if messagebox.askyesno("Confirmação", "Tem certeza de que deseja excluir todos os fornecedores?"):
        cursor.execute("DELETE FROM supplier")
        conn.commit()
        messagebox.showinfo("Sucesso", "Todos os fornecedores foram excluídos com sucesso!")

def limpar_campos():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_father_name.delete(0, tk.END)
    entry_mother_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_zip_code.delete(0, tk.END)

criar_tabela()

root = tk.Tk()
root.title("Banco de Dados de Fornecedores")
root.geometry("600x400")
root.configure(bg="#F5F5F5")

main_frame = tk.Frame(root, bg="#F5F5F5")
main_frame.pack(padx=20, pady=20)

title_text = "Banco de Dados de Fornecedores"
lbl_title = tk.Label(main_frame, text=title_text, font=("Courier New", 20), bg="#F5F5F5", fg="#4682B4")
lbl_title.pack(pady=(10, 0))

form_frame = tk.Frame(main_frame, bg="#F0F8FF")
form_frame.pack(padx=10, pady=10, fill=tk.X)

entries = {}

labels = [
    ("Nome (obrigatório)", "entry_first_name"),
    ("Sobrenome", "entry_last_name"),
    ("CPF (obrigatório)", "entry_cpf"),
    ("Nome do Pai (obrigatório)", "entry_father_name"),
    ("Nome da Mãe (obrigatório)", "entry_mother_name"),
    ("Endereço (obrigatório)", "entry_address"),
    ("CEP", "entry_zip_code"),
]

for i, (field_name, field_var) in enumerate(labels):
    lbl = tk.Label(form_frame, text=field_name, bg="#F0F8FF")
    lbl.grid(row=i, column=0, sticky="w", padx=5, pady=5)

    entry = tk.Entry(form_frame)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    entries[field_var] = entry

entry_first_name = entries["entry_first_name"]
entry_last_name = entries["entry_last_name"]
entry_cpf = entries["entry_cpf"]
entry_father_name = entries["entry_father_name"]
entry_mother_name = entries["entry_mother_name"]
entry_address = entries["entry_address"]
entry_zip_code = entries["entry_zip_code"]

btn_register = tk.Button(main_frame, text="Cadastrar Fornecedor", command=cadastrar_supplier, bg="#90EE90")
btn_register.pack(pady=5)

btn_consult_all = tk.Button(main_frame, text="Consultar Todos Fornecedores", command=consultar_todos_suppliers, bg="#FFD700")
btn_consult_all.pack(pady=5)

btn_consult_id = tk.Button(main_frame, text="Consultar Fornecedor por CPF", command=consultar_supplier_por_id, bg="#ADD8E6")
btn_consult_id.pack(pady=5)

btn_delete = tk.Button(main_frame, text="Excluir Fornecedor", command=excluir_supplier, bg="#FF6347")
btn_delete.pack(pady=5)

btn_delete_all = tk.Button(main_frame, text="Excluir Todos os Fornecedores", command=excluir_todos_suppliers, bg="#FF4500")
btn_delete_all.pack(pady=5)

btn_exit = tk.Button(main_frame, text="Sair", command=root.quit, bg="#FFB6C1")
btn_exit.pack(pady=5)

root.mainloop()
conn.close()
