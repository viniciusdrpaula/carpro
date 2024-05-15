import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

base = declarative_base() # guarda informaçoes das classes representa tabelas no banco de dados

engine = create_engine('sqlite:///banco.db')
base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Carro(base):
    __tablename__ = "Carros"

    placa = Column('PLACA',Integer,primary_key=True) #definindo id, int e chave
    nome = Column('NOME',String)
    disponibilidade = Column('DISPONIBILIDADE',default=True)  #tem que muda esse booleano pra disponivel = 1 indisponivel = 0
    marca = Column('MARCA',String)

    def __init__(self,placa,nome,marca,disponibilidade=True): #recebe o valor pra tabela
        self.nome = nome
        self.placa = placa
        self.disponibilidade = disponibilidade
        self.marca = marca

class Cliente(base):
    __tablename__ = "Clientes"

    nomecliente = Column('NOMECLIENTE',String)
    doc = Column('DOC',Integer,primary_key=True) #id do cliente 
    idade = Column('IDADE',Integer)
    qntd = Column('QTND',Integer) #verifica se o cliente já tem ou n carro alugado / QTND = qtnd de carros alugos

    def __init__(self,nomecliente,doc,qtnd,idade):
        self.nomecliente = nomecliente
        self.doc = doc 
        self.idade = idade 
        self.qtnd = qtnd 

class Aluguel(base):
    __tablename__ = "Aluguel"
    
    dias = Column('DIAS',Integer) 
    valor = Column('VALOR',Float)
    cliente_id = Column('CLIENTE_ID',Integer,ForeignKey("Clientes.doc")) #chave estrangeira nomeadatabela.nomedacoluna
    carro_id = Column('CARRO_ID',Integer,ForeignKey("Carros.placa"))
    dias = Column('DIAS',Integer)

    def __init__(self,dias,valor,cliente_id,carro_id):
        self.dias = dias
        self.valor = valor
        self.carro_id = carro_id
        self.cliente_id = cliente_id

    cliente = relationship("Cliente") 
    carro = relationship("Carro")     #tem q pesquisa  oq isso faz


def cadastrar_cliente(self,nomecliente, doc):
    novo_cliente = Cliente(nomecliente=nomecliente, doc=doc) #cadastro - cliente 
    session.add(novo_cliente)
    session.commit()

def cadastrar_carro(self,placa, nome, marca): 
    novo_carro = Carro(placa=placa, nome=nome, marca=marca)#cadastro - carro
    session.add(novo_carro)
    session.commit()

def calcular_preco(self): 
    preco_dia = 100        
    self.preco_total = (preco_dia * self.dias) #observação acho q tem q arrumar

def consulta_geral(self):
    clientes = session.query(Cliente).all()
    carros = session.query(Carro).all() #consulta - geral 
    alugueis = session.query(Aluguel).all()
    return {
        "clientes": clientes,
        "carros": carros,
        "alugueis": alugueis
    }


def alugar_carro(cliente_id,carro_id):
    cliente = session.query(Cliente).filter_by(doc=cliente_id)
    carro = session.query(Carro).filter_by(placa=carro.id)
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
            print(f"o carro da placa {carro_id} alugado para o cliente {cliente_id} por {novo_aluguel.dias} dias. Valor total: {novo_aluguel.valor}")
        else:
            print('o carro ja esta alugado')
    else:
        print("Aluguel não pode ser realizado. Verifique se o cliente e o carro existem e se o carro está disponível.")





#input de Carro
placa = input('placa: ')
nome = input('nome: ')
disponibilidade = input('disponibilidade:') 
marca = input('marca: ')
dias = int(input("dias: "))

cadastrar_carro(placa, nome, marca, disponibilidade)

#input de Cliente
nomecliente = input('Nome do Cliente: ')
doc = int(input('Documento : '))
idade = int(input('Idade: '))

cadastrar_cliente(nomecliente, doc, idade)

#input do aluguel 

