# NB6 — Final Candidate Retraining

## Obiettivo

Eseguire il retraining finale del modello selezionato utilizzando **l'intero dataset storico disponibile**.

Obiettivi principali:

- costruire il modello finale utilizzando tutte le informazioni disponibili
- mantenere invariata la pipeline validata nei notebook precedenti
- preparare il modello per la registrazione nel Model Registry
- separare chiaramente la fase di validazione dalla fase di produzione

---

## Contesto

Nei notebook precedenti è stata definita la pipeline completa:

- NB4 → tracking esperimenti con MLflow
- NB5 → validazione con walk-forward su subset
- NB5 full data → validazione ufficiale su dataset completo

NB5 full data rappresenta:

**il riferimento principale per la valutazione del modello**

Questo notebook non introduce nuove valutazioni, ma utilizza il modello già validato.

---

## Pipeline

È stata mantenuta invariata la pipeline:

- feature engineering avanzato (lag, rolling, trend, promozioni)
- modello LightGBM
- stessi iperparametri validati

Differenze principali rispetto ai notebook precedenti:

- utilizzo dell'intero dataset storico
- nessuna suddivisione train/validation
- nessuna cross-validation

---

## Strategia di training

Il modello viene addestrato su:

- tutto il dataset disponibile (2013 → 2017)
- tutte le feature già validate

Motivazione:

- sfruttare al massimo le informazioni disponibili
- migliorare la capacità di generalizzazione del modello finale

---

## Metriche

In questa fase:

- non vengono calcolate nuove metriche
- non viene eseguita alcuna validazione

Le metriche di riferimento restano quelle ottenute in:

**NB5 full data**

Valori principali:

- RMSLE mean ≈ 0.600  
- RMSLE std ≈ 0.015  

---

## Interpretazione

- Il modello finale è costruito sulla base di una pipeline già validata
- Le performance sono stimate tramite cross-validation precedente
- Il retraining su full data consente di sfruttare l'intero storico disponibile

Nota importante:

Il miglioramento non deriva da modifiche al modello, ma:

- dalla validazione robusta
- dall'utilizzo di più dati in fase finale

---

## Integrazione con MLflow

Durante questo notebook:

- viene tracciato il retraining finale
- vengono loggati:
  - parametri del modello
  - riferimento alle metriche NB5 full data
- il modello viene salvato come artefatto

Il modello è poi registrato nel Model Registry come:

**final candidate**

---

## Conclusione

Questo notebook rappresenta lo step finale della pipeline di forecasting.

Risultato:

- modello addestrato su full dataset
- pipeline coerente e validata
- separazione chiara tra:
  - validazione (NB5)
  - produzione (NB6)

Il modello è pronto per utilizzo e deploy.

---

## Step successivo

- utilizzo del modello per inferenza su test set
- eventuale deployment / integrazione in pipeline reale