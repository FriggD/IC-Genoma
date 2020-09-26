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
        self.tem_filhos     = dataArr[6]
        self.genoma_files   = str(dataArr[7]).split(sep=";")
        try:
            self.attr       = str(dataArr[8]).split(sep=";")
        except:
            self.attr = ""
    
    def add_animal_id(self, id):
        for animal_id in self.animal_id:
            if str(animal_id) == str(id):
                return
        self.animal_id.append(str(id))

    def get_attr_value(self, attr):
        attr = str(attr).upper().replace(' ', '_')
        for aux_attr in self.attr:
            try:
                key, value = aux_attr.split(sep=":")
                if key == attr:
                    return value
            except:
                continue
        return -1

    def has_attr(self, attr):
        attr = str(attr).upper().replace(' ', '_')
        for aux_attr in self.attr:
            try:
                key, value = aux_attr.split(sep=":")
                if key == attr:
                    return True
            except:
                continue
        return False

    def add_attr(self, attr, value):
        attr = str(attr).upper().replace(' ', '_')
        if str(value).strip() == "":
            return

        if not(self.has_attr(attr)):
            self.attr.append(str(attr)+ ":"+str(value))
        else:
            self.set_attr(attr, value)

    def set_attr(self, attr, value):
        attr = str(attr).upper().replace(' ', '_')
        if str(value).strip() == "":
            return

        for idx, aux_attr in enumerate(self.attr):
            try:
                key, value = aux_attr.split(sep=":")
            except:
                continue

            if key == attr:
                self.attr[idx] = str(attr)+":"+str(value)

    def __str__(self):
        return 'Animal {}, sexo {}, nascido em {}, pai: {}, mãe: {}'.format(self.animal_id, self.sexo, self.nasc, self.id_pai, self.id_mae)

    def toArray(self):
        return [";".join(self.animal_id), self.sexo, self.nasc, self.id_pai, self.id_mae, self.avo_materno, self.tem_filhos, ";".join(self.genoma_files), ";".join(self.attr)]

