# 🧠 ARSENAL — CONTRAT CAPTEURS DE CONTEXTE HUMAIN STRATÉGIQUE · Absence / Géofencing / Anticipation retour
# Domaine : Chauffage / Contexte humain & autorisations
# Couche  : Contexte stratégique du moteur thermique
# Statut  : STRUCTURANT — FRONTIÈRES STRATÉGIQUES D’OCCUPATION
#
# 🎯 Rôle global :
#   Définir la COUCHE DE CONTEXTE HUMAIN STRATÉGIQUE du moteur Chauffage Arsenal.
#
#   Cette couche fournit :
#     - le SIGNAL CANONIQUE UNIQUE DE PRÉSENCE / ABSENCE,
#     - les AUTORISATIONS CONTEXTUELLES D’ANTICIPATION programmée,
#
#   utilisés pour orienter :
#     - la stratégie confort / sobriété,
#     - l’inhibition géofencing,
#     - les opportunités de reprise,
#     - les protections bâtiment en absence,
#     - les reprises anticipées avant retour réel.
#
#   Elle constitue la FRONTIÈRE OFFICIELLE ENTRE :
#     - occupation humaine réelle,
#     - anticipation programmée de retour,
#     - et politique thermique de la maison.
#
# 🧱 Frontières d’autorité protégées :
#   - CONTEXTE HUMAIN RÉEL (Présence / Absence)
#   - AUTORISATIONS D’ANTICIPATION PROGRAMMÉE (retour vacances)
#
#   Cette couche :
#     - n’élabore aucune décision thermique,
#     - ne bloque aucune exécution,
#     - n’autorise aucune chauffe directe,
#     - ne simule aucune présence,
#     - mais ORIENTE TOUTE LA STRATÉGIE THERMIQUE.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune décision de consigne
#   - Aucune décision de mode thermique
#   - Aucun pilotage direct du matériel
#   - Aucune écriture d’offset
#   - Aucune lecture de température
#   - Aucun calcul inertiel
#   - Aucun diagnostic calibrant
#   - Aucun déclenchement d’action
#   - Aucune simulation de présence
#
# 🔒 Garanties exigées :
#   - Agrégation exclusive de sources humaines gouvernées
#   - Séparation stricte :
#       • présence réelle
#       • autorisation anticipée programmée
#   - Temporisations strictes anti-fluctuations
#   - Valeurs binaires pures
#   - Stabilité temporelle garantie
#   - Immunité aux micro-coupures
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d’effet matériel direct
#
# 🔗 Autorités amont légitimes :
#   - Capteurs de présence humains gouvernés
#   - Sécurité présence
#   - Calendrier Vacances (fin_vacances)
#   - Mode Maison
#
# 🔗 Autorités aval autorisées :
#   - 60_absence_inhibition_geofencing.md
#   - Décision centrale Chauffage
#   - Triggers décisionnels
#   - Standby / hystérésis
#   - Autorisation thermostat
#   - Pipelines retour vacances
#
# ⚠️ Risques systémiques surveillés :
#   - Confusion présence réelle / anticipation
#   - Faux confort anticipé
#   - Sur-sobriété excessive
#   - Chauffes illégitimes hors occupation
#   - Dérive métier si enrichi avec logique thermique
#   - Rupture de souveraineté contextuelle
#
# 🔒 Statut d’autorité :
#   FRONTIÈRES STRATÉGIQUES D’OCCUPATION & D’ANTICIPATION
#   Toute altération impacte directement sobriété, confort et sécurité thermique globale.
#
# ==========================================================

### 🔒 binary_sensor.presence_famille_unifiee

- Domaine : Absence / Inhibition géofencing / Autorisation contextuelle  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Fournir le **signal canonique unique de présence familiale** destiné au moteur Chauffage Arsenal,
en consolidant plusieurs sources de détection avec **temporisation anti-fluctuations**,
afin de définir de manière **fiable, stable et gouvernée** l’état Présence / Absence de la maison.

Ce capteur constitue la **frontière contextuelle officielle** entre :

- mode présence (confort, opportunités thermiques),  
- mode absence (réduction, inhibition géofencing, protections bâtiment).

Il est la **référence souveraine de contexte humain** du moteur thermique.

🧭 Périmètre d’influence autorisé :
- Détermination officielle Présence / Absence maison  
- Condition primaire de :
  - décisions centrales chauffage  
  - inhibition géofencing  
  - choix confort / réduit  
  - opportunités de reprise  
- Garde-fou contre faux départs thermiques  
- Synchronisation chauffage ↔ occupation réelle  
- Base des modules :
  - 60_absence_inhibition_geofencing.md  
  - 30_decision_centrale.md  
  - 20_triggers_decisionnels.md  

⛔ Interdictions absolues :
- Ne décide jamais d’une consigne  
- Ne décide jamais d’un mode thermique  
- Ne pilote jamais directement la chaudière  
- Ne modifie jamais un offset  
- Ne lit jamais de température  
- Ne bloque jamais directement une exécution  
- Ne sert jamais de seuil thermique  
- Ne produit jamais de calibration  
- Ne participe jamais à un calcul inertiel  

