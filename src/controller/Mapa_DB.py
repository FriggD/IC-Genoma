from ../models/model_app import Animal, Mapa, session

# CRUD
class Mapa_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, mapa_id):
        try: 
            # Recupera o animal do banco pelo id
            return self.session.query(Mapa).filter_by(id=mapa_id).one()
            
        except:
            print("Erro ao tentar buscar Animal por id")
            return False

    def getAllAnimais(): # Retorna todos os animais
        try: 
            # Recupera o animal do banco pelo id
            # return self.session.query(Animal).all()
            mapas = session.query(mapa).all()
            for mapa in mapas:
        print(mapa)

        except:
            print("Erro ao tentar buscar todos os mapa")
            return False

    # Procura o nome em anim_nome, se encontrado, busca o registro do animal que contém o nome, senão, retorna False
    def getByName(self, name):
        try: 
            # Select por nome em animal_nome
            mapa_nome = self.session.query(Mapa_nome).filter_by(nome=name).one()
            #Select pelo id retornado do animal_nome
            mapa_nome.mapa_id
            return self.session.query(Mapa).filter_by(id=mapa_nome.mapa_id).one()
            #retorna o mapa encontrado
        except:
            print("Erro ao tentar buscar mapa pelo nome")
            return False


    # Recebe uma instância de mapa como parâmetro, e cria o registro dele no banco
    def create(self, mapa):
        try: 
            self.session.add(mapa)
            self.session.commit()

            return mapa
        except:
            print("Erro ao fazer o create (mapa)!")
            return False


    # Recebe uma instância de mapa como parâmetro, e cria o registro dele no banco
    def createAll(self, mapaArr):
        try: 
            self.session.add_all(mapaArr)
            self.session.commit()

            return mapa
        except:
            print("Erro ao fazer o createAll (mapa)!")
            return False

    # Recebe um id de mapa, e remove-o do banco
    def delete(self, mapa_id):
        try: 
            # Recupera o mapa do banco pelo id
            mapa = self.session.query(Mapa).filter_by(id=mapa_id).one()
            
            # Deleta o mapa
            self.session.delete(mapa)

            # Commita no banco as mudanças
            self.session.commit()
        except:
            print("Erro ao fazer o delete (mapa)!")
            return False

    # Atualiza um mapa utilizando o id do mesmo
    def update(self, mapa):
        # try:
        # Recupera o mapa do banco de dados
        mapa_bd = self.session.query(Mapa).filter_by(id=mapa.id)

        # Atualiza os campos do animal
        # animal_bd.id_pai = animal.id_pai
        # animal_bd.id_mae = animal.id_mae
        # animal_bd.sexo = animal.sexo
        # animal_bd.data_nasc = animal.data_nasc