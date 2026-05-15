# Arsenal Search — Vision de domaine

**Domaine** : Outils externes / NAS Arsenal / Recherche
**Date de figeage** : 2026-05-13
**Statut** : Actif
**Documents enfants** :
- `contrat_webapp.md` — service Flask/Docker
- `contrat_moteur_cli.md` — moteur `ha_search.py`

---

## Objet

Arsenal Search fournit un moteur de recherche à la demande dans les versions Home Assistant extraites automatiquement par le pipeline NAS timeline.

Le système vise à remplacer les scripts locaux PC de recherche d'entités Home Assistant et permet une consultation depuis :

- PC,
- mobile,
- navigateur web,
- réseau local ou VPN.

Arsenal Search n'est pas limité à la recherche d'entités Home Assistant. Il constitue un moteur général de recherche et d'audit textuel Arsenal.

---

## Source de données

La recherche s'appuie exclusivement sur :

```text
/volume1/Backups_HA/ha_backup_timeline/versions/
```

Ce périmètre est déjà filtré en amont par la doctrine patrimoine/runtime du pipeline timeline : `versions/` ne contient ni backups bruts, ni Emergency Kit, ni `.storage`, ni bases SQLite, ni logs, ni runtime Zigbee2MQTT.

Arsenal Search hérite de ce filtrage : il n'a pas à le redéfinir, mais il s'engage à ne jamais sortir du périmètre.

---

## Principe architectural

```text
Home Assistant
  → backups chiffrés
  → NAS timeline
  → versions extraites
  → Arsenal Search
  → navigateur PC / mobile
```

Arsenal Search appartient exclusivement à la couche outillage / audit.

Le moteur ne produit aucune décision Home Assistant.

---

## Séparation des responsabilités

| Composant          | Responsabilité                      |
| ------------------ | ----------------------------------- |
| Timeline extractor | Extraction des sauvegardes          |
| Diff engine        | Génération des diffs inter-versions |
| `ha_search.py`     | Moteur de recherche borné           |
| Flask UI           | Présentation HTML et export Markdown |
| Docker             | Isolation runtime                   |
| VPN / LAN          | Contrôle d'accès réseau             |

La couche web ne décide rien, ne parse pas la logique métier Arsenal, ne modifie jamais les données. Elle orchestre, présente et encapsule. Le moteur CLI reste l'autorité fonctionnelle.

---

## Invariants

Contrats durs du domaine. Toute évolution doit les préserver.

- **Lecture seule** : Arsenal Search ne modifie jamais les versions extraites, ni Home Assistant, ni la timeline. Cet invariant s'applique aussi à l'export Markdown, généré en mémoire et jamais persisté sur le NAS.
- **Périmètre borné** : la recherche est strictement confinée à `ha_backup_timeline/versions/`. Aucun chemin hors de ce volume n'est lisible.
- **Aucun shell libre** : l'utilisateur saisit une requête, jamais une commande. La requête n'est jamais interprétée comme une commande système.
- **Aucune exposition publique** : accès LAN ou VPN uniquement. Aucun reverse-proxy public, aucun QuickConnect.
- **Résultats bornés** : nombre de résultats, profondeur de contexte et durée de recherche sont plafonnés et non négociables côté client.
- **Isolation Docker** : le service web monte `versions/` et `ha_search.py` en lecture seule et n'a aucun autre accès au NAS.
- **Autorité moteur** : la webapp ne réimplémente jamais la logique de recherche. Toute recherche passe par `ha_search.py`. L'export Markdown encapsule le stdout du moteur sans le parser, sans le reformater et sans l'agréger.

---

## Architecture par phases

### Phase 1 — Moteur backend CLI

- Outil interne NAS uniquement.
- Non destiné à un usage mobile ni quotidien.
- Usage : maintenance, validation, mise au point du moteur, audits ponctuels depuis le NAS.
- Ne suppose aucune ouverture SSH permanente : utilisé pendant les fenêtres de maintenance.

La Phase 1 valide la logique de filtrage, la grammaire de requête et les bornes de résultats avant emballage en service.

### Phase 2 — Interface utilisateur webapp

- Vraie interface utilisateur.
- Service Docker local sur NAS.
- Accessible PC et mobile, LAN ou VPN.
- C'est la cible d'usage réelle du domaine.

La Phase 1 n'est pas une interface utilisateur. Toute consultation utilisateur passe par la Phase 2.

---

## Fonctions v1

### Recherche

- recherche texte simple,
- insensible à la casse par défaut,
- option casse stricte,
- option regex,
- recherche dans la dernière version,
- recherche dans une version spécifique,
- recherche multi-versions.

### Gestion de la documentation Arsenal

La documentation Arsenal (`00_documentation_arsenal/`) peut être incluse, exclue ou ciblée seule.

```text
mode normal      → inclut la documentation
--exclude-docs   → exclut 00_documentation_arsenal/
--docs-only      → recherche uniquement dans 00_documentation_arsenal/
```

`--exclude-docs` est destiné aux recherches métier/runtime afin d'éviter le bruit documentaire.

`--docs-only` est destiné aux audits de documentation, contrats et changelogs.

### Export Markdown

Les résultats d'une recherche peuvent être téléchargés sous forme de document Markdown.

```text
recherche interactive  → affichage HTML (/search)
export markdown        → téléchargement .md (/export)
```

