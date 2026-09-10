# `40_dashboards/system/` — Architecture UI

## Nature du dossier

`system/` est un **dashboard de supervision opérationnelle du socle maison**, centré sur la disponibilité, la stabilité, la connectivité et la santé des composants critiques.

Ce n'est pas un domaine métier utilisateur, ni une UI transactionnelle. C'est une **UI de supervision et d'alerte**, orientée détection d'incident, visibilité de stabilité, lecture de santé synthétique et accès optionnel à une action de remédiation manuelle.

La structure du domaine est :

```
information → statut / santé → diagnostic / supervision → action de remédiation optionnelle
```

---

## Structure implicite identifiée

Le dossier est organisé en **7 familles UI distinctes** :

### A. Information de stabilité

Exemple : `carte_uptime_systeme`

- Uptime transformé en lecture sémantique : bleu si récent, vert si stable
- **Type UI : interprétative** (transformation locale, pas une info neutre)

---

### B. Supervision d'incident / alerte

Exemples : `carte_compteur_alerte`, `systeme_bandeau_stabilite`

- Signalement rapide d'un état d'alerte ou d'instabilité avec forte priorité visuelle
- `systeme_bandeau_stabilite` : fonction de signal prioritaire, pas d'analyse fine
- `carte_compteur_alerte` : compteur transformé en état binaire (`0 = normal`, `> 0 = incident`)
- **Type UI : diagnostic**

---

### C. Diagnostic de connectivité

Exemple : `carte_etat_internet`

- Connectivité instantanée + qualité à 7 jours, classification composite
- Action de remédiation manuelle disponible en hold — secondaire, ne fait pas de cette carte une carte d'action
- **Type UI : diagnostic**

> La carte combine deux horizons temporels (instantané + historique) sous une seule couleur — lecture compacte mais composite. À documenter dans l'entête.

---

### D. Diagnostic d'intégrations

Exemples : `carte_integration_critique`, `netatmo_diagnostic`

- Supervision binaire ou temporelle d'une intégration critique, avec action de récupération optionnelle
- `carte_integration_critique` : **carte canonique générique du domaine** — logique la plus réutilisable (binaire ou âge, seuil, action optionnelle)
- `netatmo_diagnostic` : spécialisation à états textuels normalisés Arsenal
- **Type UI : diagnostic**

> `carte_integration_critique` constitue le socle canonique de supervision d'intégration. Aucune autre carte ne doit redéfinir cette logique. L'action de récupération reste secondaire et conditionnelle — ce template ne doit pas dériver vers une carte d'action déguisée.

---

### E. Santé de sous-système

Exemple : `boiler_status_health`

- Health synthétique multi-états d'un sous-système spécifique
- **Type UI : diagnostic**

> Ce template est cohérent dans `system/` comme supervision transversale de santé. À distinguer de `boiler/` : `boiler/` expose l'observabilité interne du sous-système, `system/` en expose la santé synthétique depuis l'extérieur.

---

### F. Résultat métier des jobs NAS commandés par Arsenal

Exemples : `arsenal_self_audit_status_card`, `arsenal_nas_release_diff_status_card`

- Verdict métier (`ok`/`alert`/`error`, `ok`/`partial`/`error`) des deux opérations
  commandables du socle `contrats/nas_transactionnel.md` (`AUDIT` → `arsenal_self`,
  `RELEASE_DIFF` → `arsenal_nas`) — chantier `audits/04_chantiers/transverses/c51_commandabilite_nas.md`
- Le NAS exécute la commande ; le résultat métier reste l'autorité exclusive du domaine
  Home Assistant correspondant (`arsenal_self.md`, `arsenal_nas.md`) — jamais recalculé ici
- **Type UI : diagnostic**

---

### G. Demande et transaction des jobs NAS commandés par Arsenal (C51)

Exemples : `carte_action_nas_admission_demander`, `carte_nas_admission_etat_transaction`

- Service rendu à Arsenal (audit Arsenal, release diff Arsenal), pas « commandabilité du
  NAS » : la demande part d'Arsenal, le NAS n'est que l'exécutant technique externe de la
  commande MQTT (chantier C51 §4 « Matrice des autorités » — le NAS n'a ici aucune autorité
  de décision), le résultat revient nourrir les cartes de la famille F ci-dessus
- `carte_action_nas_admission_demander` déclenche, après confirmation, le script backend
  désigné (`script.nas_admission_demander_audit`/`_release_diff`) — aucune publication MQTT,
  aucun `request_id` construit côté UI (« Backend Arsenal décide, UI Lovelace rend »)
- `carte_nas_admission_etat_transaction` affiche le dernier verdict **transactionnel**
  (admission/terminaison NAS) — jamais assimilé au résultat métier de la famille F ; séparation
  stricte transaction/résultat métier opposable par `nas_transactionnel.md` §12
