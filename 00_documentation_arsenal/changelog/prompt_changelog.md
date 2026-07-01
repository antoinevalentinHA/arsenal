# Procédure — Rédaction d'un changelog Arsenal

Cette procédure décrit **comment produire un changelog de release Arsenal** :
le déclenchement, les entrées, le mode opératoire pas à pas, le format
attendu, puis les **règles de rédaction** (style, ton, format du texte).

Elle s'applique à partir :
- d'un diff de release,
- d'un digest,
- ou d'une liste de fichiers modifiés.

---

## 1. Nature et déclenchement

- Un changelog Arsenal = **une release sauvegardée par l'opérateur**, pas un
  journal de commit.
- Les fichiers `changelog/changelogs/vXX/*.md` et leurs entrées dans
  `changelog/index.md` sont des **sauvegardes release**.
- **Déclenchement (obligatoire).** La rédaction est engagée **uniquement**
  quand l'opérateur :
  1. dépose les diffs de release dans `changelog/diffs_temporaires/`, **et**
  2. demande explicitement la rédaction du changelog.
- **Ne jamais fabriquer ni numéroter un changelog de sa propre initiative**
  pour acter un changement (même runtime). Hors du déclenchement ci-dessus,
  un changement livré se trace via le **commit de merge / la PR** dans les
  contrats et la ligne de clôture du registre (`REGISTRE_CHANTIERS.md`),
  jamais via un changelog inventé.

---

## 2. Entrées

Déposées par l'opérateur dans `changelog/diffs_temporaires/` :

- `vX__to__vY.md` — diff de release détaillé. Son **entête** porte les
  snapshots `From` / `To` (nom horodaté + sha) : la **date du changelog = date
  du snapshot `To`**.
- `vX__to__vY__digest.md` — digest statistique (fichiers ajoutés/modifiés,
  top domaines, top fichiers). Sert à cadrer la volumétrie et les domaines.

Ces fichiers sont **temporaires** : ils sont supprimés en fin de procédure
(cf. §3, étape 10).

---

## 3. Mode opératoire

1. **Lire les règles de rédaction** (§5 de ce document).
2. **Lire le digest** (volumétrie, domaines, fichiers) puis **le diff complet**.
3. **Lire le dernier changelog gelé** de la série (`changelogs/vNN/`) pour caler
   le format exact (sections par domaine + « Fichiers impactés »).
4. **Lire la section de la série** dans `changelog/index.md` : format d'entrée
   et emplacement d'insertion.
5. **Lire le contenu réel de chaque fichier AJOUTÉ** que le diff ne montre pas
   (fichiers nouveaux souvent listés sans corps) : décrire le runtime exact
   (entités, ids, gardes), sans paraphraser des commentaires YAML.
6. **Déterminer la date** = date du snapshot `To` de l'entête du diff.
7. **Créer** `changelogs/vNN/vNN_X_Y.md` (format §4).
8. **Ajouter l'entrée d'index** dans `changelog/index.md`, après la version
   précédente et **avant** le bloc `FIN INDEX` (format §4).
9. **Ne pas toucher `historique.md`** : c'est un récit rétrospectif par phases ;
   les versions correctives / mineures en sont volontairement exclues.
10. **Vérifier** :
    - `python scripts/docs_lint/docs_lint.py --exceptions scripts/docs_lint/docs_lint_exceptions.txt`
    - `python scripts/docs_lint/docs_ci_changelog_index.py` (contrôle complet en
      contexte PR).
11. **Supprimer les fichiers** de `changelog/diffs_temporaires/` (fichiers de
    travail ; conserver le dossier, zone de dépôt des prochains diffs).
12. **Livrer** via branche dédiée → PR → checks verts → squash-merge →
    suppression de la branche → nettoyage local.

---

## 4. Format des livrables

### 4.1 Fichier changelog `vNN_X_Y.md`

Un **unique bloc Markdown**, directement intégrable, structuré ainsi :

```md
# Changelog Arsenal — vX.Y.Z

_Date : JJ/MM/AAAA_

---

# Domaine

## Sous-section

- modification
- modification
- impact concret

---

# Fichiers impactés

## Catégorie

- fichier
- fichier
```

Catégories usuelles de « Fichiers impactés » : `Ajoutés`, `Supprimés`,
`Modifiés — runtime`, `Modifiés — Lovelace`, `Modifiés — contrats et
documentation`, `Modifiés — checkers`, `Modifiés — changelog`, adaptées au
contenu réel de la release.

### 4.2 Entrée d'index (`changelog/index.md`)

