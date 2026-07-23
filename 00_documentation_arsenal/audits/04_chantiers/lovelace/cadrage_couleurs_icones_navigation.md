# 🎨 Dossier d'arbitrage — Couleurs d'icônes des tuiles de navigation

> **Type :** dossier d'arbitrage Lovelace / UI (non décisionnel). **Document faisant foi** du sujet (pointé par `REGISTRE_CHANTIERS.md`).
> **ID registre :** `D-NAV-COULEUR`. **Statut : ✅ SOLDÉ (2026-07-19)** — menu ☰ Navigation : 5 tuiles dynamisées (Option C ; Arrosage, Rec. météo, Volets, NAS, Imprimerie — cf. §2 sexies) + 3 neutralisées au gris de base NAV (Option A ; Prises, Santé, Énergie — cf. §2 quinquies). **Section ⚙️ Système : reliquat résorbé — Option A (neutralisation) au gris de base NAV, combinée à une refonte du menu (12 → 6 tuiles), Reboot HA inclus — cf. §2 septies.** Plus aucune couleur d'icône figée hors palette dans `navigation.yaml`. **Chantier clos** (registre ⑤ Clos récents).
> **Post-solde (2026-07-23) — Arrosage, deux temps :** (1) la tuile suit le **besoin non couvert** plutôt que l'épisode d'action — §2 octies ; (2) après retour terrain, le **besoin couvert** (invisible en gris) reçoit un niveau propre 🟡 via la **formalisation du jaune NAV** dans l'Exception 3 (instancie l'Option B) — §2 nonies. Échelle finale : 🔴 besoin non couvert · 🟡 besoin pris en charge (à savoir) · ⚪ sol suffisant.
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
| ~~Prises~~ | ~~`#607D8B`~~ | domaine | **✅ résorbé** — neutralisé au gris de base NAV (pas de capteur de synthèse → Option A), cf. §2 quinquies |
| ~~Santé~~ | ~~`#E91E63`~~ | domaine | **✅ résorbé** — neutralisé au gris de base NAV (pas de capteur de synthèse → Option A), cf. §2 quinquies |
| ~~Imprimerie~~ | ~~`#1E468C`~~ | lien dashboard | **✅ résorbé** — bleu hors palette retiré, dynamisé sur la santé du NAS imprimerie (alert si défaut, gris au repos), cf. §2 sexies |
| ~~NAS~~ | ~~`#1976D2`~~ | lien dashboard | **✅ résorbé** — bleu interdit retiré, dynamisé sur l'état de sécurité (C-light), cf. §2 quater |
| ~~Énergie~~ | ~~`#FBC02D`~~ | lien natif HA | **✅ résorbé** — neutralisé au gris de base NAV (lien natif, aucun état latent → Option A), cf. §2 quinquies |

### Section ⚙️ Système (tous `bouton_navigation` figés) — ✅ RÉSORBÉ (2026-07-19, cf. §2 septies)

> **✅ Résorbé — Option A (neutralisation) + refonte du menu.** Les 13 tuiles ci-dessous ont été soit **supprimées**, soit **factorisées**, soit **neutralisées** au gris de base NAV. Inventaire historique conservé pour trace :

~~Automations `#F9A825` · Scripts `#D84315` · Logs HA `#8E24AA` · Journal `#5D4037` · Historique `#1E88E5` · États `#3949AB` · Entités `#3F51B5` · Sauvegardes `#E53935` · Dashboards `#009688` · Intégrations `#1E88E5` · Templates `#6A1B9A` · YAML `#F4511E` · Reboot HA `#F57C00`~~ *(l'orange-rouge de Reboot faisait office d'affordance « action sensible » — annotation renversée en §2 septies)* — **tous résorbés**.

> **Périmètre à étendre si l'arbitrage est promu :** balayer aussi les tuiles de navigation hors `navigation.yaml` — `18_lovelace/includes/navigation/*` et les en-têtes de retour/hub des autres dashboards. *(Reste ouvert — la présente résorption est bornée à `navigation.yaml`.)*

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

