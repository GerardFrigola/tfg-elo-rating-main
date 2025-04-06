# TODO

### Objectiu
- Objectiu és calcular els ratings fins un cert punt i predir els resultats d'enfrontaments passats i futurs. 

### Sobre tenis:
- [] Aprendre sobre tenis
    - [] Saber els tipus de tornejos que hi ha
    - [] Saber com funciona un any sencer de tenis (tour?). Qualifiers, tornejos, ranquings, etc. 
    - [] Aprendre i entendre els rànquings
    - [] Entendre bé que son els swings
    - [] Quant dura normalment un torneig?

# Sobre git: 
- [] Crear docu llicència

### Sobre les dades:
- [] Winner entry? 
- [] Winner seed?
- [] Preprocess? 
- [] Quins matches tinc en compte

### Sobre paràmetres:
- [] Determinar K-factor 
    - [] En funció de què val una cosa o una altra? (competi, ronda, best_of, )
- [] Determinar Logistic Parameter
- [] Considerar altres paràmetres possibles
- [] Elo inicial quan entres?

### Sobre implementació: 
- [x] Codi fórmules bàsiques
- [x] Estructura general del projecte --> Anar definint
- [x] Estructura de les dades
    - [x] Quines dades necessito i quines no?
    - [x] Preprocess de dades?
- [x] poo?
- [] Vectoritzar llegir els csv amb pandas.
- [x] Afegir històric del rating
- [x] Fer ranking global sencer
    - [] Determinar paràmetres en funció de si és ranking històric o ranking de tour. 
- [] Inactivitat: Si una persona deixa de jugar fora del ranking. Però si torna que passa?
- [] Implementar opcions dels paràmetres. 
    - [] Tots els partits valen igual
    - [] Variar en funció del torneig
    - [] Altres 
- [] Que les funcions de simular i calcular no siguin de la classe Tour si no que rebin un tour com a argument. 
- [] Veure el ranking en una data concreta. Que pugui anar avançant temporalment manualment el ranking (per exemple setmana a setmana)
- [] Per pàgina web mirar paquet shiny per python.

### Sobre validació: 
- [] Implementar correlation coeficient --> Al final de cada tour
- [] Alguna manera d'avaluar 
- [] Fer servir fitxers atp_rankings per validar. 

### Sobre extres
- [] Aprendre els factors modificables que millor vagin? --> Fumada però en un futur podria ser una bona implementació





### Web: 
 - [ ] Preprocessar les dades
    - [ ] Importar dades de wta
    - [x] Llegir totes les dades de wta i atp per separat i concatenar-les (per separat)
    - [ ] Netejar les dades -> Filtrar les columnes que volem , fumarse 1968, assegurar not na, 

- Escriure els paràmetres k, xi, s
- calcular el rating 
    - Intentar millorar l'eficiència d'això
