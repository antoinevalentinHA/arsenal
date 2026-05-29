# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE GOUVERNANCE
#     CHAUFFAGE — TRIGGERS DÉCISIONNELS (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF — ACTIF — NIVEAU STRUCTURANT
#
# 🔒 AUTORITÉ :
#   Ce document est OPPOSABLE à toute implémentation liée :
#     • aux automatismes de déclenchement,
#     • aux triggers décisionnels,
#     • aux pipelines d’observation,
#     • à l’ordonnancement de la Décision Centrale Chauffage.
#
#   Il constitue la RÉFÉRENCE UNIQUE pour déterminer :
#     • quelles causes doivent rappeler la Décision Centrale,
#     • avec quelle obligation,
#     • avec quelle criticité,
#     • dans quel périmètre architectural.
#
#   En cas de divergence, ce document fait foi sur :
#     • les triggers autorisés,
#     • les triggers obligatoires,
#     • les absences légitimes de rappel décisionnel.
#
# ----------------------------------------------------------
# 🧠 POSITIONNEMENT DANS L’ARCHITECTURE ARSENAL
# ----------------------------------------------------------
#
# Ce contrat se situe ENTRE :
#
#   - les contrats métier (hiérarchie, régimes, décisions),
#   - et l’implémentation technique des automatismes.
#
# Il définit :
#   • la surface officielle des événements décisionnels,
#   • la gouvernance du rappel de la Décision Centrale,
#   • le périmètre exact de l’espace de recalcul thermique.
#
# Il ne définit PAS :
#   ❌ les règles thermiques,
#   ❌ la hiérarchie métier,
#   ❌ la table de décision,
#   ❌ les mécanismes d’application,
#   ❌ les actions matérielles.
#
# ----------------------------------------------------------
# ⚠️ ANALYSE ARCHITECTURALE
# ----------------------------------------------------------
#
# Ce document :
#
# - Formalise EXHAUSTIVEMENT l’espace des causes décisionnelles.
# - Garantit :
#     • l’absence de latence décisionnelle,
#     • l’absence de décisions obsolètes,
#     • l’absence de transitions non arbitrées,
#     • le déterminisme global du système Chauffage.
#
# - Constitue un pilier de :
#     • la souveraineté décisionnelle,
#     • la cohérence inter-domaines,
#     • la stabilité post-reboot,
#     • la convergence système.
#
# Toute omission d’un trigger classé CRITIQUE constitue :
#   - une rupture de gouvernance,
#   - une perte de déterminisme,
#   - une régression architecturale majeure.
#
# ----------------------------------------------------------
# 🧠 HIÉRARCHIE DOCUMENTAIRE
# ----------------------------------------------------------
#
# Ce contrat est :
#   Subordonné à :
#     /00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Complémentaire de :
#     /00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     /00_documentation_arsenal/contrats/chauffage/80_table_decision_canonique.md
#
# Il gouverne spécifiquement :
#     • les automatismes de rappel décisionnel,
#     • l’ordonnancement des recalculs,
#     • la surface officielle des événements structurants.
#
# ----------------------------------------------------------
# 🔒 RÈGLES DE GOUVERNANCE
# ----------------------------------------------------------
#
# - Ce document :
#     ✅ est pleinement normatif,
#     ✅ est directement opposable au YAML,
#     ✅ doit être cité dans tout automatisme de trigger,
#     ✅ gouverne toute logique de rappel décisionnel.
#
# - Il est strictement interdit :
#     ❌ d’ajouter un trigger décisionnel hors de cette table,
#     ❌ d’omettre un trigger CRITIQUE,
#     ❌ de rappeler la Décision Centrale sans cause référencée ici,
#     ❌ de déclencher une action thermique sans décision récente valide.
#
# ----------------------------------------------------------
# 📌 VALEUR STRATÉGIQUE
# ----------------------------------------------------------
#
# Nature :
#   Contrat de gouvernance décisionnelle.
#
# Rôle clé :
#   Définir QUAND le cerveau doit réfléchir à nouveau.
#
# Fonction critique :
#   Garantir que toute transition pertinente est arbitrée,
#   que toute décision est fraîche,
#   et que tout état thermique est légitime.
#
# ==========================================================


