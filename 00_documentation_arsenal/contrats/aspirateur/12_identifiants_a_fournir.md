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
| `‹etat_canonique›` | L'état du domaine parmi les **dix** du chapitre [`08`](08_etats_et_observation.md), `‹mission_ouverte›` étant rendu séparément (`ASP-INV-68`) |
| `‹derniere_intention_lancee›` | La trace de l'intention effectivement émise — jamais relue depuis l'appareil (`ASP-INV-15`) |

> **`ASP-INV-70` — vocabulaire de cycle de vie du verdict, fermé et distinct.**
> Le rôle `‹verdict_de_mission›` porte, **en plus** des codes du catalogue
> ([`09`](09_refus_et_diagnostics.md)), un **ensemble fermé de valeurs de cycle
> de vie** : elles disent **où en est** la demande — validation engagée, issue
> non établie, commande prise en charge, démarrage observé — là où un code dit
> **pourquoi** elle n'aboutit pas.
>
> **Ces deux vocabulaires ne se confondent jamais.** Une valeur de cycle de vie
> n'est **ni un refus ni un échec** : elle n'entre pas au catalogue, et
> l'inscrire y ferait croire à un motif qui n'existe pas. Réciproquement, un
> code du catalogue ne décrit **jamais** une étape.
>
> **L'ensemble est arrêté par le lot runtime et gardé par la CI.** Ce contrat
> n'en propose aucune valeur — `ASP-INV-58` s'applique sans réserve. Il exige
> seulement que l'ensemble soit **fermé**, **énuméré au runtime**, et
> **mécaniquement confronté** : une valeur écrite hors de cet ensemble est une
> non-conformité, au même titre qu'un motif de refus hors catalogue
> (`ASP-INV-52`).

---

## 3. Ce qui n'est **pas** à fournir

| Objet | Statut |
|---|---|
| **Entités natives Roborock** | **Déjà existantes et observées** — elles ne sont ni à créer ni à renommer. Leur usage est borné par `ASP-INV-31`. |
| **Areas Home Assistant** | Aucune création, aucune modification (`ASP-INV-8`) |
| **Mappage area ↔ segment** | Sans objet pour la voie retenue |
| **Entités désactivées du registre** | Aucune réactivation n'est exigée par ce contrat au-delà de celles déjà réalisées ; le domaine ne dépend d'aucune entité désactivée |
| **Entrée `recorder`** | Aucune ([`08`](08_etats_et_observation.md) §6) |
| **Helper temporel** | **Aucun.** Les deux fenêtres du domaine sont des **constantes de contrat** écrites littéralement dans le moteur ([`07`](07_moteur_de_mission.md) §3.1, `ASP-INV-69`) : aucun `input_number`, aucune entité et aucun paramètre d'appel ne les porte. |
| **Checker CI** | Étendu au lot d'intégrité normative — aucun nouveau checker à fournir |

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
