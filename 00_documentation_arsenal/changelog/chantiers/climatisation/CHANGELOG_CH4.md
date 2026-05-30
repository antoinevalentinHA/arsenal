# Arsenal CI — Changelog du chantier CH-4

**Chantier** : CH-4 — Fermeture de la topologie d'appel de la couche d'Application Chauffage
**Domaine** : Chauffage
**Date** : 2026-05-30
**État** : clos — 136 tests verts, verdict R-CALL-1 conforme, 0 modification du runtime Chauffage

---

## Résumé architectural

CH-4 ferme l'ensemble des appelants légitimes de la couche d'Application
Chauffage (`script.chauffage_appliquer_consigne`). Le contrat fondateur de
souveraineté d'exécution instituait cette couche et interdisait tout accès
matériel hors chaîne officielle, mais ne **nommait pas** les entités autorisées à
l'invoquer : un appelant tiers pouvait apparaître sans rupture visible. CH-4
comble cet angle mort (dette D7).

Le chantier livre trois résultats indissociables : un **amendement normatif** qui
énumère les appelants légitimes et pose leur classification doctrinale ; un
**invariant CI structurel** (`R-CALL-1`) qui garde mécaniquement cette
énumération ; et une **troisième région d'analyse** du validateur,
`tools/arsenal_ci/execution/`, parallèle et étanche aux deux étages existants. La
topologie d'appel de la frontière d'exécution est désormais **énumérée, fermée et
surveillée** — sans aucune modification du runtime, des contrats existants, de
l'étage 1 template ni de l'étage 2 décision.

---

## 1. Gouvernance d'exécution

Résultats portés par l'amendement `10_souverainete_execution__amendement.md`,
subordonné au contrat fondateur `10_souverainete_execution.md`.

### Fermeture de la topologie d'appel
L'ensemble des invocateurs légitimes de la couche d'Application est désormais
**fini et énuméré** dans le contrat : `decision_centrale`,
`retry_transactionnel/declenchement` et `modification_consigne`. Objectif métier :
transformer une frontière implicite (« qui peut appliquer une consigne ? ») en un
ensemble explicite, opposable et vérifiable.

### Distinction autorité décisionnelle / ré-applicateurs bornés
Le contrat distingue deux **natures** d'appelant. L'**autorité décisionnelle**
(`decision_centrale`) produit une décision thermique nouvelle et l'applique. Les
**ré-applicateurs bornés** (`retry_transactionnel`, `modification_consigne`)
rejouent exclusivement une intention déjà décidée et mémorisée, sans aucun mandat
de décision autonome. Objectif métier : reconnaître les seconds appelants comme
conformes à la souveraineté de la décision sans leur concéder le pouvoir de
décider — un retry et une réapplication de consigne ne sont pas des décisions.

### Clause de fermeture (numerus clausus)
Tout invocateur non énuméré constitue une **rupture de souveraineté
d'exécution**. L'ajout d'un appelant exige un **amendement explicite** du contrat,
jamais un simple ajout runtime ; le déplacement d'un appelant contractualisé est
traité comme un retrait. Objectif métier : interdire l'apparition silencieuse
d'un nouveau chemin d'exécution et faire de toute extension une décision
documentée.

### Prédicat de ré-application
Le mandat des ré-applicateurs est borné par contrat : rejouer une intention déjà
mémorisée, n'émettre aucune raison décisionnelle nouvelle, ne jamais écrire la
mémoire de décision, ne contenir aucune logique de décision. Objectif métier :
qualifier précisément ce que « ré-appliquer » autorise et interdit — étant
entendu que ce prédicat reste contractuel (cf. §2, périmètre exclu).

---

## 2. Invariant CI — R-CALL-1

