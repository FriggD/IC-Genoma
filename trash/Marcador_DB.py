from src.models.DB_Connection import Marcador_Schema

class Marcador_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, marcador_snp):
        try: 
            # Recupera o marcador do banco pelo snp
            return self.session.query(Marcador_Schema).filter_by(snp=marcador_snp).one()
            
        except:
            print("Erro ao tentar buscar Marcador por snp")
            return False

    # Retorna todos os registros da tabela Marcador
    def getAll(self):
        try: 
            return session.query(Marcador_Schema).all()         

        except:
            print("Erro ao tentar buscar todos os marcadores")
            return False


    # Recebe uma instância de marcador como parâmetro, e cria o registro dele no banco
    def create(self, marcador):
        try: 
            self.session.add(marcador)
            self.session.commit()

            return marcador
        except:
            print("Erro ao fazer o create (marcador)!")
            return False


    # Recebe uma lista de Marcadores, e os salva no banco
    def createAll(self, marcadorArr):
        try: 
            self.session.add_all(marcadorArr)
            self.session.commit()

            return marcadorArr
        except:
            print("Erro ao fazer o createAll (marcador)!")
            return False

    # Recebe um snp de marcador, e remove-o do banco
    def delete(self, marcador_snp):
        try: 
            # Recupera o marcador do banco pelo snp
            marcador = self.session.query(Marcador_Schema).filter_by(snp=marcador_snp).one()
            
            # Deleta o marcador
            self.session.delete(marcador)

            # Commita no banco as mudanças
            self.session.commit()
            
            return True
        except:
            print("Erro ao fazer o delete (marcador)!")
            return False

    # Atualiza um marcador utilizando o snp do mesmo
    def update(self, marcador):
        try:
            # Recupera o marcador do banco de dados
            marcador_bd = self.session.query(Marcador_Schema).filter_by(snp=marcador.snp)

            # Atualiza os campos do animal
            marcador_bd.missing_count = marcador.missing_count
            marcador_bd.nomissing_count = marcador.nomissing_count
            marcador_bd.aa_count = marcador.aa_count
            marcador_bd.bb_count = marcador.bb_count
            marcador_bd.ab_count = marcador.ab_count
            marcador_bd.desconhecido_count = marcador.desconhecido_count

            # Atualiza no banco a informações
            self.session.commit()
            
            return marcador_bd

        except:
            print("Erro ao tentar atualizar (Marcador_Schema)!")
            return False

