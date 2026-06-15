# Audit UI — Dashboard diagnostics vannes thermostatiques

> **Périmètre audité :** dépôt `antoinevalentinHA/arsenal`. Dashboard `18_lovelace/dashboards/diagnostics/vannes_thermo.yaml`, ses templates `button-card`, l'`input_select` de sélection de pièce, le script de reset plateau, les capteurs sources, la doctrine couleur UI et la doctrine de socle KPI.
> **Nature :** audit **lecture seule**, consigné a posteriori. La correction de l'écart V-1 a été appliquée par un patch UI séparé (voir §5). V-2 et V-3 restent ouverts.
> **Référence couleur opposable :** [`06_kpi.md`](../../../ui/socle_ui/06_kpi.md) (doctrine de socle), [`02_palette.md`](../../../ui/couleurs/02_palette.md), [`05_regles.md`](../../../ui/couleurs/05_regles.md).
> **Complément :** audit UI voisin du même axe → [`audit_dashboard_diagnostics_chauffage.md`](audit_dashboard_diagnostics_chauffage.md). Suivi des arbitrages ouverts → [`suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md`](../../04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md).
> **Méthode :** traçage `entity_id` → définition pour les 3 pièces, extraction systématique des `rgba()`/hex, vérification du flux reset (script → input_number → capteur), comparaison du style maison `badge_action_confirmee`, vérification de navigation.

---

## 1. Résumé exécutif

| Indicateur | Valeur |
|---|---|
| Vue auditée | 1 (`vertical-stack` unique) |
| Tuiles `button-card` | 5 (4 KPI + 1 verdict) — toutes `action: none` |
| Cartes interactives | 2 : 1 `tile` sélecteur (natif) + 1 `badge_action_confirmee` (action confirmée) |
| Références d'entités mortes | **0** (3 pièces × 3 capteurs + affichage + 3 input_numbers + script + input_select : tous résolus) |
| Cibles de navigation non résolues | **0** (bidirectionnel chauffage ↔ vannes) |
| Action pilotant du matériel | **0** (le seul script écrit un `input_number` de diagnostic) |
| Écart UI V-1 | **CORRIGÉ** (patch séparé) |
| Arbitrages restants | V-2, V-3 (ouverts) |

**Verdict :** dashboard fonctionnellement sain et, après correction de V-1, **conforme sur l'axe couleur UI**. Le sous-domaine reste toutefois **non contractualisé** (V-3) et porte une frontière de classification UI non gouvernée (V-2).

---

## 2. Fichiers inspectés

**Dashboard** — `18_lovelace/dashboards/diagnostics/vannes_thermo.yaml` ; enregistrement dans `18_lovelace/dashboards.yaml` (`diagnostics-vannes-dashboard`).

**Templates `button-card`** (`19_button_card_templates/40_dashboards/chauffage/60_thermostatique/`) — `thermo_plateau_strict_72`, `thermo_plateau_affichage_72`, `thermo_mean_12h_72`, `thermo_variance_12h_72` (ce dernier contient aussi `thermo_stabilite_12h_status`). Plus `10_generiques/badges/badge_action_confirmee` et les socles `socle_kpi_label_72_sans_icone`, `socle_status_72`.

**Helpers / script / capteurs** — `06_input_selects/chauffage/piece_analyse_vanne.yaml` (`input_select.adjustment_piece`, 3 options) ; `10_scripts/chauffage/reset_plateau.yaml` (`script.reset_plateau_piece`) ; `03_input_numbers/chauffage/plateau_temperature.yaml` ; `12_template_sensors/chauffage/vannes_thermostatiques/{plateaux_stricts,affichage_plateau}.yaml` ; `13_sensor_platforms/statistics/chauffage/vannes_thermostatiques/chambre_{arnaud,matthieu,parents}.yaml`.

**Contrat documentaire dédié** — **aucun** (cf. V-3).

---

## 3. Cartographie

Une vue, un `vertical-stack`. Badges : Accueil · Navigation · Retour → `/diagnostics-chauffage-dashboard/diagnostics-chauffage`.

