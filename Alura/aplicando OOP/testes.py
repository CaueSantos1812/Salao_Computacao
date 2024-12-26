import pickle
import os
from datetime import datetime

class Consultorio:
    def __init__(self, dono, servicos, horario, agenda, clientes, aberto=False, data_file="dados_consultorio.pkl"):
        self.data_file = data_file

        if os.path.exists(data_file):
            print("Carregando dados do arquivo...")
            self.load_data()
        else:
            self.dono = dono
            self.servicos = servicos
            self.aberto = 'Aberto' if aberto else 'Fechado'
            self.horario = horario
            self.agenda = agenda
            self.clientes = clientes

    def save_data(self):
        data = {
            "dono": self.dono,
            "servicos": self.servicos,
            "aberto": self.aberto,
            "horario": self.horario,
            "agenda": self.agenda,
            "clientes": self.clientes
        } 
        with open(self.data_file, "wb") as file:
            pickle.dump(data, file)
        print("Dados salvos com sucesso!")

    def load_data(self):
        with open(self.data_file, "rb") as file:
            data = pickle.load(file)
        self.dono = data["dono"]
        self.servicos = data["servicos"]
        self.aberto = data["aberto"]
        self.horario = data["horario"]
        self.agenda = data["agenda"]
        self.clientes = data["clientes"]

    def __str__(self):
        return f'O consultório da(o) {self.dono} está {self.aberto}'

    def options(self):
        opcoes = {
            "cadastro": self.cadastro,
            "mostrar_agenda": self.mostrar_agenda,
            "agendar": self.agendar,
            "ver_cliente": self.ver_cliente,
            "cadastrar_procedimento": self.cadastrar_procedimento,
        }

        print("Opções disponíveis:")
        for opcao in opcoes.keys():
            print(f"- {opcao}")

        escolha = input("Digite a opção desejada: ").strip().lower()

        if escolha in opcoes:
            opcoes[escolha]()
        else:
            print("Opção inválida. Tente novamente.")
        self.save_data()

    def ver_cliente(self):
        nomes = [nam.nome for nam in self.clientes]

        print('As clientes disponíveis para visualização são:')
        for nam in nomes:
            print(nam)

        nome_cliente = input('Qual o nome da cliente que você deseja ver: ').strip()

        if nome_cliente in nomes:
            for cliente in self.clientes:
                if cliente.nome == nome_cliente:
                    print(cliente)
        else:
            print('Cliente ainda não cadastrada, realizando o cadastro (...)')
            self.cadastro(nome_cliente)

    def cadastro(self, nome=None):
        if nome:
            nome = nome
        else:
            nome = input("Qual o nome completo da nova cliente? \n")

        celular = input("Qual o celular da cliente?\n")
        genero = input("Qual o gênero da cliente? \n")
        nas = input("Qual a sua data de nascimento? (DD/MM/AAAA)\n")

        nova_cliente = Cliente(nome, celular, genero, nas)
        self.clientes.append(nova_cliente)

        print(f"A cliente {nome} foi cadastrada com sucesso!")

    def mostrar_agenda(self):
        if not self.agenda:
            print("A agenda está vazia.")
            return

        print("Agenda do Consultório:")
        for data, agendamentos in sorted(self.agenda.items()):
            print(f"\nData: {data}")
            for procedimento, cliente in agendamentos:
                print(f"{procedimento} - Cliente: {cliente.nome}")


    def cadastrar_procedimento(self):
        nome_procedimento = input("Digite o nome do procedimento: ").strip()
        preco = float(input("Digite o preço do procedimento: "))
        duracao = input("Digite a duração do procedimento (HH:MM): ").strip()

        # Adicionar o novo procedimento à lista de serviços
        procedimento = Procedimento(nome_procedimento, preco, duracao)
        self.servicos.append(procedimento)

        print(f"Procedimento '{nome_procedimento}' cadastrado com sucesso!")
        
        # Retorna o objeto Procedimento para ser usado no agendamento
        return procedimento



    def agendar(self):
        nome_cliente = input("Digite o nome da cliente: ").strip()

        # Verifica se o cliente existe
        cliente_existente = None
        for cliente in self.clientes:
            if cliente.nome.lower() == nome_cliente.lower():
                cliente_existente = cliente
                break

        if not cliente_existente:
            print("Cliente não encontrada. Cadastrando a cliente...")
            self.cadastro()
            cliente_existente = self.clientes[-1]

        # Mostra os serviços disponíveis
        print("Serviços disponíveis:")
        nome_servicos = [servico.nome for servico in self.servicos]
        for nomes in nome_servicos:
            print(f"- {nomes}")

        procedimento_nome = input("Digite o procedimento desejado: ").strip()

        # Verifica se o procedimento já existe
        procedimento = None
        for servico in self.servicos:
            if servico.nome == procedimento_nome:
                procedimento = servico
                break

        # Se o procedimento não existir, solicita o cadastro do novo
        if procedimento is None:
            print("Procedimento não encontrado. Cadastrando procedimento...")
            procedimento = self.cadastrar_procedimento()  # Agora retorna o objeto Procedimento

        # Obtém a data do agendamento
        data = input("Digite a data do agendamento (DD/MM/AAAA): ").strip()

        # Adiciona o procedimento na agenda
        if data not in self.agenda:
            self.agenda[data] = []

        self.agenda[data].append((procedimento, cliente_existente))

        # Registra o procedimento no histórico do cliente
        cliente_existente.registrar_procedimento(procedimento)

        print(f"Agendamento de {procedimento.nome} realizado com sucesso para {cliente_existente.nome} no dia {data}!")


class Cliente:
    def __init__(self, nome, celular, genero, nas, servicos_realizados=None):
        self.nome = nome
        self.celular = celular
        self.genero = genero
        self.nas = datetime.strptime(nas, "%d/%m/%Y")
        self.servicos_realizados = servicos_realizados if servicos_realizados is not None else {}

    @property
    def idade(self):
        hoje = datetime.today()
        idade = hoje.year - self.nas.year - ((hoje.month, hoje.day) < (self.nas.month, self.nas.day))
        return idade

    def registrar_procedimento(self, procedimento):
        if procedimento.nome in self.servicos_realizados:
            self.servicos_realizados[procedimento.nome] += 1
        else:
            self.servicos_realizados[procedimento.nome] = 1

    def __str__(self):
        return (f"A cliente {self.nome}, possui {self.idade} anos e tem o celular {self.celular}."
                f"\nHistórico de Procedimentos: {self.servicos_realizados}")

class Procedimento:
    def __init__(self, nome, preco, duracao):
        self.nome = nome
        self.preco = preco
        self.duracao = duracao

    def __str__(self):
        return (f"Procedimento: {self.nome}, Preço: R${self.preco:.2f}, Duração: {self.duracao}")

# Exemplo de uso
ser = []
cl = []
agenda = {}

consultorio = Consultorio("Dra. Valéria", ser, "Segunda a Sexta, 10:00 - 19:00", agenda, cl)
while True:
    consultorio.options()
