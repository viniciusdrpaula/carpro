import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean


base = declarative_base() # classe vira tabelas no banco de dados


class Carro(base):
    __tablename__ = "Carros"

    placa = Column(Integer,primary_key=True) #definindo id, int e chave
    nome = Column(String)
    disponibilidade = Column(Boolean,disponivel = True)
    marca = Column(String)

    def __init__(self,placa,nome,disponibilidade,marca): #recebe o valor pra tabela
        self.nome = nome
        self.placa = placa
        self.disponibilidade = disponibilidade
        self.marca = marca

class cliente(base):
    __tablename__ = "Clientes"

    nomecliente = Column(String)
    doc = Column(Integer,primary_key=True) #id do cliente 
    qntd = Column(Integer) #qntd de carros q o clinte tm alugado

    def __init__(self,nomecliente,doc,qtnd):
        self.nomecliente = nomecliente
        self.doc = doc
        self.qntd = qtnd

class Aluguel(base):
    __tablename__ = "Aluguel"
    
    dias = Column(Integer) 
    valor = Column(Float)
    cliente_id = Column(Integer,ForeignKey("Clientes.doc")) #chave estrangeira nomeadatabela.nomedacoluna
    carro_id = Column(Integer,ForeignKey("Carros.placa"))

    def __init__(self,dias,valor,cliente_id,carro_id):
        self.dias = dias
        self.valor = valor
        self.carro_id = carro_id
        self.cliente_id = cliente_id



