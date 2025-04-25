import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

ARQ_FUNCIONARIOS = 'funcionarios.json'
ARQ_ESCALAS = 'escalas.json'

def carregar_dados(arquivo):
    if not os.path.exists(arquivo):
        return {}
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def cadastrar_funcionario():
    nome = simpledialog.askstring("Cadastro", "Nome do funcionário:")
    if not nome:
        return
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    id_func = str(len(funcionarios) + 1)
    funcionarios[id_func] = {"nome": nome}
    salvar_dados(ARQ_FUNCIONARIOS, funcionarios)
    messagebox.showinfo("Sucesso", "Funcionário cadastrado!")

def criar_escala():
    data = simpledialog.askstring("Escala", "Data da escala (AAAA-MM-DD):")
    if not data:
        return
    escalas = carregar_dados(ARQ_ESCALAS)
    if data not in escalas:
        escalas[data] = []
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    lista_ids = "\n".join([f"{id} - {dados['nome']}" for id, dados in funcionarios.items()])
    ids = simpledialog.askstring("Escala", f"Funcionários:\n{lista_ids}\n\nIDs (separados por vírgula):")
    if ids:
        escalas[data] = [i.strip() for i in ids.split(",")]
        salvar_dados(ARQ_ESCALAS, escalas)
        messagebox.showinfo("Sucesso", "Escala salva com sucesso!")

def consultar_por_data():
    data = simpledialog.askstring("Consulta", "Informe a data (AAAA-MM-DD):")
    escalas = carregar_dados(ARQ_ESCALAS)
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    if data in escalas:
        nomes = [funcionarios.get(id.strip(), {"nome": "Desconhecido"})["nome"] for id in escalas[data]]
        messagebox.showinfo("Escala", f"Escala para {data}:\n" + "\n".join(nomes))
    else:
        messagebox.showinfo("Consulta", "Nenhuma escala cadastrada.")

def consultar_por_funcionario():
    nome_busca = simpledialog.askstring("Consulta", "Nome do funcionário:")
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    escalas = carregar_dados(ARQ_ESCALAS)
    id_func = None
    for id_f, dados in funcionarios.items():
        if dados["nome"].lower() == nome_busca.lower():
            id_func = id_f
            break
    if not id_func:
        messagebox.showinfo("Erro", "Funcionário não encontrado.")
        return
    datas = [data for data, lista in escalas.items() if id_func in lista]
    messagebox.showinfo("Escalas", f"Escalas para {nome_busca}:\n" + "\n".join(datas) if datas else "Nenhuma escala encontrada.")

def main():
    root = tk.Tk()
    root.title("Gerenciador de Escala de Serviço")
    root.geometry("300x300")

    tk.Button(root, text="Cadastrar Funcionário", command=cadastrar_funcionario, width=30).pack(pady=10)
    tk.Button(root, text="Criar/Editar Escala", command=criar_escala, width=30).pack(pady=10)
    tk.Button(root, text="Consultar por Data", command=consultar_por_data, width=30).pack(pady=10)
    tk.Button(root, text="Consultar por Funcionário", command=consultar_por_funcionario, width=30).pack(pady=10)
    tk.Button(root, text="Sair", command=root.quit, width=30).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()