# 🧠 ARSENAL — DOCUMENTATION DE RÉFÉRENCE

---

## 🎯 OBJET

Ce dossier contient la **documentation fonctionnelle, architecturale et historique**
du système **Arsenal**.

Il ne s'agit **ni** d'une aide Home Assistant,
**ni** d'un tutoriel,
**ni** d'un journal de commits Git.

Cette documentation décrit :

- ce que le système **doit faire** (contrats),
- **comment** et **pourquoi** il est construit ainsi (architecture),
- comment il a **évolué** dans le temps (changelog, historique),
- comment il est **audité** et gouverné (audits),
- comment il s'**interface** avec des outils externes,
- comment il se **navigue** transversalement (navigation).

Elle constitue la **référence de vérité** du système Arsenal.

> **Règle d'or.** Ce qui n'est pas documenté ici n'existe pas fonctionnellement.
> Inversement, ce qui est documenté ici doit pouvoir être retrouvé dans le système.

---

## 🧱 PHILOSOPHIE GÉNÉRALE

Arsenal repose sur une séparation stricte entre :

- **Intention utilisateur**
- **Règles métier**
- **Décisions observables**
- **Actions matérielles**

La documentation reflète cette séparation. En particulier, le **contrat** (ce que
le système doit faire) est distinct de l'**architecture** (comment il le fait) :
si une implémentation contredit un contrat, c'est l'implémentation qui est fausse.

---

## 📁 STRUCTURE RÉELLE DU DOSSIER

Le dossier est organisé en **neuf zones de premier rang**, plus ce README.

```
00_documentation_arsenal/
│
├── README.md                ← ce fichier
│
├── architecture/            ← référence d'implémentation (comment / pourquoi)
├── audits/                  ← cycle de vie d'audit par domaine
├── changelog/               ← évolution versionnée + récit historique
├── contrats/                ← référence normative (ce que le système doit faire)
├── evolutions_futures/      ← fiches prospectives (sas)
├── navigation/              ← orientation inter-familles (hubs, carte, pivots)
├── outils_externes/         ← supervision d'outils hors Home Assistant
├── schemas_ascii/           ← diagrammes ASCII de pipelines
└── ui/                      ← charte couleurs + socle de cartes Lovelace
```

---

## 📂 LES NEUF ZONES

### 🏗️ `architecture/`
Décrit **comment** le système est construit et **pourquoi** : doctrines transverses
(`03_doctrines/`), structure des includes (`00_structure_includes/`), recorder,
étiquettes, et documents d'architecture par sous-système.
👉 Référence d'implémentation. **N'introduit aucune règle métier.**
👉 Point d'entrée : [`architecture/index.md`](architecture/index.md).

### 🔍 `audits/`
Trace le **cycle de vie d'audit** par domaine, en étapes successives :
`01_rapports/` → `02_{arbitrages, conception, constats, contre_expertises}/` →
`03_plans_action/` → `04_chantiers/` → `05_clotures/`.
👉 Point d'entrée : [`audits/index.md`](audits/index.md).

### 📜 `changelog/`
Trace **l'évolution du système** dans le temps. Versionnage atomique et diffable
sous `changelogs/vXX/`, changelogs de chantiers sous `chantiers/`, récit
rétrospectif des inflexions dans `historique.md`.
👉 Point d'entrée : [`changelog/index.md`](changelog/index.md).
👉 Récit : [`changelog/historique.md`](changelog/historique.md).

### 📘 `contrats/`
Définit **ce que chaque sous-système DOIT faire** : intention utilisateur, règles
métier, invariants, dérives interdites. Domaines folderisés (`chauffage/`,
`climatisation/`, `alarme/`, `ecs/`, `meteo/`, `aeration_blocage_chauffage/`,
`boiler/`, `pannes/`…) et contrats de domaine à la racine.
👉 Principe : **le contrat précède l'implémentation.**
👉 Point d'entrée : [`contrats/index.md`](contrats/index.md).

### 🌱 `evolutions_futures/`
Sas de **fiches prospectives**. Une fiche y séjourne tant qu'elle n'est pas
formalisée ; une fois actée, elle migre vers `contrats/` ou `outils_externes/`.
👉 Voir [`evolutions_futures/README.md`](evolutions_futures/README.md).

