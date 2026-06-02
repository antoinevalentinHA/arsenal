# ==========================================================
# 📋 ARSENAL — BACKLOG PRIORISÉ
#     Domaine : Sécurité / Alarme
# ==========================================================

## 📌 Cadre

- **Sources** : `audit_alarme_rapport_officiel.md` + `plan_action_alarme.md` (HEAD `4336b1d`).
- **Nature** : backlog priorisé des 6 chantiers (CH-1 → CH-6). Pas de calendrier, pas de charge en jours.
- **Interdits respectés** : aucun patch, aucun YAML, aucune correction. Les arbitrages restent ouverts.

### Définitions

- **Bénéfice attendu** : valeur de sécurité / observabilité / dette résorbée.
- **Risque de régression** : probabilité de perturber le système de sécurité **en production** en exécutant le chantier.
- **Effort relatif** : surface technique + conception (`faible` · `moyen` · `élevé`).
- **ROI** (qualitatif) : bénéfice × levier de déblocage, rapporté à effort × risque (`élevé` · `moyen` · `faible`). Le ROI **n'est pas** la priorité de sécurité : un chantier incontournable peut avoir un ROI d'efficience modéré.

---

## 🗂️ Fiches chantiers

### CH-1 — Ouvrants d'entrée & confirmation d'intrusion *(CRIT-1, CRIT-2, MIN-5)*

- **Bénéfice attendu** : **maximal** — résorbe les deux défauts critiques de sécurité (faux positif à l'entrée, faux négatif porte/garage à l'expiration du délai) sur la voie d'accès principale.
- **Risque de régression** : **élevé** — touche la détection vivante ; transition sensible (faux positifs/négatifs possibles).
- **Effort relatif** : **élevé** — surface large, interaction domaine ouvertures, refonte de frontière + cible §9.
- **Prérequis** : doctrine helpers stabilisée (CH-2) ; contrats `50`, `51`, `contrats/ouvertures/{alarme, redondance}` ; dissociation sémantique de `ouverture_qualifiee_maison`.
- **Dépendances** : amont = **CH-2** ; externe = domaine **ouvertures** ; latérale = **CH-4** (chaîne sirène).
- **ROI** : **moyen** — bénéfice absolu maximal, mais effort et risque maximaux (incontournable, peu efficient).

### CH-2 — Cerveau décisionnel : autorité des helpers & propreté *(IMP-2, MIN-4)*

