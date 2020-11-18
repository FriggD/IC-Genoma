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
    
    def delete(self, animal_atributo_id):
        try: 
            # Recupera o animal do banco pelo id
            animal_atributo = self.session.query(Animal_atributo).filter_by(id=animal_atributo_id).one()
            
            # Deleta o animal
            self.session.delete(animal_atributo)

            # Commita no banco as mudanças
            self.session.commit()
        except:
            print("Erro ao fazer o delete (animal_atributo)!")
            return False

    # Atualiza um animal utilizando o id do mesmo
    def update(self, animal_atributo):
        # try:
        # Recupera o animal do banco de dados
        animal_atributo_bd = self.session.query(animal_atributo).filter_by(id=animal_atributo.id)

        # Atualiza os campos do animal
        animal_atributo_bd.animal_id = animal_atributo.animal_id
        animal_atributo_bd.atributo_id = animal_atributo.atributo_id
        animal_atributo_bd.sexo = animal_atributo.sexo
        animal_atributo_bd.valor = animal_atributo.valor

        # Atualiza no banco as informações
        self.session.commit()