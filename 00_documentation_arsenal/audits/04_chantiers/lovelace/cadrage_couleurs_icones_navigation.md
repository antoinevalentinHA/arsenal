# 🎨 Dossier d'arbitrage — Couleurs d'icônes des tuiles de navigation

> **Type :** dossier d'arbitrage Lovelace / UI (non décisionnel). **Document faisant foi** du sujet (pointé par `REGISTRE_CHANTIERS.md`).
> **ID registre :** `D-NAV-COULEUR`. **Statut :** **À arbitrer / dormant** — constat posé, aucune action ordonnancée.
> **Règle qui fait foi :** [`ui/couleurs/03_exceptions.md`](../../../ui/couleurs/03_exceptions.md) § *Exception 3 — Couleurs dynamiques d'icône en contexte NAV/HUB*.
> **Discipline :** aucune modification UI tant qu'un arbitrage n'est pas tranché ; co-commit du registre à chaque changement d'état.

---

## 0. Constat

L'Exception 3 réserve l'icône des tuiles de navigation à **4 couleurs opaques** (`rgb(244,67,54)` 🔴, `rgb(76,175,80)` 🟢, `rgb(33,150,243)` 🔵, `rgb(158,158,158)` ⚪) et la veut **dynamique** (dérivée d'un état). Le gris est l'**état de base** (neutre / standby / off). La charte interdit explicitement « toute autre nuance de bleu / rouge / vert » et cite `rgb(25,118,210)` comme bleu prohibé.

Deux patterns coexistent dans [`18_lovelace/dashboards/navigation.yaml`](../../../../18_lovelace/dashboards/navigation.yaml) :

| Pattern | Couleur icône | Conforme Exception 3 |
|---|---|---|
| `bouton_navigation_dynamique` (via `sensor.etat_*_dashboard`) | gris au repos, colorée selon l'état réel | ✅ |
| `bouton_navigation` + `styles.icon.color` figé | couleur d'identité **permanente**, hors palette NAV | ❌ |

**Cas Arrosage déjà résorbé** (bascule en dynamique + `sensor.etat_arrosage_dashboard`) — voir C10. Le présent dossier porte le **reliquat** : les autres tuiles à couleur figée.

## 1. Inventaire des écarts (couleurs d'icône figées)

### Menu principal (☰ Navigation)

| Tuile | Couleur figée | Nature | Note |
|---|---|---|---|
| Rec. météo | `#F9A825` | lien dashboard | hors palette NAV — **piste de dynamisation cadrée, cf. §2 bis** |
| Volets | `#6D4C41` | domaine | pas de capteur d'état de synthèse |
| Prises | `#607D8B` | domaine | pas de capteur d'état de synthèse |
| Santé | `#E91E63` | domaine | pas de capteur d'état de synthèse |
| Imprimerie | `#1E468C` | lien dashboard | hors palette NAV |
| NAS | `#1976D2` | lien dashboard | **= `rgb(25,118,210)`, bleu explicitement interdit** |
| Énergie | `#FBC02D` | lien natif HA | hors palette NAV |

### Section ⚙️ Système (tous `bouton_navigation` figés)

Automations `#F9A825` · Scripts `#D84315` · Logs HA `#8E24AA` · Journal `#5D4037` · Historique `#1E88E5` · États `#3949AB` · Entités `#3F51B5` · Sauvegardes `#E53935` · Dashboards `#009688` · Intégrations `#1E88E5` · Templates `#6A1B9A` · YAML `#F4511E` · Reboot HA `#F57C00` *(call-service ; l'orange-rouge fait office d'affordance « action sensible »)*.

> **Périmètre à étendre si l'arbitrage est promu :** balayer aussi les tuiles de navigation hors `navigation.yaml` — `18_lovelace/includes/navigation/*` et les en-têtes de retour/hub des autres dashboards.

## 2. Options d'arbitrage (non tranchées)

| Option | Principe | Effet | Coût |
|---|---|---|---|
| **A — Neutraliser** | Retirer toutes les couleurs d'icône figées → icône neutre (thème) au repos ; la couleur ne sert qu'aux tuiles dynamiques. | Conforme à l'Exception 3 **telle qu'écrite**. | Perte de l'affordance d'identité visuelle des tuiles. |
| **B — Formaliser une exception « identité NAV »** | Ajouter à `03_exceptions.md` une exception couvrant une **couleur d'icône d'identité** (catégorielle, statique, non décisionnelle), comme l'Exception 4 le fait déjà pour le **fond**. | Conserve l'identité visuelle, charte cohérente. | Élargit la charte ; impose une palette d'identité documentée (les hex actuels sont ad hoc). |
| **C — Hybride** | Dynamiser les domaines à état latent exploitable (cf. arrosage) ; neutraliser / identité pour les purs liens outils (Système, Énergie, NAS, Imprimerie). | Maximise la valeur sémantique. | Le plus de travail ; à arbitrer domaine par domaine. |

## 2 bis. Sous-cas instrumenté — *Rec. météo : dynamisation par fraîcheur des records*

> **Statut :** **cadrage en lecture seule** — conception posée, **aucun runtime touché**, reste dormant jusqu'à promotion explicite. Instanciation concrète de l'**Option C** (dynamiser un lien dashboard à état latent exploitable), comme Arrosage l'a fait (C10).

**Pourquoi cette tuile est éligible.** Contrairement aux autres liens dashboard (Imprimerie, NAS, Énergie) qui n'exposent aucun état latent, la tuile **Rec. météo** pointe vers le dashboard des palmarès, et ces palmarès **datent leurs records** : chaque famille expose la date du record absolu en `rang_01_date` (format `%Y-%m-%d`, ancienneté trivialement dérivable). Quatre familles :

| Famille | Capteur synthèse | Sémantique |
|---|---|---|
| Chaud | `sensor.palmares_temperature_journalier_chaud` | chaleur 🔥 |
| Nuit tropicale (min haute) | `sensor.palmares_temperature_min_journaliere_haute` | chaleur 🔥 |
| Froid | `sensor.palmares_temperature_journalier_froid` | froid ❄️ |
| Pluie | `sensor.palmares_pluie_journalier` | pluie 🌧️ |

**Mécanisme proposé (un seul artefact runtime).** Un `sensor.etat_meteo_palmares_dashboard` (synthèse, calcul pur, lecture seule, nature `synthese` comme les `sensor.etat_*_dashboard` existants) lit les quatre `rang_01_date`, calcule l'ancienneté du record le plus récent, et renvoie un état mappé sur la palette NAV. La tuile bascule de `bouton_navigation` (+ `#F9A825` figé) vers `bouton_navigation_dynamique` — **aucun nouveau template** (le mapping état→couleur existe déjà) ; la couleur figée hors-charte disparaît.

**Fenêtre de fraîcheur retenue : J-2 glissant.** Coloré si un record est tombé **hier ou aujourd'hui** ; sinon gris (repos). Capte l'événement sans clignoter sur une seule journée. Seuil à exposer en paramètre (`input_number`) à l'implémentation plutôt qu'en dur.

**Mapping couleur (réutilise `bouton_navigation_dynamique`) :**

| État renvoyé | Couleur NAV | Condition |
|---|---|---|
| `off` | ⚪ gris (base) | aucun record frais (le plus récent hors fenêtre J-2) — repos, conforme Exception 3 |
| `alert` | 🔴 rouge | record de **chaleur** frais (chaud **ou** nuit tropicale) dans la fenêtre |
| `normal` | 🔵 bleu | record de **froid ou de pluie** frais dans la fenêtre |
| `confort` | 🟢 vert | **non utilisé** — pas de sémantique « favorable » pour un record (cohérent R4 arrosage : pas de vert confort) |

> Priorité si plusieurs familles fraîches le même jour : à trancher à l'implémentation (proposition : la chaleur 🔴 prime sur froid/pluie 🔵 — l'extrême chaud porte le signal le plus fort). Le gris reste l'**état par défaut** (capteur indisponible / palmarès vierge → ⚪, le gris prime, comme pour Arrosage).

**Ce que ça coûte / ce que ça rapporte.** Coût : un capteur de synthèse + bascule d'une ligne de tuile. Gain : résorbe un écart de l'inventaire (`#F9A825` hors palette) **et** ajoute une vraie valeur sémantique (la tuile signale « un record vient de tomber »). Reste **strictement** dans la palette des 4 couleurs opaques.

**Déclencheur de promotion (sortie du dormant) :** décision explicite d'implémenter, ou promotion de l'Option C au niveau du dossier. Tant qu'aucune décision : cadré mais **non ordonnancé**.

## 3. Déclencheur de réveil

Refonte de la charte couleurs, refonte du menu de navigation, ou décision explicite d'harmoniser l'UI NAV. En l'absence : dormant (aucun impact runtime, pur cosmétique / cohérence).

---

*Dossier d'arbitrage dormant — non normatif. Pose le constat et les options ; ne tranche rien.*
