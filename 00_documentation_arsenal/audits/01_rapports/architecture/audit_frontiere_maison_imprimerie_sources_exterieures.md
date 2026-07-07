# Audit d'architecture — Frontière Maison / site Imprimerie et sources extérieures

**Périmètre** : consommation, par une décision du domaine **Maison**, d'une **source extérieure hors domicile** (extérieur local du **site Imprimerie**), à l'occasion de l'incident corrigé par la **PR #298** (canal demande climatique de l'arrosage).
**Base** : HEAD `a7b0896` (post-#298).
**Nature** : audit d'architecture **statique, en lecture seule**. Aucun runtime, aucune entité, aucun `entity_id` modifié par le présent document. Il **fige** le constat à date et **propose** un alignement doctrinal ; il ne s'auto-applique pas.
**Référentiel opposable** :
- [`architecture/03_doctrines/principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) — invariants universels (autorité unique par domaine, séparation des couches, nommage par représentation).
- [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) — autorité unique de décision.
- [`architecture/03_doctrines/nommage_entites.md`](../../../architecture/03_doctrines/nommage_entites.md) — convention de nommage (zones).
- [`architecture/capteurs_meteo.md`](../../../architecture/capteurs_meteo.md) — architecture des capteurs météo.
- [`architecture/securisation_capteurs_externes.md`](../../../architecture/securisation_capteurs_externes.md) — sécurisation des capteurs issus d'intégrations externes.
- [`contrats/arrosage/16_canal_demande_climatique.md`](../../../contrats/arrosage/16_canal_demande_climatique.md) — contrat du canal demande climatique.

---

## 1. Rappel factuel

Le canal **demande climatique** de l'arrosage (`12_template_sensors/arrosage/demande_climatique.yaml`) expose deux grandeurs d'observation : l'**ET₀** (journalière) et le **VPD** (courant). Avant la PR #298 :

- la branche **ET₀** lisait déjà les sources locales du **domicile** (suffixe `_jardin`), directement et via la moyenne 24 h dérivée du jardin ;
- la branche **VPD** lisait `sensor.temperature_exterieur` et `sensor.humidite_relative_exterieur`.

Ces deux dernières entités agrègent des **capteurs météo extérieurs situés sur un autre site géographique et fonctionnel — le site Imprimerie** — distant du domicile d'environ 8 km. Elles ne mesurent donc **pas** les conditions du jardin du domicile. Le VPD « du jardin » était de fait piloté par une **source extérieure hors domicile**, non représentative du jardin. Lorsque cette source extérieure distante est devenue indisponible, `sensor.arrosage_demande_climatique_vpd` est passé indisponible.

Les sources locales représentatives du jardin **existaient déjà** (`sensor.temperature_jardin`, `sensor.humidite_relative_jardin`), et étaient déjà utilisées par la branche ET₀ du même fichier. L'incohérence était donc **interne au fichier** : deux branches d'un même capteur reposant sur deux périmètres géographiques différents.

La **PR #298** a réaligné la branche VPD (et l'état qualitatif associé) sur les sources `_jardin`, et mis le tableau des entrées du contrat 16 en cohérence.

**Point de qualification essentiel.** Le problème n'était **pas** l'existence d'une source extérieure sur le site Imprimerie — cette source est légitime dans son propre périmètre (supervision et affichage de l'extérieur du site professionnel distant). Le problème était sa **consommation par une décision Maison locale**, pour laquelle elle n'est ni représentative ni autorisée.

---

## 2. Nature exacte de l'erreur

L'incident se décompose en quatre niveaux distincts, qu'il faut ordonner pour ne pas le réduire à un seul.

| Niveau | Qualification | Description |
|---|---|---|
| **Cause racine** | Liaison rôle → interface canonique insuffisamment opposable | Le contrat 16 décrit ses entrées par leur **rôle** (« température extérieure courante », « humidité relative extérieure courante ») et **ne fige volontairement aucun `entity_id`**. Le pont entre le rôle métier et l'entité concrète n'était garanti par aucun mécanisme opposable : il reposait sur le jugement de l'implémenteur. |
| **Mécanisme** | Homonymie de périmètre | Le mot « extérieur » a **deux sens** dans le dépôt : (a) un **rôle météo générique** (« l'air au-dehors, au-dessus du jardin ») et (b) un **périmètre toponymique** — le suffixe `_exterieur`, qui désigne l'**extérieur local du site Imprimerie**. L'entité au nom le plus proche du rôle (`sensor.temperature_exterieur`) appartenait au périmètre (b). |
| **Conséquence** | Franchissement de frontière de périmètre | Une décision du périmètre **Maison / jardin domicile** a consommé une entrée du périmètre **site Imprimerie**. |
| **Symptôme** | Donnée non représentative, puis indisponibilité | La grandeur produite ne décrivait pas le jardin ; elle s'est effacée quand la source distante a décroché. C'est la seule strate réellement observée en exploitation. |

**Formulation à retenir (corrige une lecture trop courte).** Il serait inexact de qualifier l'incident de simple consommation d'une « source brute ». La source en cause est une **source agrégée**, stable et exploitable **dans son propre périmètre**. L'erreur n'est pas un défaut de qualité de la source : c'est un **défaut d'autorisation de périmètre**. La règle exacte est :

> Une source peut être correcte, stable et exploitable **dans son propre périmètre**, tout en étant **interdite** pour une décision Maison si elle n'est pas explicitement promue comme **interface canonique autorisée** pour ce domaine.

**Enseignement doctrinal.** La convention « `_exterieur` = extérieur local du site Imprimerie / `_jardin` = extérieur local du domicile » n'a pas été inventée par la PR #298 : elle **découlait déjà** des invariants existants (autorité unique par domaine, séparation des couches, nommage par représentation). Le défaut a tout de même été écrit. C'est la démonstration que **la documentation seule ne protège pas une architecture** : une convention décrite mais non défendue par une **interface** ou un **contrôle opposable** reste franchissable, en particulier par un intervenant — humain ou outil — travaillant par recherche lexicale et en contexte partiel.

---

## 3. Typologie des sources

L'incident impose de distinguer explicitement des catégories que le langage courant confond sous le mot « extérieur ».

| Catégorie | Définition | Exemples dans le dépôt | Consommable par une décision Maison ? |
|---|---|---|---|
| **Source locale domicile / jardin** | Grandeur mesurée dans le périmètre du domicile | axe `_jardin` (température, humidité relative, humidité absolue) | Oui, **via l'interface canonique** (ci-dessous) |
| **Source extérieure du site Imprimerie** | Grandeur mesurée à l'extérieur du **site professionnel distant** | axe `_exterieur` (température, humidité relative, dérivés humidex / point de rosée / humidité absolue) | **Non** — hors périmètre Maison |
| **Source météo externe** | Donnée d'un service tiers / prévision | entités `weather.*` | Non au cœur d'un calcul de décision (cf. contrat 16 §8) |
| **Capteur physique** | Mesure d'un capteur individuel, non consolidée | sources unitaires en amont des agrégats et des pipelines | Non directement |
| **Agrégat** | Combinaison de plusieurs capteurs sans pipeline de validation métier | agrégat de l'axe `_exterieur` (combinaison de deux capteurs extérieurs du site distant) | Non pour une décision Maison |
| **Interface canonique métier** | Grandeur consolidée d'un domaine, validée, stabilisée, sous garanties de disponibilité et sous contrat | axe `_jardin` publié (chaîne validation → consolidation → façade → statut) | **Oui — voie unique légitime** |

**Point doctrinal central.**

> Une source **canonique ou valide dans un périmètre A** ne devient **pas automatiquement** canonique ou autorisée dans un **périmètre B**. La canonicité et l'autorisation sont **relatives au domaine consommateur**, jamais absolues.

Ainsi, l'agrégat de l'axe `_exterieur` est une grandeur parfaitement acceptable pour la **supervision de l'extérieur du site Imprimerie** ; il n'est ni représentatif ni autorisé pour une **décision Maison**. Symétriquement, l'axe `_jardin` est l'autorité pour le climat extérieur du domicile, et c'est **la seule** interface que les décisions Maison portant sur l'extérieur local doivent consommer.

**Asymétrie de robustesse constatée.** L'axe `_jardin` dispose d'une chaîne de consolidation complète (validation des sources, détection d'incohérence, valeur cible robuste, façade de publication, statut, mémoire à durée de vie bornée, disponibilité explicite) et de contrôles CI dédiés. L'axe `_exterieur` est une agrégation simple sans pipeline métier ni contrôle CI. Le périmètre le plus fragile est aussi le moins gardé : consommer `_exterieur` dans une décision Maison importe cette fragilité **en plus** de l'erreur de représentativité.

---

## 4. Risque de régression

### 4.1 État constaté après la PR #298

Le balayage des domaines de décision Maison à la base `a7b0896` ne fait apparaître **aucune décision Maison résiduelle** consommant l'axe `_exterieur` :

- climatisation, chauffage, aération : lecture de l'axe `_jardin` ;
- déshumidificateur : capteurs de la cave ;
- VMC : capteurs de pièces ;
- volets / pluie : pluviomètre dédié.

Les consommateurs restants de l'axe `_exterieur` relèvent tous du **périmètre site Imprimerie assumé** (dashboards du site, dérivés statistiques et de couleur du site, historisation, groupe d'intégration). Le risque de **câblage** résiduel est, à date, **nul**.

### 4.2 Risque latent — onomastique

Le risque n'est pas fermé pour autant : il est devenu **latent** et de nature **onomastique**. Trois motifs méritent une vigilance particulière.

1. **Motif inversé — le plus piégeux.** L'entité `sensor.temperature_exterieure_moyenne_jour` porte « exterieure » dans son nom mais repose en réalité sur `sensor.temperature_jardin` (source domicile ; cf. `13_sensor_platforms/statistics/meteo/temperature_jardin.yaml`, `entity_id: sensor.temperature_jardin`). Elle est légitimement consommée par l'ET₀ de l'arrosage. Un intervenant cherchant à « harmoniser » les noms pourrait la re-pointer par erreur vers l'axe `_exterieur` du site distant, rejouant l'incident à l'envers. **Ce motif interdit tout contrôle par joker large de type `*exterieur*`** : un tel contrôle produirait un faux positif sur une entité légitime et casserait la chaîne ET₀.

2. **Cohabitation de périmètres dans un même fichier.** Les dérivés `..._jardin` et `..._exterieur` (humidex, point de rosée, humidité absolue) coexistent dans les mêmes fichiers de base météo. Toute édition de ces fichiers met les deux périmètres à portée d'un copier-coller.

3. **Seuils suffixés « exterieure » / « ext ».** Plusieurs seuils (climatisation, aération) portent un suffixe évoquant « l'extérieur » tout en étant comparés à l'axe `_jardin`. Aucun n'est fautif aujourd'hui, mais le vocabulaire entretient l'intuition trompeuse « extérieur = dehors quelconque ».

### 4.3 Profils d'erreur à anticiper

- **Recherche lexicale.** Un intervenant (humain ou outil) qui relie le rôle « température extérieure » à la première entité au nom plausible retombe dans l'homonymie — précisément parce que le contrat ne fige pas l'`entity_id`.
- **Nouveaux domaines Maison consommant une grandeur extérieure.** Tout futur usage (protection gel, ventilation nocturne, gestion des volets au soleil, séchage extérieur, etc.) présente le même risque de rattachement au mauvais périmètre. La classe d'erreur est **transverse**, pas propre à l'arrosage.

---

## 5. Garde-fous — familles comparées

Le présent audit **ne code aucun contrôle**. Il compare les familles de garde-fous pour éclairer l'arbitrage.

| Famille | Effet | Portée | Limite principale |
|---|---|---|---|
| **Clarification documentaire** | Décrit la frontière et l'homonymie | Toutes zones | Ne **défend** pas la frontière ; invisible pour qui ne lit pas le bon fichier. **Nécessaire mais insuffisante seule** (cf. §2). |
| **Interfaces canoniques de domaine** | Rend l'axe `_jardin` explicitement seule autorité Maison ; déclare l'axe `_exterieur` comme canonique du **seul** périmètre site Imprimerie | Transverse | Suppose la discipline de consommation ; ne bloque pas mécaniquement une violation. |
| **Fixation d'`entity_id` dans les contrats décisionnels** | Referme la cause racine : lie le rôle à une entité opposable pour les **entrées de décision** | Par contrat | Rigidifie ; réservé aux entrées réellement décisionnelles (ne pas figer les rôles d'observation libre). |
| **Contrôle statique CI par deny-list explicite** | Refuse au merge qu'un fichier de décision Maison référence une **entité nommément listée** de l'axe `_exterieur` | Transverse | Doit être **exact** (jamais un joker `*exterieur*` — cf. motif inversé §4.2) ; ne distingue pas nativement décision et affichage. |
| **Renommage d'entités** | Supprime l'homonymie à la racine | Transverse | Rayon de souffle élevé (continuité d'historique, dashboards du site, doctrine de nommage) ; **arbitrage opérateur**, hors du présent livrable. |

**Orientation proposée (documentaire d'abord).**

1. **Court terme — documentaire (objet du présent livrable).** Formaliser la frontière dans la doctrine et les contrats : principe d'autorisation de source par périmètre, désambiguïsation des zones « Extérieur » (site Imprimerie) et « Jardin » (domicile), rappel de l'interface canonique dans le contrat 16 et l'architecture météo.
2. **Étape suivante possible (non implémentée ici).** Un contrôle CI de séparation des périmètres, fondé sur une **deny-list exacte** d'entités de l'axe `_exterieur` dans le champ des fichiers de décision Maison, avec **exceptions explicites** (notamment `sensor.temperature_exterieure_moyenne_jour`, qui repose sur le jardin). À arbitrer séparément ; **aucun joker large sur « exterieur »**.
3. **Long terme — optionnel.** Renommage éventuel de l'axe `_exterieur` pour lever l'homonymie, sous réserve d'un arbitrage opérateur sur le coût (historique, dashboards, doctrine de nommage).

Le renommage et la CI **ne sont pas décidés par cet audit** ; ils sont posés comme suites possibles.

---

## 6. Recommandation documentaire

**Principe cible.**

> Toute décision Maison portant sur une grandeur extérieure locale consomme **exclusivement l'interface canonique du domicile** (axe `_jardin`). Une source d'un **autre périmètre** (extérieur du site Imprimerie, service externe) n'est **jamais** autorisée par défaut pour une décision Maison ; son autorisation est **relative au domaine** et doit être explicite. La frontière est **formalisée en doctrine et en contrat**, et pourra ensuite être défendue par un contrôle statique à deny-list exacte.

**Alignements doctrinaux retenus (appliqués dans le présent lot documentaire).**

- **Principes généraux** — ajout d'un principe « autorisation de source par périmètre » (une source canonique dans un périmètre A n'est pas automatiquement autorisée dans un périmètre B).
- **Nommage des entités** — désambiguïsation explicite des zones « Extérieur » (extérieur local du site Imprimerie) et « Jardin » (extérieur local du domicile), avec avertissement sur l'homonymie « extérieur » rôle vs périmètre.
- **Capteurs météo** — note de périmètre sur les axes `_exterieur` et `_jardin`, et rappel que les décisions Maison consomment l'axe `_jardin`.
- **Contrat arrosage — canal demande climatique** — clarification que les entrées de décision (VPD, ET₀) désignent l'extérieur **du domicile** et se consomment via l'interface canonique `_jardin`, distincte de l'axe `_exterieur` du site distant.

**Volontairement non traité dans ce lot.**

- **Aucun contrôle CI** n'est créé (étape suivante possible, cf. §5).
- **Aucun renommage** d'entité (arbitrage opérateur, cf. §5).
- **Aucun runtime** modifié (l'incident de code est déjà corrigé par la PR #298).
- **Aucun changelog** produit : la procédure de changelog n'est engagée que sur dépôt de diffs de release et demande explicite de l'opérateur ; une modification documentaire se trace par le commit / la PR.
- `architecture/securisation_capteurs_externes.md` est **laissé inchangé** : ce document est en version figée et son Invariant 4 (séparation source brute / état local sécurisé) traite une question **orthogonale** à l'autorisation de périmètre ; la doctrine du dépôt veut qu'une extension fasse l'objet d'un document distinct — rôle tenu ici par le principe ajouté aux principes généraux et par le présent audit.

**Risques et limites de la recommandation documentaire.**

- Elle **formalise et décrit** la frontière ; elle ne la **défend pas mécaniquement**. La défense mécanique relève de la fixation d'`entity_id` et/ou du contrôle CI (étapes suivantes).
- Elle réduit le risque pour qui **lit** la doctrine ; elle reste sans effet sur un intervenant travaillant en contexte strictement partiel — d'où l'intérêt d'une étape CI ultérieure.
- La deny-list CI évoquée devra impérativement **exempter** les entités au nom trompeur mais à source domicile (motif inversé §4.2), sous peine de faux positifs bloquants.

---

## 7. Suites possibles (non engagées ici)

- **CI de séparation des périmètres** : contrôle statique à **deny-list exacte** des entités de l'axe `_exterieur` dans les fichiers de décision Maison, avec **exceptions explicites**, sur le modèle des contrôles de contrat existants. À cadrer et arbitrer séparément ; à ne pas construire sur un joker « exterieur ».
- **Fixation d'`entity_id`** pour les entrées **décisionnelles** des contrats concernés (au-delà de l'arrosage), là où le rôle doit être lié à une entité opposable.
- **Renommage** éventuel de l'axe `_exterieur`, sous arbitrage opérateur (coût historique / dashboards / doctrine de nommage).

---

*Audit d'architecture Arsenal — lecture seule. Aucun runtime, aucune entité, aucun `entity_id` modifié par ce document. Les alignements doctrinaux associés sont portés par les modifications documentaires du même lot (principes généraux, nommage, capteurs météo, contrat arrosage 16).*
