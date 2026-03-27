# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     CHAUFFAGE — AUTO-AJUSTEMENT DE LA COURBE DE CHAUFFE (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — CALIBRATION THERMIQUE SUPERVISÉE
#
# 📋 VERSION : 2.1
# 📅 MISE À JOUR : 2026-03-27
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   d'**auto-ajustement de la courbe de chauffe** du sous-système Chauffage Arsenal.
#
#   Il formalise la gouvernance officielle de la calibration thermique :
#     • pente de courbe,
#     • parallèle de courbe,
#     • conditions d'apprentissage,
#     • frontières décision / exécution / diagnostic.
#
#   Il est OPPOSABLE à toute implémentation :
#     • capteurs de suggestion,
#     • automations décisionnelles,
#     • scripts d'application,
#     • UI de réglage,
#     • mécanismes d'apprentissage.
#
#   Subordonné à :
#     /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif du mécanisme
d'**auto-ajustement de la courbe de chauffe**.

Il formalise :

- la finalité réelle de la calibration thermique,
- les conditions légitimes d'apprentissage,
- la séparation stricte proposition / décision / exécution,
- les garde-fous d'immunité thermique,
- les interdictions absolues,
- la distinction entre domaine physique et domaine d'auto-ajustement.

Ce mécanisme constitue une **calibration supervisée lente**,  
et non un pilotage adaptatif autonome.

---

# ----------------------------------------------------------
# 🧠 2. FINALITÉ RÉELLE DE L'AUTO-AJUSTEMENT
# ----------------------------------------------------------

L'auto-ajustement ne vise PAS :

- une régulation adaptative en boucle fermée,
- une optimisation temps réel,
- une compensation automatique d'erreur instantanée,
- une décision thermique autonome,
- un pilotage direct de la chaudière.

Il vise exclusivement :

- corriger lentement la loi de chauffe globale,
- stabiliser la qualité de confort long terme,
- réduire les dérives structurelles de réglage,
- assister le réglage utilisateur de manière objective.

Objectif fondamental :

> 🧠 **Améliorer durablement la loi de chauffe  
> sans jamais créer de boucle thermique autonome.**

---

# ----------------------------------------------------------
# 🧱 3. POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------

L'auto-ajustement :

- est hors décision centrale,
- ne modifie jamais un mode thermique,
- ne produit jamais une autorisation,
- ne pilote jamais directement un service.

Il agit exclusivement sur :

- `input_number.chauffage_pente_consigne`
- `input_number.chauffage_parallele_consigne`

via une chaîne stricte à six étapes — détaillée au §6 :

1. **Qualification du signal** (représentativité thermique + immunité poêle)
2. **Capteurs diagnostiques gouvernés**
3. **Capteurs de proposition (`*_suggeree`)**
4. **Automation décisionnelle supervisée**
5. **Écriture helpers consigne → Scripts d'application**
6. **Journalisation événementielle**

Il est :

- post-décisionnel
- non critique temps réel
- strictement supervisé

---

# ----------------------------------------------------------
# 🧠 4. GRANDEURS CANONIQUES UTILISÉES
# ----------------------------------------------------------

Grandeurs de base autorisées :

- écart consigne instantané (régime doux / froid)
- moyenne glissante 24 h de l'écart
- moyennes spécialisées doux / froid
- température extérieure locale
- température intérieure minimale gouvernée

Grandeurs interdites :

- présence
- géolocalisation
- puissance chaudière
- durée de marche
- états cloud instables
- capteurs non gouvernés

Principe :

> ⚠️ Toute calibration doit être fondée exclusivement  
> sur des écarts thermiques mesurés gouvernés.

---

# ----------------------------------------------------------
# 🧠 5. SÉMANTIQUE DES PARAMÈTRES DE COURBE
# ----------------------------------------------------------

## 5.1 Parallèle de courbe (offset)

Rôle :

- corriger un biais thermique global
- agir principalement en régime doux
- déplacer verticalement la loi de chauffe

Grandeur de référence :

- `sensor.ecart_consigne_moyenne_24h`
- `sensor.ecart_consigne_moyenne_doux`

Effet autorisé :

- translation lente de la courbe
- correction fine de confort stationnaire

---

## 5.2 Pente de courbe

Rôle :

- corriger la réponse thermique en régime froid
- ajuster la sensibilité extérieure / intérieure
- stabiliser le comportement hivernal

