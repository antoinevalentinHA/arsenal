# Clôture de chantier — CH-2 Alarme

> **Statut :** clôture de **chantier** — CH-2 **soldé** ; domaine **Alarme NON clôturé**
> **Domaine :** `alarme` — cerveau décisionnel et helpers de sortie
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/alarme/cloture_ch2_alarme.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
> - `00_documentation_arsenal/audits/03_plans_action/alarme/plan_action_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/backlog_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/dossier_conception_CH2_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/plan_implementation_CH2_alarme.md`
> **État du dépôt à la rédaction :** `origin/main` = `99cbc0b`. Runtime CH-2 intégré — `dc8667e` (ALM-MIN-4) et `99cbc0b` (ALM-IMP-2) ; `git pull` effectué, scripts et input_texts rechargés, **aucune erreur signalée**.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Acter la clôture documentaire du chantier **CH-2** (cerveau décisionnel : autorité des helpers de sortie & propreté logique), après implémentation et déploiement runtime. Ce document **solde CH-2** ; il **ne prononce pas** la clôture du domaine Alarme (cf. §7).

---

## 2. Constat traité

| Constat | Gravité | Énoncé |
|---------|---------|--------|
| **ALM-IMP-2** | 🟠 Important | `input_text.alarme_raison` était écrit par les scripts d'armement/désarmement (`"armement"` / `"desarmement"`), jamais par le cerveau — qui calculait pourtant la raison décisionnelle puis l'abandonnait. Inversion d'autorité (contrat `30`) et observabilité dégradée (l'alerte d'incohérence affichait une raison trompeuse). Intègre la contradiction documentaire de l'en-tête `raison.yaml` (ex-C14). |
| **ALM-MIN-4** | 🟡 Mineur | Variable `alarme_etat` calculée et inutilisée dans le cerveau ; terme `and not presence_securite` redondant dans la branche `DELAI_ENTREE`. |

Référence détaillée : `04_chantiers/alarme/backlog_alarme.md` (CH-2) et `01_rapports/alarme/audit_alarme_rapport_officiel.md` (ALM-IMP-2 / ALM-MIN-4).

---

## 3. Arbitrage retenu

**Option 1** — `input_text.alarme_raison` = raison décisionnelle humaine, **écrivain exclusif = `script.alarme_decision_centrale`**. (Arbitrage instruit dans `04_chantiers/alarme/dossier_conception_CH2_alarme.md`, exécution cadrée par `04_chantiers/alarme/plan_implementation_CH2_alarme.md`.)

- Les scripts d'armement/désarmement n'écrivent plus le helper.
- **Aucun helper créé ni supprimé** ; `alarme_decision` et `alarme_etat_cible` inchangés.
- Le marqueur persistant `armement` / `desarmement` n'est pas conservé ; l'origine reste portée par les **notifications existantes**.
- Sous Option 1, les contrats `30` et `40` décrivaient **déjà** cette autorité : le runtime rejoint le contrat, **sans réécriture contractuelle** ; seul l'en-tête du helper `raison.yaml` a été aligné, dans le commit runtime.

---

## 4. Travaux réalisés

| Lot | Objet | Constat | Commit |
|-----|-------|---------|--------|
| **MIN-4** | Suppression de `alarme_etat` ; simplification de la condition `DELAI_ENTREE` (cerveau) | ALM-MIN-4 | `dc8667e` |
| **IMP-2** | Cerveau écrivain exclusif de `alarme_raison` ; retrait des écritures dans armement/désarmement ; en-tête `raison.yaml` aligné | ALM-IMP-2 | `99cbc0b` |

Fichiers runtime concernés : `10_scripts/alarme/decision_centrale.yaml`, `10_scripts/alarme/armement.yaml`, `10_scripts/alarme/desarmement.yaml`, `04_input_texts/alarme/raison.yaml`. Consommateurs (`alerte_incoherence.yaml`, `carte_alarme_decision.yaml`) **non modifiés**.

---

## 5. Validations réalisées

- **Statiques :** parse YAML OK ; `yamllint` (config dépôt) OK ; `git apply --check` OK sur base vierge pour les deux patchs séquentiels ; **écrivain unique** de `alarme_raison` vérifié (seul `decision_centrale.yaml`).
- **Équivalence MIN-4 :** démontrée — **64/64** combinaisons d'entrées identiques entre l'ancienne et la nouvelle condition `DELAI_ENTREE` (comportement strictement préservé).
- **Runtime :** `git pull` effectué ; scripts et input_texts rechargés ; **aucune erreur signalée**.

---

## 6. Statut de CH-2

**SOLDÉ.** Les deux lots sont intégrés, validés statiquement et déployés sans erreur. Invariants préservés : cerveau pur (publication d'un helper uniquement, aucune action de sécurité ajoutée) ; comportements **armement, désarmement, sirène, délai d'entrée, blocage et notifications inchangés**.

---

## 7. Impacts sur les chantiers restants

- **CH-1** (🔴 critique — faux positif/négatif sur la voie d'entrée) : **non touché, reste OUVERT**. La doctrine d'autorité de sortie fixée par CH-2 conditionnera la matérialisation d'un éventuel état « intrusion confirmée ». **Non ouvert dans le cadre de cette clôture.**
- **CH-3** (contextes humains / babysitting) : prérequis CH-2 (cerveau nettoyé, doctrine de sortie stabilisée) **satisfait** ; chantier toujours conditionné à sa validation runtime (V3).
- **CH-4** (sirène) : non concerné.
- **CH-5** (cohérence documentaire) : sous Option 1, contrats `30`/`40` déjà conformes ; en-tête `raison.yaml` aligné par CH-2. Restent ouverts : décalage des en-têtes des contrats `20`/`30`/`40` (ALM-DOC-1) et autres lots documentaires.
- **CH-6** (PIN) : non concerné.

Les chantiers restants ne sont **pas portés en chantier dédié** dans le cadre de cette clôture ; ils demeurent décrits dans `04_chantiers/alarme/backlog_alarme.md`.

---

## 8. Verdict

**Chantier CH-2 SOLDÉ — domaine Alarme NON clôturé.** Le domaine conserve au moins un constat critique ouvert (CH-1). L'autorité de la raison décisionnelle est désormais **unique et observable** ; conformément au principe directeur, le runtime est la référence et les contrats en documentent l'état réconcilié.

---

*Clôture de chantier CH-2 Alarme. Établie en lecture du dépôt (`origin/main` = `99cbc0b`) ; acte documentaire sans modification du runtime ni des contrats.*
