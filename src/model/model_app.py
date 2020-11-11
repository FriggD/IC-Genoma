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

class Animal_atributo(Base):
    

engine = create_engine('mysql+pymysql://root:secret@192.168.0.13/genoma', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# session = Session()
# animais = session.query(Animal).all()
# for animal in animais:
#     print(animal)

# session.close()