=================================================================
🧠 ARSENAL — AÉRATION (RECOMMANDATION)
Schéma architectural décisionnel
=================================================================

                   ┌────────────────────────────┐
                   │     CAPTEURS PHYSIQUES     │
                   │────────────────────────────│
                   │ • T° int RDC / étage       │
                   │ • T° extérieure            │
                   │ • HA int / ext             │
                   │ • RH extérieure            │
                   │ • CO₂ RDC / étage          │
                   │ • Pluie (Zigbee / Netatmo) │
                   │ • Saison                   │
                   └─────────────┬──────────────┘
                                 │
                                 ▼
                   ┌────────────────────────────┐
                   │   CAPTEURS DÉRIVÉS / NORMAL│
                   │────────────────────────────│
                   │ • humidité absolue calculée│
                   │ • températures max zones   │
                   │ • indicateurs météo        │
                   └─────────────┬──────────────┘
                                 │
                                 ▼
                   ┌────────────────────────────┐
                   │ PARAMÉTRAGE DÉCLARATIF     │
                   │ (input_number / boolean)   │
                   │────────────────────────────│
                   │ • seuils ΔHA / ΔT          │
                   │ • modulateurs (nuit, pluie)│
                   │ • seuils CO₂               │
                   │ • temporalité / anti-spam  │
                   │ • autorisations utilisateur│
                   └─────────────┬──────────────┘
                                 │
          ┌──────────────────────┴──────────────────────┐
          │                                             │
          ▼                                             ▼
┌───────────────────────────────┐              ┌────────────────────────────────┐
│ 🪟 DÉCISION LOCALE RDC        │              │     🪟 DÉCISION LOCALE ÉTAGE   │
│───────────────────────────────│              │────────────────────────────────│
│ binary_sensor.aeration_       │              │ binary_sensor.aeration_        │
│ preferable_rdc                │              │ preferable_etage               │
│                               │              │                                │
│ • calcul local                │              │ • calcul local                 │
│ • tolérance unknown           │              │ • tolérance unknown            │
│ • décision explicite          │              │ • décision explicite           │
│ • attributs diagnostics       │              │ • attributs diagnostics        │
│ • aucun effet de bord         │              │ • aucun effet de bord          │
└─────────────┬─────────────────┘              └─────────────┬──────────────────┘
              │                                              │
              └───────────────────┬──────────────────────────┘
                                  ▼
               ┌────────────────────────────────┐
               │ 🌬️ AGRÉGATION GLOBALE          │
               │────────────────────────────────│
               │ binary_sensor.aeration_        │
               │ conseillee                     │
               │                                │
               │ • OR logique RDC / étage       │
               │ • aucune logique métier        │
               │ • décision_globale exposée     │
               └─────────────┬──────────────────┘
                             │
           ┌─────────────────┴─────────────────┐
           │                                   │
           ▼                                   ▼
┌──────────────────────────┐     ┌──────────────────────────────┐
│ 🔔 NOTIFICATIONS         │     │      🎨 UI (DASHBOARDS)      │
│──────────────────────────│     │──────────────────────────────│
│ Automations dédiées      │     │      button-cards Arsenal    │
│                          │     │                              │
│ • présence               │     │      • restitution fidèle    │
│ • fenêtres ouvertes      │     │      • lecture seule         │
│ • autorisations          │     │      • motifs visibles       │
│ • anti-spam persistant   │     │      • aucun calcul métier   │
│                          │     │                              │
│    Aucune décision       │     │          Aucun effet de bord │
└──────────────────────────┘     └──────────────────────────────┘


=================================================================
INVARIANTS STRUCTURELS
=================================================================

✗ La recommandation ne pilote rien
✗ La recommandation ne bloque rien
✗ L’UI ne décide rien
✗ Les notifications ne modifient aucun état

✓ Décision = capteurs
✓ Action = humaine
✓ UI = observation
✓ Reload YAML = test de robustesse
=================================================================