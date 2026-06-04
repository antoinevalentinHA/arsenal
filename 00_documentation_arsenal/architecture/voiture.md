# 🚗 ARSENAL — ARCHITECTURE · VOITURE — Audi A3 e-tron

## 🎯 OBJET DU DOCUMENT

Ce document décrit l'**architecture technique** du sous-système **Voiture
(Audi A3 e-tron)** dans Arsenal : la manière dont les données sont sécurisées,
sélectionnées, mémorisées, historisées et restituées.

👉 Ce document **N'EST PAS** un contrat métier.
Il **N'INTRODUIT AUCUNE règle fonctionnelle nouvelle**.
La gouvernance normative (sources autorisées, invariants, interdits) est définie
dans le **contrat** : [`contrats/voiture.md`](../contrats/voiture.md).

> **Note de cadrage.** Ce document cartographie fidèlement l'**implémentation
> existante** telle qu'observée dans le dépôt. La justification architecturale
> approfondie de chaque choix (alternatives écartées, ADR) **reste à rédiger** ;
> elle sera ajoutée au fil des décisions, sans modifier la cartographie ci-dessous.

---

## 🧱 POSITIONNEMENT ARCHITECTURAL

Le sous-système Voiture est :

- **observationnel** (il lit l'état d'un véhicule, il ne le pilote pas) ;
- **défensif vis-à-vis du cloud** (la donnée brute fournisseur est réputée non
  fiable et n'est jamais consommée directement) ;
- **stratifié** : chaque couche ne consomme que la sortie de la couche précédente.

L'invariant architectural central est la **non-consommation directe de la donnée
cloud brute** par une automation métier, un helper, une statistique ou un
dashboard.

---

## 🧩 CHAÎNE CANONIQUE (vue d'ensemble)

```
Cloud brut (non fiable)
        │
        ▼
Capteurs locaux stabilisés        (12_template_sensors/voiture/…)
        │
        ▼
Automatisations de sélection      (11_automations/voiture/…)
        │
        ▼
Helpers de mémorisation           (03_input_numbers/voiture/…)
        │
        ▼
Capteurs statistiques + utility_meter
        │
        ▼
Persistance Recorder
        │
        ▼
UI & Dashboards                   (18_lovelace/dashboards/voiture/…)
```

La structure des couches est posée normativement par le contrat ; ce document en
décrit l'**ancrage réel dans l'arborescence**.

---

## 🗂️ ANCRAGE DANS LE DÉPÔT (implémentation observée)

### Couche perception — capteurs locaux stabilisés
`12_template_sensors/voiture/` (template *triggered* sensors), notamment :

- `batterie/` — `etat_charge.yaml`, `pourcentage.yaml`, `autonomie.yaml`,
  `snapshots_pleine_charge.yaml` ;
- `kilometrage.yaml`, `derniere_maj.yaml`, `stationnement.yaml` ;
- `revision/` — `temps.yaml`, `distance.yaml` ;
- `ouvertures/fenetres/` — capteurs d'ouvrants (voir dette AUDI-04 ci-dessous).

### Couche sélection — automatisations métier
`11_automations/voiture/` :

- `autonomie.yaml` — consolidation du snapshot d'autonomie ;
- `archive.yaml` — archivage périodique ;
- `notification_etat_charge.yaml` — restitution d'état (projection, non décision).

### Couche mémorisation — helpers
`03_input_numbers/voiture/autonomie.yaml` — baselines et snapshots d'autonomie.

### Couche mesure — utility_meter
Dans `utility_meter.yaml` : `audi_e_tron_distance_mois` et
`audi_e_tron_distance_an`, tous deux dérivés de
`sensor.audi_e_tron_kilometrage_local` (source locale, jamais le cloud brut).

### Couche persistance — Recorder
Section dédiée du `recorder.yaml` (catégorie automobile, dont la corrélation
thermique). L'historisation est volontairement bornée et explicite.

### Couche restitution — UI
`18_lovelace/dashboards/voiture/` : `audi.yaml`, `audi_batterie.yaml`,
`audi_securite.yaml`, et `18_lovelace/includes/navigation/voiture.yaml`.

---

## ❄️ SNAPSHOT ATOMIQUE & CORRÉLATION THERMIQUE

Le domaine repose sur un **snapshot atomique** d'autonomie : les valeurs liées
(autonomie pleine charge, température au moment du relevé, autonomie corrigée à
20 °C) sont écrites **dans la même automation, au même instant logique**, afin de
former un tuple cohérent exploitable pour l'analyse de l'influence thermique sur
l'autonomie.

C'est une **propriété d'architecture** (atomicité d'écriture, cohérence du tuple),
distincte de la règle métier qui en fixe la finalité — cette dernière relevant du
contrat.

---

## 🩹 DETTE & POINTS D'ATTENTION (issus de l'audit du domaine)

Source : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../audits/01_rapports/voiture/audit_domaine_audi.md).

- **AUDI-11 — Reproductibilité dépôt → runtime non garantie** *(majeur, enseignement
  principal)* : l'état documenté/dépôt peut diverger de l'état runtime ; toute
  évolution doit être revérifiée sur le système réel.
- **AUDI-04 — Sous-système ouvrants / sécurité hors contrat** *(dette
  documentaire)* : les capteurs d'ouvrants (`ouvertures/fenetres/…`, dashboard
  `audi_securite.yaml`) existent en implémentation mais ne sont pas couverts par le
  contrat. Périmètre à clarifier.
- **AUDI-05 — Angle mort du checker contractuel** : la validation contractuelle ne
  couvre pas l'intégralité du domaine.
- **AUDI-03 (recorder)** : lignes recorder résiduelles à surveiller.

Ces points sont des **constats d'audit**, pas des décisions d'architecture : ils
sont listés ici comme entrées de travail, et leur résolution éventuelle sera tracée
dans le changelog.

---

## 🔗 RÉFÉRENCES

- Contrat normatif : [`contrats/voiture.md`](../contrats/voiture.md)
- Audit du domaine : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../audits/01_rapports/voiture/audit_domaine_audi.md)
- Persistance : section automobile de `recorder.yaml`

---

## 📌 STATUT

- Nature : **document d'architecture** (référence d'implémentation)
- Autorité : **subordonnée au contrat** `contrats/voiture.md`
- Complétude : **cadrage + cartographie de l'existant** ; rationale détaillée à compléter
