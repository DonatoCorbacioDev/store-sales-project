# NB2 — Metrics and Error Analysis della baseline LightGBM

## Obiettivo

Analizzare in modo approfondito la baseline costruita in NB1 utilizzando una pipeline temporale corretta.

Obiettivi principali:

- valutare il modello con più metriche di regressione
- analizzare gli errori di predizione
- individuare pattern sistematici di errore
- guidare il feature engineering del prossimo notebook

## Pipeline del notebook

### 1. Ricostruzione della baseline

Ho ricostruito esattamente la pipeline di NB1:

- ordinamento per `store_nbr`, `family`, `date`
- subset temporale (ultimi 365 giorni)
- feature temporali
- lag features (`lag_1`, `lag_7`)
- encoding della variabile `family`
- split temporale train/validation

**Perché:**  
L’analisi degli errori ha senso solo se fatta su una pipeline corretta.

### 2. Addestramento del modello

Ho riutilizzato il modello baseline:

- `LGBMRegressor`
- stessi iperparametri

**Perché:**  
Non voglio migliorare il modello qui, ma capire dove sbaglia.

### 3. Metriche globali

Ho calcolato:

- RMSLE (metrica principale)
- MAE
- RMSE
- R²

Risultati:

- RMSLE ≈ 0.78
- MAE ≈ 67
- RMSE ≈ 240
- R² ≈ 0.96

**Perché:**

- RMSLE → errore relativo (Kaggle metric)
- MAE → errore medio interpretabile
- RMSE → penalizza errori grandi
- R² → qualità globale del fit

### 4. Creazione del dataset di analisi errori

Ho costruito una tabella `results` contenente:

- valori reali (`sales`)
- predizioni (`y_pred`)
- errore (`error`)
- errore assoluto (`abs_error`)
- errore quadratico
- variabili utili (store, family, dayofweek, ecc.)

Ho aggiunto:

- `is_weekend` (1 se sabato/domenica)

**Perché:**  
Serve una struttura unica per analizzare facilmente gli errori.

### 5. Analisi globale degli errori

Ho analizzato:

- scatter plot: True vs Predicted
- distribuzione degli errori (residui)

**Insight:**

- il modello segue bene il trend generale
- tende a sbagliare sui valori molto alti (outlier)

### 6. Errori per giorno della settimana

Ho raggruppato per `dayofweek`.

**Risultato:**

- errori più alti nel weekend
- errore massimo su domenica

Come si vede anche nel grafico (pagina 10), il MAE cresce molto nei giorni 5 e 6.

**Interpretazione:**

Il modello non cattura bene i pattern specifici del weekend.

### 7. Weekend vs Weekday

Ho confrontato:

- giorni lavorativi
- weekend

Risultato:

- Weekday MAE ≈ 59.8
- Weekend MAE ≈ 87.0 :contentReference[oaicite:1]{index=1}

**Insight:**

Il modello sottostima sistematicamente il weekend (errore medio negativo).

### 8. Errori per mese

Ho analizzato errori aggregati per `month`.

**Risultato:**

- variazione dell’errore tra mesi
- agosto presenta errori più alti

**Interpretazione:**

Possibili effetti stagionali non catturati dal modello.

### 9. Errori per store

Ho identificato i negozi più difficili.

Esempi:

- store 44, 47, 45, 46 → MAE più alto :contentReference[oaicite:2]{index=2}

**Interpretazione:**

Il comportamento dei negozi è eterogeneo e non completamente modellato.

### 10. Errori per famiglia prodotto

Ho analizzato le `family`.

Famiglie più difficili:

- GROCERY I
- BEVERAGES
- CLEANING

**Insight:**

Le famiglie ad alto volume hanno errori molto più grandi.

### 11. Worst predictions

Ho isolato i peggiori errori.

**Osservazioni:**

- errori molto alti su vendite elevate
- forte sottostima su picchi di domanda
- spesso associati a:
  - weekend
  - promozioni
  - family ad alto volume

### 12. Trend temporale degli errori

Ho analizzato l’errore medio per giorno.

**Insight:**

- presenza di spike di errore in alcune date
- instabilità del modello su certi periodi

## Key findings

Principali risultati:

- il modello performa peggio nel weekend
- alcuni store hanno errori sistematici più alti
- alcune famiglie sono più difficili da predire
- il modello tende a “smussare” i picchi elevati
- la baseline non cattura completamente la stagionalità

## Conclusione

Questo notebook ha permesso di:

- validare la baseline su pipeline corretta
- identificare pattern chiari di errore
- individuare limiti strutturali del modello

Questi risultati guidano il prossimo step (NB3), dove verranno introdotte feature avanzate per modellare meglio:

- il comportamento del weekend
- la variabilità delle vendite
- i picchi di domanda
- l’effetto cumulativo delle promozioni

---