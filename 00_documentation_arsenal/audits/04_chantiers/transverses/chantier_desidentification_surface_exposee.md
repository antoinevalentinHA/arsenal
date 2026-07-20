# Chantier TRANSVERSE (C33) — Dé-identification de la surface exposée (adultes) + durcissement du verrou de publication

| Champ | Valeur |
|---|---|
| **Chantier** | Retirer les **prénoms adultes** (`antoine`, `valentin`, `constance`) de la **surface exposée** du dépôt public : runtime, libellés UI, contrats actifs. Canon retenu : **`parent_1` / `parent_2`**. Solde des annotations transitoires « ex-… » héritées de C32. Extension du verrou CI **S7** aux prénoms adultes. **Le résidu historique Git est assumé et non traité** (voir D1). |
| **Domaine** | TRANSVERSE (Présence ↔ Sécurité/Alarme ↔ Notifications mobiles ↔ BSSID/Wi-Fi ↔ UI Lovelace ↔ Doctrine de nommage ↔ Publication/confidentialité). |
| **Statut** | **ACTIF (2026-07-20) — L0 à L5 livrés ; L6 (validation terrain) partiel.** Runtime dé-identifié (L2 + correctif L2b), documentation active soldée (L2c, L3a, L3c), instance migrée (L5), verrou S7 étendu aux adultes (L4, mergé en dernier). **R4 levé** (notification reçue et confirmée) ; **R1 partiel** — le relâchement de la chaîne présence → sécurité a été observé, pas son établissement. |
| **Priorité** | **P2** (proposée) — voir §Priorité. |
| **Ouvert le** | 2026-07-20. |
| **Preuve de départ** | Décision propriétaire (le dépôt **reste public**, sa surface exposée doit être assainie) + **inventaire d'impact en lecture seule** §3 + rapport `audit_publication_git.py` du 2026-07-20 (0 `CRITICAL`, 3 `WARNING` S7 en documentation active) + **constat d'exposition** : dépôt public depuis le 2026-05-23, **fork tiers** (`kloggy`, 2026-06-08), star tierce (`aruesberg`). |
| **Prochain jalon** | **L6 — clôture de la validation terrain.** Reste à observer une transition de présence **entrante** (`not_home → Maison securite`) confirmant la chaîne présence → alarme dans le sens de l'établissement. **Aucune panne fabriquée** : attendre une occurrence naturelle. Puis **L7** (clôture). |

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
  intégration `linky_antoine_fork`), compte et URL GitHub. Voir §5.

  > **⚠️ Justification corrigée (2026-07-20) — la conclusion tient, sa motivation était fausse.**
  > D3 s'appuyait initialement sur « **34 entités live non référencées par le dépôt** ». C'est
  > **inexact**, et pour la même cause que L2b : le motif d'inventaire à frontières de mot masquait les
  > formes encapsulées. Le balayage corrigé montre que ces entités **sont largement référencées** —
  > `18_lovelace/dashboards/systeme/nas.yaml` (26 occurrences), `02_groups/integrations/synology.yaml`
  > (18), `12_template_sensors/system/cartes_dashboard_navigation/nas.yaml` (3), et d'autres. Elles
  > **font donc bien partie de la surface exposée**.
  >
  > **La conclusion reste néanmoins valide, sur un autre fondement.** Ces entités ne portent que
  > `valentin` (patronyme) et `antoine` (prénom) — c'est-à-dire **le nom de l'auteur, et lui seul**.
  > **Aucune** ne porte le prénom d'un autre membre du foyer (vérifié : 39 entités `nas_valentin*`,
  > 1 `linky_antoine*`, 0 autre). Elles relèvent donc de **D4** — *auteur assumé* — et non du périmètre
  > de dé-identification des **sujets**. Le nom de l'auteur est de toute façon déjà public par l'URL du
  > dépôt et le `LICENSE`.
  >
  > **Conséquence** : hors périmètre **par D4**, non « parce que non référencées ». Si D4 venait à être
  > révisé, ces entités **rentreraient** dans le périmètre — et le coût serait élevé (renommage du
  > hostname Synology, réinitialisation des historiques longs de 39 entités).
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
2. Recherche `antoine|valentin|constance` — **sans frontières de mot** — sur `01_` à `19_`, `scripts/`
   et la racine : le résultat doit être **exactement** la liste d'exclusions ci-dessous, **ni plus, ni
   moins**.

   | Exclusion attendue | Fondement |
   |---|---|
   | `nas_valentin*` (39 entités), `linky_antoine*` (1) | D3 — nom de l'**auteur**, relève de D4 |
   | `LICENSE:3` — `Copyright (c) 2026 …` | D4 |
   | `10_scripts/chauffage/REVUE_CLOTURE_CH2.md:5` — URL du dépôt | D3 (compte/URL hors périmètre) |
   | `10_scripts/chauffage/REVUE_CLOTURE_CH2.md:145` — signature d'opérateur | D4 — auteur validant sa propre procédure |

   *Formulation en liste positive et non en « 0 occurrence » : un compteur nul se satisfait aussi d'un
   motif qui ne matche rien — c'est précisément le défaut qui a produit L2b.*
