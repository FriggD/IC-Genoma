from model_app import Animal, session

class Animal_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, animal_id):
        try: 
            # Recupera o animal do banco pelo id
            return self.session.query(Animal).filter_by(id=animal_id).one()
            
        except:
            print("Erro aop tentar buscar Animal por id")
            return False

    # Procura o nome em anim_nome, se encontrado, busca o registro do animal que contém o nome, senão, retorna False
    # def getByName(self, nae):

    # def 

    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def create(self, animal):
        try: 
            self.session.add(animal)
            self.session.commit()

            return animal
        except:
            print("Erro ao fazer o create (Animal)!")
            return False


    # Recebe uma instância de animal como parâmetro, e cria o registro dele no banco
    def createAll(self, animaisArr):
        try: 
            self.session.add_all(animaisArr)
            self.session.commit()

            return animal
        except:
            print("Erro ao fazer o createAll (Animal)!")
            return False

    # Recebe um id de animal, e remove-o do banco
    def delete(self, animal_id):
        try: 
            # Recupera o animal do banco pelo id
            animal = self.session.query(Animal).filter_by(id=animal_id).one()
            
            # Deleta o animal
            self.session.delete(animal)

            # Commita no banco as mudanças
            self.session.commit()
        except:
            print("Erro ao fazer o delete (Animal)!")
            return False

    # Atualiza um animal utilizando o id do mesmo
    def update(self, animal):
        # try:
        # Recupera o animal do banco de dados
        animal_bd = self.session.query(Animal).filter_by(id=animal.id)

        # Atualiza os campos do animal
        animal_bd.id_pai = animal.id_pai
        animal_bd.id_mae = animal.id_mae
        animal_bd.sexo = animal.sexo
        animal_bd.data_nasc = animal.data_nasc

        # Atualiza no banco as informações
        self.session.commit()

        # except:
        #     print("Erro ao tentar atualizar (Animal)!")
        #     return False

# TESTES 
# Comentar após testar

# Teste de criação de um Animal
animal_session = Animal_DB(session)

animal_20 = animal_session.getById(20)

animal_20.id_pai = 5

animal_session.update(animal_20)

# retorno = animal_session.create(Animal(sexo="M", data_nasc="2020-11-11"))
# print("Retorno:", retorno)

# animais = session.query(Animal).all()
# for animal in animais:
#     print(animal)


# print(animais)