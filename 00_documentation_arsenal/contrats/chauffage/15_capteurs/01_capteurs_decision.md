# 🧠 ARSENAL — CONTRAT CAPTEURS STRUCTURANTS · Cœur thermique — Références et signaux internes canoniques
# Domaine : Chauffage / Moteur thermique
# Couche  : Capteurs structurants du cœur décisionnel
# Statut  : STRUCTURANT — FRONTIÈRE FONDATRICE
#
# 🎯 Rôle global :
#   Définir le SOCLE DES CAPTEURS INTERNES STRUCTURANTS du moteur thermique Arsenal.
#
#   Cette couche regroupe exclusivement :
#     - des RÉFÉRENCES THERMIQUES CRITIQUES
#     - des SIGNAUX INTERNES CANONIQUES
#
#   servant de fondation directe à :
#     - la décision centrale
#     - la table de décision canonique
#     - l’autorisation thermostat
#     - les mécanismes de protection et de standby
#
# 🧱 Frontière d’autorité protégée :
#   STRUCTURATION INTERNE DU MOTEUR THERMIQUE
#
#   Ces capteurs constituent l’INTERFACE INTERNE ENTRE :
#     - la réalité thermique mesurée
#     - la souveraineté décisionnelle du moteur
#
#   Ils ne sont :
#     - ni des capteurs de pilotage
#     - ni des capteurs de diagnostic libre
#     - ni des mécanismes de décision
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucun ordre matériel direct
#   - Aucun déclenchement d’action
#   - Aucune écriture de consigne
#   - Aucun pilotage de service
#   - Aucune dépendance matérielle ou API
#   - Aucun accès direct à la chaudière
#   - Aucune logique de calibration
#   - Aucun diagnostic exploratoire ou statistique
#
# 🔒 Garanties exigées :
#   - Déterminisme strict
#   - Sémantique stable et documentée
#   - Reload-safe / restart-safe / runtime-safe
#   - Indépendance totale vis-à-vis du matériel et du Cloud
#   - Dépendance exclusive à des sources gouvernées
#   - Absence totale d’effet de bord
#
# 🔗 Autorités amont légitimes :
#   - Capteurs thermiques physiques gouvernés
#   - Helpers de paramétrage canonique
#   - Contextes métier validés
#
# 🔗 Autorités aval autorisées :
#   - Décision centrale Chauffage
#   - Table de décision canonique
#   - Triggers décisionnels
#   - Autorisation thermostat logique
#   - Standby / hystérésis
#   - Diagnostics structurants d’inertie
#   - Calibration future (lecture uniquement)
#
# ⚠️ Risques systémiques surveillés :
#   - Dérive sémantique des références
#   - Introduction d’une dépendance matérielle ou Cloud
#   - Contournement implicite de la table canonique
#   - Usage direct comme déclencheur matériel
#   - Ajout d’une logique décisionnelle cachée
#
# 🔒 Statut d’autorité :
#   SOCLE STRUCTURANT DU MOTEUR THERMIQUE
#   Toute modification impacte directement la stabilité décisionnelle globale.
#
# ==========================================================

### 🔒 sensor.temperature_min_chambres

- Domaine : Diagnostic structurant / Décision thermique
- Autorité : **STRUCTURANT**

---

🎯 Rôle :
Fournir la **température minimale représentative de la zone Chambres**,
utilisée comme borne basse de référence pour la décision thermique,
la protection en absence et les diagnostics d'inertie.

---

🧭 Périmètre d'influence autorisé :
- `sensor.chauffage_autorisation_cible` (borne basse de zone)
- Standby / hystérésis thermique
- Protection absence (garde-fou refroidissement)
- Diagnostics structurants d'inertie
- Base de calibration future (offset absence)

---

⛔ Interdictions absolues :
- Ne pilote jamais directement un ordre matériel
- Ne déclenche aucune automatisation action
- Ne définit aucun mode thermique
- Ne sert jamais de température moyenne
- Ne pilote jamais seul une décision finale

---

🔒 Garanties exigées :
- Agrégation min déterministe sur les valeurs numériques disponibles
- Ignorance des valeurs non numériques (`unknown`, `unavailable`)
- Fallback mémoire via `this.state` en cas de rupture temporaire —
  garanti en fonctionnement normal ; peut retourner `unknown` au premier démarrage à froid
  avant toute donnée disponible
- Robustesse en cascade : chaque source amont (`temperature_chambre_*`) dispose
  elle-même d'un fallback HomeKit → Zigbee → mémoire — la rupture totale
  nécessite la défaillance simultanée des six capteurs physiques et de toutes les mémoires
- Expose en attribut la chambre la plus froide identifiée
- Reload-safe / runtime-safe (trigger `homeassistant start` inclus)
- Aucune logique métier embarquée

---

🔗 Dépendances :

Sources amont (capteurs consolidés) :
- `sensor.temperature_chambre_enfants` (HomeKit → Zigbee → mémoire)
- `sensor.temperature_salle_de_jeux` (HomeKit → Zigbee → mémoire)
- `sensor.temperature_chambre_parents` (HomeKit → Zigbee → mémoire)

Consommateurs contractuels :
- `sensor.chauffage_autorisation_cible`
- Diagnostics structurants d'inertie thermique

---

