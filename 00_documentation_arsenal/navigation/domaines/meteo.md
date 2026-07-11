# 🌦️ Hub de domaine — Météo

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Domaine météo extérieure : observation et structuration des données météo (température jardin, humidité jardin, pluie, palmarès, affichage). Distinct de `temperature_interieure` et `humidite_relative_interieure` — deux domaines propres co-hébergés sous `contrats/meteo/` **pour des raisons d'héritage documentaire** (arbitrage acté — voir [`carte_domaines.md`](../carte_domaines.md) §5.3). Trois docs architecture. Audit partiel (rapport + plan d'action, **non clôturé**).

## Contrat — « ce que le système doit faire »

**Fondation :**
- Entrée : [`gouvernance.md`](../../contrats/meteo/gouvernance.md)
- Contrat principal : [`meteo.md`](../../contrats/meteo/meteo.md)
- Validation : [`validation.md`](../../contrats/meteo/validation.md)

**Axes extérieurs :**
- [`axe_temperature_jardin.md`](../../contrats/meteo/axe_temperature_jardin.md)
- [`axe_humidite_relative_jardin.md`](../../contrats/meteo/axe_humidite_relative_jardin.md)

**Analytics :**
- [`extrema_jour_courant.md`](../../contrats/meteo/extrema_jour_courant.md)
- [`tendance_temperature.md`](../../contrats/meteo/tendance_temperature.md)
- [`palmares_chaleur.md`](../../contrats/meteo/palmares_chaleur.md)
- [`palmares_froid.md`](../../contrats/meteo/palmares_froid.md)
- [`palmares_min_haute.md`](../../contrats/meteo/palmares_min_haute.md)
- [`pluie_palmares.md`](../../contrats/meteo/pluie_palmares.md)

**Précipitations :**
- [`pluie_production.md`](../../contrats/meteo/pluie_production.md) — production / qualification des signaux de précipitation (autorité de la frontière d'entrée de `volets_pluie.md`)

**Affichage :**
- [`affichage.md`](../../contrats/meteo/affichage.md)

> `contrats/meteo/axe_temperature.md` (axe température intérieure) est physiquement co-hébergé ici mais appartient au domaine `temperature_interieure` (voir vigilance).

## Architecture — « comment / pourquoi »

- [`capteurs_meteo.md`](../../architecture/capteurs_meteo.md) — capteurs météo & climat intérieur *(voir vigilance)*
- [`meteo_affichage.md`](../../architecture/meteo_affichage.md) — affichage météo
- [`meteo_interpretation_contextuelle.md`](../../architecture/meteo_interpretation_contextuelle.md) — modèle d'interprétation contextuelle (amont de l'affichage)

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md). État : chaîne partielle, domaine **non clôturé**.

- Rapport final — [`audit_meteo_axe_temperature_rapport_final.md`](../../audits/01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md)
- Plan d'action — [`plan_action_meteo_axe_temperature.md`](../../audits/03_plans_action/meteo/plan_action_meteo_axe_temperature.md)
- Audit affichage — [`audit_affichage_meteo.md`](../../audits/01_rapports/meteo/audit_affichage_meteo.md)
- Audit tendance température (sensibilité) — [`audit_tendance_temperature_sensibilite.md`](../../audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md) — faux `stable` ; **contrat [`tendance_temperature.md`](../../contrats/meteo/tendance_temperature.md) amendé v1.1**, runtime en écart temporaire (contrat §18), correction runtime à venir.

> **Changelog** (pas de chantier dédié) : mentions diffuses `v15_7_2`, `v15_7_3`, `v15_8_3`, `v15_8_9`.

## Liens croisés (sens & appartenance)

- **temperature_interieure** — [`contrats/meteo/temperature_interieure/`](../../contrats/meteo/temperature_interieure/) ; domaine propre co-hébergé dans `contrats/meteo/` pour des raisons d'héritage documentaire (carte §5.3).
- **humidite_relative_interieure** — [`contrats/meteo/humidite_relative_interieure/`](../../contrats/meteo/humidite_relative_interieure/) ; idem.
- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; consomme les données météo extérieures (température jardin, dérive thermique) — aval.
- **Climatisation** — [`contrats/climatisation/`](../../contrats/climatisation/) ; consomme l'humidex (dérivé température + humidité) — aval.

## Organisation des vues — pages live & records (chantier C7, réalisé)

> **NON NORMATIF — état final.** Note d'orientation ; aucune donnée ni capteur n'est concerné. Détail faisant foi : [`audits/04_chantiers/lovelace/cadrage_palmares_meteo.md`](../../audits/04_chantiers/lovelace/cadrage_palmares_meteo.md) (chantier **C7**, clos).

- **Pages météo de consultation courante** : elles restent centrées sur l'**état du jour**, les **valeurs courantes**, les **cumuls** et les **graphes** utiles — lecture « live », pas archive.
- **Palmarès historiques** : les **trois** palmarès (chaud, froid, précipitations) sont **regroupés** dans la destination dédiée **Palmarès météo**, atteinte depuis le hub Navigation (bouton « Rec. météo »). *Min · Max* et *Précipitations* n'en portent plus.
- **Sans effet sur la donnée** : cette destination **réunit** des cartes de restitution existantes ; **aucune donnée ni aucun capteur** n'est modifié, et les contrats palmarès restent inchangés (UI hors périmètre).

## Points de vigilance (non normatif)

- **`axe_temperature.md`** dans `contrats/meteo/` = axe température **intérieure** — appartient au domaine `temperature_interieure` malgré son hébergement physique ici (héritage documentaire, carte §5.3).
- **`capteurs_meteo.md`** (architecture/) titre « météo & **climat intérieur** » : couvre les capteurs des domaines co-hébergés — document antérieur à l'arbitrage de séparation des domaines.
- **Audit partiel** : axe température (rapport + plan d'action) et affichage (audit de découverte) — domaine non clôturé.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
