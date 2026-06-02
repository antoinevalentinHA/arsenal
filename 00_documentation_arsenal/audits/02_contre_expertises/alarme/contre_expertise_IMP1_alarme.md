# Contre-expertise — ALM-IMP-1 (babysitting & décision d'armement)

> **Statut :** contre-expertise de constat — `ALM-IMP-1` **requalifié Important 🟠 → Mineur 🟡** ; facette « armement automatique en babysitting » **INVALIDÉE par le runtime** ; chantier **CH-3 dissous → fusionné dans CH-5** ; domaine **Alarme NON clôturé**.
> **Domaine :** `alarme` — contextes humains (babysitting), décision centrale, diagnostic de cohérence.
> **Destination d'archivage :** `00_documentation_arsenal/audits/02_contre_expertises/alarme/contre_expertise_IMP1_alarme.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/backlog_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/etat_post_CH6.md`
> - `00_documentation_arsenal/audits/03_plans_action/alarme/plan_action_alarme.md`
> **État du dépôt à la rédaction :** `origin/main` = `92b2ede`.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Réexaminer `ALM-IMP-1` (« Babysitting demi-intégré : neutralise le diagnostic, n'inhibe pas la décision ») à la lumière du runtime, statuer sur la validité de sa prémisse centrale, proposer sa nouvelle qualification, et déterminer le sort du chantier **CH-3** qui le portait. Acte documentaire — aucune modification runtime, contrat ou CI.

---

## 2. Constat initial (rappel)

`ALM-IMP-1` affirmait : `decision_centrale.yaml` ne lit pas `mode_babysitting` et `coherence.yaml` force « cohérent » en babysitting ; donc si la présence sécurité retombe à `off` pendant qu'un baby-sitter et des enfants sont présents, le cerveau pourrait décider `ARMEMENT_AUTORISE` **sans alerte de cohérence** → armement automatique en présence humaine non tracquée. Gravité **Important**, escalade **Critique** envisagée (gated **V3**).

---

## 3. Hypothèse infirmée

La **prémisse centrale** — « babysitting n'inhibe pas la décision » — est **fausse dans le runtime**. L'audit initial a examiné `decision_centrale.yaml` et `coherence.yaml`, mais a **omis `11_automations/modes/babysitting/activation.yaml`**, qui établit l'inhibition par un chemin indirect.

---

## 4. Preuves de code (dépôt `92b2ede`)

Chaîne d'inhibition, vérifiée fichier par fichier :

| # | Fichier (ligne) | Fait |
|---|-----------------|------|
| P1 | `11_automations/modes/babysitting/activation.yaml` (L69, L80-81) | sur `mode_babysitting → on`, **force** `input_boolean.presence_arnaud` + `presence_matthieu` à `on` |
| P2 | `12_template_sensors/presence/enfants.yaml` (L19, L25-26) | `binary_sensor.presence_enfants` = OU(`presence_arnaud`, `presence_matthieu`) |
| P3 | `12_template_sensors/presence/securite/presence.yaml` (L63) | `presence_famille_securite` inclut `presence_enfants` |
| P4 | `10_scripts/alarme/decision_centrale.yaml` (L85-86, L103-104, L96) | `elif presence_securite → PRESENCE` ; `PRESENCE → DISARMED` ; `ARMEMENT_AUTORISE` seulement sinon ; **0** lecture de `mode_babysitting` |
| P5 | `12_template_sensors/alarme/coherence.yaml` (L39, L52) | force « cohérent » si `mode_babysitting == on` (dépendance diagnostic ↔ mode) |

**Conclusion de chaîne :** `mode_babysitting=on` ⇒ (P1) présence enfants forcée ⇒ (P2-P3) `presence_famille_securite=on` ⇒ (P4) décision `PRESENCE` ⇒ `etat_cible = DISARMED`. L'armement automatique est **structurellement empêché** pendant le babysitting. Concordant avec l'observation terrain (« l'alarme ne s'arme pas en babysitting »).

---

## 5. Analyse (réponses aux questions de gouvernance)

- **A. Le risque d'armement automatique en babysitting existe-t-il dans le runtime ?** **Non** (P1→P4). *Réserve : cas-limite théorique — booléens de présence retoggés manuellement / course au reload — non observé, hors cadre « babysitting actif ».*
- **B. La description d'`ALM-IMP-1` est-elle factuellement correcte ?** **Partiellement** : les faits atomiques (P4 « ne lit pas `mode_babysitting` », P5 « force cohérent ») sont exacts, mais la **prémisse/impact** (« n'inhibe pas la décision » → armement possible) est **fausse** (omission de P1).
- **C. « Important » est-il défendable ?** **Non** : la gravité reposait sur un risque de sécurité réalisable, **réfuté**. Escalade Critique **écartée**.
- **D. Résidu concret réel ?** Deux, **Mineurs / gouvernance**, sans impact sécurité : **(1)** diagnostic dépendant de `mode_babysitting` (**violation du contrat `96`**, P5), effet **bénin** (aucun armement à masquer) ; **(2)** inhibition **implicite** (effet de bord du forçage de présence) vs inhibiteur **explicite** attendu (contrat `99`) — écart de représentation + fragilité **théorique** non observée.

