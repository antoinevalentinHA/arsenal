# Arsenal — Amorçage Claude Code

Ce fichier est un **pointeur d'amorçage**, pas une source de vérité. Il ne
redéfinit aucune règle métier, aucune doctrine Git, aucun statut de chantier,
et ne recopie aucune liste de checkers. En cas de divergence avec l'un des
documents cités ci-dessous, **le document cité prime toujours** sur ce fichier.

Objectif : permettre à une session Claude Code neuve de reconstruire l'état
réel du dépôt avant d'agir, puis de savoir où trouver — jamais deviner —
la règle applicable.

## 0. L'état Git réel, jamais un résumé

Ne jamais supposer l'état du dépôt depuis une mémoire de conversation ou un
résumé. Le reconstruire depuis le terrain avant toute intervention :

- branche courante, HEAD, propreté du working tree ;
- remote(s) et écart avec `origin/<branche courante>` **et** `origin/main` —
  un `main` local peut être périmé, ne jamais s'y fier seul ;
- clone superficiel (`--depth`) : si c'est le cas, aller chercher l'historique
  nécessaire avant de conclure quoi que ce soit sur des commits absents ;
- worktrees actifs — un travail en cours ailleurs ne doit pas être ignoré ni
  écrasé.

## 1. Point d'entrée documentaire canonique

Lire **en entier** [`00_documentation_arsenal/README.md`](00_documentation_arsenal/README.md),
en particulier sa section « Avant de proposer ou modifier — IA & contributeurs ».
Cette section route déjà, par type de modification, vers le contrat ou la
doctrine à lire et vers le(s) checker(s) CI applicable(s) : ne pas la
reformuler, ne pas la contourner.

## 2. Ce qui est réellement ouvert aujourd'hui

Lire [`00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md`](00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md)
(cockpit des chantiers). Si plusieurs chantiers sont des candidats plausibles
pour la tâche demandée, **ne pas trancher par supposition** : l'expliciter et
obtenir confirmation avant de patcher. Une tâche qui ne correspond à aucun
chantier existant n'a pas à en inventer un.

## 3. Contrat et doctrine du domaine réellement touché

Identifier le domaine par ce qui est effectivement modifié, jamais par
ressemblance de nom ou intuition, puis lire son contrat et sa doctrine
propres avant de patcher — jamais se fonder sur un fichier voisin. La table
de routage vit dans le document du point 1, pas ici.

## 4. Hiérarchie des sources

Un fait a un document propriétaire unique, une décision a un décideur unique
(principe posé dans [`architecture/03_doctrines/principes_generaux.md`](00_documentation_arsenal/architecture/03_doctrines/principes_generaux.md)).
En cas de divergence entre deux documents, le document propriétaire prime —
jamais le registre, jamais ce fichier.

## 5. Contrôles avant de conclure

Exécuter les checkers et gates identifiés au point 1 pour le domaine et le
type de fichier réellement touchés avant d'affirmer qu'un changement est
correct. Un sous-ensemble choisi a priori ne vaut pas preuve.

## 6. Mise à jour du registre et des artefacts

Un changement qui modifie l'état d'un chantier (ouverture, patch, clôture,
requalification) suit les règles de gouvernance déjà écrites en tête du
registre cité au point 2 (co-commit, identifiants attribués). Un changement
qui ne touche aucun chantier ne l'implique pas artificiellement.

## 7. Git ≠ runtime ≠ déploiement ≠ validation terrain

Un merge sur `main` ne met à jour ni le clone runtime, ni ce qui est chargé
dans Home Assistant, ni ce qui est validé en conditions réelles : quatre
états distincts, à qualifier séparément. Voir
[`architecture/03_doctrines/git.md`](00_documentation_arsenal/architecture/03_doctrines/git.md)
(frontière patrimoine / runtime) et la section « Déploiement » de
[`.github/pull_request_template.md`](.github/pull_request_template.md).

## 8. Avant de dire « terminé »

« Terminé » n'est ni « CI verte » ni « code écrit ». Vérifier les critères de
clôture réels de la source faisant foi, et la solvabilité des preuves
attendues (échelle L1–L5) via
[`architecture/03_doctrines/solvabilite_probatoire.md`](00_documentation_arsenal/architecture/03_doctrines/solvabilite_probatoire.md),
avant de l'affirmer.

## 9. Ce qui doit survivre à cette session

Toute décision, dette, réserve ou arbitrage nécessaire à une session future
doit être écrit dans le dépôt (document de chantier, contrat, ou registre
selon le point 6) — jamais seulement dans une réponse de chat ou une
description de PR.

---

Ce fichier n'est jamais mis à jour pour refléter un statut de chantier. Il ne
change que si l'amorçage lui-même doit évoluer.
