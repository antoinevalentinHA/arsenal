# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF CENTRAL
#     CHAUFFAGE — DÉCISION CENTRALE (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF CENTRAL — CERVEAU MÉTIER DU DOMAINE CHAUFFAGE
#
# 🔒 AUTORITÉ :
#   Ce document définit l’ALGORITHME MÉTIER OFFICIEL
#   de décision thermique du sous-système Chauffage Arsenal.
#
#   Il est OPPOSABLE à toute implémentation :
#     • scripts,
#     • automatismes,
#     • capteurs décisionnels,
#     • interfaces utilisateur.
#
#   Toute divergence entre ce contrat et le YAML constitue
#   une erreur critique de conception.
#
#   Subordonné à :
#     /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif de la **Décision Centrale Chauffage**.

Il formalise :

- le rôle exclusif du cerveau thermique,
- la hiérarchie réelle des causes,
- les règles d’arbitrage entre contextes,
- les mécanismes d’abstention,
- les garde-fous anti-oscillation,
- les conditions légitimes de changement de programme.

Ce contrat est la **référence unique** décrivant *comment* et *quand* le système
est autorisé à changer de régime thermique.

---

# ----------------------------------------------------------
# 🧠 2. RÔLE FONDAMENTAL DE LA DÉCISION CENTRALE
# ----------------------------------------------------------

La Décision Centrale est :

- l’unique autorité habilitée à décider un changement de programme chauffage,
- le point de convergence de toutes les causes thermiques et contextuelles,
- la source officielle de toute intention d’application.

Elle peut uniquement :

- ordonner un passage en `comfort`,
- ordonner un passage en `reduced`,
- ou refuser volontairement toute action.

Elle ne peut jamais :

- régler une consigne,
- appeler ViCare directement,
- produire une hypothèse thermique,
- déclencher une action implicite.

---

# ----------------------------------------------------------
# 🧱 3. PÉRIMÈTRE COUVERT
# ----------------------------------------------------------

La Décision Centrale couvre exclusivement :

- l’arbitrage entre confort et sobriété,
- la hiérarchie des causes métier,
- la production d’une décision explicite,
- le refus volontaire d’action,
- la traçabilité métier de toute transition.

Hors périmètre strict :

- calcul des besoins thermiques,
- estimation d’inertie,
- réglage des consignes,
- pilotage matériel,
- correction ViCare,
- UI et pédagogie.

---

# ----------------------------------------------------------
# ⚖️ 4. HIÉRARCHIE OFFICIELLE DES CAUSES
# ----------------------------------------------------------

La décision est gouvernée par une hiérarchie descendante stricte.

Aucune cause de niveau inférieur ne peut contredire un niveau supérieur.

## 4.1 NIVEAU 1 — INTERDICTIONS ABSOLUES

Causes structurantes bloquantes :

- chauffage non autorisé système,
- standby forcé.

Effet normatif :

- décision forcée en `reduced`,
- aucune autre cause n’est évaluée.

---

## 4.2 NIVEAU 2 — CONTEXTES MAJEURS BLOQUANTS

Causes imposant la sobriété :

- poêle actif (instantané ou mémoire),
- blocage aération actif,
- blocage post-aération,
- fenêtre ouverte avec délai,
- mode maison = Vacances.

Effet normatif :

- décision forcée en `reduced`,
- toute autorisation confort est ignorée.

---

---

### Autorisations amont en contexte Vacances

En contexte `mode_maison = Vacances` :

- toute interdiction NIVEAU 2 demeure absolue,
- aucune décision confort n’est autorisée,
- aucune exception hiérarchique n’est permise.

Toute autorisation amont active dans ce contexte :

- ne constitue jamais une levée d’interdiction,
- ne modifie jamais le régime effectif,
- ne peut jamais produire une décision de reprise autonome.

Le pré-confort retour vacances est soumis intégralement à ces règles
et demeure strictement écrasé par toute cause NIVEAU 2.

Il ne constitue :

- ni une exception Vacances,
- ni une levée d’interdiction,
- ni un mécanisme de reprise automatique.

---

## 4.3 NIVEAU 3 — AUTORISATION DE CONFORT (PRÉSENCE)

La présence réelle autorise un régime confortable.

Règles :

- la présence n’est JAMAIS une décision,
- elle délègue l’intention à `autorisation_cible`,
- elle peut produire :
  - `comfort`
  - `neutre`
  - `reduced`

Effet normatif :

- la décision suit strictement l’autorisation cible,
- aucune hypothèse locale n’est autorisée.

---

---

### Autorisations de confort forcées amont

Certaines autorisations de confort peuvent être produites en amont
de la Décision Centrale par des mécanismes non liés à la présence.

Caractéristiques cardinales :

