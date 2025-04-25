import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog

# Criação do banco de dados
conn = sqlite3.connect("escala.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS escalas (
    data TEXT NOT NULL,
    funcionario_id INTEGER NOT NULL,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
)
""")
conn.commit()

# Funções
def cadastrar_funcionario():
    nome = simpledialog.askstring("Cadastro", "Nome do funcionário:")
    if nome:
        cursor.execute("INSERT INTO funcionarios (nome) VALUES (?)", (nome,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Funcionário cadastrado!")

def criar_escala():
    data = simpledialog.askstring("Escala", "Data da escala (AAAA-MM-DD):")
    if not data:
        return

    cursor.execute("SELECT id, nome FROM funcionarios")
    funcionarios = cursor.fetchall()
    if not funcionarios:
        messagebox.showwarning("Aviso", "Nenhum funcionário cadastrado.")
        return

    lista = "\n".join([f"{id} - {nome}" for id, nome in funcionarios])
    ids = simpledialog.askstring("Escala", f"Funcionários disponíveis:\n{lista}\n\nIDs (separados por vírgula):")
    if not ids:
        return

    cursor.execute("DELETE FROM escalas WHERE data = ?", (data,))
    for id_str in ids.split(","):
        try:
            cursor.execute("INSERT INTO escalas (data, funcionario_id) VALUES (?, ?)", (data, int(id_str.strip())))
        except ValueError:
            continue
    conn.commit()
    messagebox.showinfo("Sucesso", "Escala criada com sucesso!")

def consultar_por_data():
    data = simpledialog.askstring("Consulta", "Data da escala (AAAA-MM-DD):")
    if not data:
        return
    cursor.execute("""
        SELECT f.nome FROM escalas e
        JOIN funcionarios f ON e.funcionario_id = f.id
        WHERE e.data = ?
    """, (data,))
    nomes = cursor.fetchall()
    if nomes:
        nomes_formatados = "\n".join(nome for (nome,) in nomes)
        messagebox.showinfo("Escala", f"Escala de {data}:\n{nomes_formatados}")
    else:
        messagebox.showinfo("Escala", "Nenhuma escala encontrada para esta data.")

def consultar_por_funcionario():
    nome = simpledialog.askstring("Consulta", "Nome do funcionário:")
    if not nome:
        return
    cursor.execute("SELECT id FROM funcionarios WHERE LOWER(nome) = ?", (nome.lower(),))
    resultado = cursor.fetchone()
    if not resultado:
        messagebox.showerror("Erro", "Funcionário não encontrado.")
        return
    id_func = resultado[0]
    cursor.execute("SELECT data FROM escalas WHERE funcionario_id = ?", (id_func,))
    datas = cursor.fetchall()
    if datas:
        datas_formatadas = "\n".join(data for (data,) in datas)
        messagebox.showinfo("Escalas", f"{nome} está escalado nos dias:\n{datas_formatadas}")
    else:
        messagebox.showinfo("Escalas", "Nenhuma escala encontrada para este funcionário.")

# Interface gráfica
def main():
    root = tk.Tk()
    root.title("Gerenciador de Escala - SQLite")
    root.geometry("300x300")

    tk.Button(root, text="Cadastrar Funcionário", command=cadastrar_funcionario, width=30).pack(pady=10)
    tk.Button(root, text="Criar/Editar Escala", command=criar_escala, width=30).pack(pady=10)
    tk.Button(root, text="Consultar por Data", command=consultar_por_data, width=30).pack(pady=10)
    tk.Button(root, text="Consultar por Funcionário", command=consultar_por_funcionario, width=30).pack(pady=10)
    tk.Button(root, text="Sair", command=root.quit, width=30).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()