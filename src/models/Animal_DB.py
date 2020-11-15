from model_app import Animal, session

class Animal_DB:
    def __init__(self, session):
        self.session = session

    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, animal):
        try: 
            self.session.add(animal)
            self.session.commit()

            return animal
        except:
            print("Erro!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    # def createAll(self, animaisArr):

    # Recebe um id de animal, e remove-o do banco
    # def delete(self, animal_id):

    # Atualiza um animal utilizando o id do mesmo
    # def update(self, animal):

# TESTES 
# Comentar após testar

# Teste de criação de um Animal
animal_session = Animal_Db(session)
retorno = animal_session.create(Animal(sexo="M", data_nasc="2020-11-11"))
print("Retorno:", retorno)

# animais = session.query(Animal).all()
# for animal in animais:
#     print(animal)


# print(animais)