## 2 quinquies. Prises, Santé, Énergie — *neutralisation au gris de base NAV*

> **Statut :** **✅ implémenté (runtime)** — **Option A retenue** (neutraliser). Artefacts : bascule des trois tuiles dans `navigation.yaml` ; couleurs figées hors palette (`#607D8B`, `#E91E63`, `#FBC02D`) remplacées par le **gris de base NAV** `rgb(158, 158, 158)`.

**Pourquoi la neutralisation et non la dynamisation.** Ces trois tuiles n'exposent **aucun état latent exploitable** qui justifierait l'Option C : **Prises** et **Santé** sont des domaines **sans capteur d'état de synthèse** ; **Énergie** est un **lien natif HA** (`/energy`) sans état propre. Faute de signal notable à dériver, la couleur figée n'était qu'une **identité décorative hors palette NAV** — exactement le cas que l'Option A neutralise. Le gris au repos est **conforme à l'Exception 3** (gris = état de base / neutre).

**Choix du gris.** Plutôt que de retirer entièrement `styles.icon.color` (gris neutre du thème), on fixe explicitement `rgb(158, 158, 158)` — le **même gris que les tuiles dynamiques au repos** (état `off`/`standby` de `bouton_navigation_dynamique`) et l'une des **4 couleurs opaques** de la palette NAV. Cohérence visuelle directe avec le reste du menu, et la valeur reste **whitelistée par le contrôle CI** `ui_runtime_colors` (rgb opaque T2).

**Suite éventuelle.** Si l'un de ces domaines se dote plus tard d'un capteur de synthèse (p. ex. une santé batteries agrégée, une consommation anormale), la tuile pourra être **promue en Option C** (dynamisation) sans dette : la bascule gris→dynamique est triviale (le mapping état→couleur existe déjà). En l'état, neutralisation assumée.

## 2 sexies. Imprimerie — *bleu hors palette résorbé + dynamisation sur la santé du NAS imprimerie*

> **Statut :** **✅ implémenté (runtime)** — **Option C retenue**. Artefacts : `sensor.etat_imprimerie_dashboard` (`12_template_sensors/system/cartes_dashboard_navigation/imprimerie.yaml`), bascule de la tuile dans `navigation.yaml`, **`#1E468C` (bleu hors palette) retiré**.

**La non-conformité.** `#1E468C` = `rgb(30, 70, 140)`, **une nuance de bleu hors palette NAV** — prohibée par la charte (« toute autre nuance de bleu ») au même titre que l'ancien `#1976D2` du NAS, et **passant la CI** pour la même raison (le contrôle `ui_runtime_colors` ne bloque en HEX que les noirs). Non-conformité documentaire réelle, résorbée par la dynamisation.

**État latent disponible.** Contrairement aux trois tuiles neutralisées (§2 quinquies), Imprimerie **dispose d'un capteur de synthèse santé** : `sensor.nas_imprimerie_sante_synthese` (enum fermé `ok / degraded / critical / offline / unknown`, agrégeant connectivité / VPN / UPS / stockage du `nas_imprimerie`). Un état latent exploitable existe donc → Option C éligible (comme Arrosage, NAS).

**Articulation avec la doctrine couleur arrêtée.** La doctrine réserve le **bleu** (`normal`) à une **activité réelle observable** (par analogie au domaine Bruit) — *pas de bleu décoratif / de simple navigation / d'existence du domaine*. **Correction d'une rédaction antérieure erronée :** ce signal d'activité **existe bel et bien**. Il ne s'agit pas d'une imprimante de bureau mais d'une **usine** : `sensor.regime_acoustique_imprimerie` (`12_template_sensors/imprimerie/regime_acoustique_global.yaml`) synthétise le régime acoustique des presses **Komori / Bobst / Media** (états `bas` → `transition` → `haut_modere` → `haut_eleve` → `haut_extreme`, `indisponible`), et un régime **> `bas`** traduit une **production en cours**. Le 🔵 bleu est donc une cible **légitime et disponible** — l'ancienne mention « faute de signal d'impression » était fausse. **Mapping de la tuile (câblé sur `sensor.etat_imprimerie_dashboard`) :** 🔴 défaut santé NAS (priorité) · 🔵 usine en activité (`regime_acoustique_imprimerie` > `bas`) · ⚪ repos (NAS sain **et** usine au repos / indisponible).