Insérée après la version précédente, avant `FIN INDEX`, précédée d'un `---` :

```md
## 🧠 ARSENAL HA — [vNN.X.Y](changelogs/vNN/vNN_X_Y.md) — STABLE — AAAA-MM-JJ
**Tags :** tag, tag, tag

**Signal net :**
- domaine — changement concret (entités / fichiers / comportements)
- …
```

- La date de l'entête d'index est au format `AAAA-MM-JJ`.
- **Signal net** : 4 à 6 puces, une par grand axe de la release.
- **Tags** : vocabulaire existant de l'index (domaines et natures).

---

## 5. Règles de rédaction

### 5.1 Objectif

Le changelog doit être :

- technique,
- factuel,
- traçable aux diffs,
- directement exploitable,
- lisible rapidement.

Il ne doit PAS devenir :
- une documentation,
- un manifeste architectural,
- un article technique,
- un commentaire philosophique du système.

### 5.2 Style

Le ton doit être :

- sobre,
- compact,
- professionnel,
- concret.

Le changelog NE DOIT PAS :

- raconter une histoire,
- extrapoler une vision système,
- inventer des doctrines,
- « vendre » la release,
- interpréter des intentions,
- dramatiser les changements.

Préférer :

```text
- remplacement de X par Y
- ajout de robustesse au redémarrage
- migration vers deadline persistante
- clarification du contrat
```

Éviter :

```text
- maturité architecturale
- philosophie système
- doctrine renforcée
- approche conceptuelle
- vision Arsenal
- paradigme
- stratégie
```

### 5.3 Ton rédactionnel

Le changelog doit utiliser un ton :

- neutre,
- impersonnel,
- technique,
- sobre,
- proche d'un audit Git ou d'une note de release industrielle.

Éviter les formulations :
- emphatiques,
- littéraires,
- journalistiques,
- marketing,
- ou « consultant ».

Éviter notamment :
- matérialisation
- pipeline événementiel
- alignement visuel
- gouvernance
- purge
- brique
- stratégie
- paradigme
- orchestration
- industrialisation
- robustesse doctrinale
- lecture système
- couche métier
- composante native
- implémentation directe d'une invariante

Préférer :

```text
- ajout de
- suppression de
- déplacement de
- renommage de
- remplacement de
- correction de
- clarification de
- mise à jour de
- ajout d'un trigger
- suppression d'un helper
- ajout d'un capteur
- ajout d'une garde
```

### 5.4 Adjectifs

Limiter fortement les adjectifs qualificatifs.

Éviter :
- complète
- robuste
- définitive
- stricte
- totale
- intégrale
- majeure
- avancée
- enrichie
- étendue
- renforcée

Sauf si le diff démontre explicitement cette propriété.

Préférer :
- description factuelle du changement,
- sans qualification inutile.

### 5.5 Pas de synonymes pompeux

Éviter les formulations abstraites ou administratives
quand une description simple existe.

Éviter notamment :
- formalisation
- concrétisation
- rationalisation
- convergence
- stabilisation
- optimisation globale
- montée en charge
- convergence documentaire

Préférer :
- ajout de
- déplacement de
- renommage de
- suppression de
- mise à jour de

### 5.6 Longueur des phrases

Privilégier :
- phrases courtes,
- une idée par ligne,
- listes à puces,
- formulations directes.

Éviter :
- les phrases longues,
- les propositions multiples,
- les explications imbriquées,
- les parenthèses explicatives longues.

### 5.7 Référence de style

Le style attendu est proche :
- d'un changelog GitHub technique,
- d'une release note d'équipe infra,
- d'un journal de migration industriel.

Le style attendu n'est PAS proche :
- d'un article Medium,
- d'une RFC complète,
- d'un ADR détaillé,
- d'un billet d'architecture.

### 5.8 Règle majeure

Tout ce qui est écrit doit être :
- visible dans les diffs,
- ou directement déductible techniquement.

Ne jamais :
- inventer des concepts,
- inventer des patterns,
- inventer des intentions produit,
- transformer une implémentation en doctrine.

### 5.9 Contrats / doctrines

Les fichiers de doctrine, architecture ou contrat doivent être décrits simplement :

```text
- ajout du contrat X
- déplacement du document Y
- clarification des règles de nommage
- ajout de documentation sur la gestion du temps
```

Pas de :
- « formalisation philosophique »
- « cadre doctrinal »
- « modèle architectural renforcé »

même si les fichiers concernés parlent de doctrine.

### 5.10 Automatisations

