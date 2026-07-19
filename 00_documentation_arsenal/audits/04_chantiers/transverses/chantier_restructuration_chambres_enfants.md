# Chantier TRANSVERSE (C32) — Restructuration des chambres enfants (déménagement) : Chambre Enfants + Salle de Jeux

| Champ | Valeur |
|---|---|
| **Chantier** | Restructuration des pièces enfants suite au déménagement : la chambre d'Arnaud devient la **Chambre Enfants** (partagée), la chambre de Matthieu devient une **Salle de Jeux**, la Chambre Parents est inchangée. Passage de **3 chambres → 2 chambres + 1 salle de jeux** dans toute la logique. Dé-identification des prénoms enfants obtenue **en sous-produit**. |
| **Domaine** | TRANSVERSE (Météo/température intérieure ↔ Chauffage/vannes thermostatiques ↔ Sommeil/réveils ↔ Volets ↔ Aération ↔ UI Lovelace ↔ Doctrine de nommage ↔ Publication/confidentialité). |
| **Statut** | **ACTIF — Lot 1 livré (canon des pièces).** Lot 0 (ouverture) + Lot 1 (doctrine `nommage_entites.md` alignée sur Chambre Enfants / Salle de Jeux ; header `salle_de_jeux` créé ; `chambre_enfants` déjà présent) acquis. Décisions propriétaire A1–A3 **rendues (2026-07-19)**, consignées §Décisions. **Aucun renommage d'entité runtime** à ce stade (relève de L3). |
| **Priorité** | **P2** (proposée) — voir §Priorité. |
| **Ouvert le** | 2026-07-19. |
| **Preuve de départ** | Besoin propriétaire (déménagement physique **à venir** : enfants regroupés dans l'ex-chambre Arnaud ; ex-chambre Matthieu → salle de jeux) + **inventaire d'impact en lecture seule** consigné §3. Aucun rapport d'audit préalable mergé — l'inventaire est la preuve de départ. |
| **Prochain jalon** | **L2** — amendement contractuel du périmètre « chambres » (contrat C27 `bornes_thermiques_chambres_etage.md`, 3→2 façades). |

> **⚠️ Portée de l'ouverture.** L'ouverture de C32 **consigne les décisions propriétaire déjà rendues**
> (A1–A3, §Décisions) et l'**inventaire d'impact** (§3). Elle **ne crée aucun contrat, aucun runtime,
> aucun template, aucun dashboard, aucun helper, aucun checker.** Le renommage n'est **pas** un simple
> `sed` : une partie des occurrences relève d'un changement de logique (agrégats, besoin de chauffe,
> suivi sommeil) et non d'un renommage. Le présent dossier est **descriptif** ; les changements
> normatifs et runtime relèvent des lots suivants, sous barrière (§Barrières).

---

## Priorité (justification)

**P2 proposée.** Aucun défaut fonctionnel ni de sûreté : c'est une **restructuration** cadrée par une
décision propriétaire, pas la correction d'un incident. La **confidentialité** (disparition des prénoms
enfants du dépôt versionné — libellés, `entity_id`, chemins) est réelle mais obtenue **en sous-produit**
du renommage ; le contrôle CI dédié (S7) est traité **hors chemin critique et non bloquant** (L8). La
priorité définitive relève de l'arbitrage propriétaire.

---

## 1. Objet

Restructurer, de la **doctrine** au **runtime**, la représentation des pièces enfants après déménagement :

- **Chambre Arnaud → Chambre Enfants** (pièce conservée, désormais partagée par les deux enfants) ;
- **Chambre Matthieu → Salle de Jeux** (pièce qui **change de fonction** : elle sort de la logique
  « chambre / sommeil ») ;
- **Chambre Parents** inchangée ;
- **logique « chambres » : 3 → 2** (Enfants, Parents), la Salle de Jeux étant traitée **à part**.

Trois couches sont à gouverner, à ne pas confondre :