- **Bénéfice attendu** : **élevé** — restaure l'autorité d'écriture, rend la raison décisionnelle observable (alerte d'incident fiable), nettoie le cerveau. **Effet de levier** : prérequis de CH-1 et CH-3.
- **Risque de régression** : **moyen** — pas d'action de sécurité directe ; impact sur l'observabilité du diagnostic.
- **Effort relatif** : **moyen** — cerveau pur + 2 scripts d'application + 1 automation d'alerte ; arbitrage doctrinal préalable.
- **Prérequis** : arbitrage « helper unique vs scindé » pour la raison ; contrats `30`, `40`, en-têtes helpers.
- **Dépendances** : aucune amont ; **débloque CH-1 et CH-3**.
- **ROI** : **élevé** — effort modéré, fort levier, améliore l'observabilité socle.

### CH-3 — Contextes humains & câblage des déclencheurs *(IMP-1, MIN-1)*

- **Bénéfice attendu** : **élevé** — ferme un angle mort sécurité adjacent (babysitting) et l'incohérence de câblage des déclencheurs.
- **Risque de régression** : **moyen** — domaine adjacent à la sécurité (occupants vulnérables) ; calibrage d'inhibition délicat.
- **Effort relatif** : **moyen** — extension bornée de la décision + réalignement de déclencheurs.
- **Prérequis** : arbitrage du rôle du babysitting ; source de vérité « visite active » ; contrats `99`, `96`, `20/30`, contrat Présence.
- **Dépendances** : amont = **CH-2**.
- **ROI** : **moyen** — bon bénéfice sécurité, mais gated (V3) et dépendant.

### CH-4 — Sirène & feedback sonore *(MIN-2 ; `ALM-IMP-3` requalifié Mineur post-V4)*

> **Post-V4 (dépôt `e3d1349`) — traçabilité.** Auto-extinction device confirmée **reboot-safe** → **`ALM-IMP-3` requalifié Important → Mineur**. CH-4 devient un chantier de **dette technique / gouvernance + hygiène feedback**, **sans enjeu sécurité**. **Gate V4 : résolu.** Les classements ci-dessous, antérieurs à V4, sont à lire à la lumière de cette requalification.
>
> **Statut (dépôt `5892d35`) — lot CH-4-A implémenté.** `ALM-MIN-2` : bip de désarmement émis uniquement par `script.alarme_desarmer`, restreint aux origines explicites (`dashboard`/`clavier`/`badge`) ; `bip_desactivation.yaml` supprimée. **Implémenté runtime + déployé HA** (commit `5892d35`, pull + reload effectués) ; **validation terrain opportuniste en attente**. **Lot CH-4-B (`ALM-IMP-3`, dette/gouvernance) : à traiter.** CH-4 **non clôturé**.
>
> **Statut (dépôt `476116e`) — lot CH-4-B implémenté.** Automatisation morte `11_automations/alarme/sirene/stop.yaml` (ID `1002000000012`) **supprimée** (entité fantôme `switch.sirene_alarm` + `delay` latent + notification morte éliminés ; commit `476116e`). Chemin d'arrêt réel **inchangé** (`script.arret_sirene` = coupe immédiate ; durée device = auto-extinction reboot-safe). `ALM-IMP-3` : **résidu runtime résolu** ; reste la documentation du mécanisme canonique (→ CH-5). **CH-4 : clôture conditionnelle acquise** — réserve unique : **validation terrain de `ALM-MIN-2`**.
>
> **Statut (validation terrain réalisée) — CH-4 SOLDÉ.** Désarmement clavier validé : **un seul bip, aucun double bip** → `ALM-MIN-2` **résolu et validé terrain** ; **réserve levée**. `ALM-IMP-3` résidu runtime déjà résolu (`476116e`). **CH-4 clôturé** (clôture définitive ; cf. clôture CH-4 §10). Dette doc du coupe-circuit canonique → CH-5.

- **Bénéfice attendu** : **faible à moyen** — retrait du code mort (`stop.yaml`, entité fantôme `switch.sirene_alarm`), documentation de la durée device comme coupe-circuit canonique, feedback de désarmement propre (unique, neutralisé en test, hors auto-désarmement).
- **Risque de régression** : **faible** — aucun filet retiré (durée device + `arret_sirene` conservés) ; MIN-2 = feedback.
- **Effort relatif** : **faible** — périmètre localisé.
- **Prérequis** : **V4 réalisée** ; contrats `70`, `00`.
- **Dépendances** : latérale = **CH-1** (satisfaite). **Gate V4 : résolu.**
- **ROI** : **moyen** — petit effort, ferme une dette de gouvernance et nettoie le feedback ; sans urgence.

### CH-5 — Cohérence documentaire & nommage *(DOC-1, DOC-2, MIN-3, MIN-6)*

- **Bénéfice attendu** : **moyen** — fidélité documentaire et opposabilité (contrat d'application restauré), cohérence déclaration↔application (durée de blocage), hygiène de nommage.
- **Risque de régression** : **faible** — aucun impact sur l'actionnement de sécurité.
- **Effort relatif** : **faible**.
- **Prérequis** : contrats `20/30/40`, `60`, `80` ; arbitrage durée de blocage (3 ou 5 min) ; arbitrage notification visiteur (créer ou retirer la clause).
- **Dépendances** : lots de réalignement contractuel **en aval de CH-1/CH-2/CH-3/CH-4** ; lots **DOC-2** et **MIN-6** indépendants.
- **ROI** : **mixte** — lots indépendants à ROI élevé (quick wins) ; lots de réalignement à ROI différé (doivent refléter le runtime final).
>
> **Statut (lot 5-DOC réalisé)** — sous-lot documentaire autonome traité : **contrat `70`** complété (chemin d'arrêt canonique : `arret_sirene` = coupe immédiate ; durée device = auto-extinction reboot-safe ; mention explicite que `stop.yaml` / `switch.sirene_alarm` ne participent plus) ; **en-tête `delai_entree_fin.yaml`** réaligné post-CH-1. Restent : DOC-1, MIN-6, **5-DEC** (MIN-3, DOC-2 — décision métier), **5-S3** (contrats 50/51, post-`S3`).

### CH-6 — Intégrité du flux clavier (PIN) *(CRIT-3)*

- **Bénéfice attendu** : **élevé (conditionnel)** — restaure un chemin d'accès potentiellement totalement inopérant, à faible coût ; nul si V5 montre que le PIN fonctionne déjà.
- **Risque de régression** : **faible à moyen** — surface limitée au clavier PIN ; le badge n'est pas concerné.
- **Effort relatif** : **faible à moyen** — chemin localisé, mécanisme bien compris.
- **Prérequis** : confirmation V5 (le constat est *À confirmer en runtime*) ; en-tête script clavier, contrat `50`.
- **Dépendances** : aucune.
- **ROI** : **élevé (conditionnel)** — petit effort, restauration d'accès, sous réserve de V5.

---

## 🏆 Classement par ROI (décroissant)

1. **CH-2** — levier de déblocage + observabilité, effort modéré → ROI élevé.
2. **CH-6** — restauration d'accès à faible coût (conditionnel V5) → ROI élevé.
3. **CH-5 (lots indépendants)** — DOC-2 / MIN-6 / MIN-3 : cheap, immédiats → ROI élevé.
4. **CH-4** — dette/gouvernance + hygiène feedback (post-V4) → ROI moyen, sans urgence.
5. **CH-3** — bénéfice sécurité, mais gated + dépendant → ROI moyen.
6. **CH-1** — bénéfice maximal mais effort/risque maximaux → ROI moyen (efficience faible, incontournable).
7. **CH-5 (lots de réalignement)** — valeur réelle mais différée (aval) → ROI différé.

---

## ⚠️ Classement par risque de régression (décroissant)

1. **CH-1** — élevé (détection vivante).
2. **CH-3** — moyen (sécurité adjacente, occupants vulnérables).
3. **CH-4** — **faible** (post-V4 : aucun filet retiré ; durée device + `arret_sirene` conservés).
4. **CH-2** — moyen (observabilité, pas d'action directe).
5. **CH-6** — faible à moyen (chemin clavier isolé).
6. **CH-5** — faible (documentaire / hygiène).

---

## 🔗 Classement par dépendances

- **Déclencheurs (aucun amont — à traiter tôt pour débloquer)** :
  - **CH-2** → débloque CH-1 et CH-3 (levier le plus fort).
  - **CH-6** → indépendant, ne bloque rien.
  - **CH-5 (DOC-2, MIN-6)** → indépendants.
- **Intermédiaires (dépendent de CH-2 et/ou couplés)** :
  - **CH-3** (amont CH-2).
  - **CH-1** (amont CH-2 + domaine ouvertures ; latéral CH-4).
  - **CH-4** (latéral CH-1).
- **Terminaux (dépendent de l'aboutissement amont)** :
  - **CH-5 (lots de réalignement contractuel)** — reflètent le runtime stabilisé.

---

## 1️⃣ Ordre optimal de traitement

> Intègre ROI, risque, dépendances **et** priorité de sécurité. La Phase 0 (validations runtime) est la porte d'entrée.

1. **Phase 0 — Constatation** : exécuter V1–V5. Confirmer/infirmer les constats *À confirmer en runtime* et figer les périmètres (notamment escalade possible d'ALM-IMP-1, et engagement réel de CH-6).
2. **CH-2 d'abord** : effort modéré, risque moindre que CH-1, **débloque** CH-1 et CH-3, restaure l'observabilité socle. En parallèle dès la Phase 0 : **quick wins** de CH-5 (DOC-2, MIN-6, MIN-3) et nettoyage du code mort (MIN-4, extractible de CH-2).
3. **CH-6 en parallèle** : dès V5 connue ; restauration d'accès indépendante, faible risque.
4. **CH-3** : après CH-2 ; gated V3.
5. **CH-1** : après CH-2 ; le chantier critique structurant ; gated V1 ; à coordonner avec CH-4.
6. **CH-4** : **V4 réalisée** → dette/gouvernance + hygiène feedback (plus de gate).
7. **CH-5 (lots de réalignement)** : en clôture, pour aligner les contrats sur le runtime final.

> Tension assumée : CH-1 porte l'urgence sécurité maximale mais dépend de CH-2. Résolution : CH-2 est court et débloquant ; on le traite vite pour enchaîner immédiatement sur CH-1. CH-6 (autre critique, indépendant) avance en parallèle.

---

## 2️⃣ Quick wins (lot-level, faible effort / faible risque, valeur immédiate)

- **ALM-DOC-2** (CH-5) — clause notification visiteur : créer ou retirer. Indépendant, documentaire.
- **ALM-MIN-6** (CH-5) — hygiène nom de fichier ↔ entité (sans renommage d'entité). Indépendant.
- **ALM-MIN-3** (CH-5) — trancher la durée de blocage (3 ou 5 min) et aligner la documentation. Décision simple.
- **ALM-MIN-4** (CH-2) — suppression du code mort dans le cerveau (variable inutilisée, condition redondante). Extractible sans attendre l'arbitrage sur la raison.

> Ces quick wins sont des **lots** extraits de leurs chantiers ; ils n'attendent aucune validation runtime et n'ont aucune dépendance amont.

---

## 3️⃣ Chantiers bloqués par validation runtime

> Périmètre / engagement conditionnés par une confirmation à chaud avant exécution.

| Chantier | Gate | Conséquence de la validation |
|----------|------|------------------------------|
| **CH-1** | V1 (course détection) | Détermine l'ampleur de la refonte de frontière |
| **CH-3** | V3 (présence en babysitting) | Conditionne l'escalade d'ALM-IMP-1 et le choix d'inhibition |
| **CH-4** | V4 (entité sirène / durée / reboot) — **réalisée** | Coupe-circuit assuré **reboot-safe** côté device ; `ALM-IMP-3` requalifié Mineur ; CH-4 = dette/gouvernance |
| **CH-6** | V5 (test PIN réel) | Engage ou annule le chantier (si PIN fonctionnel → sans objet) |

> **CH-2** n'est **pas bloqué** : V2 est confirmatoire (le constat est déjà *Confirmé* statiquement). **CH-5** n'est pas bloqué par une validation runtime ; ses lots de réalignement sont seulement en aval des chantiers amont (revue finale).

---

## 4️⃣ Chantiers / lots préparables immédiatement

> Démarrables sans attendre les validations runtime (analyse, doctrine, arbitrage, lecture des contrats, ou exécution pour les lots non gatés).

- **CH-2 (intégral)** — arbitrage doctrinal sur l'autorité de la raison + exécution du nettoyage de code mort (MIN-4). Aucun gate bloquant.
- **CH-5 (lots indépendants)** — DOC-2, MIN-6, MIN-3 : exécutables immédiatement.
- **Préparation (doctrine / arbitrage / lecture contrats) des chantiers gatés** : CH-1, CH-3, CH-4 et CH-6 peuvent être **instruits** (cible visée, arbitrages, prérequis documentaires) **pendant** que V1–V5 sont menées — seule l'**exécution** est suspendue à la validation.

---

## 🧾 Synthèse

| Chantier | Bénéfice | Risque régression | Effort | ROI | Dépend de | Gate runtime | Préparable maintenant |
|----------|:--------:|:-----------------:|:------:|:---:|-----------|:------------:|:---------------------:|
| CH-2 | élevé | moyen | moyen | **élevé** | — | V2 (confirmatoire) | ✅ intégral |
| CH-6 | élevé (cond.) | faible-moyen | faible-moyen | **élevé (cond.)** | — | **V5 (bloquant)** | ✅ préparation |
| CH-5 (indép.) | moyen | faible | faible | **élevé** | — | — | ✅ exécutable |
| CH-4 | faible-moyen | **faible** | faible | moyen | ⟂ CH-1 | **V4 résolu** | ✅ exécutable |
| CH-3 | élevé | moyen | moyen | moyen | CH-2 | **V3 (bloquant)** | ✅ préparation |
| CH-1 | maximal | **élevé** | **élevé** | moyen | CH-2 + ouvertures | **V1 (bloquant)** | ✅ préparation |
| CH-5 (réalign.) | moyen | faible | faible | différé | CH-1/2/3/4 | revue finale | ⏳ aval |

---

*Fin du backlog priorisé. Aucun code, aucun YAML, aucune correction. Les arbitrages (rôle du babysitting, durée de blocage, source « visite active », mécanisme d'extinction sirène, autorité de la raison) restent ouverts et conditionnent le périmètre exact des chantiers.*
