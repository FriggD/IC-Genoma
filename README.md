# SISTEMA COMPUTACIONAL PARA IMPUTAÇÃO DE DADOS GENÔMICOS
## Objetivos:
- Desenvolver um sistema informatizado que estime a probabilidade de transmissão de alelos através das gerações de espécies de interesse zootécnico.
- Aplicar as técnicas de probabilidade em ordem computacional, possibilitando a imputação de dados genômicos.

## Sistema de pastas:
- dados
    - Aqui ficarão todos os csv's dos animais
    - Animais
        - mais alguns csv's

- Python-app
    - Data
        - Application
        - Input

    - IC-Genoma
        - src
            - Aqui ficarão os códigos

## Arquivos.py
### App
    É o programa de entrada, onde são extraídos os dados do genoma.

### Animal
    Os dados de cada animal são organizados conforme seu id, id do pai, genoma do pai, id da mãe,
     genoma da mãe e o caminho até om genoma do próprio animal, sendo este separado pela 
     quanntidade de marcadores.

### AnimaisCtrl
    Gera um arquivo csv com os dados 'Animal_id', 'sexo', 'data_nascimento', 'id_pai', 'id_mae', 
    'avo_materno', 'tem_filhos', 'genoma_files'. 
        
### Genomas
    Podem existir vários tipos de genoma, como de 65k marcadores, 90k marcadores, etc..., para isso foi criado uma tabela que terá controle em todos os tipos de genoma que passaram pelo sistema, essa tabela é referenciada pelo Animal, isso significa que aquele animal possui este tipo de arquivo de genoma

### Info_Animais
    