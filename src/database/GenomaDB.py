from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean, orm, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

from src.configuration.config import DB_PATH

Base = declarative_base()

class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


class Animal(BaseModel):
    __tablename__= "Animal"
    __repr_attrs__ = ['sexo', 'data_nasc']

    id = Column('id', String(128), primary_key=True)
    id_Pai = Column('id_pai', String(128))
    id_Mae = Column('id_mae', String(128))
    sexo = Column('sexo', String(1))
    data_nasc = Column('data_nasc', Date)

    Animal_mapas = orm.relationship('Animal_mapa', backref='Animal',lazy=False)


class Mapa(BaseModel):
    __tablename__="Mapa"
    __repr_attrs__ = ['nome', 'snp_count']

    id = Column('id', String(128), primary_key=True)
    nome = Column('nome', String(128))
    snp_count = Column('snp_count', Integer)


class Animal_mapa(BaseModel):
    __tablename__="Animal_mapa"
    __repr_attrs__ = ['animal_id', 'mapa_id']

    id = Column('id', Integer, primary_key=True)
    animal_id = Column(String(128), ForeignKey('Animal.id'))
    mapa_id = Column(String(50), ForeignKey('Mapa.id'))

class Marcador(BaseModel):
    __tablename__ = "Marcador"
    __repr_attrs__ = ['snp']

    snp = Column('snp', String(50), primary_key=True)


class Mapa_marcador(BaseModel):
    __tablename__ = "Mapa_marcador"
    __repr_attrs__ = ['snp', 'mapa_id', 'chromossome', 'position']  

    id = Column('id', Integer, primary_key=True)
    snp = Column(String(50), ForeignKey('Marcador.snp'))
    mapa_id = Column(String(50), ForeignKey('Mapa.id'))

    chromossome = Column('chromossome',Integer)
    position = Column('position', Integer)


class BaseDados(BaseModel):
    __tablename__ = "BaseDados"
    __repr_attrs__ = ['nome', 'tipo', 'marcadores', 'animais', 'created_at']  

    uuid = Column('uuid', String(32), primary_key=True)
    nome = Column(String(150))
    tipo =  Column(String(30))
    marcadores = Column(Integer)
    animais = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    

engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)
session = scoped_session(sessionmaker(bind=engine))
BaseModel.set_session(session)

Base.metadata.create_all(bind=engine) # Descomentar se precisar recriar a estrutura