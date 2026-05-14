# NB4 — Experiment Tracking con MLflow

## Obiettivo

Introdurre un sistema di tracking degli esperimenti per rendere il workflow di Machine Learning più strutturato, riproducibile e facilmente confrontabile.

L’obiettivo è passare da una sperimentazione manuale a un processo più simile a quello utilizzato in contesti aziendali.

## Perché MLflow

Durante NB1–NB3:

- i modelli venivano confrontati manualmente
- mancava uno storico degli esperimenti
- era difficile tracciare feature, parametri e risultati
- non era possibile riprodurre facilmente i risultati

MLflow risolve questi problemi permettendo:

- tracciamento automatico degli esperimenti
- confronto strutturato tra modelli
- gestione centralizzata di parametri e metriche
- maggiore riproducibilità del workflow

## Pipeline

### 1. Standardizzazione del validation setup

È stato definito un **fixed temporal split** comune a tutti gli esperimenti:

- train → fino a **2017-06-04**
- validation → **2017-06-05 → 2017-08-15**

**Perché:**

Per garantire un confronto corretto tra modelli, è fondamentale che tutti gli esperimenti vengano valutati sulla stessa finestra temporale.

### 2. Logging degli esperimenti

Per ogni run MLflow vengono registrati:

- parametri del modello
- metriche:
  - RMSLE (metrica principale)
  - MAE, RMSE, R²
- segment metrics:
  - errore su weekday
  - errore su weekend
- feature list utilizzata
- modello addestrato
- feature importance
- prediction sulla validation

**Perché:**

Questo permette di analizzare non solo la performance globale, ma anche il comportamento del modello su segmenti specifici.

### 3. Run context

Per ogni esperimento viene salvato anche il contesto:

- intervalli temporali di train e validation
- numero di osservazioni
- numero di feature utilizzate

**Perché:**

In questo modo ogni run è completamente tracciabile e riproducibile.

### 4. Confronto baseline vs advanced

Sono stati tracciati due esperimenti principali:

- **Baseline (NB1)**  
  modello con lag features (`lag_1`, `lag_7`)

- **Advanced (NB3)**  
  modello con feature avanzate:
  - rolling statistics
  - trend
  - promozioni
  - weekend indicator

## Risultati

- Baseline RMSLE ≈ **0.78**
- Advanced RMSLE ≈ **0.68**

**Miglioramento:** ≈ **-0.10 RMSLE**

## Interpretazione dei risultati

Il miglioramento è principalmente dovuto a:

- introduzione di feature temporali più informative
- migliore modellazione del contesto recente (rolling features)
- capacità di catturare trend e variazioni della serie
- gestione più efficace del comportamento nel weekend
- integrazione dell’effetto delle promozioni

## Nota importante: Training range

La finestra di validazione è fissa e identica per tutti gli esperimenti.

Tuttavia, l’intervallo di training differisce tra baseline e modello avanzato.

Questo è dovuto al fatto che le feature avanzate (rolling e promozioni) richiedono uno storico maggiore, eliminando più osservazioni iniziali.

Di conseguenza:

- il modello baseline utilizza più dati di training
- il modello avanzato parte da una data successiva

Questo comportamento è atteso e non compromette il confronto, poiché la valutazione avviene sulla stessa validation window.

## Conclusione

L’introduzione di MLflow ha trasformato il workflow:

- da sperimentazione manuale
- a processo strutturato, tracciabile e riproducibile

Questo rappresenta un passo importante verso un approccio più professionale al Machine Learning.

## Prossimi step

- refactor del codice in una struttura `src/`
- separazione tra:
  - feature engineering
  - training
  - evaluation
- costruzione di una pipeline modulare e riutilizzabile
- eventuale tuning controllato degli iperparametri