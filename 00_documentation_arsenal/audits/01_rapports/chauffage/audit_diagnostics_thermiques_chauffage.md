# 🧠 ARSENAL — AUDIT ARCHITECTURAL — Diagnostics thermiques du chauffage

**Périmètre audité :** `00_documentation_arsenal/contrats/chauffage/15_capteurs/` (docs 08 à 12) + implémentations réelles, consommateurs, dashboards, recorder, CI.
**Nature :** audit de fondations — aucun patch, aucune implémentation, aucune modification runtime proposée.
**Méthode :** lecture des 5 contrats + index (13), traçage par `entity_id` de chaque capteur dans tout le dépôt, vérification contrat↔implémentation, couverture recorder, recherche de consommateurs décisionnels.

---

## 0. Cartographie reconstruite (état réel du dépôt)

Le sous-domaine est **réellement implémenté** : les 13 capteurs structurants décrits aux contrats 08–11 existent tous en YAML. Répartition par famille :

| Famille (contrat) | Capteur (`sensor.*`) | Fichier d'implémentation |
|---|---|---|
| **C — Inertie absence (08)** | `duree_stabilisation_absence_chambres` | `…/absence/duree_stabilisation.yaml` |
| | `temperature_plancher_absence_chambres` | `…/absence/temperature_plancher.yaml` |
| **B — Cycles présence (09)** | `amplitude_oscillation_cycle_presence_chambres` | `…/cycles/amplitude_oscillation_cycle_presence_chambres.yaml` |
| | `duree_cycle_moyenne_presence_chambres` | `…/cycles/duree_cycle_moyenne.yaml` |
| | `nombre_cycles_jour_presence_chambres` | `…/cycles/nombre_cycles_par_jour.yaml` |
| **A-arrêt — Inertie arrêt (10)** | `temperature_arret_presence_chambres` *(ancre B0)* | `…/inertie_arret/temperature_arret_presence_chambres.yaml` |
| | `amplitude_overshoot_arret_presence_chambres` | `…/inertie_arret/amplitude_overshoot_arret_presence_chambres.yaml` |
| | `duree_overshoot_arret_presence_chambres` | `…/inertie_arret/duree_overshoot_arret_presence_chambres.yaml` |
| | `vitesse_refroidissement_presence_chambres` | `…/inertie_arret/vitesse_refroidissement_presence_chambres.yaml` |
| **A-reprise — Inertie reprise (11)** | `temperature_reprise_presence_chambres` *(ancre A1)* | `…/inertie_reprise/temperature_reprise_presence_chambres.yaml` |
| | `amplitude_chute_reprise_presence_chambres` | `…/inertie_reprise/amplitude_chute_reprise_presence.yaml` |
| | `duree_chute_reprise_presence_chambres` | `…/inertie_reprise/duree_chute_reprise_presence_chambres.yaml` |
| | `vitesse_reprise_presence_chambres` | ⚠️ `…/**inertie_arret**/vitesse_reprise_presence_chambres.yaml` |

**Couche de consommation (aval) — entièrement en lecture seule :**

- **4 synthèses texte** (`…/syntheses/`) : `regulation.yaml` (lit `amplitude_oscillation`), `stabilite.yaml` (lit `nombre_cycles_jour`), `inertie.yaml` (lit `vitesse_refroidissement`), `reprise.yaml` (lit `vitesse_reprise`). Aucune n'appelle de `service`/`action` → publication textuelle pure, conforme.
- **Dashboards** (`18_lovelace/includes/cartes/`) : `diagnostic_thermique_inertie`, `_oscillateur`, `_reprise`, `_contexte`, `_interpretation`.

**Constat d'isolation (capital) :** aucun composant de `10_scripts/`, `11_automations/`, `06_input_selects/`, ni la décision centrale (`01_capteurs_decision`, `30_decision_centrale`), ni l'autorisation thermostat, **ne consomme ces 13 capteurs par leur `entity_id`**. L'auto-ajustement de courbe existant (contrat 06) repose **exclusivement** sur une autre famille (`sensor.ecart_consigne_*`, `pente_suggeree`, `parallele_suggeree`) et **ne câble aucun** des 13 capteurs diagnostiques.

> 👉 Le sous-domaine est aujourd'hui un **îlot d'observabilité pure** : mesure riche, **zéro raccordement décisionnel**. C'est doctrinalement correct (un diagnostic ne décide jamais) — mais cela signifie que la valeur décisionnelle reste **entièrement potentielle**.

---

## A. Audit détaillé

### A.1 — Cohérence contrat ↔ implémentation

