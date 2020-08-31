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
    cur_AutoIncrement = 0

    def __init__(self, dataArr):
        self.animal_id      = str(dataArr[0]).split(sep=";")
        self.sexo           = dataArr[1]
        self.nasc           = dataArr[2]
        self.id_pai         = dataArr[3]
        self.id_mae         = dataArr[4]
        self.avo_materno    = dataArr[5]
        self.genoma_files   = str(dataArr[6]).split(sep=";")

    def __str__(self):
        return 'Animal {}, sexo {}, nascido em {}, pai: {}, mãe: {}'.format(self.animal_id, self.sexo, self.nasc, self.id_pai, self.id_mae)

    def toArray(self):
        return [";".join(self.animal_id), self.sexo, self.nasc, self.id_pai, self.id_mae, self.avo_materno, ";".join(self.genoma_files)]