Décrire :
- le comportement réel,
- les changements de logique,
- les mécanismes de robustesse,
- les nouveaux helpers,
- les changements de triggers,
- les changements de persistance.

Exemple acceptable :

```text
- remplacement des temporisations `for:` par des deadlines persistantes
- ajout du rattrapage post-redémarrage Home Assistant
- ajout du rattrapage post-rechargement des automatisations
```

Exemple interdit :

```text
- nouveau paradigme temporel
- résilience événementielle
- orchestration temporelle robuste
```

### 5.11 Refactorings

Tu peux mentionner :
- restructuration,
- clarification,
- simplification,
- homogénéisation,
- harmonisation.

Mais uniquement si le diff le montre clairement.

### 5.12 Niveau de détail

Le changelog doit :
- synthétiser les vrais changements,
- éviter de paraphraser les commentaires YAML,
- éviter de recopier les contrats,
- rester plus court que les fichiers modifiés.

Préférer :
- listes courtes,
- vocabulaire simple,
- impacts techniques concrets.

### 5.13 Éviter les redondances

Ne pas répéter plusieurs fois la même idée
avec des formulations différentes.

Regrouper les changements fortement liés.

Mauvais :

```text
- ajout du helper X
- ajout du trigger X
- ajout de l'automatisation X
```

Bon :

```text
Ajouts :
- helper X
- trigger X
- automatisation X
```

### 5.14 Priorité aux changements concrets

Toujours privilégier :
- les entités,
- les fichiers,
- les triggers,
- les helpers,
- les IDs,
- les comportements runtime,
- les changements visibles.

Éviter les formulations abstraites quand une formulation concrète existe.

Mauvais :

```text
- amélioration de la robustesse temporelle
```

Bon :

```text
- ajout d'un trigger `homeassistant.start`
- ajout d'un helper `input_datetime`
- remplacement d'un `for:` par une deadline persistante
```

### 5.15 Préférer les objets concrets

Préférer :
- les noms d'entités,
- les fichiers,
- les automatisations,
- les helpers,
- les triggers,
- les dashboards,
- les contrats.

Éviter de remplacer des objets concrets par :
- pipeline
- couche
- flux
- orchestration
- projection
- composant métier
- mécanisme systémique

### 5.16 Pas d'explication détaillée

Le changelog décrit :
- ce qui change,
- éventuellement l'effet concret,

mais ne doit pas expliquer en détail :
- le raisonnement,
- la théorie,
- l'architecture interne,
- les invariants,
- le fonctionnement complet du système.

Le lecteur est supposé :
- connaître le domaine,
- ou lire les contrats associés si nécessaire.

### 5.17 Pas d'effet d'importance

Ne pas suggérer qu'un changement est :
- majeur,
- structurant,
- critique,
- central,
- important,
- stratégique,

sans preuve explicite dans les diffs.

Éviter :
- « nouveau domaine majeur »
- « introduction complète »
- « version structurante »
- « basculement »
- « montée en maturité »

Décrire simplement :
- les fichiers ajoutés,
- les entités ajoutées,
- les comportements modifiés.

### 5.18 Interdiction de résumer l'architecture

Le changelog ne doit pas :
- résumer le système,
- expliquer la philosophie du domaine,
- décrire les couches Arsenal,
- expliquer les invariants globaux,
- expliquer la doctrine métier.

Même si ces éléments apparaissent dans les contrats.

Le changelog décrit uniquement :
- les modifications introduites par la release.

### 5.19 Pas de contexte redondant

Ne pas réexpliquer le contexte fonctionnel
si le nom du domaine, du fichier ou de l'entité
le rend déjà évident.

Éviter :

```text
Dans le cadre du système météo...
Le domaine de supervision NAS...
Le pipeline d'auto-supervision...
```

Préférer :

```text
Ajout de :
- `sensor.audit_stale`
- `sensor.pluie_journaliere`
- `binary_sensor.vmc_conformite_decision`
```

### 5.20 Pas de commentaire sur la qualité du changement

Le changelog ne doit pas qualifier le changement comme :
- propre,
- élégant,
- cohérent,
- mature,
- fiable,
- intelligent,
- bien structuré.

Le changelog décrit le changement.
Il ne l'évalue pas.

### 5.21 Contrôle final

Si une phrase ressemble :
- à une analyse,
- à une philosophie,
- à un manifeste,
- à un billet de blog,
- à une présentation produit,

→ elle doit être supprimée ou simplifiée.

Le changelog doit donner l'impression :
- d'un audit technique de release,
- pas d'une narration.
