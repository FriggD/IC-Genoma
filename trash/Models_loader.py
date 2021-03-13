from src.models.Animal_atributo_DB import Animal_atributo_DB
from src.models.Animal_DB import Animal_DB
from src.models.Animal_mapa_DB import Animal_mapa_DB
from src.models.Animal_nome_DB import Animal_nome_DB
from src.models.Atributo_DB import Atributo_DB
from src.models.Mapa_DB import Mapa_DB
from src.models.Mapa_marcador_DB import Mapa_marcador_DB
from src.models.Marcador_DB import Marcador_DB

from src.models.DB_Connection import session


Animal_atributo = Animal_atributo_DB(session)
Animal = Animal_DB(session)
Animal_mapa = Animal_mapa_DB(session)
Animal_nome = Animal_nome_DB(session)
Atributo = Atributo_DB(session)
Mapa = Mapa_DB(session)
Mapa_marcador = Mapa_marcador_DB(session)
Marcador = Marcador_DB(session)