### Rôle
`R-CALL-1` est l'invariant qui garde mécaniquement l'énumération du §1. Il scrute
les **sites d'appel** de `script.chauffage_appliquer_consigne` dans les arbres
`10_scripts/chauffage/` et `11_automations/chauffage/`, et compare l'ensemble des
fichiers porteurs d'un appel à l'allow-list contractuelle. Objectif métier :
rendre la clause de fermeture exécutable, et non seulement déclarative.

### Garanties apportées
Deux familles de verdict. Un fichier hors allow-list portant un appel de la cible
produit une **violation bloquante** nommant le fichier fautif. Un appelant
contractualisé qui n'appelle plus la cible produit un **avertissement de
divergence** contrat ↔ runtime. Objectif métier : détecter aussi bien
l'apparition d'un appelant illégitime que la péremption d'un appelant déclaré —
les deux faces d'une topologie qui mentirait.

### Liaison contrat ↔ constante
L'allow-list de l'invariant est le **miroir mécanique** de l'énumération
normative du contrat, délimitée dans celui-ci par des sentinelles dédiées. Un
méta-test vérifie en permanence l'égalité entre la constante et l'énumération
contractuelle. Objectif métier : empêcher toute dérive entre la vérité métier (le
contrat, autorité) et sa transcription exécutable (la constante, miroir).

### Périmètre volontairement exclu
`R-CALL-1` vérifie la **topologie d'appel**, pas le **prédicat de
ré-application**. La nature de la `raison` rejouée, la lecture de l'intention
déjà décidée et l'absence d'écriture de la mémoire de décision restent des
exigences **contractuelles non vérifiées en CI** dans ce chantier. Objectif
métier : tenir une frontière nette entre ce que la machine garde et ce que le
contrat exige, sans sur-spécifier un invariant fragile.

### Frontière d'erreur
Une entrée illisible (syntaxe YAML invalide) remonte en **erreur d'exécution**,
jamais en violation : un juge défaillant est distingué d'une configuration
fautive. Les tags Home Assistant inconnus sont tolérés, le scan couvrant des
fichiers tiers du sous-arbre sans rapport avec la topologie d'appel. Objectif
métier : un invariant qui ne se fait jamais passer pour ce qu'il n'est pas.

---

## 3. Intégration CI

### Troisième analyseur parallèle
CH-4 établit la région `tools/arsenal_ci/execution/`, dotée de son propre point
d'entrée (`cli_execution`) et d'un job GitHub Actions dédié `execution`,
conditionné au self-test et publiant un artifact JSON. Codes de sortie 0/1/2
identiques aux deux autres régions. Le job est armé en phase warn-only :
`R-CALL-1` signale sans bloquer, l'erreur d'exécution bloque dans toutes les
phases. Objectif métier : porter le verdict de topologie en intégration continue
selon la même discipline que les étages existants.

### Séparation avec l'étage 1 template
La frontière d'exécution est un analyseur **distinct** de l'étage 1 structurel.
Le jeu de règles de l'étage 1 (`orchestrator.RULES`) reste inchangé ; aucune
fonction de la région `execution` n'y est câblée, et un test d'isolation le
vérifie. L'étage 1 analyse la composition des template sensors ; CH-4 analyse les
sites d'appel des automatisations et scripts. Objectif métier : ne pas
contaminer le graphe template avec une analyse de nature différente.

### Séparation avec l'étage 2 décision
La frontière d'exécution est également distincte de l'étage 2. L'étage 2 normalise
et vérifie la **cascade de décision** (couverture, synchronie, non-remontée
conséquence → cause, iso-comportement) ; CH-4 vérifie la **topologie d'appel** de
la couche qui exécute cette décision. `R-CALL-1` ne recoupe ni `R-COV-1`, ni
`R-MIRROR-1`, ni `R-CAUSE-1`, ni `R-ISO-1`. Objectif métier : trois régions, trois
objets de vérité disjoints, aucune redondance doctrinale.

---

## 4. Garanties obtenues

