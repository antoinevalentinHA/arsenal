# 🔍 ARSENAL — AUDIT : Cohérence préfixe d'ID ↔ domaine fonctionnel propriétaire

> **Statut** : audit **en lecture seule**, préparatoire, **non opposable**.
> **Date** : 2026-07-03.
> **Norme de référence** : [`architecture/03_doctrines/prefixe_domaine_automatisations.md`](../../../architecture/03_doctrines/prefixe_domaine_automatisations.md) (contrat, opposable) et [`architecture/03_doctrines/id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md).
> **Périmètre** : les **263 automatisations** de `11_automations/` (corpus post-migration AID-006, 100 % canonique 14 chiffres, 0 ERROR AID).
> **Aucune modification** de code, d'ID ou de préfixe n'a été effectuée pendant cet audit.

---

## 🎯 Objet

Premier audit d'application du contrat préfixe ↔ domaine : confronter, pour
chaque automatisation, le **domaine d'identité** (déclaré par le préfixe via
`input_select.prefix_id_select`) au **domaine fonctionnel apparent** (établi
par lecture du rôle, des déclencheurs, des entités et des contrats associés —
**jamais du seul chemin de fichier**).

---

## 🧪 Méthode

1. **Inventaire mécanique** des 263 automatisations : fichier, alias, ID,
   préfixe, domaine déclaré, dossier physique (24 préfixes déclarés,
   24 dossiers de premier niveau).
2. **Croisement 1** — dossier physique ↔ domaine du préfixe : **6 divergences**.
3. **Croisement 2** — tête d'alias ↔ domaine du préfixe : **23 signaux**,
   dont 17 écartés après lecture (pur style de nommage : série météo palmarès,
   `cumulus_studio` aliasé « ECS Petite Maison », `bouclage` aliasé
   « ECS - Bouclage », etc. — le nommage des alias est hors périmètre du
   contrat préfixe).
4. **Lecture au fond** de chaque cas signalé (en-tête, rôle, déclencheurs,
   entités lues/écrites, contrats de rattachement).
5. **Audit des références exactes** des IDs candidats dans `11_automations/`,
   `10_scripts/`, `12_template_sensors/`, `18_lovelace/`,
   `19_button_card_templates/`, `scripts/arsenal_contracts/`,
   `00_documentation_arsenal/` (hors `audits/` et `changelog/`, historiques
   gelés) et `.github/` ; plus relevé exhaustif des références par entité
   `automation.*` (slug).
6. **Évaluation des impacts Home Assistant** d'un éventuel changement d'ID.

---

## 📊 Synthèse de classification

| Classement | Nombre | Cas |
|---|:--:|---|
| **Conforme** | 256 | tout le reste du corpus, y compris les cas examinés puis blanchis (§ Cas examinés conformes) |
| **Probablement fautif** | 1 | `10170000000010` (§ Cas 1) |
| **Ambigu — arbitrage propriétaire requis** | 4 | grappe `panne/internet` `10120000000022..25` (§ Cas 3) |
| **Exception à documenter** | 2 | `10010000000030` (§ Cas 2), `10040000000003` (§ Cas 4) |
| **Transversal légitime** | 0 | aucun candidat ne satisfait les 4 critères d'entrée cumulatifs |

---

## 🧾 Cas instruits

### Cas 1 — `10170000000010` · préfixe `ouvertures`, fonction aération — **probablement fautif**

- **Fichier** : `11_automations/aeration/invalidation.yaml`
- **Alias** : « Aération - Invalidation tentative non confirmée »
- **Fonction constatée** : annule proprement une tentative d'aération non
  confirmée (trigger `binary_sensor.tentative_aeration_en_grace`, conditions
  et écriture exclusivement sur les faits `aeration_*`).
- **Rattachement contractuel** : documentée comme pièce du socle
  aération dans `contrats/aeration_blocage_chauffage/socle_transversal/`
  (`10_invalidation_tentative_non_confirmee.md`, `12_tentative_aeration_en_grace.md`),
  qui citent cet ID.
- **Verdict** : domaine fonctionnel propriétaire = **aération** ; préfixe
  `1017` (ouvertures) incohérent. La lecture d'un signal d'ouvrants ne
  transfère pas la propriété (critère d'exclusion du contrat).
- **Références exactes de l'ID** : le fichier lui-même + les 2 contrats
  ci-dessus. Aucune référence runtime, CI, Lovelace ou `.github/`.
  Aucune référence par slug `automation.*`.

### Cas 2 — `10010000000030` · préfixe `aeration`, dossier `ouvertures/` — **exception à documenter** (ou reclassement physique)

- **Fichier** : `11_automations/ouvertures/disqualification_aeration.yaml`
- **Alias** : « Ouvertures - Invalidation aération »
- **Fonction constatée** : clôt le fait métier `input_boolean.aeration_confirmee`
  sur signal « fenêtres fermées stable ». Le déclencheur vient des ouvertures,
  mais la responsabilité (cycle de vie d'un fait aération) est **aération**.
- **Verdict** : le **préfixe est correct** ; seule diverge la localisation
  physique. Deux issues conformes au contrat : documenter la divergence en
  exception, **ou** déplacer le fichier vers `aeration/` (déplacement
  transparent pour HA : `!include_dir_merge_list` récursif, ID inchangé,
  zéro impact registre).
- **Références exactes de l'ID** : le fichier lui-même uniquement.

### Cas 3 — grappe `10120000000022..25` · préfixe `system`, fonction panne Internet — **ambigu, arbitrage requis**

- **Fichiers** : `11_automations/panne/internet/{remediation_ouverture,
  remediation_fermeture, remediation_cadence, reconciliation_demarrage}.yaml`
- **Alias** : « Réseau – Ouverture/Fermeture campagne remédiation »,
  « Réseau – Cadence remédiation Internet », « Réseau – Réconciliation démarrage HA »
- **Fonction constatée** : détection/remédiation/clôture des pannes Internet —
  le cœur du domaine contractuel `contrats/pannes/internet/`.
- **Tension** : les 3 automatisations sœurs de `panne/secteur/` portent le
  préfixe `1004` (panne) ; la gouvernance
  `contrats/pannes/internet/00_panne_internet_gouvernance.md` s'auto-déclare
  « Domaine : Infrastructure / Réseau », ce qui peut plaider pour `system`.
  La carte des domaines rattache toutefois `internet` au domaine Tier 1
  `pannes`.
- **Verdict** : préfixe `1012` (system) **incohérent en apparence** avec le
  propriétaire `panne` ; mais le choix a pu être délibéré (remédiation vue
  comme infrastructure). Décision propriétaire requise :
  **(a)** exception documentée « remédiation réseau = system », ou
  **(b)** correction d'ID `1012 → 1004` (opération exceptionnelle).
- **Références exactes des IDs** : les fichiers eux-mêmes uniquement.
  **Références par slug** : `logbook.yaml` cible
  `automation.reseau_ouverture_campagne_remediation` et
  `automation.reseau_fermeture_campagne_remediation` — slug dérivé de
  l'**alias**, insensible à un changement d'ID tant que l'alias est préservé.

### Cas 4 — `10040000000003` · préfixe `panne`, domaine auto-déclaré `energie_chaudiere` — **exception à documenter**

- **Fichier** : `11_automations/panne/secteur/alerte_bluetti.yaml`
- **Alias** : « Energie chaudiere - Alerte Bluetti »
- **Fonction constatée** : l'en-tête déclare explicitement
  « Domaine : energie_chaudiere / Contrat : energie_chaudiere v1.3 » et
  l'invariant « ne qualifie jamais une panne secteur Arsenal ».
- **Verdict** : le propriétaire fonctionnel est `energie_chaudiere`
  (domaine Tier 1 de la carte, contrat `contrats/bluetti.md`) — domaine qui
  **ne possède aucun préfixe** dans `prefix_id_select`. Créer un préfixe +
  changer l'ID pour une seule automatisation serait disproportionné ;
  la voie proportionnée est l'**exception documentée** (propriétaire
  `energie_chaudiere`, préfixe historique `1004`, adjacence panne secteur).
- **Références exactes de l'ID** : le fichier lui-même uniquement.
  Aucune référence par slug.

---

## ✅ Cas examinés puis jugés conformes

- **`10010000000022`** (`aeration/blocage_chauffage/securite_blocage.yaml`,
  alias « Chauffage - Blocage aération - Sécurité démarrage ») : garde-fou de
  la machine aération→blocage, documenté dans
  `contrats/aeration_blocage_chauffage/socle_transversal/06_securite_demarrage.md`.
  Préfixe `1001` (aeration) **correct** ; seul l'alias prête à confusion
  (nommage, hors périmètre du présent contrat).
- **`10030000000015`** (`climatisation/modes.yaml`, alias « Mode Maison -
  Gestion chauffage clim hiver ») : gate de **capacité** du chauffage par
  climatisation (autorité d'écriture unique de
  `chauffage_clim_active_en_hiver`). Lit le mode maison et le babysitting,
  mais la responsabilité — autoriser ou non la clim en hiver — appartient à
  la **climatisation**. Propriétaire unique identifiable ⇒ non transversal
  (critères d'exclusion du contrat : lire un signal d'un autre domaine ne
  transfère pas la propriété).
- **Domaine `modes`** (13 automatisations, dont « Vacances - Orchestrateur »
  et « Vacances - Gestion ECS désinfection ») : l'application des modes de
  maison EST la responsabilité du domaine `modes` ; les effets sur d'autres
  domaines sont des actions d'application, pas une orchestration sans
  propriétaire.
- **Domaine `system`** (18 automatisations du dossier `system/`) : relances
  d'intégrations, batteries, BSSID, NAS, saison, stabilisation, synchro IDs —
  toutes légitimement `system`.
- **Séries d'alias atypiques** (`meteo` palmarès/clôtures, `cumulus_studio`
  « ECS Petite Maison », `bouclage` « ECS - Bouclage ») : style de nommage
  seulement ; préfixes cohérents.

---

## 🏷️ Domaine `transversal` — verdict

**Aucune automatisation du corpus ne satisfait les 4 critères d'entrée
cumulatifs** du contrat (coordination multi-domaines + absence de
propriétaire unique + rôle d'orchestration/médiation + rattachement
artificiel). Les candidats plausibles (`climatisation/modes.yaml`, les
orchestrateurs `modes/*`) ont tous un propriétaire unique identifiable.

⚠️ Note de vocabulaire (pour la passe contractuelle finale) : le mot
« transversal » est déjà utilisé ailleurs dans le corpus documentaire en un
sens différent — `contrats/index.md` étiquette `poele` et
`aeration_recommandation` « (transversal) » (= à impact multi-domaines), et
`contrats/aeration_blocage_chauffage/socle_transversal/` nomme un socle.
Ces usages désignent des domaines **à propriétaire unique** ; ils ne
créent aucun droit d'entrée dans le futur domaine `transversal` du contrat.

---

## 🏠 Impacts Home Assistant (si des IDs étaient corrigés)

- Pour une automation YAML, **`id` = `unique_id`** de l'entité : changer
  l'ID crée une nouvelle entité et orpheline l'ancienne — risque de slug
  `automation.*_2`, perte de `last_triggered` et des traces.
- Aucun des 7 IDs candidats n'est référencé par ID hors de son propre
  fichier (sauf `10170000000010`, cité par 2 documents de contrat — mise à
  jour documentaire triviale). Aucune cascade runtime.
- Les 2 références `logbook.yaml` ciblent des **slugs** (dérivés d'alias) :
  insensibles à un changement d'ID à alias constant.
- Tout changement d'ID exigerait donc une **procédure transitoire type
  AID-006** (sauvegarde, fenêtre courte « entités absentes », purge UI des
  orphelines, redéploiement, vérification zéro `_2`), avec rollback —
  proportionnée ici à 1 à 5 entités selon l'arbitrage.

---

## 📌 Recommandation

Par ordre de proportionnalité :

1. **Documenter** (registre d'exceptions opposable, à créer à l'étape CI) :
   - Cas 4 (`alerte_bluetti`) : exception assumée `energie_chaudiere` → `1004` ;
   - Cas 2 (`disqualification_aeration`) : soit exception « dossier
     `ouvertures/`, propriétaire `aeration` », soit simple **déplacement de
     fichier** vers `aeration/` (zéro impact HA) — le déplacement est
     préférable (supprime l'exception au lieu de la consigner).
2. **Arbitrer** (décision propriétaire explicite requise) :
   - Cas 3 (grappe réseau ×4) : exception documentée « = system » **ou**
     correction d'ID `1012 → 1004` ;
   - Cas 1 (`invalidation` aération) : correction d'ID `1017 → 1001`
     (opération exceptionnelle, procédure AID-006) **ou** exception documentée
     — la correction est ici la voie propre, le préfixe étant contredit par
     les contrats mêmes qui documentent l'automatisation.
3. **Ne PAS créer le domaine `transversal` maintenant** : aucun ayant droit
   dans le corpus actuel. Le contrat le définit ; sa création attendra le
   premier cas légitime (ou une décision propriétaire).
4. **Créer ensuite la CI** (étape 4) : cohérence préfixe ↔ domaine résolu,
   registre d'exceptions opposable couvrant exactement les cas arbitrés
   ci-dessus, zéro faux positif sur corpus aligné.

Aucun ID ne doit être modifié sans validation explicite de l'arbitrage
ci-dessus, ni sans procédure runtime HA dédiée, hors de la PR Git.

---

## 📎 Annexe — inventaire des divergences mécaniques dossier ↔ préfixe

| ID | Préfixe (domaine) | Dossier | Alias |
|---|---|---|---|
| `10170000000010` | 1017 (ouvertures) | `aeration/` | Aération - Invalidation tentative non confirmée |
| `10010000000030` | 1001 (aeration) | `ouvertures/` | Ouvertures - Invalidation aération |
| `10120000000022` | 1012 (system) | `panne/internet/` | Réseau – Ouverture campagne remédiation |
| `10120000000023` | 1012 (system) | `panne/internet/` | Réseau – Fermeture campagne remédiation |
| `10120000000024` | 1012 (system) | `panne/internet/` | Réseau – Cadence remédiation Internet |
| `10120000000025` | 1012 (system) | `panne/internet/` | Réseau – Réconciliation démarrage HA |

(Le cas 4, `10040000000003`, ne diverge pas mécaniquement — dossier `panne/`,
préfixe `panne` — il n'est détecté que par lecture de l'en-tête : illustration
directe de l'interdit contractuel de déduction naïve dossier → préfixe.)
