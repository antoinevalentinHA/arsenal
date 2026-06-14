# CHANTIER OBSERVATIONNEL — EFFICACITÉ DE LA CLIM PAR CHAMBRE (Phase 0)
## Cadrage d'une observation pure : effectivité de couplage, sans toucher au système

> **Statut :** cadrage de chantier **observationnel**, Phase 0 — *préparation*.
> **Nature :** document de méthode (objectif, définitions, métriques, limites).
> **Non normatif** — n'est ni un contrat, ni une décision, ni une spécification.
> **Aucun réglage proposé. Aucune évolution de la décision COOL.**
> **Domaine :** `climatisation`
> **Périmètre Phase 0 — strictement nul côté système :** zéro runtime, zéro
> capteur, zéro `statistics`, zéro `recorder`, zéro UI Lovelace, zéro contrat,
> zéro changelog. Phase 0 **n'observe que ce qui est déjà historisé**.
> **Rattachement :** prolonge empiriquement la contre-analyse topologique
> [`audit_strategie_max_on_min_off_cool.md`](audit_strategie_max_on_min_off_cool.md)
> (Phase 6 — robustesse mono-zone, régimes couplé/découplé) et l'investigation
> dynamique [`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md).
> Hub : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md).

---

## 0. Objectif observationnel

Comprendre, **à partir des seules données déjà enregistrées**, dans quelle mesure
le climatiseur unique de palier refroidit **réellement chaque chambre**
(Arnaud, Matthieu, Parents), et **comment cette efficacité varie** avec
l'extérieur et l'état (inféré) d'ouverture des portes.

Ce chantier **ne cherche pas à améliorer** la clim. Il cherche à **rendre visible
et mesurable** le phénomène de couplage/découplage déjà identifié théoriquement,
afin que toute évolution future (hors périmètre) repose sur des faits mesurés et
non sur des hypothèses.

**Ce que Phase 0 produit :** une lecture conditionnée de l'historique + des
métriques candidates **figées**. **Ce que Phase 0 ne produit pas :** aucune
entité, aucune carte, aucune modification.

---

## 1. Définition de l'« efficacité » retenue — **effectivité de couplage, pas COP**

Avec **un seul appareil** (sur le palier) desservant plusieurs chambres
(`11_perimetre_exclu.md` : pilotage multi-zones hors périmètre), le mot
« efficacité » est **volontairement restreint** :

> **Efficacité par chambre = réponse thermique de la chambre par unité de temps
> de climatisation active (COOL ON), conditionnée aux conditions extérieures.**

C'est une mesure d'**effectivité de couplage** entre le volume climatisé (palier)
et chaque chambre — c'est-à-dire **à quel point l'air froid atteint la pièce**.

**Ce n'est PAS :**
- un **COP / rendement énergétique** de l'appareil (on ne mesure ni puissance
  frigorifique réelle, ni énergie absorbée fiable par pièce) ;
- une **performance intrinsèque** du climatiseur (un seul appareil ; le
  différentiel entre chambres reflète la **distribution d'air et les portes**,
  pas la machine) ;
- un indicateur de **confort** (le confort est traité ailleurs : protocole
  d'observation des seuils).

Cette restriction est **structurelle** : aucune donnée du dépôt ne permet un COP
par pièce. La nommer évite toute sur-interprétation.

---

## 2. Signaux **déjà historisés** mobilisables (Phase 0 — aucun ajout)

Tous présents dans `recorder.yaml` à ce jour ; Phase 0 **n'en ajoute aucun**.

| Famille | Entités (par chambre sauf mention) |
|---|---|
| Température chambre | `sensor.temperature_chambre_arnaud` · `_matthieu` · `_parents` |
| Agrégats chambres | `sensor.temperature_max_chambres` · `sensor.temperature_min_chambres` |
| Humidité / humidex | `sensor.humidite_relative_chambre_*` · `humidite_absolue_chambre_*` · `humidex_chambre_*` |
| **CO₂** (proxy découplage) | `sensor.co2_chambre_arnaud` · `_matthieu` · `_parents` |
| Bruit | `sensor.bruit_chambre_arnaud` · `_matthieu` |
| Clim — exécution commandée | `switch.clim_power` · `sensor.clim_mode_local` · `sensor.clim_target_mode` |
| Clim — explicabilité | `sensor.clim_raison_decision` · autorisations `binary_sensor.autorisation_clim_*` |
| Clim — écart consigne | `sensor.ecart_consigne_instantane` (+ `_froid`, `_doux`) |
| Clim — énergie | `sensor.clim_consommation_estimee_energie` · `_aujourd_hui` |
| Contexte | `sensor.temperature_jardin` · `binary_sensor.presence_famille_unifiee` |

---

## 3. Limites méthodologiques (à acter **avant** toute lecture)

### 3.1 La porte est une **variable cachée** (pas de capteur)
Aucun capteur d'ouverture de porte n'existe ni n'est utilisé. Or l'état de la
porte **gouverne** le couplage thermique chambre ↔ palier. **Conséquence :**
l'efficacité mesurée **mélange** l'effet de l'appareil et l'effet de la porte. On
ne peut pas l'isoler directement ; on doit **stratifier** par couplage *inféré*
(voir §3.3), jamais supposer la porte ouverte.

### 3.2 L'extérieur est le **facteur de confusion** dominant
La charge thermique (ensoleillement, température jardin) pilote largement la
température des chambres. **Toute** métrique d'efficacité doit être **conditionnée
à l'extérieur** (`sensor.temperature_jardin`, idéalement segmenté par période
jour/soir/nuit). Une comparaison brute entre chambres ou entre jours, sans
conditionnement, **mesure surtout la météo** et serait fausse.

### 3.3 Le **CO₂ comme proxy possible de découplage**
Une chambre fermée **et occupée** voit son CO₂ s'accumuler ; une chambre ouverte
se rééquilibre avec le volume commun. Croisé avec la **non-réponse thermique**
(la chambre ne suit pas le refroidissement du palier), une **montée de CO₂** est
un **indice** de porte fermée / découplage. **Proxy imparfait :** une chambre
fermée **inoccupée** ne produit pas de CO₂ — le signal est alors muet. À utiliser
comme **indice corroborant**, jamais comme vérité de porte.

### 3.4 Commandé ≠ réel
`clim_mode_local` / `clim_power` indiquent le mode **commandé**, pas l'**action
réelle** de l'appareil (`hvac_action` du `climate.clim` **non historisée**).
L'efficacité Phase 0 est donc **bout-en-bout** (réponse de la pièce au COOL
*commandé*), pas une mesure du compresseur. Gap d'observabilité **acté**, non
comblé en Phase 0.

### 3.5 Bruit de mesure des capteurs de chambre
Les températures de chambre sont consolidées (HomeKit + repli Zigbee) ;
latence et granularité varient. Les pentes courtes sont bruitées : privilégier
des fenêtres suffisamment longues et des médianes.

---

## 4. Métriques candidates — **figées avant observation**

> Gelées ici pour éviter le *cherry-picking* a posteriori. Toutes se calculent
> **par chambre** et **sur l'historique existant**, **conditionnées extérieur**
> et **stratifiées par couplage inféré** (§3.3). Aucune n'introduit d'entité.

### 4.1 Effectivité (primaires)
| Métrique | Définition (lecture historique) | Conditionnement |
|---|---|---|
| **Pente de refroidissement** | Δ(température chambre)/Δt pendant les phases `clim_mode_local='cool' ∧ clim_power='on'` (°C/h) | ext + période |
| **Réponse au démarrage** | baisse de température chambre dans les N min suivant un passage COOL ON | ext + période |
| **Écart résiduel à la cible** | température chambre − cible, en fin de phase COOL (proxy via `ecart_consigne_instantane`) | ext |
| **Suivi du palier** | corrélation température chambre ↔ refroidissement effectif du volume commun | couplage |

### 4.2 Couplage / découplage (structurelles)
| Métrique | Définition | Remarque |
|---|---|---|
| **Indice de découplage** | non-réponse thermique **+** montée CO₂ concomitante | proxy §3.3 |
| **Dispersion inter-chambres** | `temperature_max_chambres − temperature_min_chambres` aux transitions `clim_target_mode` | matérialise le `Δ` de la Phase 6 |
| **Persistance chaude d'une pièce** | durée pendant laquelle une chambre reste ≥ seuil pendant que les autres refroidissent | détecte la pièce « otage » |

### 4.3 Coût / contexte (secondaires)
| Métrique | Définition |
|---|---|
| **Temps COOL ON** (global) | durée `clim_mode_local='cool'` par période (un seul appareil → global) |
| **Énergie estimée** | `clim_consommation_estimee_*` par fenêtre |
| **Fragmentation** | nombre de cycles COOL substantiels / médiane de durée |

---

## 5. Garde-fou structurel — **aucune influence sur la décision COOL**

Phase 0 est **purement lectrice**. Invariants à respecter pour ce chantier et
toute suite éventuelle :

- **Aucune** des métriques ci-dessus n'est lue par la chaîne de décision
  (`besoin_*`, `autorisation_*`, `admissibilité`, `clim_target_mode`,
  exécution). L'observation **ne doit jamais** entrer dans le pilotage.
- Phase 0 **ne crée aucune entité** : il n'y a donc rien qui *puisse* être lu par
  la décision. La séparation est garantie par construction.
- Si une Phase 1 matérialise des capteurs (voir §6), ils devront rester
  **strictement observationnels** (même discipline que « la couche besoin n'intègre
  aucune contrainte physique ») : produits *en aval*, jamais consommés *en amont*.

---

## 6. Critères de passage éventuel en Phase 1 (matérialisation de capteurs)

Phase 1 (capteurs dérivés / `statistics` / UI) n'est **pas** engagée. Elle ne
serait justifiée **que si** Phase 0 démontre, sur l'historique existant, que :

1. **Le signal existe et est lisible** : les pentes/indices par chambre sont
   exploitables après conditionnement extérieur (sinon : bruit → pas de capteur).
2. **Le découplage est fréquent et matériel** : la dispersion inter-chambres et
   l'indice de découplage dépassent régulièrement un seuil que Phase 0 aura
   caractérisé (sinon : phénomène marginal → ne rien pérenniser).
3. **Une lecture récurrente apporte de la valeur** : besoin d'un suivi continu
   (UI/tendance) plutôt que d'analyses ponctuelles sur l'historique.
4. **Le coût CI/runtime est maîtrisé et listé** : notamment la contrainte
   **recorder ↔ statistics** (toute source d'un capteur `statistics` doit être
   historisée, sinon fenêtre tronquée silencieusement) et la pureté
   observationnelle (§5).

Tant que ces critères ne sont pas remplis et documentés, **on reste en Phase 0**.

---

## 7. Ce que ce chantier ne tranchera pas

- Le **rendement énergétique** réel de l'appareil (pas de COP par pièce).
- L'**état exact des portes** (variable cachée ; CO₂ = proxy imparfait).
- Toute **décision de réglage** (seuils, consigne, stratégie ON/OFF) — hors
  périmètre, et traité ailleurs (audit topologique, protocole seuils).
- L'**action interne** de l'appareil (`hvac_action` non historisée).

*Phase 0 — cadrage uniquement. Aucune modification du système. Aucune entité.
Aucune décision.*
