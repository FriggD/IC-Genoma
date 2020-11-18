from ../models/model_app import Atributo, session
# Create, create_all, getAll

class Atributo_DB:
    def __init__(self, session):
        self.session = session
 # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, atributo):
        try: 
            self.session.add(atributo)
            self.session.commit()

            return atributo
        except:
            print("Erro ao fazer o create (Atributo)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr_atributo):
        try: 
            self.session.add_all(animaisArr_atributo)
            self.session.commit()

            return atributo
        except:
            print("Erro ao fazer o createAll (atributo)!")
            return False

    def getAllAtributos(): # Retorna todos os atributos
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            atributos = session.query(Atributo).all()
            for atributo in atributos:
        print(atributo)

        except:
            print("Erro ao tentar buscar todos os Atributos")
            return False