# ==========================================================
# 🧠 TABLE NORMATIVE DES TRIGGERS DÉCISIONNELS
# ==========================================================

Statut : DOCUMENT NORMATIF
Portée : Gouvernance décisionnelle Chauffage
Rôle   : Référence unique des causes autorisant / imposant un rappel de la Décision Centrale Chauffage.

Ce document définit EXHAUSTIVEMENT :

- les causes décisionnelles reconnues,
- les transitions pertinentes,
- l’obligation ou non de rappel décisionnel,
- leur criticité architecturale.

Toute implémentation divergente constitue :

- soit une lacune fonctionnelle,
- soit une violation du contrat Chauffage Arsenal V3 PRO.

---

# ----------------------------------------------------------
# 🛑 PRIORITÉ ZÉRO — OVERRIDES UTILISATEUR / SYSTÈME
# ----------------------------------------------------------

| Cause                       | Transition | Trigger | Criticité | Commentaire |
|----------------------------|------------|---------|-----------|-------------|
| chauffage_autorise_systeme | OFF → ON   | OUI     | CRITIQUE  | Revalidation complète espace décisionnel |
| chauffage_autorise_systeme | ON → OFF   | OUI     | CRITIQUE  | Interdiction immédiate absolue |
| mode_confort_chauffage     | OFF → ON   | OUI     | CRITIQUE  | Override prioritaire immédiat, y compris en contournement d’anti-rebond |
| mode_confort_chauffage     | ON → OFF   | OUI     | MAJEUR    | Retour régime normal |

Règle cardinale :

- l’override opérateur contourne l’anti-rebond géoloc,
- aucun délai de stabilisation n’est opposable à `mode_confort_chauffage`,
- cette priorité ne contourne jamais les sécurités matérielles hors périmètre Arsenal.

---

# ----------------------------------------------------------
# 🧠 AUTORISATIONS CONTEXTUELLES AUTOMATIQUES
# ----------------------------------------------------------

Ces causes ne constituent pas des décisions métier,
mais modifient l’espace d’autorisation thermique
et doivent donc rappeler la Décision Centrale.

Elles sont strictement limitées à la couche d’autorisation
et ne produisent jamais d’action directe.

| Cause                                      | Transition         | Trigger | Criticité | Commentaire |
|-------------------------------------------|--------------------|---------|-----------|-------------|
| input_boolean.pre_confort_actif_calcule   | OFF → ON           | OUI     | CRITIQUE  | Ouverture fenêtre anticipation retour Vacances |
| input_boolean.pre_confort_actif_calcule   | ON → OFF           | OUI     | CRITIQUE  | Fermeture fenêtre / fin autorisation contextuelle |
| mode_maison                               | autre → Vacances   | OUI     | CRITIQUE  | Réinitialisation espace autorisations |
| mode_maison                               | Vacances → autre   | OUI     | CRITIQUE  | Nettoyage autorisations automatiques |

Note :

- la présence de `mode_maison` dans cette table et dans la table des contextes contraignants est volontaire,
- la redondance est assumée :
  - ici, `mode_maison` agit comme signal de reconfiguration de l’espace d’autorisation,
  - ailleurs, il agit comme contexte hiérarchique contraignant.

Règles cardinales :

- toute entrée ou sortie d’une autorisation contextuelle
  doit rappeler immédiatement la Décision Centrale,
- aucune autorisation automatique ne peut subsister
  sans réévaluation décisionnelle explicite,
- ces triggers ne constituent jamais une cause hiérarchique autonome,
  mais une modification de l’espace d’autorisation.

---

# ----------------------------------------------------------
# 🛑 NIVEAU 1 — CONTEXTES CONTRAIGNANTS / BLOCAGES MAJEURS
# ----------------------------------------------------------

