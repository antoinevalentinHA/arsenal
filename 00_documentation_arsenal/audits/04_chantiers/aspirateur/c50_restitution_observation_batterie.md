# Chantier ASPIRATEUR (C50) — Restitution de l'observation de charge

| Champ | Valeur |
|---|---|
| **Chantier** | **Honorer le renvoi d'`ASP-INV-41`.** Le contrat refuse tout seuil de batterie au lancement **parce que** la charge est « une **observation** exposée à l'opérateur, qui décide » ([`07`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.3). Aucune surface du domaine ne la portait : la contrepartie était **promise et non tenue**. Ce chantier la rend — **niveau** et **alimentation en cours** —, la place dans la hiérarchie du panneau plutôt qu'à côté d'elle, et ferme la boucle par un contrôle CI. |
| **Domaine** | Aspirateur. |
| **Nature** | **Écart contrat ↔ interface, corrigé.** Aucune règle métier nouvelle, aucun arbitrage nouveau : la clause existe depuis `ASP-INV-41` et n'était pas exécutée. Ce chantier **n'ajoute aucun invariant** et n'amende la portée d'aucun. |
| **Statut** | **Ouvert (2026-09-07) — Lots 1 à 4 exécutés le jour de l'ouverture ; Lot 5 (validation terrain) dû.** Contrat, interface et CI livrés d'un même mouvement ; reste à confirmer sur l'instance que les deux témoins natifs alimentent bien les deux tuiles et que la mise en page tient sur mobile portrait. |
| **Priorité** | **P2** — aucun risque de sûreté : la charge ne conditionne rien, et le backend ne la lit pas. L'enjeu est la **complétude de la lecture offerte à l'opérateur** avant une décision de lancement. |
| **Ouvert le** | 2026-09-07. |
| **Prochain jalon** | **Lot 5 — validation terrain** (§5.5). |
| **Registre** | Chantier **C50** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Autorités amont** | [`07_moteur_de_mission.md`](../../../contrats/aspirateur/07_moteur_de_mission.md) §5.3 (`ASP-INV-41`) · [`08_etats_et_observation.md`](../../../contrats/aspirateur/08_etats_et_observation.md) §2 · [`11_frontiere_ui.md`](../../../contrats/aspirateur/11_frontiere_ui.md) §3 · [`audit_faisabilite_roborock_q7_max.md`](../../01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md) §7 (attestation des deux témoins). |
| **Constats couverts** | **Aucun constat existant.** L'écart n'était relevé ni par l'audit de conformité, ni par la contre-expertise, ni par leur confrontation : les cinq constats `AUD-ASP-*` et les `CC-*` / `RC-*` portent sur d'autres objets. Il est **entré par l'observation directe de l'opérateur**, le 2026-09-07. |

> **⚠️ Ce que ce chantier ne fait pas.**
> Il ne crée **aucun seuil**, visuel ou logique — `ASP-INV-41` l'interdit, et une couleur d'alerte serait un seuil (§4, `D-3`).
> Il ne touche **ni le moteur de mission, ni la conduite, ni la supervision, ni l'entretien** : la charge ne gate rien et n'est lue par aucun backend.
> Il **n'inscrit aucun identifiant technique dans les contrats** (`ASP-INV-58`) : la restitution y est désignée par son rôle.
> Il **ne recoupe pas `C45`** : aucune ligne de la migration `Q1` / `Q2` n'est touchée, aucune preuve n'est partagée (§7).
> Aucun changelog créé (doctrine [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1 — artefact de release).

---

## 1. Origine

**Constat opérateur, 2026-09-07** : « les dashboards Aspirateur n'indiquent nulle part l'état de la
charge de l'aspirateur ». Vérification faite au SHA `48f6cb37`, le constat est **établi**, avec une
nuance qui oriente tout le chantier : ce n'est pas *rien* qui est rendu, c'est **le niveau** qui
manque.

```text
07 §5.3 (ASP-INV-41)  « aucun seuil de batterie … la batterie reste une
                        OBSERVATION EXPOSÉE À L'OPÉRATEUR (08), qui décide »
       │
       └─→ 08 §2      nomme l'AUTORITÉ (« entités natives correspondantes,
                        observation, jamais gate ») — ne prescrit aucun rendu
             │
             └─→ 11 §3  « Ce que l'UI doit faire » : huit obligations,
                          AUCUNE ne porte l'observation de charge
                   │
                   └─→ interface : rien ne la porte.   ← l'écart
```

**La chaîne de renvois se termine dans le vide.** Chaque maillon est exact ; leur composition ne
produit aucune obligation, et personne n'a donc rien implémenté. C'est un défaut de **renvoi non
honoré**, pas une violation : rien n'interdisait la restitution, rien ne l'exigeait.

**Pourquoi cela compte, et pas seulement pour le confort.** `ASP-INV-41` est une clause d'abstention :
Arsenal renonce délibérément à juger la batterie, **et transfère ce jugement à l'opérateur**. Un
transfert de décision vers quelqu'un à qui on ne montre pas la donnée n'est pas un transfert : c'est
une abstention sans destinataire.

---

## 2. Inventaire d'entrée — établi, opposable

### 2.1 Ce que les trois écrans rendent aujourd'hui

| Écran | Contenu | Charge ? |
|---|---|---|
| `/aspirateur-dashboard` — [`panneau_operationnel.yaml`](../../../../18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml) | État canonique · Mission · Dernier motif · Composition · Lancement · Conduite · Entretien | **L'activité « En charge »**, l'un des dix états canoniques. **Jamais le niveau.** |
| `/aspirateur-carte-dashboard` — [`carte_robot.yaml`](../../../../18_lovelace/includes/cartes/aspirateur/carte_robot.yaml) | Carte chargée, trois images | Non |
| `/aspirateur-entretien-dashboard` — [`entretien.yaml`](../../../../18_lovelace/includes/cartes/aspirateur/entretien.yaml) | Quatre postes d'usure, verdict de déclaration | Non |

### 2.2 Fait mécanique

Au SHA d'entrée, les deux témoins natifs de charge apparaissent **exclusivement** dans des jeux
d'essai du checker et dans l'audit de faisabilité : **aucun fichier runtime, aucun arbre Lovelace ne
les nomme.**

### 2.3 Les deux témoins sont attestés, et leur lecture est déjà licite

L'audit du domaine les relève tous deux (§7 — `75 %` et `off`). `ASP-CI-7` n'interdit en Lovelace que
les entités **d'action** et les noms de service : il porte même en jeu d'essai un cas **conforme**
nommant ces deux entités en lecture. **Aucune levée d'interdit n'est donc nécessaire** — le chantier
n'ouvre aucune porte, il emprunte une porte ouverte que personne n'avait franchie.

### 2.4 Angle mort adjacent — signalé, non traité ici

`charging_complete` fait partie des **32 valeurs natives sur 43** que le contrat ne classe pas : un
robot amarré batterie pleine tomberait en classe `N`, rendu « Non qualifié », et **refuserait le
lancement** (`ASP-INV-60`). C'est un arbitrage **rendu et assumé** (`ARB-1`), qui prévoit son propre
véhicule de révision — un lot terrain. Ce chantier **ne le rouvre pas**, mais il en atténue l'opacité :
face à un « Non qualifié », l'opérateur lira désormais le niveau et l'alimentation, au lieu de n'avoir
aucune prise. **Aucune conclusion n'est tirée ici de cette hypothèse, qui reste à observer (§5.5).**

---

## 3. Ce que le contrat exigeait déjà, et ce qu'il lui manquait

| Source | Dit | Manquait |
|---|---|---|
| `07` §5.3 — `ASP-INV-41` | Aucun seuil ; la batterie est une observation **exposée à l'opérateur** | Le destinataire du renvoi n'oblige personne |
| `08` §2 | L'**autorité** : entités natives, « observation, jamais gate » | Une autorité n'est pas un rendu |
| `11` §3 | Huit obligations de restitution | Aucune ne nomme la charge |

**Correctif contractuel retenu : un neuvième item au `11` §3**, et deux renvois rendus explicites en
`07` §5.3 et `08` §2. C'est le **minimum suffisant** : l'obligation naît là où vivent déjà les
obligations d'interface, et **aucun invariant nouveau n'est déclaré** — l'exigence est celle
d'`ASP-INV-41`, enfin adressée.

---

## 4. Décisions de conception rendues

### `D-1` — La restitution vit dans le bloc d'entrée, en deuxième ligne

Le bloc d'entrée du panneau est une grille à deux colonnes portant **État** et **Mission**. Il devient
une grille **2 × 2** : la charge occupe la **seconde ligne**, sous les deux tuiles existantes, et
**avant** le « Dernier motif » pleine largeur.

**La hiérarchie est portée par la géométrie, et redoublée par la couleur** :

```text
┌───────────────┬───────────────┐   ligne 1 — CE QUE FAIT LE ROBOT
│ État          │ Mission       │   verdicts, colorés (vert / bleu / orange / rouge)
├───────────────┼───────────────┤   ligne 2 — DE QUOI IL DISPOSE POUR LE FAIRE
│ Batterie      │ En charge     │   observations, gris neutre — jamais un verdict
├───────────────┴───────────────┤
│ Dernier motif                 │   phrase du backend, pleine largeur
└───────────────────────────────┘
```

**Alternatives examinées et écartées** :

| Écartée | Motif |
|---|---|
| Passer le bloc d'entrée à **trois colonnes** | Tronquerait les libellés existants (« Non qualifié », « Indisponible ») sur mobile portrait, que la géométrie à deux colonnes protège explicitement. On ne dégrade pas ce qui marche pour loger ce qui manque. |
| Une **cinquième section** avec en-tête | Cinq en-têtes pour deux tuiles de lecture : c'est précisément le « vrac » que la commande interdit. La charge n'est pas un sujet, c'est une lecture d'entrée. |
| Une tuile **pleine largeur** | Un pourcentage n'a pas besoin de toute la largeur ; il déséquilibrerait le bloc et concurrencerait le « Dernier motif », seul objet qui mérite cette forme. |
| Une **troisième tuile seule** dans la grille à deux colonnes | Laisse une demi-cellule vide, et `R-LL-GRID-1` refuse une cardinalité non divisible. La contrainte CI et l'exigence esthétique disent ici la même chose. |

### `D-2` — Deux tuiles, pas une

Le **niveau** et l'**alimentation en cours** ont deux autorités natives distinctes et peuvent
**légitimement diverger** — c'est le régime que le `08` §1.1 pose déjà pour deux autres notions du
domaine, et qu'il demande à l'interface de **rendre** plutôt que de résorber. Les fondre en une seule
tuile serait une agrégation de confort. Elles sont donc deux, côte à côte, jamais confondues.

### `D-3` — Aucun seuil, donc aucune couleur sémantique

**Décision structurante.** Les deux tuiles sont en **gris neutre** `rgba(158, 158, 158, 0.2)`, et
retombent au **gris d'indisponibilité** `rgba(158, 158, 158, 0.1)` sur `unknown` / `unavailable` ou
valeur non numérique (`ASP-INV-45`, règle `R6` de la charte).

Trois raisons cumulatives, dont une seule suffirait :

1. **`ASP-INV-41` refuse tout seuil de batterie.** Peindre un niveau bas en rouge *est* un seuil — un
   seuil qu'aucun texte ne fixe, appliqué sans être écrit. La forme visuelle ne rend pas la règle
   moins normative.
2. **La palette du panneau est close et documentée en tête de fichier** : le rouge y signale une
   anomalie (erreur du robot, entretien dû), le vert une pièce sélectionnée, le bleu un choix actif,
   l'orange les deux gestes qui interrompent. Une batterie basse n'est **aucune** de ces quatre
   choses. Lui prêter le rouge banaliserait le rouge là où il porte.
3. **La hiérarchie du bloc en dépend** (`D-1`) : la ligne 1 est colorée parce qu'elle juge, la ligne 2
   est calme parce qu'elle observe. Colorer la ligne 2 effacerait la distinction que la mise en page
   vient d'établir.

> **`QO-C50-1` — question ouverte, non tranchée.** Si l'opérateur veut malgré tout un signal visuel
> sous un certain niveau, c'est un **arbitrage métier** : il faudrait fixer la valeur du seuil, en
> établir le fondement, et **amender la portée d'`ASP-INV-41`** — qui ne refuse aujourd'hui le seuil
> que *parce que* l'opérateur décide. Cette question est **posée, pas résolue** : ce chantier livre la
> version honnête.

### `D-4` — Le robot n'entre pas dans `group.batteries`

Le groupe alimente les capteurs agrégés de batteries faibles et à remplacer, qui déclarent faible
toute valeur **inférieure à 28 %**. Une batterie de **traction**, qui se décharge par construction à
chaque mission et se recharge ensuite, y fabriquerait une alerte de maintenance récurrente et fausse —
sur un équipement dont **aucune pile n'est à remplacer**. Le périmètre du groupe est « capteurs de
batteries » pour la **maintenance humaine** ; ce n'en est pas une. **Exclusion délibérée, inscrite ici
pour qu'elle ne se reperde pas.**

### `D-5` — Un gabarit du domaine, pas une réutilisation transverse

Un gabarit de batterie à seuils existe déjà, mais il vit sous `40_dashboards/audi/` et **impose des
seuils colorés** que `D-3` refuse. Le domaine crée donc le sien,
[`carte_aspirateur_batterie.yaml`](../../../../19_button_card_templates/40_dashboards/aspirateur/carte_aspirateur_batterie.yaml),
**satellite de `socle_status`** — le même socle que ses trois voisines de bloc, ce qui garantit
l'unité typographique de la grille 2 × 2. C'est le précédent déjà suivi par
`carte_action_aspirateur_option`, généralisé depuis un gabarit voisin plutôt qu'appelé à travers les
domaines.

L'alimentation, elle, **ne crée aucun gabarit** : elle emploie le générique
`carte_mode_binaire_interprete`, dont les variables de libellé et de couleur suffisent exactement.

### `D-6` — Identifiant de contrôle

**`ASP-CI-46`** est attribué à ce chantier, **vérifié libre** avant emploi — `ASP-CI-45` était le
dernier attribué. Aucun autre identifiant n'est créé : ni invariant, ni entité, ni automation.

---

## 5. Lots

### 5.1 Lot 1 — Ouverture documentaire — **EXÉCUTÉ (2026-09-07)**

Le présent document, la ligne `C50` au registre des chantiers, l'entrée d'index. **Aucun contrat,
aucun code.**

### 5.2 Lot 2 — Propagation contractuelle — **EXÉCUTÉ (2026-09-07)**

| Item | Contenu |
|---|---|
| **2.1** | `11` §3 — **neuvième obligation** : l'UI restitue l'observation de charge, **niveau et alimentation distinctement**, **sans seuil ni couleur d'alerte**, en rendant l'indisponibilité. |
| **2.2** | `07` §5.3 — le renvoi devient **exigible** : il nomme le chapitre qui porte désormais l'obligation. |
| **2.3** | `08` §2 — la ligne « Batterie, charge » dit que cette observation **est restituée**, et sous quel régime. |
| **Ne fait pas** | Aucun invariant déclaré. **Aucun identifiant technique porté au contrat** (`ASP-INV-58`) : le rôle, jamais l'entité. |

### 5.3 Lot 3 — Interface — **EXÉCUTÉ (2026-09-07)**

| Item | Contenu |
|---|---|
| **3.1** | Gabarit `carte_aspirateur_batterie` — lecture seule stricte, pourcentage arrondi, `—` sur valeur non numérique, icône suivant le niveau, **deux gris et rien d'autre**. |
| **3.2** | Bloc d'entrée porté à **2 × 2** selon `D-1` ; en-tête du panneau mis à jour — il énumère ses patrons et sa hiérarchie, il ne peut pas décrire un bloc qui a changé. |
| **3.3** | Tuile d'alimentation sur le générique binaire, libellés `Oui` / `Non`, **deux gris**. |
| **Preuve** | Grille à quatre cellules pour deux colonnes (`R-LL-GRID-1`) ; aucune entité d'action, aucun nom de service (`ASP-CI-7`) ; aucun Jinja dans un dashboard (`R-LL-SKEL-1`). |

### 5.4 Lot 4 — Fermeture de la boucle CI — **EXÉCUTÉ (2026-09-07)**

**`ASP-CI-46` — restitution de l'observation de charge.** Trois obligations, lues sur les fichiers
réels :

| Volet | Ce qui est vérifié | Ce qu'une régression produit |
|---|---|---|
| **Présence** | Le panneau porte **une tuile par témoin**, chacune sur l'entité native attestée, hors commentaires | Une suppression de tuile est **rouge** — l'écart de 2026-09-07 ne peut pas se reformer en silence |
| **Distinction** | Les deux tuiles sont **deux nœuds distincts** — jamais une seule qui porterait les deux | Une fusion « de confort » est **rouge** (`D-2`) |
| **Absence de seuil** | Le gabarit de batterie ne contient **aucune couleur sémantique** — ni rouge, ni orange, ni jaune, ni vert, ni bleu ; ses seules teintes sont les deux gris | L'introduction d'un seuil visuel est **rouge**, y compris déguisée en réglage de gabarit (`D-3`, `ASP-INV-41`) |

**Ce troisième volet est le cœur du contrôle** : sans lui, `ASP-INV-41` resterait une clause qu'aucun
mécanisme ne défend — exactement l'état qui a produit ce chantier.

### 5.5 Lot 5 — Validation terrain — **DÛ**

| Item | À observer sur l'instance |
|---|---|
| **5.1** | Les deux tuiles s'alimentent : un pourcentage plausible, une alimentation cohérente avec l'état du robot. |
| **5.2** | Le bloc 2 × 2 tient sur **mobile portrait** — quatre libellés entiers, quatre hauteurs égales, aucune troncature. |
| **5.3** | Sur robot amarré et plein, relever **la valeur native de l'état machine** — c'est le seul relevé qui établirait ou infirmerait l'hypothèse `charging_complete` du §2.4. **À consigner, pas à exploiter ici.** |
| **5.4** | Indisponibilité rendue : robot hors ligne, les deux tuiles tombent au gris atténué et affichent `—`. |

---

## 6. Preuves attendues — synthèse

| # | Preuve |
|---|---|
| **6.1** | Checker Aspirateur **vert**, `ASP-CI-46` compris ; batterie d'auto-tests **étendue** ; **aucun contrôle existant affaibli**. |
| **6.2** | Gates documentaires vertes : lint documentaire, `DOC-CI-*`, contrôle structurel du registre. |
| **6.3** | Contrôles Lovelace verts : géométrie des grilles, squelette pur, couleurs sémantiques. |
| **6.4** | Mutations rouges jouées dans les deux sens : tuile retirée, tuiles fusionnées, seuil coloré introduit. |
| **6.5** | Validation terrain du §5.5. |

---

## 7. Articulation avec `C42` et `C45` — sans recouvrement

| Chantier | Ce qu'il touche | Recouvrement |
|---|---|---|
| **C42** | Écran d'entretien, script de déclaration | **Aucun** — autre écran, autre objet. |
| **C45** | Projection métier de mission, migration de l'attribut ambigu, gestes de conduite | **Aucun fichier commun hors le panneau lui-même**, et **aucune ligne commune dans ce panneau** : le Lot 6 de `C45` travaille la section Mission et la section Conduite, `C50` la seconde ligne du bloc d'entrée. Les deux tuiles ajoutées ici **ne lisent ni le verdict, ni sa projection, ni le témoin de session** — aucune interaction avec `ASP-CI-11`, `ASP-CI-43`, `ASP-CI-44` ni `ASP-CI-45`. |

**Aucune dette n'est transférée, aucun constat n'est fermé, aucun état de clôture du domaine n'est
modifié.**

---

## 8. Hors périmètre — explicitement

- **Tout seuil**, visuel ou logique (`D-3`, `QO-C50-1`).
- **Toute notification** de batterie basse : elle supposerait le seuil que `D-3` refuse.
- **L'historisation** du niveau de charge — `QO-5` du chapitre `13` la tient ouverte pour tout le domaine.
- **La reclassification de `charging_complete`** (§2.4) — relève d'`ARB-1` et d'un lot terrain.
- **L'entrée du robot dans `group.batteries`** (`D-4`).
- **Les deux autres écrans du domaine** : la carte et l'entretien ne portent pas de lecture d'état.

---

## 9. Conditions de clôture

| # | Condition |
|---|---|
| **9.1** | Les deux observations sont rendues, distinctement, sur l'écran opérationnel. |
| **9.2** | Le `11` §3 porte l'obligation, et les renvois du `07` et du `08` y mènent. |
| **9.3** | `ASP-CI-46` défend les trois volets, et une régression de chacun est démontrée rouge. |
| **9.4** | La validation terrain du §5.5 est acquise, **`5.2` comprise** — l'équilibre visuel est une exigence de la commande, pas un agrément. |
| **9.5** | `QO-C50-1` est **explicitement laissée ouverte** ou tranchée par arbitrage ; elle ne se referme pas en silence. |
