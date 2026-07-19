# 🧠 ARSENAL — CONTRAT · CHAUFFAGE — VANNES THERMOSTATIQUES / PLATEAUX STRICTS

> **Nature :** contrat de gouvernance d'un **sous-domaine de diagnostic et de mémoire** du chauffage.
> **Statut :** normatif — consolide l'existant runtime sans le modifier.
> **Frontière capitale :** ce sous-domaine **ne décide jamais**. Il observe, mémorise, affiche. Aucune valeur de plateau n'alimente une décision ou une consigne chauffage.

---

## 1. Objet et périmètre

Ce contrat gouverne le sous-domaine **plateaux thermostatiques stricts** des chambres équipées de vannes thermostatiques (TRV) : la **détection** d'un plateau thermique stable, sa **mémoire persistante**, son **écriture** (automatique et manuelle), son **affichage** et son **verdict visuel de stabilité**.

Pièces couvertes : `chambre_enfants`, `chambre_matthieu`, `chambre_parents`.

Hors périmètre : toute décision, autorisation, consigne ou commande de chauffage (gouvernées par les contrats `00`/`30`/`70` et la table canonique `80`).

## 2. Statut et nature

Le plateau est une **mémoire thermique de diagnostic** : la dernière température de stabilisation stricte observée par pièce. C'est une **valeur intermédiaire**, pas une consigne. Le sous-domaine est **hors pipeline décisionnel** : il n'est subordonné à aucun contrat de décision et n'en commande aucun.

## 3. Entités concernées

| Rôle | Entité | Couche runtime |
|---|---|---|
| Détection | `sensor.plateau_thermostatique_chambre_{parents,enfants,matthieu}` | `12_template_sensors/chauffage/vannes_thermostatiques/plateaux_stricts.yaml` |
| Affichage | `sensor.plateau_thermostatique_piece_affichage` | `12_template_sensors/chauffage/vannes_thermostatiques/affichage_plateau.yaml` |
| Mémoire | `input_number.plateau_chambre_{enfants,matthieu,parents}` | `03_input_numbers/chauffage/plateau_temperature.yaml` |
| Écriture auto | automation `Chauffage – Mémorisation plateaux` | `11_automations/chauffage/update_plateaux_thermostatiques.yaml` |
| Reset (user) | `script.reset_plateau_piece` | `10_scripts/chauffage/reset_plateau.yaml` |
| Sélecteur pièce | `input_select.adjustment_piece` | (paramétrage) |
| Affichage / verdict | cartes `thermo_plateau_strict_72`, `thermo_plateau_affichage_72`, `thermo_mean_12h_72`, `thermo_variance_12h_72`, `thermo_stabilite_12h_status` | `19_button_card_templates/40_dashboards/chauffage/60_thermostatique/` |
| Dashboard | vue diagnostic vannes | `18_lovelace/dashboards/chauffage/vannes_thermo.yaml` |

## 4. Sources statistiques 12 h

La détection s'appuie exclusivement sur les capteurs `statistics` natifs, par pièce :

- `sensor.temperature_stats_12h_mean_chambre_<piece>` — moyenne glissante 12 h ;
- `sensor.temperature_stats_12h_variance_chambre_<piece>` — variance thermique 12 h.

Ces capteurs sont la **seule** entrée de la détection de plateau.

## 5. Détection du plateau strict

Règle, par pièce (capteurs `plateau_thermostatique_chambre_*`) :

- **Si** `variance_12h < 0.02` **et** `mean_12h > 0` → plateau = `mean_12h` arrondie à 0,1 °C ;
- **Sinon** → fallback sur la **valeur mémorisée** dans l'`input_number` correspondant ;
- Le capteur est **numérique** : il ne renvoie **jamais** `unknown` ni `unavailable` — le fallback mémoire est toujours assuré.

## 6. Mémoire persistante

Trois helpers stockent le dernier plateau strict valide, par pièce :

- `input_number.plateau_chambre_enfants`
- `input_number.plateau_chambre_matthieu`
- `input_number.plateau_chambre_parents`

Bornes : `min: 0`, `max: 30`, `step: 0.1`. **Stockage uniquement** — aucun calcul, aucune logique métier, aucun comportement autonome porté par ces helpers.

## 7. Writers autorisés

Seuls **deux** writers peuvent écrire ces helpers :

