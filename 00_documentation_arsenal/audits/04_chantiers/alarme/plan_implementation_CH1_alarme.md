# Plan d'implémentation — CH-1 Alarme

> **Chantier :** CH-1 — Sémantique des ouvrants d'entrée & confirmation d'intrusion
> **Arbitrage fixé (non rediscuté) :** **A1** + **B2** + **C1**
> **Constats traités :** **ALM-CRIT-1**, **ALM-CRIT-2**, **ALM-MIN-5**
> **Sources :** `04_chantiers/alarme/dossier_conception_CH1_alarme.md`, `01_rapports/alarme/audit_alarme_rapport_officiel.md`, dépôt réel `origin/main` = `99cbc0b`
> **Nature :** plan d'implémentation — **analyse, ordre, validations**. Aucun YAML, aucun patch, aucun code, aucune correction rédigée, aucun changement du dépôt.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

**Rappel des décisions :**
- **A1** — Sortir la porte d'entrée et le garage du **chemin immédiat** (`autres.yaml`). Ils ne sont plus couverts que par le **délai d'entrée**.
- **B2** — `timer.finished` (sur `timer.delai_entree`) constitue **à lui seul** la preuve d'une intrusion non désarmée : le garde d'ouverture instantanée disparaît de la **fin de délai**.
- **C1** — La sirène n'est plus appelée directement par la fin de délai ; **chemin sonore unique** via l'état `triggered` → `sirene_forte`.

---

## 1. Fichiers impactés

### 1.1 Runtime (2 fichiers, 3 changements)

