from src.models.DB_Connection import Animal_atributo_Schema
# create, create_all, delete, update, getAll

class Animal_atributo_DB:
    def __init__(self, session):
        self.session = session


    # Retorna todos todos registros de Animal_atributos
    def getAll(self):
        try: 
            return session.query(Animal_atributo_Schema).all()       

        except:
            print("Erro ao tentar buscar todos os Animais_atributos")
            return False


    # Recebe uma instância de Animal_atributo_Schema como parâmetro, e cria o registro dele no banco
    def create(self, animal_atributo):
        try: 
            self.session.add(animal_atributo)
            self.session.commit()

            return animal_atributo
        except:
            print("Erro ao fazer o create (Animal_atributo)!")
            return False


    # Recebe uma lista de Animais_atributos como parâmetro, e os salva no banco
    def createAll(self, animal_atributoArr):
        try: 
            self.session.add_all(animal_atributoArr)
            self.session.commit()

            return animal_atributoArr
        except:
            print("Erro ao fazer o createAll (Animal_atributo)!")
            return False
    
    # Recebe um id de Animal_atributo, e remove-o do banco
    def delete(self, animal_atributo_id):
        try: 
            # Recupera o animal_atributo do banco pelo id
            animal_atributo = self.session.query(Animal_atributo_Schema).filter_by(id=animal_atributo_id).one()
            # Deleta o animal
            self.session.delete(animal_atributo)
            # Commita no banco as mudanças
            self.session.commit()
            return True
        except:
            print("Erro ao fazer o delete (animal_atributo)!")
            return False

    # Atualiza um animal utilizando o id do mesmo
    def update(self, animal_atributo):
        try:
            # Recupera o animal_atributo do banco de dados
            animal_atributo_bd = self.session.query(Animal_atributo_Schema).filter_by(id=animal_atributo.id)

            # Atualiza os campos do animal
            animal_atributo_bd.animal_id = animal_atributo.animal_id
            animal_atributo_bd.atributo_id = animal_atributo.atributo_id
            animal_atributo_bd.sexo = animal_atributo.sexo
            animal_atributo_bd.valor = animal_atributo.valor

            # Atualiza no banco as informações
            self.session.commit()
        except:
            print("Erro ao tentar atualizar (Animal_atributo)!")
            return False