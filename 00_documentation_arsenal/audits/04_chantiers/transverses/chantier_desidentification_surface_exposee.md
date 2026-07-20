# Chantier TRANSVERSE (C33) — Dé-identification de la surface exposée (adultes) + durcissement du verrou de publication

| Champ | Valeur |
|---|---|
| **Chantier** | Retirer les **prénoms adultes** (`antoine`, `valentin`, `constance`) de la **surface exposée** du dépôt public : runtime, libellés UI, contrats actifs. Canon retenu : **`parent_1` / `parent_2`**. Solde des annotations transitoires « ex-… » héritées de C32. Extension du verrou CI **S7** aux prénoms adultes. **Le résidu historique Git est assumé et non traité** (voir D1). |
| **Domaine** | TRANSVERSE (Présence ↔ Sécurité/Alarme ↔ Notifications mobiles ↔ BSSID/Wi-Fi ↔ UI Lovelace ↔ Doctrine de nommage ↔ Publication/confidentialité). |
| **Statut** | **OUVERT (2026-07-20) — ouverture documentaire.** Aucun runtime, contrat, template, dashboard, helper ni checker modifié par le présent lot. |
| **Priorité** | **P2** (proposée) — voir §Priorité. |
| **Ouvert le** | 2026-07-20. |
| **Preuve de départ** | Décision propriétaire (le dépôt **reste public**, sa surface exposée doit être assainie) + **inventaire d'impact en lecture seule** §3 + rapport `audit_publication_git.py` du 2026-07-20 (0 `CRITICAL`, 3 `WARNING` S7 en documentation active) + **constat d'exposition** : dépôt public depuis le 2026-05-23, **fork tiers** (`kloggy`, 2026-06-08), star tierce (`aruesberg`). |
| **Prochain jalon** | **L1 — canon des personnes** (doctrine de nommage `parent_1` / `parent_2`). |

> **⚠️ Portée de l'ouverture.** Le présent dossier est **descriptif**. Il consigne la décision
> propriétaire (§2) et l'inventaire (§3). Il **ne crée aucun contrat, aucun runtime, aucun template,
> aucun dashboard, aucun helper, aucun checker.** Le renommage n'est **pas** un `sed` : la chaîne
> présence alimente la **décision d'alarme** et les **notifications mobiles**, et le changement d'un
> `unique_id` détruit la mémoire d'un capteur (leçon C32/L6b–L6c). Les changements normatifs et runtime
> relèvent des lots suivants, sous barrière (§9).

---

## Priorité (justification)

**P2 proposée.** Aucun défaut fonctionnel ni de sûreté : le système fonctionne. L'objet est la
**confidentialité de la surface exposée** d'un dépôt public. À la différence de C32 — où la
dé-identification était obtenue **en sous-produit** d'une restructuration fonctionnelle — elle est ici
l'**objet principal**, sans contrepartie fonctionnelle. Le chantier touche en revanche une chaîne
**sensible** (présence → alarme), ce qui interdit de le traiter comme cosmétique. La priorité définitive
relève de l'arbitrage propriétaire.

---

## 1. Objet

Assainir la **surface exposée** — c'est-à-dire l'**état courant** du dépôt public, ce que lit aujourd'hui
un visiteur — de toute désignation nominative de personne.

Trois couches, à ne pas confondre :

1. **Canon** (doctrine de nommage des personnes : quelle désignation neutre, stable, distinctive).
2. **Renommage** des entités de personne (`entity_id` + libellés + références), avec migration
   d'historique.
