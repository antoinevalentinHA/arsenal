# CONTRAT ARSENAL — ASPIRATEUR
## 12 — Identifiants à fournir

**Version contrat :** v1.0
**Statut :** Normatif — **inventaire de rôles, sans valeur**
**Objet :** Recenser les objets Arsenal dont le futur runtime aura besoin, sous
leur **rôle abstrait**, et acter qu'**aucune valeur n'est proposée**.

---

## 1. Règle

> **`ASP-INV-58` — aucun identifiant inventé.** Ce contrat **ne propose aucune**
> valeur d'`entity_id`, de nom de helper, de nom de script, de nom d'automation
> ni d'ID d'automation. Chaque ligne ci-dessous décrit un **rôle** ; son
> identifiant est **attribué par l'opérateur** au lot runtime, conformément aux
> doctrines de nommage et d'identification.

Les rôles sont notés `‹…›`, convention du domaine
([`README.md`](README.md) §Convention).

---

## 2. Rôles à instancier — **identifiants à fournir**

### 2.1 Intention

| Rôle | Ce qu'il porte | Nature attendue |
|---|---|---|
| `‹intention_carte›` | La carte désignée par l'opérateur | Entrée opérateur, valeurs bornées au référentiel V1 |
| `‹intention_segments›` | Les pièces désignées, de cette carte | Entrée opérateur, sélection multiple bornée au référentiel |
| `‹intention_profil›` | Le profil demandé, parmi les cinq arrêtés | Entrée opérateur, valeurs bornées |
| `‹intention_passages›` | `×1`, `×2` ou `×3` | Entrée opérateur, valeurs bornées |

> Ces quatre rôles portent **l'intention opérateur**, jamais l'état de l'appareil
> (`ASP-INV-16`).

### 2.2 Exécution

| Rôle | Ce qu'il porte |
|---|---|
| `‹moteur_de_mission›` | L'écrivain unique : validation, séquence, émission, qualification ([`07`](07_moteur_de_mission.md)) |
| `‹conduite_pause›` · `‹conduite_arret›` · `‹conduite_retour_base›` | Les gestes de conduite, encapsulés par le moteur ([`07`](07_moteur_de_mission.md) §7) |
| `‹conduite_reprise›` | La **reprise** d'une mission en pause. Seul rôle du domaine autorisé à émettre `vacuum.start`, sous la garde fermée de `ASP-INV-62` ([`07`](07_moteur_de_mission.md) §7.1) — jamais session close |
| `‹preselection_perimetre›` | Le préremplissage d'un périmètre prédéfini, sans écrivain propre ([`10`](10_raccourcis.md)) |

### 2.3 Verdict et diagnostic

| Rôle | Ce qu'il porte |
|---|---|
| `‹verdict_de_mission›` | Le résultat de la validation : autorisée, ou refusée avec son code ([`09`](09_refus_et_diagnostics.md)) |
| `‹motif_lisible›` | La justification humaine alignée sur le code de refus ou d'échec |
| `‹etat_canonique›` | L'état du domaine parmi les huit du chapitre [`08`](08_etats_et_observation.md) |
| `‹derniere_intention_lancee›` | La trace de l'intention effectivement émise — jamais relue depuis l'appareil (`ASP-INV-15`) |

---

## 3. Ce qui n'est **pas** à fournir

| Objet | Statut |
|---|---|
| **Entités natives Roborock** | **Déjà existantes et observées** — elles ne sont ni à créer ni à renommer. Leur usage est borné par `ASP-INV-31`. |
| **Areas Home Assistant** | Aucune création, aucune modification (`ASP-INV-8`) |
| **Mappage area ↔ segment** | Sans objet pour la voie retenue |
| **Entités désactivées du registre** | Aucune réactivation n'est exigée par ce contrat au-delà de celles déjà réalisées ; le domaine ne dépend d'aucune entité désactivée |
| **Entrée `recorder`** | Aucune ([`08`](08_etats_et_observation.md) §6) |
| **Checker CI** | Aucun — lot ultérieur |

---

## 4. Discipline d'attribution

Au lot runtime, l'attribution des identifiants respecte les doctrines
transverses :

- [`nommage_entites.md`](../../architecture/03_doctrines/nommage_entites.md) —
  nommage par **représentation**, jamais par calcul ;
- [`id_automatisations.md`](../../architecture/03_doctrines/id_automatisations.md) —
  système normatif des IDs d'automatisations ;
- [`prefixe_domaine_automatisations.md`](../../architecture/03_doctrines/prefixe_domaine_automatisations.md) —
  contrat préfixe d'ID ↔ domaine propriétaire ;
- [`entetes_fichiers.md`](../../architecture/03_doctrines/entetes_fichiers.md) —
  en-tête de fichier comme contrat local.

> **`ASP-INV-59`** — Le **préfixe d'ID d'automation** du domaine `aspirateur`
> n'est **pas attribué** par ce contrat : son attribution relève de la doctrine
> ci-dessus et d'un geste opérateur. Aucune valeur n'est suggérée ici.

---

## Renvois

- Moteur de mission : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Refus et diagnostics : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Index du domaine : [`README.md`](README.md)
