# CONTRAT_ARSENAL_SEARCH_WEBAPP

**Domaine** : Outils externes / NAS Arsenal / Recherche
**Date de figeage** : 2026-05-13
**Statut** : Actif
**Document parent** : `vision_domaine.md`
**Document frère** : `contrat_moteur_cli.md`

---

## Objet

Ce contrat fige les décisions d'architecture et de sécurité du service web Arsenal Search :

- stack technique,
- exposition réseau,
- isolation Docker,
- routes HTTP,
- validation serveur,
- séparation moteur / présentation,
- format d'export Markdown,
- invariants UI.

Il est opposable : toute implémentation qui dévie d'un point de ce contrat doit être soit corrigée, soit faire l'objet d'un amendement explicite.

---

## Place dans l'architecture Arsenal

```text
Arsenal Search (vision)
  └── Phase 1 — moteur backend CLI
        └── ha_search.py
  └── Phase 2 — webapp Docker              ← CE CONTRAT
        └── consommateur officiel du moteur CLI
```

La webapp est une couche de présentation. Elle orchestre, affiche et encapsule. Elle ne décide rien, ne réimplémente aucune logique de recherche.

---

## Invariants

Hérités du contrat parent. Rappelés ici parce qu'ils gouvernent toutes les décisions techniques qui suivent.

- **Lecture seule** : le service ne modifie jamais les versions extraites, ni Home Assistant, ni la timeline. Aucune écriture sur le NAS, y compris pour les exports.
- **Aucun shell libre** : la requête utilisateur n'est jamais interprétée comme une commande système.
- **Aucune exposition publique** : LAN ou VPN uniquement.
- **Résultats bornés côté serveur** : les bornes sont appliquées par le moteur CLI, jamais déléguées au client web.
- **Autorité moteur** : la webapp ne réimplémente jamais la logique grep. Toute recherche passe par `ha_search.py` via `subprocess`. L'export n'interprète pas, n'agrège pas et ne reformate pas le stdout du moteur.

---

## Stack technique

| Élément     | Technologie         |
| ----------- | ------------------- |
| Backend web | Flask               |
| Runtime     | Python 3.12         |
| Isolation   | Docker              |
| Recherche   | délégué à `ha_search.py` |
| Frontend    | HTML serveur, sans JS côté client |
| Déploiement | Docker Compose      |

---

## Isolation Docker

### Nom du service

```text
ha_search_web
```

### Volumes montés

| Chemin hôte | Chemin conteneur | Mode |
|-------------|-----------------|------|
| `/volume1/Backups_HA/ha_backup_timeline/versions` | `/versions` | `:ro` |
| `/volume1/Backups_HA/ha_backup_timeline/scripts/ha_search.py` | `/app/ha_search.py` | `:ro` |

Aucun autre montage. Le conteneur n'a aucun autre accès au NAS.

### Variables d'environnement

| Variable | Valeur par défaut |
|----------|------------------|
| `HA_SEARCH_VERSIONS_ROOT` | `/versions` |
| `HA_SEARCH_CLI` | `/app/ha_search.py` |
| `HA_SEARCH_TIMEOUT` | `15` |
| `HA_SEARCH_MAX_QUERY_LEN` | `200` |

### Port

| Paramètre | Valeur |
|-----------|--------|
| Port hôte | `8099` |
| Port conteneur | `8099` |
| Protocole v1 | HTTP local uniquement |
| HTTPS | hors champ v1 |

Justification HTTP v1 : LAN domestique = périmètre de confiance. VPN chiffre le trafic distant. Pas d'auth applicative, pas de cookie, pas de token, aucune exposition directe Internet.

---

## Exposition réseau

| Accès | Statut |
|-------|--------|
| LAN | autorisé |
| VPN | autorisé |
| Internet public | interdit |
| QuickConnect | interdit |
| Reverse-proxy public | interdit |

Le firewall DSM doit autoriser le port `8099` uniquement depuis LAN + VPN.

---

## Routes HTTP

| Route | Méthode | Rôle |
|-------|---------|------|
| `/` | `GET` | Formulaire de recherche vide |
| `/search` | `POST` | Exécution de la recherche + affichage des résultats |
| `/export` | `POST` | Exécution de la recherche + téléchargement Markdown |
| `/health` | `GET` | État minimal du service (JSON) |

Pas de route `/api/*` en v1. Pas de redirect-after-POST. Les résultats de `/search` sont affichés dans la même réponse que le POST.

### `/health` — format de réponse

```json
{
  "status": "ok",
  "versions_root": "/versions",
  "search_cli": "/app/ha_search.py",
  "versions_root_exists": true,
  "search_cli_exists": true
}
```

Les deux champs `*_exists` permettent de détecter un montage manquant sans ouvrir de session SSH.

---

## Formulaire de recherche

### Champs exposés

