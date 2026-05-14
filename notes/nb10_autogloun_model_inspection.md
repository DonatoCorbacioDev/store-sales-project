# NB10 — AutoGluon Model Inspection & Hyperparameter Reasoning

## Obiettivo

Ispezionare i predictor AutoGluon addestrati in NB9 per capire cosa AutoGluon ha realmente fatto durante il training.

Obiettivi principali:

- identificare quali modelli AutoGluon ha effettivamente addestrato
- leggere gli hyperparameter reali usati da ciascun modello
- confrontare LightGBM e LightGBMXT
- analizzare la struttura del WeightedEnsemble_L2
- capire se il miglior modello in leaderboard è davvero il miglior candidato per la produzione

NB10 non esegue nuovo training.  
NB10 è un notebook di inspection, interpretability e production reasoning.

---

## Contesto

NB9 ha mostrato che AutoGluon Tabular migliora la baseline manuale LightGBM.

Risultati di riferimento:

| Model | RMSLE | MAE | RMSE | R² |
|---|---:|---:|---:|---:|
| Manual LightGBM NB5 | 0.5999 | 68.45 | 248.71 | 0.9651 |
| AutoGluon NB9 | 0.4761 | 55.54 | 201.04 | 0.9760 |

Tuttavia, la leaderboard da sola non è sufficiente.

NB9 mostra quale modello vince.  
NB10 serve a capire perché vince.

---

## Pipeline

NB10 non addestra nuovi modelli.

La pipeline del notebook è:

- caricare i predictor AutoGluon salvati in NB9
- ispezionare leaderboard e fit summary
- leggere hyperparameter reali
- ispezionare `model_info()`
- analizzare la struttura dell’ensemble
- confrontare best ensemble vs best single model
- valutare il trade-off per la produzione

L’obiettivo non è migliorare il benchmark, ma spiegare il benchmark.

---

## Strategia di inspection

La leaderboard è utile per ordinare i modelli, ma non è sufficiente per capire il comportamento reale di AutoGluon.

Per questo NB10 utilizza introspezione diretta del predictor tramite:

- `predictor.leaderboard()`
- `predictor.fit_summary()`
- `predictor.info()`
- `predictor.model_hyperparameters()`
- `predictor.model_info()`

Questo approccio permette di passare da un benchmark “black box” a un’analisi tecnica del comportamento del modello.

---

## Modelli realmente addestrati

AutoGluon non ha addestrato un gran numero di modelli eterogenei.

Nei due fold analizzati, i modelli effettivamente addestrati sono stati:

- LightGBM
- LightGBMXT
- WeightedEnsemble_L2

Questo è un punto importante:

AutoGluon non ha trovato una famiglia di modelli radicalmente diversa.

Il miglioramento osservato in NB9 deriva principalmente da:

- varianti LightGBM-based
- combinazione pesata di modelli gradient boosting
- ensemble stacking

---

## Hyperparameter Inspection

NB10 mostra gli hyperparameter reali usati da AutoGluon.

### LightGBM

Hyperparameter principali:

- `learning_rate = 0.05`
- `seed = 0`

LightGBM è la configurazione standard di gradient boosting usata da AutoGluon.

---

### LightGBMXT

Hyperparameter principali:

- `learning_rate = 0.05`
- `extra_trees = True`
- `seed = 0`

La differenza chiave rispetto a LightGBM è:

- `extra_trees=True`

Questo rende LightGBMXT una variante più aggressiva e più costosa del boosting standard.

---

### WeightedEnsemble_L2

Hyperparameter principali:

- `ensemble_size = 25`
- `subsample_size = 1000000`

Questo modello non apprende direttamente sulle feature originali.

Apprende invece sulle predizioni dei modelli base.

In pratica:

- input = predizioni di LightGBM e LightGBMXT
- output = combinazione pesata finale

---

## Key Findings

### Il miglioramento non viene da un nuovo paradigma

AutoGluon non ha scoperto un modello radicalmente diverso.

Il miglioramento di NB9 non deriva da una nuova architettura, ma da:

- configurazione più efficiente
- varianti LightGBM
- ensemble pesato

Questo significa che il guadagno principale viene dalla combinazione, non dal cambio di paradigma.

---

### LightGBMXT è più costoso

LightGBMXT è una variante più pesante di LightGBM.

Nei fold analizzati:

- richiede molto più tempo di training
- ha costo di inferenza più alto
- migliora solo in alcuni casi specifici

Questo lo rende interessante come modello di supporto, ma meno attraente come singolo candidato produzione.

---

### WeightedEnsemble_L2 è il miglior benchmark model

Il miglior modello in leaderboard è:

- **WeightedEnsemble_L2**

Questo modello ottiene il miglior risultato complessivo perché combina i modelli base.

Tuttavia, non è automaticamente il miglior modello da mettere in produzione.

---

### Best benchmark model ≠ best production model

Questo è il punto più importante di NB10.

Il miglior modello in validation non è automaticamente il miglior modello per il deploy.

Per la produzione bisogna considerare anche:

- latenza
- costo di inferenza
- semplicità di deploy
- facilità di debug
- monitoraggio
- manutenzione

Questa è la differenza tra benchmark optimization e production reasoning.

---

## Weighted Ensemble Inspection

NB10 mostra che `WeightedEnsemble_L2` non è un modello standalone.

È un meta-model che combina:

- LightGBM
- LightGBMXT

Pesi osservati:

### Fold 1
- LightGBM: 0.68
- LightGBMXT: 0.32

### Fold 2
- LightGBMXT: 0.92
- LightGBM: 0.08

Questo mostra che AutoGluon non applica un ensemble statico.

Adatta i pesi in base al fold e alla finestra temporale.

Questo è il vero motivo del miglioramento.

---

## Production Reasoning

NB10 introduce un ragionamento orientato alla produzione.

### Option A — Best Accuracy

Usare:

- `WeightedEnsemble_L2`

Vantaggi:

- miglior score
- modello più forte in validation
- miglior benchmark complessivo

Svantaggi:

- più complesso da deployare
- più costoso in inferenza
- meno interpretabile
- più difficile da debuggare

---

### Option B — Best Production Candidate

Usare:

- miglior singolo modello LightGBM-based

Vantaggi:

- più semplice da deployare
- più veloce in serving
- più facile da monitorare
- più facile da mantenere

Svantaggi:

- leggera perdita di performance rispetto all’ensemble

---

## Trade-off

| Aspetto | Best Single LightGBM | WeightedEnsemble_L2 |
|---|---|---|
| Accuracy | Alta | Massima |
| Inference Cost | Basso | Più alto |
| Interpretabilità | Più alta | Più bassa |
| Debug | Più semplice | Più complesso |
| Deploy | Più semplice | Più complesso |
| Produzione | Più robusta | Più costosa |

---

## Conclusione

NB10 mostra che AutoGluon non deve essere trattato come una black box.

NB9 ha mostrato che AutoGluon migliora la baseline.

NB10 spiega perché:

- il miglioramento deriva da modelli LightGBM-based
- LightGBMXT introduce una variante più aggressiva
- il vero vantaggio viene dall’ensemble
- il best leaderboard model non è automaticamente il best production model

Conclusione pratica:

- `WeightedEnsemble_L2` è il miglior benchmark model
- il miglior singolo LightGBM-based model è il candidato più sicuro per la produzione

Questo è il punto chiave di NB10:

AutoML è utile, ma deve essere ispezionato, compreso e giustificato prima di essere considerato un candidato reale per la produzione.