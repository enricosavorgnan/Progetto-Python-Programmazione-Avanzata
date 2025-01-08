### Programmazione Avanzata e Parallela
### A.A. 2024-2025
### Università degli Studi di Trieste

<br>

#### Savorgnan Enrico
#### SM 320 1371

<br>

# Progetto in Python
## LMC Assembler
<br><br><br>


<br><br><br>
### Indice
1. [Introduzione](#Introduzione)
2. [Descrizione](#Descrizione)
3. [Esecuzione](#Esecuzione)
4. [Conclusioni](#Conclusioni)
<br><br><br>


### Introduzione
Il progetto consiste nella realizzazione di un programma in Python che permetta, dato in input un file in formato .lmc, di convertirlo in un assembler specifico e di eseguirlo, restituendo una coda di output.  
Il progetto è stato realizzato come progetto finale del corso di Programmazione Avanzata e Parallela, tenuto dal Prof. Luca Manzoni.
<br><br><br>


### Descrizione
Il progetto è stato realizzato in Python ed è composto da 4 file:
- `main.py` : file principale del progetto, gestisce il flusso di esecuzione del programma.
- `assembler.py` : file contenente la classe `Assembler` che si occupa, dato in input il file .lmc, di popolare la memoria e di convertire le istruzioni in uno specifico codice macchina.
- `lmc.py` : file contenente la classe `LMC` che si occupa di eseguire il codice macchina generato dal file `assembler.py`. 
- `exceptions.py` : file contenente le eccezioni personalizzate del progetto.

Più nello specifico:


<br><br>
#### main.py
   - Il file `main.py` è composto da un'unica funzione, `main()`, che si occupa di gestire il flusso di esecuzione del programma.  
<br>
   - In particolare, la funzione `main()` si occupa di:
     - Aprire il file *.lmc* in input.
     - Creare un'istanza della classe `Assembler` e di popolare la memoria.
     - Creare un'istanza della classe `LMC` e di eseguire il codice macchina. All'utente è chiesto di scegliere tra un'esecuzione "non-stop" oppure "step-by-step". Nel secondo caso, il programma esegue un'istruzione alla volta, aspettando un'indicazione da parte dell'utente per proseguire, e stampando lo status del programma a ciascuno step.  
     - Stampare l'output della coda ottenuta al termine dell'esecuzione del codice.  
     
<br><br>
#### assembler.py
   - Il file `assembler.py` è composto dalla classe `Assembler`. Questa accetta in input il nome del file *.lmc* e si occupa di:
     - Inizializzare le componenti essenziali per la conversione del file in codice macchina. 
     - Eseguire dei check preliminari 
     - Popolare la memoria con le istruzioni del file in uno specifico formato di codice macchina. <br><br>
   - In particolare, la classe `Assembler` è composta dai seguenti metodi:
     - `__init__(self, file_name: list[str])` : costruttore della classe, accetta in input il nome del file *.lmc*. Vengono inizializzati i seguenti attributi:
       - `self.file : list[str]` : il nome del file *.lmc*
       - `self.memory : list[int]` : la memoria del codice macchina, contiene esattamente 100 valori.
       - `self.labels : dict{str: int}` : dizionario che mappa le label al valore della cella di memoria in cui vengono definite.
       - `self.opcodes : dict{str: int}` : dizionario che mappa le istruzioni al loro corrispondente opcode.
       - `self.needs_input : bool` : flag che indica se il programma necessita di input da parte dell'utente.
     - `assemble(self)` : si occupa della conversione del *.lmc* in codice macchina. Modifica l'attributo `self.memory` cella per cella. All'inizio invoca i metodi `preprocess_file(self)` e `check_for_labels(self)` rispettivamente per fare preprocessing del file e ricercare, all'interno del *.lmc*, le label.  
     Il metodo tratta diversamente le funzioni `dat`, per cui è necessario che il valore successivo, se esiste, sia un intero, e `inp`,`out`, `hlt`, che aggiungono alla memoria non un valore ma il loro specifico opcode.
     - `preprocess_file(self)` : si occupa di fare preprocessing del file *.lmc*. Rimuove i commenti e le righe vuote e scrive ogni riga del file in carattere minuscolo. Alza un'eccezione al termine del metodo se il file risultante è vuoto (e.g. se ogni riga del file è commentata).
     - `check_for_labels(self)` : si occupa di cercare, all'interno del file .lmc, le label. Queste possono trovarsi all'inizio di una riga contenente o 2 o 3 parole. È però necessario che la label sia seguita da un'istruzione valida, altrimenti viene alzata un'eccezione.  

     <br><br>
#### lmc.py
- Il file `lmc.py` è composto dalla classe `LMC`. Questa accetta in input un'istanza della classe `Assembler`, da cui ricava gli attributi `self.memory` e `self.needs_input`, e si occupa di eseguire il codice macchina, nella modalità scelta dall'utente. <br><br>
- In particolare, la classe `LMC` è composta dai seguenti metodi (in ordine di chiamata):
  - `__init__(self, memory: List[int])` : costruttore della classe, accetta in input un oggetto della classe `Assembler`. Vengono inizializzati i seguenti attributi:
    - `self.memory : List[int]`  : la memoria del codice macchina. Viene ereditata dalla classe `Assembler`.
    - `self.needs_input : bool` : flag che indica se il programma necessita di input da parte dell'utente. Viene ereditata dalla classe `Assembler`.
    - `self.accumulator : int` : l'accumulatore
    - `self.program_counter : int` : il program counter
    - `self.input_queue : Queue()` : la coda di input
    - `self.output_queue : Queue()` : la coda di output
    - `self.overflow : bool` : flag che indica se le operazioni di somma e sottrazione hanno prodotto overflow o underflow
    - `self.running : bool` : flag che indica se il programma è in esecuzione
    - `self.opcodes : Dict{int: function}` : dizionario che mappa l'opcode dell'istruzione al metodo corrispondente.
  <br>
  - `run(self)` : si occupa del flusso di esecuzione del programma. Questo termina quando l'attributo `self.running` è `False`, condizione passabile dai metodi `__hlt()` e `__inp()`. In particolare, si occupa di 
    - inizializzare la coda di input tramite il metodo `user_input()` 
    - ricavare l'istruzione dalla cella di memoria indicata dal program counter, 
    - incrementare il program counter
    - invocare il metodo `execute()` passando l'istruzione ricavata dalla memoria.
  - `run_steps(self)` : similmente alla funzione `run(self)` di cui sopra, si occupa del flusso di esecuzione del programma, ma eseguendo un'istruzione alla volta: questo metodo viene inizializzato e gestito dal file `main.py` come un generatore. A ciascuna iterazione, all'utente è chiesto di inserire un input per proseguire con l'esecuzione del programma. L'uso di questo metodo permette di verificare lo status interno del programma, mostrato a ciascuna iterazione.
  - `user_input(self)` : si occupa di inizializzare la coda di input. In particolare, chiede all'utente di inserire un input, verifica che questo sia di tipo `int` e compreso in [0, 999] e lo aggiunge alla coda di input. Il ciclo termina quando l'utente inserisce il valore `-1`. Nel caso in cui vengano inseriti valori non validi (i.e. non numeri, o interi negativi o maggiori di 999), viene passata un'eccezione e il programma termina.
  - `execute(self, instruction: int)` : si occupa dell'esecuzione del codice macchina. In particolare, a partire dal valore in input `instruction` ricava l'opcode dell'istruzione e la cella interessata dalla stessa. Se l'istruzione è uno dei due valori *speciali* `901` o `902` vengono invocati i metodi `__inp()` e `__out()`. Altrimenti, viene invocato il metodo corrispondente all'opcode dell'istruzione, secondo quanto indicato dal dizionario `self.opcodes`.
  - `__inp(self)` : si occupa di leggere un valore da `self.input_queue` e di salvarlo in `self.accumulator`.
  - `__out(self)` : si occupa di leggere il valore in `self.accumulator` e di inserirlo nella coda di output `self.output_queue`.
  - `__add(self, cell: int)` : somma il valore in `self.accumulator` con il valore contenuto nella cella di memoria `cell`. Invoca il metodo `__update_flag()` per aggiornare `self.overflow`.
  - `_sub(self, cell: int)` : sottrae il valore in `self.accumulator` con il valore contenuto nella cella di memoria `cell`. Invoca il metodo `__update_flag()` per aggiornare `self.overflow`.
  - `__sta(self, cell: int)` : salva il valore in `self.accumulator` nella cella di memoria `cell`.
  - `__lda(self, cell: int)` : carica il valore contenuto nella cella di memoria `cell` in `self.accumulator`.
  - `__bra(self, cell: int)` : setta il program counter al valore `cell`. È un branch non condizionale.
  - `_brz(self, cell: int)` : setta il program counter al valore `cell` se sia `self.accumulator` che `self.overflow` sono uguali a 0. È un branch condizionale.
  - `__brp(self, cell: int)` : setta il program counter al valore `cell` se `self.overflow` è uguale a 0. È un branch *if positive*.
  - `__hlt(self, trash)` : setta `self.running` a `False`, terminando il flusso di esecuzione del programma. L'attributo `trash` è un valore non usato ma introdotto per mantenere la forma  con gli altri metodi.
  - `__update_flag(self)` : aggiorna `self.overflow` in base al risultato dell'operazione di somma o sottrazione. In particolare, se il risultato è maggiore di 999 o minore di 0, setta `self.overflow` a `True` e assegna a `self.accumulator` il suo valore in modulo 1000.
  - `print_queue(self)` : stampa i valori contenuti in `self.output_queue`.

<br><br>
#### exceptions.py
- Il file contiene le eccezioni personalizzate del progetto. Si è ritenuto conveniente di gestire il più possibile le eccezioni in maniera che queste non siano direttamente "visibili" da parte dell'utente, ma piuttosto che il programma termini ordinatamente con un messaggio di errore.  
In particolare, sono state definite le seguenti eccezioni:
  - `AssembleException` : eccezione generica per errori durante il preprocessing e l'assembling del file.
  - `UserException` : eccezione generica per errori relativi all'input dell'utente. Un errore di questo tipo può essere causato da un input di tipo non `int` o da un input non compreso in [0, 999]. L'unico altro valore accettabile è `-1`, che termina il ciclo di input.
  - `OpcodeException` : eccezione generica per errori relativi all'opcode dell'istruzione. Un errore di questo tipo può essere causato da un opcode non riconosciuto, per esempio 4.
  - `InternalException`: eccezione che viene alzata se, per qualche ragione, il valore del program counter eccede i limiti [0-99]


<br><br><br>
### Esecuzione
Per eseguire il programma, è sufficiente eseguire il file `main.py`:
```
python3 main.py
```
Il programma chiederà in input il path al file *.lmc* da eseguire.
Il codice può alzare diverse eccezioni se il file *.lmc* non è correttamente scritto. Si veda la sezione sopra per maggiori dettagli sulle eccezioni.


<br><br><br>
### Conclusioni
Per eventualità, contattarmi all'indirizzo email `enrico.savorgnan@studenti.units.it`. 



