from ../models/model_app import Animal, Marcador, session

# CRUD
class Marcador_DB:
    def __init__(self, session):
        self.session = session

    def getById(self, marcador_snp):
        try: 
            # Recupera o animal do banco pelo snp
            return self.session.query(Marcador).filter_by(snp=marcador_snp).one()
            
        except:
            print("Erro ao tentar buscar Animal por snp")
            return False

    def getAllAnimais(): # Retorna todos os animais
        try: 
            # Recupera o animal do banco pelo snp
            # return self.session.query(Animal).all()
            marcadors = session.query(marcador).all()
            for marcador in marcadors:
        print(marcador)

        except:
            print("Erro ao tentar buscar todos os marcador")
            return False

    # Procura o nome em anim_nome, se encontrado, busca o registro do animal que contém o nome, senão, retorna False
    def getByName(self, name):
        try: 
            # Select por nome em animal_nome
            marcador_nome = self.session.query(Marcador_nome).filter_by(nome=name).one()
            #Select pelo snp retornado do animal_nome
            marcador_nome.marcador_snp
            return self.session.query(Marcador).filter_by(snp=marcador_nome.marcador_snp).one()
            #retorna o marcador encontrado
        except:
            print("Erro ao tentar buscar marcador pelo nome")
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


    # Recebe uma instância de marcador como parâmetro, e cria o registro dele no banco
    def createAll(self, marcadorArr):
        try: 
            self.session.add_all(marcadorArr)
            self.session.commit()

            return marcador
        except:
            print("Erro ao fazer o createAll (marcador)!")
            return False

    # Recebe um snp de marcador, e remove-o do banco
    def delete(self, marcador_snp):
        try: 
            # Recupera o marcador do banco pelo snp
            marcador = self.session.query(Marcador).filter_by(snp=marcador_snp).one()
            
            # Deleta o marcador
            self.session.delete(marcador)

            # Commita no banco as mudanças
            self.session.commit()
        except:
            print("Erro ao fazer o delete (marcador)!")
            return False

    # Atualiza um marcador utilizando o snp do mesmo
    def update(self, marcador):
        # try:
        # Recupera o marcador do banco de dados
        marcador_bd = self.session.query(Marcador).filter_by(snp=marcador.snp)

        # Atualiza os campos do animal
        # animal_bd.id_pai = animal.id_pai
        # animal_bd.id_mae = animal.id_mae
        # animal_bd.sexo = animal.sexo
        # animal_bd.data_nasc = animal.data_nasc