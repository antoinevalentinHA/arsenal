# Plan d'action — Corrections P1 anomalies Arsenal

> **Nature :** plan d'action documentaire et de nommage.
> **Périmètre :** anomalies P1 issues de l'audit README et du registre transverse.
> **Source :** `audits/registre_anomalies_transverses.md`.
> **Statut initial :** toutes les étapes sont **en attente** sauf indication contraire.

---

## Vue d'ensemble

| Étape | Objet | Type | Fichiers impactés | Dépend de |
|---|---|---|---|---|
| **0** | Déposer le registre d'anomalies | Création | 2 | — |
| **1** | `30_decision_centrale.md` — références mortes | Édition | 1 | — |
| **2** | `10_temporalite.md` → `11_temporalite.md` | Renommage | 2 | — |
| **3** | `guard_expostion_ha.md` → `guard_exposition_ha.md` | Renommage | 4 | — |
| **4** | `01__objet_perimetre_statut.md` → `01_objet_perimetre_statut.md` | Renommage | 2 | — |
| **5** | `contrats/README.md` — description P2 | Édition | 1 | — |
| **6** | Rerouter 6 renvois `resilience_electrique` → `pannes/secteur/` | Édition | 4 | Étape 2 (ordre) |

Toutes les étapes 1–4 sont **indépendantes** et peuvent être produites en parallèle.

---

## Étape 0 — Déposer le registre transverse

### Objectif

Rendre disponible dans le dépôt le registre des anomalies connues et non corrigées.

### Fichier à créer

```
00_documentation_arsenal/audits/registre_anomalies_transverses.md
```

