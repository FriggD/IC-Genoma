from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

from src.configuration.config import DB_IP, DB_NAME, DB_USER, DB_PASSWD

Base = declarative_base()

class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True
    pass


class Animal(BaseModel):
    __tablename__= "animal"
    __repr_attrs__ = ['sexo', 'data_nasc']

    id = Column('id', String(128), primary_key=True)
    id_Pai = Column('id_pai', String(128))
    id_Mae = Column('id_mae', String(128))
    sexo = Column('sexo', String(1))
    data_nasc = Column('data_nasc', Date)


class Mapa(BaseModel):
    __tablename__="mapa"
    __repr_attrs__ = ['nome', 'hash', 'snp_count']

    id = Column('id', String(50), primary_key=True)
    nome = Column('nome', String(128))
    snp_count = Column('snp_count', Integer)


class AnimalMapa(BaseModel):
    __tablename__="Animal_mapa"
    __repr_attrs__ = ['animal_id', 'mapa_id']

    id = Column('id', Integer, primary_key=True)
    animal_id = Column(String(128), ForeignKey('animal.id'))
    mapa_id = Column(String(50), ForeignKey('mapa.id'))


class Marcador(BaseModel):
    __tablename__ = "marcador"
    __repr_attrs__ = ['snp', 'mapa_id']

    snp = Column('snp', String(50), primary_key=True)


class Mapa_marcador(BaseModel):
    __tablename__ = "mapa_marcador"
    __repr_attrs__ = ['snp_id', 'mapa_id', 'chromossome', 'position']  

    id = Column('id', Integer, primary_key=True)
    snp = Column(String(50), ForeignKey('marcador.snp'))
    mapa_id = Column(String(50), ForeignKey('mapa.id'))

    chromossome = Column('chromossome',Integer)
    position = Column('position', Integer)
    


engine = create_engine('mysql+pymysql://'+DB_USER+':'+DB_PASSWD+'@'+DB_IP+'/'+DB_NAME, echo=True)
session = scoped_session(sessionmaker(bind=engine))
BaseModel.set_session(session)

Base.metadata.create_all(bind=engine) # Descomentar se precisar recriar a estrutura