# 🧠 ARSENAL — UI PATTERN CANONIQUE · Pattern Dashboard **Réglages**
#
# 📌 Statut :
# PROPOSITION — PRÊTE À VALIDATION
# (n'a pas encore force normative ; à valider avant opposabilité)
#
# 📌 Domaine :
# UI / Lovelace / Dashboards de réglage
#
# 📌 Portée :
# Spécialise `pattern_dashboard.md` pour la famille
# `18_lovelace/dashboards/reglages/**`. Doctrine **documentaire** :
# elle décrit ce que l'UI de réglage doit représenter, sans porter
# de logique runtime.
#
# ==========================================================


## 🎯 OBJET ET POSITIONNEMENT

`pattern_dashboard.md` fixe la **structure générale** de tout dashboard Arsenal
(racine `vertical-stack` unique, ordre badges → navigation → contenu, interdits
structurels). Ce document **ne le redéfinit pas** : il le **spécialise** pour les
dashboards de réglage.

Un dashboard de réglage est une **sous-vue d'édition de paramètres**, atteinte
depuis le dashboard métier via le badge `bouton_retour_badge_carre`. Sa fonction
est de **modifier des helpers** (`input_*`, `number`) avec lisibilité et sans
surprise.

> **Règle d'or réglages :** un dashboard de réglage rend explicite
> *ce que chaque paramètre fait* et *ce qu'il met en jeu*.
> Il n'est jamais une liste brute de helpers.

Ce document est une **doctrine documentaire UI**. Il **n'introduit aucune vérité
métier** et **aucune logique** : toute décision reste dans les contrats et le
runtime ; l'UI **observe et rend lisible** (cf. `README.md`).


---

## 🚫 NON-OBJECTIFS

Ce pattern n'autorise pas, et ne vise pas :

- ❌ le **remplacement massif** des `tile` natives Home Assistant ;
- ❌ une **refonte graphique générale** des dashboards de réglage ;
- ❌ la création d'un **nouveau template UI** sans **preuve de répétition** ;
- ❌ le **déplacement de logique métier** dans Lovelace.

Toute évolution qui franchirait l'une de ces lignes sort du périmètre de cette
doctrine et relève d'un arbitrage distinct.


---

## 🧱 TYPOLOGIE NORMATIVE DES RÉGLAGES

La typologie distingue **trois plans** qui ne se confondent pas.

### 1️⃣ Plan vue — bandeau de validité

Élément de **niveau vue** (et non de niveau réglage), placé en tête de flux.
Décrit en section ✅.

### 2️⃣ Plan réglage — classe principale (exactement une)

Tout réglage exposé porte **exactement une** classe principale, déterminée par
**la nature de l'édition** :

| Classe principale | Définition | Forme par défaut |
|-------------------|------------|------------------|
| **Courant** | Réglage simple, sans couplage fort | `tile` native (§🟩) |
| **Seuil** | Valeur numérique dont l'effet n'est pas évident en lecture directe | `tile` + carte « effet réel » (§🔎) |
| **Mode** | Choix exclusif (`input_select`) | `tile` + feature de sélection |
| **Action ponctuelle** | Déclenchement (`script`) : calibration, reset, recalcul | Socle d'action confirmé |
| **Maintenance** | Réglage technique réservé à l'entretien | Section terminale dédiée |

### 3️⃣ Plan transversal — qualificatif **Sensible** (surclassant)

**Sensible** n'est **pas** une classe principale : c'est un **qualificatif
transversal** qui peut s'ajouter à n'importe quelle classe principale.

> Lorsqu'un réglage est à la fois — par exemple — **Seuil**, **Mode** ou
> **Action** **et** Sensible, le qualificatif **Sensible surclasse** : il
> **impose** ses obligations (séparation + confirmation, §🔐) **par-dessus** la
> forme de la classe principale.

Un réglage a donc **une classe principale** et **au plus un** qualificatif
surclassant.

**Règles de typologie :**
- Chaque section est introduite par un `section_header` (ou
  `sub_section_header`) à emoji, conformément au checker `R-LL-HEADER-EMOJI-1`.