Le fichier est déjà rédigé (généré lors de la session d'audit).

### Modification induite — `audits/index.md`

Ajouter une section transverse à la fin du fichier, avant le bloc `---` final :

```markdown
## Transverse

- [registre_anomalies_transverses.md](registre_anomalies_transverses.md)
  _(registre vivant — anomalies connues et non corrigées, toutes origines)_
```

### Commit suggéré

```
docs(audits): add cross-domain anomaly register
```

---

## Étape 1 — Corriger `30_decision_centrale.md`

### Objectif

Supprimer deux références mortes dans l'en-tête du contrat :
- `CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` (nom uppercase obsolète)
- `AUDIT_CHAINE_MQTT_ACK_ECS.md` (supprimé en v12.3, "audit soldé")

### Fichier impacté

```
00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
```

**Ligne 8 — actuel :**
```
**Références boiler :** `contrats/boiler/CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` · `outils_externes/boiler_pi/AUDIT_CHAINE_MQTT_ACK_ECS.md`
```

**Ligne 8 — proposé :**
```
**Références boiler :** `contrats/boiler/socle_transactionnel.md`
```

### Aucune dépendance entrante sur ce passage.

### Commit suggéré

```
fix(contrats/chauffage): remove stale boiler refs in 30_decision_centrale
```

---

## Étape 2 — Renommer `10_temporalite.md` → `11_temporalite.md`

### Contexte

`contrats/pannes/secteur/` contient deux fichiers avec le préfixe `10_` :
- `10_socle.md`
- `10_temporalite.md`

`20_chauffage_et_ecs.md` occupe déjà le rang 20. Le rang `11_` s'insère proprement.

### Opération principale

```bash
git mv 00_documentation_arsenal/contrats/pannes/secteur/10_temporalite.md \
       00_documentation_arsenal/contrats/pannes/secteur/11_temporalite.md
```

### Références à mettre à jour

**Fichier :** `contrats/pannes/secteur/10_socle.md`

Ligne 159 — actuel :
```
| Exclusion des micro-coupures | Confirmation temporelle obligatoire → `10_temporalite.md` |
```
Proposé :
```
| Exclusion des micro-coupures | Confirmation temporelle obligatoire → `11_temporalite.md` |
```

> Ligne 49 du même fichier référence
> `/00_documentation_arsenal/architecture/resilience_electrique/10_temporalite.md`
> — chemin mort vers un dossier inexistant. **Anomalie distincte, hors périmètre de cette étape.**
> Voir section "Anomalie connexe" en fin de document.

### Hub navigation

`navigation/domaines/pannes.md` pointe vers `contrats/pannes/secteur/` (dossier),
sans lien direct vers `10_temporalite.md`. **Aucune modification nécessaire.**

### Commit suggéré

```
fix(contrats/pannes): rename 10_temporalite → 11_temporalite, fix ref in 10_socle
```

---

## Étape 3 — Renommer `guard_expostion_ha.md` → `guard_exposition_ha.md`

### Contexte

Typo dans le nom de fichier (`expostion` au lieu de `exposition`).
`changelog/index.md` utilise déjà le nom correct — le fichier a été créé avec
une coquille non détectée.

### Opération principale

```bash
git mv 00_documentation_arsenal/contrats/boiler/guard_expostion_ha.md \
       00_documentation_arsenal/contrats/boiler/guard_exposition_ha.md
```

### Références à mettre à jour

**Fichier 1 :** `contrats/chauffage/dependances_inter_domaines.md` (×2)

Ligne 107 :
```
`contrats/boiler/guard_expostion_ha.md`
→ `contrats/boiler/guard_exposition_ha.md`
```

Ligne 175 :
```
{...,guard_expostion_ha,...}
→ {...,guard_exposition_ha,...}
```

**Fichier 2 :** `changelog/changelogs/v12/v12_2.md` (×1)

Ligne 78 :
```
`contrats/boiler/guard_expostion_ha.md`
→ `contrats/boiler/guard_exposition_ha.md`
```

**Fichier 3 :** `changelog/index.md`
**Déjà correct** — `guard_exposition_ha.md`. Aucune modification.

### Hub navigation impacté

`navigation/domaines/boiler.md` signale la typo en Points de vigilance :
> `guard_expostion_ha.md` : typo dans le nom de fichier (`expostion`). Signalé, non corrigé.

Une fois le fichier renommé :
- **Si le hub est déjà appliqué** : éditer `navigation/domaines/boiler.md`,
  supprimer cet item des Points de vigilance.
- **Si le hub n'est pas encore appliqué** : mettre à jour le patch
  `navigation_domaines_boiler.patch` avant application.

### Commit suggéré

```
fix(contrats/boiler): rename guard_expostion → guard_exposition, fix 3 refs
```

---

## Étape 4 — Renommer `01__objet_perimetre_statut.md` → `01_objet_perimetre_statut.md`

### Contexte

Seul fichier de `socle_transversal/` à double underscore (`01__`).
Les 12 autres utilisent `NN_titre.md` (simple underscore).
Le README d'`aeration_blocage_chauffage` pointe déjà vers `01_` (nom correct) —
c'est le fichier disque qui porte la coquille.

### Opération principale

```bash
git mv 00_documentation_arsenal/contrats/aeration_blocage_chauffage/socle_transversal/01__objet_perimetre_statut.md \
       00_documentation_arsenal/contrats/aeration_blocage_chauffage/socle_transversal/01_objet_perimetre_statut.md
```

### Références à mettre à jour

**Fichier 1 :** `changelog/changelogs/v14/v14.md` (×1)

Ligne 43 — actuel :
```
(`socle_transversal/01__objet_perimetre_statut.md`)
```
Proposé :
```
(`socle_transversal/01_objet_perimetre_statut.md`)
```

**Fichier 2 :** `contrats/aeration_blocage_chauffage/README.md`
**Déjà correct** — `01_objet_perimetre_statut.md`. Aucune modification.

### Hub navigation

Aucun hub ne référence directement ce fichier. Aucune modification.

### Commit suggéré

```
fix(contrats/aeration): rename 01__objet → 01_objet, fix v14 changelog ref
```

---

## Étape 5 — Mise à jour `contrats/README.md` (P2)

### Objectif

La section "Contenu du dossier" décrit la famille comme entièrement plate.
Réalité : 14 domaines sont folderisés, 27 fichiers restent plats à la racine.

### Fichier impacté

```
00_documentation_arsenal/contrats/README.md
```

Remplacer :
```
Chaque fichier correspond à un domaine fonctionnel distinct.
```
Par :
```
La famille est mixte : 14 domaines sont organisés en sous-dossiers
(chauffage/, ecs/, alarme/, etc.) ; les domaines plus simples restent
en fichiers plats à la racine. Chaque dossier ou fichier correspond
à un domaine fonctionnel distinct.
```

### Commit suggéré

```
docs(contrats): update README — note mixed flat/folder structure
```

---

## Étape 6 — Rerouter les 6 références `resilience_electrique`

### Contexte

Arbitrage acté (note d'arbitrage `resilience_electrique`) : **B1 — reroute à plat**.
Le contenu existe déjà dans `contrats/pannes/secteur/` ; **aucun paquet `resilience_electrique/`** n'est créé.
Cette étape **enregistre le périmètre** ; le reroute n'est **pas** exécuté ici.

### Périmètre — 6 renvois dans 4 fichiers

| Fichier : ligne | Renvoi mort actuel | Cible de reroute |
|---|---|---|
| `secteur/10_socle.md:49` | `architecture/resilience_electrique/10_temporalite.md` | `11_temporalite.md` (nom **post-renommage**, cf. Étape 2) |
| `secteur/10_socle.md:121` | `architecture/resilience_electrique/20_fallback.md` | ancre interne au socle (fallback décrit sur place) — reformuler |
| `secteur/10_temporalite.md:18` | `contrats/resilience_electrique/00_panne_secteur_socle.md` | `10_socle.md` |
| `secteur/20_chauffage_et_ecs.md:16` | `contrats/resilience_electrique/00_panne_secteur_socle.md` | `10_socle.md` |
| `secteur/30_cycle_vie_et_signalisation.md:16` | `contrats/resilience_electrique/00_panne_secteur_socle.md` | `10_socle.md` |
| `secteur/30_cycle_vie_et_signalisation.md:22` | `contrats/resilience_electrique/01_panne_secteur_resilience_thermique.md` | `20_chauffage_et_ecs.md` |

### Dépendance d'ordre

Étape 6 **séquencée après l'Étape 2**, sans fusion : l'Étape 2 est un renommage mécanique (`10_temporalite` → `11_temporalite`) ; l'Étape 6 est un reroute. Le renvoi `10_socle.md:49` devra viser `11_temporalite.md`. **Les deux ne doivent pas être committées ensemble.**

### Cas particulier `20_fallback.md`

Aucun fichier cible : le mécanisme de fallback est décrit inline dans `10_socle.md`. Le reroute pointera une ancre interne ou reformulera le renvoi — **pas de fichier créé**. Sous-décision à acter au moment du reroute.

### Statut

**En attente** — périmètre enregistré, reroute non exécuté.

### Commit suggéré (au moment du reroute, pas maintenant)

```
fix(contrats/pannes): reroute 6 stale resilience_electrique refs to secteur/
```

---

## Anomalie connexe identifiée — *promue, voir Étape 6*

### `resilience_electrique` — nommage hérité (migration documentaire incomplète)

Découverte à l'analyse de l'Étape 2, d'abord cernée comme un seul chemin mort
(`10_socle.md:49`). La revue contradictoire a porté le périmètre réel à **6 renvois
dans 4 fichiers** de `contrats/pannes/secteur/`, vers deux racines inexistantes.

**Cause :** nommage hérité après refonte du domaine `pannes` — 6 références internes
non migrées. Les liens morts sont la conséquence, pas la nature du défaut.

Arbitrage tranché (note d'arbitrage `resilience_electrique`) : **B1 — reroute à plat**
(le contenu existe déjà sous `pannes/secteur/` ; pas de paquet `resilience_electrique/`).
L'hypothèse A (créer le paquet) est **écartée** : double source de vérité.

→ Traitement : **Étape 6**. Registre : **§1.4**.

---

## Étapes différées (décision requise)

### D1 — `eclairage/garage.md` vs `garage_implementation.md`

Deux fichiers dans `contrats/eclairage/` à titre et cible identiques.
**Question :** redondants (fusionner) ou distincts (différencier les périmètres) ?
Aucun patch avant arbitrage.

### D2 — Double emplacement `bouclage`

`contrats/bouclage.md` (racine) coexiste avec `contrats/ecs/04_*/`.
**Question :** quelle est la source de vérité ? L'autre devient redirection ou est supprimé.
Aucun patch avant arbitrage.

---

*Document généré lors de la session d'audit README Arsenal — juin 2026.
À classer dans `00_documentation_arsenal/audits/`.*
