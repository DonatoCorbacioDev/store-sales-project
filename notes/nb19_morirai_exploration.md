# NB19 — Moirai Foundation Model Exploration

## Obiettivo

NB19 introduce un’esplorazione preliminare dei forecasting foundation models usando Moirai / uni2ts.

L’obiettivo non è costruire un benchmark completo.

Il notebook esplora:

* dependency requirements
* runtime complexity
* environment setup
* operational feasibility

di una pipeline forecasting transformer-based moderna.

---

## Contesto

Dopo NB18 (Chronos exploration), NB19 esplora un secondo forecasting foundation model:

* Moirai

Il notebook nasce come esperimento tecnico per capire come forecasting transformers più avanzati possano integrarsi in future forecasting workflows.

---

## Workflow

NB19 tenta:

* installazione runtime
* dependency resolution
* framework setup
* forecasting environment preparation

L’obiettivo iniziale era eseguire inference forecasting con Moirai.

Durante l’installazione sono però emersi problemi significativi di compatibilità.

---

## Dependency Complexity

NB19 evidenzia un problema importante dei forecasting foundation models moderni:

> dependency explosion

L’installazione di uni2ts ha introdotto:

* downgrade Torch
* downgrade NumPy
* downgrade GluonTS
* conflitti AutoGluon
* installazioni CUDA molto pesanti
* dipendenze JAX aggiuntive

Il notebook mostra quindi che i foundation forecasting systems possono avere un forte impatto sugli ambienti ML esistenti.

---

## Engineering Insight

NB19 produce una conclusione importante di ML engineering:

> forecasting foundation model experimentation should be isolated from stable production environments.

In contesti reali questo significa:

* ambienti dedicati
* virtual environment separati
* container dedicati
* dependency isolation

Questo evita di destabilizzare pipeline forecasting già validate.

---

## Production Reasoning

NB19 mostra che il valore di un forecasting model non dipende solo dalla qualità del forecast.

Bisogna considerare anche:

* stabilità ambiente
* dependency management
* costo infrastrutturale
* compatibilità pipeline
* maintainability
* deployment complexity

Questo è particolarmente importante nei forecasting systems enterprise-oriented.

---

## Conclusione

NB19 non viene considerato un benchmark forecasting completo.

Il notebook viene considerato un exploratory engineering notebook.

L’esperimento ha comunque prodotto valore perché ha mostrato:

* complessità operative dei forecasting foundation models
* rischi di dependency conflicts
* necessità di environment isolation
* differenza tra experimentation e production stability

NB19 aggiunge quindi una prospettiva molto realistica di ML engineering al progetto forecasting.