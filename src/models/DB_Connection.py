from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from src.configuration.config import DB_IP, DB_NAME, DB_USER, DB_PASSWD

Base = declarative_base()

class Animal_Schema(Base): # getAll, getByName
    __tablename__= "animal"
    id = Column('id', Integer, primary_key=True)
    id_Pai = Column('id_pai', Integer)
    id_Mae = Column('id_mae', Integer)
    sexo = Column('sexo', String(1))
    data_nasc = Column('data_nasc', Date)
    
    def __repr__(self):
        return "<Animal (id={}, id_Pai={}, id_Mae={}, sexo={}, data_nasc={})>".format(self.id, self.id_Pai, self.id_Mae, self.sexo, self.data_nasc)
    # username = Column('username', String(50), unique=True)

class Animal_nome_Schema(Base): # Create, create_all
    __tablename__="animal_nome"
    id = Column('id', Integer, primary_key=True)
    nome = Column('nome',String(50), unique=True)
    principal = Column('principal', Boolean())
    animal_id = Column(Integer, ForeignKey('animal.id'))

    def __repr__(self):
        return "<Animal_nome (id={}, Nome={}, Principal={}, animal_id={})>".format(self.id, self.nome, self.principal, self.animal_id)

class Atributo_Schema(Base): # Create, create_all, getAll
    __tablename__= "atributo"
    id = Column('id', String(80), primary_key=True)

    def __repr__(self):
        return "<Atibuto (id={})>".format(self.id)

class Animal_atributo_Schema(Base): # create, create_all, delete, update, getAll
    __tablename__="animal_atributo"
    id = Column('id', Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animal.id'))
    atributo_id = Column(String(80), ForeignKey('atributo.id'))
    valor = Column('valor', String(50))

    def __repr__(self):
        return "<animal_atributo (id={}, animal_id={}, atributo_id={}, valor={})>".format(self.id, self.animal_id, self.atributo_id, self.valor)

class Mapa_Schema(Base): # CRUD
    __tablename__="mapa"
    id = Column('id', Integer, primary_key=True)
    nome = Column('nome',String(50), unique=True)
    hash = Column('hash', String(50), unique=True)
    snp_count = Column('snp_count', Integer)
    gerado_automaticamente = Column('gerado_automaticamente', Boolean())

    def __repr__(self):
        return "<Mapa (id={}, nome={}, hash={}, snp_count={}, gerado_automaticamente={})>".format(self.id, self.nome, self.hash, self.snp_count, self.gerado_automaticamente)

class Animal_mapa_Schema(Base): # Create, createAll, getAll
    __tablename__="Animal_mapa"
    id = Column('id', Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animal.id'))
    mapa_id = Column(Integer, ForeignKey('mapa.id'))

    def __repr__(self):
        return "<Mapa (id={}, animal_id={}, mapa_id={})>".format(self.id, self.animal_id, self.mapa_id)

class Marcador_Schema(Base): # Crud
    __tablename__ = "marcador"
    snp = Column('snp', String(50), primary_key=True)
    missing_count = Column('missing_count', Integer, nullable=False)
    nomissing_count = Column('nomissing_count', Integer, nullable=False)
    aa_count = Column('aa_count', Integer, nullable=False)
    bb_count = Column('bb_count', Integer, nullable=False)
    ab_count = Column('ab_count', Integer, nullable=False)
    desconhecido_count = Column('desconhecido_count', Integer, nullable=False)

    def __repr__(self):
        return "<Marcador (snp={}, missing_count={}, nomissing_count={}, aa_count={}, bb_count={}, ab_count={}, desconhecido_count={})>".format(self.snp, self.missing_count, self.nomissing_count, self.aa_count, self.bb_count, self.ab_count, self.desconhecido_count)
 
class Mapa_marcador_Schema(Base): # CCG
    __tablename__ = "mapa_marcador"
    id = Column('id', Integer, primary_key=True)
    snp_id = Column(String(50), ForeignKey('marcador.snp'))
    mapa_id = Column(Integer, ForeignKey('mapa.id'))

    def __repr__(self):
        return "<Mapa (id={}, snp_id={}, mapa_id={})>".format(self.id, self.snp_id, self.mapa_id)

engine = create_engine('mysql+pymysql://'+DB_USER+':'+DB_PASSWD+'@'+DB_IP+'/'+DB_NAME, echo=True)
# Base.metadata.create_all(bind=engine) # Descomentar se precisar recriar a estrutura
Session = sessionmaker(bind=engine)

session = Session()