Grandeur de référence :

- `sensor.ecart_consigne_moyenne_froid`
- `sensor.ecart_consigne_instantane_froid`

Effet autorisé :

- modification lente de la loi de chauffe globale
- correction structurelle en conditions sévères

---

## 5.3 Distinction normative — Domaine physique vs auto-ajustement

Deux domaines distincts sont définis :

### Domaine physique chaudière (référence absolue)

Correspond aux capacités réelles du système thermique :

- pente : **0.2 → 3.5**, pas **0.1**
- parallèle : **-13 → 40**, pas **1**

Ces bornes :

- sont définies par le constructeur (source : `CONTRAT_MQTT.md` §11)
- sont utilisées par :
  - le bridge MQTT
  - les scripts d'exécution
  - les helpers `input_number`
- constituent la **frontière d'exécution matérielle**

---

### Domaine d'auto-ajustement Arsenal (politique)

Correspond à la zone dans laquelle le système est autorisé à apprendre :

- pente : **1.0 → 2.2**
- parallèle : **-8 → 8**

Ces bornes :

- sont définies par la gouvernance Arsenal
- sont utilisées exclusivement par :
  - les capteurs de suggestion
  - la logique d'apprentissage
- sont volontairement plus restrictives que le domaine physique

---

Principe fondamental :

> ⚠️ L'auto-ajustement n'a PAS le droit d'explorer l'ensemble du domaine physique.

---

Conséquences :

- une consigne peut exister hors domaine d'auto-ajustement (réglage manuel, migration)
- mais aucune suggestion ne doit en sortir
- aucune logique d'apprentissage ne doit franchir cette frontière

**Règle normative — consigne hors domaine d'auto-ajustement :**

Si la consigne courante est hors domaine d'auto-ajustement Arsenal :

- aucune suggestion ne doit être produite
- le capteur de suggestion DOIT retourner la valeur courante inchangée
- aucun mouvement de retour progressif n'est autorisé

> ⚠️ Un retour progressif vers le domaine d'auto-ajustement constitue une violation.
> Il produit des suggestions implicites non gouvernées, indétectables par la couche décision.

---

# ----------------------------------------------------------
# 🧠 6. CHAÎNE NORMATIVE D'AUTO-AJUSTEMENT
# ----------------------------------------------------------

Chaîne obligatoire :

1. **Qualification du signal**
   - évaluation de la représentativité thermique (`input_select.chauffage_representativite_thermique`)
   - évaluation de l'immunité poêle (`binary_sensor.signature_thermique_poele`)
   - toute condition bloquante à cette étape interrompt la chaîne — aucune suite n'est exécutée

2. **Capteurs diagnostiques gouvernés**
   - calcul des écarts thermiques gouvernés
   - production des moyennes glissantes (24 h, doux, froid)

3. **Capteurs de proposition (`*_suggeree`)**
   - production de valeurs bornées au domaine d'auto-ajustement Arsenal
   - aucune valeur hors domaine d'auto-ajustement ne peut être produite à cette étape

4. **Automation décisionnelle supervisée**
   - vérification des conditions d'autorisation (§7)
   - décision unique, centralisée
   - aucun calcul de suggestion ici

5. **Écriture helpers consigne → Scripts d'application**
   - l'automation écrit `input_number.chauffage_pente_consigne` et/ou `input_number.chauffage_parallele_consigne`
   - les scripts d'application lisent ces helpers et appliquent la commande via MQTT
   - les scripts d'application **DOIVENT** garantir la conformité au domaine physique chaudière
     avant toute émission MQTT — cette vérification est obligatoire et non délégable
   - toute émission hors domaine physique constitue une **violation du contrat**
   - aucun script ne décide une valeur

6. **Journalisation événementielle**
   - production obligatoire d'un événement traçable
   - entrée logbook explicite
   - voir §11 pour les champs normatifs

Interdictions absolues :

- aucun capteur n'écrit directement un paramètre
- aucune automation ne calcule une suggestion
- aucun script ne décide une valeur
- aucune boucle fermée n'est autorisée
- aucune suggestion ne peut sortir du domaine d'auto-ajustement Arsenal

Principe cardinal :

> 🔒 **La décision est unique, centralisée et supervisée.**

---

# ----------------------------------------------------------
# 🛑 7. CONDITIONS D'AUTORISATION LÉGITIMES
# ----------------------------------------------------------

