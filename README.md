# README

## Objectiu
L'objectiu d'aquest treball és desenvolupar un programari que calculi un ràting Elo a partir de les dades històriques de tornejos de tenis professional, que permeti anar incorporant noves dades i ajustar a voluntat determinats paràmetres. 

## Llibreries
El projecte esta fet completament amb python i les llibreries que faig servir son les bàsiques numpy, pandas, etc. 
Per poder instal·lar les llibreries has de tenir conda instalat al teu ordinador i executar el fitxer `env.cmd` (en windows) o el fitxer `env.sh` (en macOs i Linux).

## Estructura

A la carpeta `modeling` hi trobaràs els següents fitxers: 

  - `main.py`: Conté el codi principal on es criden les diferents funcions que executen el projecte.

  - `entities.py`: Conté les classes `Tour`, `Match` i `Player` amb les seves respectives funcions. 

  - `data.py`: Conté el codi que carrega totes les dades dels partits. 



A la carpeta `data` hi trobaràs tots els fitxers .csv amb la informació de diferents tipus de partits. Cada fixer conté tots els partits d'un Tour (any) sencer. Aquests partits estàn estructurats en diferents carpetes. 

  - `atp_matches`: Partits individuals de l'ATP des de 1968 fins a 2024.

  - `atp_matches_doubles`: Partits de dobles d'ATP des de 2000 fins a 2020. --> Aquesta info no la faig servir.

  - `atp_matches_futures`: No la faig servir.

  - `atp_matches_quall_chall`: Qualificacions challenger. No la faig servir.

  - `atp_rankings`: Evolució dels rankigns de l'ATP en el temps. Cada fitxer és una dècada.

  - `examples`: No la faig servir, l'eliminaré.

  - `atp_players.csv`: Fitxer amb tots els jugadors que apareixen al projecte.

  - `atp_matches_amateur`: No la faig servir.


A la carpeta `outputs`es guardaràn les sortides


A la carpeta `config`hi ha els fitxers de configuració -> TODO

## Execució 

Per executar el projecte assegura't de tenir totes les llibreries i dependències instal·lades i al terminal escriu la comanda: 

`python ./modeling/main.py`

De moment aquesta execució només genera un rànquing històric de tots els jugadors des de 1968 fins 2024, fent servir l'ELO rating. Aquesta informació es guarda en el fitxer `rankings.txt`

## Llicència