| Champ | Type | Défaut | Validation serveur |
|-------|------|--------|-------------------|
| `query` | text | — | non vide, strip, max 200 chars |
| `context` | checkbox | off | booléen |
| `latest` | checkbox | off | booléen |
| `exclude_docs` | checkbox | off | booléen |
| `docs_only` | checkbox | off | booléen |

### Contraintes

- `exclude_docs` et `docs_only` sont mutuellement exclusifs → rejet 400 si les deux sont cochés.
- La validation HTML5 (`required`, `maxlength`) améliore l'UX mais ne constitue jamais une frontière de sécurité. La validation serveur est l'autorité.

Les mêmes champs et les mêmes contraintes s'appliquent aux deux routes `/search` et `/export`.

---

## Codes HTTP de retour

| Cas | Code |
|-----|------|
| Résultat OK | 200 |
| Options incompatibles / query invalide | 400 |
| Exit code non nul du moteur | 502 |
| Timeout subprocess | 504 |

Les erreurs 502 et 504 sont remontées dans le corps HTML (bloc `error`) et visibles dans `docker logs ha_search_web`.

Pour la route `/export`, aucun fichier n'est livré en cas d'erreur. La réponse est exclusivement HTML.

---

## Intégration moteur

Le moteur est invoqué exclusivement via `subprocess.run()`, sans `shell=True`.

La requête utilisateur est passée en argument de liste, jamais concaténée à une chaîne de commande.

Le timeout subprocess est `HA_SEARCH_TIMEOUT` secondes (défaut : 15 s).

Le service est mono-worker (serveur Flask de développement, `CMD python3 /app/app.py`). Le lock threading interne est valide dans ce contexte. Toute migration vers Gunicorn multi-worker nécessite un inter-process lock ou une stratégie sans état partagé.

Les routes `/search` et `/export` partagent strictement le même mode d'invocation : mêmes flags, mêmes paramètres, mêmes garde-fous. Seul le traitement du stdout diffère (affichage HTML vs. encapsulation Markdown).

---

## Route `/export`

### Rôle

Encapsuler le stdout exact du moteur CLI dans un document Markdown minimal téléchargeable.

### Principe

`/export` ne réimplémente aucune logique de recherche. Elle :

1. valide les paramètres du formulaire selon les mêmes règles que `/search` ;
2. invoque `ha_search.py` via `subprocess.run()` avec les mêmes flags que `/search` ;
3. encapsule le stdout dans une enveloppe Markdown ;
4. retourne le fichier au navigateur en pièce jointe.

La webapp n'interprète pas, ne parse pas, ne reformate pas le stdout du moteur. Elle l'encapsule.

### Format de sortie

````markdown
# Arsenal Search — Résultats

- Requête : `<query>`
- Contexte : `oui` / `non`
- Latest seulement : `oui` / `non`
- Documentation : `incluse` / `exclue` / `seulement`
- Date export : `YYYY-MM-DD HH:MM`

```text
<stdout exact du moteur CLI, footer inclus>
```

---
Export généré par Arsenal Search
````

L'en-tête reflète les paramètres effectivement passés au moteur. Le bloc `text` contient le stdout intégral du moteur, footer du moteur compris (compteurs, durée, troncature éventuelle). Le footer Markdown identifie l'enveloppe, pas le contenu.

### Nommage du fichier

Format :

```text
arsenal_search_<slug>_<YYYY-MM-DD_HH-MM>.md
```

Règle de slugification de `<query>` :

- conversion en minuscules,
- caractères autorisés : `[a-z0-9_-]`,
- tout autre caractère remplacé par `_`,
- compression des `_` consécutifs,
- strip des `_` en début et fin,
- borne dure : 64 caractères maximum,
- si slug vide après nettoyage : `requete`.

Le slug est ASCII pur par construction.

### Headers HTTP

```text
Content-Type: text/markdown; charset=utf-8
Content-Disposition: attachment; filename="arsenal_search_<slug>_<timestamp>.md"
```

Pas de header `Content-Length` calculé en streaming. Le fichier étant borné en taille par les plafonds moteur (max 2000 résultats), il est généré en mémoire avant envoi.

### Codes HTTP — comportement spécifique

| Cas | Code | Livraison |
|-----|------|-----------|
| Résultat OK | 200 | fichier `.md` |
| Options incompatibles / query invalide | 400 | message inline HTML |
| Exit code non nul du moteur | 502 | message inline HTML |
| Timeout subprocess | 504 | message inline HTML |

Aucun fichier n'est livré en cas d'erreur, y compris timeout : un export tronqué silencieusement violerait l'invariant *résultats bornés* en présentant un document partiel comme une archive valide.

Cas de succès partiel avec troncature signalée par le moteur (`résultats tronqués : N affichés sur M` dans le footer du stdout) : le fichier **est** livré. La troncature est explicitement portée par le moteur dans le bloc `text` et reste lisible dans l'archive. Aucun traitement spécial côté webapp.

### Note d'implémentation : ANSI