L'auto-ajustement est autorisé uniquement si toutes les conditions suivantes sont satisfaites,
dans l'ordre d'évaluation indiqué :

1. **état de représentativité thermique = REPRESENTATIF** ← précondition prioritaire (§8)
2. **aucune signature thermique poêle active ou récente** ← verrou d'immunité (§9)
3. auto-ajustement activé explicitement
4. régime maison = Normal
5. grandeurs diagnostiques valides et stables
6. au moins une suggestion différente de la consigne courante

> ⚠️ Les conditions 1 et 2 sont des préconditions de qualification du signal.
> Elles sont évaluées avant toute autre condition.
> Leur échec interrompt immédiatement l'évaluation — les conditions 3 à 6 ne sont pas examinées.

Interdictions :

- jamais en Vacances
- jamais en absence
- jamais en reprise
- jamais en post-aération
- jamais en présence d'apports externes
- jamais hors domaine d'auto-ajustement Arsenal

---

# ----------------------------------------------------------
# 🧠 8. REPRÉSENTATIVITÉ THERMIQUE — ÉLIGIBILITÉ D'APPRENTISSAGE
# ----------------------------------------------------------

## Principe

L'auto-ajustement de la courbe de chauffe est autorisé uniquement si
la période d'observation est **thermiquement représentative**.

Ce mécanisme constitue un **verrou de qualité de signal**.

Il ne participe pas au calcul de la correction.
Il conditionne uniquement le droit d'apprentissage.

Il est évalué en premier, avant toute autre condition d'autorisation.

---

## Indicateur canonique

`sensor.pourcentage_consigne_eco_24h_proxy`

Sémantique :

Plus la valeur est élevée, plus la période récente a été
peu sollicitée thermiquement, donc moins elle est représentative.

---

## Définition de l'état

L'état de représentativité thermique est un **état système stable**,
déterminé avec hystérésis.

Il ne reflète pas une valeur instantanée mais une position mémorisée.

Règles de transition :

- valeur > 55 % → NON_REPRESENTATIF
- valeur < 40 % → REPRESENTATIF
- 40 % ≤ valeur ≤ 55 % → état conservé

État initial :

- NON_REPRESENTATIF (conservatoire)

---

## Support d'état

L'état de représentativité thermique est porté exclusivement par :

`input_select.chauffage_representativite_thermique`

Toute modification de cet état doit être réalisée exclusivement
par le mécanisme d'évaluation de la représentativité thermique.

Toute écriture externe constitue une violation du contrat.

---

## Usage contractuel

- état = REPRESENTATIF → précondition satisfaite
- état = NON_REPRESENTATIF → auto-ajustement interdit, chaîne interrompue

Toute décision d'ajustement produite hors état REPRESENTATIF est :

→ contractuellement nulle

---

## Interdictions normatives

- Ce critère ne pondère jamais une correction
- Il ne modifie aucune grandeur thermique
- Il ne peut pas être contourné par une logique décisionnelle
- Il ne peut pas être forcé sans mécanisme explicite documenté

---

## Traçabilité

Toute transition d'état doit produire :

- un événement traçable
- une entrée logbook explicite

Principe :

> 🧠 Une invalidation d'apprentissage doit être observable et explicable.

---

# ----------------------------------------------------------
# 🔒 9. IMMUNITÉ THERMIQUE & PROTECTIONS
# ----------------------------------------------------------

Frontière d'immunité thermique :

- `binary_sensor.signature_thermique_poele`
- mémoire thermique récente (24 h)

Principe :

Toute signature thermique compatible avec un apport poêle
rend la période thermique impropre à l'apprentissage.

La présence d'une signature thermique active ou récente
suspend toute calibration de la courbe de chauffe.

Ce mécanisme est indépendant :

- du domaine physique chaudière
- du domaine d'auto-ajustement Arsenal

Il agit exclusivement comme **verrou d'apprentissage**.

Il est évalué immédiatement après la représentativité thermique (§8),
avant toute autre condition d'autorisation.

---

# ----------------------------------------------------------
# 🔁 10. TEMPORALITÉ & RYTHME
# ----------------------------------------------------------

Règles temporelles :

- exécution planifiée lente (quotidienne typiquement)
- une décision maximum par cycle
- pas de rafale
- pas de recalcul rapide
- pas de dépendance événementielle temps réel

Objectifs :

- éviter oscillations lentes
- garantir stabilité longue
- préserver lisibilité utilisateur

