# ✅ ARSENAL — CLÔTURE DE CHANTIER (CONDITIONNELLE)

## Voiture (C25) — Commande de climatisation distante Audi

| Champ | Valeur |
|---|---|
| **Type** | Clôture **conditionnelle** — construction complète livrée + **nominal validé en terrain**, réserve **E6** (discriminant d'échec). |
| **Domaine** | Voiture — Audi A3 Sportback e-tron PHEV (API level 0), intégration custom `audiconnect`. |
| **Statut** | ✅ **CLÔTURE CONDITIONNELLE ACQUISE (2026-07-21).** Faisabilité démontrée, contrat amendé, runtime + UI livrés et **validés end-to-end en nominal** (bouton → `Confirmée`). **Reste E6** (échec véhicule non branché) pour lever la dernière réserve et retirer l'outil d'observation temporaire. |
| **Version** | 1.0 |
| **Date** | 2026-07-21 |
| **Chantier** | [C25 — Climatisation distante Audi](../../04_chantiers/voiture/chantier_commande_climatisation_distante.md) |
| **Cadrage** | [`cadrage_commande_climatisation_distante.md`](../../02_conception/voiture/cadrage_commande_climatisation_distante.md) (D1–D8) |
| **Protocole terrain** | [`protocole_caracterisation_terrain_climatisation_distante.md`](../../04_chantiers/voiture/protocole_caracterisation_terrain_climatisation_distante.md) (§6) |
| **Contrat** | [`contrats/voiture.md`](../../../contrats/voiture.md) — amendement **A1** (COUCHE ACTION) |

---

## 1. Objet

Clore le chantier C25, ouvert le 2026-07-17 comme **caractérisation de faisabilité** de la commande de
climatisation stationnaire distante de l'Audi. La feuille de route **doc chantier → cadrage contractuel →
runtime → UI → clôture** a été déroulée **dans l'ordre**. Cette clôture est **conditionnelle** : tout est
livré et le **cas nominal est validé en conditions réelles**, mais l'essai **E6** (comportement en échec)
reste à consigner pour qualifier pleinement le détecteur.

## 2. Ce qui est acquis

- **Faisabilité (2026-07-21)** : succès terminal démontré (HA `climatisation_state=cooling` + myAudi
  « Actif » + corroboration physique), après un premier essai en `fail_vehicle_timeout` (intermittence
  backend confirmée). *(§6, reprise E1.)*
- **Frontière observationnelle franchie et bornée** : contrat `voiture.md` amendé **A1** — une **seule**
  surface de pilotage, **manuelle**, sans décision automatique ; invariants **INV-CMD-1…7**.
- **Runtime honnête** : `script.audi_climatisation_distante` (single-shot) — appel `start_climate_control`
  (ciblage portable `device_id(nom)`, booléens forcés `false`), **observation terminale** de
  `climatisation_state`, restitution `input_select.audi_climatisation_commande_etat`
  (`Au repos`/`En cours`/`Confirmée`/`Non confirmée (timeout)`).
- **UI compacte** (arbitrage propriétaire) : `dashboards/voiture/audi.yaml`, bouton confirmé + état, sans
  logique métier (INV-CMD-7). Réglages temp/mode = défauts du script (non exposés).
- **Chaîne de détection vérifiée au code** : `climatisation_state` = valeur brute véhicule (endpoint
  `climater`/MBB, `audi_connect_account.py:906-908`) ; refresh post-action dans un `finally` (`:451-453`),
  `update_sleep` 5 s (`const.py:28`) ⇒ témoin fiable en succès **et** échec.
- **Validation end-to-end NOMINALE (2026-07-21, ~15:54)** : bouton Arsenal → **`Confirmée`** (le script a
  observé une transition réelle de `climatisation_state`). *(§6.)*

## 3. Réserve — condition de levée

- **E6 — comportement en échec (non fait)** : exécuter la commande en état **naturellement incompatible**
  (véhicule non branché) et vérifier que `climatisation_state` **reste inchangé** ⇒ pas de faux
  « Confirmée ». Si l'état bougeait aussi, basculer le témoin sur `remaining_climatisation_time`.
- **Fines (facultatif)** : valeur littérale de `climatisation_state` et latence exacte, via
  `script.audi_climatisation_observation`.
- **Outil d'observation conservé** jusqu'à la levée de la réserve, puis **à retirer** (il est temporaire).

## 4. Décisions différées (hors périmètre C25)

- **`economy`** : non prouvé (essai E2), non exposé en UI ; à confirmer avant offre pleine.
- **Options** sièges / vitrage / clim-à-l'ouverture (E3–E5) : hors périmètre, forcées `false`.
- **Déclenchement automatique** (préconditionnement) : chantier distinct éventuel.
- **Dashboard Réglages voiture** : à créer seulement si le besoin d'exposer temp/mode se confirme.

## 5. Suite

Dérouler **E6** (opérateur), consigner le résultat au §6, puis **clôture définitive** : lever la réserve,
retirer `script.audi_climatisation_observation`, et sortir C25 des Actifs vers « Clos récent ».

---

## 6. Renvois

- Chantier : [`chantier_commande_climatisation_distante.md`](../../04_chantiers/voiture/chantier_commande_climatisation_distante.md)
- Cadrage : [`cadrage_commande_climatisation_distante.md`](../../02_conception/voiture/cadrage_commande_climatisation_distante.md)
- Protocole terrain : [`protocole_caracterisation_terrain_climatisation_distante.md`](../../04_chantiers/voiture/protocole_caracterisation_terrain_climatisation_distante.md)
- Contrat : [`contrats/voiture.md`](../../../contrats/voiture.md) (amendement A1)
- Audit du domaine : [`audit_domaine_audi.md`](../../01_rapports/voiture/audit_domaine_audi.md)