- ne constituent jamais une cause hiérarchique,
- ne constituent jamais une décision thermique,
- ne modifient jamais le régime de référence,
- restent entièrement soumises aux niveaux supérieurs.

Sources reconnues :

- inhibition géofencing,
- pré-confort retour vacances.

Règles cardinales :

- toute autorisation forcée est évaluée strictement
  dans le cadre de la hiérarchie officielle,
- toute interdiction NIVEAU 1 ou NIVEAU 2 écrase immédiatement
  toute autorisation forcée,
- aucune autorisation forcée ne peut produire
  une reprise automatique post-blocage.

Le pré-confort retour vacances appartient exclusivement à cette catégorie
et ne bénéficie d’aucun privilège hiérarchique particulier.

---

## 4.4 NIVEAU 4 — INHIBITION GÉOFENCING (ABSENCE ACTIVE)

Mécanisme de confort différé en absence.

Règles :

- le régime reste **absence**,
- l’autorisation simulée devient `comfort`,
- l’objectif est la qualité de reprise,
- jamais la recherche permanente de confort.

Effet normatif :

- autorisation ponctuelle de passage en `comfort` en absence,
- strictement contrôlée par garde-fous.

---

# ----------------------------------------------------------
# 🔁 5. HYSTÉRÉSIS DÉCISIONNELLE & ABSTENTION
# ----------------------------------------------------------

Principes cardinaux :

- fin de blocage ≠ reprise automatique,
- aucune action « par principe »,
- toute reprise doit être justifiée par un besoin valide.

Règles :

- aucune reprise immédiate après interdiction,
- aucune oscillation autorisée,
- inertie thermique respectée,
- abstention privilégiée par défaut.

---

# ----------------------------------------------------------
# 🛑 6. GARDE-FOUS D’ABSTENTION
# ----------------------------------------------------------

AUCUNE action n’est autorisée si :

- le programme actuel est inconnu,
- le mode désiré est déjà actif,
- un anti-rebond géolocalisation est en cours,
- l’autorisation est `neutre`.

Règle :

> ⚠️ Une autorisation sans besoin produit une abstention stricte.

---

# ----------------------------------------------------------
# 🔒 7. ANTI-REBOND & SÉRIALISATION
# ----------------------------------------------------------

Toute décision validée déclenche :

- un verrou temporel géolocalisation,
- l’interdiction de toute décision concurrente immédiate.

Objectifs :

- stabilisation logique,
- protection thermique,
- protection API ViCare,
- élimination des oscillations rapides.

---

# ----------------------------------------------------------
# 🧾 8. TRAÇABILITÉ MÉTIER
# ----------------------------------------------------------

Toute décision explicite doit produire :

- un changement de programme observable,
- une raison métier explicite,
- un logbook lisible,
- une notification persistante si pertinente.

Toute transition est :

- traçable,
- explicable,
- audit-compatible.

### 🔔 Projection UI — Notifications persistantes (invariant)

Les notifications persistantes Chauffage (Confort / Réduit) sont des **projections d’état secondaires**.

Règles opposables :
- Une notification persistante **ne dépend jamais** de la fin d’un script.
- Toute logique `persistent_notification.*` est **strictement interdite**
  dans un script `mode: restart` (Décision Centrale incluse).
- La production et la disqualification des notifications sont assurées
  exclusivement par une **automation UI dédiée**, idempotente et reconstructible
  (reconstruction garantie après redémarrage système).

---

# ----------------------------------------------------------
# 🔒 9. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

La Décision Centrale ne doit JAMAIS :

- appeler ViCare directement,
- modifier une consigne,
- estimer un besoin thermique,
- lire un retour matériel comme vérité,
- produire une décision implicite,
- court-circuiter la hiérarchie.

---

# ----------------------------------------------------------
# 🧱 10. INVARIANTS DE DÉCISION
# ----------------------------------------------------------

Invariants absolus :

- une seule décision à la fois,
- zéro appel inutile,
- zéro oscillation programme,
- zéro ambiguïté d’état,
- zéro reprise automatique post-blocage,
- zéro décision sans cause référencée.

Toute violation constitue :

- une régression critique,
- une rupture de gouvernance,
- une erreur majeure d’architecture.

---

# ----------------------------------------------------------
# 🧠 11. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- complémentaire de :
  - `20_triggers_decisionnels.md`
  - `70_autorisation_thermostat.md`
  - `80_table_decision_canonique.md`

Il gouverne directement :

- le script `chauffage_decision_centrale`,
- tous les automatismes de rappel décisionnel,
- toute transition de programme chauffage.

---

# ----------------------------------------------------------
# 📌 12. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- central dans l’architecture Chauffage,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue le **cerveau normatif officiel du Chauffage Arsenal V3 PRO**.

# ==========================================================