3. **0 entité live** portant un prénom, **hors** entités d'intégration listées hors périmètre (§5).
4. **R1 levé** : `presence_famille_securite` réagit correctement aux deux personnes (preuve terrain).
5. **R4 levé** : notification effectivement **reçue** sur le téléphone `parent_1` (preuve terrain).

> **⚠️ Correction du critère 2 (2026-07-20).** Sa rédaction initiale — `\b(antoine|valentin|constance)\b`,
> restreinte à `05_`, `11_`–`14_`, `18_`, `19_` — était **intestable** : dans `telephone_antoine_notify`
> le prénom est encadré d'**underscores**, caractères de mot, donc **sans frontière `\b`** ; le motif ne
> matche pas. Ce critère aurait été déclaré **satisfait** alors que **50 fichiers** portaient encore
> l'ancien nommage et que les notifications étaient rompues (L2b). Le critère est réécrit **sans
> frontières de mot** et sur le **périmètre complet du dépôt**. *Leçon opposable : un critère de clôture
> qui repose sur un motif de recherche doit être éprouvé sur un cas connu positif avant d'être opposé.*
>
> **Correction du critère 5** : « les deux téléphones » était **factuellement faux**. Le comptage des
> cibles donne **62** références à `telephone_parent_1_notify` (toute la couche d'alerte) contre **1** à
> `telephone_parent_2_notify` — et cette unique référence est un **canal de commande**
> (`script.mobile_high_accuracy_off`, pilotage du GPS), **jamais une notification à lire**. Un seul
> téléphone reçoit des alertes.

---

## 11. Suivi des lots

### Lot 0 — ouverture documentaire (terminé, 2026-07-20)

Décisions D1–D4 consignées. Inventaire §3 établi par relevé croisé dépôt (`Select-String`
sur `05_`–`19_`) et instance (`hass.states`, 54 entités portant un prénom, dont 34 hors périmètre).
Constat d'exposition établi par `gh repo view` / `gh api .../forks`. **Aucun runtime, contrat, template,
dashboard, helper ni checker créé ou modifié.**

> ⚠️ **L'inventaire de ce lot était faux** — motif à frontières de mot, périmètre de balayage partiel.
> Corrigé en deux temps : **11 → 15 fichiers** (encart §3), puis **15 → 65 fichiers** (L2b). Voir L2b.

### Lot 1 — canon des personnes (terminé, 2026-07-20, #461)

Section **PERSONNES** ajoutée à `architecture/03_doctrines/nommage_entites.md`, absente jusqu'ici : la
doctrine ne gouvernait que les **ZONES** (lieux), aucune règle ne portait sur les entités désignant un
**SUJET** — d'où la dérive constatée (prénoms en clair, `person.valentin` désignant le téléphone d'un
autre). Canon `parent_1` / `parent_2` (individuel, index **stable et opaque**) et `enfants`
(**collectif**, conséquence physique de C32/A1). Règle capitale : **la correspondance index → personne
n'est pas documentée dans le dépôt** — un canon non nominatif publié avec sa table de correspondance ne
dé-identifie rien. **Aucun checker n'ancre cette doctrine au runtime** (vide déjà consigné au
`REGISTRE_COUVERTURE_VERIFICATION`) : le canon pouvait précéder le renommage sans faux positif CI —
corollaire assumé, **rien ne signale une divergence canon/runtime**.

