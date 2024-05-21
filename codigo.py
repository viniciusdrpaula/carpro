from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base() # guarda informaçoes das classes representa tabelas no banco de dados

engine = create_engine('sqlite:///banco.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Carro(Base):
    __tablename__ = "Carros"

    placa = Column('PLACA',Integer,primary_key=True) #definindo id, int e chave
    nome = Column('NOME',String)
    disponibilidade = Column('DISPONIBILIDADE',Boolean,default=True)  #tem que muda esse booleano pra disponivel = 1 indisponivel = 0
    marca = Column('MARCA',String)

    def __init__(self,placa,nome,marca,disponibilidade=True): #recebe o valor pra tabela
        self.nome = nome
        self.placa = placa
        self.disponibilidade = disponibilidade
        self.marca = marca

class Cliente(Base):
    __tablename__ = "Clientes"

    nomecliente = Column('NOMECLIENTE',String)
    doc = Column('DOC',Integer,primary_key=True) #id do cliente 
    idade = Column('IDADE',Integer)
    qntd = Column('QTND',Integer,default=0) #verifica se o cliente já tem ou n carro alugado / QTND = qtnd de carros alugos

    def __init__(self,nomecliente,doc,idade,qtnd=0):
        self.nomecliente = nomecliente
        self.doc = doc 
        self.idade = idade 
        self.qtnd = qtnd 

class Aluguel(Base):
    __tablename__ = "Aluguel"
    
    dias = Column('DIAS',Integer) 
    valor = Column('VALOR',Float,primary_key=True) 
    cliente_id = Column('CLIENTE_ID',Integer,ForeignKey("Clientes.doc")) #chave estrangeira nomeadatabela.nomedacoluna
    carro_id = Column('CARRO_ID',Integer,ForeignKey("Carros.placa"))

    def __init__(self,dias,valor,cliente_id,carro_id):
        self.dias = dias
        self.valor = valor
        self.carro_id = carro_id
        self.cliente_id = cliente_id

Cliente.alugueis = relationship("Aluguel", back_populates="cliente")
Carro.alugueis = relationship("Aluguel", back_populates="carro")


def cadastrar_cliente(nomecliente, doc):
    novo_cliente = Cliente(nomecliente=nomecliente, doc=doc) #cadastro - cliente 
    session.add(novo_cliente)
    session.commit()

def cadastrar_carro(placa, nome, marca,disponibilidade): 
    novo_carro = Carro(placa=placa, nome=nome, marca=marca,disponibilidade=disponibilidade)#cadastro - carro
    session.add(novo_carro)
    session.commit()

def calcular_preco(dias): 
    preco_dia = 100        
    return (preco_dia * dias) #observação acho q tem q arrumar

def consulta_geral():
    clientes = session.query(Cliente).all()
    carros = session.query(Carro).all() #consulta - geral 
    alugueis = session.query(Aluguel).all()
    return {
        "clientes": clientes,
        "carros": carros,
        "alugueis": alugueis
    }


def alugar_carro(cliente_id,carro_id,dias):
    cliente = session.query(Cliente).filter_by(doc=cliente_id).first()
    carro = session.query(Carro).filter_by(placa=carro_id).first()
    if cliente and carro:
        if carro.disponibilidade: # disponibilidade observação acho q tem q arrumar
            novo_aluguel = Aluguel(
                dias=dias, 
                valor=calcular_preco(dias),  #para calcular o valor do aluguel dependendo dos dias
                cliente_id=cliente_id, 
                carro_id=carro_id)
            carro.disponibilidade = False #torna o carro indisponivel
            cliente.qntd += 1 #adiciona um carro para o cliente
            session.add(novo_aluguel)
            session.commit()
            print(f"o carro da placa {carro_id} alugado para o cliente {cliente_id} por {dias} dias. Valor total: {novo_aluguel.valor}")
        else:
            print('o carro ja esta alugado')
    else:
        print("Aluguel não pode ser realizado. Verifique se o cliente e o carro existem e se o carro está disponível.")



def devolver_carro(cliente_id, carro_id):
    aluguel = session.query(Aluguel).filter_by(cliente_id=cliente_id, carro_id=carro_id).first()

    if aluguel:
        carro = session.query(Carro).filter_by(placa=carro_id).first()
        carro.disponibilidade = True
        cliente = session.query(Cliente).filter_by(doc=cliente_id).first()
        cliente.qntd -= 1
        session.delete(aluguel)
        session.commit()
        print(f"Carro de placa {carro_id} devolvido pelo cliente {cliente_id}.")
    else:
        print("O carro não foi alugado por este cliente.")



def menu():
    while True:
        print("\n Sistema de aluguel CARPRO")
        print("1. Alugar Carro")
        print("2. Devolver Carro")
        print("3. Cadastrar Cliente")
        print("4. Cadastrar Carro")
        print("5. Consulta Geral")
        print("6. Sair")
    
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente_id = int(input('ID do Cliente: '))
            carro_id = int(input('Placa do Carro: '))
            dias = int(input('Dias: '))
            alugar_carro(cliente_id, carro_id, dias)
        elif opcao == "2":
            cliente_id = int(input('ID do Cliente: '))
            carro_id = int(input('Placa do Carro: '))
            devolver_carro(cliente_id, carro_id)
        elif opcao == "3":
            nomecliente = input('Nome do Cliente: ')
            doc = int(input('Documento: '))
            idade = int(input('Idade: '))
            cadastrar_cliente(nomecliente, doc)
        elif opcao == "4":
            placa = int(input('Placa: '))
            nome = input('Nome: ')
            disponibilidade = input('Disponibilidade (True/False): ') == 'True'
            marca = input('Marca: ')
            cadastrar_carro(placa, nome, marca, disponibilidade)
        elif opcao == "5":
            dados = consulta_geral()
            print("Clientes:", dados["clientes"])
            print("Carros:", dados["carros"])
            print("Aluguéis:", dados["alugueis"])
        elif opcao == "6":
            break
        else:
            print("Opção inválida, tente novamente.")


menu()