**Mapping couleur (réutilise `bouton_navigation_dynamique`) :**

| État renvoyé | Couleur NAV | Condition (priorité décroissante) |
|---|---|---|
| `alert` | 🔴 rouge | `nas_imprimerie_sante_synthese` ∈ {`degraded`, `critical`, `offline`} — tout défaut santé actif du NAS imprimerie (**prime sur l'activité**) |
| `normal` | 🔵 bleu | NAS sain ET `regime_acoustique_imprimerie` > `bas` — **usine en activité** (production en cours) |
| `off` | ⚪ gris (base) | NAS sain/`unknown`/indisponible ET usine au repos (`bas`/`indisponible`) — repos, conforme Exception 3 |
| `confort` | 🟢 vert | **non utilisé** — pas de vert « confort » (R4) |

> **Honnêteté de repos.** Donnée incomplète → la synthèse source renvoie `unknown` (sa note v1.1 fait primer l'honnêteté sur le danger interprété) → tuile grise, comme NAS. **Couverture assumée** : tout défaut (y compris `degraded`) remonte en rouge — choix conservateur (le seul autre slot, le bleu, est doctrinalement réservé à l'activité). Collapsible vers « critical/offline seuls » si le rouge sur `degraded` s'avère trop bruyant.

**Ce que ça coûte / ce que ça rapporte.** Coût : un capteur de synthèse (dérivation pure de la synthèse santé existante) + bascule d'une ligne de tuile. Gain : résorbe la non-conformité bleu **et** ajoute une vraie valeur (un défaut du NAS imprimerie → tuile rouge). Reste strictement dans la palette NAV.

## 2 septies. Section ⚙️ Système — *neutralisation (Option A) + refonte du menu*

> **Statut :** **✅ implémenté (runtime, 2026-07-19)** — **Option A retenue** pour les tuiles survivantes, **combinée à une refonte structurelle du menu**. Artefacts : `18_lovelace/dashboards/navigation.yaml` (commits `d9a221b5` → `efd6ae49` → `7756e6d4`), **déployés et vérifiés en direct sur HA**. Solde le **reliquat** du dossier ; le menu principal ☰ Navigation était déjà harmonisé (§2 bis → sexies).

**Pourquoi Option A (et pas C).** La section ⚙️ Système est un **tiroir d'outils d'administration** — de purs lanceurs vers des pages système HA (`/config/*`, `/developer-tools/*`, `/logbook`, `/history`), **sans état latent exploitable**. Aucun signal notable à dériver ⇒ la dynamisation (C) n'a pas d'objet, exactement comme pour Prises / Santé / Énergie (§2 quinquies). De plus, **l'état système réel est déjà porté** par la tuile dynamique « Système » de la section ☰ Navigation (`sensor.etat_systeme_dashboard` → `/system-dashboard`) : la section ⚙️ Système n'a donc aucune vocation à porter de la couleur d'état. Toutes les tuiles survivantes passent au **gris de base NAV** `rgb(158, 158, 158)` (whitelisté CI `ui_runtime_colors`, T2).

**Refonte du menu (12 → 6 tuiles).** La résorption a été l'occasion de trancher aussi la **structure**, redondante et encombrée :

| Devenir | Tuiles | Cible / raison |
|---|---|---|
| **Supprimées** | Automations, Scripts | éditées depuis le repo `arsenal` (git), pas depuis l'UI ; accessibles par la barre latérale |
| **Supprimée** | Dashboards | non utilisée |
| **Factorisées → « Paramètres »** | Intégrations, Entités | toutes deux vivent sous `/config/dashboard` (Appareils & services / Entités) → une seule tuile `mdi:cog` → `/config/dashboard` |
| **Factorisées → « Outils Dev »** | États, Templates, YAML | trois onglets d'une même page `/developer-tools` → une seule tuile `mdi:tools` → `/developer-tools/state` |
| **Conservées (neutralisées)** | Logs HA, Journal, Historique, Sauvegardes | destinations distinctes réellement utilisées ; couleurs figées → gris |

Résultat : grille **3 × 2 pleine** (`columns: 3`), zéro trou, deux rangées thématiques (**administration** : Paramètres · Sauvegardes · Outils Dev — **observation** : Logs HA · Journal · Historique).

**Reboot HA — neutralisation assumée (renversement de doctrine).** L'inventaire §1 annotait l'orange `#F57C00` de Reboot HA comme *« affordance action sensible »*. **Arbitrage propriétaire inverse (2026-07-19)** : pour une **action destructive** (`homeassistant.restart`), une couleur chaude **invite au clic** — précisément l'effet à éviter. La tuile passe au **gris** : présente mais **discrète**, non incitative (le garde-fou reste la `confirmation:` déjà en place). La couleur cesse d'être une affordance d'action et redevient, ici aussi, réservée au **signal d'état**.

**Ce que ça coûte / ce que ça rapporte.** Coût : édition d'un seul fichier. Gain : plus **aucune** couleur d'icône figée hors palette dans `navigation.yaml` (menu **entièrement** conforme à l'Exception 3), section Système densifiée (12 → 6) et hiérarchisée. La grammaire visuelle est désormais stricte sur tout le menu : **gris = repos, couleur = signal d'état dérivé**.

## 2 octies. Arrosage — *recalibrage du seuil de parole (épisode → besoin non couvert)*

> **Statut :** **✅ implémenté (runtime, 2026-07-23)** — recalibrage d'une tuile **déjà dynamisée** (pas une nouvelle dynamisation). Artefact unique : `sensor.etat_arrosage_dashboard` (`12_template_sensors/system/cartes_dashboard_navigation/arrosage.yaml`). Aucune bascule dans `navigation.yaml`, aucun template touché, palette et enum inchangés → CI verte.

**Le constat.** La tuile Arrosage (premier cas dynamisé, C10) colorait sur l'**épisode d'action** : `alert` 🔴 si `categorie == 'arrose'` ou `intention == 'on'`, `normal` 🔵 si suspension pluie. Or `binary_sensor.arrosage_intention` n'est `on` que si **les 7 verrous** sont réunis *en même temps* (dont la fenêtre d'aube et le cooldown). Conséquence : **hors fenêtre, la tuile est grise alors même que le sol a soif** — exactement l'information que l'utilisateur ouvre le dashboard pour lire. La couleur marquait l'action, pas le besoin.

**Le principe qui tranche — « seuil de parole ».** Le système Arsenal est **silencieux par philosophie** : sur 268 automations, la notification persistante n'est levée que ~29 fois, réservée aux moments où **un humain est requis** (panne, alarme, échec d'exécution, non-conformité) ; l'arrosage n'en lève **aucune**. En colorant les tuiles, le menu de navigation devient un *tableau de bord* — légitime **à condition** que la couleur soit aussi parcimonieuse que cette couche notification. La couleur ne doit donc rompre le gris qu'au **même niveau qu'une notification persistante** : quand la situation devient **l'affaire de l'utilisateur**.