| Ordre | Carte | Type | Template | Cible |
|---|---|---|---|---|
| 1 | Header | `button-card` | `section_header` | — |
| 2 | Pièce sélectionnée | `tile` natif + `select-options` | — | `input_select.adjustment_piece` |
| 3a | Plateau strict | `button-card` | `thermo_plateau_strict_72` | `sensor.plateau_thermostatique_<piece>` |
| 3b | Plateau affiché | `button-card` | `thermo_plateau_affichage_72` | `sensor.plateau_thermostatique_piece_affichage` |
| 3c | Moyenne 12h | `button-card` | `thermo_mean_12h_72` | `sensor.temperature_stats_12h_mean_<piece>` |
| 3d | Variance 12h | `button-card` | `thermo_variance_12h_72` | `sensor.temperature_stats_12h_variance_<piece>` |
| 4 | Stabilité 12h | `button-card` | `thermo_stabilite_12h_status` | verdict couleur sur la variance |
| 5 | Reset plateau | `badge_action_confirmee` | → `script.reset_plateau_piece` | reset d'une donnée de diagnostic |

**Routage dynamique :** 4 cartes construisent l'`entity_id` cible à partir de `input_select.adjustment_piece`. La carte 3b lit un capteur fixe.

---

## 4. Constats validés