🔒 Garanties exigées :
- Agrégation **exclusive de sources de présence humaines**  
- Temporisation stricte anti-fluctuations (ON et OFF)  
- Valeur binaire pure : présent / absent  
- Aucune lecture thermique  
- Aucune logique métier thermique  
- Immunité aux micro-coupures de détection  
- Reload-safe / runtime-safe  
- Stabilité temporelle garantie  
- Absence totale d’effet direct matériel  

🔗 Dépendances :
Sources de présence :
- binary_sensor.presence_famille  
- binary_sensor.presence_famille_securite  

Consommateurs contractuels majeurs :
- 60_absence_inhibition_geofencing.md  
- 30_decision_centrale.md  
- 20_triggers_decisionnels.md  
- 50_standby_hysteresis.md  
- 70_autorisation_thermostat.md  

⚠️ Risques :
- Décisions erronées si temporisations mal calibrées  
- Faux confort si source sécurité trop permissive  
- Absence prolongée mal détectée → surconsommation  
- Rupture de souveraineté si une source est polluée  
- Dérive critique s’il est enrichi avec logique thermique  

❗ Statut particulier :
CAPTEUR STRUCTURANT DE CONTEXTE HUMAIN THERMIQUE  
Frontière d’autorité officielle Présence / Absence du moteur Chauffage Arsenal.  
Signal maître de l’inhibition géofencing et des choix de régime thermique.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Absence / Inhibition géofencing  
Classe : Capteur STRUCTURANT

# ----------------------------------------------------------

### 🔒 binary_sensor.pre_confort_actif

- Domaine : Autorisation / Opportunité thermique / Anticipation de reprise  
- Autorité : STRUCTURANT  

🎯 Rôle :  
Indiquer qu’une **fenêtre d’anticipation de retour de vacances est ouverte**,
afin d’**autoriser exceptionnellement le chauffage en mode Confort avant réapparition de présence**,
sur la base d’un **calendrier programmé (fin_vacances)**.

Ce capteur crée une **autorisation contextuelle anticipée** permettant :

- une remise en température progressive,  
- un retour dans un bâtiment déjà tempéré,  
- sans jamais simuler une présence ni perturber les autres domaines.

Il constitue la **frontière officielle d’anticipation thermique programmée** du moteur Chauffage Arsenal.

🧭 Périmètre d’influence autorisé :
- Autorisation exceptionnelle de décisions Confort en mode Vacances  
- Levée partielle de l’inhibition Vacances dans une fenêtre temporelle bornée  
- Condition primaire de :
  - 60_absence_inhibition_geofencing.md  
  - 30_decision_centrale.md (opportunités de reprise anticipée)  
- Synchronisation chauffage ↔ calendrier de retour  
- Protection contre retours dans bâtiment froid  

⛔ Interdictions absolues :
- Ne simule jamais une présence  
- Ne modifie jamais l’état présence / absence  
- Ne désarme jamais l’alarme  
- Ne déclenche jamais ECS  
- Ne décide jamais seul d’un mode thermique  
- Ne modifie jamais une consigne  
- Ne modifie jamais un offset  
- Ne participe jamais à la table de décision  
- Ne pilote jamais directement la chaudière  

🔒 Garanties exigées :
- Dépendance **exclusive au calendrier de retour Vacances**  
- Fenêtre temporelle fixe et bornée (10 h avant fin_vacances)  
- Conditionnée strictement à l’état Mode Maison = Vacances  
- Valeur binaire pure : anticipation active / inactive  
- Aucune lecture thermique  
- Aucune interaction sécurité / ECS / présence  
- Réévaluation périodique (time_pattern)  
- Reload-safe / runtime-safe  
- Absence totale de logique métier thermique  

🔗 Dépendances :
Contexte maison :
- input_select.mode_maison (Vacances)  

Calendrier retour :
- input_datetime.fin_vacances  

Stabilité système :
- input_boolean.systeme_stable  

Consommateurs contractuels majeurs :
- 60_absence_inhibition_geofencing.md  
- 30_decision_centrale.md  
- 70_autorisation_thermostat.md  
- Pipelines retour vacances  

⚠️ Risques :
- Chauffe anticipée trop précoce si fin_vacances mal renseigné  
- Surconsommation si retour finalement annulé  
- Incohérence si mode_maison quitte Vacances sans reset  
- Dérive dangereuse s’il est utilisé comme signal de présence  
- Rupture de souveraineté s’il est utilisé hors contexte Vacances  

❗ Statut particulier :
CAPTEUR STRUCTURANT D’AUTORISATION D’ANTICIPATION THERMIQUE  
Frontière officielle de levée partielle du mode Vacances.  
Autorité unique d’anticipation Confort avant retour programmé.  

⚠️ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Absence / Inhibition géofencing / Anticipation retour  
Classe : Capteur STRUCTURANT