1. **Canon** (doctrine de nommage, définition des pièces, câblage capteur↔pièce).
2. **Renommage** des entités **de pièce** (`entity_id` + libellés + chemins), avec migration d'historique.
3. **Logique** (agrégats « chambres », besoin de chauffe, suivi sommeil par enfant, volets nuit).

---

## 2. Décisions propriétaire acquises (A1–A3, rendues 2026-07-19)

> Descriptives de la décision propriétaire ; opposables aux lots. Instruites avant l'ouverture à partir
> de l'inventaire §3.

- **A1 — Suivi sommeil / réveils (CAT-C) : fusion au niveau pièce.** Un seul jeu **« Chambre Enfants »**
  (babyphone, compteurs de réveils, recap) indexé sur la **pièce partagée**. Le suivi sommeil est
  **retiré de la Salle de Jeux** (plus d'occupant nocturne). Motif : un **capteur de bruit unique** dans
  la pièce partagée ne permet pas de distinguer physiquement quel enfant se réveille ; deux index
  nominatifs sur la même source seraient redondants. Effet secondaire : disparition des prénoms de CAT-C.

- **A2 — Salle de Jeux hors agrégats « chambres » (CAT-D).** La Salle de Jeux est **retirée** des
  agrégats chambres (`temperature_min_chambres` — qui pilote le **besoin de chauffe** nocturne —,
  `temperature_max_chambres`, `humidex_max_chambres`, `humidite_relative_max_chambres`, plateaux
  thermostatiques) et du **groupe volets nuit**. Elle conserve **sa vanne / consigne propre**, **hors
  logique sommeil**. Motif : éviter qu'une pièce non-sommeil, possiblement plus froide, déclenche à tort
  le besoin de chauffe nocturne.

- **A3 — Renommage `entity_id` avec migration d'historique (CAT-A/B).** Les `entity_id` sont renommés
  proprement (`…_chambre_arnaud → …_chambre_enfants` ; `…_chambre_matthieu → …_salle_de_jeux`) **et**
  l'historique (recorder / statistics / LTS) est **migré** côté instance pour préserver les séries des
  pièces. Motif : cohérence avec C27/C28/C29 qui viennent de durcir précisément ces agrégats chambres —
  l'historique long a de la valeur.

---

## 3. État réel synthétique — inventaire d'impact (lecture seule)

~1272 occurrences de `arnaud`/`matthieu` sur ~235 fichiers. Le nom d'entité canonique
`…_chambre_<prénom>` sert **à la fois** d'index de **pièce** (température, CO₂, volet…) **et** d'index
d'**enfant** (réveils, babyphone, présence) : cette **double fonction** rend le renommage non mécanique.
`17_zones/` **n'est pas concerné** (zones GPS `maison_securite`/`approche_securite`) — la notion de
« zone pièce » vit dans `01_customize/` + `18_lovelace/includes/section_headers/` + `02_groups/`.

| Cat. | Nature | Emplacements représentatifs | Traitement |
|---|---|---|---|
| **A** | Entités **de pièce** Arnaud → Enfants | `01_customize/meteo/*`, `01_customize/{batteries,connectivite/*}`, `13_sensor_platforms/statistics/**`, `12_template_sensors/couleurs/meteo/*`, `12_template_sensors/meteo/mesures/**`, volet/contact de pièce | Renommage `entity_id`+libellé (**L3**) + migration historique (**L6**) |
| **B** | Entités **de pièce** Matthieu → Salle de Jeux | mêmes patterns, brin `matthieu` | Renommage (**L3**) **+ sortie des agrégats/logique** (**L4**, cf. A2) |
| **C** | Entités **par enfant** | `11_automations/reveils/{babyphone,compteurs,reset}/{arnaud,matthieu}.yaml`, `03_input_numbers/reveils/compteurs.yaml`, `04_input_texts/reveils/recap.yaml`, `05_input_booleans/{babyphone/*,presence/enfants.yaml}`, `12_template_sensors/presence/enfants.yaml`, `12_template_sensors/couleurs/meteo/bruit_chambres.yaml`, `11_automations/meteo/reboot_station/{arnaud,matthieu}.yaml` | **Fusion pièce** (**L5**, cf. A1). Les entités lisent `sensor.bruit_chambre_<prénom>` (**pièce**) |
| **D** | Agrégats **énumérant/comptant les 3 chambres** | `12_template_sensors/meteo/mesures/temperature/chambres/{min,max}/**` (**besoin de chauffe**), `humidex/chambre_max.yaml`, `humidite_relative/max_chambres.yaml`, `chauffage/vannes_thermostatiques/{plateaux_stricts,affichage_plateau,stabilite_globale}.yaml`, `11_automations/chauffage/update_plateaux_thermostatiques.yaml`, `03_input_numbers/chauffage/plateau_temperature.yaml`, `06_input_selects/chauffage/piece_analyse_vanne.yaml`, `10_scripts/volets/commandes_groupees/chambres.yaml`, `12_template_sensors/statistiques/{filtres,seuils_dynamiques/**}`, `12_template_sensors/aeration/*` | **Logique** 3→2 + Salle de Jeux exclue (**L2** contrat, **L4** runtime) |
| **E** | Documentation / changelog / audits | `00_documentation_arsenal/**` (~240 occ.) | Contrats **actifs** mis à jour (**L7**) ; **changelog/audits historiques gelés** |
| **F** | Doctrine & canon des pièces | `00_documentation_arsenal/architecture/03_doctrines/nommage_entites.md`, `18_lovelace/includes/section_headers/*` (`chambre_enfants.yaml` + `salle_de_jeux.yaml`), `02_groups/integrations/{homekit,netatmo}.yaml` (câblage capteur↔pièce), `02_groups/{batteries,connectivite/*}` | Doctrine + headers **L1 (fait)** ; `02_groups` câblage → **L3** (couplé aux `entity_id`) |

**Cœur « besoin de chauffage ».** Il n'existe pas d'entité `besoin_chauffage` unique : le besoin repose
sur `sensor.temperature_min_chambres` (min des 3 chambres, défini dans
`12_template_sensors/meteo/mesures/temperature/chambres/min/valeur.yaml`) consommé par les seuils on/off
de chauffe (`12_template_sensors/climatisation/seuils_on_off/heat/*`). A2 en retire la Salle de Jeux.

---

## 4. Articulation avec C27 (dépendance normative)

C27 (**clos 2026-07-19**) vient de **contractualiser** `temperature_min_chambres` /
`temperature_max_chambres` comme bornes des **trois chambres de l'étage** dans
[`../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md`](../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md)
(périmètre souverain « 3 façades », invariants `INV-BTE-*`) et la restitution associée dans
[`restitution_chambres_etage.md`](../../contrats/meteo/temperature_interieure/restitution_chambres_etage.md).
**Réduire le périmètre à 2 chambres (Enfants, Parents) et exclure la Salle de Jeux est un amendement de
ce contrat**, pas une doctrine parallèle : le Lot 2 **amende** `bornes_thermiques_chambres_etage.md`
(3→2 façades) sans avenant empilé ni document concurrent. L'historique reste porté par Git.

---

## 5. Périmètre / Hors périmètre

**Périmètre :** canon des pièces (nommage, headers, groups) ; renommage des entités de pièce
(`entity_id`+libellé+chemins) + migration d'historique ; amendement du périmètre « chambres » (contrats
C27 + chauffage/réveils impactés) ; sortie de la Salle de Jeux des agrégats et de la logique de chauffe ;
fusion du suivi sommeil au niveau « Chambre Enfants » ; mise à jour des contrats **actifs** concernés ;
contrôle CI S7 (confidentialité prénoms) **non bloquant**.