⚠️ Risques :
- Dérive sémantique : min ≠ température de confort — ne pas interpréter comme cible de chauffe
- Retour `unknown` au premier démarrage à froid si aucune source n'est encore disponible
- Usage direct en pilotage interdit
- Extension de périmètre sans mise à jour contractuelle

---

⚠️ Classification :
INCLUS DANS [`index.md`](index.md)
Section : Diagnostic structurant / Décision thermique
Classe : **STRUCTURANT**

# ----------------------------------------------------------

### 🔒 sensor.chauffage_autorisation_cible

- Domaine : Autorisation thermostat / Évaluation thermique canonique
- Autorité : **STRUCTURANT — NIVEAU CRITIQUE**

---

🎯 Rôle :
Calculer l'**intention thermique canonique ternaire** (`comfort` / `neutre` / `reduced`)
à partir des faits physiques et contextuels du moment,
indépendamment de tout mécanisme de blocage N1 ou de décision d'exécution.

Ce capteur constitue le **pivot d'évaluation thermique de fond** du système Arsenal.
Il répond exclusivement à : fait-il froid dehors, fait-il froid dedans
— sans tenir compte du contexte Vacances, des mécanismes de blocage ou d'exécution.
Le contexte Vacances est arbitré exclusivement en amont par la Décision Centrale
(cf. `30` §4) ; ce capteur **ne le connaît pas**.

Il est une **entrée** de la décision centrale — pas sa sortie.
Il est également consommé directement par le mécanisme de standby,
les diagnostics structurants et les triggers décisionnels.

Il représente une **autorisation thermique calculée**, jamais une décision finale,
jamais une action, jamais un ordre matériel.

---

🧭 Périmètre d'influence autorisé :
- Décision centrale chauffage (régime présence uniquement)
- Automation d'application du verrou standby (`input_boolean.chauffage_standby_force`)
- Triggers décisionnels présence (capteur pivot)
- Diagnostics structurants (`sensor.chauffage_mode_calcule`, `sensor.chauffage_raison_calculee`)
- Observabilité (recorder, logbook, UI)

---

⛔ Interdictions absolues :
- Ne déclenche jamais directement une chauffe
- Ne produit jamais d'ordre matériel
- Ne modifie jamais une consigne
- Ne pilote jamais un service
- Ne dépend jamais directement d'un équipement matériel
- Ne dépend jamais d’une source externe non maîtrisée
- Ne contourne jamais la table de décision
- Ne doit pas connaître les blocages N1 (dépendance actuelle à `blocage_chauffage_poele` documentée comme dette à migrer vers la décision centrale)

---

🔒 Garanties exigées :
- Valeurs strictement bornées : `comfort` / `neutre` / `reduced` / `unknown`
- Décision pure, sans effet de bord
- Reload-safe / restart-safe
- Indépendance totale vis-à-vis du matériel et de l'API
- Dépendance exclusive à des capteurs et helpers gouvernés
- Fallback `unknown` si données amont indisponibles — jamais de repli mensonger

---

🔗 Dépendances :

Sources thermiques :
- `sensor.temperature_jardin`
- `sensor.temperature_min_chambres`

Paramètres décisionnels :
- `input_number.chauffage_consigne_confort`
- `input_number.chauffage_offset_on`
- `input_number.chauffage_offset_off`
- `input_number.chauffage_seuil_ext_on`
- `input_number.chauffage_seuil_ext_off`

Contextes :
- `input_boolean.blocage_chauffage_poele` ⚠️ dette architecturale — ce capteur devrait ignorer les blocages N1 ; cette dépendance doit être migrée vers la décision centrale
- `input_boolean.chauffage_anticipation_meteo`
- `binary_sensor.meteo_favorable_chauffage`

> Le retrait de `input_select.mode_maison` (VAC-IMP-1, option B) applique au contexte Vacances la même réduction de dette de couche que celle documentée ci-dessus pour `input_boolean.blocage_chauffage_poele` : ce capteur ne porte que le thermique pur. Le contexte Vacances est arbitré exclusivement par la Décision Centrale.

Consommateurs contractuels :
- `decision_centrale.yaml` — régime présence (entrée, pas sortie)
- `11_automations/chauffage/autorisation.yaml` — application du verrou standby
- [`20_triggers_decisionnels.md`](../20_triggers_decisionnels.md) — capteur pivot des triggers présence
- [`50_standby_hysteresis.md`](../50_standby_hysteresis.md) — pilotage du standby
- `diagnostic/mode.yaml` et `diagnostic/raison.yaml` — diagnostics structurants
- Recorder / logbook / UI

---

⚠️ Risques :
- Altération sémantique des seuils — impact global immédiat sur tout le système
- Introduction d'une dépendance matérielle ou API — violation de souveraineté
- Confusion avec une sortie décisionnelle — ce capteur est une entrée, pas une sortie
- Ajout implicite d'une action — dette systémique critique
- Usage direct comme déclencheur matériel — interdit

---

❗ Statut particulier :
**CAPTEUR D'ÉVALUATION THERMIQUE CANONIQUE — ENTRÉE DU MOTEUR DE DÉCISION**
Pivot d'autorisation thermique de fond, consommé par la décision centrale,
le standby et les diagnostics structurants.
Ne connaît pas les blocages N1.
Toute modification est une modification MÉTIER de premier niveau.

---

⚠️ Classification :
INCLUS DANS [`index.md`](index.md)
Section : Autorisation thermostat / Évaluation thermique canonique
Classe : **STRUCTURANT — NIVEAU CRITIQUE**
