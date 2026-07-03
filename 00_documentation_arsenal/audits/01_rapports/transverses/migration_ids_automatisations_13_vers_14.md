# 🔧 ARSENAL — MIGRATION : IDs d'automatisations legacy 13 → 14 chiffres (reprise AID-006)

> **Statut** : opération préparée, exécution runtime Home Assistant **en attente**.
> **Date de préparation** : 2026-07-03.
> **Nature** : reprise de dette de format, exceptionnelle, tracée, atomique.
> **Non opposable en soi** : la norme reste la doctrine [`architecture/03_doctrines/id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md) (§ Exception tracée). Ce document trace *l'opération*, pas la règle.

---

## 🎯 Objet

Migration des **58 identifiants d'automatisations legacy à 13 chiffres** (préfixe 4 + suffixe 9) vers le **format canonique à 14 chiffres** (préfixe 4 + suffixe 10), aligné sur le générateur `script.generate_next_id_from_prefix` (`'%010d'`).

Déclencheur : le contrat CI `AID-006` (cf. `scripts/arsenal_contracts/check_automation_ids_contracts.py`, introduit en PR #251) remonte cette dette en INFO non bloquant.

## 🧭 Décision & mandat

L'invariant doctrinal « un ID ne change jamais après création » **demeure**. Une **exception unique** a été explicitement décidée par le propriétaire pour cette reprise de format, à condition d'être déterministe, sans réattribution métier, et atomique. Voir la clause d'exception dans la doctrine.

## 🧱 Mapping déterministe

```
OLD (13) = PPPP + s9
NEW (14) = PPPP + 0 + s9      (insertion d'un « 0 » après le préfixe)
exemple  : 1015000000001 → 10150000000001
```

- Aucun nouveau préfixe, aucune réattribution métier, aucun ID inventé ou incrémenté.
- Mapping **injectif** ; l'espace entier des suffixes du générateur est **inchangé** (`int("000000001") == int("0000000001")`), donc `generate_next_id_from_prefix` n'est pas affecté.

## 📦 Périmètre (58 IDs, 75 fichiers de dépôt + 2 documents)

| Catégorie | Fichiers | Nature |
|---|---|---|
| Automations — `id:` + en-têtes | 58 | cœur de la migration |
| Automations — références inter-fichiers | 2 | `climatisation/ventilation/application_mode.yaml`, `eclairage/jardin/soir/mouvements_sejour.yaml` |
| CI (contrats couplés) | 3 | `check_alarme_contracts.py`, `check_voiture_contracts.py`, `resilience_integrations_registre.yaml` |
| Templates | 2 | `climatisation/ventilation/diagnostic.yaml`, `eclairage/jardin/soir/off.yaml` |
| Helpers | 3 | `07_input_datetimes/eclairage/*` |
| Docs vivantes / normatives | 7 | `architecture/eclairage_jardin.md`, `contrats/{alarme/50_intrusion_detection, climatisation/12_ventilation_intention, climatisation/14_recommandation_ventilation, electromenager, pannes/secteur/11_temporalite, voiture}.md` |
| Documents ajoutés | 2 | clause d'exception (doctrine) + le présent rapport |

Total remplacements : **154** (151 lignes ; 3 lignes portent 2 IDs).

## 🔒 Collisions — aucune (vérifié)

- Aucun NEW n'existe déjà dans le corpus (0/58).
- Mapping injectif (aucun doublon interne).
- Aucune ambiguïté d'espace-entier parmi les IDs existants.

## ✂️ Méthode — remplacement exact, jamais `sed`

Remplacement à **frontière de chiffres** `(?<!\d)OLD(?!\d)` sur une whitelist explicite de racines. Justification impérative : le legacy `1016000000002` est le préfixe des 13 premiers caractères du canonique `10160000000022` — un `sed`/sous-chaîne corromprait des IDs canoniques voisins. Périmètre excluant `audits/` et `changelog/`.

## 🗂️ Références : migrées vs préservées

- **Migrées** (vivantes) : contrats CI, docs normatives (`architecture/`, `contrats/`), templates, helpers, commentaires d'en-tête runtime — y compris l'en-tête opérationnel `# CHANGELOG` de `voiture.md` et `voiture/autonomie.yaml`.
- **Préservées** (historique réel, **non réécrites**) : `00_documentation_arsenal/audits/**`, `00_documentation_arsenal/changelog/**`, et la **ligne de changelog datée** `contrats/electromenager.md:122` (`| 1.0 | 2026-06-07 | Création… |`).
- **Hors périmètre par nature** : `logbook.yaml` et le bouton dashboard imprimerie ciblent les automations par **slug** (dérivé de l'alias, inchangé), pas par `id` — non modifiés, non impactés tant que les slugs sont préservés.

## 🏠 Risque Home Assistant & procédure runtime

**Fait structurant** : pour une automation YAML, `id` = `unique_id` d'entité. Changer l'`id` crée une nouvelle entité et orpheline l'ancienne (risque `automation.*_2`, perte `last_triggered`/traces). Aucune automation/script/template ne lit l'**état** d'une automation legacy → **pas de cascade** ; seules les 58 sont inertes pendant la fenêtre.

**Procédure nominale retenue — fenêtre transitoire « 58 absentes » (courte, surveillée)** :
1. Sauvegarde HA complète ; alarme **désarmée**, maison occupée, hors créneaux planifiés, pas de coupure secteur.
2. Déploiement d'un état transitoire **local, jamais mergé/poussé** où les 58 automations sont absentes.
3. Reload complet → les 58 entités deviennent orphelines/indisponibles.
4. Suppression **via l'UI** des 58 entités orphelines (libère les slugs).
5. Déploiement de la configuration **complète migrée** → reload.
6. HA recrée les 58 avec des **slugs propres** (aucun `_2`).
7. Vérifs : aucune `automation.*_2`, aucune indisponible persistante, bouton `automation.imprimerie_stock_archivage_hebdo` OK, `logbook.yaml` de nouveau alimenté.

Coût **assumé** : `last_triggered`/traces des 58 repartent de zéro. Édition manuelle de `.storage/core.entity_registry` = **recours exceptionnel**, hors chemin nominal.

## ✅ Vérifications réalisées (isolées, dépôt principal intact)

Migration appliquée dans un `git worktree` jetable puis contrôlée :
- `check_automation_ids_contracts.py` : **263 canoniques, 0 legacy, 0 ERROR, 0 INFO**.
- `check_alarme_contracts.py`, `check_voiture_contracts.py`, `check_resilience_integrations_contracts.py` : **exit 0** (identiques à `main`).
- Reliquat legacy hors historique : **seule** `electromenager.md:122` subsiste (préservation voulue).
- Historique `audits/` + `changelog/` : **intact**.

## ↩️ Rollback

- Avant merge : vérif en échec → correction sur branche.
- Après merge, CI rouge : `git revert` du commit atomique.
- Runtime : si nettoyage UI insuffisant → redéployer l'état complet migré + reload (renommer d'éventuels `_2`) ; snapshot HA en dernier recours.

## 🔜 Suite

Après validation runtime, **second lot séparé** : durcissement du contrat `AID-006` en **ERROR** (longueur 14 exigée) pour interdire toute régression 13 chiffres.