- Une même section **ne mélange jamais** un réglage Sensible avec des réglages
  courants.
- Un réglage de diagnostic ou de lecture seule **n'a pas sa place** ici : il
  relève de `dashboards/diagnostics/**`.


---

## 🟩 QUAND UNE `TILE` NATIVE EST ACCEPTABLE

La `tile` native est la forme **par défaut et suffisante** pour les classes
**Courant** et **Mode**, ainsi que pour la partie *édition* d'un **Seuil**.

| `tile` native suffisante | `tile` native insuffisante |
|--------------------------|----------------------------|
| Réglage **Courant** | Réglage **Sensible** (→ §🔐) |
| **Mode** (`input_select`) | **Seuil** dont l'effet n'est pas lisible (→ §🔎) |
| Bascule simple sans risque | **Action ponctuelle** `script` (→ socle confirmé) |
| Édition d'un Seuil **accompagnée** d'une carte effet | Réglage **ignoré** sans indication d'inactivité (→ §🟦) |

La `tile` **édite** ; elle n'explique jamais. Dès qu'un paramètre exige
explication, conséquence ou confirmation, la `tile` est **encadrée**, jamais
remplacée par un widget d'édition concurrent. Conserver une `tile` suffisante
est **conforme**, pas un compromis.


---

## 🔐 RÉGLAGES SENSIBLES — SÉPARATION & CONFIRMATION

Un réglage reçoit le qualificatif **Sensible** s'il remplit au moins un critère
opposable :

1. il modifie un comportement de **sécurité** (armement, délais d'alarme, rayon
   de zone, durée de sirène) ;
2. il a un effet **matériel direct** potentiellement coûteux ou risqué ;
3. il est **difficilement réversible** ou peut placer le système dans un état
   incohérent silencieux.

**Obligations (surclassent la classe principale) :**
- regroupement dans une **section distincte**, jamais entrelacé avec des
  réglages courants ;
- **confirmation explicite** de toute bascule/action (socle confirmé existant,
  ex. `socle_toggle_confirme`) ;
- en-tête portant un emoji de mise en garde **textuel/iconographique**
  (ex. 🛡️ / 🔐), **jamais** une couleur inventée (§🎨).

La sensibilité se traduit **d'abord** par la séparation et la confirmation,
**ensuite seulement** par l'iconographie.


---

## 🔎 STATUT DES CARTES MARKDOWN « EFFET RÉEL »

Une carte « effet réel » est une carte `markdown` qui **affiche la conséquence
calculée** d'un ou plusieurs seuils (p. ex. la température d'autorisation
résultant d'une consigne et d'un offset). Le motif existe déjà au runtime.

**Statut :**
- **obligatoire** pour tout réglage **Seuil** dont l'effet n'est pas
  immédiatement lisible à partir de la valeur seule ;
- **descriptive et non décisionnelle** : elle reformule une réalité, ne calcule
  **aucune** logique métier propre et n'est **jamais** une source de vérité ;
- en cas de donnée `unknown` / `unavailable`, elle affiche un état d'attente
  neutre et **ne masque pas** l'indisponibilité ;
- **secondaire** à l'entité : en cas de divergence, le runtime fait foi.

Tant qu'un template dédié n'est pas justifié par une **preuve de répétition**
(§🚫), la forme `markdown` est la forme **canonique et suffisante**.


---

## ✅ RÔLE DU BANDEAU DE VALIDITÉ

Chaque dashboard de réglage **devrait** exposer, en **tête du flux de
contenu**, un **bandeau de validité conditionnel** adossé à l'indicateur de cohérence
global existant (`binary_sensor.parametres_invalides_global`, via l'include
`alerte_configuration_invalide.yaml`).

**Doctrine du bandeau :**
- **conditionnel** : invisible quand la configuration est saine, visible
  uniquement en cas d'incohérence ;
- **sans vérité concurrente** : il consomme un indicateur déjà produit par le
  backend, il n'en fabrique aucun ;
