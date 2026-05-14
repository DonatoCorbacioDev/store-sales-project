# NB12 — Business-Aware Forecast Evaluation

## Obiettivo

NB12 valuta la qualità del forecast da una prospettiva business-oriented.

I notebook precedenti si erano concentrati su:

* accuratezza predittiva
* robustezza del modello
* costo computazionale
* qualità del benchmark

NB12 cambia prospettiva.

L’obiettivo non è più capire quale modello predice meglio in media,
ma quale modello sbaglia in modo meno costoso per il business.

NB12 introduce una valutazione orientata al rischio operativo.

Questo notebook misura:

* forecast bias (underforecast vs overforecast)
* rischio nei giorni promozionali
* rischio nei segmenti ad alto volume
* esposizione sulle top-selling families
* impatto economico pesato dell’errore

NB12 non è un notebook di training.

È un notebook di **business-facing forecast evaluation**.

---

## Contesto

NB9 e NB11 hanno mostrato due candidati validi:

* **NB9** → miglior configurazione default cost/performance
* **NB11** → configurazione più costosa ma migliore su errore assoluto

Tuttavia, metriche come MAE, RMSE e RMSLE non sono sufficienti da sole.

Due modelli possono avere errori simili in media,
ma produrre errori molto diversi nei punti che contano davvero.

Nel forecasting retail questo è il punto critico:

> non tutti gli errori hanno lo stesso costo.

Sbagliare una previsione:

* in un giorno normale
* su un prodotto marginale
* con vendite basse

non ha lo stesso impatto di sbagliare:

* in un giorno promozionale
* su una top family
* con volumi alti

NB12 nasce per misurare questa differenza.

---

## Pipeline

NB12 non addestra nuovi modelli.

NB12 usa le predizioni già salvate da:

* `NB9`
* `NB11`

e le confronta riga per riga.

Per ogni previsione calcola:

* errore grezzo
* errore assoluto
* errore relativo
* underforecast flag
* overforecast flag

Queste informazioni vengono poi segmentate in slice business-oriented.

L’obiettivo non è migliorare il benchmark.

L’obiettivo è misurare il rischio operativo.

---

## Strategia

NB12 introduce una logica di valutazione più vicina al contesto reale.

Il notebook segmenta l’errore in base a quattro dimensioni operative:

* promo vs non-promo
* low vs high sales
* top families vs long tail
* weighted business exposure

Questo permette di capire non solo quanto il modello sbaglia,
ma soprattutto dove sbaglia e quanto costa sbagliare lì.

NB12 trasforma metriche di regressione in segnali di rischio operativo.

---

## Key Findings

### NB11 è più sicuro del solo confronto MAE/RMSE

NB11 era già risultato migliore di NB9 su errore assoluto.

NB12 mostra che il vantaggio di NB11 non è solo statistico.

È operativo.

NB11 riduce l’errore proprio nei segmenti più costosi:

* promo days
* high sales
* top-selling families
* high-risk slices

Questo rende NB11 più interessante non solo come benchmark,
ma come candidato operativo nei segmenti sensibili.

---

### Le promozioni restano il principale driver di errore

Il risultato più chiaro di NB12 è che le promozioni restano il punto più critico.

Su giorni non promozionali l’errore medio è basso.
Su giorni promozionali l’errore esplode.

Questo vale per entrambi i modelli.

NB11 migliora rispetto a NB9, ma il gap resta enorme.

Questo indica che il principale problema residuo del sistema è ancora la gestione delle promozioni.

---

### Gli errori più costosi si concentrano nei segmenti very_high

NB12 mostra che il costo operativo non è distribuito in modo uniforme.

La maggior parte del rischio si concentra nei segmenti ad alto volume, in particolare:

* `high`
* `very_high`

Qui gli errori sono molto più costosi,
e qui NB11 mostra il vantaggio più utile.

Questo conferma che il valore di NB11 non è migliorare la media,
ma ridurre il rischio nei punti ad alta esposizione.

---

### Le top-selling families concentrano gran parte del rischio

NB12 mostra che il rischio non è distribuito in modo uniforme nemmeno tra le famiglie prodotto.

Le top-selling families concentrano una quota molto più alta di errore pesato.

Questo significa che il forecast non dovrebbe essere valutato in modo uniforme su tutte le family.

Gli errori sulle famiglie ad alto volume pesano molto di più.

NB11 migliora proprio in questo segmento.

---

### Il vero vantaggio di NB11 emerge nei casi più costosi

Il risultato più importante di NB12 è la high-risk operational slice:

* promo days
* high / very_high sales

Questo è il caso più costoso del sistema.

Ed è qui che NB11 mostra il vantaggio più forte.

Questo è il punto chiave del notebook:

NB11 non è semplicemente “più accurato”.

NB11 è più sicuro dove il forecast costa di più.

---

## Production Reasoning

NB12 cambia il criterio di scelta del modello.

Prima:

> scegliere il modello con la metrica media migliore

Dopo NB12:

> scegliere il modello che riduce il rischio nei segmenti più costosi

Questo cambia il significato della selezione.

### NB9

Resta il miglior modello default:

* più semplice
* più economico
* più veloce
* miglior cost/performance

### NB11

Diventa il miglior modello per scenari ad alta esposizione:

* promo-heavy periods
* high-volume operations
* top-selling segments
* cost-sensitive forecasting

NB12 non sostituisce NB9.

NB12 spiega quando NB11 è preferibile.

---

## Problemi emersi

NB12 mostra tre problemi ancora aperti:

* le promozioni restano il principale driver di errore
* i segmenti `very_high` restano molto costosi
* il modello tende ancora a sottostimare in media

Questo significa che il sistema è migliore,
ma non ancora robusto nei punti di massimo rischio.

---

## Proposte di miglioramento

Le azioni più sensate dopo NB12 non sono nuovi benchmark.

Le azioni più sensate sono:

* migliorare feature promozionali
* introdurre promo uplift / promo intensity
* correggere il bias di underforecast
* introdurre forecast weighting business-aware
* specializzare il modello per segmenti high-risk

NB12 mostra che il collo di bottiglia non è più il modello in generale.

Il collo di bottiglia è la gestione dei segmenti ad alta esposizione.

---

## Conclusione

NB12 sposta la valutazione del forecasting da qualità predittiva a utilità operativa.

Il punto non è solo quale modello sbaglia meno.

Il punto è quale modello sbaglia in modo meno costoso.

NB12 mostra che:

* NB9 resta il miglior default cost/performance
* NB11 è il candidato più sicuro nei segmenti ad alta esposizione
* il rischio reale è concentrato in promo, top families e volumi alti

Questo è il punto chiave di NB12:

il miglior forecast non è quello con l’errore medio più basso,
ma quello con gli errori meno costosi in produzione.
