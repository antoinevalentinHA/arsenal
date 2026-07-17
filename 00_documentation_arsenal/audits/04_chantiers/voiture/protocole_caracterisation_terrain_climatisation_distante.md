# Protocole de caractérisation terrain — C25 · Climatisation distante Audi

| Champ | Valeur |
|---|---|
| **Chantier** | [C25 — Climatisation distante Audi](chantier_commande_climatisation_distante.md). |
| **Nature** | **Protocole documentaire, lecture-guidée.** Exécution manuelle via **Outils de développement → Actions**. |
| **Exécutant** | L'opérateur. Il exécute les essais et remplit la trace (§6). |
| **Statut** | **Aucune preuve recueillie.** C25 non clôturable tant que la trace §6 est vide. |
| **Sécurité** | Aucune dégradation artificielle, manipulation risquée ni panne simulée n'est demandée. |

> **Objectif.** Répondre par des preuves aux inconnues de C25 : le service fonctionne-t-il réellement sur
> ce véhicule, quels paramètres sont acceptés, quelles entités observent un démarrage réel, quelle
> latence, comment se manifeste un refus, et peut-on distinguer honnêtement refus / erreur / absence de
> confirmation. **Ce protocole ne transpose aucun modèle transactionnel et ne fige aucun statut terminal.**

---

## 0. Prérequis & rappels

- **Relever d'abord les `entity_id` runtime réels** avant tout essai : le device Audi, les capteurs
  `climatisation_state` et `remaining_climatisation_time`, et une entité brute stable de l'appareil.
  **Ne rien supposer** : ces identifiants sont des valeurs de registre (dette AUDI-11), pas des valeurs du
  dépôt.
- **Cibler le véhicule via le sélecteur d'appareil** de l'interface Actions (mode UI), sans manipuler
  d'identifiant opaque.
- **Un refus Audi est un résultat métier attendu**, pas un défaut de configuration Arsenal : il doit être
  observé et consigné honnêtement.
- **Un appel sans exception ne prouve rien** (l'intégration absorbe les erreurs). Toute conclusion de
  succès exige une **preuve indépendante de l'émission de l'appel**.

Squelette d'appel (illustratif — l'appareil se sélectionne dans l'interface ; ne pas coder d'identifiant
en dur) :

```yaml
action: audiconnect.start_climate_control
target:
  device_id: <Audi — sélectionner via le sélecteur d'appareil>
data:
  temp_c: 21
  climatisation_mode: comfort
  seat_fl: false
  seat_fr: false
  seat_rl: false
  seat_rr: false
  glass_heating: false
  climatisation_at_unlock: false
```

---

## 1. Relevés à consigner (chaque essai)

Pour **chaque** essai, consigner :

- les `entity_id` runtime exacts observés ;
- l'état initial des entités d'observation ;
- les attributs utiles ;
- l'heure d'émission de l'appel ;
- l'heure de la première transition observable ;
- le résultat dans Home Assistant ;
- le résultat dans myAudi ;
- le constat physique sur le véhicule, si possible ;
- le **niveau de preuve** (voir ci-dessous) ;
- le verdict.

### Niveau de preuve (obligatoire)

Chaque essai porte un niveau de preuve parmi :

- `HA seulement` ;
- `HA + myAudi` ;
- `HA + constat véhicule` ;
- `non confirmé`.

> **Règle de verdict.** Le verdict ne doit **jamais** être « conforme » sur la seule absence d'erreur dans
> Outils de développement. `HA seulement` **n'établit pas** un succès terminal.

---

## 2. Essai E1 — minimal

**Paramètres :** `temp_c` (ex. 21) + `climatisation_mode: comfort` + **tous les booléens à `false`**
(`seat_fl`, `seat_fr`, `seat_rl`, `seat_rr`, `glass_heating`, `climatisation_at_unlock`).

**Question :** le service **démarre-t-il réellement** la climatisation ?

**Succès minimal E1 — exige une preuve indépendante de l'émission de l'appel**, par exemple :

- une transition **crédible** de `climatisation_state` ;
- un `remaining_climatisation_time` **cohérent** ;
- une confirmation **myAudi** ;
- ou un **constat physique** sur le véhicule.

En l'absence d'au moins une de ces preuves, le verdict reste `non confirmé` — jamais « conforme ».

---

## 2 bis. Essai E1b — fin de cycle et retour à l'état initial

