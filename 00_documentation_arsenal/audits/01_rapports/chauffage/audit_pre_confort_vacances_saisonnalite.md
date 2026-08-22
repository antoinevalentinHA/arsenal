# Audit — Pré-confort retour Vacances et pertinence saisonnière (Confort 19 °C en été)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit de la chaîne conduisant du retour de vacances programmé au passage du chauffage en **mode Confort**, et de l'absence de garde de **pertinence saisonnière** sur cette chaîne. Élément déclencheur : passage observé en Confort / 19 °C le **22 août** (saison `Été`). |
| **Domaine** | chauffage (contexte Vacances) |
| **Date** | 2026-08-22 |
| **Nature** | **Audit statique, lecture seule.** Aucun reboot, reload, appel de service ou changement d'état provoqué. **Aucun runtime / contrat / checker / UI / registre modifié par ce rapport.** |
| **Base** | HEAD `5a9a316`. |
| **Couverture** | Chaîne `vacances → pré-confort → Décision Centrale → écrivain unique → bridge MQTT chaudière` · contrats `vacances.md`, chauffage `30` (+ amendement), `40__amendement`, `50__amendement`, `65`, `66`, `70` (+ amendement), `75` §8, `80` (+ réécriture partielle) · `interface_ha_boiler_bridge.md` · rapport transverse #361 · chantier C21. |
| **Portée normative** | **Nulle.** Aucune architecture cible décidée, aucun chantier ouvert, aucune piste promue en décision. Les formulations normatives citées renvoient à des contrats **déjà** opposables et sont signalées comme telles. |