**Hors périmètre :**
- Réécriture de l'historique factuel (`changelog/`, `audits/`) — **gelé** (Git porte la mémoire).
- Réécriture de l'historique **Git** (les prénoms passés restent dans l'historique ; S7 `--history`
  signalera — arbitrage `git filter-repo` **séparé**, non ouvert ici).
- Fonctionnement métier général Chauffage / Climatisation / Aération hors changement de périmètre.
- `17_zones/`, zones hors chambres, chaîne extérieure / jardin, RDC, petite maison.
- Toute modification runtime tant que canon (L1) et contrats (L2) ne sont pas validés.

---

## 6. Risques

- **Amendement de contrat frais (C27).** Le périmètre « 3 façades » est gravé depuis aujourd'hui : le
  réduire doit passer par un **amendement traçable** de `bornes_thermiques_chambres_etage.md`, pas un
  patch runtime silencieux.
- **Changement métier involontaire.** Retirer la Salle de Jeux de `temperature_min_chambres` modifie le
  **besoin de chauffe** : à valider par domaine (consommateurs des seuils on/off).
- **Rupture d'historique.** A3 exige une **migration** recorder/statistics/LTS ; un renommage sans
  migration coupe les séries (contraire à la décision).
- **Renommage à l'aveugle.** CAT-C/D ne sont **pas** mécaniques ; un `sed` global casserait la logique
  (double fonction pièce/enfant).
