# Correctif de déploiement — amorçage des paramètres et conformité UI (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.4 |
| **Nature** | **Correctif post-déploiement.** Deux défauts constatés en exploitation, l'un **fonctionnel**, l'autre d'**affichage** |
| **Statut** | **Préparé sur branche.** **Aucune écriture runtime effectuée** |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.4**. **Non modifié par ce lot** |

> **Deux causes, une racine commune : une hypothèse non vérifiée, et une
> doctrine non lue.**

---

## 1. Défaut fonctionnel — les paramètres n'ont jamais été initialisés

### 1.1 Ce qui s'est passé

L'automatisation `10190000000006`, introduite par L7.0, n'écrivait les valeurs
d'amorce que si un helper était **disponible et non numérique**.

> **Un `input_number` sans état restaurable ne prend jamais `unknown` : il
> prend son `min`.**

Le prédicat ne pouvait donc **jamais** devenir vrai.

**Preuve, sur le corpus des 38 bases** : 73 `input_number`, **32 065 lignes
d'état**, **aucun état non numérique**.

**Constat au déploiement**, qui la confirme sur l'instance :

- **aucune notification d'initialisation** n'a été émise — la garde
  `a_initialiser | count > 0` a arrêté la séquence avant toute écriture ;
- les dix helpers ont démarré **à leur minimum**.

| Helper | Chargé | Amorce prévue |
|---|---:|---:|
| `vmc_borne_basse_*` | **40** | 50 |
| `vmc_borne_haute_*` | **40** | 70 |
| `vmc_seuil_on_*` | **50** | 74 |
| `vmc_fenetre_sdb_parents` | **5 min** | 20 |
| `vmc_fenetre_sdb_enfants` | **5 min** | 30 |
| `vmc_evolution_*` | **1 pt** | 5 |

### 1.2 Conséquence fonctionnelle

Bornes égales → `OFF = 40` **en permanence**, la modulation écrasée. Entrée à
50 % ou sur une montée d'**1 point en 5 minutes** ; libération à `HR ≤ 40` — or
L5 a mesuré une ligne de base entre **53 et 63 %**.

> **Un besoin ouvert ne se libérait quasiment jamais.**

### 1.3 C'est la deuxième fois que la même erreur se produit

**L7.5 avait déjà démontré** qu'un `input_boolean` sans état restaurable
apparaît à `off`, jamais à `unknown` — et en avait tiré le retrait d'un
indicateur inopérant.

**Le même raisonnement n'a pas été porté à `input_number`.** La vérification
tenait en une requête ; elle n'a pas été faite avant le déploiement.

### 1.4 Pourquoi aucun mécanisme automatique ne peut corriger cela

**Une fois un helper à son minimum, rien ne distingue « jamais initialisé » de
« réglé au minimum par l'utilisateur ».**

C'est **exactement** la limite d'origine non observable que le **§9.1 quater**
énonce pour l'état des besoins. Un amorçage automatique écraserait donc, tôt ou
tard, un réglage délibéré.

### 1.5 Ce qui remplace le mécanisme

**L'automatisation `10190000000006` est supprimée.**

**Une automatisation d'amorçage manuel `10190000000011` la remplace**, avec une
propriété structurelle : **sa clé `trigger` est vide**. Elle ne peut donc
**jamais** s'exécuter d'elle-même — ni au démarrage, ni sur changement d'état,
ni sur minuterie. Seule une action délibérée la déclenche.

> **Pourquoi une automatisation sans déclencheur plutôt qu'un `script`.** Le
> test 2 du contrat VMC interdit le terme `vmc_seuil` dans tout fichier de
> `10_scripts/vmc/`. Un script d'amorçage y contreviendrait par construction.
> **Plutôt que d'affaiblir une garde CI pour y loger mon propre code**, la
> forme retenue est une automatisation sans déclencheur — qui offre la même
> garantie, et une de plus : l'absence de déclencheur est **vérifiable**, et
> elle l'est (VINIT-001).

Elle publie une notification listant ce qu'elle a écrit.

**Elle n'a pas été exécutée.** Aucune valeur n'a été écrite dans le runtime par
ce lot.

### 1.6 Impact sur la décision et la commande

**Aucune logique métier n'est modifiée.** La machine, l'agrégation, la commande
et les relais sont inchangés — vérifié : le diff ne touche ni
`haute_vitesse_requise.yaml`, ni les machines de besoin, ni `gestion_auto.yaml`,
ni les scripts.

Après exécution de l'amorçage, `binary_sensor.vmc_haute_vitesse_requise`
retrouvera le comportement calibré : `OFF = borne(A − B·T_ext)` dans `[50, 70]`,
entrée à 74 % ou sur montée de 5 points au-dessus du plancher.

---

## 2. Défaut d'affichage — la doctrine UI n'avait pas été lue

`00_documentation_arsenal/ui/` contient **27 documents normatifs**, dont
`pattern_dashboard.md` (*référence UI officielle*), `pattern_dashboard_reglages.md`
(*normatif — opposable*) et onze fiches `socle_ui/`.

**Aucun n'a été consulté avant L7.7.** C'est la cause commune des deux défauts
d'affichage.

### 2.1 Réglages — les grilles à 3 colonnes