Le socle doctrinal est **solide et réellement respecté** sur la grande majorité des capteurs : ancrage événementiel (A1/B0), idempotence/anti-replay, invariance numérique `float|none`, figement intra-cycle. Trois écarts méritent attention, par ordre de gravité :

**🔴 Écart majeur — `duree_stabilisation_absence_chambres` viole son propre contrat (08).**
Le contrat 08 impose deux règles cardinales pour toute la couche absence : (a) **NEUTRALISATION PAR AÉRATION** via `input_boolean.aeration_pipeline_arme`, et (b) **VALIDITÉ DES CYCLES** — durée d'absence **≥ 3600 s** sinon état forcé à `unknown`, aucune valeur par défaut. Or :

- `temperature_plancher.yaml` (même famille, même contrat) implémente **correctement les deux** : flag `cycle_valide` latché, publication conditionnée à `duree >= 3600`, neutralisation aération.
- `duree_stabilisation.yaml` **n'implémente ni l'une ni l'autre** : aucune référence à `aeration_pipeline_arme` (seul capteur du sous-domaine dans ce cas — 12/13 l'implémentent), aucun gate ≥ 3600 s, et le `state` retombe sur **la valeur numérique précédente** (`last = this.state | float(0)`) au lieu de `unknown`.

Conséquence concrète : un cycle d'absence pollué par une aération, ou un cycle < 1 h, **publie quand même une durée de stabilisation** — qui alimente la carte `diagnostic_thermique_inertie`. C'est une métrique potentiellement fausse présentée comme structurante. Incohérence intra-famille la plus actionnable de l'audit.

