# Observations techniques

Nature : observations explicatives (non normatives)

---

## Coexistence de deux capteurs DRY ON

**Entités :**
- `binary_sensor.clim_humidex_sup_cible_dry`
- `binary_sensor.chambre_max_humidex_au_dessus_seuil`

Les deux capteurs reposent sur la même condition : `humidex_max > seuil_humidex_deshumidification`.

Ils présentent des différences de comportement :

- `clim_humidex_sup_cible_dry` : sans fallback, sans hystérésis
- `chambre_max_humidex_au_dessus_seuil` : avec fallback, intégré dans une logique d'hystérésis (avec `chambre_max_humidex_en_dessous_seuil_off`)

La coexistence reflète deux niveaux d'abstraction : lecture directe (non filtrée) et lecture stabilisée (hystérésis).

---

## Absence de fallback sur `clim_humidex_sup_cible_dry`

**Entité :** `binary_sensor.clim_humidex_sup_cible_dry`

Contrairement aux autres capteurs de franchissement, ce capteur ne comporte pas de fallback explicite à ce niveau.

Ce choix repose sur l'hypothèse que `sensor.humidex_max_chambres` est considéré comme fiable et que les protections sont traitées en amont. Aucun traitement défensif supplémentaire n'est appliqué à ce niveau.

---

## Asymétrie max / min — COOL

Allumage COOL : basé sur `temperature_max_chambres`.  
Extinction COOL : basée sur `temperature_min_chambres`.

Cette asymétrie est volontaire :

- l'allumage se déclenche dès qu'une zone atteint une température élevée
- l'extinction attend que l'ensemble des zones redescendent sous le seuil

Ce mécanisme favorise une réactivité rapide à la surchauffe locale et une extinction stabilisée (évite les oscillations).

---

## Nature non déclenchée des seuils HEAT

**Entités :**
- `sensor.seuil_allumage_chauffage_clim`
- `sensor.seuil_extinction_chauffage_clim`

Ces capteurs sont définis comme Template Sensors continus (non déclenchés), contrairement aux seuils COOL qui sont déclenchés.

Leur mise à jour dépend des variations de `sensor.temperature_consigne_appliquee_locale` et des `input_number.clim_offset_on` / `clim_offset_off`.

Ce choix reflète leur nature : dérivation directe d'une consigne physique, sans logique contextuelle, contrairement aux seuils COOL dépendants de la présence (capteur contextuel)
