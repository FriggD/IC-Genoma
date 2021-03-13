from src.models.DB_Connection import Animal_Schema, Animal_nome_Schema

class Animal_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, animal_id):
        try: 
            # Recupera o animal do banco pelo id
            return self.session.query(Animal_Schema).filter_by(id=animal_id).one()
            
        except:
            print("Erro ao tentar buscar Animal por id")
            return False

    # Retorna todos os animais
    def getAll(self):
        try: 
            return session.query(Animal_Schema).all()           

        except:
            print("Erro ao tentar buscar todos os Animal")
            return False

    # Procura o nome em Animal_nome_Schema, se encontrado, busca o registro do animal que contém o nome, senão, retorna False
    def getByName(self, name):
        try:
            # Select por nome em animal_nome
            animal_nome = self.session.query(Animal_nome_Schema).filter_by(nome=name).one()
            # Select pelo id retornado do animal_nome e Retorna o animal encontrado
            return self.session.query(Animal_Schema).filter_by(id=animal_nome.animal_id).one()
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


    # Recebe uma lista de Animal como parâmetro, e os salva no banco como um batch de dados
    def createAll(self, animaisArr):
        try: 
            self.session.add_all(animaisArr)
            self.session.commit()

            return animaisArr
        except:
            print("Erro ao fazer o createAll (Animal)!")
            return False

    # Recebe um id de animal, e remove-o do banco
    def delete(self, animal_id):
        try: 
            # Recupera o animal do banco pelo id
            animal = self.session.query(Animal_Schema).filter_by(id=animal_id).one()
            # Deleta o animal
            self.session.delete(animal)
            # Commita no banco as mudanças
            self.session.commit()
            return True
        except:
            print("Erro ao fazer o delete (Animal)!")
            return False

    # Atualiza um animal no banco
    def update(self, animal):
        try:
            # Recupera o animal do banco de dados
            animal_bd = self.session.query(Animal_Schema).filter_by(id=animal.id)

            # Atualiza os campos do animal
            animal_bd.id_pai = animal.id_pai
            animal_bd.id_mae = animal.id_mae
            animal_bd.sexo = animal.sexo
            animal_bd.data_nasc = animal.data_nasc

            # Atualiza no banco as informações
            self.session.commit()

            return animal_bd

        except:
            print("Erro ao tentar atualizar (Animal)!")
            return False

# TESTES 
# Comentar após testar
"""
animal_session = Animal_DB(session)
animal_session.create(Animal(sexo="M", data_nasc="2020-01-01"))

# Teste de criação de um Animal
animal_session = Animal_DB(session)

animal_20 = animal_session.getById(20)
if not(animal_20):
    # Significa que o animal com id 20 não existe

animal_20.id_pai = 5

animal_session.update(animal_20)
"""