
---

# NB1 — Baseline LightGBM con pipeline temporale corretta

## Obiettivo

Costruire una baseline di forecasting corretta per il dataset Store Sales, mantenendo la coerenza temporale delle serie `store_nbr × family`, evitando leakage e creando lag features affidabili.

## Pipeline del notebook

### 1. Caricamento del dataset

Ho caricato `train.csv` e `test.csv` dal progetto locale.

**Perché:**  
Prima di costruire il modello devo controllare:

- dimensione del dataset
- colonne disponibili
- tipo delle variabili
- intervallo temporale coperto dai dati

Nel train ci sono circa 3 milioni di righe e le date vanno dal 2013-01-01 al 2017-08-15.

### 2. Ordinamento dei dati

Ho ordinato il dataset per:

- `store_nbr`
- `family`
- `date`

**Perché:**  
Questo è fondamentale in una time series panel.  
Le lag features devono essere calcolate su una serie temporale ordinata.  
Se i dati non sono ordinati, il modello usa un “passato” sbagliato.

Nel mio caso ogni serie è definita dalla coppia:

- negozio
- famiglia prodotto

Quindi devo rispettare l’ordine temporale dentro ogni serie.

### 3. Selezione di un subset temporale coerente

Non ho fatto campionamento casuale.  
Ho preso gli **ultimi 365 giorni** del dataset.

**Perché:**  
Il sample casuale rompe la continuità temporale.  
Se tolgo righe a caso:

- `lag_1` non rappresenta più il valore precedente reale
- `lag_7` non rappresenta più una dipendenza temporale corretta

Con il subset temporale:

- mantengo continuità
- velocizzo gli esperimenti
- lavoro comunque su dati realistici

Il nuovo intervallo temporale va da `2016-08-15` a `2017-08-15`.

### 4. Creazione delle feature temporali

Ho creato queste feature:

- `year`
- `month`
- `day`
- `dayofweek`
- `weekofyear`

**Perché:**  
Servono a dare al modello informazione sul calendario.  
Le vendite non dipendono solo dal passato immediato, ma anche da pattern temporali come:

- giorno della settimana
- mese
- settimana dell’anno

Queste feature aiutano a modellare una prima forma di seasonality.

### 5. Creazione delle lag features

Ho creato:

- `lag_1`
- `lag_7`

Le ho calcolate separatamente per ogni serie `store_nbr, family`.

**Perché:**  
Le lag features servono a catturare la dipendenza seriale.

- `lag_1` = valore osservato nello step precedente
- `lag_7` = valore osservato 7 step prima

Questo permette al modello di usare il passato della serie per prevedere il presente.

Adesso hanno senso perché i dati sono ordinati e continui.

### 6. Pulizia dei valori mancanti

Ho eliminato le righe con `NaN` nelle lag features.

**Perché:**  
All’inizio di ogni serie non esiste un valore precedente sufficiente per costruire `lag_1` e `lag_7`.  
Questi NaN sono normali e devono essere rimossi prima del training.

Dopo la pulizia il dataset rimane con circa `637,956` righe.

### 7. Encoding della variabile categorica

Ho convertito `family` in codici numerici.

**Perché:**  
LightGBM lavora con input numerici.  
La famiglia prodotto è una variabile categorica e va codificata per poter essere usata come feature.

Le famiglie codificate sono 33.

### 8. Selezione delle feature finali

Ho usato queste feature:

- `store_nbr`
- `family`
- `onpromotion`
- `year`
- `month`
- `day`
- `dayofweek`
- `weekofyear`
- `lag_1`
- `lag_7`

**Perché:**  
Questo è un set baseline semplice ma sensato:

- informazioni del negozio
- informazione della famiglia prodotto
- promozioni
- calendario
- dipendenza dal passato

Serve come punto di partenza prima di passare a feature più avanzate.

### 9. Split temporale train/validation

Ho diviso i dati in modo cronologico, non casuale.

- train: fino al `2017-06-04`
- validation: dal `2017-06-05` al `2017-08-15`

**Perché:**  
Nel forecasting non si può usare random split.  
Bisogna allenare sui dati passati e validare su dati futuri, altrimenti si crea leakage.

Questo rende la validazione più realistica.

### 10. Addestramento del modello

Ho usato `LGBMRegressor`.

**Perché:**  
LightGBM è molto adatto a dati tabellari:

- è veloce
- gestisce bene molte righe
- è una baseline forte per forecasting tabellare con feature engineering

Quindi è una buona scelta come primo modello.

### 11. Predizioni e clipping

Ho generato le predizioni sul validation set e poi ho fatto clipping a zero.

**Perché:**  
Le vendite non possono essere negative.  
Se il modello produce valori sotto zero, vanno riportati a zero prima della valutazione.

### 12. Valutazione

Ho usato come metrica principale **RMSLE**.

Risultato:

- `Validation RMSLE = 0.7598` circa

**Perché RMSLE:**  
È la metrica della competition Kaggle ed è adatta quando:

- le vendite hanno scale molto diverse
- conta l’errore relativo più che assoluto

Questa baseline è tecnicamente corretta e più affidabile della versione precedente.

---