### Lot 2 — dé-identification runtime, première passe (terminé, 2026-07-20, #461)

15 fichiers. `person.*`, `input_text.telephone_*` (définitions + 3 suffixes), `sensor.*_bssid_dynamic`,
`binary_sensor.approche_securite_*`, `id:` de trigger, littéraux Jinja, `notification_id`, libellés UI.
Accord grammatical **neutralisé** (« est présente » → « est présent ») : l'accord suivait le prénom et
reconduisait un marqueur de genre. **Incomplet — voir L2b.**

### Lot 2b — 50 fichiers manqués (correctif urgent, terminé, 2026-07-20, #462)

**Défaut de production.** Le L2 déployé a renommé les **définitions** des `input_text` sans renommer les
**50 fichiers qui les consomment** : **toutes les notifications mobiles du système ont cessé**, sans
erreur ni entité indisponible — R4 réalisé exactement comme il était décrit.

**Cause racine — motif d'inventaire défaillant.** Le balayage utilisait
`\b(antoine|valentin|constance)\b`. Dans `telephone_antoine_notify`, le prénom est encadré
d'**underscores**, qui sont des **caractères de mot** : il n'existe donc **aucune frontière `\b`** et le
motif **ne matche pas**. Seuls les fichiers contenant *par ailleurs* un « Antoine » isolé ont été vus ;
ceux ne portant que des formes encapsulées sont restés **invisibles** — dont
`12_template_sensors/system/bssid/telephones_dynamiques.yaml`, qui **définit** les deux capteurs
`*_bssid_dynamic`, absents du runtime depuis L2.

**Portée** : ~70 occurrences dans 50 fichiers, dominées par `cible:
input_text.telephone_parent_1_notify` — **62 références**, soit la quasi-totalité de la couche d'alerte
(alarme, arrosage, ECS, panne secteur, coupure internet, Zigbee, électroménager, météo, cumulus, santé,
voiture). Également `presence/securite/wifi.yaml` (variables Jinja) et `notification_id:
presence_valentin`.

**Leçon opposable** : les vérifications post-déploiement affichaient `automations_ko: 0` et une chaîne
de présence saine — **aucun indicateur ne signale une notification qui ne part pas**. Une couche dont la
défaillance est silencieuse ne peut être validée que par **preuve de réception**, jamais par absence
d'erreur.

### Lot 2c — solde documentaire des dettes de L2b (terminé, 2026-07-20, #463)

Les deux dettes ouvertes par le défaut d'inventaire de L2b sont soldées, dans le dossier lui-même :

- **Critère de clôture 2 — était intestable.** Rédigé `\b(antoine|valentin|constance)\b` sur un périmètre
  partiel, il aurait été déclaré **satisfait** alors que 50 fichiers portaient encore l'ancien nommage et
  que les notifications étaient rompues. Réécrit **sans frontières de mot**, sur le dépôt complet, et
  surtout en **liste positive d'exclusions attendues** plutôt qu'en « 0 occurrence » : un compteur nul se
  satisfait aussi d'un motif qui ne matche rien — précisément le défaut à l'origine de L2b.
- **Critère de clôture 5 — était factuellement faux.** Il exigeait la réception « sur les deux
  téléphones ». Le comptage donne **62** références à `telephone_parent_1_notify` contre **1** à
  `telephone_parent_2_notify`, et cette unique référence est un **canal de commande**
  (`script.mobile_high_accuracy_off`), jamais une notification à lire.
- **Justification de D3 corrigée** : la conclusion tient, sa motivation était fausse (voir l'encart §2).

**Leçon opposable** : un critère de clôture qui repose sur un motif de recherche doit être **éprouvé sur
un cas connu positif** avant d'être opposé.

### Lot 3a — réparation des références mortes (terminé, 2026-07-20, #464)

**25 références mortes** introduites par L2/L2b dans la documentation active : les contrats et documents
d'architecture continuaient de citer les anciens `entity_id` (`telephone_antoine_*`,
`sensor.telephone_constance_bssid_dynamic`…) alors que le runtime portait déjà le canon
`parent_1`/`parent_2`. Cinq fichiers réalignés — `architecture/notifications_mobiles.md`,
`contrats/bssid.md`, `contrats/arrosage/18_notification_batterie.md`, `contrats/electromenager.md`,
`contrats/reveils.md`.

