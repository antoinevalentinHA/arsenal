# CONTRAT ARSENAL — CLIMATISATION
## 04 — Entrées métier

**Version contrat :** v1.2

---

## Principe

Les entrées métier définissent ce qui alimente la couche Décision.  
Elles ne décident pas. Elles conditionnent.

Les entrées métier sont des observations du contexte thermique, physique ou humain du logement.  
Elles ne portent aucune décision de confort.

---

## Températures intérieures

- Température minimale chambres
- Température maximale chambres

Utilisées pour déterminer les besoins thermiques consommés par la couche Décision.

Les seuils sont calculés ailleurs et consommés tels quels.

---

## Température extérieure

- Peut rendre COOL ou HEAT non applicables
- **Ne force jamais un mode**

---

## Humidex (DRY)

- Basé sur l'humidex maximal des chambres (`sensor.humidex_max_chambres`)
- Hystérésis ON / OFF explicite, portée par :
  - `binary_sensor.chambre_max_humidex_au_dessus_seuil` (seuil allumage)
  - `binary_sensor.chambre_max_humidex_en_dessous_seuil_off` (seuil extinction = seuil - 1)
- DRY interdit sans présence ou babysitting

---

## Présence

- La présence ne déclenche jamais une action seule
- Elle conditionne DRY et HEAT
- L'absence prolongée peut inhiber COOL — portée par `binary_sensor.clim_extinction_absence_prolongee_autorisee`, alimenté par `timer.absence_longue_clim`

---

## Contraintes physiques et métier

- Fenêtres ouvertes — `binary_sensor.fenetre_ouverte_maison`
- Aération favorable — `binary_sensor.aeration_preferable_etage`
- Blocage horaire — primitive canonique : `binary_sensor.clim_blocage_horaire_reel`
  (calculé depuis `input_boolean.clim_blocage_horaire_actif` + `input_datetime.clim_heure_blocage_autom_*`)
- Blocage poêle — `input_boolean.blocage_clim_poele`
- Autorisation chauffage par clim — `input_boolean.chauffage_clim_active_en_hiver`
  (autorité d'écriture unique : `automation.mode_maison_gestion_chauffage_clim_hiver`)
- Blocage post-aération — `input_boolean.chauffage_blocage_aeration` (domaine chauffage, consommé par HEAT uniquement)
- Consigne chauffage appliquée — `sensor.temperature_de_consigne_appliquee_locale` (domaine chauffage, base de calcul des seuils HEAT clim — HEAT clim est un appoint indexé sur la consigne du chauffage principal)

Les contraintes :
- **n'imposent jamais un mode**,
- peuvent rendre un mode requis **non applicable**, sans jamais sélectionner un autre mode.