| # | Fichier | Changement (descriptif) | Décision |
|---|---------|--------------------------|----------|
| F1 | `11_automations/alarme/intrusion/ouverture/autres.yaml` (`1002000000007`) | Retirer **deux** déclencheurs d'état : `binary_sensor.contact_entree_porte` et `binary_sensor.contact_garage`. Conserver les cinq autres (chambres Arnaud / Matthieu / parents, séjour, entrée-fenêtre), **toutes** les conditions (`capteur valide`, `armed_away`, `delai_desarmement_en_cours == off`) et **toutes** les actions (bifurcation mode test inchangée). Aligner l'en-tête (le rôle ne couvre plus les ouvrants d'entrée). | A1 |
| F2 | `11_automations/alarme/intrusion/ouverture/delai_entree_fin.yaml` (`10020000000032`) | **B2** : retirer la condition `binary_sensor.ouverture_qualifiee_maison == on` ; **conserver** les gardes `input_boolean.systeme_stable == on` et `alarm_control_panel.alarme_maison == armed_away`. **C1** : retirer l'action directe `script.sirene_brutale` (et le bloc `choose` mode-test qui la porte) ; **conserver** `alarm_trigger` et la notification critique. Aligner l'en-tête (robustesse : suppression du garde d'ouverture ; suppression de l'appel sirène direct ; dette §9 réduite). | B2 + C1 |

### 1.2 Fichiers à NE PAS modifier (vérifiés)

- `12_template_sensors/ouvertures/ouverture_qualifiee_maison.yaml` — **conservé tel quel** : il reste consommé par l'aération/M5 (`11_automations/aeration/blocage_chauffage/pipeline.yaml`, `11_automations/ouvertures/qualification_aeration.yaml`). B2 supprime seulement **sa lecture par l'alarme**, pas le capteur.
- `11_automations/alarme/sirene/sirene_forte.yaml` (`1002000000011`) — **inchangé** : devient l'**unique** déclencheur de `script.sirene_brutale` (garde mode test conservée).
- `10_scripts/alarme/sirene/brutale.yaml` — inchangé (action terminale).
- `11_automations/alarme/intrusion/ouverture/delai_entree_start.yaml` (`10020000000031`) — inchangé : reste le **seul** point d'entrée du délai (front `off→on` sur `alarme_ouverture_entree`/`alarme_ouverture_garage`).
- `11_automations/alarme/timer_cancel.yaml` (`10020000000033`) — inchangé : annule `timer.delai_entree` au désarmement (socle de validité de B2).
- `11_automations/alarme/intrusion/mouvement.yaml` (`1002000000009`) — inchangé : couverture résiduelle.
- `12_template_sensors/alarme/{ouvrants_entree, delai_desarmement}.yaml`, `08_timers/alarme/delai_entree.yaml`, `03_input_numbers/alarme/delai_desarmement.yaml` — inchangés.

> **Aucun nouveau helper, aucun capteur supprimé, aucun timer modifié.** La surface runtime de CH-1 se réduit à **deux automations**.

---

## 2. Contrats impactés (identification — alignement documentaire, sans rédaction ici)

| Contrat | Élément concerné | Effet de l'arbitrage |
|---------|------------------|----------------------|
| `50_intrusion_detection.md` | l.57 garde `ouverture_qualifiee_maison` de `…032` ; l.58 action `sirene_brutale` ; l.118 liste des appelants de `sirene_brutale` ; l.137‑142 §9 ; l.161 table « confirmation intrusion active » ; l.164 ; l.75 « hors ouvrants d'entrée » | **B2** invalide la l.57 et la l.161 ; **C1** invalide la l.58, met à jour la l.118 (appelant unique) et **réduit** la §9 (le court-circuit *sirène* de `…032` disparaît) ; **A1** met le runtime **en conformité** avec la l.75 déjà existante. **Contrat principal à aligner.** |
| `51_ouvrants_entree.md` | rôle des ouvrants d'entrée | **A1** : confirmer que porte/garage sont couverts **exclusivement** par le délai. Alignement de confirmation. |
| `60_delais_et_blocages.md` | sémantique de fin de délai | **B2** : documenter que `timer.finished` + `systeme_stable` + `armed_away` **suffit** à confirmer (plus de garde d'ouverture). |
| `70_sirene_actions_terminales.md` | déclenchement terminal sirène | **C1** : sirène pilotée **uniquement** par l'état `triggered` → `sirene_forte`. |

> **Hors scope contractuel de CH-1 :** la §9 conserve un volet **non traité** — l'appel **direct** de `alarm_trigger` par `…007`, `…009`, `…032` (court-circuit Décision→Helpers→Application). **C1 ne supprime que le doublon *sonore***, pas le court-circuit panneau (qui relèverait d'une refonte type B3, **non retenue**). Ce point reste une dette documentée, **inchangée**.

L'alignement des contrats suit la règle « le contrat documente le runtime » : il est réalisé **après** la bascule runtime, en lot documentaire dédié (cf. §5, Lot 4), sans aucune réécriture dans le présent plan.

---

## 3. Dépendances impactées

- **`ouverture_qualifiee_maison`** : perd son **unique** consommateur d'intrusion (`delai_entree_fin`) ; conserve ses consommateurs **aération/M5**. → Aucune régression M5 (à vérifier en statique, §8).
- **`script.sirene_brutale`** : passe de **deux** appelants (`delai_entree_fin`, `sirene_forte`) à **un** (`sirene_forte`). → Élimination du doublon (MIN-5).
- **Couverture de la voie d'entrée** : transférée intégralement du chemin immédiat vers le **chemin temporisé** (`delai_entree_start` → `timer.delai_entree` → `delai_entree_fin`). → La justesse du délai devient **critique** ; A1 et B2 sont **co-dépendants** (cf. §5).
- **Cycle de vie du timer** : `timer_cancel` (désarmement) garantit que `timer.finished` n'advient **que** sans désarmement → socle de B2.
- **Inter-chantiers** : amont = **CH-2** (soldé) ; latéral = **CH-4** (sirène) ; aval documentaire = **CH-5** (contrats 50/51/60/70) ; externe = domaine **ouvertures** (non touché).

---

## 4. Vérification d'élimination des constats (exigence explicite)

### 4.1 ALM-CRIT-1 (faux positif immédiat) — **éliminé par A1**
La porte et le garage ne sont **plus** des déclencheurs de `autres.yaml`. Le chemin immédiat n'observe plus la voie d'entrée ⇒ **la course** entre la chaîne du timer et le garde `delai_desarmement_en_cours` **n'a plus d'objet** pour les ouvrants d'entrée (il n'existe plus de chemin immédiat susceptible de déclencher à l'ouverture de la porte). Une entrée légitime ne peut plus produire de déclenchement instantané. ✅

### 4.2 ALM-CRIT-2 (faux négatif à l'expiration) — **éliminé par B2**
La fin de délai ne dépend plus de `ouverture_qualifiee_maison` (qui excluait structurellement porte/garage). Comme `timer_cancel` annule le timer au désarmement, atteindre `timer.finished` **encode déjà** « ouvrant d'entrée ouvert en `armed_away` **et** aucun désarmement ». Le déclenchement est donc émis (gardes `systeme_stable` + `armed_away` conservées). L'intrusion par la voie principale est **sanctionnée**, ouvrant refermé ou non. ✅

### 4.3 ALM-MIN-5 (double sirène) — **éliminé par C1**
`delai_entree_fin` n'appelle plus `sirene_brutale` directement. La sirène est émise **une seule fois**, via `alarm_trigger` → état `triggered` → `sirene_forte` → `sirene_brutale`. ✅

### 4.4 Absence de **nouvelle fenêtre aveugle** — **vérifiée**
- **Pendant le délai** : `autres.yaml` (ouvrants restants) et `mouvement.yaml` restent inhibés comme avant (grâce volontaire). **Inchangé.**
- **À l'expiration** : B2 déclenche dès `timer.finished` (plus de condition bloquante). La fenêtre où l'intrusion d'entrée n'était pas sanctionnée (CRIT-2) est **fermée**, pas déplacée.
- **Après l'expiration** : `autres.yaml` (ouvrants restants) et `mouvement.yaml` redeviennent actifs comme avant. **Inchangé.**
- **Ouvrants non-entrée** : toujours couverts par le chemin immédiat (déclencheurs conservés). **Inchangé.**
- **Reboot / restore** : garde `systeme_stable` conservée ; `timer.delai_entree` `restore: true` inchangé. **Inchangé.**
- **Concurrence** : seconde ouverture d'entrée pendant un délai actif ⇒ `delai_entree_start` reste bloqué par sa condition `timer idle`, mais le timer en cours ira à `finished` ⇒ déclenchement. Pas de double timer, pas de trou.
- **Bord préexistant non introduit par CH-1** : armement avec porte **déjà** ouverte (aucune transition `off→on`) ⇒ pas de démarrage de délai. Comportement **antérieur**, **non modifié** par A1/B2/C1 ; signalé pour mémoire (candidat hors périmètre). ✅

---

## 5. Ordre des modifications, lots et granularité de commits

> **Règle de sûreté impérative :** **A1 et B2 sont co-dépendants** et **doivent être déployés ensemble** (un seul rechargement). Déployer A1 **sans** B2 transférerait toute la voie d'entrée vers une fin de délai encore aveugle (CRIT-2) → aggravation du faux négatif. **Interdit.**

### Lots
- **Lot 1 — A1** (`autres.yaml`) : retrait des deux déclencheurs d'entrée. Élimine CRIT-1.
- **Lot 2 — B2** (`delai_entree_fin.yaml`) : retrait du garde `ouverture_qualifiee_maison`. Élimine CRIT-2.
- **Lot 3 — C1** (`delai_entree_fin.yaml`) : retrait de l'appel sirène direct. Élimine MIN-5.
- **Lot 4 — Documentaire** : alignement des contrats `50` (principal), `51`, `60`, `70` + clôture CH-1. Aucun runtime.

### Granularité de commits (recommandée)
Trois commits runtime atomiques, **un seul déploiement** :
1. `fix(alarme): retirer les ouvrants d'entrée du chemin immédiat (CH-1 / ALM-CRIT-1)` — F1.
2. `fix(alarme): fin de délai = preuve d'intrusion, sans garde d'ouverture (CH-1 / ALM-CRIT-2)` — F2 (B2).
3. `refactor(alarme): chemin sonore unique en fin de délai (CH-1 / ALM-MIN-5)` — F2 (C1).

Puis un commit documentaire séparé (Lot 4). Les commits 1 et 2 sont **indissociables au déploiement** ; le commit 3 est indépendant.

### Séquence de bascule
1. Appliquer les trois lots runtime (clone vierge).
2. Validations statiques (§8).
3. `git apply --check` séquentiel sur base propre.
4. Pousser les commits 1‑3 **ensemble** ; `git pull` runtime ; **recharger automations** (un seul reload).
5. Validations runtime (§9).
6. Lot 4 (documentaire) une fois la bascule validée.

---

## 6. Stratégie de rollback

- **Sans migration de données** : aucun helper, aucun schéma d'état ; le timer et les capteurs sont inchangés. Le rollback est un simple revert + reload.
- **Granularité :**
  - **Commit 3 (C1)** : **réversible seul** (réintroduit le doublon sirène, sans risque de sécurité).
  - **Commits 1 + 2 (A1 + B2)** : **réversibles uniquement ensemble** (retour au comportement antérieur). **Ne jamais** réverter A1 seul (laisserait la fin de délai aveugle) ni B2 seul (réintroduirait CRIT-2 avec une voie d'entrée désormais sans chemin immédiat).
- **Rollback atomique total** : revert des deux fichiers à l'état pré-CH-1 + reload.
- **Critères de déclenchement :** faux positif/négatif observé sur la voie d'entrée ; erreur de parsing au reload ; sirène muette en réel (échec `sirene_forte`) ; double sirène persistante.
- **État de référence :** commit/tag pris **avant** CH-1.

---

## 7. Risques de régression

| Réf | Risque | Mitigation |
|-----|--------|------------|
| RG1 | Déploiement A1 sans B2 (ou inverse) → aggravation voie d'entrée | Règle de co-déploiement §5 ; commits 1+2 indissociables |
| RG2 | Ouvrant d'entrée non détecté si le délai ne démarre pas (porte déjà ouverte à l'armement) | Bord **préexistant**, non introduit ; à documenter (hors périmètre) ; couvert partiellement par mouvement après expiration |
| RG3 | `timer.finished` spurious (reboot/restore) → faux déclenchement | Garde `systeme_stable` conservée ; `restore: true` inchangé ; valider S après reboot |
| RG4 | C1 → sirène muette en réel | `sirene_forte` (garde mode test off) reste l'émetteur ; valider S3/S6 |
| RG5 | Mode test : `alarm_trigger` en test fait passer le panneau à `triggered` | **Préexistant** (inchangé par C1) ; sirène inhibée en test via `sirene_forte` ; signalé hors périmètre |
| RG6 | B2 casse un autre consommateur d'intrusion de `ouverture_qualifiee_maison` | Vérifié : seul consommateur intrusion = `delai_entree_fin` ; reste = aération/M5 ; grep statique §8 |
| RG7 | Dérive contrat/runtime tant que Lot 4 non fait | Lot 4 planifié immédiatement après bascille ; principe « contrat documente le runtime » |
| RG8 | Couverture mouvement modifiée | `mouvement.yaml` **non touché** ; vérifier S5/S8 |

---

## 8. Validations statiques (avant déploiement)

- **T1** — Parse YAML des deux fichiers ; `yamllint` (config dépôt).
- **T2** — `git apply --check` séquentiel des trois commits sur base propre.
- **T3 (A1)** — Confirmer l'**absence** de `binary_sensor.contact_entree_porte` et `binary_sensor.contact_garage` dans les déclencheurs de `autres.yaml`, et la **présence** des cinq autres + conditions + actions inchangées.
- **T4 (B2)** — Confirmer l'**absence** de toute référence à `ouverture_qualifiee_maison` dans `delai_entree_fin.yaml` ; **présence** conservée de `systeme_stable` et `armed_away`.
- **T5 (C1)** — Confirmer l'**absence** de `script.sirene_brutale` dans `delai_entree_fin.yaml` ; appelant **unique** de `sirene_brutale` = `sirene_forte` (grep global).
- **T6** — Confirmer que `ouverture_qualifiee_maison` conserve ses consommateurs aération/M5 (grep) ; capteur **non modifié**.
- **T7** — IDs d'automations **inchangés** (`1002000000007`, `10020000000032`).
- **T8** — `Check configuration` Home Assistant.
- **T9** — Chaîne CI contrats Arsenal (`tools/arsenal_ci` / `scripts/arsenal_contracts`) sur le domaine alarme.

---

## 9. Validations runtime (après déploiement)

Scénarios à exécuter en environnement réel (mode test selon indication) :

- **S1 (CRIT-1)** — `armed_away`, ouverture **porte** : aucun déclenchement immédiat ; `timer.delai_entree` démarre ; bip (hors test). **Attendu : pas d'`alarm_trigger` à l'ouverture.**
- **S2 (désarmement à temps)** — porte → délai actif → désarmement → `timer_cancel` → `idle` → **aucun déclenchement**.
- **S3 (CRIT-2)** — porte → délai → **pas** de désarmement → `timer.finished` (`systeme_stable` on, `armed_away`) → `alarm_trigger` → `triggered` → sirène **une fois**, **même porte refermée**.
- **S4 (garage)** — répéter S1/S3 via le **garage**.
- **S5 (ouvrant non-entrée)** — `armed_away`, ouverture **fenêtre séjour** hors délai → `autres.yaml` déclenche **immédiatement** (chemin immédiat conservé).
- **S6 (MIN-5)** — à l'expiration, vérifier **une seule** invocation de `sirene_brutale` (via `sirene_forte` uniquement).
- **S7 (mode test)** — porte → délai (bip inhibé) → `finished` en test → panneau `triggered` mais **aucune sirène réelle** (garde `sirene_forte`).
- **S8 (non-régression / fenêtre aveugle)** — mouvement pendant le délai = inhibé ; mouvement après expiration = déclenche ; reboot pendant le délai → garde `systeme_stable` ; seconde ouverture d'entrée pendant délai actif → pas de double timer, déclenchement à l'échéance.

---

## 10. Synthèse

CH-1 se réalise par **deux automations** et **trois changements** :
- **A1** ferme CRIT-1 (les ouvrants d'entrée quittent le chemin immédiat) ;
- **B2** ferme CRIT-2 (`timer.finished` = preuve, garde d'ouverture supprimé) ;
- **C1** ferme MIN-5 (chemin sonore unique).

Aucune nouvelle fenêtre aveugle n'est introduite (§4.4). La contrainte de sûreté centrale est le **co-déploiement A1 + B2**. L'alignement des contrats `50`/`51`/`60`/`70` (Lot 4) suit la bascule. La dette §9 résiduelle (court-circuit `alarm_trigger`) reste **hors périmètre** et inchangée.

---

*Plan d'implémentation CH-1 Alarme. Établi en lecture du dépôt (`origin/main` = `99cbc0b`) et du dossier de conception CH-1. Analyse, ordre et validations uniquement — aucun YAML, aucun patch, aucun code, aucune correction, aucun changement du dépôt. Arbitrage A1 + B2 + C1 considéré comme décidé.*
