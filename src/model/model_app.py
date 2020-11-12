from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Animal(Base):
    __tablename__= "animal"
    id = Column('id', Integer, primary_key=True)
    id_Pai = Column('id_pai', Integer)
    id_Mae = Column('id_mae', Integer)
    sexo = Column('sexo', String(1))
    data_nasc = Column('data_nasc', Date)
    
    # username = Column('username', String(50), unique=True)

class Animal_nome(Base):
    __tablename__="animal_nome"
    id = Column('id', Integer, primary_key=True)
    nome = Column('nome',String(50), unique=True)
    principal = Column('principal', Boolean())
    animal_id = Column(Integer, ForeignKey('animal.id'))

class Atributo(Base):
    __tablename__="atributo"
    id = Column('id', Integer, primary_key=True)

class Animal_atributo(Base):
    __tablename__="animal_atributo"
    id = Column('id', Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animal.id'))
    atributo_id = Column(Integer, ForeignKey('atributo.id'))
    valor = Column('valor', String(50))

class Mapa(Base):
    __tablename__="mapa"
    id = Column('id', Integer, primary_key=True)
    nome = Column('nome',String(50), unique=True)
    hash = Column('hash', String(50), unique=True)
    snp_count = Column('snp_count', Integer)
    gerado_automaticamente = Column('gerado_automaticamente', Boolean())

class Animal_mapa(Base):
    __tablename__="Animal_mapa"
    id = Column('id', Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey('animal.id'))
    mapa_id = Column(Integer, ForeignKey('mapa.id'))

class Marcador(Base):
    __tablename__ = "marcador"
    snp = Column('snp', String(50), primary_key=True)
    missing_count = Column('missing_count', Integer, nullable=False)
    nomissing_count = Column('nomissing_count', Integer, nullable=False)
    aa_count = Column('aa_count', Integer, nullable=False)
    bb_count = Column('bb_count', Integer, nullable=False)
    ab_count = Column('ab_count', Integer, nullable=False)
    desconhecido_count = Column('desconhecido_count', Integer, nullable=False)

class Mapa_marcador(Base):
    __tablename__ = "mapa_marcador"
    id = Column('id', Integer, primary_key=True)
    snp_id = Column(String(50), ForeignKey('marcador.snp'))
    mapa_id = Column(Integer, ForeignKey('mapa.id'))

engine = create_engine('mysql+pymysql://root:secret@192.168.0.13/genoma', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# session = Session()
# animais = session.query(Animal).all()
# for animal in animais:
#     print(animal)

# session.close()