- **Divergence registre ↔ index ↔ source.** Co-commit obligatoire ; la source prime.
- **Perte de la surveillance nocturne** de l'ex-chambre Matthieu : **assumée** par A1 (pièce devenue
  salle de jeux, sans occupant nocturne).

---

## 7. Dépendances (ordre imposé)

1. **Canon (L1)** validé **avant** tout renommage runtime.
2. **Amendement contractuel (L2)** validé **avant** toute évolution de logique (L4).
3. **Renommage de pièce (L3)** avant **migration d'historique (L6)** (les nouveaux `entity_id` doivent
   exister).
4. **Logique agrégats (L4)** après L2 (contrat) **et** L3 (entités renommées).
5. **Fusion suivi enfants (L5)** après L1 (canon), indépendante de L4.
6. **S7 CI (L8)** indépendant et **non bloquant** — peut avancer en parallèle dès L0.
7. **Validation (L9)** avant **clôture (L10)**.

---

## 8. Lots

| Lot | Objet | Nature | Dépend de |
|---|---|---|---|
| **L0** | Ouverture documentaire (ce dossier + registre + index) + consignation A1–A3 | descriptif | — |
| **L1** | Canon des pièces : `nommage_entites.md` (zones), section headers (réutiliser `chambre_enfants`, créer `salle_de_jeux`) | normatif / définition | L0 |
| **L2** | Amendement contractuel du périmètre « chambres » : C27 `bornes_thermiques_chambres_etage.md` (3→2) + contrats chauffage/réveils impactés | normatif | L1 |
| **L3** | Renommage des entités **de pièce** CAT-A/B (`entity_id`+libellé+chemins) : Arnaud→Enfants, Matthieu→Salle de Jeux (customize, statistics, couleurs, mesures, volets/contacts) **+ `02_groups` câblage capteur↔pièce** (couplé au renommage des `entity_id`) | runtime | L2 |
| **L4** | Logique agrégats CAT-D : Salle de Jeux hors 5 agrégats chambres + besoin de chauffe + volets nuit + seuils/aération | runtime | L2, L3 |
| **L5** | Fusion suivi enfants CAT-C : un jeu « Chambre Enfants » (babyphone/compteurs/réveils/recap/présence) ; suivi sommeil retiré Salle de Jeux | runtime + helpers | L1 |
| **L6** | Migration d'historique HA (recorder / statistics / LTS) selon A3 | opérationnel (instance) | L3 |
| **L7** | Documentation **active** (contrats CAT-E impactés) + changelog de release ; historique gelé | descriptif | L2–L5 |
| **L8** | *(parallèle, non bloquant)* Contrôle CI **S7 — noms propres nominatifs** : script `audit_publication_git.py` + amendement contrat `securite_publication_git.md` (v1.4→v1.5) | normatif + CI | L0 |
| **L9** | Validation statique (checkers de domaine, `yamllint`, chargement HA, rendu Jinja) puis terrain | contrôle / preuve | L3–L6 |
| **L10** | Clôture documentaire (registre + index à jour) | descriptif | L9 |