### Lot 3c — solde des annotations transitoires « ex-… » de C32 (terminé, 2026-07-20, #465)

Retrait des **7 dernières annotations** « ex-Chambre Matthieu » / « ex-chambre_arnaud » des 2 contrats
actifs (`bornes_thermiques_chambres_etage.md`, `climatisation/13_intensite_besoin_froid.md`). Elles ont
servi la migration C32 ; le canon étant établi, elles n'ont plus d'objet — c'est le **périmètre B** de D3.

**Effet mesuré** : `audit_publication_git.py` ne remonte plus **aucun** signal S7 (678 → 675 `WARNING`,
soit exactement les 3 occurrences détectées). C'était le dernier résidu de prénom d'enfant en
documentation active ; le reste est en **historique gelé** (`changelog/`, `audits/`), exempté par D1.

**Traçabilité (mitigation R5)** : la correspondance ancien/nouveau nommage demeure dans le dossier C32,
le changelog et l'historique Git — aux emplacements dont c'est le rôle, et non dans un contrat normatif.

### Lot 5 — migration instance (terminé, 2026-07-20)

Exécuté sur l'instance, dans l'ordre imposé par R2/R3/R4 :

1. **Capture** préalable des 8 valeurs d'`input_text` (hors dépôt — elles portent la correspondance
   index → personne).
2. **Registre HA** : `person.valentin` → `person.parent_1`, `person.constance` → `person.parent_2` via
   `config/entity_registry/update`, **`entity_id` seul, libellés conservés** — le dépôt voit
   `parent_1`, l'instance affiche le prénom. C'est la frontière prévue au canon L1.
3. **Déploiement** (`git pull` dans `/config`) + `ha core check` **successful** + reload ciblé
   (`input_text`, `automation`, `template`, `script`).
4. **Restauration** des 8 valeurs par `input_text.set_value`.
5. **Purge de 4 entités orphelines** (`sensor.telephone_*_bssid_dynamic`,
   `binary_sensor.approche_securite_*` en ancien nommage) — résidu de `unique_id` renommé, même
   phénomène qu'en C32.

**Confirmation de R3** : pour un `input_text` défini en YAML, l'identité **est la clé** ; le renommage
au registre **ne préserve pas** l'état, d'où les étapes 1 et 4. Pour `person.*` (storage-managed), le
renommage au registre **préserve** l'historique.

### Lot 4 — verrou S7 étendu aux adultes (terminé, 2026-07-20, #466)

Extension du contrôle **S7** créé par C32/L8 : aux prénoms enfants s'ajoutent les **adultes**, avec la
**frontière sujets / auteur** posée par D4.

- **Sujets** (`arnaud`, `matthieu`, `constance`) : sans exclusion.
- **Auteur** (`antoine`, `valentin`) : neutralisation des usages légitimes — `nas_valentin*`,
  `linky_antoine*`, compte GitHub, `LICENSE`.
- **Détection** : abandon de `\b…\b` au profit d'une **frontière de lettre**. `\b` laissait passer
  `telephone_arnaud_notify`, l'underscore étant un caractère de mot — c'est la cause racine de L2b,
  désormais verrouillée en CI. Sous-chaîne nue écartée (`constance` est un nom commun).
- **Gradation** conservée : `CRITICAL` en runtime, `WARNING` en documentation active, hors périmètre pour
  l'historique gelé.

Script `audit_publication_git.py` v1.5.0 → **v1.6.0**, contrat `securite_publication_git.md` v1.4.0 →
**v1.5.0**. Mergé **en dernier**, conformément à §7 : le `CRITICAL` runtime n'est introduit qu'une fois
le runtime propre (L2/L2b) et l'instance migrée (L5), faute de quoi la CI casse pendant le chantier.

### Lot 6 — validation terrain (partiel, 2026-07-20)

