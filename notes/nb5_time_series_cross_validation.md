# NB5 — Time Series Cross Validation

## Obiettivo

Introdurre una validazione più robusta rispetto al singolo split temporale utilizzato in NB4.

Obiettivi:

- valutare la stabilità del modello nel tempo
- ottenere una stima più realistica delle performance
- ridurre la dipendenza da un singolo periodo di validazione

---

## Pipeline

Ho mantenuto la stessa pipeline di NB3/NB4:

- subset temporale (ultimi 365 giorni)
- feature engineering avanzato
- modello LightGBM

L’unica modifica riguarda la strategia di validazione.

---

## Strategia di validazione

È stata utilizzata una **walk-forward time series cross-validation**:

- il training cresce progressivamente
- la validation si sposta in avanti nel tempo
- ogni fold rappresenta un periodo diverso

Numero fold: 3  
Validation window: 28 giorni

---

## Risultati

RMSLE per fold:

- Fold 1 → ~0.67  
- Fold 2 → ~0.73  
- Fold 3 → ~0.66  

Media RMSLE:

- ≈ 0.687  

Deviazione standard:

- ≈ 0.035  

---

## Confronto con NB4

NB4 (single split):

- RMSLE ≈ 0.68  

NB5 (cross-validation):

- RMSLE mean ≈ 0.687  
- maggiore variabilità

---

## Interpretazione

- Il modello mostra variabilità nel tempo
- Fold 2 presenta errori più elevati → possibile instabilità temporale
- Il risultato NB4 è leggermente ottimistico

La cross-validation fornisce una stima più realistica della performance.

---

## Conclusione

L’introduzione della time series cross-validation ha permesso di:

- valutare il modello su più scenari temporali
- ottenere una misura più robusta della performance
- migliorare la qualità della validazione

Questo rende la pipeline più vicina a un contesto reale di forecasting.