---

## 9. Barrières entre lots

- **Aucune PR ne mélange** ouverture / canon / contrat / runtime / migration / clôture.
- **L3** exclu sans **L1 + L2** validés.
- **L4** exclu sans **L2** (contrat) **et L3** (entités renommées).
- **L6** (migration d'historique) exclu tant que **L3** n'est pas stable.
- **S7 (L8)** indépendant : ne bloque ni n'est bloqué par le cœur déménagement.
- **Aucune réécriture** de `changelog/` ni `audits/` (historique factuel gelé).

---

## 10. Critères de clôture (bornés)

- **Canon** à jour (doctrine `nommage_entites.md` : `Chambre Enfants` / `Salle de Jeux` / `Chambre
  Parents` ; headers ; groups capteur↔pièce).
- **Contrat C27 amendé** (périmètre 2 chambres, `INV-BTE-*` réalignés) + contrats chauffage/réveils
  impactés à jour.
- **Aucune occurrence `arnaud`/`matthieu`** dans les `entity_id`, libellés, chemins et contrats
  **actifs** (hors historique `changelog/`/`audits/` et hors historique Git).
- **Salle de Jeux** hors des 5 agrégats chambres et du besoin de chauffe ; **vanne/consigne propre**.
- **Suivi sommeil** fusionné au niveau « Chambre Enfants » ; Salle de Jeux hors surveillance nocturne.
- **Historique migré** (séries des pièces préservées) selon A3.
- **S7** implémenté et documenté (contrat v1.5), CI verte — **non bloquant pour la clôture du cœur**.
- **Validation statique** verte (checkers, `yamllint`, chargement HA, rendu Jinja) + **validation
  terrain** (besoin de chauffe nocturne piloté par 2 chambres, réveils « Chambre Enfants »).
- **Clôture documentaire** ; registre et index à jour.

---

## 11. Suivi des lots

### Lot 0 — ouverture documentaire (terminé, 2026-07-19)

Ce dossier créé ; décisions A1–A3 consignées (§2) ; inventaire d'impact consigné (§3) ; articulation
C27 posée (§4) ; entrées **registre** (§① Actifs) et **index** (§Transverses) ajoutées au **même
commit**. Aucun contrat, runtime, template, dashboard, helper ni checker. **C32 actif ; prochain jalon
L1 (canon des pièces).**

### Lot 1 — canon des pièces (terminé, 2026-07-19)

Le **vocabulaire canonique** des zones est aligné sur la cible, **avant** tout renommage runtime :

- **Doctrine `nommage_entites.md`** : liste des zones et exemples migrés `Chambre Arnaud → Chambre
  Enfants` / `Chambre Matthieu → Salle de Jeux` (`Chambre Parents` inchangée). Aucun checker n'enchaîne
  cette doctrine à des entités runtime — le canon peut donc précéder le renommage sans faux positif CI.
- **Section headers** : header `salle_de_jeux.yaml` créé (`🧸 Salle de jeux`) ; header
  `chambre_enfants.yaml` **déjà présent** (`🛏️ Chambre enfants`, référencé par
  `dashboards/ouvertures/principal.yaml` — migration réellement amorcée côté ouvertures). Les headers
  `chambre_arnaud`/`chambre_matthieu` **subsistent** (encore référencés par des dashboards) ; leur
  retrait relève de **L3/L4**.

**Raffinement de périmètre** : le câblage capteur↔pièce de `02_groups` (listes d'`entity_id`) est
**couplé au renommage des `entity_id`** ; il est déplacé de L1 vers **L3** pour éviter des références
pendantes. Décision purement documentaire, sans effet sur A1–A3.

**Aucun `entity_id` renommé, aucun agrégat modifié, aucun contrat touché.** `check_lovelace_section_headers`
+ `docs_lint` verts. **C32 actif ; prochain jalon L2 (amendement contractuel C27).**
