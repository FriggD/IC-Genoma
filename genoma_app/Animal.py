ANIMAL_ID = 0
ID_PAI = 1
PAI_GENOMA = 2
ID_MAE = 3
MAE_GENOMA = 4
PATH_35K = 5
PATH_50K = 6
PATH_75K = 7
PATH_90K = 8

class Animal:
    def __init__(self, dataArr):
        self.animal_id  = dataArr[0].split(sep=";")
        self.id_pai     = dataArr[1]
        self.pai_genoma = dataArr[2]
        self.id_mae     = dataArr[3]
        self.mae_genoma = dataArr[4]
        self.path_35k   = dataArr[5]
        self.path_50k   = dataArr[6]
        self.path_75k   = dataArr[7]
        self.path_90k   = dataArr[8]

    def mostrar_informacoes(self):
        print('Olá, sou o animal de código', self.animal_id, ' Nasci dos pais ', self.id_pai,'(pai) e ', self.id_mae, '(mae)')

    def toArray(self):
        return [";".join(self.animal_id), self.id_pai, self.pai_genoma, self.id_mae, self.mae_genoma, self.path_35k, self.path_50k, self.path_75k, self.path_90k]