**🟠 Écart de taxonomie — `vitesse_reprise_presence_chambres` mal rangé.**
Capteur de la famille **reprise** (contrat 11, qui le déclare consommateur de l'ancre A1), mais implémenté dans le dossier `inertie_arret/`. `unique_id` correct, fonctionnellement sain, mais viole le principe d'index « un fichier = une frontière » et brouille la lecture de la cartographie.

**🟡 Robustesse — détection de stabilisation dépendante de l'échantillonnage.**
`duree_stabilisation` ne latche la stabilisation que lors d'un **nouvel échantillon** de `temperature_min_chambres` (gate `now() - t_candidate >= 5400`). Si la température se stabilise au point de ne plus émettre de changement d'état, aucun trigger ne survient et la stabilisation **peut ne jamais être figée**. Défensif sur le plan doctrinal (pas de temps vivant), mais fragile sur le plan physique.

### A.2 — Mono-zone structurel

**L'intégralité du sous-domaine repose sur une seule source thermique : `sensor.temperature_min_chambres`.** Toutes les inerties, vitesses, amplitudes et cycles décrivent le **minimum de la zone chambres**, c.-à-d. la pièce la plus froide (radiateurs les plus éloignés, forte inertie — cohérent avec le contexte connu du logement). C'est un choix défendable (zone-pilote = pire cas), mais toute interprétation « bâtiment » est en réalité une interprétation « chambres ». Aucune observabilité multi-zone, aucune vue séjour/global.

### A.3 — Absence de normalisation météo / ΔT

Les contrats 08 et 10 listent eux-mêmes « comparaisons inter-saison non normalisées » comme **risque surveillé** — mais aucun capteur de normalisation n'existe. `vitesse_refroidissement` et `temperature_plancher` dépendent massivement de la température extérieure ; bruts, ils ne sont **pas comparables d'un cycle à l'autre** ni d'une saison à l'autre. Ce sont des grandeurs physiques honnêtes, mais **non encore des signatures d'isolation/inertie exploitables** pour de l'apprentissage.

### A.4 — Persistance (Recorder) — angle mort critique

`recorder.yaml` fonctionne en **liste blanche explicite** (`include: entities:`). Trois capteurs en sont **absents** :

- `vitesse_refroidissement_presence_chambres` (°C/h — perte thermique)
- `vitesse_reprise_presence_chambres` (°C/h — récupération)
- `temperature_reprise_presence_chambres` (**ancre A1**)

Ces trois-là sont précisément les plus pertinents pour l'auto-ajustement (dynamiques °C/h + borne zéro de reprise). **Sans historique : pas de statistiques, pas de tendance, graphes vides en dashboard, et aucun substrat possible pour un apprentissage supervisé.** Asymétrie notable : l'ancre B0 (`temperature_arret`) est enregistrée, l'ancre A1 (`temperature_reprise`) ne l'est pas.

### A.5 — Pas de mesure de rendement / efficacité

Aucune métrique de **duty-cycle**, de **temps de chauffe**, de **runtime chaudière** ou d'**énergie** dans le sous-domaine. L'« efficacité du chauffage » demandée n'est donc **pas observée**. Les cycles comptent des *occurrences* et des *périodes*, jamais du *temps de marche* ni de la *consommation*.

---

## B. Tableau de synthèse par capteur

Confiance = robustesse + représentativité + exploitabilité (historisation incluse).

| Capteur | Objectif | Qualité | Utilité | Réutilisabilité | Confiance | Statut |
|---|---|---|---|---|---|---|
| `temperature_reprise` *(A1)* | Ancre thermique début reprise | Haute (ancre brute) | Fondatrice (7 consommateurs) | Vacances, clim | **Moyenne** (⚠️ non recordée) | **Améliorer** (recorder) |
| `amplitude_chute_reprise` | Erreur initiale post-reprise | Bonne | Réglage offset ON | Vacances | Bonne | Conserver |
| `duree_chute_reprise` | Latence de reprise | Bonne | Réglage offset ON | Aération, vacances | Bonne | Conserver |
| `vitesse_reprise` | Récupération °C/h | Bonne mais non normalisée | Courbe, **préchauffage** | Vacances, aération | **Faible** (⚠️ non recordée + mal rangé) | **Améliorer** |
| `temperature_arret` *(B0)* | Ancre thermique arrêt | Haute (ancre brute) | Fondatrice arrêt | Clim | Bonne | Conserver |
| `amplitude_overshoot_arret` | Surchauffe inertielle | Bonne | Réglage offset OFF | Clim | Bonne | Conserver |
| `duree_overshoot_arret` | Latence hydraulique | Bonne | Réglage offset OFF | Clim | Bonne | Conserver |
| `vitesse_refroidissement` | Perte thermique °C/h | Bonne mais non normalisée | **Isolation**, **blocage post-aération** | Aération, vacances, énergie | **Faible** (⚠️ non recordée + non normalisée) | **Améliorer** |
| `amplitude_oscillation_cycle` | Oscillation autour consigne | Bonne | Qualité hystérésis | Clim | Bonne | Conserver |
| `duree_cycle_moyenne` | Période propre | Bonne | Stabilité régulation | Clim, diagnostics | Bonne | Conserver |
| `nombre_cycles_jour` | Charge de cyclage | Bonne | Usure, court-cycle | Clim, énergie, diag | Bonne | Conserver |
| `temperature_plancher_absence` | Plancher passif | Bonne (validité OK) | Isolation, **préchauffage** | Vacances, énergie | Moyenne (non normalisée) | Conserver |
| `duree_stabilisation_absence` | Durée mise à l'équilibre | **Fragile** (contrat violé) | Inertie passive | Vacances | **Faible** | **Améliorer (prioritaire)** |

*Aucun capteur n'est à supprimer.* Le sous-domaine est cohérent ; les faiblesses sont de **fiabilisation** et de **valorisation**, pas de conception.

---

## C. Cartographie des usages futurs

| Métrique | Cas d'usage décisionnel cible | Prérequis manquant |
|---|---|---|
| `vitesse_reprise` + `temperature_plancher_absence` | **Préchauffage vacances** : estimer durée pour passer du plancher froid à la consigne confort | Historisation ; **représentativité de régime** (la reprise mesurée part d'un *réduit*, pas d'un *cold-soak* vacances → transfert non direct) |
| `vitesse_refroidissement` + `duree_chute_reprise` | **Blocage post-aération adaptatif** : durée de blocage = f(perte thermique réelle + latence de récupération) | Historisation ; normalisation ΔT |
| `vitesse_refroidissement` (normalisée ΔT) + `temperature_plancher` | **Signature d'isolation** / détection de dérive d'isolation long terme | Capteur de normalisation météo/ΔT (absent) |
| `amplitude_overshoot` + `duree_overshoot` | Réglage supervisé **offsets OFF** | Couche de proposition supervisée (absente) |
| `amplitude_chute` + `vitesse_reprise` | Réglage supervisé **offsets ON** + agressivité courbe | Couche de proposition supervisée (absente) |
| `nombre_cycles_jour` + `duree_cycle_moyenne` | **Alarme court-cyclage** / usure chaudière ; KPI santé MQTT | Seuil de diagnostic (à porter hors couche, en 07) |
| Toute la cinématique cycles | **Réutilisation climatisation** (court-cycle/hystérésis refroidissement) | Généralisation du patron à la source thermique clim |

---

## D. Recommandations priorisées

Classées par (valeur décisionnelle × robustesse) / coût. **Aucune n'est implémentée ici — ce sont des orientations.**

**P0 — Fiabiliser avant toute valorisation (coût faible, robustesse haute)**
1. **Mettre `duree_stabilisation_absence` en conformité contrat 08** : neutralisation aération + gate ≥ 3600 s + `unknown` sur cycle invalide. C'est un correctif de gouvernance, pas une amélioration : aujourd'hui le capteur peut publier du faux.
2. **Ajouter les 3 capteurs manquants au recorder** (`vitesse_reprise`, `vitesse_refroidissement`, `temperature_reprise`). Sans historique, toute la section C est inatteignable. Coût quasi nul, déblocage maximal.
3. **Reclasser le fichier `vitesse_reprise` dans `inertie_reprise/`** (cohérence index).

**P1 — Rendre les dynamiques exploitables (coût moyen, valeur décisionnelle haute)**
4. **Introduire une couche de normalisation ΔT/météo** (intérieur−extérieur) : keystone manquant pour transformer les °C/h bruts en signatures d'isolation/inertie comparables. Sans elle, l'auto-ajustement apprendra du bruit saisonnier.
5. **Ajouter un « rendement de cycles valides »** (compteur cycles retenus vs invalidés par aération/durée) : aujourd'hui la qualité de la donnée n'est ni tracée ni auditable.

**P2 — Construire le pont décisionnel (coût moyen-élevé, valeur stratégique)**
6. **Créer une couche explicite de *proposition supervisée*** (les contrats l'autorisent déjà comme « aval : lecture/proposition uniquement »), distincte des capteurs et de la décision centrale, où les diagnostics deviennent des *suggestions* d'offset/durée — jamais des écritures directes.
7. **Réévaluer la représentativité de régime** pour le préchauffage vacances : la reprise présence n'est pas un proxy fiable d'un démarrage à froid prolongé. Confiance préchauffage = **faible** tant que ce point n'est pas levé (idéalement par une mesure de reprise post-absence longue).

**P3 — Étendre la couverture (coût élevé, valeur long terme)**
8. **Mesure d'efficacité** (duty-cycle / runtime / énergie) : seul moyen de répondre à « efficacité du chauffage », non couverte aujourd'hui.
9. **Observabilité multi-zone** : sortir du mono-`temperature_min_chambres` pour distinguer zones.

---

## Verdict sur `12_capteurs_observabilite_pure.md`

**État réel : fichier 0 octet, et — point important — absent de la table d'orientation officielle de l'index (`13_capteurs_index.md`), qui ne liste que les frontières 01 → 11.** C'est donc un **orphelin documentaire** : référencé dans le dossier, mais hors de la cartographie canonique.

**Recommandation : le conserver et lui donner un rôle réel**, car plusieurs préoccupations légitimes n'ont **aucun propriétaire contractuel** aujourd'hui :
- la **doctrine de persistance** (qui doit être recordé, à quelle granularité — précisément le trou des 3 capteurs non historisés) ;
- le **rendement de cycles valides** / qualité de donnée ;
- la **doctrine d'export** (vers `ha-state-archive` / MQTT self-supervision).

Ces sujets sont l'essence même d'une « observabilité pure » : des signaux dont l'unique finalité est d'être enregistrés, tracés et exportés, sans qualification ni seuil (par opposition aux capteurs structurants qui *ancrent* les cycles, et aux synthèses qui *qualifient* en texte). Le doc 12 est l'endroit naturel pour cela.

**À défaut** (s'il n'est pas doté de ce mandat), il devrait être **supprimé** et son intention fusionnée dans `07_capteurs_diagnostics_structurants.md` — un fichier vide dans une cartographie « opposable » est lui-même une violation de gouvernance.

---

## Conclusion — les fondations sont-elles suffisantes pour un auto-ajustement fiable ?

**Conception : oui. État opérationnel : pas encore.**

Le découpage en frontières d'autorité, la discipline événementielle et l'isolation stricte décision/diagnostic sont d'un niveau qui supporte sans réécriture une future couche d'intelligence thermique. Mais **trois manques bloquants** se dressent entre l'état actuel et un auto-ajustement fiable : (1) les dynamiques décisives ne sont **pas historisées**, (2) elles ne sont **pas normalisées** (donc non comparables), et (3) il n'existe **aucune couche de proposition** entre l'observation et la décision. Tant que P0 et P1 ne sont pas traités, le niveau de confiance pour piloter un blocage post-aération ou un préchauffage vacances reste **faible** — non par défaut de mesure, mais par défaut de **fiabilisation, de persistance et de représentativité**.