L'export Markdown produit une **enveloppe minimale** autour du stdout exact du moteur CLI : un en-tête de paramètres, le stdout brut dans un bloc `text`, un footer d'identification. Aucune structuration ni reformatage du contenu de recherche.

Cas d'usage :

- conservation locale d'une recherche complexe,
- partage propre d'une investigation,
- archivage d'un audit ponctuel,
- exploitation des résultats hors interface web.

Invariants hérités du domaine :

- lecture seule (génération en mémoire, aucune écriture NAS),
- moteur borné (plafonds résultats / contexte / durée appliqués),
- autorité CLI (aucune logique grep dupliquée),
- aucune exposition publique (route locale comme `/search`).

Le détail du format, du nommage de fichier, des headers HTTP et des codes de retour est porté par `contrat_webapp.md`.

---

## Requêtes

Les requêtes sont du texte libre. Elles peuvent contenir :

```text
/  \  :  .  -  _  #  ()  []  {}
```

Exemples valides :

```text
00_documentation_arsenal/
11_automations/chauffage/
mdi:router-wireless
rgba(76, 175, 80, 0.2)
sensor.temperature_jardin
/volume1/Backups_HA/
```

La grammaire de requête est portée par la couche moteur. L'absence d'interprétation shell est garantie par le moteur (`subprocess` sans `shell=True`, requête passée en paramètre, jamais concaténée).

---

## Périmètre de fichiers

### Extensions recherchées

```text
.yaml  .yml  .json  .txt
.j2  .jinja  .jinja2
.md  .py  .js  .ts  .css  .html
```

Les fichiers binaires sont ignorés.

### Répertoires exclus (défense en profondeur)

```text
.storage/
.git/
__pycache__/
deps/
node_modules/
temp/
logs/
```

Ces répertoires ne sont en principe pas présents dans `versions/` (filtrage amont par la timeline). Leur exclusion côté Search est une garantie redondante.

---

## Bornes de résultats

| Paramètre | Valeur par défaut | Plafond dur |
|-----------|-------------------|-------------|
| Nombre de résultats | 200 | 2000 |
| Contexte (lignes) | 5 | 50 |
| Timeout requête | 10 s | 30 s |

En cas de troncature, la sortie l'indique explicitement (`résultats tronqués : N affichés sur M`). Cette indication est portée par le footer du moteur CLI et se retrouve telle quelle dans l'export Markdown.

---

## Sécurité

### Surface d'exposition

| Accès | Statut |
|-------|--------|
| LAN | autorisé |
| VPN | autorisé |
| Internet public | interdit |
| QuickConnect | interdit |
| Reverse-proxy public | interdit |

### Obligations du moteur

- toute recherche est exécutée via paramètres sécurisés (`subprocess` sans shell),
- la requête utilisateur n'est jamais concaténée à une ligne de commande,
- les chemins manipulés sont confinés au volume `versions/` (vérification d'appartenance avant lecture),
- les bornes de résultats et de timeout sont appliquées côté serveur, jamais côté client.

---

## Non-objectifs

Arsenal Search ne doit jamais :

- modifier Home Assistant,
- modifier les versions extraites,
- accéder aux backups bruts,
- accéder à l'Emergency Kit,
- exposer un terminal distant,
- exécuter des commandes arbitraires,
- remplacer Git,
- remplacer la timeline de backups.

---

## Évolutions futures

- sélection graphique de version,
- recherche multi-version avec groupement,
- export markdown structuré (par version / fichier / match),
- lien direct vers fichier/résultat,
- comparaison grep entre deux versions,
- recherche de dépendances d'entités,
- graphe de consommation entité → fichier.

L'export Markdown structuré supposerait une sortie structurée du moteur CLI (par exemple `--output-format json`, listée comme compatibilité Phase 2 dans `contrat_moteur_cli.md`). Tant que le moteur produit uniquement un flux texte, l'export reste une enveloppe minimale sans interprétation.

---

## Cas d'usage typiques

- retrouver une entité,
- auditer un refactor,
- identifier une introduction de capteur,
- retrouver une dépendance,
- analyser un contrat,
- comparer versions,
- retrouver un helper ou un dashboard,
- suivre une dette technique,
- archiver une investigation sous forme de document Markdown.

---

## Gouvernance

Toute évolution majeure doit être tracée dans le changelog Arsenal et dans le présent document.

Toute extension augmentant la surface réseau, les privilèges, les capacités d'exécution, l'exposition WAN ou les possibilités d'écriture doit faire l'objet d'une revue de sécurité explicite.

---

## Amendements

### v1.0 — 2026-05-08

- Création initiale du domaine.
- Pipeline timeline → diff → recherche.
- Interface web Flask Dockerisée.
- Accès LAN/VPN sur port 8099.
- Moteur borné, consultation read-only du patrimoine Arsenal.
- Phase 1 CLI validée.
- Phase 2 webapp opérationnelle.
- Accès SSH NAS refermé après mise en place.

### v1.1 — 2026-05-13

- Export Markdown des résultats intégré aux fonctions v1.
- Précision « structuré » ajoutée à l'évolution future correspondante pour distinguer la v1.1 (enveloppe minimale) d'une éventuelle évolution structurée ultérieure.
- Invariant *autorité moteur* précisé : l'export encapsule le stdout sans le parser, le reformater ou l'agréger.
- Invariant *lecture seule* précisé : s'applique aussi à l'export, généré en mémoire et jamais persisté.
- Détail technique du contrat porté par `contrat_webapp.md` v1.1.
