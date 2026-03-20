# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     CHAUFFAGE — PRÉ-CONFORT RETOUR VACANCES (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — ANTICIPATION THERMIQUE TEMPORISÉE
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   de **pré-confort retour Vacances** du sous-système Chauffage Arsenal.
#
#   Il formalise la stratégie officielle d’anticipation thermique
#   précédant un retour utilisateur après une période de Vacances.
#
#   Il est OPPOSABLE à toute implémentation :
#     • helpers temporels,
#     • capteurs d’anticipation,
#     • scripts d’autorisation,
#     • lectures par la Décision Centrale.
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
de **pré-confort retour Vacances**.

Il formalise :

- la finalité réelle de ce mécanisme,
- ses conditions d’activation légitimes,
- sa portée strictement limitée,
- ses effets autorisés,
- ses interdictions absolues.

Ce mécanisme constitue une **anticipation thermique temporelle contrôlée**,  
et non un mécanisme de confort d’absence.

---

# ----------------------------------------------------------
# 🧠 2. FINALITÉ RÉELLE DU PRÉ-CONFORT
# ----------------------------------------------------------

Le pré-confort retour Vacances ne vise PAS :

- la continuité de confort en absence,
- un confort prolongé avant retour,
- une simulation de présence,
- une protection du bâti,
- une stratégie de chauffage autonome.

Il vise exclusivement :

- anticiper thermiquement un retour utilisateur planifié,
- réduire la violence thermique de la reprise,
- limiter les appels de puissance brutaux,
- garantir un confort acceptable à l’arrivée.

Objectif fondamental :

> 🧠 **Préparer la dynamique de reprise thermique  
> sans jamais produire de confort autonome en absence.**

---

# ----------------------------------------------------------
# 🧱 3. POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------

Le pré-confort :

- s’applique uniquement en régime **Vacances**,
- ne modifie PAS le régime courant,
- ne lève JAMAIS le mode Vacances,
- ne modifie PAS la hiérarchie métier,
- ne pilote JAMAIS directement le matériel.

Il agit exclusivement sur :

> 🧠 **L’autorisation thermique simulée de type `comfort`**

via la couche définie dans :

- `70_autorisation_thermostat.md`

Il est :

- pré-décisionnel  
- non exécutoire  
- strictement subordonné  

---

# ----------------------------------------------------------
# 🧠 3 bis. SUBORDINATION À LA SOUVERAINETÉ OPÉRATEUR
# ----------------------------------------------------------

Le pré-confort retour Vacances est strictement subordonné
à toute commande explicite de l’opérateur.

Règle cardinale :

> 🔒 Toute activation de `mode_confort_chauffage`
> écrase immédiatement tout mécanisme de pré-confort.

L’override opérateur a priorité sur
input_boolean.pre_confort_actif_calcule.

Conséquences normatives :

- le pré-confort ne peut jamais limiter un override humain,
- il ne peut jamais retarder une décision volontaire,
- il ne peut jamais conditionner un forçage utilisateur,
- il ne peut jamais être interprété comme une alternative à l’override.

En présence d’un forçage opérateur :

- toute logique de pré-confort est neutralisée,
- seule la souveraineté humaine s’applique,
- aucune temporisation automatique n’est opposable.

Objectif :

> 🧠 Garantir que le pré-confort reste un outil d’anticipation,
> jamais un mécanisme de contrôle.

---

# ----------------------------------------------------------
# 🌡️ 4. PRINCIPE DE FONCTIONNEMENT
# ----------------------------------------------------------

Lorsque les conditions temporelles sont réunies :

- une **autorisation forcée de type `comfort`** est produite,
- cette autorisation est injectée dans la couche thermostat logique,
- la Décision Centrale peut décider une montée en confort.

Mais :

- le régime reste officiellement **Vacances**,
- toute hiérarchie supérieure continue de s’appliquer,
- toute abstention reste souveraine.

Le pré-confort :

- n’est jamais une décision,
- n’est jamais une transition,
- n’est jamais une reprise,
- n’est jamais un retour de présence.

---

# ----------------------------------------------------------
# 🧠 5. CONDITIONS D’ACTIVATION LÉGITIMES
# ----------------------------------------------------------

Le pré-confort peut être autorisé uniquement si :

- le régime courant est **Vacances**
  (au sens strict : `binary_sensor.vacances_actives = on`),
