# NB8 — Targeted Improvement on Critical Segments

## Obiettivo

Sviluppare e valutare un esperimento di **feature engineering mirato** per migliorare le performance del modello nei segmenti più critici identificati in NB7.

Obiettivi principali:

- migliorare le performance durante:
  - periodi di promozione
  - osservazioni ad alto volume di vendita
  - situazioni di elevata variabilità (weekend)
- verificare se feature specifiche possono ridurre gli errori nei casi più rilevanti
- confrontare il nuovo modello con la baseline avanzata (NB5 / NB6)
- prendere una decisione basata su evidenze

Questo notebook NON introduce nuovi modelli ma testa un'ipotesi mirata basata su error analysis

---

## Contesto

In NB7 è emerso che il modello presenta difficoltà in:

- promozioni
- picchi di vendita
- weekend
- categorie ad alta variabilità

NB8 nasce come risposta diretta a queste criticità

Strategia:

- mantenere invariata la pipeline validata
- introdurre solo nuove feature mirate
- valutare l’impatto in modo controllato

---

## Pipeline

Pipeline invariata rispetto a NB5:

- preprocessing temporale
- feature engineering baseline + avanzato
- modello LightGBM
- walk-forward cross-validation

Differenza principale:

introduzione di un nuovo set di feature (Targeted V2)

---

## Strategia di esperimento

Approccio adottato:

1. definizione baseline (Advanced V1)
2. costruzione nuovo set di feature (Targeted V2)
3. valutazione con stessa validazione temporale
4. confronto:
   - metriche globali
   - metriche per segmento

Confronto equo e controllato (no leakage, stessa CV)

---

## Feature Engineering

### Baseline (V1)

Feature già validate:

- lag_1, lag_7
- rolling_mean_7, rolling_std_7
- rolling_mean_14
- trend_1_7
- promo_last_7
- feature temporali (calendar)

---

### Targeted Features (V2)

Feature introdotte per catturare:

#### Promozioni

- `is_promo`
- `promo_intensity`
- `promo_rolling_mean_7`
- `promo_rolling_sum_14`

Obiettivo: modellare meglio l’effetto cumulativo delle promozioni

---

#### Picchi di vendita / volatilità

- `rolling_max_7`
- `rolling_max_14`
- `rolling_std_14`
- `sales_spike_ratio_7`

Obiettivo: catturare dinamiche non lineari e spike improvvisi

---

## Validazione

Stessa configurazione di NB5:

- walk-forward cross-validation
- 4 fold
- validation window: 28 giorni
- training solo su dati passati

Garantisce confronto corretto tra V1 e V2

---

## Risultati Globali

Confronto medio sui fold:

- **Advanced V1**
  - RMSLE ≈ 0.6046
  - MAE ≈ 68.42

- **Targeted V2**
  - RMSLE ≈ 0.6094
  - MAE ≈ 68.05

---

### Interpretazione

- MAE leggermente migliorato
- RMSLE peggiorato

Miglioramento non consistente a livello globale

---

## Analisi per Segmento

### Promozioni

- V1 MAE ≈ 137.03
- V2 MAE ≈ 136.35

Miglioramento molto limitato

---

### High Sales

- V1 MAE ≈ 237.75
- V2 MAE ≈ 236.39

Lieve miglioramento sui picchi

---

### Weekend

- V1 MAE ≈ 86.94
- V2 MAE ≈ 86.65

Miglioramento marginale

---

## Interpretazione Complessiva

Le nuove feature:

- migliorano leggermente i segmenti critici
- NON migliorano in modo significativo il modello globale

Segnale importante:

Il problema NON è risolvibile solo con feature rolling o interne al dataset

---

## Insight Tecnico

Questo esperimento evidenzia che:

- le promozioni introducono dinamiche complesse e non lineari
- i picchi di vendita richiedono segnali più informativi
- le feature attuali non catturano completamente il contesto reale

Limite strutturale del dataset / feature set

---

## Impatto Business

Gli errori più critici restano in:

- promozioni
- picchi di vendita

Ovvero nei momenti più rilevanti per il business

Nonostante piccoli miglioramenti:

Il modello NON è ancora affidabile nei casi ad alto impatto economico

---

## Decisione

Targeted V2 NON sostituisce il modello attuale.

Motivazioni:

- peggioramento RMSLE globale
- miglioramenti troppo marginali nei segmenti critici
- aumento complessità senza reale beneficio

Si mantiene Advanced V1 come modello finale

---

## Conclusione

NB8 rappresenta un esperimento guidato da error analysis.

Risultati:

- validazione dell’approccio data-driven
- identificazione dei limiti delle feature attuali
- esclusione di una soluzione non efficace

Questo notebook dimostra capacità di:

- analizzare errori
- formulare ipotesi
- testare in modo controllato
- prendere decisioni corrette

---

## Step successivi

Possibili direzioni future:

- integrazione dati esterni (festività, eventi)
- modellazione più avanzata delle promozioni
- modelli specifici per segmento (store / family)
- approcci probabilistici
- ensemble o modelli ibridi

Focus: migliorare nei casi business-critical, non solo sulle metriche medie