Après E1, observer la **fin du cycle nominal** (peut être fusionné avec E1 ou traité séparément).
Relever si possible :

- la **durée annoncée** du cycle ;
- l'**évolution** de `remaining_climatisation_time` ;
- le **retour** de `climatisation_state` à l'état inactif ;
- le **délai** de ce retour ;
- le **comportement lorsque la climatisation s'arrête naturellement** ;
- l'**existence éventuelle d'une commande d'arrêt** — **sans l'utiliser** tant qu'elle n'a pas été
  auditée.

> E1b **n'élargit pas** le chantier à une commande d'arrêt : il se limite à **observer** la fin de cycle
> et à **consigner** l'existence d'un éventuel arrêt, sans l'exercer.

---

## 3. Essais d'options — un par un (jamais groupés)

Ne regrouper **aucune** capacité non encore validée dans un même essai.

- **E2 — mode `economy`** : `temp_c` + `climatisation_mode: economy`, booléens `false`.
- **E3 — siège avant gauche** : ajouter `seat_fl: true` (le reste `false`).
- **E4 — siège avant droit** : ajouter `seat_fr: true` (le reste `false`).
- **E5 — climatisation à l'ouverture** : ajouter `climatisation_at_unlock: true`.

### Prudence spécifique sièges chauffants (E3, E4)

Distinguer **deux questions séparées**, et les consigner distinctement :

1. le backend **accepte-t-il le paramètre** sans erreur visible ?
2. le chauffage du siège est-il **réellement observable ou vérifiable** sur ce véhicule (entité dédiée,
   confirmation myAudi, ou constat physique) ?

> **L'absence de preuve physique ou d'entité dédiée ne vaut pas validation de la capacité.** Un appel sans
> exception est insuffisant, **y compris pour les options** : sans preuve indépendante, le niveau de
> preuve reste `non confirmé`.

---

## 4. Essai E6 — état naturellement incompatible

**Ne provoquer aucun état incompatible.** Exécuter l'essai **lorsqu'un état naturellement incompatible,
connu et sans risque, est disponible** — par exemple lorsque le véhicule **n'est pas branché** ou lorsque
ses **conditions habituelles de climatisation distante ne sont pas réunies**.

**Objectif :** caractériser un **refus réel**, pas fabriquer une panne. Observer **comment se manifeste le
refus**, **sans présumer** que Home Assistant exposera le motif.

---

## 5. Grille d'interprétation honnête

Distinguer trois niveaux, qui ne se confondent pas :

1. **acceptation de l'appel Home Assistant** (aucune exception) — **ne prouve rien** ;
2. **acceptation par le backend Audi** ;
3. **succès terminal de l'action véhicule** (climatisation réellement démarrée).

Consigner, à la lumière des essais, si un statut du type **`not_confirmed` / `timeout`** est plus honnête
qu'un `rejected` — l'intégration **ne semble pas** exposer le motif d'un refus (à confirmer par E6).
**Aucun statut n'est acquis avant le terrain.**

---

## 6. Trace terrain (à remplir par l'opérateur)

| Essai | `entity_id` observés | État initial | Attributs utiles | Heure émission | Heure 1ʳᵉ transition | Résultat HA | Résultat myAudi | Constat véhicule | Niveau de preuve | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 — minimal | | | | | | | | | | |
| E1b — fin de cycle | | | | | | | | | | |
| E2 — mode economy | | | | | | | | | | |
| E3 — siège avant gauche | | | | | | | | | | |
| E4 — siège avant droit | | | | | | | | | | |
| E5 — clim à l'ouverture | | | | | | | | | | |
| E6 — état incompatible | | | | | | | | | | |

---

## 7. Décision différée

À la lumière de la trace §6, l'opérateur et l'assistant statueront sur :

- si le chantier mérite une implémentation ;
- quel périmètre fonctionnel est **réellement supporté** ;
- si un contrat de commande est justifié ;
- si une architecture transactionnelle complète est nécessaire ;
- ou si une **solution beaucoup plus simple** suffit.

**Aucune de ces décisions n'est prise avant que la trace §6 ne soit remplie.**

---

## 8. Renvois

- Chantier : [`chantier_commande_climatisation_distante.md`](chantier_commande_climatisation_distante.md).
- Contrat du domaine : [`contrats/voiture.md`](../../../contrats/voiture.md).
- Audit du domaine : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../../01_rapports/voiture/audit_domaine_audi.md).