- **Type UI : action** (`carte_action_nas_admission_demander`) et **diagnostic**
  (`carte_nas_admission_etat_transaction`) — première introduction du type `action` dans ce
  domaine
- Repositionnées ici depuis `40_dashboards/nas/` (correction C51, 2026-09-10) : elles ne
  qualifient jamais la santé du NAS, seulement une demande/transaction Arsenal — voir
  `c51_commandabilite_nas.md` §12.9

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                                 |
|----------------|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| interprétative | transformation locale tolérée, non source de vérité système                                    | `carte_uptime_systeme`                                                                   |
| diagnostic     | qualifie un état de santé, une cohérence ou une disponibilité                                   | `carte_compteur_alerte`, `systeme_bandeau_stabilite`, `carte_etat_internet`, `carte_integration_critique`, `netatmo_diagnostic`, `boiler_status_health`, `arsenal_self_audit_status_card`, `arsenal_nas_release_diff_status_card`, `carte_nas_admission_etat_transaction` |
| pure           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                        |
| action         | proxy UI d'une commande backend                                                                  | `carte_action_nas_admission_demander` *(C51)*                                            |
| info           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                        |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Information stabilité    → 10_info_stabilite/
Niveau 2 — Supervision / Alerte     → 20_supervision/
Niveau 3 — Connectivité             → 30_diagnostic_connectivite/
Niveau 4 — Intégrations / Santé     → 40_diagnostic_integrations/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.
>
> Les templates C51 (`carte_action_nas_admission_demander`,
> `carte_nas_admission_etat_transaction`) vivent dans des couches propres à part
> (`50_action_admission_arsenal/`, `51_diagnostic_transaction_arsenal/`), non numérotées dans
> la séquence 10→40 ci-dessus : elles ne qualifient pas la santé d'un sous-système, mais une
> commande Arsenal exécutée par le NAS — un axe orthogonal aux quatre niveaux d'origine,
> volontairement non intercalé pour ne pas renuméroter l'existant.

---

## Structure cible recommandée

```
40_dashboards/system/

  10_info_stabilite/
    carte_uptime_systeme.yaml

  20_supervision/
    carte_compteur_alerte.yaml
    systeme_bandeau_stabilite.yaml
    arsenal_self_audit_status_card.yaml
    arsenal_nas_release_diff_status_card.yaml

  30_diagnostic_connectivite/
    carte_etat_internet.yaml

  40_diagnostic_integrations/
    carte_integration_critique.yaml
    netatmo_diagnostic.yaml
    boiler_status_health.yaml

  50_action_admission_arsenal/                  ← C51
    carte_action_nas_admission_demander.yaml

  51_diagnostic_transaction_arsenal/             ← C51
    carte_nas_admission_etat_transaction.yaml
```

> `20_supervision/` et `30_diagnostic_connectivite/` peuvent être fusionnés en une seule couche si la compacité prime. La séparation est recommandée car les deux familles ont des rôles distincts (signal prioritaire vs diagnostic qualifié).

---

## Points de fragilité documentés

### 1. `carte_integration_critique` — hybride action/diagnostic à surveiller

Combine diagnostic et action manuelle optionnelle. Acceptable, car l'action est secondaire et conditionnelle. Ne pas laisser dériver vers une carte d'action déguisée — la finalité reste diagnostique.

### 2. `carte_etat_internet` — deux horizons temporels, une couleur

Mélange connectivité instantanée et qualité historique à 7 jours. Utile, mais composite. À documenter dans l'entête pour éviter une mauvaise lecture.

### 3. `carte_uptime_systeme` — lecture `states[]` directe

Dépendance forte à l'entity sous-jacente. À documenter dans l'entête comme dépendance non découplée.

### 4. `boiler_status_health` dans `system/`

Cohérent ici comme vue externe de santé. Risque de doublon conceptuel avec `boiler/` si mal utilisé. La règle : `boiler/` = observabilité interne, `system/` = santé synthétique vue de l'extérieur.

### 5. `carte_action_nas_admission_demander` — premier type `action` du domaine

Introduit un déclenchement direct (pas une remédiation secondaire comme en B/C/D). Acceptable car il reste un satellite conditionnel de la famille G (jamais une action autonome hors contexte) et ne redéfinit aucune logique de transport — le backend Arsenal décide, cette carte ne fait qu'exprimer une intention utilisateur. À ne pas généraliser sans réexaminer la doctrine « remédiations secondaires » du domaine.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Ajouter le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter `carte_integration_critique` comme canonique**
Ajouter dans son entête : rôle canonique de supervision d'intégration, action secondaire et conditionnelle, non généralisable comme carte d'action.

**Étape 4 — Documenter les fragilités**
Ajouter dans les entêtes : dualité temporelle (`carte_etat_internet`), dépendance `states[]` (`carte_uptime_systeme`), frontière `boiler/` vs `system/` (`boiler_status_health`).
