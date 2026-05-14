# NB13 — Business Error Diagnosis & Action Plan

## Obiettivo

NB13 estende la valutazione business-oriented introdotta in NB12.

NB12 aveva mostrato che NB11 è più sicuro di NB9 nei segmenti di forecast più costosi.

NB13 risponde alla domanda successiva:

> dove sono concentrati esattamente gli errori più costosi
> e quali interventi ridurrebbero davvero il rischio operativo?

NB13 non è un notebook di training.

È un notebook di **diagnosi operativa** e **action planning**.

L’obiettivo non è migliorare il benchmark.

L’obiettivo è identificare:

* dove il forecast genera il costo maggiore
* quali combinazioni store/family concentrano il rischio
* dove NB11 migliora rispetto a NB9
* dove NB11 continua a fallire
* quali azioni ridurrebbero il rischio reale

NB13 è il notebook che trasforma il forecast in un piano di intervento.

---

## Contesto

NB12 aveva già mostrato che il rischio non è distribuito in modo uniforme.

Gli errori più costosi si concentrano in:

* promo days
* high / very_high sales
* top-selling families

NB13 fa un passo ulteriore.

Non si limita a misurare il rischio.

NB13 localizza il rischio.

Questo notebook serve a capire:

> quali store
> quali family
> quali date
> quali pattern

stanno generando la parte più costosa dell’errore.

NB13 è il passaggio da business evaluation a business diagnosis.

---

## Pipeline

NB13 non addestra nuovi modelli.

NB13 utilizza le prediction row-level già salvate in:

* `NB9`
* `NB11`

e le allinea riga per riga sulla stessa osservazione.

Per ogni riga confronta:

* errore NB9
* errore NB11
* weighted error NB9
* weighted error NB11
* gain operativo di NB11

Questo permette di costruire una diagnosi comparativa molto più precisa.

NB13 non misura solo quanto sbagliano i modelli.

Misura:

* dove sbagliano
* quanto costa
* dove NB11 migliora
* dove resta ancora fragile

---

## Strategia

NB13 introduce una logica di diagnosi operativa.

Il notebook segmenta il rischio su quattro livelli:

* store/family concentration
* promo failure analysis
* worst underforecast analysis
* NB11 gains vs NB11 residual failures

Questo permette di passare da una valutazione aggregata del rischio
a una diagnosi localizzata dei punti di fallimento.

NB13 non chiede più:

> quale modello è migliore?

NB13 chiede:

> dove intervenire per ridurre davvero il rischio?

---

## Key Findings

### Il rischio è fortemente concentrato

NB13 mostra che il rischio operativo non è distribuito in modo uniforme.

La quota maggiore di errore pesato si concentra in un numero limitato di combinazioni:

* `store_nbr`
* `family`

Questo è uno dei risultati più importanti del notebook.

Il rischio non è diffuso in modo omogeneo.
È concentrato in pochi cluster ad alta esposizione.

Questo significa che il forecast non deve essere migliorato ovunque allo stesso modo.

Deve essere migliorato prima nei punti che pesano di più.

---

### Le promozioni restano il failure mode dominante

NB12 aveva già mostrato che le promozioni sono il segmento più costoso.

NB13 lo conferma con maggiore precisione.

I peggiori errori assoluti e pesati restano concentrati in:

* giorni promozionali
* store ad alto volume
* top-selling families

Questo conferma che il principale failure mode del sistema resta il promo forecasting.

---

### NB11 migliora dove il costo è più alto

NB13 mostra che NB11 migliora rispetto a NB9 proprio nei casi più costosi.

I maggiori gain di NB11 si osservano in:

* promo-heavy slices
* high-volume stores
* top-selling families

Questo rafforza la conclusione di NB12:

NB11 non migliora semplicemente la media.
NB11 migliora soprattutto dove il rischio costa di più.

---

### NB11 non è ancora robusto sugli spike estremi

NB13 mostra anche il limite principale di NB11.

Nonostante il miglioramento generale, NB11 continua a fallire in alcuni casi estremi:

* promo spikes molto aggressivi
* underforecast severi su high-volume
* picchi localizzati store/family

Questo è il limite residuo più importante.

NB11 è migliore.
Ma non ancora robusto sugli spike estremi.

---

### L’underforecast resta il rischio più costoso

I casi peggiori di NB11 sono ancora dominati da underforecast.

Questo è il rischio operativo più pericoloso, perché implica:

* stockout
* perdita vendite
* perdita margine
* rottura della pianificazione

NB13 mostra che il problema residuo non è solo “errore alto”.

È soprattutto:

> errore alto nei casi in cui sottostimare costa molto.

---

## Production Reasoning

NB13 cambia il significato della fase successiva.

Dopo NB13 il problema non è più:

> quale modello allenare?

Il problema diventa:

> dove intervenire prima?

Questo cambia la logica di miglioramento.

La prossima iterazione non dovrebbe partire da un nuovo benchmark generale.

Dovrebbe partire da:

* promo uplift features
* underforecast correction
* segment-specific logic
* local overrides
* alerting su high-risk slices

NB13 sposta il focus da model improvement a risk reduction.

---

## Problemi emersi

NB13 mostra quattro problemi ancora aperti:

* promo spikes restano il principale failure mode
* il rischio è concentrato in pochi store/family pockets
* NB11 fallisce ancora sugli spike estremi
* l’underforecast resta il rischio operativo più costoso

Questo significa che il sistema è migliore,
ma non ancora robusto nei punti di massimo impatto.

---

## Proposte di miglioramento

NB13 suggerisce quattro interventi concreti:

* introdurre feature promozionali più forti
* applicare bias correction / asymmetric underforecast penalty
* specializzare il forecast su cluster store/family ad alto rischio
* introdurre confidence / alerting layer per high-risk slices

Questi interventi sono più utili di un nuovo benchmark generico.

NB13 mostra che il prossimo guadagno non verrà da un altro modello generico.

Verrà da interventi mirati sui failure modes.

---

## Conclusione

NB13 chiude il blocco NB9–NB13 trasformando il forecasting da benchmark tecnico a piano operativo.

NB12 aveva mostrato quale modello è più sicuro.

NB13 mostra dove intervenire per ridurre ancora il rischio.

Questo è il punto chiave di NB13:

il passo successivo non è allenare un altro modello.

Il passo successivo è correggere i punti in cui il forecast continua a perdere valore.
