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
    nome = input("Nome do funcionário: ")
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    id_func = str(len(funcionarios) + 1)
    funcionarios[id_func] = {"nome": nome}
    salvar_dados(ARQ_FUNCIONARIOS, funcionarios)
    print("Funcionário cadastrado com sucesso!")

def criar_escala():
    data = input("Data da escala (AAAA-MM-DD): ")
    escalas = carregar_dados(ARQ_ESCALAS)
    if data not in escalas:
        escalas[data] = []
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    print("Funcionários disponíveis:")
    for id_func, dados in funcionarios.items():
        print(f"{id_func} - {dados['nome']}")
    ids = input("IDs dos funcionários na escala (separados por vírgula): ")
    escalas[data] = ids.split(",")
    salvar_dados(ARQ_ESCALAS, escalas)
    print("Escala criada/atualizada com sucesso!")

def consultar_escala_por_data():
    data = input("Informe a data (AAAA-MM-DD): ")
    escalas = carregar_dados(ARQ_ESCALAS)
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    if data in escalas:
        print(f"Escala para {data}:")
        for id_func in escalas[data]:
            nome = funcionarios.get(id_func.strip(), {}).get("nome", "Desconhecido")
            print(f"- {nome}")
    else:
        print("Nenhuma escala cadastrada para essa data.")

def consultar_escala_por_funcionario():
    nome_busca = input("Nome do funcionário: ").lower()
    funcionarios = carregar_dados(ARQ_FUNCIONARIOS)
    escalas = carregar_dados(ARQ_ESCALAS)
    id_func = None
    for id_f, dados in funcionarios.items():
        if dados["nome"].lower() == nome_busca:
            id_func = id_f
            break
    if not id_func:
        print("Funcionário não encontrado.")
        return
    print(f"Escalas para {funcionarios[id_func]['nome']}:")
    for data, lista in escalas.items():
        if id_func in lista:
            print(f"- {data}")

def menu():
    while True:
        print("\n--- Sistema de Escala de Serviço ---")
        print("1. Cadastrar funcionário")
        print("2. Criar/editar escala")
        print("3. Consultar escala por data")
        print("4. Consultar escala por funcionário")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_funcionario()
        elif opcao == '2':
            criar_escala()
        elif opcao == '3':
            consultar_escala_por_data()
        elif opcao == '4':
            consultar_escala_por_funcionario()
        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

if __name__ == "_main_":
    menu()