- une date / fenêtre de retour utilisateur est connue,
- la fenêtre temporelle d’anticipation est atteinte,
- aucune interdiction hiérarchique n’est active :
  - chauffage autorisé système,
  - fenêtres fermées,
  - aucune aération,
  - aucun poêle actif,
  - aucun blocage post-aération.

Règle cardinale :

> ⚠️ Le pré-confort est déclenché exclusivement  
> par une ANTICIPATION TEMPORELLE DE RETOUR,  
> jamais par un seuil thermique.

---

# ----------------------------------------------------------
# 🧠 5bis. DÉTERMINATION NORMATIVE DE LA FENÊTRE D’ANTICIPATION
# ----------------------------------------------------------

La fenêtre temporelle de pré-confort n’est PAS arbitraire.

Elle est déterminée exclusivement par une estimation
du **délai thermique réel nécessaire pour atteindre un confort acceptable**.

Ce délai est calculé à partir de grandeurs physiques observées,
issues du système d’observabilité thermique Arsenal.

Grandeurs canoniques utilisées :

- température plancher réellement atteinte pendant le régime Vacances,
- consigne confort cible officielle,
- vitesse réelle de reprise thermique mesurée,
- inertie post-reprise éventuellement observée.

Notations normatives :

- ΔT_rattrapage = T_confort_cible – T_plancher_vacances  
- V_reprise = vitesse réelle de reprise thermique (°C/h)  
- D_chute = durée chute post-reprise (si non nulle)  

Délai thermique normatif :

> 🧠 D_préchauffage = (ΔT_rattrapage / V_reprise) + D_chute + marge_sécurité

Règles impératives :

- ce délai est recalculé à chaque cycle Vacances,
- il constitue la seule base légitime de déclenchement temporel,
- aucune valeur fixe ne peut s’y substituer durablement,
- toute implémentation doit rester conservative.

Objectifs :

- déclencher le pré-confort au plus tard nécessaire,
- éviter toute anticipation excessive,
- préserver strictement la sobriété en absence,
- garantir un confort acceptable à l’arrivée.

---

### 🔧 Implémentation transitoire (phase initiale)

Dans la phase actuelle du système Arsenal :

- le système d’observabilité thermique est en cours de validation,
- les grandeurs canoniques (T_plancher, V_reprise, D_chute) ne sont pas encore
  considérées comme suffisamment stables pour piloter une décision normative.

À titre transitoire :

- la fenêtre de pré-confort est déterminée par un **helper utilisateur**
  `input_number.duree_prechauffage_retour_vacances`,
- exprimée en heures,
- bornée strictement (min / max),
- utilisée exclusivement comme approximation conservative.

Cette implémentation :

- respecte intégralement les invariants du mécanisme,
- ne modifie pas la sémantique du pré-confort,
- ne produit aucune dérive fonctionnelle,
- est conçue pour être **remplacée sans rupture**
  par le calcul normatif dès validation du système d’observabilité.

Statut :

> ⚠️ Source temporelle transitoire — mécanisme normatif conservé

---

# ----------------------------------------------------------
# 🔧 5ter. IMPLÉMENTATION TECHNIQUE ÉVÉNEMENTIELLE (V3)
# ----------------------------------------------------------

L’implémentation V3 du mécanisme de pré-confort repose
sur une orchestration strictement événementielle,
sans polling périodique.

## 🧱 Architecture technique

La fenêtre de pré-confort est matérialisée explicitement via :

- `input_datetime.pre_confort_debut_calcule`
- `input_datetime.pre_confort_fin_calcule`

L’état interne canonique est porté par :

- `input_boolean.pre_confort_actif_calcule`

Ce boolean constitue la **vérité opérationnelle unique**
du mécanisme de pré-confort.

Il ne produit aucune décision,
mais alimente exclusivement la couche :

- `70_autorisation_thermostat.md`

---

## 🔁 Recalcul & Réconciliation

Le mécanisme est recalculé exclusivement lors :

- d’un redémarrage Home Assistant,
- du passage de `systeme_stable` à `on`,
- d’une modification de :
  - `input_datetime.fin_vacances`,
  - `input_number.duree_prechauffage_retour_vacances`,
  - `binary_sensor.vacances_actives`,
  - `input_boolean.pre_confort_enable`,
- de la fin des timers instrumentaux.

Aucun recalcul périodique n’est autorisé.

---

## ⏱️ Timers instrumentaux

Les timers :

