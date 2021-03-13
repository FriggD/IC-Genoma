from src.models.DB_Connection import Atributo_Schema

class Atributo_DB:
    def __init__(self, session):
        self.session = session


    # Retorna todos registros da tabela Atributo
    def getAll(self):
        try: 
            return session.query(Atributo_Schema).all()

        except:
            print("Erro ao tentar buscar todos os Atributos")
            return False


    # Recebe uma instância de Atributo como parâmetro, e cria o registro dele no banco
    def create(self, atributo):
        try: 
            self.session.add(atributo)
            self.session.commit()

            return atributo
        except:
            print("Erro ao fazer o create (Atributo)!")
            return False


    # Recebe uma lista de Atributo como parâmetro, e salva no banco
    def createAll(self, animal_atributoArr):
        try: 
            self.session.add_all(animal_atributoArr)
            self.session.commit()

            return animal_atributoArr
        except:
            print("Erro ao fazer o createAll (atributo)!")
            return False


"""
# Teste de criação de um Animal
animal_session = Animal_DB(session)

animal_20 = animal_session.getById(20)
if not(animal_20):
    # Significa que o animal com id 20 não existe

animal_20.id_pai = 5

animal_session.update(animal_20)

"""