3. **Verrou** (contrôle CI d'anti-retour, sans lequel l'assainissement n'est que ponctuel).

---

## 2. Décisions propriétaire acquises (D1–D4, rendues 2026-07-20)

> Descriptives de la décision propriétaire ; opposables aux lots.

- **D1 — Le dépôt reste PUBLIC ; le résidu historique est assumé et non traité.** Aucun
  `git filter-repo`, aucun force-push, aucune réécriture d'historique. **Motif** : la réécriture
  casserait les **1440 SHA** et, avec eux, tout l'appareil de traçabilité du dépôt (liens
  `Claude-Session`, renvois inter-documents, citations de commits dans les audits) — pour un bénéfice
  **partiel par construction** : le fork tiers du 2026-06-08 contient déjà les prénoms enfants et
  échappe à toute réécriture, de même que les objets GitHub adressables par SHA et tout clone réalisé
  depuis mai. **La dé-identification porte donc sur l'état courant et l'avenir, pas sur le passé
  publié.** Cette décision **confirme et étend** l'arbitrage déjà inscrit au script S7 (« leur purge
  relève d'un `git filter-repo`, hors état courant »).
- **D2 — Canon adultes : `parent_1` / `parent_2`.** Cohérent avec le canon maison existant
  (`chambre_parents`, `sdb_parents`, `presence_enfants`). Corrige **au passage** l'incohérence
  actuelle : `person.valentin` désigne le téléphone d'**Antoine** (patronyme pour l'un, prénom pour
  l'autre).
- **D3 — Périmètre : A + B + C** (runtime adultes, solde des annotations « ex-… », extension du verrou
  S7). **Hors périmètre** : entités issues d'intégrations et d'appareils (hostname NAS `valentin`,
  intégration `linky_antoine_fork` — **34 entités live non référencées par le dépôt**), compte et URL
  GitHub. Voir §5.
- **D4 — L'identité Git de l'auteur est maintenue.** `user.name` et `user.email` restent renseignés en
  identité réelle ; aucune bascule vers l'adresse `noreply` GitHub. **Motif** : la dé-identification a
  pour objet les **personnes du foyer** désignées par le système — dont des mineurs, qui n'ont pas
  consenti à figurer dans un dépôt public — et **non l'attribution de l'auteur sur son propre travail**.
  Un dépôt public revendiqué engage son auteur ; l'anonymiser affaiblirait la traçabilité sans protéger
  qui que ce soit d'autre. **La frontière du chantier est donc : sujets du système = dé-identifiés ;
  auteur du système = assumé.**

---

## 3. État réel synthétique — inventaire d'impact (lecture seule)

**Occurrences dans le dépôt** (`\b(antoine|valentin|constance)\b`) : `constance` 54 (dont 27 runtime),
`valentin` 35 (19), `antoine` 40 (17).

**Entités définies par le dépôt** — périmètre du renommage :

| Domaine | Entités | Fichiers porteurs |
|---|---|---|
| `person` | `valentin` *(= Antoine)*, `constance` | référencées seulement (storage-managed, voir R3) |
| `input_text` | `telephone_{antoine,constance}` + suffixes `_notify`, `_tracker`, `_wifi_bssid` (8) | `11_automations/system/telephones_synchro_helpers.yaml`, `presence/high_accuracy_on.yaml` |
| `sensor` | `telephone_{antoine,constance}_bssid_dynamic` | `12_template_sensors/system/bssid/nouveau.yaml` |
| `binary_sensor` | `approche_securite_{antoine,constance}` | `12_template_sensors/presence/securite/approche.yaml` |
| Libellés UI | « 👤 Présence Antoine », « Téléphone Constance », « 💤 Antoine » | `18_lovelace/dashboards/{sommeil/principal,systeme/telephones}.yaml` |

**15 fichiers porteurs** :

| Emplacement | Occ. | Fichiers |
|---|---|---|
| `11_automations` | 28 | `presence/{high_accuracy_on,notification_presence}.yaml` · `system/{bssid_wifi,telephones_synchro_helpers}.yaml` · `system/release_diff/notification.yaml` |
| `12_template_sensors` | 24 | `presence/{famille,securite/approche,securite/presence}.yaml` · `system/bssid/nouveau.yaml` |
| `04_input_texts` | 8 | `system/telephones.yaml` — **définitions** des helpers |
| `scripts/arsenal_contracts` | 6 | `check_bssid_contracts.py` — **checker CI** |
| `18_lovelace` | 4 | `dashboards/{sommeil/principal,systeme/telephones}.yaml` |
| `10_scripts` | 3 | `system/notifications_mobiles.yaml` · `chauffage/REVUE_CLOTURE_CH2.md` |
| `LICENSE` | 1 | `Copyright (c) 2026 …` — **hors périmètre (D4)** |

