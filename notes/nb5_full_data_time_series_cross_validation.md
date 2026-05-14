# NB5 — Full Data Time Series Cross Validation

## Obiettivo

Estendere la validazione del modello introducendo una **walk-forward cross-validation su tutto il dataset storico**.

Obiettivi principali:

- ottenere una stima più robusta e realistica delle performance
- valutare la stabilità temporale del modello su periodi diversi
- ridurre la dipendenza da un subset limitato (ultimi 365 giorni)

---

## Pipeline

È stata mantenuta invariata la pipeline già validata in NB3/NB4:

- feature engineering avanzato (lag, rolling, trend, promozioni)
- modello LightGBM
- nessuna modifica ai parametri

Differenza principale:

- utilizzo dell'intero dataset storico (2013 → 2017)
- validazione su finestre temporali recenti

---

## Strategia di validazione

È stata utilizzata una **walk-forward time series cross-validation ancorata alla parte finale del dataset**:

- il training utilizza tutto il passato disponibile
- la validation copre finestre temporali successive
- i fold sono posizionati su periodi recenti (2017), più vicini al contesto reale

Configurazione:

- Numero fold: 4  
- Validation window: 28 giorni  
- Strategia: expanding window + validation recente

---

## Risultati

RMSLE per fold:

- Fold 1 → ~0.600  
- Fold 2 → ~0.615  
- Fold 3 → ~0.579  
- Fold 4 → ~0.606  

Media RMSLE:

- ≈ 0.600  

Deviazione standard:

- ≈ 0.015  

---

## Confronto con NB5 (subset 365 giorni)

NB5 subset:

- RMSLE mean ≈ 0.687  
- RMSLE std ≈ 0.035  

NB5 full data:

- RMSLE mean ≈ 0.600  
- RMSLE std ≈ 0.015  

---

## Interpretazione

- Il modello mostra una **migliore performance media** su full dataset
- La **deviazione standard è significativamente più bassa**, indicando maggiore stabilità temporale
- I risultati sono più consistenti tra i diversi fold
- L’utilizzo di uno storico più ampio consente al modello di catturare pattern più robusti

Nota importante:

Il miglioramento osservato è dovuto principalmente a:

- una validazione più robusta
- un training su un dataset più ampio

Non sono state introdotte modifiche al modello o alla pipeline.

---

## Conclusione

La validazione su full dataset rappresenta il riferimento principale per il progetto.

Risultati:

- performance più stabile nel tempo
- minore variabilità tra i fold
- maggiore affidabilità della stima

Questo notebook diventa quindi:

**la validazione ufficiale del modello**

---

## Prossimo step

- retraining finale su tutto il dataset (NB6)
- registrazione del modello nel Model Registry