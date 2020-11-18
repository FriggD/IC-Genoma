from ../models/model_app import Animal, Atributo, Animal_atributo, session
# create, create_all, delete, update, getAll

class Animal_atributo_DB:
    def __init__(self, session):
        self.session = session
# Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, Animal_atributo):
        try: 
            self.session.add(Animal_atributo)
            self.session.commit()

            return Animal_atributo
        except:
            print("Erro ao fazer o create (Animal_atributo)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr_Animal_atributo):
        try: 
            self.session.add_all(animaisArr_Animal_atributo)
            self.session.commit()

            return Animal_atributo
        except:
            print("Erro ao fazer o createAll (Animal_atributo)!")
            return False

    def getAllAtributos(): # Retorna todos os atributos
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            Animais_atributos = session.query(Animal_atributo).all()
            for Animal_atributo in Animais_atributos:
        print(Animal_atributo)

        except:
            print("Erro ao tentar buscar todos os Animais_atributos")
            return False
