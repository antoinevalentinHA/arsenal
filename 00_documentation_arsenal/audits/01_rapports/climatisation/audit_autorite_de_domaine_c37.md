# Audit — Autorité de domaine climatisation (C37)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit de conformité du domaine **climatisation** à la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md), appliquée par le chantier C37 (patron VMC/C36). Complément de l'[audit C36](../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md), qui avait explicitement exclu ce domaine. |
| **Domaine** | climatisation |
| **Date** | 2026-07-27 |
| **Nature** | **Audit statique, lecture seule.** Aucun reboot, reload, appel de service ou changement d'état provoqué. **Aucun runtime / contrat / checker / UI / registre modifié par ce rapport.** |
| **Base** | HEAD `6169b4d`. |
| **Couverture** | Stack autorité clim (5 helpers, 2 primitives, décision exécutoire `sensor.clim_mode_commande`, 2 automations de médiation, chaîne d'exécution `clim_execution` → `exec_apply_*`, Guard) · contrats `16_autorite_de_domaine_climatisation.md` et `03_decision_canonique.md` (v1.4) · checkers `check_climatisation_*` + transverses. |

> **Règle appliquée.** Verdict de conformité porté sur le **code déployé** (templates,
> conditions, écrivains suivis jusqu'au service appelé), pas sur la seule prose contractuelle.

---

## 1. Chaîne d'autorité reconstituée

| Rôle | Composant réel |
|---|---|
| Intention UI | `input_select.clim_autorite_intention` (surface, **jamais** le titulaire) |
| Traduction / médiation | automation `10030000000123` (gardée « divergence réelle » + `systeme_stable`) ; re-synchro inverse `10030000000124` |
| Primitives supervisées | `script.clim_entrer_mode_manuel` (consigne **puis** titulaire) · `script.clim_revenir_mode_automatique` |
| Titulaire (vérité) | `input_select.clim_titulaire_autorite` ∈ `{automatique, manuel}` |
| Décision exécutoire | `sensor.clim_mode_commande` = manuel ? `clim_consigne_manuelle` : `sensor.clim_target_mode` |
| Décision théorique | `sensor.clim_target_mode` (exposée en attribut `mode_theorique`, non exécutoire) |
| Application | automation `10030000000105` (gardée `systeme_stable`) → **écrivain unique** `script.clim_execution` |
| Writers matériels | `script.clim_exec_apply_{cool,dry,heat,off}` → `climate.clim` + `switch.clim_power` |
| Réassertion | watchdog `10030000000106`, reprise après échec, réarmement — **tous** routés par `clim_execution` |

---

## 2. Conformité aux invariants INV-AUT-1..7

| Invariant | Verdict | Preuve statique |
|---|---|---|
| **INV-AUT-1** Unicité | **CONFORME** | Titularité portée par `clim_titulaire_autorite` (2 options exclusives), écrit **uniquement** par les 2 primitives. L'intention UI est déclarée « PAS le titulaire ». |
| **INV-AUT-2** Écrivain unique | **CONFORME** (1 point d'attention) | Seuls `clim_exec_apply_*` émettent `climate.clim`(mode)/`switch.clim_power` ; toute réassertion passe par `clim_execution`. **Point d'attention** : le **Guard** appelle `clim_exec_apply_off` **en direct** (court-circuite postcondition/retry) — doctrinalement couvert (protection impérative §16.5, borné à l'état sûr `off`, gardé `systeme_stable`, s'abstient si décision indisponible), mais c'est un second chemin d'invocation **non gardé CI**. Les axes ventilation / consigne T° / silence écrivent `climate.clim` sur **d'autres axes** (hors périmètre §16.3) — pas un second écrivain de l'exécutoire. |
| **INV-AUT-3** Pas de concurrents | **CONFORME** | `mode_commande` : bascule nette par le régime (`if manuel → consigne else → target_mode`), aucune fusion, aucun `min/max` entre décisions. |
| **INV-AUT-4** Théorique non exécutoire | **CONFORME** | En manuel, `state` = consigne ; `clim_target_mode` n'est qu'un attribut informatif. L'exécution ne lit que `clim_mode_commande`. Seul usage résiduel de `target_mode` : semence de la consigne **à l'entrée** en manuel (information → consigne, pas un chemin d'exécution). |
| **INV-AUT-5** Transition explicite | **CONFORME** | Primitives supervisées ; entrée atomique (consigne avant autorité, abstention sur consigne invalide) ; retour explicite ; UI n'écrit que l'intention, traduite sous garde de divergence + stabilité. |
| **INV-AUT-6** Pas de reprise silencieuse | **CONFORME (robuste)** | Aucun `initial:` sur les 3 helpers d'autorité. Traduction gardée `systeme_stable` ; la synchro réaligne l'intention sur le titulaire **restauré** au `homeassistant.start` avant toute traduction ; application gardée `systeme_stable`. Aucune reprise implicite vers l'automatique. |
| **INV-AUT-7** Expiration volontaire | **NON OFFERT — conforme** | Régime manuel indéfini jusqu'à restitution explicite ; expiration « admise en option », non implémentée. Légitime au titre de la non-sur-spécification (doctrine §6). |

**Anti-fallback (démontré).** `mode_commande.yaml` porte une `availability` stricte : indisponible
si titulaire invalide OU si la source qu'il désigne l'est ; aucun `unknown` n'est substitué par
`automatique`/une valeur métier. La couche conformité (`clim_incoherence_decision_reel`) se compare
à l'**exécutoire** et s'abstient quand il est indisponible.

**Bilan §2 : 7/7 invariants tenus par le runtime déployé.** Instanciation fidèle du patron VMC.

---

## 3. Réconciliation du contrat de souveraineté `03_decision_canonique.md` — **close**

La contradiction historique (`D-C36-L4` : invariant *« non modifiable manuellement »* vs doctrine)
est **levée et tracée**, contrairement au chauffage (cf. audit C39) :

- `03_decision_canonique.md` est passé en **v1.4** avec un encart de portée (l. 39-47) : l'invariant
  vaut **pour la décision automatique** ; sous régime manuel l'utilisateur devient titulaire,
  l'exécutoire dérive du titulaire + consigne, `clim_target_mode` demeure calculé/exposé comme
  **décision théorique non exécutoire** ⇒ « l'invariant n'est donc **pas** contredit ». Renvoi
  explicite au contrat `16_autorite_de_domaine_climatisation.md`. Réciproque dans le contrat 16.7.
- **Résidu purement documentaire** : la doctrine elle-même (§9) liste **encore** `03_decision_canonique.md`
  parmi les contrats « à réconcilier ultérieurement » — alors que la réconciliation est faite (v1.4).
  Simple **retard de mise à jour de la doctrine**, sans incident runtime.

---

## 4. Couverture CI

**Gardé par un checker :**

- **Pas de `initial:` (INV-AUT-6)** — `check_initial_key_contracts.py` (HINIT-001, ERROR bloquant)
  scanne `06_input_selects/` → couvre les 3 helpers d'autorité clim. Filet réel.
- **Anti-fallback de l'opérande de conformité** — `check_climatisation_admissibilite_contracts.py::test_coherence_abstention_operandes`
  impose que l'`availability` de `clim_incoherence_decision_reel` observe `clim_mode_commande` (touche
  INV-AUT-4 indirectement).

**Angles morts (conformité auto-déclarée, aucun filet) :**

| # | Invariant non gardé | Risque |
|---|---|---|
| A1 | **Écrivain unique clim (INV-AUT-2)** | **Aucun** checker n'affirme que seuls `clim_execution`/`exec_apply_*` écrivent le mode, ni que l'unique bypass toléré est Guard→`apply_off`. **Contraste net avec le déshumidificateur**, qui possède `check_deshum_tx_contracts.py` (« aucun writer matériel hors autorité unique »). Angle mort majeur. |
| A2 | **Availability propre de `clim_mode_commande`** (anti-fallback de l'exécutoire) | Le checker la qualifie de « native » **sans jamais lire** son bloc `availability`. Non testée. |
| A3 | **INV-AUT-1/3/4/5** (titulaire écrit par les 2 primitives seules ; pureté de dérivation ; ordre atomique) et garde `systeme_stable` sur 105/123 | Aucun checker dédié. **Aucun `check_climatisation_autorite_*.py` n'existe.** |

---

## 5. Écarts contrat↔runtime & points d'attention

1. **Commentaires périmés « ÉCHAFAUDAGE INERTE » (démontré).** Les en-têtes de `titulaire_autorite.yaml`,
   `consigne_manuelle.yaml`, `mode_commande.yaml`, `entrer_mode_manuel.yaml`, `revenir_mode_automatique.yaml`
   décrivent encore l'état **pré-bascule** (« aucun consommateur d'exécution »), alors que le runtime
   **prouve la bascule faite** (l'application déclenche sur `clim_mode_commande`, l'exécution le lit) et
   que le contrat 16.8 déclare le pilote clos (2026-07-25). **Prose trompeuse, sans effet fonctionnel.**
2. **Guard court-circuite `clim_execution`** (cf. INV-AUT-2) — couvert doctrinalement, non gardé CI.
3. **Retard documentaire de la doctrine §9** (cf. §3) — à rafraîchir.
4. **Régime manuel = axe MODE uniquement.** Ventilation, consigne T° et silence continuent d'être
   pilotés par Arsenal dans les deux régimes (conforme §16.3, hors périmètre) : un titulaire manuel ne
   gouverne pas ces axes — à garder en tête.
5. **Réserve fail-open C30 (P1, héritée).** Un état d'intégration dégradé peut faire échouer
   silencieusement une commande ; réserve non régressive (affecte déjà l'automatique), suivie par C30 —
   hors de cet audit.

---

## 6. Synthèse

- **Conformité runtime : 7/7 invariants tenus** (INV-AUT-7 non offert, légitime). Le patron VMC est
  fidèlement répliqué. **Aucun P1** propre à l'autorité.
- **Réconciliation de souveraineté : close et tracée** (contrat v1.4) — meilleur état que le chauffage.
- **Deux points d'attention réels** : le bypass **Guard→`apply_off`** (sanctionné doctrinalement, non
  gardé), et surtout **l'absence totale de garde CI d'écrivain unique / d'availability de l'exécutoire**
  (angle mort A1/A2, en retrait du patron déshumidificateur). Écart classé **P2 (durcissement CI)**.
- **Dette résiduelle purement documentaire** : commentaires « échafaudage inerte » périmés + doctrine §9
  non rafraîchie. **P3.**

**Aucun runtime / contrat / checker / UI / registre / changelog modifié par ce rapport.** Les pistes de
durcissement sont **classées, non prescrites** (relèveraient d'un chantier CI distinct, cf. C14).

---

## 📎 Renvois

- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Contrats : [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) · [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) (v1.4)
- Audits jumeaux : [`../chauffage/audit_autorite_de_domaine_c39.md`](../chauffage/audit_autorite_de_domaine_c39.md) · [`../deshumidificateur/audit_autorite_de_domaine_c40.md`](../deshumidificateur/audit_autorite_de_domaine_c40.md)
- Audit d'origine (C36/VMC) : [`../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md`](../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md)