| Critère | État |
|---|---|
| **R4 — réception d'alerte** | ✅ **levé** — notification de test émise sur `parent_1` et **réception confirmée par le propriétaire**. Les 62 automatisations d'alerte partageant cette cible unique, le canal est rétabli dans son ensemble. |
| **R1 — chaîne d'alarme** | ⏳ partiel — `presence_famille_securite` = `on`, 0 automatisation et 0 script indisponible, `sensor.telephone_parent_1_bssid_dynamic` = BSSID nominal. **Manque** l'observation d'une transition de présence réelle. **✅ Levé le 2026-07-20 à 19:03 — voir infra.** |
| Entités portant un prénom | ✅ **0** hors `nas_valentin*` / `linky_antoine*` (D3) |

**L6 reste ouvert** jusqu'à observation d'une transition `not_home → Maison securite` confirmant la
chaîne présence → alarme de bout en bout. **Aucune panne fabriquée** : attendre une occurrence
naturelle.

#### Apport de l'audit fonctionnel post-migration v17 (2026-07-20, 17:05–17:25)

Audit en lecture seule sur l'instance. Ce qu'il **ajoute** à L6 :

- **Sens sortant de la chaîne observé de bout en bout**, à 16:56:31, en millisecondes :
  `timer.babysitting → idle` (.001) · `mode_babysitting → off` (.006) · `presence_enfants → off` (.009) ·
  `binary_sensor.presence_enfants → off` (.010) · `presence_famille → off` (.010) ·
  **`presence_famille_securite → off`** (.010). L'agrégat de sécurité retombe correctement quand son
  dernier contributeur se libère, `person.parent_1` et `person.parent_2` étant déjà `not_home`.
- **Transition `person.*` réelle post-migration** : `person.parent_1 → not_home` à 14:06, sur l'entité
  renommée au registre en L5.
- **Cibles de notification** : les 6 helpers téléphone sont correctement restaurés et les deux services
  `notify.mobile_app_*` **existent** — la restauration L5 étape 4 est vérifiée.
- **Critère de clôture 3** : **0 entité live** portant un prénom, hors `nas_valentin*` / `linky_antoine*`
  (D3/D4). 29 entrées subsistent au **registre**, toutes `disabled_by` et **sans état** — elles ne
  participent donc pas à la surface exposée.

**Ce qu'il n'établit pas.** Le sens **entrant** (`not_home → Maison securite`) n'a pas été observé : seul
le relâchement l'a été. R1 reste donc `⏳ partiel` et **L6 n'est pas soldé**. La distinction est
délibérée — un agrégat qui retombe correctement ne prouve pas qu'il se lève correctement.

#### Observation du sens entrant (2026-07-20, 19:00→19:03) — R1 levé

**Occurrence naturelle, aucune panne fabriquée.** Relevé en lecture seule de la base recorder :

| Heure | Entité | Transition |
|---|---|---|
| 19:00:43 | `binary_sensor.presence_famille_unifiee` | `off` → `on` |
| **19:02:37** | `binary_sensor.presence_famille_securite` | `off` → **`on`** |
| 19:02:43 | `binary_sensor.presence_famille_securite` | `on` → `off` (6 s) |
| **19:03:12** | `binary_sensor.presence_famille_securite` | `off` → **`on`** (stable) |

Le sens **entrant** est donc observé : l'agrégat de sécurité **se lève**, et pas seulement
il retombe. **Arbitrage propriétaire (2026-07-20) : R1 est levé.**

**Portée exacte de la preuve — limite consignée.** Le recorder n'historise que
`presence_famille_securite` et `presence_famille_unifiee` ; `presence_enfants`,
`presence_famille` et `presence_famille_securite_confirmee_alarme` **en sont absents**.
L'établissement est donc établi **à son aboutissement**, et non maillon par maillon comme
l'avait été le relâchement (cascade milliseconde du 16:56:31). Les deux preuves ne sont pas
de même nature ; celle-ci est jugée **suffisante par arbitrage propriétaire**.

**Micro-oscillation notée, sans suite.** Le `on → off → on` de 6 s à 19:02:43 est le yoyo
décrit en `D-PRES`, que `presence_famille_securite_confirmee_alarme` (`delay_on 15 s`)
absorbe par construction — un pic de 6 s ne franchit pas 15 s. Ce capteur n'étant pas
historisé, le fait est **attendu, non vérifié**. Aucun travail ouvert à ce titre.