La temporalité s'applique :

- uniquement au domaine d'auto-ajustement
- jamais à la couche d'exécution physique

---

# ----------------------------------------------------------
# 🧩 11. TRAÇABILITÉ OBLIGATOIRE
# ----------------------------------------------------------

Toute décision d'auto-ajustement doit produire :

- un événement `chauffage_adjustment`
- un logbook explicite
- une ligne mémoire lisible
- distinction simulation / réel

Champs normatifs minimaux :

| Champ | Description |
|-------|-------------|
| `mode` | `simulation` ou `real` |
| `pente_before` | Valeur pente avant décision |
| `pente_suggested` | Valeur suggérée par le capteur de proposition |
| `pente_after` | Valeur pente après décision (ou `null` si non appliquée) |
| `pente_applied` | `true` si la pente a été effectivement modifiée, `false` sinon |
| `para_before` | Valeur parallèle avant décision |
| `para_suggested` | Valeur suggérée par le capteur de proposition |
| `para_after` | Valeur parallèle après décision (ou `null` si non appliquée) |
| `para_applied` | `true` si le parallèle a été effectivement modifié, `false` sinon |
| `representativite` | État `input_select.chauffage_representativite_thermique` au moment de la décision |
| `timestamp` | Horodatage UTC ISO 8601 |
| `refus_reason` | Présent si `pente_applied = false` ou `para_applied = false` — raison normative parmi : `non_representatif`, `immunite_poele`, `hors_domaine`, `conditions_non_remplies`, `suggestion_identique` |

Principe :

> 🧠 **Toute calibration doit être auditée humainement.**

La trace doit permettre de distinguer sans ambiguïté :

- refus qualité signal (`non_representatif`, `immunite_poele`)
- refus politique (`conditions_non_remplies`, `hors_domaine`)
- non-application fonctionnelle (`suggestion_identique`)
- application effective avec ou sans écart entre suggestion et valeur appliquée

Si `pente_suggested ≠ pente_after` ou `para_suggested ≠ para_after` (clamp domaine), l'écart doit être explicitement traçable.

---

# ----------------------------------------------------------
# 🔒 12. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Il est strictement interdit :

- toute écriture automatique sans supervision
- toute boucle fermée thermique
- toute calibration temps réel
- toute dépendance cloud instable
- toute décision hors automation dédiée
- toute modification hors helpers consigne
- toute application directe depuis un capteur
- toute réécriture non tracée
- toute suggestion sortant du domaine d'auto-ajustement Arsenal
- toute tentative d'exploration automatique du domaine physique complet

Toute violation constitue :

- une rupture de gouvernance thermique,
- un risque d'instabilité systémique,
- une régression architecturale majeure.

---

# ----------------------------------------------------------
# 🧱 13. INVARIANTS DU MÉCANISME
# ----------------------------------------------------------

Invariants absolus :

- séparation stricte calcul / décision / application
- aucune boucle fermée
- supervision humaine implicite
- immunité aux apports externes
- traçabilité complète
- stabilité longue privilégiée
- aucune urgence thermique
- respect strict du domaine d'auto-ajustement Arsenal

Relation d'invariant :

- le domaine d'auto-ajustement est un **sous-ensemble strict**
  du domaine physique chaudière
- aucune couche d'apprentissage ne peut franchir cette frontière

---

# ----------------------------------------------------------
# 🧠 14. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Subordonné à :

- `00_gouvernance_chauffage.md`

Complémentaire de :

- `15_capteurs_thermiques.md`
- `70_autorisation_thermostat.md`
- `80_table_decision_canonique.md`
- `90_semantique_thermique.md`

Gouverne directement :

- toutes suggestions de pente / parallèle
- toutes décisions de calibration
- toutes écritures de courbe
- tous mécanismes d'apprentissage thermique

Dépend explicitement de :

- `CONTRAT_MQTT.md` §11 — Règle normative de validation des bornes côté exécution Arsenal
  (bornes physiques opposables : pente [0.2 ; 3.5] pas 0.1 / parallèle [-13 ; 40] pas 1)

---

# ----------------------------------------------------------
# 📌 15. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- stratégique dans l'architecture Chauffage,
- frontière critique d'optimisation thermique,
- stable long terme,
- modifié uniquement lors d'évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **stratégie officielle de calibration thermique  
supervisée du Chauffage Arsenal V3 PRO**.

# ==========================================================