---

## 6. Nouvelle qualification proposée

**`ALM-IMP-1` : Important 🟠 → Mineur 🟡.** Énoncé requalifié : « Babysitting : inhibition **implicite** de la décision (via forçage de présence enfants) + diagnostic dépendant du mode (contrat `96`) ; facette *armement automatique* **invalidée** par le runtime. » Identifiant `ALM-IMP-1` **conservé** (stable) ; traçabilité par repère sous « Constats importants » + bannières.

Comparaison des options : **maintien Important** — non soutenable (risque réfuté) ; **clôture sèche** — recevable seulement si scindée, sinon perd le fil du contrat `96` ; **rétrogradation Mineur (reformulée)** — retenue : retire la gravité infondée et conserve les résidus à suivre.

---

## 7. Détermination du chantier CH-3

CH-3 (« Contextes humains & câblage ») portait `ALM-IMP-1` (sa raison d'être « angle mort sécurité babysitting ») et `ALM-MIN-1` (câblage visite, atténué).

- Le **bénéfice « élevé — angle mort sécurité »** est **caduc** : il n'y a pas d'angle mort.
- L'**arbitrage central** (« le babysitting doit-il inhiber l'armement ? ») est **déjà tranché par le runtime** (oui, implicitement).
- La gate **V3** est **répondue** par le code + le terrain : la présence est couverte en babysitting.
- Les résidus survivants sont **documentaires / câblage** (contrats `96`/`99` ; réalignement de déclencheur MIN-1) — registre **CH-5**.

**Décision : CH-3 est DISSOUS et FUSIONNÉ dans CH-5.** `ALM-IMP-1` (requalifié Mineur, résidus contrats `96`/`99`) et `ALM-MIN-1` (câblage visite) y sont **reversés**. *(Options écartées : rétrogradation de CH-3 en chantier Mineur distinct — redondant, les résidus sont du registre CH-5 ; clôture de CH-3 — laisserait les résidus sans porteur.)*

---

## 8. Verdict

**`ALM-IMP-1` requalifié Important → Mineur** ; facette « armement automatique en babysitting » **invalidée par le runtime** (preuves P1→P4) ; deux résidus Mineurs de gouvernance (contrats `96`/`99`) à porter par **CH-5**. **CH-3 dissous, fusionné dans CH-5.** Décision applicable **sans validation terrain supplémentaire** (V3 répondue). Domaine **Alarme non clôturé**. Aucune correction runtime requise ni proposée.

---

*Contre-expertise `ALM-IMP-1`. Établie en lecture du dépôt (`origin/main` = `92b2ede`) et de l'observation terrain fournie. Acte documentaire — aucune modification runtime, aucun contrat, aucune CI.*