Appliqué à l'arrosage : un sol sec en attente de l'arrosage d'aube n'est **pas** l'affaire de l'utilisateur — la V1 autonome s'en charge, en silence → **gris**. Le rouge n'est justifié que si le besoin **ne sera pas couvert** par la chaîne autonome.

**Mapping recalibré (`sensor.etat_arrosage_dashboard`) :**

| État renvoyé | Couleur NAV | Condition |
|---|---|---|
| `alert` | 🔴 rouge | `arrosage_besoin_sol` actif **ET** non pris en charge (pas de session, pas de pluie) **ET** chaîne autonome hors d'état d'agir : maître coupé, ou pont / préconditions / canal sol indisponible |
| `off` | ⚪ gris (base) | le système assure : sol suffisant · sec mais pris en charge (arrosage en cours / pluie / attente de la fenêtre) · repos |
| `unknown` | ⚪ gris indispo | besoin/pont illisible (garde-fou ; `pont_donnees_disponibles` est un booléen pur → un pont HS renvoie `off`, donc *besoin non couvert* → 🔴, pas gris) |
| `normal` / `confort` | 🔵 / 🟢 | **non utilisés** — pas d'info bleue ni de vert nominal (doctrine « majoritairement gris, couleur = attention ») |

> **Note doctrinale (deux rôles de couleur, hors périmètre arrosage).** Le clivage n'est pas *quelle couleur* mais *le seuil de parole*. Deux rôles de couleur restent légitimes dans le cockpit : (1) **attention** — 🔴 rare, « à toi » ; (2) **réassurance saisonnière** — 🟢/🔵 « le domaine de saison tourne bien » (chauffage l'hiver, clim l'été), bornée par la saison donc compatible avec « majoritairement gris ». Le seul cas illégitime est le nominal coloré d'un domaine **hors de sa saison de garde et sans réassurance à donner**. Chauffage (🟢 sur programme Confort) et Clim (🟢/🔵 sur mode) relèvent du rôle (2) — **non traités ici**, laissés en l'état.