1. **Aucune référence morte.** Les 3 options (`chambre_arnaud`, `chambre_matthieu`, `chambre_parents`) mappent toutes à des capteurs existants (plateau strict, mean 12h, variance 12h), plus le capteur fixe d'affichage et les 3 `input_number` cibles du reset.
2. **Flux reset cohérent et tracé.** `script.reset_plateau_piece` écrit `input_number.plateau_chambre_<piece> = 0` ; le capteur `plateau_thermostatique_<piece>` lit `input_number.plateau_<suffixe>` (ancre YAML partagée) → le reset efface bien le plateau mémorisé.
3. **Seuils de détection plateau possédés par le backend.** `var < 0.02 and mean > 0` vit dans le capteur (`plateaux_stricts.yaml`), pas dans l'UI.
4. **Action bornée, confirmée, non-pilotante.** `badge_action_confirmee` exige une confirmation explicite ; le script ne pilote aucune vanne, ne modifie aucune consigne, ne déclenche aucune régulation (garanties écrites dans le script ET dans l'`input_select`). Reset de **donnée de diagnostic**, explicitement anticipé par le contrat du helper.
5. **Navigation bidirectionnelle saine.** Dashboard enregistré, atteint depuis le dashboard chauffage, retour déclaré. Zéro lien mort.
6. **Lecture seule des tuiles.** Les 5 tuiles `button-card` sont `action: none` (explicite sur les KPI, hérité de `socle_status_72` sur le verdict).
7. **Carte verdict exemplaire.** `thermo_stabilite_12h_status` applique la priorité indisponibilité (`rgba(158,158,158,0.1)`), l'escalade vert → orange → rouge, et `Number.isFinite` (robustesse totale).

---

## 5. V-1 — CORRIGÉ

**Écart constaté (avant patch) :** les 4 cartes KPI (`thermo_plateau_strict_72`, `thermo_plateau_affichage_72`, `thermo_mean_12h_72`, `thermo_variance_12h_72`) conservaient un fond bleu info fixe `rgba(33,150,243,0.2)` même quand la donnée cible était `unknown`/`unavailable`, ne dégradant que le texte (`—`). Cela contredisait la doctrine de leur propre socle ([`06_kpi.md`](../../../ui/socle_ui/06_kpi.md) : indisponibilité → `rgba(158,158,158,0.1)`) et la priorité indisponibilité de [`05_regles.md`](../../../ui/couleurs/05_regles.md).

**Correction appliquée (patch UI séparé) :** dans les 4 templates, le `background-color` statique est remplacé par un calcul qui **calque exactement le prédicat de disponibilité du `state_display` de chaque carte** :
- indisponibilité / valeur non exploitable → `rgba(158, 158, 158, 0.1)` ;
- valeur exploitable → `rgba(33, 150, 243, 0.2)` (bleu info inchangé).

Le fond gris et le texte `—` restent ainsi synchronisés. **Seules** les couleurs de fond des 4 KPI ont changé : aucun renommage d'entité/ID/alias/template, aucun seuil modifié, `action: none` préservé, carte verdict et `badge_action_confirmee` intacts. Le pattern reproduit celui, déjà conforme, de `thermo_stabilite_12h_status`.

**Statut :** ✅ résolu. L'axe couleur UI du dashboard est désormais conforme.

---

## 6. Arbitrages encore ouverts

### V-2 — OUVERT : seuils de classification du verdict codés en UI + duplication backend
`thermo_stabilite_12h_status` classe « Très stable / Modérément stable / Instable » à partir de seuils littéraux `0.02` et `0.05` inscrits dans le template. Le `0.02` est **dupliqué** avec le backend (`plateaux_stricts.yaml` : `var < 0.02`). Pas de source unique de vérité ; dérive silencieuse possible si le critère backend évolue. Carte diagnostique pure → pas une violation de « le backend décide », mais une frontière de classification non gouvernée. **Non traité dans la passe V-1.**

### V-3 — OUVERT : sous-domaine sans contrat de gouvernance
Le sous-domaine vannes thermostatiques comprend capteurs, `input_number`, un **script d'écriture** (`reset_plateau`), un `input_select` et un dashboard — mais aucun document de `00_documentation_arsenal/contrats/` ne le contractualise (seules traces : changelogs v8/v12). Gap vis-à-vis de « contrats explicites avant tout YAML », d'autant plus notable qu'il inclut une écriture d'état. **Gap documentaire, pas défaut UI. Non traité dans la passe V-1.**

---

## 7. Faux problèmes — à NE PAS corriger

- **FV-1 — « Action/service dans un dashboard de diagnostic ».** À ne pas retirer. `badge_action_confirmee` est une primitive Arsenal établie (aussi dans `18_lovelace/includes/badges/ecs_reglages_sauvegarde_restore.yaml` et les dashboards imprimerie) ; ici confirmée (pas cachée), non-pilotante, et explicitement contractée comme reset de donnée de diagnostic.
- **FV-2 — `icon_color: "#EF6C00"` (hex opaque).** Conforme au style maison : `badge_action_confirmee` associe un fond `rgba(…,0.2)` à une icône hex Material 800 assortie (bleu `#1565C0`, vert `#2E7D32`, rouge `#B71C1C`, orange `#EF6C00`). Convention établie.
- **FV-3 — Orange pour l'action reset.** Affordance d'action (sévérité), cohérente cross-domaine ; pas un encodage d'état « warning ».
- **FV-4 — `tile` interactif sur `input_select.adjustment_piece`.** Sélecteur de pièce de diagnostic, sa raison d'être. Carte HA native, ne pilote rien.
- **FV-5 — Mono-vue / 2ᵉ segment `navigation_path` sans path de vue.** Style maison (cf. audit chauffage). Ne pas ajouter de `path:`.
- **FV-6 — Rouge sur « Instable ».** Usage réel : la charte liste « état défavorable » sous rouge ; escalade vert → orange → rouge cohérente.
- **FV-7 — « Dashboard dense ».** Faux. Le dashboard est compact. Rien à simplifier.

---

## 8. Conclusion

Le dashboard diagnostics vannes thermostatiques est **fonctionnellement sain**, et **l'écart UI V-1 est désormais corrigé** : les 4 cartes KPI dégradent correctement leur fond en gris indisponibilité, conformément à la doctrine de leur socle.

Restent ouverts, hors de la passe de correction V-1 :
- **V-2** — gouvernance des seuils `0.02` / `0.05` du verdict (codés en UI, `0.02` dupliqué backend) ;
- **V-3** — le sous-domaine **n'est toujours pas documenté contractuellement**, malgré capteurs, helpers, script de reset et dashboard.

En résumé : **dashboard corrigé sur l'écart UI V-1, mais sous-domaine encore à documenter contractuellement.** Les deux arbitrages sont suivis dans [`suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md`](../../04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_vannes_thermostatiques.md).