1. **Automation** `update_plateaux_thermostatiques` (`Chauffage – Mémorisation plateaux`, `mode: single`) — écriture **automatique** : déclenchée par un changement d'état des capteurs `plateau_thermostatique_chambre_*`, elle met à jour l'`input_number` **uniquement si** `variance < 0.02` **et** que la variation dépasse `0.1 °C` (évite les écritures inutiles et les boucles d'auto-mémorisation).
2. **Script** `reset_plateau_piece` — écriture **manuelle** (cf. §8).

Tout autre writer est interdit. Toute écriture doit rester **traçable à son auteur** (automation ou reset).

## 8. Reset

- **Action utilisateur uniquement** : `script.reset_plateau_piece`, appelé **exclusivement** depuis un bouton du dashboard diagnostic.
- **Jamais automatique** : aucun trigger, aucune automation ne déclenche le reset.
- **Ciblage** : la pièce visée est lue dans `input_select.adjustment_piece`.
- **Effet** : remet la valeur mémorisée de la pièce ciblée à `0`, forçant une reprise propre de l'observation. Effet **strictement local** (une pièce), sans impact global sur le chauffage.

## 9. Frontières

| Couche | Présence | Précision |
|---|---|---|
| Diagnostic / détection | ✅ | capteurs `plateau_thermostatique_*` sur stats 12 h |
| Mémoire / écriture d'état | ✅ | `input_number.plateau_chambre_*` ; 2 writers (§7) |
| Action utilisateur | ✅ | reset ponctuel (§8) |
| Affichage | ✅ | capteur d'affichage + cartes `60_thermostatique` |
| Verdict visuel | ✅ | `thermo_stabilite_12h_status` + axe couleur |
| **Décision chauffage** | ❌ | **hors périmètre — non câblée** : aucune décision, consigne ou ajustement ne lit le plateau |

## 10. Interdits / invariants

| Code | Énoncé |
|---|---|
| VP1 | Le plateau n'est jamais utilisé comme **consigne** thermique. |
| VP2 | Aucune **décision** chauffage n'est déclenchée depuis ces helpers ou capteurs. |
| VP3 | Aucun **ajustement automatique** (courbe, offsets) ne consomme le plateau. |
| VP4 | **Stockage ≠ détection** : on ne détecte jamais un plateau depuis l'`input_number` ; la détection vit dans les capteurs. |
| VP5 | Le reset est une action **utilisateur ponctuelle**, **jamais** automatique. |
| VP6 | Les capteurs de plateau ne renvoient **jamais** `unknown` (fallback mémoire systématique). |
| VP7 | Toute écriture des helpers est **traçable à son auteur** ; seuls les 2 writers du §7 sont autorisés. |
| VP8 | **Aucune promotion décisionnelle** du plateau sans **amendement explicite** de ce contrat. |

## 11. Seuils

Le seuil **`0.02`** (variance 12 h) est **canonique** : il définit le **plateau strict** et la **stabilité stricte** pour ce sous-domaine. Il est la référence unique côté détection (`plateaux_stricts.yaml`) et écriture (`update_plateaux_thermostatiques`).

> **V-2 (ouvert, hors de ce contrat).** Les cartes UI dupliquent encore des seuils de verdict (`0.02` / `0.05`) codés côté affichage. Tant que cette duplication subsiste, V-2 reste ouvert : la canonisation ci-dessus pose la source unique, mais le **dé-doublonnage UI** relève d'une passe distincte (touche `19_button_card_templates/`). Ce contrat **ne corrige pas** V-2.

## 12. UI / Lovelace

- **Dashboard diagnostic** : `18_lovelace/dashboards/chauffage/vannes_thermo.yaml` — expose mean/variance 12 h, plateau strict, plateau d'affichage, verdict de stabilité, et le bouton de reset, le tout filtré par `input_select.adjustment_piece`.
- **Cartes** : famille `60_thermostatique` (`*_72`).
- **Verdict couleur** : porté par `thermo_stabilite_12h_status` et l'axe couleur des cartes.
- **Indisponibilité** : le fond gris d'indisponibilité doit rester conforme à la charte UI (`ui/couleurs/`) ; cet axe a été corrigé (V-1).

## 13. Relations avec les contrats voisins

- [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) — autorisation/exécution des TRV ; **distinct** : ce contrat ne touche pas l'autorisation, seulement l'observation du plateau.
- [`72_offsets_thermiques_lecture_physique.md`](72_offsets_thermiques_lecture_physique.md) — lecture physique et réglage des seuils ; voisinage thématique, **sans** consommation du plateau.
- [`75_auto_ajustement_courbe.md`](75_auto_ajustement_courbe.md) / [`76_observabilite_auto_ajustement_courbe.md`](76_observabilite_auto_ajustement_courbe.md) — auto-ajustement de courbe (chantier C5 d'observabilité) : **ne consomme pas** le plateau aujourd'hui. Tout câblage futur relèverait de VP8 (amendement explicite).

## 14. Maintenance / évolution

- **Ajout d'un writer** : tout nouveau writer des helpers `plateau_chambre_*` doit être **contractualisé** ici (mise à jour du §7) avant câblage runtime.
- **Câblage décisionnel** : toute consommation du plateau par une décision/ajustement exige un **amendement explicite** (VP8) ; sans cet amendement, la frontière du §9 prévaut.
- **Changement de seuil** : toute évolution du `0.02` doit passer par une **source unique** (ce contrat, §11) et être répercutée de façon cohérente détection ↔ UI (cf. V-2).