### 🧰 `outils_externes/`
Documente la **supervision d'outils hors Home Assistant** : pont chaudière
(`boiler_pi/`), outillage NAS Arsenal (`nas_arsenal/`), NAS Imprimerie
(`nas_imprimerie/`).
👉 Voir [`outils_externes/README.md`](outils_externes/README.md).

### 🧭 `navigation/`
Couche d'**orientation inter-familles** : carte des domaines (`carte_domaines.md`),
22 hubs Tier-1 (un par domaine, point d'entrée transversal), pivots thématiques.
👉 **Non normative** — oriente sans redéfinir. Porte d'entrée : [`navigation/README.md`](navigation/README.md).
👉 Routeur des 22 hubs de domaine : [`navigation/carte_domaines.md`](navigation/carte_domaines.md).

### 🗺️ `schemas_ascii/`
Diagrammes **ASCII** de pipelines (aération, NAS↔HA, régulation thermique),
destinés à une lecture rapide en texte brut.
👉 Voir [`schemas_ascii/README.md`](schemas_ascii/README.md).

### 🎨 `ui/`
**Charte couleurs** (`couleurs/`) et **socle de cartes** Lovelace (`socle_ui/`),
plus les documents d'architecture UI transverse.
👉 Voir [`ui/README.md`](ui/README.md).

---

## 🧭 OÙ CHERCHER QUOI

| Question | Zone |
|---|---|
| « Que **doit** faire ce domaine ? » | `contrats/` |
| « **Comment** est-ce implémenté, et pourquoi ? » | `architecture/` |
| « **Qu'est-ce qui a changé** et quand ? » | `changelog/` |
| « Cet état a-t-il été **audité** ? » | `audits/` |
| « Comment Arsenal parle à un **outil externe** ? » | `outils_externes/` |
| « À quoi ressemble le **pipeline** ? » | `schemas_ascii/` |
| « Quelle **couleur / carte** UI utiliser ? » | `ui/` |
| « Une **idée** pas encore formalisée ? » | `evolutions_futures/` |
| « **Comment naviguer** dans la documentation ? » | `navigation/` |

---

## 🚦 AVANT DE PROPOSER OU MODIFIER — IA & CONTRIBUTEURS

> **Pointeur d'orientation, non normatif.** Cette section ne redéfinit rien et ne
> duplique pas la table ci-dessus : elle **route** vers les documents propriétaires.
> En cas de divergence, le document de famille fait foi.

Avant de proposer un changement — qu'on soit humain ou IA — s'assurer d'avoir
intégré les points suivants :

- **Un seul propriétaire par vérité ; aucune vérité concurrente.** Une décision a
  un décideur unique, un fait a un document propriétaire unique ; ne pas recréer
  ailleurs une vérité déjà détenue. Voir
  [`architecture/03_doctrines/principes_generaux.md`](architecture/03_doctrines/principes_generaux.md)
  (autorité unique par domaine).
- **Contrat / doctrine avant runtime.** Le contrat précède l'implémentation : si le
  YAML contredit le contrat, c'est l'implémentation qui est fausse.

**Lire la doc canonique applicable _avant_ de créer ou modifier — jamais se fonder
sur un fichier voisin ou une intuition.** Selon ce qu'on modifie, lire d'abord :

| Type de modification | Doc(s) canonique(s) à lire avant patch | Gate / contrôle |
|---|---|---|
| Runtime YAML (tout include) | [`structure_includes/index.md`](architecture/00_structure_includes/index.md) — carte dossier → document | `docs_lint` + checker de domaine |
| Helpers `input_*` / `counter` (clé `initial`) | [`restauration_etat_helpers.md`](architecture/03_doctrines/restauration_etat_helpers.md) — restauration d'état, marqueur `initial VOULU` | `check_initial_key_contracts` (`contracts_initial_key.yml`) |
| Template sensors (`12_`) | [`12_template_sensors.md`](architecture/00_structure_includes/12_template_sensors.md) | `docs_lint` + checker de domaine |
| Automations (`11_`) | [`11_automations.md`](architecture/00_structure_includes/11_automations.md) + [`id_automatisations.md`](architecture/03_doctrines/id_automatisations.md) | `docs_lint` + checker de domaine |
| Scripts (`10_`) | [`10_scripts.md`](architecture/00_structure_includes/10_scripts.md) + [`separation_decision_action.md`](architecture/03_doctrines/separation_decision_action.md) | `docs_lint` + checker de domaine |
| Customize (`01_`) | [`01_customize.md`](architecture/00_structure_includes/01_customize.md) | `check_01_customize_contracts` |
| Lovelace (`18_`) | [`18_lovelace.md`](architecture/00_structure_includes/18_lovelace.md) | `check_lovelace_includes_contracts` |
| Button-card templates (`19_`) | [`button_card_templates.md`](architecture/00_structure_includes/button_card_templates.md) + [`socle_ui/index.md`](ui/socle_ui/index.md) | `check_19_button_card_templates_contracts` |
| **UI couleurs** | **corpus `ui/couleurs/` à lire _intégralement_** : [`README.md`](ui/couleurs/README.md) + `01_principes` → `05_regles` (pas seulement le README) | `check_ui_couleurs_contracts` + `check_ui_runtime_colors_contracts` |
| Doc métier / contrats | [`contrats/index.md`](contrats/index.md) | `docs_ci_contract_counts` |
| Changelog / release | [`architecture/03_doctrines/redaction_changelog.md`](architecture/03_doctrines/redaction_changelog.md) | `docs_ci_changelog_index` |
| Navigation documentaire | [`navigation/README.md`](navigation/README.md) — règles R1–R8 | `docs_ci_navigation_leaf_pages` |
| Registre des chantiers | [`REGISTRE_CHANTIERS.md`](audits/REGISTRE_CHANTIERS.md) — gouvernance, co-commit | `check_registre_chantiers` |
| Checkers CI | [`../.github/workflows/docs.yml`](../.github/workflows/docs.yml) + `scripts/arsenal_contracts/` | `check_arsenal_self_contracts` (self-test) |

> Pointeur, non normatif : la table **route** vers les documents propriétaires, qui
> font foi. Elle ne recopie ni règle, ni seuil. « checker de domaine » = le checker
> du domaine fonctionnel touché (cf. `scripts/arsenal_contracts/`).

- **Ce qui est réellement ouvert aujourd'hui.** Consulter le cockpit
  [`audits/REGISTRE_CHANTIERS.md`](audits/REGISTRE_CHANTIERS.md) — statut des
  chantiers, à ne pas confondre avec la navigation.
- **S'orienter par domaine.** Entrer par
  [`navigation/carte_domaines.md`](navigation/carte_domaines.md) (registre des
  domaines et hubs) plutôt que par un fichier isolé.
- **Identifier les checkers CI applicables _avant_ le patch.** Les gates
  documentaires (`scripts/docs_lint/`) et les checkers de contrat par domaine
  (`scripts/arsenal_contracts/`) sont orchestrés en intégration continue — voir
  [`../.github/workflows/docs.yml`](../.github/workflows/docs.yml) pour le corpus.
  Un changement non conforme est rejeté par la machine, pas par un relecteur.
- **Discipline de commit.** Respecter la frontière patrimoine / runtime et les
  règles de commit. Voir
  [`architecture/03_doctrines/git.md`](architecture/03_doctrines/git.md).

---

## 🚫 CE QUE CETTE DOCUMENTATION N'EST PAS

- ❌ un dump de configuration Home Assistant
- ❌ une documentation utilisateur finale
- ❌ un journal de commits Git
- ❌ un espace de notes temporaires

---

## 📌 STATUT

- Portée : **système Arsenal**
- Nature : **documentation de référence**
- Autorité : **contrats fonctionnels** (prioritaires sur le code)
- Mise à jour : volontaire, réfléchie, tracée dans le changelog

---

## ✍️ NOTE FINALE

Cette documentation n'est pas figée, mais elle ne doit évoluer **que** lorsqu'une
intention utilisateur, une décision d'architecture ou un fait d'évolution le
justifie. Toute modification doit être **consciente, explicitée et tracée**.
