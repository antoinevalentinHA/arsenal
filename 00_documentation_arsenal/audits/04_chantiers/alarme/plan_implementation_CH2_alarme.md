# ==========================================================
# 🛠️ ARSENAL — PLAN D'IMPLÉMENTATION
#     Chantier CH-2 — Option 1 : raison décisionnelle, autorité unique au cerveau
# ==========================================================

## 📌 Cadre

- **Chantier** : CH-2 — lots **ALM-IMP-2** (autorité/observabilité de `alarme_raison`) + **ALM-MIN-4** (code mort du cerveau).
- **Option retenue** : **Option 1** — le cerveau `script.alarme_decision_centrale` devient l'**écrivain exclusif** de `input_text.alarme_raison` (raison décisionnelle) ; les scripts d'application cessent d'y écrire.
- **Interdits respectés** : aucun YAML complet, aucun patch, aucune correction rédigée. Ce document est **uniquement** le plan d'implémentation.
- **Avantage structurel d'Option 1** : les contrats `30_decision_centrale.md` et `40_application_decision.md` **décrivent déjà** cette autorité ; le runtime rejoint donc le contrat existant. Le travail documentaire se réduit à l'en-tête du helper (et au réalignement formel porté par CH-5).
- **Conséquence assumée d'Option 1** : le marqueur persistant « armement / desarmement » disparaît du helper. Impact faible — l'origine de l'action reste visible dans la **notification utilisateur** émise par les scripts (champ `origine` déjà présent).

---

## 1️⃣ Fichiers à modifier

