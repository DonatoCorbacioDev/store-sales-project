# NB9 — AutoGluon Tabular Benchmark

## Obiettivo

Valutare AutoGluon Tabular come benchmark AutoML sulla pipeline di forecasting già validata.

Obiettivi principali:

- valutare AutoGluon su una pipeline già stabile
- identificare quali modelli AutoGluon seleziona internamente
- confrontare performance, stabilità e costo rispetto alla baseline validata
- misurare il valore pratico di un approccio AutoML
- analizzare i trade-off tra performance e semplicità di produzione

---

## Contesto

Nei notebook precedenti è stata costruita e validata una pipeline manuale di forecasting basata su:

- feature engineering avanzato
- LightGBM
- walk-forward cross-validation
- tracking con MLflow

NB9 introduce un benchmark AutoML con AutoGluon Tabular.

Questo notebook non sostituisce la pipeline manuale.  
Serve a valutare in modo strutturato quanto un approccio AutoML possa migliorare il risultato finale.

---

## Pipeline

La pipeline è stata mantenuta coerente con i notebook precedenti:

- stesso dataset
- stessa logica di preprocessing
- stessa feature engineering validata
- stessa validazione walk-forward
- stesso tracking MLflow

Differenza principale:

- il training non è gestito manualmente
- la selezione del modello è delegata ad AutoGluon

---

## Strategia di benchmark

L’obiettivo non è costruire una nuova pipeline, ma confrontare un approccio AutoML sulla stessa base tecnica già validata.

Per garantire un confronto corretto:

- non sono state introdotte nuove feature
- non è stato modificato il dataset
- non è stata cambiata la logica di validazione

AutoGluon è stato valutato come benchmark puro.

---

## Setup sperimentale

Il benchmark è stato eseguito con:

- full training history
- 2 fold walk-forward recenti
- finestra di validazione di 28 giorni
- AutoGluon Tabular
- preset `medium_quality`
- budget di 600 secondi per fold

Questo setup consente un benchmark realistico ma ancora sostenibile a livello computazionale.

---

## Modelli valutati da AutoGluon

AutoGluon ha testato automaticamente diversi modelli tabulari.

Nel benchmark eseguito, i modelli effettivamente utilizzati sono stati principalmente:

- LightGBM
- LightGBMXT
- WeightedEnsemble_L2

Il modello migliore in entrambi i fold è risultato:

- **WeightedEnsemble_L2**

L’ensemble combina automaticamente modelli gradient boosting già forti, migliorando il risultato finale.

---

## Risultati

AutoGluon ha ottenuto performance migliori rispetto alla baseline manuale validata.

### Metriche medie

**AutoGluon Tabular**
- RMSLE ≈ 0.4761
- MAE ≈ 55.54
- RMSE ≈ 201.04
- R² ≈ 0.9760

**NB5 Full Data LightGBM**
- RMSLE ≈ 0.5999
- MAE ≈ 68.45
- RMSE ≈ 248.71
- R² ≈ 0.9651

AutoGluon migliora in modo consistente tutte le metriche principali.

---

## Key Findings

### Performance

AutoGluon ha superato la baseline manuale su tutti i principali indicatori.

Il miglioramento è stato stabile su entrambi i fold.

---

### Modello migliore

AutoGluon non ha trovato una famiglia di modelli radicalmente diversa.

Il miglior risultato è arrivato da un ensemble di modelli LightGBM-based.

Questo indica che il vantaggio principale non è il cambio di algoritmo, ma una combinazione più efficiente di modelli già forti.

---

### Stabilità

Il comportamento del benchmark è stato molto stabile:

- stesso miglior modello su entrambi i fold
- metriche molto consistenti
- deviazione molto bassa tra fold

Questo suggerisce una buona robustezza temporale.

---

### Costo computazionale

Il miglioramento ha un costo.

AutoGluon richiede:

- ~10 minuti di training per fold
- maggiore costo computazionale
- maggiore complessità operativa

Il miglioramento non è “gratis”.

---

### Interpretabilità

Il vantaggio prestazionale riduce però il controllo diretto sul training.

Rispetto alla pipeline manuale:

- minore trasparenza
- minore controllo sui modelli
- minore semplicità di debug
- maggiore complessità in produzione

---

## Interpretazione pratica

AutoGluon si è dimostrato un benchmark AutoML molto forte per questo problema.

Il suo valore principale non è sostituire completamente la pipeline manuale, ma:

- validare rapidamente alternative
- costruire benchmark robusti
- esplorare ensemble più forti
- accelerare la fase di model exploration

---

## Trade-off

| Aspetto | Manual LightGBM | AutoGluon |
|---|---|---|
| Performance | Buona | Migliore |
| Training Cost | Più basso | Più alto |
| Interpretabilità | Più alta | Più bassa |
| Controllo | Più alto | Più basso |
| Produzione | Più semplice | Più complessa |

---

## Conclusione

NB9 ha validato AutoGluon come benchmark AutoML sulla pipeline di forecasting.

Risultati principali:

- performance migliori
- benchmark stabile
- ensemble più forte della baseline manuale

Tuttavia:

- il costo computazionale è maggiore
- la pipeline è meno interpretabile
- la produzione è meno semplice

AutoGluon è quindi molto utile come strumento di benchmark e model exploration.

La pipeline manuale resta preferibile quando controllo, interpretabilità e semplicità di produzione sono priorità più importanti.

---

## Step successivo

Possibili sviluppi:

- tuning mirato del miglior ensemble
- benchmark con TimeSeriesPredictor
- confronto costi/benefici in produzione
- selezione finale tra benchmark e deployment candidate