# NB15 — Forecast Monitoring & Drift Strategy

## Obiettivo

NB15 introduce il layer finale di monitoring della pipeline di forecasting.

I notebook precedenti avevano già costruito il sistema di forecasting e introdotto:

* benchmark e validazione robusta
* valutazione business-aware
* trust scoring
* decision policy

NB15 risponde alla domanda finale:

> come capisco quando il forecast sta iniziando a peggiorare?

NB15 non è un notebook di training.

È un notebook di **monitoring operativo** e **drift governance**.

L’obiettivo non è migliorare il benchmark.

L’obiettivo è definire come monitorare il forecasting system dopo il deploy.

NB15 introduce:

* monitoring signals
* drift detection
* alerting logic
* retraining triggers

NB15 trasforma il forecast da sistema decisionale
a sistema monitorabile nel tempo.

---

## Contesto

NB14 aveva introdotto il layer decisionale del forecast.

Dopo NB14 il sistema era già in grado di:

* produrre forecast
* stimare il livello di trust
* decidere quando usare, rivedere o bloccare una previsione

A questo punto il problema non era più:

> quando fidarsi del forecast?

Il problema successivo era:

> come capire quando il sistema sta smettendo di essere affidabile?

NB15 introduce questo layer.

Il notebook non cerca un modello migliore.

NB15 costruisce una logica per monitorare il comportamento del sistema nel tempo
e rilevare segnali di degradazione prima che diventino un problema operativo.

---

## Pipeline

NB15 non addestra nuovi modelli.

NB15 utilizza l’output operativo prodotto in:

* `NB14`

In particolare carica:

* trust score
* trust tier
* decision action
* abs error
* pct error
* underforecast
* promo risk

NB15 non monitora solo la performance.

Monitora il comportamento operativo del sistema.

Il notebook aggrega il comportamento del forecast per data
e costruisce un monitoring frame giornaliero.

Per ogni giorno calcola:

* mean trust
* risky share
* review share
* mean absolute error
* mean percentage error
* underforecast rate
* promo risky share

Questi segnali diventano i KPI di monitoring del sistema.

---

## Strategia

NB15 introduce una logica di drift detection.

Il drift non viene definito come “errore alto”.

Il drift viene definito come:

> comportamento fuori dal range operativo normale

Per farlo, NB15 costruisce una baseline di comportamento atteso
usando i quantili storici osservati.

Questa baseline definisce:

* trust minimo accettabile
* risky share massimo accettabile
* errore medio massimo accettabile
* underforecast massimo tollerabile
* promo risk massimo tollerabile

Ogni giorno il sistema confronta il comportamento osservato
con questa baseline.

Quando il comportamento esce dal range normale,
NB15 attiva segnali di drift.

---

## Key Findings

### Il sistema è stabile la maggior parte del tempo

NB15 mostra che il forecasting system opera in stato stabile
per la maggior parte del tempo.

Distribuzione degli stati di monitoring:

* **Stable** = 75.00%
* **Watch** = 7.14%
* **Warning** = 10.71%
* **Critical** = 7.14%

Questo è uno dei risultati più importanti del notebook.

Il sistema non è perfetto,
ma è stabile nella maggior parte delle finestre osservate.

---

### Il drift esiste ma non è casuale

NB15 mostra che il degrado del forecast non è uniforme né casuale.

Esistono finestre specifiche
in cui il sistema mostra segnali di instabilità:

* calo del trust medio
* aumento dei forecast Risky
* crescita dell’underforecast
* peggioramento del comportamento promozionale

Questo significa che il drift non è invisibile.

È osservabile e misurabile.

---

### Le promo restano il principale segnale di degrado

Anche in monitoring emerge lo stesso pattern visto nei notebook precedenti.

Le promozioni restano il principale driver di instabilità.

Quando il sistema degrada,
il primo segnale tende a emergere nelle:

* promo risky share
* underforecast su promo
* aumento del risky rate nei giorni promozionali

Questo conferma che il promo forecasting resta
il principale punto di fragilità del sistema.

---

### Il monitoring rende il sistema controllabile

Il risultato più importante di NB15 non è una metrica.

È una logica di controllo.

NB15 dimostra che il sistema non deve essere solo accurato.

Deve essere anche osservabile e controllabile.

Il monitoring introduce quattro stati operativi:

* **Stable** → nessuna azione
* **Watch** → monitoraggio stretto
* **Warning** → investigazione
* **Critical** → review / retraining

Questo è il vero output del notebook.

---

## Production Reasoning

NB15 cambia il significato del forecasting system.

Dopo NB15 il problema non è più:

> il forecast è accurato?

Il problema diventa:

> il forecast sta continuando a comportarsi come dovrebbe?

Questo cambia il ruolo del sistema.

Il forecast non è più solo:

* prediction
* trust
* decision

Diventa:

* prediction
* trust
* decision
* monitoring
* alerting
* retraining governance

NB15 sposta il forecasting da decision system
a monitored production system.

---

## Problemi emersi

NB15 mostra quattro limiti ancora aperti:

* il drift viene rilevato ma non ancora corretto automaticamente
* le soglie sono ancora euristiche e non calibrate su feedback reale
* il promo degradation resta il principale punto fragile
* il retraining è ancora una decisione assistita, non automatica

Questo significa che il sistema è monitorabile,
ma non ancora pienamente autonomo.

---

## Proposte di miglioramento

NB15 suggerisce quattro estensioni naturali:

* calibrare le soglie di monitoring su feedback reale
* integrare alert automatici su dashboard / logging
* automatizzare trigger di retraining
* collegare il monitoring a una pipeline di retraining orchestrata

Questi interventi sono più utili di un nuovo benchmark generico.

NB15 mostra che il prossimo guadagno non verrà
da un altro modello generico.

Verrà da una migliore capacità di controllo del sistema.

---

## Conclusione

NB15 aggiunge il layer finale di monitoring alla pipeline di forecasting.

I notebook precedenti avevano già mostrato:

* quanto il forecast è accurato
* dove fallisce
* quanto costa sbagliare
* quando il forecast è abbastanza affidabile da essere usato

NB15 mostra come capire quando il sistema sta iniziando a degradare.

Questo è il punto chiave di NB15:

il forecast non è solo un sistema decisionale.

È un sistema che deve anche essere monitorato e governato nel tempo.