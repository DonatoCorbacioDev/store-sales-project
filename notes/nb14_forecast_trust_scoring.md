# NB14 — Forecast Trust Scoring & Decision Framework

## Obiettivo

NB14 introduce il layer decisionale finale della pipeline di forecasting.

I notebook precedenti avevano già risposto a tre domande fondamentali:

* quanto il forecast è accurato
* dove il modello fallisce
* quanto questi errori costano operativamente

NB14 risponde alla domanda successiva:

> quando il forecast è abbastanza affidabile da essere usato?

NB14 non è un notebook di training.

È un notebook di **forecast governance** e **decision policy**.

L’obiettivo non è migliorare il benchmark.

L’obiettivo è trasformare l’output del forecast in un segnale decisionale utilizzabile.

NB14 introduce:

* forecast trust scoring
* trust tier assignment
* decision rules
* review / fallback logic

NB14 trasforma il forecast da output numerico a decisione operativa.

---

## Contesto

NB12 aveva già mostrato che non tutti gli errori hanno lo stesso costo.

NB13 aveva localizzato dove il forecast perde più valore:

* promo days
* underforecast
* high-sales slices
* few high-risk store/family pockets

A questo punto il problema non era più capire solo dove il modello sbaglia.

Il problema era capire:

> quando il forecast è abbastanza affidabile da essere usato direttamente
> e quando invece richiede controllo o protezione

NB14 introduce questo layer.

Il notebook non cerca un modello migliore.

NB14 costruisce una logica per decidere come usare il forecast che abbiamo oggi.

---

## Pipeline

NB14 non addestra nuovi modelli.

NB14 utilizza il candidato operativo più forte identificato nei notebook precedenti:

* `NB11` (AutoGluon extended budget)

NB11 viene usato come base perché aveva mostrato il miglior comportamento operativo
nei segmenti più costosi.

NB14 carica le prediction row-level di NB11 e costruisce un evaluation frame orientato alla decisione.

Per ogni previsione calcola:

* errore grezzo
* errore assoluto
* errore percentuale
* underforecast / overforecast
* promo exposure
* revenue proxy
* weighted error exposure

Queste variabili non servono per ri-valutare il benchmark.

Servono per stimare quanto il forecast sia affidabile in un contesto operativo.

---

## Strategia

NB14 introduce una logica di trust scoring.

Il trust non viene stimato usando una sola metrica.

Viene costruito combinando più segnali di rischio operativo:

* errore relativo
* esposizione promozionale
* rischio da underforecast
* intensità vendite
* impatto operativo pesato

Questi segnali vengono trasformati in un `risk_score`
e poi invertiti in un `trust_score`.

La logica è semplice:

* alto rischio → bassa fiducia
* basso rischio → alta fiducia

Questo permette di passare da una previsione numerica
a una previsione con livello di affidabilità.

NB14 non chiede più:

> quanto è buono il forecast?

NB14 chiede:

> quanto è sicuro usare questo forecast?

---

## Key Findings

### Il forecast non è ugualmente affidabile ovunque

NB14 mostra che il forecast non ha un livello di affidabilità uniforme.

Le predizioni si distribuiscono in tre livelli di trust:

* **Safe** = 33.72%
* **Review** = 50.92%
* **Risky** = 15.36%

Questo è uno dei risultati più importanti del notebook.

Il forecast non va trattato come un output uniforme.

Va trattato come un output con livelli diversi di affidabilità.

---

### Solo una parte del forecast è direttamente automatizzabile

NB14 mostra che solo circa un terzo delle previsioni
è abbastanza affidabile da essere usato direttamente.

Questa è la quota **Safe**.

Queste previsioni possono essere utilizzate senza intervento.

Il resto del forecast richiede:

* revisione
oppure
* fallback

Questo significa che il forecast non va usato in modo cieco.

Va usato con policy diverse in base al rischio.

---

### Le promo concentrano la maggior parte delle predizioni rischiose

NB14 conferma il pattern già osservato nei notebook precedenti.

Le osservazioni promozionali concentrano la quota maggiore di forecast a basso trust.

Le promo non sono solo il segmento con errore più alto.

Sono anche il segmento con affidabilità più bassa.

Questo conferma che il principale driver di rischio resta il promo forecasting.

---

### Gli high-sales segment restano i più fragili

NB14 mostra che il trust cala fortemente nei segmenti ad alta intensità di vendita.

Le osservazioni `high` e `very_high` concentrano:

* meno forecast Safe
* più forecast Review
* più forecast Risky

Questo conferma che il rischio operativo cresce
quando cresce anche l’esposizione economica.

---

### Il forecast va trattato come sistema decisionale

Il risultato più importante di NB14 non è una metrica.

È una policy.

NB14 dimostra che il forecast non deve essere usato come output unico.

Deve essere usato come sistema decisionale con tre stati:

* **Safe** → usa forecast
* **Review** → richiede revisione
* **Risky** → attiva fallback

Questo è il vero output del notebook.

---

## Production Reasoning

NB14 cambia il significato del forecast.

Dopo NB14 il problema non è più:

> quanto il forecast è accurato?

Il problema diventa:

> quando il business può fidarsi del forecast?

Questo cambia completamente il ruolo del modello.

Il forecast non è più solo una previsione.

Diventa un segnale operativo con:

* livello di fiducia
* azione associata
* policy di utilizzo

NB14 sposta il forecasting da prediction problem a decision system.

---

## Problemi emersi

NB14 mostra quattro limiti ancora aperti:

* solo una parte del forecast è direttamente automatizzabile
* le promo restano il segmento meno affidabile
* gli high-sales segment restano ad alta fragilità
* la decision policy è ancora euristica e non calibrata su feedback reale

Questo significa che il sistema è utilizzabile,
ma non ancora completamente automatizzabile.

---

## Proposte di miglioramento

NB14 suggerisce quattro estensioni naturali:

* calibrare il trust score su feedback reale
* raffinare le soglie decisionali per segmento
* introdurre fallback specifici per promo / high-risk slices
* integrare il trust score in un layer di monitoring continuo

Questi interventi sono più utili di un nuovo benchmark generico.

NB14 mostra che il prossimo guadagno non verrà
da un altro modello generico.

Verrà da una migliore gestione operativa del forecast.

---

## Conclusione

NB14 aggiunge il layer decisionale finale alla pipeline di forecasting.

I notebook precedenti avevano già mostrato:

* quanto il forecast è accurato
* dove fallisce
* quanto costa sbagliare

NB14 mostra quando il forecast è abbastanza affidabile da essere usato.

Questo è il punto chiave di NB14:

il forecast non è solo una previsione.

È un sistema decisionale con livelli diversi di fiducia.