> **Règle appliquée.** Verdict porté sur le **code déployé** (templates, branches de décision,
> `mqtt.publish` suivi jusqu'au topic), pas sur la seule prose contractuelle. Lorsque runtime et contrat
> divergent, la divergence est **signalée**, le runtime n'est jamais présumé faire autorité.

> **Distinction de lecture.** **FAIT** (vérifié sur pièce) · **INTERPRÉTATION** (lecture fonctionnelle
> proposée) · **QUESTION OUVERTE** (arbitrage propriétaire requis). Aucun diagnostic n'est converti en
> décision.

---

## État Git au moment de l'audit

| Champ | Valeur |
|---|---|
| Branche | `claude/audit-vacances-chauffage-xrjvyg` |
| HEAD | `5a9a316` — *docs: refresh README metrics (#694)* |
| `git status --porcelain` | **vide** (arbre propre) |
| `git diff HEAD` | **vide** |

> L'audit lui-même s'est déroulé **intégralement en lecture seule** sur cet arbre propre.
> L'**intégration de ce rapport au corpus** (le présent fichier + sa référence dans
> [`audits/index.md`](../../index.md)) est un acte **postérieur et distinct**, réalisé sur demande
> explicite du propriétaire. Elle ne touche **aucun** runtime, contrat, checker, UI ni registre.

---

## Périmètre réellement audité

**Normatif (lu intégralement ou sur les sections décisives)**

- `00_documentation_arsenal/contrats/vacances.md` (v1.4.0, *Normatif — Clos*)
- `00_documentation_arsenal/contrats/chauffage/` :
  `30_decision_centrale.md` (+ `__amendement`), `40_blocages__amendement.md`,
  `50_standby_hysteresis__amendement.md`, `65_pre_confort_retour_vacances.md` (V3.1),
  `66_adaptation_consigne_vacances.md`, `70_autorisation_thermostat.md` (+ `__amendement`),
  `75_auto_ajustement_courbe.md` (§8), `80_table_decision_canonique.md` +
  `80_table_decision_canonique__reecriture_partielle.md`, `85` (via `30` / `mode_commande`)
- `00_documentation_arsenal/architecture/chauffage/interface_ha_boiler_bridge.md`
- `00_documentation_arsenal/audits/01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md` (#361)
- `00_documentation_arsenal/audits/04_chantiers/climatisation/chantier_preparation_retour_vacances_cool.md` (C21)
- `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md`

**Runtime**

- `11_automations/chauffage/pre_confort_vacances/{orchestrateur,cycle,notification}.yaml`
- `11_automations/chauffage/{decision_centrale_trigger,execution_mode_commande,autorisation,representativite_thermique}.yaml`
- `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml`
- `11_automations/system/saisons.yaml` · `11_automations/poele/blocage_chauffage.yaml`
- `10_scripts/chauffage/{decision_centrale,application_consigne,consigne_vacances}.yaml`
- `12_template_sensors/chauffage/{autorisation,autorisation_cible_selon_temperature,programme,mode_commande}.yaml`
- `12_template_sensors/chauffage/diagnostic/{mode,raison}.yaml` · `12_template_sensors/chauffage/pre_confort/*.yaml`
- `12_template_sensors/modes/vacances_actives.yaml` · `12_template_sensors/meteo/meteo_favorable.yaml`
- `12_template_sensors/poele/detection.yaml` · `12_template_sensors/boiler/bruleur/{bruleur_actif,mode,modes}.yaml`
- `14_mqtt_sensors/boiler/boiler_telemetry.yaml`
- Helpers : `03_input_numbers/chauffage/{consignes,seuils_temperature_exterieure,duree_prechauffage_vacances}.yaml`,
  `05_input_booleans/chauffage/{preconfort,preconfort_cycle,standby}.yaml`,
  `06_input_selects/system/saison.yaml`, `07_input_datetimes/vacances/vacances.yaml`
- `tools/arsenal_ci/` (checkers décision)

**`/ui`** : consulté uniquement pour vérifier la nature d'observation des cartes
(`19_button_card_templates/40_dashboards/chauffage/20_statut_metier/carte_chauffage_synthese.yaml`).
**Aucune logique métier en UI n'a été trouvée sur cette chaîne** — la distinction état métier / représentation est respectée.

---

## A. Comportement actuel — chaîne exacte

```
input_datetime.debut_vacances / fin_vacances + input_boolean.mode_vacances_auto
   └─ 11_automations/modes/vacances/programmation/orchestrateur.yaml
        → input_boolean.vacances_fenetre_active
   └─ binary_sensor.vacances_planifiees_actives → binary_sensor.vacances_demandees
   └─ binary_sensor.vacances_actives                     [12_template_sensors/modes/vacances_actives.yaml:45-50]
        = demandées ∧ presence_famille_unifiee=off ∧ visite_en_cours=off

fin_vacances − input_number.duree_prechauffage_retour_vacances (3–24 h)
   └─ sensor.pre_confort_debut_ts / _fin_ts              [pre_confort_debut_ts.yaml:41, :62]
   └─ binary_sensor.pre_confort_fenetre_valide (début < fin)
   └─ AUTOMATION 10240000000020 (orchestrateur)          [orchestrateur.yaml:88-96, :157-174]
        éligible = pre_confort_enable ∧ systeme_stable ∧ vacances_actives
                   ∧ fenêtre valide ∧ ts>0 ∧ ¬cycle_consomme ∧ ¬cycle_override
        et now ∈ [début ; fin[  →  input_boolean.pre_confort_actif_calcule = ON

   ├─ AUTOMATION 10240000000026 (cycle)  → pre_confort_cycle_consomme = ON  [cycle.yaml:43-46, :72-78]
   ├─ AUTOMATION 10240000000017 (notif)  → persistent_notification "🔥 Pré-confort fin Vacances"
   └─ AUTOMATION decision_centrale_trigger                [decision_centrale_trigger.yaml:83-84]
        → script.chauffage_decision_centrale

script.chauffage_decision_centrale — NIVEAU 2, branche Vacances
                                                         [decision_centrale.yaml:211-216 / :252-256]
   {% elif is_state('binary_sensor.vacances_actives','on') %}
     {% if is_state('input_boolean.pre_confort_actif_calcule','on') %} comfort
   →  desired_mode = comfort ; reason = pre_confort_vacances
   →  input_text.chauffage_raison = "pre_confort_vacances"
   →  input_select.chauffage_mode_session = "confort"
   →  event: chauffage_execution_requise ; timer anti-rebond démarré

sensor.chauffage_mode_commande (décision exécutoire, §85.2)  → "confort"
   └─ AUTOMATION 10240000000028                          [execution_mode_commande.yaml:120-155]
        gardes : systeme_stable ∧ mode_commande ∈ {confort,reduite} ∧ ≠ programme réel
        → script.chauffage_appliquer_consigne(consigne=confort, raison=pre_confort_vacances)

script.chauffage_appliquer_consigne                       [application_consigne.yaml:186-266]
   précheck : boiler_bridge_online=on · consigne valide · consigne numérique disponible
   → mqtt.publish  topic "boiler/command/heating/set_temperature"
                   value = input_number.chauffage_consigne_confort   ⇒ 19
   → attente ACK corrélé (request_id) → input_select.chauffage_dernier_mode_decide = comfort

Chaudière (bus MQTT — vérité externe)
   → boiler/telemetry/heating/setpoint → sensor.boiler_heating_setpoint
   → sensor.programme_chauffage = "Confort"               [programme.yaml:37-47]
```

> **Point structurant.** Le seul intrant saisonnier / thermique existant dans le domaine chauffage
> (`sensor.chauffage_autorisation_cible`) **n'est jamais lu sur ce chemin** : il n'est consulté qu'au
> **Niveau 3** (branche présence), que la branche Vacances court-circuite au **Niveau 2**.

---

## B. Autorités impliquées

| Autorité demandée | Existe ? | Porteur | Consultée sur cette chaîne ? |
|---|---|---|---|
| Programmation vacances | ✅ | `contrats/vacances.md` — vérité = `binary_sensor.vacances_actives` | **Oui** (déclencheur) |
| Anticipation / préchauffage retour | ✅ | contrat `65` — vérité = `input_boolean.pre_confort_actif_calcule`, écrivain unique `10240000000020` | **Oui** (déclencheur) |
| Saison / période de chauffe | ✅ (partiel) | `input_select.saison` (`06_input_selects/system/saison.yaml`), maintenu par `11_automations/system/saisons.yaml` (mois 6-7-8 → `Été`). Le helper déclare lui-même : *« Ne pilote AUCUN système (chauffage, clim, aération) »* | **Non** |
| Besoin thermique | ✅ | `sensor.chauffage_autorisation_cible` (contrat `70`) : `ext ≥ chauffage_seuil_ext_off` → `reduced` ; + modulation `suspension_relance_meteo` via `binary_sensor.meteo_favorable_chauffage` (amendement `70`) | **Non** (Niveau 3 uniquement) |
| Choix du mode chauffage | ✅ | `script.chauffage_decision_centrale` — arbitre unique (contrats `30` / `80`) | **Oui** — c'est elle qui produit `comfort` |
| Consignes | ✅ | `input_number.chauffage_consigne_confort` / `_reduite` / `_vacances` ; contrat `66` pour l'adaptation | **Oui** (valeur 19 émise) |
| Autorisation effective de chauffe | ⚠️ **vide** | `binary_sensor.chauffage_autorise_systeme` — **hook réservé, `state: {{ true }}` constant** depuis CH-2 (`autorisation.yaml:57`) | Oui, mais **toujours vraie** |
| Commande chaudière / actionneurs | ✅ | `script.chauffage_appliquer_consigne` (écrivain unique, transactionnel ACK) | **Oui** — commande MQTT réelle |

---

## C. Le comportement est-il prévu par les contrats ?

**Oui, explicitement — et le runtime est conforme.**

- `80_table_decision_canonique.md` §4, **ligne 6\*** :
  *« Absence effective Vacances (`vacances_actives = on`), pré-confort actif *(exception)* → `comfort` —
  Exception normative explicite »*, sous la seule réserve de l'absence de blocage pur (lignes 1 à 5).
- `80_table_decision_canonique__reecriture_partielle.md` §4.2 : reprend la règle à l'identique.
- `30_decision_centrale.md:90` : *« absence effective Vacances → `reduced`, **sauf exception normative
  explicite** : pré-confort actif → `comfort` »* ; et `:92` : *« La Décision Centrale est l'unique arbitre
  du contexte Vacances […] Aucune autre couche (capteur d'autorisation thermique, miroir de diagnostic)
  ne porte de logique Vacances. »*
- `65` §5 énumère limitativement les gardes hiérarchiques opposables au pré-confort : chauffage autorisé
  système, fenêtres fermées, aucune aération, aucun poêle, aucun blocage post-aération.
  **Aucun critère saisonnier ni thermique.** §5 pose au contraire la règle cardinale :
  *« Le pré-confort est déclenché exclusivement par une ANTICIPATION TEMPORELLE DE RETOUR,
  jamais par un seuil thermique. »*

> **Ce n'est donc pas un effet de composition non prévu : c'est la règle contractuelle appliquée telle
> qu'écrite.** Le caractère estival n'est traité **nulle part** — ni comme autorisé, ni comme interdit.

### Tensions normatives relevées

#### T1 — Asymétrie interne au corpus chauffage, sur exactement la même question

Le contrat `66` (*Adaptation consigne Vacances*, 2026-04-14) tranche déjà, pour un mécanisme voisin
déclenché par le **même** contexte Vacances et agissant sur le **même** domaine :

> *« La surcote Vacances vise exclusivement la protection du bâti pendant les périodes de chauffe.
> En été, le chauffage ne chauffe pas […] Elle est donc conditionnée à la saison. »*
> Invariant : *« Aucune surcote Vacances en vigueur pendant la saison `Été` »*
> Doctrine : *« La surcote Vacances protège le bâti en saison de chauffe, pas en été. »*

Le runtime correspondant l'implémente (`10_scripts/chauffage/consigne_vacances.yaml`, variable `est_ete`),
avec traitement explicite de `unknown` / `unavailable` (fail-safe assumé vers la protection du bâti).

**Le contrat `65` (pré-confort), pourtant plus intrusif — il produit une *décision*, pas un paramètre —
n'a aucun équivalent.**

#### T2 — La prémisse de `66` n'est pas garantie sur le chemin du pré-confort

`66` s'appuie sur *« en été, le chauffage ne chauffe pas »*. Le seul mécanisme du dépôt qui réalise cette
prémisse est `sensor.chauffage_autorisation_cible` (`ext ≥ seuil_ext_off → reduced`,
`autorisation_cible_selon_temperature.yaml:151-152`). Or la branche Niveau 2 du pré-confort **ne le
consulte pas**. La prémisse est vraie pour le chemin Niveau 3, **fausse pour le chemin pré-confort**.

#### T3 — `80` §9 contre `80` §4 ligne 6\*

`80` §9 range parmi les cas formellement interdits : *« Confort sans autorisation ❌ — Violation
séparation faits / décision »*. Le 22 août, `sensor.chauffage_autorisation_cible` vaut nécessairement
`reduced` (température extérieure ≥ seuil, borné à 24 °C max) et `input_boolean.chauffage_standby_force`
est posé — et pourtant `comfort` est décidé. L'exception 6\* prévaut par *lex specialis*, mais les deux
sections du même contrat se contredisent en apparence.
**Ambiguïté contractuelle, pas non-conformité runtime.**

#### T4 — Écart de couche déjà consigné, sans effet sur la saisonnalité

`65` §3 / §4 / §5ter et `70` (*Autorisations forcées amont*) décrivent le pré-confort comme émettant une
autorisation `comfort` **injectée dans la couche `70`**. Aucun consommateur de
`input_boolean.pre_confort_actif_calcule` n'existe dans `sensor.chauffage_autorisation_cible` : la
Décision Centrale lit le booléen **directement**. C'est le constat §6.3 du rapport #361, non soldé.

> **Important :** combler cet écart **ne corrigerait rien ici**. `70` stipule que *« toute autorisation
> forcée est strictement équivalente à une autorisation locale `comfort` »*, c'est-à-dire qu'elle
> **écraserait** la cible locale `reduced` au lieu de s'y soumettre. **L'écart de couche et la question
> saisonnière sont deux sujets distincts.**

---

## D. Effets réels — ce passage à Confort peut-il chauffer ?

> **Réponse tranchée : dans le périmètre Arsenal, rien ne le neutralise.
> Arsenal ne peut pas prouver l'absence de chauffe.**

### Ce qui est établi sur pièces

1. **Ce n'est pas un simple état logique.** Une commande MQTT réelle est publiée :
   `boiler/command/heating/set_temperature`, `value: 19`, avec attente d'ACK corrélé
   (`application_consigne.yaml:246-266`).
2. **Elle a été appliquée.** `sensor.programme_chauffage` est dérivé de `sensor.boiler_heating_setpoint`,
   c'est-à-dire de la **télémétrie retour de la chaudière** (`programme.yaml:37-47`). Observer « Confort »
   signifie que la chaudière **porte effectivement** la consigne 19 en mode confort — et non qu'un helper
   Home Assistant l'affiche.
3. **Aucune couche aval ne bloque.**
   - `binary_sensor.chauffage_autorise_systeme` : `state: {{ true }}` constant (`autorisation.yaml:57`) —
     hook réservé sans cause active.
   - `input_boolean.chauffage_standby_force` est bien à `on` en été (piloté par la cible `reduced`), mais
     il **n'a aucun consommateur exécutoire** : contrat `50` amendement A4/A5 le confirme (*« l'effet de
     `reduced` est porté au Niveau 3 »*), et la recherche runtime ne trouve que du log et un attribut
     d'observabilité.
   - Gardes restantes du script exécutif : bridge en ligne, consigne valide, idempotence.
     **Aucune garde thermique, aucune garde saisonnière.**
4. **La combustion effective dépend uniquement de la régulation propre de la chaudière** (courbe :
   `slope` / `shift` + sonde extérieure + éventuelle économie d'été). Le dépôt déclare explicitement ce
   domaine hors périmètre : `interface_ha_boiler_bridge.md` §2 (*« HA ne fait pas : interpréter la logique
   chaudière »*) et §3.3 (*« Le bridge expose uniquement des valeurs techniques »*).
   **Aucun contrat, aucune doctrine, aucun capteur du dépôt n'affirme une coupure estivale côté
   chaudière.** L'hypothèse « ça ne chauffera pas » est plausible physiquement, mais **elle n'est adossée
   à aucune pièce du dépôt** — c'est précisément ce que l'audit devait éviter de présupposer.

> **Conclusion C :** le passage à Confort n'est **pas** neutralisé par une couche Arsenal. Il constitue une
> **possibilité réelle de mise en chauffe**, dont la non-réalisation ne repose que sur un comportement
> chaudière non contractualisé et non observé ici.
> Preuve observable disponible si besoin : `sensor.boiler_burner_modulation` et
> `binary_sensor.bruleur_chauffage_actif` sur la fenêtre concernée.

### Effets sur d'autres composants (constatés, non spéculatifs)

| Effet | Preuve |
|---|---|
| `binary_sensor.bruleur_chauffage_actif` **armé** — sa première condition est `programme == 'Confort'` | `12_template_sensors/boiler/bruleur/bruleur_actif.yaml:36` |
| → `sensor.bruleur_mode` / `binary_sensor.bruleur_mode_chauffage` changent de régime | `boiler/bruleur/mode.yaml:28-31`, `modes.yaml:49` |
| → **la détection poêle est affectée** : `poele_en_fonction` exige `bruleur_mode_chauffage = off` (« chaudière hors cause ») | `12_template_sensors/poele/detection.yaml:124-126` |
| `pre_confort_cycle_consomme = on` — droit de pré-confort **consommé définitivement** pour le cycle Vacances, réinitialisable seulement sur `vacances_actives → off` | `cycle.yaml:43-46`, `:108-116` ; contrat `65` §7 |
| Notification persistante créée (*« Autorisation simulée : comfort »*) | `notification.yaml:52-62` |
| `sensor.pourcentage_consigne_eco_24h` / `_7j` dégradés (history_stats sur `programme_chauffage`) | `pourcentage_eco/24h.yaml:22` |

**Effet de second ordre, borné.** `sensor.pourcentage_consigne_eco_24h_proxy` alimente
`input_select.chauffage_representativite_thermique` (contrat `75` §8), **sans garde Vacances**
(`representativite_thermique.yaml:70-79`). Basculer en `REPRESENTATIF` exige eco < 40 % sur 24 h, soit
**> 14,4 h de Confort** — atteignable seulement si `duree_prechauffage_retour_vacances` ≳ 15 h (max 24).
L'auto-ajustement de courbe lui-même reste bloqué (`c2 : mode_maison == 'Normal'`,
`auto_ajustement.yaml:77`), mais **l'état de représentativité survit au retour en Normal**.
Exposition réelle mais étroite.

### Constat périphérique (hors sujet saisonnier, signalé pour complétude)

`40__amendement` A4 et `80…__reecriture` §4.3 / **INV-TBL-1** posent : *« Aucune décision `comfort` n'est
émise en présence d'un poêle corroboré, **y compris** dans le contexte Vacances + pré-confort »*, et
concluent que l'ordre des branches est *indifférent*.

**Au runtime il ne l'est pas** : `decision_centrale.yaml:211` (Vacances) précède `:218` (poêle). Un
`input_boolean.blocage_chauffage_poele` résiduel — c'est un verrou **latché par timer**, jamais levé par
le capteur (`11_automations/poele/blocage_chauffage.yaml:14-16`) — coexistant avec le pré-confort
produirait `comfort`. L'exposition est très étroite (`poele_en_fonction` exige
`presence_humaine_sejour`, incompatible avec `vacances_actives`), mais la conclusion « l'ordre est
indifférent » n'est pas vérifiée par la structure du code.

> **Non lié à l'objet de cet audit ; à traiter séparément si jugé utile.**

---

## E. Autorités existantes permettant de distinguer les trois notions

La question architecturale posée est exactement la bonne, et le dépôt **contient déjà les briques** —
dispersées, non composées.

| Notion | Autorité existante | Statut |
|---|---|---|
| « préparer le retour de vacances » | `input_boolean.pre_confort_actif_calcule` (contrat `65`) | ✅ existe, écrivain unique, boot-proof |
| « préparer **thermiquement** la maison » | *aucune autorité dédiée* — le pré-confort saute directement de l'intention temporelle à la décision `comfort` | ❌ **manquante** |
| « chauffage actuellement pertinent / autorisé » | trois candidats **existants** : `sensor.chauffage_autorisation_cible` (seuil extérieur `seuil_ext_off`) ; `binary_sensor.meteo_favorable_chauffage` + modulation `suspension_relance_meteo` (amendement `70`) ; `input_select.saison` (`Été`) | ✅ existent — **aucun n'est consulté** sur cette branche |
| « autorisation effective de chauffe » | `binary_sensor.chauffage_autorise_systeme` | ⚠️ **hook réservé, constant `true`** — l'emplacement architectural existe, il est vide |

### Précédent de gouvernance directement applicable

Le chantier **C21** (*Préparation COOL du retour de Vacances*, réservé / parqué) traite la question
symétrique côté climatisation et a **déjà tranché la doctrine d'arbitrage** :

> **I-C21-2 —** la préparation *« neutralise **uniquement** `(absence_longue OR vacances)`, **jamais**
> aération / fenêtres / blocage horaire / **température extérieure** / indisponibilités »*,
> avec fail-closed explicite et *« pas de fallback silencieux »*.

Autrement dit : **du côté climatisation, Arsenal a déjà décidé qu'une préparation de retour de vacances
ne lève pas la garde de température extérieure.** Le pré-confort chauffage, plus ancien, lève tout ce qui
se trouve au Niveau 3, garde extérieure comprise.

### Réponse à la question architecturale posée

> *« Le domaine vacances doit-il pouvoir demander un état de confort thermique sans connaître lui-même la
> pertinence saisonnière du chauffage, et quelle autorité doit alors arbitrer cette demande ? »*

Le domaine vacances **ne demande rien** — et c'est correct : `binary_sensor.vacances_actives` est une
vérité d'effectivité pure, sans effet de bord (`contrats/vacances.md` §3.4). Le demandeur est le mécanisme
**65**, qui **appartient déjà au domaine chauffage**.

**Aucune logique saisonnière n'a donc à être ajoutée au domaine vacances** — la doctrine est respectée sur
ce point. L'arbitre naturel est celui que `30:92` désigne déjà comme *« unique arbitre du contexte
Vacances »* : la **Décision Centrale**.

La question ouverte n'est donc pas *« qui arbitre ? »* mais :

> *« Sur quelle autorité de pertinence thermique la branche 6\* devrait-elle être gardée, et cette autorité
> doit-elle être `input_select.saison`, la cible thermique, ou une autorité `chauffage_autorise_systeme`
> enfin composée ? »*

---

## Qualification

> ### **Défaut de conception mineur.**

**Ce que ce n'est pas :**

- ❌ *défaut fonctionnel réel* — le runtime est **strictement conforme** à `80` §4 ligne 6\*,
  `80…__reecriture` §4.2 et `30:90`. Aucune règle n'est violée. La CI (`tools/arsenal_ci/decision/`)
  vérifie l'isomorphisme des axes, le miroir de diagnostic et la couverture des causes : elle est verte
  et le restera.
- ❌ *normal et souhaitable* — chauffer à 19 °C le 22 août n'a aucune finalité identifiable au regard de
  `65` §2 (*« réduire la violence thermique de la reprise »*, *« limiter les appels de puissance
  brutaux »*), objectifs vides de sens quand la maison est déjà au-dessus de la consigne.

**Ce que c'est, et pourquoi :**

1. Ce n'est pas une simple étrangeté sémantique : la branche **émet une commande physique réelle** à la
   chaudière (§D.1-2), et **aucune couche Arsenal ne l'arrête** (§D.3).
2. Ce n'est pas une composition accidentelle de règles correctes : c'est une **lacune de spécification**
   dans `65`, qui énumère limitativement ses gardes (§5) sans jamais poser la question de la pertinence
   saisonnière — alors que le contrat voisin `66`, sur le même contexte et le même domaine, l'a
   explicitement posée et tranchée trois mois plus tôt.
3. Il produit des effets mesurables hors du domaine (détection poêle, statistiques éco, représentativité
   thermique) et **consomme irréversiblement** le droit de pré-confort du cycle.
4. « Mineur » et non « majeur » parce que : la fenêtre est bornée, l'exposition est saisonnière
   (juin-août), la sobriété est probablement préservée de fait par la chaudière, et le mécanisme reste
   sous disjoncteur opérateur (`input_boolean.pre_confort_enable`).

---

## Risques

| # | Risque | Portée |
|---|---|---|
| **R1** | **Chauffe estivale réelle non exclue** — aucune preuve dans le dépôt d'une coupure aval ; la non-combustion repose sur un comportement chaudière non contractualisé | Consommation gaz, usure brûleur |
| **R2** | **Précédent doctrinal** — C21 cite `65` comme *« patron d'orchestration (référence) »*. Si la lacune saisonnière n'est pas nommée, elle risque d'être recopiée. C21 s'en prémunit déjà (I-C21-2), mais le registre parle du *« patron chauffage **sans ses dettes** »* — encore faut-il que la dette soit inscrite | Gouvernance |
| **R3** | **Contradiction interne de `80`** (§9 « Confort sans autorisation ❌ » vs §4 ligne 6\*) non résolue | Lisibilité normative |
| **R4** | **Contagion représentativité thermique** — bornée aux durées de préchauffage ≳ 15 h, mais l'état survit au retour en Normal et peut débloquer l'auto-ajustement de courbe sur données non représentatives | Calibration courbe |
| **R5** | **Écart de couche `65` / `70`** (rapport #361 §6.3) toujours ouvert — indépendant, mais il entretient l'illusion qu'une garde thermique s'appliquerait déjà | Documentaire |
| **R6** | **Risque du remède** — toute garde saisonnière posée dans la mauvaise couche violerait `30:92` (*« aucune autre couche ne porte de logique Vacances »*) ou `70` §7 (*« l'autorisation locale ne connaît jamais les vacances »*). Le point d'application est **contraint, pas libre** | Architecture |

---

## Options architecturales

> *Présentées comme espace de décision. **Aucune n'est choisie, aucun code n'est produit.***

| # | Option | Autorité concernée | Avantages | Inconvénients |
|---|---|---|---|---|
| **O0** | **Ne rien changer**, acter le comportement dans `65` comme conséquence assumée | — | Zéro risque ; conforme aux contrats actuels | Laisse R1 sans preuve, R2/R3 ouverts ; le corpus reste asymétrique (`66` conditionné, `65` non) |
| **O1** | **Documentaire seul** — amender `65` pour nommer la lacune saisonnière + lever la contradiction `80` §9 / §4 ; aucun runtime | `65`, `80` | Restaure la cohérence normative sans risque ; conforme au principe *« contrat avant runtime »* | Ne change rien au comportement ni à R1 |
| **O2** | **Garder la branche 6\* sur la cible thermique** : le pré-confort ne produit `comfort` que si `sensor.chauffage_autorisation_cible` n'est pas `reduced` | Décision Centrale (`30` / `80`) | Réutilise une autorité **existante** ; aucun helper, aucun concept nouveau ; homogène avec I-C21-2 côté clim ; l'`unknown` est déjà géré à la source | Contredit `65` §5 (*« jamais par un seuil thermique »*) — exige une révision explicite de `65` ; le pré-confort devient partiellement conditionnel à la thermique |
| **O3** | **Garder sur `input_select.saison`** (`Été` → pas de pré-confort), sur le modèle exact de `66` | Décision Centrale, lecture seule de `saison` | Symétrie parfaite avec `66` ; sémantique explicite (« préparer le retour » ≠ « saison de chauffe ») ; précédent de traitement `unknown` / `unavailable` déjà écrit | `saison` se déclare *« ne pilote AUCUN système »* → cette doctrine devrait être amendée ; découpage par mois, grossier ; deuxième source de vérité saisonnière à côté du seuil extérieur |
| **O4** | **Composer enfin `binary_sensor.chauffage_autorise_systeme`** — le hook réservé porterait une cause de pertinence (saison et/ou extérieure), interdisant `comfort` à **tous** les niveaux | Niveau 1, contrats `30` / `50` / `80` | L'emplacement architectural existe déjà et est vide ; couvre le pré-confort **et** toute future branche ; réponse structurelle à la question posée | Le plus lourd : `autorisation.yaml` est explicitement un registre **sécurité** (D0/D1) ; y loger une cause de sobriété serait une inversion de registre — précisément ce que CH-2 a démonté. Exigerait une révision de la doctrine des registres (`01`) |
| **O5** | **Déplacer la fenêtre** — rendre `pre_confort_actif_calcule` lui-même conditionné (garde dans l'orchestrateur `10240000000020`) | Contrat `65`, orchestrateur | Le mécanisme s'auto-désactive ; la Décision Centrale reste inchangée ; `sensor.pre_confort_raison` gagne un état diagnostique lisible | Déplace une décision de pertinence thermique dans un orchestrateur déclaré *« aucune décision centrale »* (`65` §5ter) — risque de duplication d'autorité |

**Observation transverse.** O2 et O5 diffèrent sur *où* l'arbitrage vit ; O3 et O4 diffèrent sur *quelle*
autorité de pertinence fait foi. Les quatre supposent une **révision préalable de `65`**, puisque sa règle
cardinale (§5 : *« jamais par un seuil thermique »*) interdit aujourd'hui la plupart d'entre elles.

Aucune ne peut être conduite sans trancher d'abord la question de fond :

> **« Préparer le retour de vacances » est-il un besoin de confort inconditionnel,
> ou un besoin subordonné à la pertinence thermique du moment ?**

Le corpus a déjà répondu deux fois, dans deux directions différentes — `66` (subordonné) et `65`
(inconditionnel).

---

## GO / NO-GO

> ### **GO pour ouvrir un chantier — de nature d'abord normative.**

Le comportement n'est **pas** un bug : il est prescrit. Mais la conclusion *« rien à modifier, l'autorité
de chauffe située en aval empêche déjà toute chauffe estivale »* est **fausse sur pièces** : cette autorité
aval est `binary_sensor.chauffage_autorise_systeme`, et elle est un `state: {{ true }}` constant. Aucune
couche Arsenal ne neutralise le passage à Confort ; le dépôt ne contient aucune preuve du contraire côté
chaudière.

L'incohérence métier est réelle et documentable : **deux mécanismes du même corpus, tous deux déclenchés
par `binary_sensor.vacances_actives`, tous deux agissant sur le chauffage, sont traités de façon
opposée** — `66` conditionné à la saison avec fail-safe explicite, `65` inconditionnel.

### Périmètre recommandé pour l'ouverture *(sans préjuger de la solution)*

1. **Lot normatif d'abord** — trancher la question de fond (le pré-confort est-il subordonné à la
   pertinence thermique ?), amender `65` en conséquence, lever la contradiction `80` §9 / §4 ligne 6\*.
   Conforme à la doctrine *« contrat avant runtime »* et au précédent C20 / C21.
2. **Lot probatoire, préalable à toute décision runtime** — établir sur données réelles ce que la chaudière
   a effectivement fait pendant la fenêtre observée (`sensor.boiler_burner_modulation`,
   `binary_sensor.bruleur_chauffage_actif`, `sensor.boiler_supply_temperature`). Cela répond à **R1 par la
   preuve plutôt que par l'intuition**, et détermine la priorité du chantier (P2 si combustion, P3 sinon).
   **Instrumentation recorder à vérifier au préalable** — le registre C20 / C22 montre que ce point a déjà
   été un angle mort deux fois.
3. **Lot runtime** — seulement après 1 et 2.
4. **Hors périmètre, à consigner séparément** : l'écart de couche `65` / `70` (#361 §6.3), et l'ordre de
   branches poêle / Vacances au regard d'INV-TBL-1.

**Priorité suggérée : P3**, relevable en **P2** si le lot 2 démontre une combustion réelle.

**Aucun caractère bloquant** : le disjoncteur `input_boolean.pre_confort_enable` permet une neutralisation
opérateur immédiate en attendant, et la fenêtre estivale se referme début septembre.

---

*Rapport d'audit statique, lecture seule — non normatif, non prescriptif.*
*Aucun runtime, contrat, checker, UI, registre ou workflow CI modifié. Aucun patch proposé.*