> **⚠️ Correction d'inventaire (2026-07-20).** Le relevé initial du Lot 0 annonçait **11 fichiers**. Il
> était **incomplet** : le balayage ne couvrait que `05_`, `11_`–`14_`, `18_`, `19_`, et omettait
> `01_`–`10_`, `15_`–`17_`, `scripts/` et la racine. Trois manques **matériels** en découlaient :
> **(a)** `04_input_texts/system/telephones.yaml` porte les **définitions** des 8 helpers — sans lui, le
> renommage des références aurait pointé dans le vide ; **(b)** `scripts/arsenal_contracts/check_bssid_contracts.py`
> **code les noms d'entités en dur** — renommer le runtime sans le checker **casse la CI** ;
> **(c)** `LICENSE` porte le copyright de l'auteur, **hors périmètre par D4**. Périmètre corrigé :
> **11 → 15 fichiers** (dont 1 exclu).

**Documentation active porteuse** (hors historique gelé) : `contrats/arrosage/18_notification_batterie.md`
(2 occurrences « Antoine ») + les **3 annotations transitoires C32** (`contrats/climatisation/13_intensite_besoin_froid.md`,
`contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md`) — seuls `WARNING` S7 restants.

**Hors périmètre, pour mémoire** : 34 entités live `nas_valentin_*` (hostname Synology) et
`linky_antoine_fork_*` (entrée d'intégration). **Aucune n'est référencée par le dépôt** — elles ne
participent donc pas à la surface exposée.

---

## 4. Articulation avec C32 (héritage direct)

C33 **solde** ce que C32 laisse ouvert côté confidentialité :

- C32 a dé-identifié les **enfants** ; C33 traite les **adultes**, non couverts.
- C32/L8 a créé le verrou S7 sur `(arnaud|matthieu)` ; C33 l'**étend** aux adultes (même gradation).
- C32 a introduit des annotations « ex-… » **transitoires** en documentation active ; C33 les **solde**
  à la clôture de C32.

**Deux leçons techniques de C32 sont opposables à C33** (§6, R2) : le changement d'un `unique_id` crée
une entité **neuve** (L6b : boucle fermée non auto-réparable sur les attributs ; L6c : fenêtre aveugle
de ≤ 24 h sur les filtres de période).

---

## 5. Périmètre / Hors périmètre

**Dans le périmètre** — A : runtime adultes (11 fichiers, ~20 entités) · B : solde des annotations
« ex-… » + occurrences « Antoine » en documentation active · C : extension du verrou S7.

**Hors périmètre, explicitement** :

- **Historique Git** (1440 commits) — D1.
- **Fork tiers et copies déjà diffusées** — hors de tout contrôle technique. Traitement possible
  **relationnel** (demande de suppression au propriétaire du fork), non traité ici.
- **Compte et URL GitHub** (`antoinevalentinHA/arsenal`) — le renommage casserait tous les liens
  existants ; arbitrage séparé.
- **Hostname NAS `valentin`, intégration `linky_antoine_fork`** — opérations appareil/intégration, hors
  dépôt, avec risque de rupture d'historiques longs.
- **Identité Git des commits** — maintenue (D4).

---

## 6. Risques

- **R1 — Chaîne de sécurité.** `person.*` alimente `binary_sensor.presence_famille_securite`, donc la
  **décision d'alarme** (`PRESENCE → DISARMED`). Un renommage incomplet peut **armer ou désarmer à
  tort**. ⇒ barrière de validation dédiée (L6), aucune clôture sans preuve terrain.
- **R2 — Perte de mémoire au changement d'`unique_id`** (leçon C32/L6b–L6c). ⇒ procédure imposée :
  **renommer d'abord l'`entity_id` dans le registre HA** (migre l'historique), **puis** aligner le YAML.
  Jamais le YAML seul.
- **R3 — `person.*` est storage-managed.** Ces entités ne sont **pas définies en YAML** : le dépôt ne
  fait que les référencer. Le renommage est une opération **d'instance** (UI/registre) ; le lot runtime
  ne peut que suivre. ⇒ ordre imposé (§7).
- **R4 — Notifications mobiles.** `input_text.telephone_*_notify` porte le **service de notification**
  de l'app mobile HA. Un renommage désaligné coupe silencieusement les notifications (pas d'erreur, pas
  d'entité indisponible). ⇒ validation par réception effective (L6).
- **R5 — Perte de trace de migration.** Supprimer les annotations « ex-… » retire des contrats le
  pointeur vers l'ancien nommage. **Mitigation** : la trace demeure dans C32, dans le changelog et dans
  l'historique Git — c'est-à-dire aux emplacements dont c'est le rôle.

---

## 7. Dépendances (ordre imposé)

`L1 (canon)` → `L2 (runtime)` → `L3 (docs actives)` → `L5 (migration instance)` → `L4 (verrou S7 durci)` → `L6 (validation)` → `L7 (clôture)`.

**Le verrou S7 durci est mergé en dernier** — précédent **C32/L8** : le contrôle `CRITICAL` en runtime
n'est introduit qu'**une fois le runtime propre**, faute de quoi la CI casse pendant le chantier.

**R3 impose** que le renommage d'instance (L5) précède l'activation du verrou : tant que
`person.valentin` existe côté instance, le dépôt doit pouvoir le référencer.

---

## 8. Lots

| Lot | Objet | Portée |
|---|---|---|
| **L0** | Ouverture documentaire (ce document) | doc |
| **L1** | Canon des personnes : `parent_1` / `parent_2` inscrit à la doctrine de nommage | doc normatif |
| **L2** | Renommage runtime adultes — 11 fichiers, **behavior-preserving** | runtime |
| **L3** | Solde des annotations « ex-… » C32 + occurrences « Antoine » en documentation active | doc |
| **L4** | Verrou S7 étendu aux adultes (`CRITICAL` runtime / `WARNING` doc active / exempt historique gelé) + contrat `securite_publication_git.md` | script + contrat |
| **L5** | Migration instance : `entity_id` renommés au registre HA (historique préservé) | instance |
| **L6** | Validation terrain : chaîne alarme + réception des notifications sur les deux téléphones | terrain |
| **L7** | Clôture | doc |

---

## 9. Barrières entre lots

- **Aucune PR ne mélange** canon (L1), runtime (L2), documentation (L3) et verrou (L4).
- **L4 n'est pas mergé avant que L2 + L5 soient acquis** (§7).
- **L7 n'est pas prononcé sans L6** : R1 et R4 sont des défaillances **silencieuses**, aucune preuve
  statique ne les couvre.

---

## 10. Critères de clôture (bornés)

1. `audit_publication_git.py` : **0 `CRITICAL`** et **0 `WARNING` S7** (enfants **et** adultes) hors
   historique gelé.
2. **0 occurrence** de `\b(antoine|valentin|constance)\b` dans `05_`, `11_`, `12_`, `13_`, `14_`, `18_`,
   `19_`.
3. **0 entité live** portant un prénom, **hors** entités d'intégration listées hors périmètre (§5).
4. **R1 levé** : `presence_famille_securite` réagit correctement aux deux personnes (preuve terrain).
5. **R4 levé** : notification effectivement **reçue** sur les deux téléphones (preuve terrain).

---

## 11. Suivi des lots

### Lot 0 — ouverture documentaire (terminé, 2026-07-20)

Décisions D1–D4 consignées. Inventaire §3 établi par relevé croisé dépôt (`Select-String`
sur `05_`–`19_`) et instance (`hass.states`, 54 entités portant un prénom, dont 34 hors périmètre).
Constat d'exposition établi par `gh repo view` / `gh api .../forks`. **Aucun runtime, contrat, template,
dashboard, helper ni checker créé ou modifié.**