- `timer.pre_confort_jusqua_debut`
- `timer.pre_confort_jusqua_fin`

sont strictement instrumentaux.

Ils :

- ne portent aucune autorité décisionnelle,
- ne constituent pas une source de vérité,
- ne remplacent jamais la réconciliation logique.

Toute perte d’état est compensée
par la logique de recalcul idempotente.

---

## 🔒 Invariants techniques V3

- aucune dépendance au `time_pattern`,
- aucune temporisation aveugle,
- aucune activation autonome post-reboot,
- invalidation immédiate si les préconditions deviennent fausses,
- orchestration déterministe et reproductible.

Statut :

> Implémentation événementielle robuste,  
> cohérente avec la gouvernance Chauffage Arsenal V3 PRO.

---

# ----------------------------------------------------------
# 🔁 6. EFFETS NORMATIFS AUTORISÉS
# ----------------------------------------------------------

Lorsque le pré-confort est actif :

- l’autorisation thermique simulée devient `comfort`,
- la Décision Centrale peut décider un passage en confort,
- le régime Vacances reste pleinement actif,
- toute hiérarchie continue de s’appliquer.

Effets interdits :

- aucune levée du régime Vacances,
- aucune simulation de présence,
- aucune continuité de confort prolongée,
- aucune annulation automatique post-retour.

---

# ----------------------------------------------------------
# 🛑 7. GARDE-FOUS STRICTS
# ----------------------------------------------------------

Garde-fous absolus :

- fenêtre temporelle strictement bornée,
- activation unique par cycle Vacances,
- anti-rebond obligatoire,
- durée maximale impérative.

Règles :

- aucune activation hors fenêtre définie,
- aucune réactivation rapprochée autorisée,
- En fin de fenêtre, l’autorisation simulée comfort est retirée.
Toute décision ultérieure relève exclusivement de la Décision Centrale.
- aucune continuité de confort possible sans décision fraîche.

Objectifs :

- éviter toute dérive de confort en absence,
- préserver la sobriété structurelle,
- empêcher tout pré-chauffage abusif.

---

# ----------------------------------------------------------
# 🧩 8. INDÉPENDANCE & NEUTRALITÉ
# ----------------------------------------------------------

Le pré-confort :

- ne connaît PAS la présence réelle,
- ne modifie PAS les états de géolocalisation,
- ne déclenche PAS de retour de présence,
- ne produit AUCUNE décision autonome.

Il agit uniquement comme :

> 🧠 **UNE AUTORISATION D’ANTICIPATION TEMPORELLE  
> STRICTEMENT SOUMISE À LA DÉCISION CENTRALE**

---

# ----------------------------------------------------------
# 🔒 9. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Le pré-confort retour Vacances ne doit JAMAIS :

- lever le mode Vacances,
- simuler une présence,
- produire une reprise automatique,
- maintenir un confort prolongé,
- court-circuiter un blocage hiérarchique,
- ignorer une abstention décisionnelle,
- écrire une consigne,
- appeler directement la couche matérielle,
- déclencher une transition directe.

Toute dérive constitue :

- une rupture de souveraineté décisionnelle,
- une dérive de confort implicite,
- une régression architecturale critique.

---

# ----------------------------------------------------------
# 🧱 10. INVARIANTS DU MÉCANISME
# ----------------------------------------------------------

Invariants absolus :

- mécanisme actif uniquement en Vacances,
- déclenché uniquement par anticipation temporelle,
- durée strictement bornée,
- aucun impact hiérarchique,
- aucune mémoire inter-cycle,
- aucune restauration automatique.

Toute violation constitue :

- une perte de maîtrise thermique,
- une dérive de pré-chauffage,
- une rupture de gouvernance.

---

# ----------------------------------------------------------
# 🧠 11. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- utilisé par :
  - `30_decision_centrale.md`

- complémentaire de :
  - `60_absence_inhibition_geofencing.md`
  - `70_autorisation_thermostat.md`
  - `80_table_decision_canonique.md`
  - `90_semantique_thermique.md`

Il gouverne directement :

- tout helper de pré-confort Vacances,
- toute autorisation d’anticipation temporelle,
- toute activation de confort pré-retour.

---

# ----------------------------------------------------------
# 📌 12. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- stratégique dans l’architecture Chauffage,
- strictement borné fonctionnellement,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **stratégie officielle d’anticipation thermique  
retour Vacances du Chauffage Arsenal V3 PRO**.

# ==========================================================