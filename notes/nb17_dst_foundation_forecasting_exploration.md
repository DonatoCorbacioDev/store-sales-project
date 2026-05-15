# NB17 — DST & Foundation Forecasting Exploration

## Obiettivo

NB17 introduce un’esplorazione tecnica sui problemi di forecasting causati dalle irregolarità temporali legate al daylight saving time (DST).

Il notebook non costruisce una nuova pipeline forecasting.

L’obiettivo è analizzare edge case temporali che possono emergere in sistemi reali:

* giorni da 23 ore
* giorni da 25 ore
* timestamp mancanti
* timestamp duplicati

NB17 affronta il problema da una prospettiva ML engineering e forecasting operations.

---

## Contesto Business

In sistemi energy forecasting, billing e time-sensitive forecasting, le transizioni DST possono generare anomalie operative:

* aggregazioni inconsistenti
* rolling statistics instabili
* lag features disallineate
* errori di billing
* degradazione forecasting

Questi problemi sono particolarmente rilevanti in:

* energy forecasting
* smart metering
* utility systems
* industrial monitoring
* high-frequency forecasting systems

NB17 esplora questi scenari in modo controllato usando dati sintetici.

---

## Simulazione DST

Il notebook costruisce una serie temporale oraria sintetica di consumo energetico.

Successivamente vengono simulati due scenari DST:

### Missing timestamp

Simulazione di un giorno da 23 ore:

* rimozione di una finestra temporale
* perdita di continuità temporale

### Duplicated timestamp

Simulazione di un giorno da 25 ore:

* duplicazione della stessa finestra oraria
* possibile ambiguità nelle aggregazioni

Questi scenari permettono di osservare il comportamento delle pipeline forecasting sotto irregolarità temporali.

---

## Rolling Statistics Instability

NB17 mostra che molte pipeline forecasting classiche assumono implicitamente:

* spacing temporale regolare
* rolling window stabili
* lag deterministici

Le transizioni DST possono rompere queste assunzioni.

Le conseguenze osservate includono:

* rolling mean instabili
* lag alignment incoerente
* mismatch aggregativi
* forecasting degradation

Questo è particolarmente importante per pipeline basate su:

* lag features
* rolling statistics
* temporal aggregation

---

## Foundation Forecasting Models

NB17 introduce anche una riflessione preliminare sui forecasting foundation models.

Modelli come:

* Chronos
* Moirai
* transformer-based forecasting systems

potrebbero offrire vantaggi in scenari forecasting più eterogenei o irregolari.

Possibili vantaggi:

* migliore temporal representation learning
* forecasting probabilistico
* maggiore robustezza a pattern temporali complessi
* multi-domain pretraining

NB17 non implementa ancora una pipeline transformer completa.

Introduce però il ragionamento ingegneristico che motiva future esplorazioni foundation-model.

---

## Production Reasoning

NB17 mostra che un forecasting system production-oriented non deve solo massimizzare una metrica.

Deve anche:

* validare la consistenza temporale
* gestire edge case operativi
* controllare anomalie temporali
* monitorare degradazioni causate da irregular temporal spacing

Questo cambia il ruolo del forecasting engineering.

Il problema non è solo:

> prevedere bene

ma anche:

> garantire robustezza operativa sotto condizioni temporali irregolari.

---

## Key Takeaways

NB17 evidenzia alcuni punti importanti:

* i sistemi forecasting devono validare esplicitamente la coerenza temporale
* le transizioni DST possono impattare feature engineering e business logic
* la normalizzazione UTC può ridurre alcune ambiguità
* il business local time può comunque restare necessario
* edge case temporali devono essere monitorati in produzione

---

## Conclusione

NB17 aggiunge una prospettiva ML engineering alla pipeline forecasting.

Il notebook non introduce un nuovo benchmark.

Introduce invece un problema operativo reale:

> forecasting under temporal irregularities.

NB17 mostra che forecasting engineering significa anche:

* robustezza
* monitoring
* temporal consistency
* operational reliability

non solo forecasting accuracy.