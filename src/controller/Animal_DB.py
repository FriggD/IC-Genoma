from ../models/model_app import Animal, Animal_nome, session

class Animal_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, animal_id):
        try: 
            # Recupera o animal do banco pelo id
            return self.session.query(Animal).filter_by(id=animal_id).one()
            
        except:
            print("Erro ao tentar buscar Animal por id")
            return False

    def getAllAnimais(): # Retorna todos os animais
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            animais = session.query(Animal).all()
            for animal in animais:
        print(animal)

        except:
            print("Erro ao tentar buscar todos os Animal")
            return False

    # Procura o nome em anim_nome, se encontrado, busca o registro do animal que contém o nome, senão, retorna False
    def getByName(self, name):
        try: 
            # Select por nome em animal_nome
            animal_nome = self.session.query(Animal_nome).filter_by(nome=name).one()
            #Select pelo id retornado do animal_nome
            animal_nome.animal_id
            return self.session.query(Animal).filter_by(id=animal_nome.animal_id).one()
            #retorna o animal encontrado
        except:
            print("Erro ao tentar buscar Animal pelo nome")
            return False


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
"""
# Teste de criação de um Animal
animal_session = Animal_DB(session)

animal_20 = animal_session.getById(20)
if not(animal_20):
    # Significa que o animal com id 20 não existe

animal_20.id_pai = 5

animal_session.update(animal_20)




"""