Le moteur CLI désactive la coloration ANSI lorsque `stdout` n'est pas un TTY (`sys.stdout.isatty()`). Le stdout capturé par `subprocess.run(..., capture_output=True)` est par construction non-TTY. Le contenu reçu est donc monochrome ; aucune désinfection ANSI n'est requise côté export.

### Invariants préservés

- **Lecture seule** : aucun fichier n'est écrit sur le NAS. Le Markdown est généré en mémoire puis transmis dans la réponse HTTP.
- **Autorité moteur** : `/export` utilise exactement les mêmes paramètres et le même mode d'invocation que `/search`. Aucune logique grep n'est dupliquée.
- **Bornes serveur** : les plafonds du moteur (résultats, contexte, durée) s'appliquent intégralement. L'export ne contourne aucun garde-fou.
- **Aucun shell libre** : la requête utilisateur reste transmise au moteur via `subprocess.run(..., shell=False)`, en liste d'arguments.
- **Aucun état persistant** : pas d'historique d'export, pas de cache, pas de stockage.

### Compatibilité avec le contrat moteur CLI

Le contrat moteur CLI (v1.0) liste parmi ses non-objectifs : « export markdown structuré ». L'export Markdown défini par le présent contrat est **non-structuré** : il s'agit d'une enveloppe minimale autour du stdout exact. Aucune structuration sémantique (par version, par fichier, par match) n'est produite. La cohérence inter-contrats est préservée.

Toute évolution future vers un export structuré nécessiterait une sortie structurée du moteur CLI (par exemple un flag `--output-format json`, déjà listé comme compatibilité Phase 2 dans le contrat moteur) et un nouvel amendement explicite.

---

## Invariants UI

### La UI n'est pas la source de vérité

La UI présente, groupe, structure et améliore la lisibilité. Elle ne recalcule pas d'états, n'interprète pas les contrats Arsenal, ne reconstruit pas de dépendances métier.

Le texte produit par le moteur CLI est la vérité. La UI l'affiche, elle ne le parse pas. L'export l'encapsule, il ne le réécrit pas.

### Affichage des résultats

Les résultats de `/search` sont rendus dans un bloc `<pre>` avec la sortie brute du moteur. Pas de re-parsing, pas de reconstruction HTML structurée du contenu de recherche en v1.

### Gestion des erreurs

| Cas | Affichage |
|-----|-----------|
| Query vide | Message inline, refus immédiat |
| Options incompatibles | Message inline, refus immédiat |
| Timeout | "Recherche trop longue (> N s)" |
| Exit code non nul | Contenu stderr dans bloc `error` |
| `versions/` inaccessible | Géré par le moteur → stderr capturé |

Aucune stack trace exposée à l'utilisateur.

---

## Périmètre interdit au service

Le service ne doit jamais accéder à :

- système DSM,
- Docker runtime,
- `/etc`, `/proc`, `/root`,
- dossiers utilisateurs NAS,
- shell système,
- backups bruts,
- Emergency Kit,
- secrets.

---

## Logs

Les logs vont uniquement vers stdout/stderr Docker.

```bash
docker logs ha_search_web
```

Pas de répertoire `logs/` hôte en v1. Pas d'écriture applicative sur l'hôte.

---

## Non-objectifs v1

- authentification applicative,
- HTTPS,
- API publique JSON,
- historique de recherches,
- historique d'exports,
- stockage NAS des exports,
- export PDF, DOCX ou ZIP,
- export HTML,
- export structuré (par version / fichier / match),
- génération d'exports planifiée,
- édition de fichiers,
- navigation libre dans le filesystem,
- terminal distant,
- cache,
- index inversé,
- comparaison graphique entre versions.

---

## Gouvernance

Toute extension augmentant la surface réseau, les privilèges, les capacités d'exécution, l'exposition WAN ou les possibilités d'écriture doit faire l'objet d'une revue de sécurité explicite et d'un amendement à ce contrat.

---

## Amendements

### v1.0 — 2026-05-08

Création initiale :

- service Flask/Docker opérationnel sur port 8099,
- accès LAN/VPN validé,
- montages `:ro` `versions/` et `ha_search.py` actifs,
- codes HTTP 502/504 sur erreurs moteur,
- validation serveur active,
- accès SSH NAS refermé après mise en place.

### v1.1 — 2026-05-13

Ajout de la route `POST /export` :

- enveloppe Markdown minimale autour du stdout exact du moteur,
- champs identiques à `/search`,
- mêmes codes HTTP, mêmes invariants,
- aucune écriture sur le NAS,
- aucune logique grep dupliquée,
- cohérence inter-contrats préservée (l'export reste non-structuré, le moteur CLI exclut explicitement l'export structuré).

Précisions complémentaires apportées à cette occasion :

- non-objectifs v1 enrichis (export structuré, export PDF/DOCX/ZIP, export HTML, historique d'exports, génération planifiée, stockage NAS des exports),
- formulation explicite que `/search` et `/export` partagent strictement le même mode d'invocation moteur.