| Cause                               | Transition         | Trigger | Criticité | Commentaire |
|------------------------------------|--------------------|---------|-----------|-------------|
| aeration_episode_en_cours          | OFF → ON           | OUI     | CRITIQUE  | Début contexte d’aération |
| aeration_episode_en_cours          | ON → OFF           | OUI     | MAJEUR    | Fin épisode, bascule potentielle vers post-aération |
| aeration_confirmee                 | OFF → ON           | OUI     | CRITIQUE  | Qualification de l’aération en blocage effectif |
| aeration_confirmee                 | ON → OFF           | OUI     | MAJEUR    | Déqualification du contexte d’aération |
| chauffage_blocage_aeration         | OFF → ON           | OUI     | CRITIQUE  | Blocage post-aération actif |
| chauffage_blocage_aeration         | ON → OFF           | OUI     | CRITIQUE  | Fin blocage post-aération |
| fenetre_ouverte_maison_avec_delai  | OFF → ON           | OUI     | CRITIQUE  | Blocage fenêtre qualifié |
| fenetre_ouverte_maison_avec_delai  | ON → OFF           | OUI     | MAJEUR    | Fin blocage fenêtre qualifié |
| blocage_chauffage_poele            | OFF → ON           | OUI     | CRITIQUE  | Blocage poêle temporisé |
| blocage_chauffage_poele            | ON → OFF           | OUI     | MAJEUR    | Fin blocage poêle |
| mode_maison                        | autre → Vacances   | OUI     | CRITIQUE  | Entrée contexte majeur Vacances |
| mode_maison                        | Vacances → autre   | OUI     | MAJEUR    | Sortie contexte Vacances / revalidation régime |

---

# ----------------------------------------------------------
# 🧠 NIVEAU 2 — CHANGEMENT DE RÉGIME (PRÉSENCE / ABSENCE)
# ----------------------------------------------------------

| Cause                     | Transition | Trigger | Criticité | Commentaire |
|--------------------------|------------|---------|-----------|-------------|
| presence_famille_unifiee | OFF → ON   | OUI     | CRITIQUE  | ABSENCE → PRÉSENCE |
| presence_famille_unifiee | ON → OFF   | OUI     | CRITIQUE  | PRÉSENCE → ABSENCE |

---

# ----------------------------------------------------------
# 🔁 ABSENCE — INHIBITION GÉOFENCING / PROTECTION THERMIQUE
# ----------------------------------------------------------

| Cause                           | Transition | Trigger | Criticité | Commentaire |
|--------------------------------|------------|---------|-----------|-------------|
| chauffage_inhibition_geofencing| OFF → ON   | OUI     | CRITIQUE  | Entrée confort différé |
| chauffage_inhibition_geofencing| ON → OFF   | OUI     | CRITIQUE  | Sortie confort différé |
| protection annulée par présence| OFF → ON   | OUI     | MAJEUR    | Fin protection par retour |
| protection annulée par blocage | OFF → ON   | OUI     | CRITIQUE  | Blocage prioritaire |
| protection annulée par mode_maison | OFF → ON | OUI   | MAJEUR    | Régime changé |

---

# ----------------------------------------------------------
# 🌡️ PRÉSENCE — THERMOSTAT LOGIQUE (CŒUR DU SYSTÈME)
# ----------------------------------------------------------

Capteur pivot : `sensor.chauffage_autorisation_cible`

| Transition          | Trigger | Criticité | Signification |
|--------------------|---------|-----------|---------------|
| reduced → neutre   | OUI     | MAJEUR    | Entrée zone morte |
| neutre → reduced   | OUI     | MAJEUR    | Sortie zone morte |
| neutre → comfort   | OUI     | CRITIQUE  | Apparition besoin thermique |
| reduced → comfort  | OUI     | CRITIQUE  | Besoin thermique direct |
| comfort → reduced  | OUI     | CRITIQUE  | Fin besoin thermique |
| comfort → neutre   | OUI     | CRITIQUE  | Retour abstention |

👉 Tout changement de valeur DOIT rappeler la Décision Centrale.

---

