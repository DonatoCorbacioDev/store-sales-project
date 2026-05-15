# NB16 — AutoGluon TimeSeries vs Tabular Forecasting

## Obiettivo

NB16 introduce un confronto metodologico tra due paradigmi di forecasting:

* tabular feature-driven forecasting
* native time-series forecasting

Il notebook non riapre la pipeline principale NB1–NB15.

L’obiettivo non è sostituire il modello candidato, ma capire quando un approccio tabular può essere preferibile rispetto a un approccio nativo time-series.

La domanda centrale è:

> quando conviene trasformare il forecasting in regressione tabulare e quando conviene usare un modello nativo per serie temporali?

---

## Contesto

NB1–NB15 avevano già costruito una pipeline forecasting production-oriented con:

* baseline
* feature engineering
* walk-forward validation
* AutoML benchmark
* business-aware evaluation
* trust scoring
* monitoring e drift strategy

NB16 aggiunge un esperimento laterale controllato.

Il riferimento tabular è NB9, dove AutoGluon Tabular era stato applicato alla pipeline validata con feature ingegnerizzate.

NB16 usa invece AutoGluon TimeSeries, sfruttando direttamente la struttura temporale multi-serie.

---

## Approccio

Il dataset viene trasformato in formato panel time-series.

Ogni serie è identificata da:

* `store_nbr`
* `family`

Queste due variabili vengono combinate in un unico `item_id`.

La struttura diventa:

* `item_id`
* `timestamp`
* `target`

AutoGluon TimeSeries riceve quindi la sequenza temporale direttamente, mentre il modello tabular riceve feature costruite manualmente.

---

## Validazione

NB16 usa una validazione coerente con il confronto NB9:

* 2 fold recenti
* orizzonte di previsione a 28 giorni
* training sempre sul passato
* validazione sul periodo successivo

Questo mantiene il confronto metodologico controllato.

---

## Risultati

AutoGluon TimeSeries ottiene:

* RMSLE medio: circa 0.443
* MAE medio: circa 61.42
* RMSE medio: circa 226.08
* R² medio: circa 0.969

Il riferimento NB9 AutoGluon Tabular aveva:

* RMSLE: circa 0.476
* MAE: circa 55.54
* RMSE: circa 201.04
* R²: circa 0.976

NB16 mostra quindi che AutoGluon TimeSeries migliora RMSLE, ma peggiora MAE e RMSE rispetto al tabular benchmark.

Il risultato non va interpretato come “un modello è sempre migliore”.

Va interpretato come differenza tra paradigmi.

---

## Interpretazione

### Tabular feature-driven forecasting

L’approccio tabular trasforma il forecasting in un problema di regressione supervisionata.

Punti di forza:

* controllo esplicito delle feature
* lag e rolling costruiti manualmente
* forte integrazione con variabili business
* migliore interpretabilità
* debug più semplice
* buona performance quando il feature engineering è solido

Limiti:

* maggiore lavoro di feature engineering
* rischio leakage da gestire con attenzione
* la struttura temporale non è modellata nativamente

---

### Native time-series forecasting

L’approccio time-series modella direttamente ogni serie come sequenza temporale.

Punti di forza:

* orizzonte di forecast gestito direttamente
* meno feature engineering manuale
* buon fit per forecasting multi-serie
* astrazione più naturale per problemi forecasting

Limiti:

* minore controllo diretto sulle feature
* debug più difficile
* covariate business da gestire con attenzione
* comportamento del modello meno interpretabile

---

## Production Reasoning

NB16 mostra che la scelta del modello non dipende solo dalla metrica.

In un contesto aziendale bisogna valutare:

* performance
* interpretabilità
* controllo sulle feature
* facilità di debug
* gestione delle covariate business
* costo computazionale
* integrazione nella pipeline esistente

L’approccio tabular resta molto forte quando il team vuole controllo, ispezionabilità e integrazione con feature business.

L’approccio time-series è interessante quando il team vuole prototipare rapidamente forecast multi-serie e ridurre il feature engineering manuale.

---

## Conclusione

NB16 non sostituisce NB1–NB15.

Aggiunge una lettura metodologica del progetto.

Il punto chiave è:

> la scelta tra tabular forecasting e native time-series forecasting dipende dal contesto produttivo, non solo dalla metrica migliore.

NB16 dimostra che un Machine Learning Engineer deve saper confrontare paradigmi diversi e scegliere quello più adatto al problema, alla pipeline e ai vincoli aziendali.