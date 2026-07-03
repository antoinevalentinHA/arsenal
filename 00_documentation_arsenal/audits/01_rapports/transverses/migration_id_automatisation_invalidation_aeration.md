# 🔧 ARSENAL — MIGRATION : ID automation « Aération - Invalidation tentative non confirmée » (correction de préfixe fautif)

> **Statut** : opération préparée, exécution runtime Home Assistant **en attente**.
> **Date de préparation** : 2026-07-03.
> **Nature** : correction exceptionnelle d'identité fonctionnelle, unique, décidée, tracée, atomique.
> **Non opposable en soi** : les normes restent le contrat [`architecture/03_doctrines/prefixe_domaine_automatisations.md`](../../../architecture/03_doctrines/prefixe_domaine_automatisations.md) et la doctrine [`architecture/03_doctrines/id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md). Ce document trace *l'opération*, pas la règle.

---

## 🎯 Objet

| | |
|---|---|
| **Automation** | « Aération - Invalidation tentative non confirmée » |
| **Fichier** | `11_automations/aeration/invalidation.yaml` |
| **Ancien ID** | `10170000000010` (préfixe `1017` — ouvertures) |
| **Nouvel ID** | `10010000000031` (préfixe `1001` — aeration) |

## 🧭 Justification & mandat

L'audit préfixe ↔ domaine ([`audit_prefixes_domaines_automatisations.md`](./audit_prefixes_domaines_automatisations.md), PR #255) a établi que cette automation est **fonctionnellement pure aération** (déclencheur, conditions et écriture exclusivement sur les faits `aeration_*`) et qu'elle est documentée comme pièce du socle aération par les contrats mêmes qui la référencent. Le préfixe `1017` (ouvertures) est donc une **erreur d'identité fonctionnelle**, pas une exception admissible (contrat, § Principe fondamental et § Interdictions).

L'invariant doctrinal « un ID ne change jamais après création » **demeure**. La correction a été **explicitement arbitrée par le propriétaire** (validation de l'audit, 2026-07-03) comme opération exceptionnelle, seule du corpus (256/263 conformes ; 5 exceptions assumées au registre `scripts/arsenal_contracts/prefix_domain_exceptions.yaml` ; aucun autre ID modifié). Elle ne crée **aucun précédent**.

## 🧱 Attribution du nouvel ID

`10010000000031` réplique le calcul doctrinal de `script.generate_next_id_from_prefix` : suffixes existants du préfixe `1001` dans le corpus déclaré = {22, 23, 24, 25, 26, 29, 30} → `max + 1 = 31`, zero-pad 10. Les trous de numérotation (1–21, 27–28) ne sont **pas** réutilisés (interdiction de recyclage).

## 🔒 Collisions — aucune (vérifié)

- `10010000000031` : **0 occurrence** dans le dépôt avant opération (`git grep`).
- Corpus : 263 IDs, tous uniques (contrat AID vert avant et après).
- Aucune ambiguïté de sous-chaîne à frontière de chiffres avec un ID existant.

## ✂️ Méthode & références migrées

Remplacement **exact à frontière de chiffres** `(?<!\d)10170000000010(?!\d)` (jamais de `sed` naïf), sur les **3 fichiers vivants** — 4 lignes :

| Fichier | Lignes |
|---|---|
| `11_automations/aeration/invalidation.yaml` | en-tête + `id:` |
| `contrats/aeration_blocage_chauffage/socle_transversal/10_invalidation_tentative_non_confirmee.md` | 1 |
| `contrats/aeration_blocage_chauffage/socle_transversal/12_tentative_aeration_en_grace.md` | 1 |

**Préservés** (constats datés, non réécrits) : le rapport d'audit PR #255 et `audits/index.md`, qui citent l'ancien ID comme état observé. Aucune mention dans `changelog/`. Aucune référence dans `10_scripts/`, `12_template_sensors/`, `18_lovelace/`, `19_button_card_templates/`, `scripts/arsenal_contracts/`, `.github/`, `logbook.yaml`.

## 🏠 Impact Home Assistant

Pour une automation YAML, **`id` = `unique_id`** d'entité : le changement crée une nouvelle entité et orpheline l'ancienne (risque de slug `automation.*_2`, perte `last_triggered`/traces — coût assumé, 1 seule entité). Le slug `automation.aeration_invalidation_tentative_non_confirmee` n'est **référencé nulle part** (alias inchangé) : aucune cascade, aucun consommateur d'état.

## 🗓️ Procédure runtime prévue (séparée de la PR Git, après merge)

1. État transitoire **local, jamais commité** : retrait de `11_automations/aeration/invalidation.yaml` → reload automations.
2. Suppression **via l'UI** de l'ancienne entité orpheline (libère le slug).
3. Retour sur `main` complet (nouvel ID) → reload automations.
4. Vérifications : aucune `automation.*_2`, entité active sous slug propre, aucun résidu indisponible.

Conditions : fenêtre calme, `aeration_episode_en_cours` off, sauvegarde HA disponible.

## ↩️ Rollback

- Avant merge : correction sur branche.
- Après merge, CI rouge : `git revert` du commit atomique.
- Runtime : redéploiement de l'état antérieur + reload ; renommage manuel d'un éventuel `_2` ; snapshot HA en dernier recours.

## 🔗 Lien contractuel

Cette opération est la **conséquence d'exécution** du contrat préfixe ↔ domaine (§ Interdictions, pt 4 : toute mise en cohérence identité/propriété passe par une exception explicitement décidée, documentée et localisée, sur le modèle de méthode AID-006). Elle clôt le seul cas « probablement fautif » de l'audit. `id_automatisations.md` n'est **pas modifié** : la clause AID-006 y reste l'unique exception datée, et le présent rapport trace la présente opération sans créer de règle.
