# NB7 — Error Analysis on Validation Predictions

## Obiettivo

Analizzare il comportamento del modello finale utilizzando le predizioni generate durante la **walk-forward cross-validation (NB5 full data)**.

Obiettivi principali:

- comprendere dove il modello commette errori
- identificare pattern di errore (temporali e segmentati)
- analizzare l’impatto di variabili chiave (weekend, promozioni, vendite)
- estrarre insight utili per miglioramenti futuri
- collegare i risultati tecnici al contesto business

---

## Contesto

Il modello è stato:

- validato in NB5 full data tramite walk-forward cross-validation
- retrainato su full dataset in NB6

Questo notebook utilizza:

- le predizioni generate sui fold di validazione
- dati completamente **unseen durante il training**

NB7 rappresenta la fase di **model diagnosis**

---

## Pipeline

È stata mantenuta invariata la pipeline:

- feature engineering avanzato
- modello LightGBM
- stessa configurazione dei fold di NB5 full data

Differenza principale:

- utilizzo delle predizioni di validazione per analisi errori
- nessun training aggiuntivo

---

## Strategia di analisi

L’analisi viene effettuata su:

- predizioni out-of-fold (validation)
- finestre temporali recenti (2017)
- dataset aggregato su tutti i fold

Questo consente di:

- simulare uno scenario reale di forecasting
- analizzare errori su dati mai visti

---

## Metriche

Sono utilizzate metriche di errore per interpretazione:

- MAE (Mean Absolute Error)
- distribuzione degli errori
- errori per segmento

Nota:

Le metriche globali di riferimento restano quelle di NB5 full data.

---

## Analisi degli errori

L’analisi è stata suddivisa in più dimensioni:

### Temporale
- errore medio per fold
- andamento giornaliero degli errori

### Segmentazione
- errori per store
- errori per product family

### Pattern comportamentali
- weekday vs weekend
- promozioni vs no promozioni
- low vs high sales

---

## Key Findings

L’analisi degli errori evidenzia diversi pattern importanti e quantificabili nel comportamento del modello.

---

### Stabilità del modello

Il modello mostra una buona stabilità sui diversi fold di validazione.

- Il MAE varia indicativamente tra ~58 e ~78
- Non emergono segnali evidenti di forte overfitting temporale
- Le differenze tra fold sembrano legate più alla variabilità dei dati che a instabilità del modello

Questo indica che il modello generalizza in modo abbastanza stabile nel tempo.

---

### Pattern temporali: weekday vs weekend

Gli errori risultano più elevati durante il weekend:

- Weekday MAE ≈ 60.9
- Weekend MAE ≈ 87.2

La domanda nel weekend risulta più variabile e meno prevedibile.

---

### Impatto delle promozioni

Le promozioni hanno un impatto molto forte sugli errori di previsione:

- No promotion MAE ≈ 11.5
- Promotion MAE ≈ 137.1

Il modello fatica molto di più quando i prodotti sono in promozione.

---

### Effetto del volume di vendita

L’errore aumenta in modo significativo al crescere del volume di vendita:

- Low sales MAE ≈ 2.4
- High sales MAE ≈ 238.0

Il modello funziona bene sulle osservazioni a bassa domanda, ma fatica sui picchi di vendita.

---

### Variabilità per product family

Alcune famiglie di prodotto risultano molto più difficili da prevedere:

- GROCERY I MAE ≈ 557
- BEVERAGES MAE ≈ 483

Queste categorie presentano elevata variabilità e complessità.

---

### Differenze tra store

Alcuni store mostrano errori medi più alti in modo consistente.

Questo suggerisce che il modello globale non cattura completamente le dinamiche specifiche dei singoli punti vendita.

---

### Interpretazione complessiva

Il modello mostra una buona stabilità generale, ma presenta difficoltà nei casi caratterizzati da:

- alta variabilità della domanda
- promozioni
- weekend
- picchi di vendita
- categorie ad alto volume

---

### Impatto business

Dal punto di vista business, gli errori più importanti si verificano nei momenti più critici:

- periodi promozionali
- situazioni ad alto volume di vendita
- categorie ad alto impatto economico

Migliorare questi segmenti avrebbe il maggiore valore per il business.

---

### Direzioni di miglioramento

Possibili miglioramenti:

- feature più avanzate per le promozioni
- migliore gestione dei picchi di vendita
- modelli specifici per store o product family
- introduzione di segnali esterni (festività, eventi)

Trade-off:

- maggiore complessità → possibile perdita di generalizzazione
- aumento del costo computazionale

---

## Conclusione

NB7 fornisce una visione dettagliata del comportamento del modello.

Risultati principali:

- modello stabile nel tempo
- errori concentrati in specifici scenari
- identificazione chiara dei limiti attuali

Questo notebook:

- non migliora il modello  
- ma consente di **capire come migliorarlo**

---

## Step successivo

Possibili sviluppi:

- miglioramento mirato delle feature sulle promozioni
- gestione specifica dei picchi di vendita
- segmentazione del modello per store o categoria
- integrazione in pipeline reale di forecasting