| # | Fichier | Nature de la modification (descriptive, non rédigée) |
|---|---------|------------------------------------------------------|
| F1 | `10_scripts/alarme/decision_centrale.yaml` | **IMP-2** : ajouter, à la suite des deux publications existantes (`alarme_decision`, `alarme_etat_cible`), une **troisième publication** ciblant `input_text.alarme_raison` avec la variable `raison` **déjà calculée**. **MIN-4** : retirer la variable `alarme_etat` (inutilisée) et simplifier la condition de la branche `DELAI_ENTREE` (le terme `and not presence_securite` est toujours vrai à ce stade de l'`elif`). |
| F2 | `10_scripts/alarme/armement.yaml` | **IMP-2** : retirer l'écriture de `input_text.alarme_raison` (`"armement"`). Conserver intactes l'action d'armement, le bip conditionnel, la notification (avec origine). |
| F3 | `10_scripts/alarme/desarmement.yaml` | **IMP-2** : retirer l'écriture de `input_text.alarme_raison` (`"desarmement"`). Conserver l'arrêt prioritaire de la sirène, le désarmement, le bip conditionnel, la notification. |
| F4 | `04_input_texts/alarme/raison.yaml` | **Doctrine** : aligner l'en-tête « ÉCRIT PAR » sur l'écrivain unique (cerveau). Aucune modification de la définition de l'entité elle-même. |

### Fichiers à VÉRIFIER sans modifier (consommateurs)

| Fichier | Raison de la vérification |
|---------|---------------------------|
| `11_automations/alarme/system/alerte_incoherence.yaml` | Affiche `input_text.alarme_raison` dans sa notification critique → bénéficiera de la raison décisionnelle réelle. Aucune modification attendue. |
| `19_button_card_templates/40_dashboards/alarme/30_diagnostic/carte_alarme_decision.yaml` | Affiche `input_text.alarme_raison` (fallback `|| ''` présent) → tolère le changement. Aucune modification attendue. |

### Hors périmètre (ne pas toucher)

- `input_text.alarme_etat_cible` et `input_text.alarme_decision` : sémantique et publication **inchangées**.
- Clause `person.* == 'Zone maison'` de `presence.yaml` : **domaine Présence**, hors CH-2.
- Attribut `raison` du capteur `binary_sensor.alarme_systeme_coherent` : concept distinct, **non concerné**.

---

## 2️⃣ Ordre des modifications

> Toutes les modifications sont appliquées dans **une seule passe de déploiement** (un reload groupé), pour éviter toute fenêtre où `alarme_raison` n'aurait aucun écrivain. L'ordre ci-dessous est l'ordre de **revue/commit** recommandé.

1. **F1 — Publication de la raison par le cerveau** (avant tout retrait côté application). Tant que cette étape n'est pas en place, ne pas retirer les écritures des scripts.
2. **F1 — Nettoyage MIN-4** (même fichier, même passe) : suppression de `alarme_etat` et simplification de la condition. *Peut faire l'objet d'un commit distinct (cf. rollback).*
3. **F2 puis F3 — Retrait des écritures `alarme_raison`** dans les scripts d'application.
4. **F4 — Réalignement de l'en-tête doctrinal** du helper `raison.yaml`.

> **Recommandation de granularité de commit** : deux commits distincts — (A) **MIN-4** (nettoyage, comportement inchangé), (B) **IMP-2** (publication + retrait + doctrine). Cela autorise un rollback ciblé (cf. §7).

> **Séquencement inter-chantiers** : CH-2 **doit précéder CH-3** (qui éditera aussi `decision_centrale.yaml`) afin d'éviter une édition concurrente du cerveau.

---

## 3️⃣ Invariants à préserver

- **I-A — Autorité unique** : après application, `input_text.alarme_raison` n'est écrit **que** par le cerveau. Aucun autre écrivain.
- **I-B — Cerveau pur** : la seule action ajoutée est une publication `input_text` (cohérente avec les deux existantes). Aucune action sur `alarm_control_panel`, timer, notification ou sirène.
- **I-C — Non-exécutoire** : `alarme_raison` ne doit jamais devenir une condition ou un trigger d'armement (contrat `10`). Le risque de sécurité reste **nul**.
- **I-D — Déterminisme** : mêmes entrées → mêmes sorties ; la raison reste alignée sur le code décisionnel (`alarme_decision`).
- **I-E — Idempotence** : republier une raison identique ne crée aucun effet de bord ni bruit de notification.
- **I-F — Intangibilité** : `alarme_etat_cible` et `alarme_decision` conservent sémantique et publication. Le pipeline d'application n'est pas modifié.
- **I-G — Équivalence logique MIN-4** : la simplification de la branche `DELAI_ENTREE` doit être **strictement équivalente** (à ce point de l'`elif`, `presence_securite` est déjà faux).
- **I-H — Normalisation** : la valeur publiée de `alarme_raison` doit suivre **exactement** le même schéma de normalisation que `alarme_decision` et `alarme_etat_cible` déjà publiés (pas d'espaces ni de sauts de ligne parasites).
- **I-I — Visibilité de l'origine** : les scripts d'application conservent leur notification incluant l'`origine`, seule trace utilisateur de l'acte.

---

## 4️⃣ Tests statiques (avant déploiement)

- **T1 — Lint** : `yamllint` (configuration `.yamllint` du dépôt) sur F1–F4.
- **T2 — Unicité d'écrivain** : recherche globale confirmant qu'après modification, **seul** le cerveau écrit `input_text.alarme_raison` (aucune autre occurrence d'écriture).
- **T3 — Normalisation** : revue du rendu attendu de la variable `raison` ; comparaison avec le schéma de `alarme_decision`/`alarme_etat_cible` pour garantir l'absence de whitespace parasite (I-H).
- **T4 — Équivalence MIN-4** : revue de la table de décision confirmant que la suppression de `and not presence_securite` ne modifie aucune sortie (I-G).
- **T5 — Référence morte** : confirmer que `alarme_etat` n'est référencée nulle part avant suppression.
- **T6 — Check configuration HA** : validation du parsing des scripts (`Check configuration`).
- **T7 — Tolérance consommateurs** : revue de `alerte_incoherence.yaml` (interpolation texte) et `carte_alarme_decision.yaml` (fallback présent) au nouveau contenu.
- **T8 — Cohérence contractuelle** : confirmer que `30`/`40` décrivent déjà l'autorité unique (pas de réécriture nécessaire) et que l'en-tête `raison.yaml` est aligné.
- **T9 — CI contrats** : exécution de la chaîne de validation contractuelle Arsenal (`scripts/arsenal_contracts` / `tools/arsenal_ci`) sur le domaine alarme.

---

## 5️⃣ Vérifications runtime (après application)

- **R1 — Reload propre** : recharger scripts + templates ; vérifier l'absence d'erreur/avertissement au log.
- **R2 — Raison décisionnelle** : provoquer un recalcul (ex. changement de `mode_alarme`) et vérifier que `input_text.alarme_raison` reflète la **raison décisionnelle** (ex. « Mode alarme non automatique »), et **non** `armement`/`desarmement`.
- **R3 — Non-écrasement** : armer puis désarmer manuellement ; vérifier que `alarme_raison` n'est plus écrasé par les scripts d'application.
- **R4 — Observabilité d'incident** : en **mode test**, provoquer une divergence réel/cible > seuil et vérifier que la notification d'incohérence affiche la **vraie cause**.
- **R5 — UI** : vérifier l'affichage de la raison sur `carte_alarme_decision` (pas de valeur vide ni parasitée).
- **R6 — Non-régression application** : vérifier l'armement/désarmement automatique nominal (pipeline `automation 27` inchangé).
- **R7 — Normalisation à l'affichage** : confirmer l'absence d'espaces/sauts parasites côté UI et notification.
- **R8 — Idempotence** : déclencher plusieurs recalculs successifs ; vérifier l'absence de bruit (pas de notifications répétées, pas d'oscillation).

---

## 6️⃣ Risques de régression

| Réf | Risque | Mitigation |
|-----|--------|------------|
| RG1 | Fenêtre transitoire sans écrivain de `alarme_raison` (déploiement non atomique) | Déploiement en une seule passe ; F1 (publication) avant F2/F3 (retraits) dans la revue |
| RG2 | Valeur de raison avec whitespace parasite → UI/alerte dégradée | T3 + I-H + R7 |
| RG3 | Simplification MIN-4 introduisant une divergence logique | T4 + R2 ciblé sur la branche `DELAI_ENTREE` ; commit MIN-4 séparé (rollback isolé) |
| RG4 | Perte du marqueur persistant « armement/desarmement » | Accepté par Option 1 ; origine toujours visible en notification (I-I) |
| RG5 | Consommateur caché dépendant de la valeur « armement/desarmement » | T2 + revue : les deux consommateurs n'utilisent la valeur qu'en **affichage** (aucune logique) |
| RG6 | Édition concurrente future du cerveau (CH-3) | Séquencer CH-2 avant CH-3 |
| RG7 | Risque de sécurité directe | **Nul** — cerveau pur, raison non-exécutoire (I-B, I-C) |

---

## 7️⃣ Points de rollback

- **Granularité recommandée** : deux commits — (A) MIN-4 (nettoyage), (B) IMP-2 (publication + retrait + doctrine) — pour un **rollback ciblé** de l'un sans l'autre.
- **Rollback atomique** : revert des fichiers concernés à l'état HEAD `4336b1d` + reload. Sans effet de bord de sécurité (cerveau pur, raison non-exécutoire).
- **Aucune migration de données** : `input_text` ne porte pas de schéma ; la dernière valeur restaurée sera réécrite au prochain recalcul du cerveau. Le rollback ne nécessite aucune réinitialisation.
- **Critères de déclenchement du rollback** :
  - erreur de parsing / d'analyse au reload (échec R1) ;
  - raison affichée vide ou parasitée, non corrigeable par normalisation (échec R5/R7) ;
  - régression observée sur le pipeline d'application (échec R6) ;
  - divergence de comportement de la branche `DELAI_ENTREE` (échec R2 lié à MIN-4) → rollback **du seul commit A**.
- **État de référence** : commit/tag pris **avant** le chantier ; conservation des deux documents (audit officiel + ce plan) comme dossier de traçabilité.

---

## 🔗 Rappels d'articulation

- **Contrats** : sous Option 1, `30`/`40` sont **déjà conformes** ; seul l'en-tête `raison.yaml` est à aligner immédiatement. Le réalignement formel résiduel (et la dette ALM-DOC-1) reste du ressort de **CH-5**.
- **CH-1 / CH-3** : CH-2 fixe la doctrine d'autorité de sortie que CH-1 (état « intrusion confirmée » éventuel) et CH-3 (branche babysitting) devront respecter. CH-2 **précède** ces deux chantiers.

---

*Fin du plan d'implémentation CH-2 (Option 1). Aucun YAML complet, aucun patch, aucune correction rédigée : ce document décrit les fichiers, l'ordre, les invariants, les tests, les vérifications, les risques et les points de rollback. La rédaction effective des modifications fera l'objet d'une étape ultérieure, sur décision explicite.*
