# Clôture de chantier — CH-4 Alarme (sirène & feedback sonore)

> **Statut :** clôture de **chantier** — CH-4 en **clôture conditionnelle acquise** ; deux lots **implémentés + déployés** ; **réserve unique** pour clôture définitive = **validation terrain de `ALM-MIN-2`** (feedback bip de désarmement) ; domaine **Alarme NON clôturé**.
> **Domaine :** `alarme` — pile sirène (déclenchement, arrêt, feedback)
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/alarme/cloture_ch4_alarme.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/backlog_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/etat_post_CH6.md`
> **État du dépôt à la rédaction :** `origin/main` = `476116e`. Correctifs runtime CH-4 : `5892d35` (lot A / `ALM-MIN-2`) et `476116e` (lot B / `ALM-IMP-3`).
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Acter la **clôture conditionnelle** du chantier **CH-4** après application et déploiement des deux lots runtime. Ce document **ne prononce pas** la clôture définitive de CH-4 (réserve §6) ni celle du domaine Alarme (§7).

---

## 2. Constats traités (rappel + historique de requalification)

- **`ALM-MIN-2`** — double bip de désarmement + absence de garde mode test + bip sur désarmement automatique. Gravité **Mineur** (inchangée).
- **`ALM-IMP-3`** — auto-extinction sirène : entité non définie + `delay` long. **Requalifié Important 🟠 → Mineur 🟡 (post-V4)** : la validation terrain V4 a établi que l'auto-extinction est portée par le **device** (durée MQTT `burglar` = `number.sirene_max_duration`), qu'elle s'auto-coupe et qu'un redémarrage HA pendant le hurlement ne modifie pas ce comportement (**reboot-safe**). Le risque de sécurité présumé n'existe pas ; le résidu était du code mort + une dette de représentation. *(Traçabilité : bannières post-V4 et post-CH-4-B dans le rapport officiel.)*

---

## 3. Correctifs appliqués

| Lot | Objet | Commit |
|-----|-------|--------|
| **A — `ALM-MIN-2`** | Émetteur de bip de désarmement unique = `script.alarme_desarmer` ; bip restreint aux origines explicites (`dashboard`/`clavier`/`badge`), hors mode test ; suppression de l'automatisation redondante `bip_desactivation.yaml` (ID `1002000000010`) | `5892d35` |
| **B — `ALM-IMP-3`** | Suppression de l'automatisation morte `11_automations/alarme/sirene/stop.yaml` (ID `1002000000012`) : entité fantôme `switch.sirene_alarm`, `delay` latent et notification morte éliminés | `476116e` |

Aucun ID modifié (seuls deux ID d'automatisations **mortes/redondantes** retirés avec leur fichier), aucun alias ni entité renommé, aucun helper ni timer créé. `script.arret_sirene`, `script.sirene_brutale` et la durée device **non modifiés**.

---

## 4. Validation

| Lot | Nature de la validation | Statut |
|-----|-------------------------|--------|
| **B (`ALM-IMP-3`)** | Statique (retrait de code **mort** — aucun changement de comportement) + mécanisme réel déjà établi par **V4** (reboot-safe) | **Acquis** — pas de validation terrain requise |
| **A (`ALM-MIN-2`)** | Comportementale (bip de désarmement) — nécessite observation en conditions réelles | **En attente** (validation terrain opportuniste, utilisateur absent) |

Scénarios terrain attendus pour le lot A : un seul bip au désarmement explicite (clavier/badge/dashboard) ; aucun bip en mode test ; aucun bip sur désarmement automatique (présence/géoloc) ; bips d'armement et de début de délai inchangés.

---

## 5. Chemin d'arrêt sirène canonique (état post-CH-4)

Deux mécanismes **complémentaires et suffisants**, confirmés par la cartographie runtime :

- **Coupe immédiate** = `script.arret_sirene` (MQTT `warning/stop`), appelé **inconditionnellement** en première étape de `script.alarme_desarmer` (priorité absolue, contrat 70). S'exécute sur tout désarmement explicite ou automatique.
- **Auto-extinction sans désarmement** = durée device (`burglar` / `number.sirene_max_duration`), **reboot-safe** (V4).

L'ancienne automatisation `stop.yaml` (commutateur fantôme) n'a jamais participé à ce chemin ; sa suppression ne modifie aucun comportement.

> **Réserve documentaire (hors lot runtime)** : la durée device n'est pas encore **documentée comme coupe-circuit canonique** au niveau du contrat `70` / des en-têtes — dette de représentation à porter par **CH-5**.

---

## 6. Résidus et réserve

- **Réserve unique de clôture (lot A)** : **validation terrain de `ALM-MIN-2`**. Tant qu'elle n'est pas réalisée, CH-4 reste en **clôture conditionnelle acquise**.
- **Dette documentaire (lot B)** : documenter la durée device comme coupe-circuit canonique → **CH-5** / contrat `70`.
- **Note hors contrat** : un désarmement par la carte panneau HA brute (sans passer par `script.alarme_desarmer`) ne déclenche ni le bip ni `arret_sirene` immédiat — la sirène n'est alors coupée que par la durée device. Conforme au principe « tout désarmement transite par le script » ; pas un défaut du chemin d'arrêt.

---

## 7. Statut de CH-4 et impact domaine

**CH-4 — CLÔTURE CONDITIONNELLE ACQUISE.** Les deux lots sont implémentés et déployés ; le lot B (`ALM-IMP-3`) est résolu au runtime (résidu strictement documentaire) ; la clôture **définitive** est suspendue à la **seule** validation terrain de `ALM-MIN-2`.

**Domaine Alarme NON clôturé.** État :
- **CH-2** soldé ; **CH-6** soldé (validé terrain).
- **CH-1** en clôture conditionnelle acquise — réserve : test positif `S3`.
- **CH-4** en clôture conditionnelle acquise — réserve : validation terrain `ALM-MIN-2`.
- Chantiers restants : **CH-3** (`ALM-IMP-1`, gated V3), **CH-5** (documentaire ; porte aussi la doc du coupe-circuit canonique).
- Observation distincte ouverte : **R2** (flux RFID inerte).

---

## 8. Qualification finale des constats

- **`ALM-IMP-3`** — **résidu runtime RÉSOLU** (`476116e`) ; gravité Mineur (requalifiée post-V4) ; reste une dette de représentation (CH-5). Aucun enjeu de sécurité.
- **`ALM-MIN-2`** — **implémenté + déployé** (`5892d35`) ; **non soldé** : validation terrain en attente.

---

## 9. Verdict

**CH-4 en clôture conditionnelle acquise — deux lots implémentés et déployés — domaine Alarme non clôturé.** Réserve unique : validation terrain de `ALM-MIN-2`. Résidu documentaire (coupe-circuit canonique) renvoyé à CH-5. Conformément au principe directeur, le runtime est la référence ; l'alignement des contrats/en-têtes suivra.

---

*Clôture conditionnelle de chantier CH-4 Alarme. Établie en lecture du dépôt (`origin/main` = `476116e`) et des observations fournies. Acte documentaire — aucune modification runtime, aucun YAML fonctionnel, aucun contrat, aucune CI.*
