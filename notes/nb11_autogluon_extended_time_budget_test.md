# NB11 — AutoGluon Extended Time Budget Test

## Obiettivo

Valutare se aumentare il budget di training di AutoGluon produce un miglioramento sufficiente da giustificare il costo computazionale aggiuntivo.

NB9 aveva utilizzato AutoGluon Tabular con:

* 2 fold walk-forward
* 600 secondi per fold
* feature set `advanced_v1`
* full training history

NB11 mantiene la stessa pipeline validata, ma aumenta il budget AutoML da **600s** a **3600s** sul fold più recente.

L’obiettivo non è cambiare modello o pipeline.
L’obiettivo è rispondere a una domanda pratica:

> una ricerca AutoML più lunga produce un miglioramento abbastanza utile da giustificare il costo?

NB11 è un esperimento di **cost-benefit evaluation**.

---

## Contesto

NB9 aveva mostrato che AutoGluon migliora la pipeline manuale LightGBM.

Tuttavia, il benchmark di NB9 usava un budget AutoML relativamente contenuto (600 secondi per fold).

NB11 nasce per capire se:

* AutoGluon migliora ancora con più tempo
* il miglioramento è sostanziale o marginale
* il costo aggiuntivo è giustificato
* il paradigma del modello cambia o resta lo stesso

NB11 non cambia il setup sperimentale.
Cambia solo una variabile:

* `time_limit`: da **600s** a **3600s**

Questo rende NB11 un test controllato del valore marginale del compute.

---

## Pipeline

NB11 mantiene invariata la pipeline validata di NB9:

* stesso dataset full history
* stesso feature set `advanced_v1`
* stessa logica walk-forward
* stesso fold di validazione recente
* stesso setup AutoGluon Tabular

L’unica differenza è:

* budget AutoML esteso a 3600 secondi

Questo permette di isolare una sola variabile:

> il valore di una ricerca AutoML più profonda

---

## Strategia

NB11 non è un nuovo benchmark completo.

È un **esperimento controllato di costo vs beneficio**.

Per evitare rumore sperimentale:

* non vengono introdotte nuove feature
* non cambia il validation design
* non viene cambiato il modello target
* non vengono modificati i preset

Questo permette di attribuire ogni differenza osservata al solo aumento del budget computazionale.

---

## Risultati principali

Confronto diretto sullo stesso fold di validazione:

| Experiment           |  RMSLE |   MAE |   RMSE |     R² | Train Time |
| -------------------- | -----: | ----: | -----: | -----: | ---------: |
| NB9 AutoGluon 600s   | 0.4757 | 58.00 | 198.50 | 0.9756 |       601s |
| NB11 AutoGluon 3600s | 0.5915 | 55.78 | 191.54 | 0.9773 |      3605s |

Risultato chiave:

* **MAE migliora**
* **RMSE migliora**
* **R² migliora leggermente**
* **RMSLE peggiora**
* **training cost ~6x**

NB11 non produce un miglioramento uniforme.
Produce un trade-off.

---

## Key Findings

### Più compute non cambia il paradigma

Anche con più budget, il miglior modello resta:

* `WeightedEnsemble_L2`

Questo conferma che il paradigma non cambia.

AutoGluon non scopre una nuova famiglia di modelli.
Continua a vincere un ensemble tree-based.

Il miglioramento non arriva da un nuovo paradigma, ma da una ricerca più profonda nello stesso spazio.

---

### Migliora l’errore assoluto, peggiora la calibrazione relativa

NB11 migliora:

* MAE
* RMSE
* R²

Quindi migliora la qualità delle previsioni in termini assoluti.

Tuttavia peggiora RMSLE.

Questo significa:

> il modello migliora sui volumi grandi, ma perde calibrazione relativa sui volumi piccoli.

Questa è una differenza importante.

NB11 non è “meglio” in senso assoluto.
È migliore in un contesto specifico.

---

### Il costo cresce molto più del guadagno

Il training passa da:

* ~600s
  a
* ~3600s

Quindi il costo aumenta di circa **6x**.

Il miglioramento ottenuto esiste, ma è marginale rispetto al costo.

Questo rende NB11 utile come upper-bound benchmark,
ma non automaticamente giustificato come default operativo.

---

### Il committee migliora, non il paradigma

Con 600s, NB9 era dominato da:

* LightGBMXT
* LightGBM

Con 3600s, NB11 introduce:

* CatBoost
* XGBoost

e costruisce un ensemble più ricco.

Pesi osservati:

* CatBoost: 0.50
* LightGBM: 0.25
* LightGBMXT: 0.125
* XGBoost: 0.125

Il miglioramento di NB11 deriva da:

* ensemble diversification
* maggiore profondità di search
* combinazione più ricca di booster tree-based

Non da una nuova architettura.

---

## Production Reasoning

NB11 non sostituisce automaticamente NB9.

I due modelli rispondono a esigenze diverse.

### NB9 — Best Default

Vantaggi:

* più veloce
* più economico
* più stabile
* miglior cost/performance
* migliore configurazione di default

### NB11 — Best Upper-Bound Candidate

Vantaggi:

* migliore errore assoluto
* migliore RMSE
* migliore R²
* ensemble più ricco
* più adatto a scenari high-volume

Svantaggi:

* ~6x training cost
* inferenza più costosa
* peggiore RMSLE
* maggiore complessità

---

## Trade-off

| Aspetto               | NB9 (600s)   | NB11 (3600s) |
| --------------------- | ------------ | ------------ |
| Training Cost         | Basso        | Alto         |
| MAE                   | Alto         | Più basso    |
| RMSE                  | Alto         | Più basso    |
| RMSLE                 | Migliore     | Peggiore     |
| Inference Cost        | Più basso    | Più alto     |
| Ensemble Complexity   | Più semplice | Più ricco    |
| Default Usage         | Sì           | No           |
| Upper Bound Benchmark | No           | Sì           |

---

## Conclusione

NB11 mostra che aumentare il budget AutoML non cambia il paradigma del modello,
ma migliora la qualità dell’ensemble.

Il guadagno osservato non è gratuito:

* migliora l’errore assoluto
* peggiora la calibrazione relativa
* aumenta molto il costo computazionale

Conclusione pratica:

* **NB9** resta il miglior default cost/performance
* **NB11** è il miglior upper-bound benchmark
* NB11 è utile per capire il valore marginale del compute
* NB11 non è il nuovo default, ma il limite superiore del benchmark

Questo è il punto chiave di NB11:

più compute aiuta, ma non abbastanza da giustificare automaticamente il costo.
