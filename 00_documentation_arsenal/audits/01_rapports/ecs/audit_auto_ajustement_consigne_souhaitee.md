# Audit Arsenal — ECS / Auto-ajustement de la consigne souhaitée (étude d'opportunité)

> Type : rapport d'audit exploratoire — étude d'opportunité (aucune décision d'implémentation).
> Portée : opportunité d'un futur mécanisme d'auto-ajustement de la **consigne ECS souhaitée** — l'abaisser (recommander/ajuster) quand les usages réels laissent une marge d'eau chaude, notamment par forte chaleur ou moindre besoin. Distinct de la boucle d'apprentissage des **offsets** existante (consigne **envoyée**).
> Mode : lecture seule — aucun runtime, contrat, YAML, CI ni UI modifié ; aucun patch produit ; aucune entité créée ; aucun ID inventé.
> Référence dépôt : branche `main`, HEAD `f291e67`.
> Limite de méthode : audit sur l'état committé de `main` (clone). Le runtime Home Assistant n'a pas été observé ; « comportement runtime » = déduit des sources + sémantique d'exécution Home Assistant.
> Contre-expertise associée : [`02_contre_expertises/ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md`](../../02_contre_expertises/ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md) — réexamen adversarial qui **tempère** la présente conclusion (à lire conjointement).
> Principe directeur : *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Contexte

La température ECS est réglable par l'opérateur (dashboard). Une logique d'ajustement de la consigne **envoyée** à la chaudière existe déjà (offsets, contrat `11`). L'idée étudiée : quand les usages montrent qu'il reste de l'eau chaude après les cycles (douches soir/matin), Arsenal pourrait recommander — puis, à terme, ajuster — une consigne **souhaitée** plus basse. La désinfection hebdomadaire reste hors négociation. L'étude part de l'existant, sans présumer de la pertinence de l'idée.

## 2. Cartographie de l'existant

| Couche | Élément | Rôle |
|---|---|---|
| Consigne **souhaitée** (opérateur) | `input_number.ecs_consigne_temperature` (+ `ecs_consigne_vaisselle`, `ecs_temperature_desinfection`) | Cible à atteindre. **Aucun écrivain automatique.** |
| Consigne **envoyée** | `effective_target_int = souhaitée − offset_bucket` (calcul mémoire, `10_scripts/ecs/cycle.yaml`) → `input_text.ecs_target_temp_session` → bridge MQTT | Publiée à la chaudière ; volontairement **inférieure** à la souhaitée. |
| Boucle d'apprentissage | `script.ecs_autocorrect_offsets` (contrat `11_ajustement_des_offsets.md`) | Correcteur proportionnel discret **sur les `ecs_off_*` uniquement** (§2.2). Calibre l'envoyée pour atteindre la souhaitée. |
| Température ballon | `sensor.ecs_temperature_ballon_securisee` (sonde unique, ~30 s, historisé) ; `input_number.ecs_temperature_max_reelle_figee` | Observable central. |
| Cycle | `input_boolean.ecs_cycle_en_cours`, `ecs_fin_cycle_signal`, `input_text.ecs_resume_dernier_cycle_fige` (`date\|mode\|consigne\|t0\|boost\|valide`), `ecs_duree_dernier_cycle_figee` | Signaux + résumé figé. |
| Désinfection | mode hebdo (`ecs_desinfection_active`, `input_select.ecs_desinfection_jour`, `input_datetime.ecs_desinfection_heure`) + retour-vacances souverain (`input_boolean.ecs_desinfection_retour_due`) | Invariant (contrat `09`). |

**Point cardinal.** L'automatisme existant est **confiné au moyen technique (offset)** ; la cible souhaitée est un **intrant stable**. Un auto-ajustement de la souhaitée serait une **seconde boucle, en amont**, de nature différente : elle **n'existe pas** (confirmé contrats + runtime).

## 3. Données disponibles pour raisonner

| Besoin | Disponible | Statut |
|---|---|---|
| Température ballon (marge résiduelle) | `sensor.ecs_temperature_ballon_securisee` | fiable, historisé — mais **sonde unique** |
| Tmax réelle / durée figées | `ecs_temperature_max_reelle_figee`, `ecs_duree_dernier_cycle_figee` | historisés |
| Contexte thermique | `sensor.temperature_jardin`, `sensor.temperature_moyenne_maison`/`_sejour` | historisés |
| Présence / mode | `binary_sensor.presence_famille_unifiee`, `input_select.mode_maison` | historisés |
| Fenêtres d'usage | `input_datetime.ecs_<jour>_<matin/soir>_heure`, `binary_sensor.ecs_creneau_ponctuel_en_cours` | **non historisés** |
| Puisage / débit / volume | — | **absent** |
| Énergie ECS (kWh, temps flamme) | — | **absent** |
| Consigne souhaitée historisée | `input_number.ecs_consigne_temperature` | **non historisé** |

## 4. Lacunes

1. **Pas de mesure du besoin réel** : aucun capteur de puisage/débit/volume, une seule sonde ballon, pas d'eau froide entrante → le « reste utile » n'est pas **mesurable**, seulement **inférable** (trajectoire ballon).
2. Le système **ne distingue pas** l'inertie d'un tirage d'eau (`reference_thermique_post_inertie_ecs.md` §9.1) : la brique « il restait de l'eau chaude » n'existe pas.
3. **Aucune donnée d'énergie ECS** → pas d'arbitrage coût/confort, gains non mesurables.
4. Consigne souhaitée et fenêtres d'usage **non historisées** ; **aucun** `statistics`/`history_stats` ECS.

## 5. Faisabilité : **PARTIELLE**

- Observabilité d'une marge résiduelle : **inférable** (proxy : température ballon avant la chauffe suivante), non mesurée ; moyennant des ajouts d'historisation.
- Distinguer « pas de besoin » d'un « défaut de chauffe » : **partiel** (macro via présence/vacances ; micro non fiable sans mesure de tirage).
- Détecter les fenêtres d'usage sans intrusion : **partiel** (créneaux planifiés = bornes, pas douches réelles).

## 6. Modèle de décision *théorique* (hypothèse documentaire — non validée)

Formulé sans conclure à une implémentation, dans le respect de la séparation observabilité / décision / action / diagnostic / UI :

- **Observabilité** (read-only) : dériver une marge résiduelle et un indice de moindre besoin, sans aucune écriture décisionnelle.
- **Recommandation** (« conseil seulement ») : *si* marge résiduelle **récurrente** sur N jours **et** contexte de moindre besoin **et** aucune contre-indication → **recommander** une baisse d'un palier prudent (sortie diagnostic, **jamais** d'écriture de consigne).
- **Décision / action** : différée, **après validation architecturale** et une période de conseil probante ; par paliers, bornée par les planchers de sécurité (10 °C nominal, ≥ 15 °C effectif, `min_target`).
- **Interdictions de baisse** : confort insuffisant, chauffe anormale, donnée indisponible (abstention), désinfection proche/en cours, marge sanitaire insuffisante.
- **Remontée automatique prioritaire** : tout usage réel ou inconfort probable prime.
- **Découplage des deux boucles** : la boucle « souhaitée » devrait tourner à une constante de temps nettement plus lente que la boucle offsets (ou geler l'une pendant l'autre) pour éviter l'oscillation croisée.