Aucun autre dashboard de réglage du dépôt ne dépasse **2 colonnes** ; la plupart
n'emploient **aucune grille**. À 3 colonnes, une tuile à contrôle
`numeric-input` tombe sous ~160 px en colonne masonry : libellés tronqués,
boutons tassés.

**Correction** : tuiles **une par ligne**, groupées par `sub_section_header`,
libellés portant leur unité.

> **Les `tile` sont conservées, et c'est la doctrine qui l'impose.** Le §🟩 du
> pattern réglages en fait la forme « par défaut et suffisante » pour l'édition
> d'un Seuil, et le §🚫 range le « remplacement massif des tile natives » parmi
> les **non-objectifs**. Les remplacer aurait été une faute, pas une
> amélioration.

**Deux manques réels comblés** : la carte **« effet réel »** que le §🔎 rend
**obligatoire** pour un Seuil dont l'effet n'est pas lisible — c'est le cas
ici, la frontière étant modulée — est externalisée dans
`includes/cartes/vmc/`, **seule convention du dépôt** ; et le bandeau est bien
adossé à `parametres_invalides_global`, comme le §✅ l'exige.

### 2.2 Diagnostic — trois cartes `entities`

Sur les **13 dashboards de diagnostic** du dépôt, **VMC était le seul** à
employer `type: entities` — 3 cartes ajoutées par L7.7, totalisant 26 lignes
dont 18 attributs à libellés longs, tronqués sous 500 px et sans hauteur
contractuelle.

**Correction** : remplacement par `custom:button-card` sur **templates et socles
existants**, sans en créer aucun :

| Objet | Template réutilisé |
|---|---|
| État d'un besoin | `carte_etat_interprete` |
| Conditions d'entrée / maintien / libération | `carte_attribut_categoriel_interprete` |
| Frontière modulée + plancher en label | `socle_kpi_label_72` |
| Grandeur modulante | `socle_info_72` |
| Statut de l'axe météo | `carte_capteur_etat_textuel` |
| Intégrité et bande morte | `carte_etat_interprete`, `socle_info_72` |

**Hiérarchie plutôt que mur de cartes** : le détail *maintien / libération* d'un
besoin n'a de sens que lorsqu'il est **actif** ; il est donc placé sous un
`conditional`, autorisé par `pattern_dashboard.md`. Au repos, chaque besoin
n'occupe que deux cartes.

**Couleurs** : palette déclarée **au site d'appel**, conformément à la doctrine ;
aucune couleur décorative ; une valeur catégorielle non mappée tombe sur le
**gris indisponibilité**, seul repli autorisé.

---

## 3. Écart entre le texte UI et la pratique — consigné, non tranché

`pattern_dashboard.md` liste `entities` 🟩 **Autorisé** et `markdown` 🟩
**Autorisé**.

**La pratique est plus stricte** : 13 dashboards de diagnostic sur 13
n'emploient que `custom:button-card` et des conteneurs structurels ; un seul
`markdown` inline existe dans tout le corpus diagnostic.

> **Ce lot applique la pratique et garde la pratique.** Il ne modifie pas la
> doctrine : **l'aligner relève d'un arbitrage propriétaire**, non d'un
> correctif.

Deux issues possibles, à arbitrer : restreindre le texte pour qu'il dise ce que
la pratique fait, ou assumer que `entities` demeure admis là où la pratique ne
l'emploie pas.

---

## 4. Gardes CI ajoutées

| Garde | Objet | Preuve négative |
|---|---|---|
| **VINIT-001** | l'amorçage **n'a aucun déclencheur** | un déclencheur ajouté fait échouer le checker |
| **VINIT-002** | **aucune automatisation VMC** ne conditionne un paramètre à `unknown`/`unavailable` — prédicat structurellement inopérant | motif détecté, et **pas de faux positif** sur un `sensor` |
| **VINIT-004** | table d'amorce **complète** : tout helper déclaré y figure | un helper manquant fait échouer |
| **§UI (a)** | **aucune carte native** dans le diagnostic VMC | ✅ établie |
| **§UI (b)** | **aucune grille > 2 colonnes** dans les réglages VMC | ✅ établie |

Le checker `check_vmc_initialisation_contracts.py` **change d'objet** : il
vérifiait le comportement d'un mécanisme ; il garde désormais **son absence**.

---

## 5. Ce que ce lot ne fait pas

- il **n'écrit aucune valeur** dans le runtime — l'amorçage est manuel et **n'a
  pas été exécuté** ;
- il **ne modifie aucune logique métier** : machine, agrégation, commande et
  relais sont inchangés ;
- il **ne modifie pas le contrat** ;
- il **ne modifie pas la doctrine UI** — l'écart texte / pratique est consigné,
  pas tranché ;
- il **ne recalibre rien** : les amorces demeurent celles de la passe 5,
  **provisoires et révisables** ;
- il **ne crée aucun template UI** — la doctrine exige une preuve de
  répétition, non réunie.

---

## 6. Ce qu'il reste à faire, et qui vous revient

1. **déployer** ce correctif dans `/config` ;
2. **exécuter l'amorçage** — automatisation « VMC - Amorçage manuel des
   paramètres », bouton *Exécuter* — **sur votre seule instruction** ;
3. **vérifier** que `binary_sensor.parametres_invalides_vmc` repasse à `off` et
   que la notification d'amorçage apparaît.
