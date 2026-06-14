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

Cette asymétrie est volontaire et reflète la topologie **mono-zone** du système (un seul climatiseur sur le palier, chambres ouvrables/fermables, aucun capteur de porte ; pilotage multi-zones explicitement hors périmètre — voir `11_perimetre_exclu.md`) :

- **Allumage indexé sur la chambre la plus chaude** (`temperature_max_chambres`) : réactivité à la surchauffe locale — aucune pièce chaude n'est ignorée.
- **Extinction indexée sur la chambre la plus froide** (`temperature_min_chambres`) : en régime de refroidissement, la pièce la plus froide est presque toujours une pièce **couplée** (porte ouverte), donc une pièce que le climatiseur **contrôle effectivement**. Indexer l'extinction sur elle garantit que l'état **OFF reste atteignable**.

**Intention réelle.** L'extinction n'attend **pas** que toutes les zones repassent sous le seuil (cela imposerait `max` pour OFF). Le critère `min`-OFF empêche qu'une chambre **thermiquement découplée** (porte fermée, hors d'atteinte de l'appareil de palier) ne maintienne **indéfiniment** la climatisation active. Rappel `01_finalite.md` : « OFF est un état normal et volontaire, jamais une erreur ».

⚠️ **Portée exacte de la garantie.** `min`-OFF protège l'atteignabilité de OFF **uniquement lorsque la chambre la plus chaude est repassée sous le seuil d'allumage** (le franchissement ON est prioritaire dans `besoin_clim_cool`). Au-dessus du seuil d'allumage, c'est le critère d'**allumage sur le max** qui gouverne le maintien en marche, indépendamment de l'extinction.

**Compromis assumé.** En régime entièrement **couplé** (toutes portes ouvertes) et avec un écart inter-chambres ≥ hystérésis, le revers de `min`-OFF est un arrêt **possiblement précoce** de la pièce la plus chaude accessible. Ce compromis est **accepté** : il est borné et auto-corrigé (la pièce se réchauffe et redéclenche, ou l'utilisateur ouvre une porte). Le compromis **refusé** est celui qu'imposerait `max`-OFF : un **acharnement climatique** sur une chambre fermée, sans échappatoire automatique. Analyse complète : `audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md`, Phase 6.

---

## Nature non déclenchée des seuils HEAT

**Entités :**
- `sensor.seuil_allumage_chauffage_clim`
- `sensor.seuil_extinction_chauffage_clim`

Ces capteurs sont définis comme Template Sensors continus (non déclenchés), contrairement aux seuils COOL qui sont déclenchés.

Leur mise à jour dépend des variations de `sensor.temperature_consigne_appliquee_locale` et des `input_number.clim_offset_on` / `clim_offset_off`.

Ce choix reflète leur nature : dérivation directe d'une consigne physique, sans logique contextuelle, contrairement aux seuils COOL dépendants de la présence (capteur contextuel)
