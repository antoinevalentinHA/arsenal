┌──────────────────────────────┐
│  TRANSITION DÉCISIONNELLE    │
│  chauffage_dernier_mode      │
└──────────────┬───────────────┘
               │   (T0)
┌──────────────────────────────┐
│  CAPTURE CONTEXTE T0         │
│  - T0 température            │
│  - type transition (T1/T2)   │
│  - offsets en vigueur        │
│  - pente / parallèle         │
│  - regime_id courant         │
│  - horodatage                │
└──────────────┬───────────────┘
               │
┌──────────────────────────────┐
│  FENÊTRE D’OBSERVATION       │
│  - recherche min / max       │
│  - surveillance courbe       │
│  - surveillance event        │
└──────────────┬───────────────┘
               │
┌─────────────────────────────────┐
│  VALIDATION / INVALIDATION      │
│  - pente/parallèle changé ?     │
│  - event chauffage_adj ?        │
│  - zone 10h00 ?                 │
│  - timeout ?                    │
│  - épisode aération ouverture ? │
│  - blocage aération actif ?     │
│  - post-aération non désarmé ?  │
└──────────────┬──────────────────┘
               │
┌──────────────────────────────┐
│  JOURNAL ÉCHANTILLON         │
│  (attaché à regime_id)       │
└──────────────┬───────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌──────────────────┐  ┌─────────────────────────────┐
│ SYNTHÈSES LOCALES│  │ AGRÉGATION CYCLES (PHASE 1) │
│ PAR RÉGIME       │  │ - reprises validées A1      │
│ - ΔT_drop        │  │ - timestamps inter-reprises │
│ - Δt_drop        │  │ - cycles journaliers        │
│ - V_reprise      │  └──────────────┬──────────────┘
│ - ΔT_rise        │                 │
│ - Δt_rise        │                 ▼
└───────────────┬──┘   ┌───────────────────────────────┐
                │      │ OSCILLATEUR THERMIQUE GLOBAL  │
                │      │ (FAMILLE D)                   │
                │      │ - D1 : amplitude oscillation  │
                │      │ - D2 : cycles / jour          │
                │      │ - D3 : durée cycle moyenne    │
                │      └──────────────┬────────────────┘
                │                     │
                ▼                     ▼
          ┌──────────────────────────────┐
          │  UI DIAGNOSTIC & ANALYSE     │
          │  - lectures physiques        │
          │  - stabilité globale         │
          │  - dérives lentes            │
          └──────────────────────────────┘
