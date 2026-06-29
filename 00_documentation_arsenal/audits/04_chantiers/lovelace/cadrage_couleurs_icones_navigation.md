# 🎨 Dossier d'arbitrage — Couleurs d'icônes des tuiles de navigation

> **Type :** dossier d'arbitrage Lovelace / UI (non décisionnel). **Document faisant foi** du sujet (pointé par `REGISTRE_CHANTIERS.md`).
> **ID registre :** `D-NAV-COULEUR`. **Statut :** **Option C (hybride) en exécution incrémentale** — 4 tuiles résorbées (Arrosage, Rec. météo, Volets, NAS) ; **reliquat dormant** (Prises, Santé, Imprimerie, Énergie + section Système). L'arbitrage global A/B/C reste ouvert pour le reliquat.
> **Règle qui fait foi :** [`ui/couleurs/03_exceptions.md`](../../../ui/couleurs/03_exceptions.md) § *Exception 3 — Couleurs dynamiques d'icône en contexte NAV/HUB*.
> **Discipline :** aucune modification UI d'une tuile tant que son cas n'est pas tranché (cas par cas) ; co-commit du registre à chaque changement d'état.

---

## 0. Constat

L'Exception 3 réserve l'icône des tuiles de navigation à **4 couleurs opaques** (`rgb(244,67,54)` 🔴, `rgb(76,175,80)` 🟢, `rgb(33,150,243)` 🔵, `rgb(158,158,158)` ⚪) et la veut **dynamique** (dérivée d'un état). Le gris est l'**état de base** (neutre / standby / off). La charte interdit explicitement « toute autre nuance de bleu / rouge / vert » et cite `rgb(25,118,210)` comme bleu prohibé.

Deux patterns coexistent dans [`18_lovelace/dashboards/navigation.yaml`](../../../../18_lovelace/dashboards/navigation.yaml) :

| Pattern | Couleur icône | Conforme Exception 3 |
|---|---|---|
| `bouton_navigation_dynamique` (via `sensor.etat_*_dashboard`) | gris au repos, colorée selon l'état réel | ✅ |
| `bouton_navigation` + `styles.icon.color` figé | couleur d'identité **permanente**, hors palette NAV | ❌ |

**Cas déjà résorbés** (bascule en dynamique) : **Arrosage** (`sensor.etat_arrosage_dashboard`, voir C10), **Rec. météo** (`sensor.etat_meteo_palmares_dashboard`, cf. §2 bis), **Volets** (`sensor.etat_volets_dashboard`, cf. §2 ter) et **NAS** (`sensor.etat_nas_dashboard`, cf. §2 quater). Le présent dossier porte le **reliquat** : les autres tuiles à couleur figée.

## 1. Inventaire des écarts (couleurs d'icône figées)

### Menu principal (☰ Navigation)

| Tuile | Couleur figée | Nature | Note |
|---|---|---|---|
| ~~Rec. météo~~ | ~~`#F9A825`~~ | lien dashboard | **✅ résorbé** — dynamisé par fraîcheur des records, cf. §2 bis |
| ~~Volets~~ | ~~`#6D4C41`~~ | domaine | **✅ résorbé** — dynamisé sur signal pluie (Option C), cf. §2 ter |
| Prises | `#607D8B` | domaine | pas de capteur d'état de synthèse |
| Santé | `#E91E63` | domaine | pas de capteur d'état de synthèse |
| Imprimerie | `#1E468C` | lien dashboard | hors palette NAV |
| ~~NAS~~ | ~~`#1976D2`~~ | lien dashboard | **✅ résorbé** — bleu interdit retiré, dynamisé sur l'état de sécurité (C-light), cf. §2 quater |
| Énergie | `#FBC02D` | lien natif HA | hors palette NAV |

### Section ⚙️ Système (tous `bouton_navigation` figés)

Automations `#F9A825` · Scripts `#D84315` · Logs HA `#8E24AA` · Journal `#5D4037` · Historique `#1E88E5` · États `#3949AB` · Entités `#3F51B5` · Sauvegardes `#E53935` · Dashboards `#009688` · Intégrations `#1E88E5` · Templates `#6A1B9A` · YAML `#F4511E` · Reboot HA `#F57C00` *(call-service ; l'orange-rouge fait office d'affordance « action sensible »)*.

> **Périmètre à étendre si l'arbitrage est promu :** balayer aussi les tuiles de navigation hors `navigation.yaml` — `18_lovelace/includes/navigation/*` et les en-têtes de retour/hub des autres dashboards.

## 2. Options d'arbitrage

> **Direction de fait : Option C (hybride), appliquée cas par cas.** Quatre tuiles ont été résorbées par dynamisation (Arrosage, Rec. météo, Volets, NAS — détail §2 bis/ter/quater). L'arbitrage **global** A/B/C reste néanmoins **ouvert pour le reliquat** (tuiles restantes + section Système) : chaque tuile est tranchée individuellement avant action.

| Option | Principe | Effet | Coût |
|---|---|---|---|
| **A — Neutraliser** | Retirer toutes les couleurs d'icône figées → icône neutre (thème) au repos ; la couleur ne sert qu'aux tuiles dynamiques. | Conforme à l'Exception 3 **telle qu'écrite**. | Perte de l'affordance d'identité visuelle des tuiles. |
| **B — Formaliser une exception « identité NAV »** | Ajouter à `03_exceptions.md` une exception couvrant une **couleur d'icône d'identité** (catégorielle, statique, non décisionnelle), comme l'Exception 4 le fait déjà pour le **fond**. | Conserve l'identité visuelle, charte cohérente. | Élargit la charte ; impose une palette d'identité documentée (les hex actuels sont ad hoc). |
| **C — Hybride** | Dynamiser les tuiles à état latent exploitable (cf. arrosage, NAS) ; neutraliser / identité pour les purs liens outils sans état latent. | Maximise la valeur sémantique. | Le plus de travail ; à arbitrer tuile par tuile. |

## 2 bis. Sous-cas instrumenté — *Rec. météo : dynamisation par fraîcheur des records*

> **Statut :** **✅ implémenté (runtime)** — instanciation concrète de l'**Option C** (dynamiser un lien dashboard à état latent exploitable), comme Arrosage l'a fait (C10). Artefacts : `sensor.etat_meteo_palmares_dashboard` (`12_template_sensors/system/cartes_dashboard_navigation/meteo_palmares.yaml`), paramètre `input_number.palmares_meteo_fraicheur_jours` (`03_input_numbers/meteo/`), bascule de la tuile dans `navigation.yaml`. Le **reste** du dossier (autres tuiles figées) demeure dormant.

**Pourquoi cette tuile est éligible.** Contrairement aux autres liens dashboard (Imprimerie, NAS, Énergie) qui n'exposent aucun état latent, la tuile **Rec. météo** pointe vers le dashboard des palmarès, et ces palmarès **datent leurs records** : chaque famille expose la date du record absolu en `rang_01_date` (format `%Y-%m-%d`, ancienneté trivialement dérivable). Quatre familles :

| Famille | Capteur synthèse | Sémantique |
|---|---|---|
| Chaud | `sensor.palmares_temperature_journalier_chaud` | chaleur 🔥 |
| Nuit tropicale (min haute) | `sensor.palmares_temperature_min_journaliere_haute` | chaleur 🔥 |
| Froid | `sensor.palmares_temperature_journalier_froid` | froid ❄️ |
| Pluie | `sensor.palmares_pluie_journalier` | pluie 🌧️ |

**Mécanisme réalisé (un seul artefact de calcul).** `sensor.etat_meteo_palmares_dashboard` (synthèse, calcul pur, lecture seule, comme les `sensor.etat_*_dashboard` existants) lit **tous les rangs** (`input_text.palmares_*_rang_01..10_date`) des quatre familles, calcule l'ancienneté de chaque entrée, et renvoie un état mappé sur la palette NAV. La tuile est passée de `bouton_navigation` (+ `#F9A825` figé) à `bouton_navigation_dynamique` — **aucun nouveau template** (le mapping état→couleur existe déjà) ; la couleur figée hors-charte a disparu.

**Fenêtre de fraîcheur : J-2 glissant, paramétrée et PARTAGÉE.** Un record est « frais » si l'ancienneté en jours calendaires d'**au moins un rang** vérifie `0 ≤ âge < seuil`, avec `seuil = input_number.palmares_meteo_fraicheur_jours` (défaut **2** = aujourd'hui + la veille). **Définition unique** : la tuile NAV **et** le badge « 🔥 récent » des cartes palmarès (`18_lovelace/includes/cartes/meteo/palmares/*`) partagent ce même critère (tous rangs + ce même seuil) — corrige une incohérence antérieure (tuile rang 1 seul / J-2 vs cartes rang 1 seul / 7 j figé). Capte l'entrée d'un record à n'importe quel rang ; seuil ajustable sans toucher au code.

**Mapping couleur (réutilise `bouton_navigation_dynamique`) :**

| État renvoyé | Couleur NAV | Condition |
|---|---|---|
| `off` | ⚪ gris (base) | aucun record frais (le plus récent hors fenêtre J-2) — repos, conforme Exception 3 |
| `alert` | 🔴 rouge | record de **chaleur** frais (chaud **ou** nuit tropicale) dans la fenêtre |
| `normal` | 🔵 bleu | record de **froid ou de pluie** frais dans la fenêtre |
| `confort` | 🟢 vert | **non utilisé** — pas de sémantique « favorable » pour un record (cohérent R4 arrosage : pas de vert confort) |

> Priorité tranchée : si plusieurs familles sont fraîches en même temps, la **chaleur 🔴 prime** sur froid/pluie 🔵 (l'extrême chaud porte le signal le plus fort). Le gris reste l'**état par défaut** (palmarès vierge / date absente → contribue 0 → ⚪, comme pour Arrosage).

**Ce que ça coûte / ce que ça rapporte.** Coût : un capteur de synthèse + bascule d'une ligne de tuile. Gain : résorbe un écart de l'inventaire (`#F9A825` hors palette) **et** ajoute une vraie valeur sémantique (la tuile signale « un record vient de tomber »). Reste **strictement** dans la palette des 4 couleurs opaques.

**Suite éventuelle.** Le sous-cas est clos côté Rec. météo. Pistes ouvertes non ordonnancées : exposer le **type** de record frais (icône `mdi:thermometer`/`mdi:weather-pouring`) plutôt que la seule couleur ; étendre la même approche aux autres liens dashboard à état latent. La promotion du **reste** de l'Option C (autres tuiles) reste sur décision explicite.

## 2 ter. Volets — *dynamisation sur signal pluie*

> **Statut :** **✅ implémenté (runtime)** — **Option C retenue** (arbitrage tranché : dynamiser sur le signal pluie). Artefacts : `sensor.etat_volets_dashboard` (`12_template_sensors/system/cartes_dashboard_navigation/volets.yaml`), bascule de la tuile dans `navigation.yaml`, `#6D4C41` retiré. L'analyse ci-dessous (verrou sémantique, options) est conservée car elle **motive** le choix.

**Le domaine.** 4 volets `cover` à position (Zigbee : `cover.sejour_gauche`, `cover.sejour_droit`, `cover.chambre_arnaud`, `cover.chambre_matthieu`), pilotés en `set_cover_position` / `close_cover`. États HA : `open` / `closed` / `opening` / `closing` + `current_position`. **Aucun capteur d'état de synthèse** aujourd'hui. Logique métier existante : **fermeture automatique sur pluie forte** (`binary_sensor.intention_pluie_forte`, `binary_sensor.autorisation_fermeture_volets_pluie_sejour`, automations `11_automations/meteo/pluie/pluie_volets_*`).

**Le verrou sémantique.** Les autres tuiles domaine se colorent sur un état **notable** binaire (`etat_eclairage_dashboard` : une lampe ON → alert ; `etat_ouvertures_dashboard` : un ouvrant ouvert → alert ; `etat_mouvements_dashboard` : mouvement → alert). **Ce patron ne se transpose pas aux volets** : un volet **ouvert comme fermé est nominal** (ouvert le jour, fermé la nuit). « Un volet ouvert → alert » colorerait la tuile en permanence, sans valeur, à rebours de l'esprit Exception 3 (gris au repos). **La position n'est donc pas un signal exploitable.**

**Le seul signal réellement notable** est **événementiel** : la **fermeture automatique sur pluie en cours** (le domaine intervient seul), strictement analogue à l'« arrose → alert » de l'arrosage. Rare par nature → tuile grise la quasi-totalité du temps, ce qui est **conforme** (gris = repos). Signal secondaire possible : **un volet `unavailable`** (nœud Zigbee tombé) → anomalie, baseline propre (« repos = tous joignables »).

**Options pour cette tuile :**

| Option | Principe | Pour | Contre |
|---|---|---|---|
| **A — Neutraliser** | Retirer `#6D4C41` → icône neutre (thème). | Simple, conforme Exception 3, honnête (pas de signal forcé). | Perd la couleur d'identité ; n'ajoute aucune valeur. |
| **C — Dynamiser (signal pluie)** | `sensor.etat_volets_dashboard` = `normal` 🔵 si fermeture pluie en cours, sinon `off` ⚪. Réutilise les `binary_sensor` pluie existants ; petit capteur de synthèse, pas d'agrégat de position. | Cohérent avec le patron domaine ; signale une action automatique ; gris au repos. | Signal **rare** ; valeur marginale ; le bleu « info » plutôt que rouge (pas une alerte de sécurité). |
| **C′ — Dynamiser (anomalie dispo)** | `alert` 🔴 si un volet `unavailable`. | Vraie valeur diagnostique ; baseline nette. | Aucune autre tuile domaine ne surface la dispo → précédent isolé ; doublonne l'observabilité Zigbee. |

**Décision (tranchée par l'utilisateur) : Option C — dynamiser sur le signal pluie.** Tuile vivante conservée, conforme au patron domaine. Réalisation : `sensor.etat_volets_dashboard` renvoie `normal` (🔵) si `binary_sensor.intention_pluie_forte` **et** `binary_sensor.autorisation_fermeture_volets_pluie_sejour` sont `on` (pluie forte **et** dispositif armé selon mode/présence), sinon `off` (⚪) ; donnée indisponible → `off`. Bleu « info » assumé (action automatique, pas alerte de sécurité). **La position reste écartée** (aucun état de position n'est anormal). C′ (anomalie de disponibilité) non retenue (précédent isolé, doublon observabilité Zigbee) — piste ouverte si besoin diagnostic ultérieur.

## 2 quater. NAS — *non-conformité bleu résorbée + dynamisation sécurité*

> **Statut :** **✅ implémenté (runtime, variante C-light)** — **arbitrage tranché**. Artefacts : `sensor.etat_nas_dashboard` (`12_template_sensors/system/cartes_dashboard_navigation/nas.yaml`), bascule de la tuile dans `navigation.yaml`, **`#1976D2` (bleu interdit) retiré**. La couleur dérive de l'état de sécurité du Synology principal ; l'analyse ci-dessous (non-conformité, options) est conservée car elle **motive** le choix.

**La non-conformité.** `#1976D2` = `rgb(25,118,210)`, **bleu explicitement interdit par la charte** (`ui/couleurs/02_palette.md` / `03_exceptions.md`). Nuance CI : le contrôle `ui_runtime_colors` ne whiteliste que les `rgb(...)` **opaques** (T2) et ne bloque en HEX (T3) que les noirs `#000/#222/#333` — un HEX `#1976D2` **passe donc la CI** aujourd'hui tout en violant la charte écrite. C'est une non-conformité **documentaire réelle**, à résorber quel que soit l'arbitrage couleur dynamique.

**Cible de la tuile.** `/nas-dashboard` → `18_lovelace/dashboards/systeme/nas.yaml`, qui porte sur **`nas_valentin`** (le Synology principal). À ne pas confondre avec `nas_imprimerie` (serveur d'impression), qui est la tuile **Imprimerie** et dispose, lui, d'une synthèse santé (`sensor.nas_imprimerie_sante_synthese`).

**État latent disponible (`nas_valentin`).** `binary_sensor.nas_valentin_etat_de_securite` (Security Advisor Synology), `sensor.nas_valentin_volume_1_etat`, `sensor.nas_valentin_drive_{1,2}_etat` + `…_etat_intelligent` (SMART), `binary_sensor.nas_valentin_drive_2_depassement_du_nombre_maximal_de_secteurs_defectueux`, `…_en_dessous_de_la_duree_de_vie_restante_minimale`, températures/charge. **Mais : aucun capteur de synthèse** pour `nas_valentin` (contrairement à `nas_imprimerie`), et **les valeurs de ces états ne sont interprétées nulle part** dans le repo (chaînes fournies par l'intégration Synology, locale-dépendantes) ⇒ **domaine de valeurs à confirmer en runtime** avant toute synthèse.

**Options pour cette tuile :**

| Option | Principe | Pour | Contre |
|---|---|---|---|
| **A — Neutraliser** | Retirer `#1976D2` → icône neutre (thème). | **Résout immédiatement la violation de charte**, zéro runtime. | Perd l'opportunité diagnostique pourtant réelle. |
| **C — Dynamiser (synthèse santé)** | Nouveau `sensor.etat_nas_dashboard` agrégeant sécurité / volume / disques / SMART / secteurs / durée de vie → `alert` 🔴 si problème, (option `normal` 🔵 si dégradé), `off` ⚪ si sain, gris si indispo. Modèle : `nas_imprimerie_sante_synthese`. | Vraie valeur (un disque qui lâche / alerte sécurité du NAS principal → tuile rouge) ; résout aussi la charte. | Capteur de synthèse à écrire ; **domaine de valeurs Synology à vérifier d'abord** ; le plus de travail. |
| **C-light — Signal unique** | Dynamiser sur `binary_sensor.nas_valentin_etat_de_securite` seul → `alert` 🔴 si non sûr, sinon `off` ⚪. | Faible coût, valeur immédiate, résout la charte. | Couverture partielle (ignore disques/volume/SMART). |

**Décision (tranchée par l'utilisateur) : Option C-light — dynamiser sur l'état de sécurité.** Premier pas à faible risque qui résout la non-conformité de charte et apporte une valeur immédiate. Réalisation : `sensor.etat_nas_dashboard` renvoie `alert` (🔴) si `binary_sensor.nas_valentin_etat_de_securite` est `on` (défaut / alerte / intrusion), sinon `off` (⚪, y compris indisponible). **Polarité confirmée par la source faisant foi** : le template `carte_etat_securite` (`19_button_card_templates/40_dashboards/nas/`) mappe déjà `off → 🟢 sécurisé`, `on → 🔴 défaut` — pas besoin de vérification runtime supplémentaire. **Couverture partielle assumée** (disques / volume / SMART non agrégés) — extensible vers la synthèse santé complète (**C**) si besoin ultérieur. `#1976D2` retiré.

## 3. Déclencheur de réveil

Refonte de la charte couleurs, refonte du menu de navigation, ou décision explicite d'harmoniser l'UI NAV. En l'absence : dormant (aucun impact runtime, pur cosmétique / cohérence). *(La non-conformité de charte NAS `#1976D2`, qui constituait un déclencheur actif, est désormais résorbée — cf. §2 quater.)*

---

*Dossier d'arbitrage — non normatif. Option C (hybride) tranchée et exécutée cas par cas (4 tuiles résorbées) ; reliquat dormant, arbitrage global ouvert.*
