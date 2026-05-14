
# NB3 — Advanced Feature Engineering della baseline LightGBM

## Obiettivo

Migliorare la baseline costruita in NB1 introducendo feature avanzate basate sull’analisi degli errori effettuata in NB2.

Obiettivi principali:

- catturare meglio i pattern temporali
- modellare trend e variabilità delle serie
- incorporare l’effetto delle promozioni nel tempo
- ridurre gli errori sistematici (weekend e picchi di vendita)

## Pipeline del notebook

### 1. Ricostruzione della pipeline baseline

Ho mantenuto la stessa pipeline corretta utilizzata in NB1 e NB2:

- ordinamento per `store_nbr`, `family`, `date`
- subset temporale (ultimi 365 giorni)
- feature temporali base
- lag features (`lag_1`, `lag_7`)
- encoding della variabile `family`
- split temporale train/validation

**Perché:**  
Per confrontare correttamente le performance, la pipeline deve rimanere coerente.  
Le uniche modifiche introdotte riguardano il feature engineering.

### 2. Feature temporali aggiuntive

Ho aggiunto:

- `is_weekend`

**Perché:**  
In NB2 è emerso che il modello performa peggio nel weekend.  
Questa feature permette al modello di distinguere esplicitamente tra giorni lavorativi e weekend.

### 3. Rolling features

Ho introdotto:

- `rolling_mean_7`
- `rolling_std_7`
- `rolling_mean_14`

**Perché:**  

Queste feature catturano il comportamento recente della serie:

- `rolling_mean_7` → media degli ultimi 7 giorni
- `rolling_std_7` → variabilità della serie
- `rolling_mean_14` → trend su un orizzonte più lungo

In NB2 il modello mostrava difficoltà nel gestire variazioni e instabilità:  
le rolling features aiutano a fornire un contesto temporale più ricco.

### 4. Trend feature

Ho introdotto:

- `trend_1_7 = lag_1 - lag_7`

**Perché:**  

Questa feature misura la direzione della serie:

- valore positivo → crescita
- valore negativo → calo

In NB2 il modello tendeva a “smussare” i picchi e non catturare bene i cambiamenti rapidi.  
Il trend aiuta a modellare meglio queste dinamiche.

### 5. Feature sulle promozioni

Ho introdotto:

- `promo_last_7`

**Perché:**  

Le promozioni non hanno effetto solo nel giorno corrente.  
Questa feature rappresenta il numero di promozioni negli ultimi 7 giorni.

Serve a modellare effetti cumulativi e ritardati delle promozioni sulle vendite.

### 6. Pulizia dei dati

Ho rimosso le righe con valori mancanti generati da:

- lag features
- rolling features

Dopo la pulizia il dataset contiene circa 625.000 righe.

**Perché:**  
Le feature temporali richiedono uno storico minimo.  
Le prime osservazioni di ogni serie non possono essere utilizzate.

### 7. Selezione delle feature

Ho utilizzato il seguente set finale:

- feature baseline (store, family, calendario, lag)
- feature avanzate (rolling, trend, promo, weekend)

Totale feature: 16

**Perché:**  
Combinare informazioni statiche, temporali e dinamiche migliora la capacità predittiva del modello.

### 8. Addestramento del modello

Ho utilizzato:

- `LGBMRegressor`
- aumento del numero di alberi (`n_estimators = 300`)

**Perché:**  
Con più feature, il modello ha bisogno di maggiore capacità per apprendere pattern più complessi.

### 9. Valutazione

Metrica utilizzata:

- RMSLE

Risultato:

- NB3 RMSLE ≈ 0.68

## Confronto con la baseline

- NB1 RMSLE ≈ 0.75  
- NB3 RMSLE ≈ 0.68  

**Miglioramento significativo.**

## Interpretazione dei risultati

L’introduzione delle feature avanzate ha permesso di:

- migliorare la gestione del weekend
- catturare meglio la variabilità delle vendite
- ridurre gli errori sui picchi
- modellare meglio l’effetto delle promozioni

## Feature importance

L’analisi dell’importanza delle feature mostra che:

- `lag_1` e `lag_7` restano fondamentali
- le rolling features contribuiscono significativamente
- il trend e le promozioni aggiungono informazione utile

Questo conferma che le nuove feature non sono ridondanti ma migliorano il modello.

## Conclusione

Questo notebook ha permesso di:

- migliorare significativamente la baseline
- integrare feature temporali avanzate
- ridurre gli errori sistematici osservati in NB2

Il modello è ora più robusto e più adatto a catturare dinamiche reali delle vendite.

## Prossimi step

- integrazione di MLflow per il tracking degli esperimenti
- esplorazione di strategie di forecasting multi-step
- eventuale tuning degli iperparametri