**Ce que ça coûte / ce que ça rapporte.** Coût : réécriture d'un seul capteur de synthèse. Gain : la tuile signale enfin le **besoin qui vous concerne** (et son silence dit « sous contrôle »), et cesse de crier sur une action nominale. Reste strictement dans la palette NAV (🔴/⚪).

> **⏭️ Suite immédiate — cf. §2 nonies :** le §2 octies laissait le besoin *couvert* en gris (donc invisible). Retour terrain de l'utilisateur : « il y a un besoin, et c'est gris — je ne comprends pas ; je veux le savoir ». Le besoin couvert reçoit désormais un niveau propre 🟡 (formalisation du jaune NAV). La ligne `off` du tableau ci-dessus ne couvre donc plus le cas « besoin pris en charge ».

## 2 nonies. Arrosage — *formalisation du jaune NAV (besoin couvert = vigilance)*

> **Statut :** **✅ implémenté (runtime, 2026-07-23)** — instancie l'**Option B** (formaliser une exception), restée ouverte depuis §2 (col. « B »). Étend l'**Exception 3** : le jaune opaque `rgb(255, 235, 59)` entre dans la palette d'icône NAV/HUB. Artefacts : `ui/couleurs/03_exceptions.md` (Exception 3), `scripts/arsenal_contracts/check_ui_runtime_colors_contracts.py` (whitelist `ALLOWED_RGB`), `bouton_navigation_dynamique.yaml` (clé `vigilance`), `sensor.etat_arrosage_dashboard`.

**Le retour terrain.** Après §2 octies, un besoin *couvert par l'autonome* (le cas fréquent : sol sec, la V1 arrosera à l'aube) restait **gris** — donc **invisible**. Or l'utilisateur ouvre le dashboard précisément pour *voir* ce besoin (« demain le système va arroser, je veux le savoir »). Le §2 octies confondait deux réalités sous le gris : *rien à signaler* et *besoin détecté, pris en charge*.