## 7. Risques

| Risque | Gravité | Note |
|---|---|---|
| Confort familial (douche froide « économisée ») | élevé | échec produit |
| Enfants / bains / usages exceptionnels | élevé | un pic ponctuel ne doit pas être « appris » comme norme |
| Légionellose / désinfection | critique | jamais toucher désinfection ni plancher sanitaire |
| Faux positifs météo chaude | moyen | exiger la **récurrence** + garde saisonnière |
| Défaut de capteur (sonde unique) | moyen | `unavailable` → abstention, jamais « marge » |
| Économies surestimées | moyen | aucun capteur d'énergie → gain non prouvable |
| Complexité pour gain marginal | moyen | 2ᵉ boucle coûteuse en gouvernance |

## 8. Recommandation

**Pertinent — mais uniquement en observabilité / recommandation à ce stade.** La brique de mesure manque (pas de tirage, pas d'énergie, sonde unique) ; agir sur la consigne serait piloter à l'aveugle sur un domaine à fort enjeu confort/sanitaire. Le domaine possède déjà le bon patron (apprentissage offsets + observabilité) et Arsenal a un précédent méthodologique éprouvé (chantier observabilité auto-ajustement courbe chauffage : observer/prouver avant d'agir). La voie propre est **d'abord observer et conseiller**, prouver le gain, *puis* seulement — après validation architecturale — envisager une éventuelle auto-action bornée.

## 9. Conclusion

> **✅ Pertinent, mais uniquement en observabilité / recommandation (« conseil seulement »).**
> **Pas** d'auto-ajustement de la consigne souhaitée à ce stade : la base de mesure (tirage réel, énergie, « reste utile ») n'existe pas et n'est qu'**inférable**, sur un domaine à fort enjeu confort + sanitaire. La désinfection reste hors négociation en toute hypothèse.
>
> **Nuance importante :** cette conclusion est **réexaminée et tempérée** par la contre-expertise associée ([`contre_expertise_auto_ajustement_consigne_souhaitee.md`](../../02_contre_expertises/ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md)), qui — en posture adversariale — juge l'idée **prématurée et partiellement en rupture** avec l'architecture existante. Les deux documents doivent se lire ensemble.

---

*Rapport d'audit exploratoire — lecture seule. Aucune modification du dépôt, aucun code, aucun plan d'implémentation.*