### Désormais impossible sans rouge CI
- Introduire un appelant de `script.chauffage_appliquer_consigne` hors des trois
  fichiers contractualisés, dans les arbres scriptés et d'automatisation du
  domaine Chauffage.
- Laisser diverger l'allow-list exécutable de l'énumération normative du contrat
  (méta-test contrat ↔ constante).
- Voir un appelant contractualisé cesser d'appeler la cible sans signalement
  (avertissement de divergence inverse).
- Faire passer une entrée illisible pour une configuration conforme (erreur
  d'exécution bloquante en toutes phases).

### Ce qui reste contractuel et hors vérification
- Le **prédicat de ré-application** lui-même : qu'un ré-applicateur rejoue bien une
  intention déjà décidée, n'émette pas de raison décisionnelle nouvelle et
  n'écrive pas la mémoire de décision. Ces exigences sont opposables par contrat,
  non gardées par `R-CALL-1`.
- Les **invocations non résolues statiquement** : appel construit dynamiquement,
  ou invocation indirecte ne portant pas la cible en valeur d'appel. Ces limites
  sont documentées et assumées, jamais masquées.
- Un appelant **hors des arbres scrutés** (autre domaine) : résiduel documenté,
  non gardé, la cible étant chauffage-spécifique.

---

## 5. Hors périmètre

CH-4 ne touche ni ne duplique trois domaines voisins.

### Mécanique transactionnelle MQTT
La corrélation `request_id`, les états d'ACK, le plafond de tentatives et
l'annulation sur relance amont restent **intégralement régis** par le contrat
`boiler/retry_transactionnel.md`. L'amendement y renvoie explicitement et ne
redéfinit rien. Objectif métier : une seule autorité par objet, pas de doctrine
dupliquée.

### Logique de décision
Aucune règle ni branche décisionnelle n'est ajoutée, retirée ou réordonnée. La
Décision Centrale demeure l'unique autorité thermique ; CH-4 ne fait que clore
l'ensemble de ceux qui peuvent exécuter ses décisions.

### Runtime Chauffage
Aucun fichier de `10_scripts/chauffage/`, `11_automations/chauffage/` ni
`12_template_sensors/chauffage/` n'est modifié. La topologie d'appel existante est
décrite et fermée telle qu'elle est, jamais altérée.

---

## État de validation

- 136 tests Arsenal CI verts (lots 1.x, 2.x, et nouvelle famille 3.x).
- Verdict `R-CALL-1` conforme sur le runtime : aucun appelant illégitime, aucune
  divergence inverse.
- Verdict étage 2 (`cli_decision`) conforme : non-régression confirmée.
- Job `execution` intégré au workflow Chauffage en phase warn-only.

---

## Réalisation sans modification du runtime Chauffage

CH-4 a été réalisé **sans aucune modification de la configuration Home Assistant
Chauffage**. La cascade de décision, ses miroirs, la composition d'autorisation et
les automatisations d'exécution sont restés intacts. L'étage 1 template et
l'étage 2 décision sont demeurés inchangés. L'ensemble du chantier est confiné à
l'outillage (`tools/arsenal_ci/execution/`), à ses tests, à l'amendement
contractuel et au workflow CI.

---

## Clôture du chantier CH-4

CH-4 est clos. La couche d'Application Chauffage possède désormais un ensemble
d'appelants **énuméré, classé et fermé** par contrat, et `R-CALL-1` garde cette
fermeture en intégration continue, étanche aux étages 1 et 2. La dette D7 est
soldée : la frontière d'exécution n'est plus implicite.

Le chantier laisse une frontière explicite vers son armement : `R-CALL-1` opère en
phase warn-only ; sa bascule en mode bloquant est un diff unique et traçable, à
décider lorsque la surveillance de la topologie devra devenir une non-régression
définitive. Le prédicat de ré-application demeure une exigence contractuelle, dont
la mise éventuelle sous garde mécanique relèverait d'un chantier ultérieur.