**Le manque de la charte.** L'Exception 3 n'autorisait que 🔴/🟢/🔵/⚪. Aucune de ces teintes ne dit « signal présent, pris en charge, **à savoir** sans alarmer » : le 🔵 est « info/technique » (trop neutre, et réservé ailleurs à une activité observable), le 🔴 est l'alarme (trop fort). Il manquait le cran **vigilance** — précisément le sens canon du **jaune** Arsenal (`02_palette.md` : « Vigilance / attention, niveau inférieur à l'orange, non bloquant »). Décision propriétaire : **formaliser le jaune dans l'Exception 3** (Option B) plutôt que détourner le bleu.

**Ce que le jaune NAV est / n'est pas.** Version opaque `rgb(255, 235, 59)` du jaune canon `rgba(255, 235, 59, 0.2)`, exactement comme rouge/vert/bleu NAV sont les opaques de leur teinte. Sens **unique et opposable** : « un signal existe, il est pris en charge — à savoir ». Non décisionnel, non bloquant, **strictement sous le rouge** (R3 : le jaune ne masque jamais un rouge). L'orange reste hors palette NAV.

**Mapping final (`sensor.etat_arrosage_dashboard`) — échelle de sévérité :**

| État renvoyé | Couleur NAV | Condition |
|---|---|---|
| `alert` | 🔴 rouge | besoin actif **ET non couvert** : maître coupé, ou pont / préconditions / canal sol indisponible, et pas d'arrosage en cours ni de pluie → **à l'utilisateur d'agir** |
| `vigilance` | 🟡 jaune | besoin actif **ET couvert** : la chaîne autonome arrosera (aube), ou arrosage en cours, ou pluie qui couvre → **à savoir** |
| `off` | ⚪ gris (base) | sol suffisant, repos |
| `unknown` | ⚪ gris indispo | besoin/pont illisible (garde-fou) |

> **Portée de l'Exception 3 étendue.** Le jaune NAV est désormais **disponible pour toute tuile** dont un état latent relève de la vigilance « pris en charge » — pas seulement l'arrosage. Aucune tuile existante n'est migrée d'office ; l'usage reste **cas par cas**, comme le reste du dossier. La hiérarchie globale (`05_regles.md`) est inchangée : 🔴 > 🟠 > 🟡 > 🟢 > 🔵 > ⚪.

**Ce que ça coûte / ce que ça rapporte.** Coût : une entrée de charte + une entrée de whitelist CI + une clé de template + un capteur. Gain : le besoin d'arrosage est **enfin visible** (🟡) sans être traité en alarme, le 🔴 reste réservé au besoin que le système ne couvrira pas, et le gris redevient l'honnête « rien à signaler ». La grammaire du cockpit gagne un cran manquant (vigilance), utile bien au-delà de l'arrosage.

## 3. Déclencheur de réveil

**Chantier soldé (2026-07-19).** Le déclencheur « refonte du menu de navigation » a été **consommé** : la section ⚙️ Système a été refondue et neutralisée (§2 septies), dernier reliquat du dossier. Il ne reste **aucune** couleur d'icône figée hors palette dans `navigation.yaml`.

Réveil résiduel possible : refonte de la charte couleurs, ou extension du périmètre **hors `navigation.yaml`** (tuiles `18_lovelace/includes/navigation/*` et en-têtes de retour/hub des autres dashboards — cf. §1), non traité ici. En l'absence : clos. *(Non-conformités « bleu hors palette » NAS `#1976D2` / Imprimerie `#1E468C` résorbées — §2 quater / §2 sexies.)*

---

*Dossier d'arbitrage — non normatif. **Soldé (2026-07-19).** Menu ☰ Navigation : 5 tuiles dynamisées (Option C) + 3 neutralisées au gris de base NAV (Option A). Section ⚙️ Système : reliquat résorbé — Option A + refonte du menu (12 → 6 tuiles, Reboot HA inclus), §2 septies. Plus aucune couleur d'icône figée hors palette dans `navigation.yaml`.*