# ----------------------------------------------------------
# 🔥 BESOIN THERMIQUE (TRANSVERSAL)
# ----------------------------------------------------------

Ce bloc ne constitue pas une source canonique autonome de trigger
lorsque les transitions sont déjà portées par `sensor.chauffage_autorisation_cible`.

Il sert uniquement de lecture explicative transverse.

---

# ----------------------------------------------------------
# ⏳ ATTENTE THERMIQUE (STATUTS)
# ----------------------------------------------------------

| Cause                      | Transition   | Trigger | Criticité | Commentaire |
|---------------------------|--------------|---------|-----------|-------------|
| entrée attente confort    | faux → vrai  | OUI     | MAJEUR    | Surveillance seuil |
| sortie attente confort    | vrai → faux  | OUI     | CRITIQUE  | Déclenchement |
| entrée attente protection | faux → vrai  | OUI     | MAJEUR    | Surveillance |
| sortie attente protection | vrai → faux  | OUI     | CRITIQUE  | Chauffe protection |

---

# ----------------------------------------------------------
# 🧾 RAISON DOMINANTE
# ----------------------------------------------------------

| Cause            | Transition | Trigger | Criticité | Commentaire |
|-----------------|------------|---------|-----------|-------------|
| raison dominante| A → B      | OUI     | STRUCTUREL| Cohérence hiérarchie / UI |

---

# ----------------------------------------------------------
# ⏱️ ORDONNANCEMENT & CONVERGENCE
# ----------------------------------------------------------

| Cause                           | Transition | Trigger | Criticité | Commentaire |
|--------------------------------|------------|---------|-----------|-------------|
| systeme_stable                 | OFF → ON   | OUI     | CRITIQUE  | Recalcul initial |
| chauffage_application_en_cours | ON → OFF   | OUI     | MAJEUR    | Fin de transaction exécutive / convergence technique |

---

# ----------------------------------------------------------
# ⚙️ CAPACITÉ D’EXÉCUTION — INFRASTRUCTURE BOILER BRIDGE
# ----------------------------------------------------------

| Cause               | Transition | Trigger | Criticité | Commentaire |
|--------------------|------------|---------|-----------|-------------|
| boiler_bridge_online | OFF → ON | OUI     | CRITIQUE  | Revalidation après indisponibilité technique — décision due non tentée (G2 pré-exécution) |
| boiler_bridge_online | ON → OFF | OUI     | MAJEUR    | Perte capacité d’exécution — convergence / observabilité |

Règle cardinale :

- ce trigger ne remplace pas le retry transactionnel,
- il couvre spécifiquement le cas où la Décision Centrale a pu calculer une décision valide,
  mais s’est arrêtée sur la garde de capacité d’exécution avant toute tentative descendante,
- il garantit qu’aucune décision due ne reste sans nouvelle évaluation
  au retour du bridge online.

---

# ----------------------------------------------------------
# 🧠 SYNTHÈSE FINALE — RÈGLES CARDINALES
# ----------------------------------------------------------

1. Toute transition modifiant :

   - la hiérarchie,
   - le régime,
   - l’autorisation,
   - le besoin thermique,
   - un blocage majeur,
   - l’intégrité décisionnelle,
   - la capacité effective d’exécution,

   **DOIT rappeler la Décision Centrale.**

2. Aucun mécanisme d’application ne doit :

   - chauffer,
   - arrêter,
   - protéger,

   sans qu’une décision récente valide explicitement l’état.

3. Toute absence de trigger sur une cause CRITIQUE constitue :

   - une violation du contrat Chauffage V3 PRO,
   - une source de latence décisionnelle,
   - une perte de déterminisme.

---

# ----------------------------------------------------------
# ✅ STATUT FINAL
# ----------------------------------------------------------

Document : OFFICIEL — ARSENAL
Version  : Chauffage V3 PRO
Rôle     : Référence normative des triggers décisionnels

Toute évolution nécessite :

- mise à jour de ce document,
- entrée de changelog Arsenal,
- validation explicite.

# ==========================================================