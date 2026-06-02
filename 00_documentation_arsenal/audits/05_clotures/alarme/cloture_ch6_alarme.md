# Clôture de chantier — CH-6 Alarme (clavier PIN)

> **Statut :** clôture de **chantier** — CH-6 **soldé** ; `ALM-CRIT-3` **résolu et validé terrain** ; domaine **Alarme NON clôturé**
> **Domaine :** `alarme` — saisie clavier (code PIN) et flux badge
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/alarme/cloture_ch6_alarme.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/02_contre_expertises/alarme/contre_expertise_CH6_alarme.md`
> - `00_documentation_arsenal/audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
> - `00_documentation_arsenal/audits/03_plans_action/alarme/plan_action_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/backlog_alarme.md`
> **État du dépôt à la rédaction :** `origin/main` = `5f56ee7`. Correctifs runtime CH-6 : `139640b` (flux PIN explicite) et `5f56ee7` (garde badge).
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Acter la clôture documentaire du chantier **CH-6** après application des correctifs runtime **et** validation terrain. Ce document solde `ALM-CRIT-3` (clavier PIN inopérant) ; il ne prononce pas la clôture du domaine Alarme (cf. §7).

---

## 2. Constat traité (rappel)

`ALM-CRIT-3` — Clavier PIN inopérant. La **contre-expertise** avait requalifié le constat : l'hypothèse « trigger perdu via `script.turn_on` » est infirmée ; cause réelle = la valeur soumise à la validation n'était pas le code (dépendance fragile à `trigger`), et l'évènement PIN était parasité par l'automatisation badge (PIN interprété comme UID → « badge inconnu »). Gravité critique maintenue à l'époque.

---

## 3. Correctifs appliqués

| Lot | Objet | Commit |
|-----|-------|--------|
| **PIN** | Flux PIN rendu déterministe : le code et la source sont transmis explicitement au script (suppression de la dépendance à `trigger`) | `139640b` |
| **BADGE** | Le flux badge ne traite que les UID non numériques ; les codes PIN (numériques) sont ignorés, flux RFID préservé | `5f56ee7` |

Fichiers concernés : `11_automations/alarme/armement/clavier.yaml`, `10_scripts/alarme/clavier.yaml`, `11_automations/alarme/desarmement_badge.yaml`. Aucun ID modifié, aucun helper créé, aucun code secret touché.

---

## 4. Validation terrain réalisée

| Test | Scénario | Résultat |
|------|----------|----------|
| 1 | Code valide + cadenas fermé | **Armement réussi** ✅ |
| 2 | Code valide + cadenas ouvert | **Désarmement réussi** ✅ |
| 3 | Opérations PIN | **Aucune notification « Badge inconnu »** ✅ |

Les trois objectifs fonctionnels de CH-6 (armement PIN, désarmement PIN, non-parasitage badge) sont **confirmés en conditions réelles**.

**Observation complémentaire — armement clavier avec présence active.** Un armement par clavier réalisé alors que la géolocalisation / présence était active **arme bien l'alarme**, immédiatement suivie d'un **désarmement par la logique de présence**. Ce comportement est **attendu** dans l'architecture Arsenal (l'automatisation de présence peut reprendre la main aussitôt) ; il **ne constitue pas un échec du flux clavier** — il confirme au contraire que le flux d'armement clavier s'exécute correctement.

---

## 5. Résidus documentés (non bloquants)

- **R1 — Sémantique du champ « badge » :** les entités du clavier continuent d'exposer la valeur du PIN dans le champ historiquement nommé « badge » (`_badge` = `action_code`). Ce comportement **n'empêche plus** le fonctionnement (le flux badge ignore désormais les valeurs numériques). Dette **cosmétique/sémantique**, non bloquante.
- **R2 — Flux badge RFID inerte (observation distincte) :** à la présentation d'un badge RFID, **aucun évènement observable** dans Home Assistant (aucune automatisation déclenchée, aucune entité modifiée). Le correctif **n'a pas cassé** le flux RFID — il a préservé son chemin de code ; mais ce flux **n'est pas exerçable** sur l'intégration actuelle (aucun évènement ne remonte). Ce point **ne relève pas d'`ALM-CRIT-3`** (qui porte sur le PIN) et **ne bloque pas** sa clôture ; il constitue une **observation nouvelle**, candidate à une investigation distincte (matériel / exposition Zigbee2MQTT), **sans intervention runtime ici**.

---

## 6. Qualification finale d'`ALM-CRIT-3`

**RÉSOLU et VALIDÉ TERRAIN → constat soldé.**
- Effet corrigé : le clavier PIN arme et désarme effectivement.
- Cause (telle que requalifiée par la contre-expertise) traitée à la racine : entrée déterministe du script + garde du flux badge.
- La gravité critique initiale est **levée** ; le constat est **clos**.

---

## 7. Statut de CH-6 et impact domaine

**CH-6 SOLDÉ.** L'objectif du chantier (rendre le clavier PIN opérant et non parasité) est atteint et validé terrain.

**Domaine Alarme NON clôturé.** État après CH-6 :
- **CH-2** soldé ; **CH-6** soldé.
- **CH-1** en **clôture conditionnelle acquise** — réserve : test positif `S3` (cf. clôture CH-1 §10).
- Chantiers restants : **CH-3** (`ALM-IMP-1`), **CH-4** (`ALM-IMP-3`), **CH-5** (documentaire).
- Observation ouverte distincte : **R2** (flux RFID inerte) — hors `ALM-CRIT-3`, à investiguer séparément.

---

## 8. Verdict

**CH-6 soldé — `ALM-CRIT-3` résolu et validé terrain — domaine Alarme non clôturé.** Deux résidus documentés sans effet bloquant (sémantique « badge » ; RFID inerte). Conformément au principe directeur, le runtime est la référence ; l'alignement éventuel des en-têtes/contrats du domaine relève du lot documentaire CH-5.

---

*Clôture de chantier CH-6 Alarme. Établie en lecture du dépôt (`origin/main` = `5f56ee7`) et des observations de validation terrain fournies. Acte documentaire — aucune modification runtime, aucun contrat, aucun code secret. Aucun code PIN réel n'est consigné.*
