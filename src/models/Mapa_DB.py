from src.models.DB_Connection import Mapa_Schema

class Mapa_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, mapa_id):
        try: 
            # Recupera o animal do banco pelo id
            return self.session.query(Mapa_Schema).filter_by(id=mapa_id).one()
            
        except:
            print("Erro ao tentar buscar Mapa por id")
            return False

    # Retorna todos os registros da tabela Mapa
    def getAll(self):
        try: 
            return session.query(Mapa_Schema).all()         

        except:
            print("Erro ao tentar buscar todos os mapa")
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


    # Recebe uma lista de Mapa como parâmetro, e salva no banco 
    def createAll(self, mapaArr):
        try: 
            self.session.add_all(mapaArr)
            self.session.commit()

            return mapaArr
        except:
            print("Erro ao fazer o createAll (mapa)!")
            return False

    # Recebe um id de mapa, e remove-o do banco
    def delete(self, mapa_id):
        try: 
            # Recupera o mapa do banco pelo id
            mapa = self.session.query(Mapa_Schema).filter_by(id=mapa_id).one()
            # Deleta o mapa
            self.session.delete(mapa)
            # Commita no banco as mudanças
            self.session.commit()

            return True
        except:
            print("Erro ao fazer o delete (mapa)!")
            return False

    # Atualiza um mapa utilizando o id do mesmo
    def update(self, mapa):
        try:
            # Recupera o mapa do banco de dados
            mapa_bd = self.session.query(Mapa_Schema).filter_by(id=mapa.id)

            # Atualiza os campos do mapa
            mapa_bd.nome = mapa.nome
            mapa_bd.hash = mapa.hash
            mapa_bd.snp_count = mapa.snp_count
            mapa_bd.gerado_automaticamente = mapa.gerado_automaticamente

            self.session.commit()

            return mapa_bd

        except:
            print("Erro ao tentar atualizar (Mapa)!")
            return False