- **seule** synthèse autorisée en tête de vue ; il ne porte ni édition ni action
  métier.

**Placement :** le bandeau est la première carte du **flux de contenu**. Dans
une vue Réglages **sans navigation interne**, il apparaît en première position
du `vertical-stack`. Dans une vue qui porte une **navigation interne** conforme
au pattern général (`badges → navigation → contenu`), cette navigation reste
prioritaire : le bandeau est placé **immédiatement après elle** et ouvre alors
le flux de contenu réglage.

Le bandeau répond à « ce que je règle ici est-il cohérent ? » à l'endroit même
où l'incohérence se crée.


---

## 🎨 COULEUR — RAPPEL CONTRAIGNANT

Ce document est **subordonné** à la charte `couleurs/`. Aucune dérogation.

- **Aucune couleur décorative.** Une couleur ne signale jamais « ceci est un
  réglage sensible » : la sensibilité se traduit par séparation + confirmation +
  icône, **pas** par une couleur inventée.
- Toute couleur affichée **traduit une réalité backend déjà calculée**, selon la
  hiérarchie sémantique (`couleurs/05_regles.md`).
- Le **gris indisponibilité** reste le seul fallback visuel autorisé pour un
  état non exploitable.


---

## 🟦 ÉTATS D'UN RÉGLAGE — ACTIF / DISPONIBLE / IGNORÉ / BLOQUÉ

Un réglage dont l'effet dépend d'un autre paramètre **ne doit pas** apparaître
comme actif quand il est inopérant.

**Moyens autorisés :**
- **structurel** : masquage / révélation conditionnel, ou regroupement sous
  l'interrupteur qui gouverne le réglage ;
- **indisponibilité réelle** : gris indisponibilité quand l'entité est
  effectivement `unavailable`.

**Interdit :** encoder « actif / ignoré » par une couleur sémantique inventée
non adossée à un état réel. La distinction est **structurelle** avant d'être
chromatique.


---

## 🧭 STRATÉGIE DE GÉNÉRALISATION PROGRESSIVE

La conformité s'installe **par vague**, jamais en refonte globale.

1. **Doctrine validée** (ce document) avant tout chantier runtime.
2. **Prototype mono-dashboard** : appliquer la typologie à **une seule** vue
   pilote (domaine déjà mature ou le plus à risque).
3. **Validation visuelle** mobile + desktop (alignement vertical, responsive,
   non-régression navigation / badges).
4. **Généralisation domaine par domaine**, en priorisant les vues à enjeu
   sécurité, puis les couples de seuils.
5. **Checker CI éventuel**, **uniquement après** stabilisation, dans la lignée
   des `check_lovelace_*` existants. Un checker ne fige jamais une convention
   immature.


---

## 🔒 RÈGLES DE CONFORMITÉ

Une fois cette proposition validée, un dashboard de `reglages/**` conforme :
- expose le **bandeau de validité conditionnel** en tête ;
- attribue à **chaque** réglage **une** classe principale et **au plus un**
  qualificatif surclassant **Sensible** ;
- limite la `tile` native aux classes **Courant / Mode** et à l'édition de
  **Seuil** ;
- accompagne tout **Seuil** non trivial d'une carte **effet réel** ;
- isole et **confirme** tout réglage **Sensible** ;
- ne distingue les états actif / ignoré que par des moyens **structurels** ou
  l'indisponibilité réelle ;
- n'introduit **aucune couleur décorative** ni vérité concurrente à un contrat.


---

## 🔚 CONCLUSION

Ce pattern fait du dashboard de réglage une **interface de confiance** : chaque
paramètre y est lisible, contextualisé et — lorsqu'il le faut — protégé. Il
s'appuie en priorité sur des **actifs déjà présents** et n'autorise un nouveau
composant que sous **preuve de répétition**.

> Arsenal ne pose plus des helpers.
> Arsenal expose des réglages gouvernés.

# ==========================================================
# 📌 Statut : PROPOSITION — prête à validation.
#    Autorité d'intégration : 00_documentation_arsenal/ui/.
# ==========================================================
