# Audit — Autorité de domaine déshumidificateur (C40)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit de conformité du domaine **déshumidificateur (cave)** à la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md), appliquée par le chantier C40 (patron VMC/C36). Boucle l'essaimage de la doctrine (après VMC/C36, clim/C37, chauffage/C39). |
| **Domaine** | déshumidificateur |
| **Date** | 2026-07-27 |
| **Nature** | **Audit statique, lecture seule.** Aucun reboot, reload, appel de service ou changement d'état provoqué. **Aucun runtime / contrat / checker / UI / registre modifié par ce rapport.** |
| **Base** | HEAD `27b67ed`. |
| **Couverture** | Stack autorité déshum (4 helpers, primitives `entrer/revenir`, `forcer_etat`, `guard`, `converger_auto`, décision exécutoire `sensor.deshumidificateur_etat_commande`, application, retry, convergence boot) · contrats `autorite_de_domaine.md` + `guard.md` + chantier C40 · checkers `check_deshum_tx`, `check_deshum_guard`, `check_deshumidificateur_metier`, `r_call_deshum.py` (R-CALL-DESHUM) + workflows. |

> **Règle appliquée.** Verdict porté sur le **code déployé** (templates, conditions, écrivain suivi
> jusqu'au `switch.turn_on/off`), pas sur la seule prose contractuelle. `[D]` = démontré ; `[I]` = inféré.

---

## 1. Chaîne d'autorité reconstituée

| Rôle | Composant réel |
|---|---|
| Observation | `binary_sensor.deshumidificateur_actif` (puissance > 100 W) — **seule vérité** ; `…_demarrage_recommande` = décision auto théorique |
| Titulaire (vérité) | `input_select.deshumidificateur_titulaire_autorite` ∈ `{automatique, manuel}`, écrit **uniquement** par les 2 primitives |
| Branche auto | `input_select.deshumidificateur_decision_auto` ∈ `{on, off}` (producteurs `activation`/`desactivation`/`converger_auto`) |
| Branche manuel | `input_select.deshumidificateur_consigne_manuelle` ∈ `{on, off}` (écrite avant le transfert) |
| Décision exécutoire | `sensor.deshumidificateur_etat_commande` = manuel ? consigne : decision_auto (availability stricte) |
| Application | automation `…application` (`systeme_stable`) sur état **ou** événement |
| **Écrivain physique unique** | `script.set_deshumidificateur_state` → `switch.deshumidificateur` ; appelants légitimes = `{application, retry_on, retry_off}` |
| Guard (passif) | `script.guard_deshumidificateur` → verdict diagnostic, **aucune écriture switch, aucune réémission** |
| Médiation UI | `input_select.deshumidificateur_autorite_intention` → automations `…013` (exécution) / `…014` (synchro) |

---

## 2. Conformité aux invariants INV-AUT-1..7

| Invariant | Verdict | Preuve statique |
|---|---|---|
| **INV-AUT-1** Unicité | **CONFORME** | Titulaire unique (2 options), écrit exclusivement par les 2 primitives. L'UI écrit l'*intention*, jamais le titulaire. |
| **INV-AUT-2** Écrivain unique | **CONFORME** | **Un seul** chemin vers `switch.deshumidificateur` (`set_deshumidificateur_state`), gardé CI (voir §5). Numerus clausus des appelants = `{application, retry_on, retry_off}`, miroir contrat↔constante. Le **Guard est le seul autre acteur et il est passif** (observation pure, aucune écriture switch). |
| **INV-AUT-3** Pas de concurrents | **CONFORME** | `etat_commande` sélectionne la source par le régime. En manuel, les producteurs auto rafraîchissent `decision_auto` (théorique) mais **conditionnent l'impulsion d'application à `titulaire == automatique`** → la branche auto n'atteint jamais l'écrivain en manuel. |
| **INV-AUT-4** Théorique non exécutoire | **CONFORME** | En manuel, `demarrage_recommande` reste en attribut `etat_theorique`. Le **retry souverain relit `etat_commande` et annule** une commande devenue non souveraine. |
| **INV-AUT-5** Transition explicite | **CONFORME** | Entrée atomique (consigne avant autorité) ; retour auto explicite/tracé avec **abstention si la décision auto n'est pas qualifiable** ; médiation gardée « intention ≠ titulaire ». |
| **INV-AUT-6** Pas de reprise silencieuse | **CONFORME (robuste)** | Aucun `initial:` (4 helpers). Application + convergence boot gardées `systeme_stable`. **Convergence boot ne reprend pas silencieusement** : en manuel elle honore la consigne restaurée ; en auto elle **miroite l'état réel observé, jamais la valeur restaurée** (une `decision_auto` restaurée est « non qualifiée » et jamais appliquée avant republication). |
| **INV-AUT-7** Expiration volontaire | **NON OFFERT — conforme** | Contrat §4 : « aucune expiration… extension future distincte, hors périmètre ». Légitime (non-sur-spécification). |

**Anti-fallback (démontré).** `etat_commande.availability` stricte : indisponible si titulaire ou source
désignée invalide ; aucun `unknown` substitué. L'inhibition réellement opposable est dans l'écrivain
(indispo source/entité → stop) = **catégorie A** (impossibilité physique).

**Bilan §2 : 7/7 invariants tenus par le runtime déployé.**

---

## 3. Protections impératives (§7) — le point central de ce domaine : **CONFORME**

Le déshum était le cas-test délicat : domaine « auto pur à contraintes de sûreté fortes », avec des
durées **min-on** (`timer.deshumidificateur_cycle`) et **min-off** (`…_blocage_redemarrage`) qui
auraient pu être confondues avec des protections impératives. La doctrine (§7 + garde anti-abus) proscrit
exactement cette confusion : une politique de préservation matérielle **négociable** est catégorie B,
outrepassable par un titulaire manuel.

**Démontré `[D]` :**

- Les timers min-on/min-off ne sont consultés **que** dans les producteurs **auto** (`activation`,
  `desactivation`) et `converger_auto` — **branche automatique uniquement**.
- Le chemin manuel `consigne → etat_commande → application → set_deshumidificateur_state → switch` ne
  consulte **aucun** de ces timers (ni l'écrivain, ni l'application, ni les retry). **Une commande
  manuelle d'arrêt pendant le min-on, ou de marche pendant le min-off, est exécutoire immédiatement.**
- Le contrat classe explicitement ces durées « politique d'usage — non invariante », « Autorité :
  aucune », avec clause de **requalification future en catégorie A sur preuve matérielle**.

Le **Guard** ne borne aucune commande : il qualifie *après coup* (verdict passif). Aucune protection de
confort/sobriété n'est traitée comme impérative. **Garde anti-abus §7 pleinement respectée.**

---

## 4. Réconciliation — **tracée**

Souveraineté antérieure = **souveraineté d'observation** (« un système non pilotable ne peut être
gouverné que par observation ») + écrivain d'exécution unique. Réconciliation explicitement tracée
(chantier C40, daté 2026-07-26) :

- **Pivot §5.1 = OUI** (mode manuel supervisé accordé) ; **§5.7 écartée** (pas de pression physique
  directe) ; **§5.8 sans objet** (pas d'écrivain concurrent).
- **Min-off/min-on requalifiés** de garde « souveraine » en **catégorie B non opposable** (§5 D5/D5-bis).
- Souveraineté d'observation **conservée dans son unicité, précisée dans sa titularité**.

C'est la réconciliation **la plus explicite** des quatre domaines (comparer au chauffage, où le résidu
`10 §6 l.244` reste ouvert au niveau textuel).

---

## 5. Couverture CI — **la plus forte des quatre domaines**, avec un angle mort de déclenchement

| Propriété | Gardé ? | Checker | Bloquant / actif |
|---|---|---|---|
| Écrivain physique unique du switch (INV-AUT-2) | **OUI** | `check_deshum_tx` (`test_no_other_physical_switch_writers`, scan repo entier ; `test_domain_automations_do_not_write_switch`) | **Bloquant, toujours actif** |
| Guard passif (aucune action/réémission, écritures diagnostiques seules) | **OUI** | `check_deshum_guard` (8 tests) | **Bloquant, toujours actif** |
| Pas de `initial:` (INV-AUT-6) | **OUI** | `check_initial_key` | **Bloquant, toujours actif** |
| Entités métier / timers déclarés | OUI | `check_deshumidificateur_metier` | Bloquant, toujours actif |
| Numerus clausus appelants `set_deshumidificateur_state` + anti-routage switchbot (R-CALL-DESHUM) | **OUI, mais déclenchement limité** | `r_call_deshum.py` via `test_bascule_c40.py` | ⚠️ voir ci-dessous |

**Le seul écart de robustesse `[D]` — scope de déclenchement de R-CALL-DESHUM.** L'enforcement
(`test_bascule_c40.py` / `r_call_deshum.py`) n'est exécuté que par `arsenal-ci-chauffage.yml` et
`arsenal-ci-climatisation.yml`. **Vérifié** : leurs path-filters incluent `tools/arsenal_ci/**` et leurs
propres domaines, mais **ni `11_automations/deshumidificateur/**` ni `10_scripts/deshumidificateur/**`**.
Conséquence : une PR **purement déshum** ajoutant un appelant illégitime de `set_deshumidificateur_state`,
ou une réémission `bot_transaction_execute`, **ne déclenche pas** ces workflows → numerus clausus et
anti-routage non re-vérifiés sur cette PR. L'**anti-appel-direct du switch** reste, lui, couvert par
`check_deshum_tx` (toujours actif) — donc l'écrivain physique est protégé ; c'est le **numerus clausus des
appelants du script** et l'**anti-routage** qui ne le sont pas sur une PR déshum.

**Autres angles morts (auto-déclarés) :** unicité d'écrivain des helpers d'autorité (titulaire, consigne,
decision_auto, intention) non gardée ; `availability` stricte de `etat_commande` non testée par un checker.

> **Nuance.** Ces angles morts n'entament pas la **conformité statique actuelle** (le runtime est
> conforme) — ils concernent la **protection contre la régression future**.

---

## 6. Écarts contrat↔runtime, résidus switchbot, points d'attention

1. **Cohérence contrat↔runtime : bonne `[D]`.** Tous les livrables déclarés au contrat §11 sont présents
   et conformes. Aucun écart de fond.
2. **Résidus retrait switchbot `[I]`.** Le contrat §9 déclare le retrait physique livré (branches et
   helpers dormants supprimés, `switchbot_transactionnel.md` v2.1.0). `bot_transaction_execute` subsiste
   comme site générique attendu (`bot_chambre_parents`) ; la couche guard est indépendante de switchbot.
3. **Priorité (robustesse, non conformité)** : rattacher R-CALL-DESHUM à un workflow **toujours actif**
   (ou étendre les path-filters aux chemins déshum) pour non-régresser le numerus clausus/anti-routage
   sur les PR purement déshum.
4. **Guard « validation V1 » instantanée** assumée au contrat : un spike bref peut donner `confirmed`
   prématuré — limite connue, hors autorité.
5. **`command_error` (source indisponible)** non traité par les retry (conditionnés `not_confirmed` +
   `timeout`) — cohérent avec la doctrine (indispo = catégorie A, non contournable).

---

## 7. Synthèse

- **Conformité runtime : 7/7 invariants tenus** (INV-AUT-7 non offert, légitime). **Aucun P1.**
- **Point §7 (protections impératives) : min-on/min-off démontrés NON opposables au manuel** — le
  domaine qui portait le risque doctrinal le plus élevé le traite **exemplairement** (garde anti-abus
  pleinement respectée). C'est le meilleur élève sur ce plan.
- **Réconciliation la plus explicite des quatre** (pivot §5.1 OUI, min-on/off → catégorie B, tracé daté).
- **Couverture CI la plus forte** (écrivain unique + guard passif + `initial:`, tous **bloquants et
  toujours actifs**). **Unique fragilité** : le **scope de déclenchement de R-CALL-DESHUM** (numerus
  clausus des appelants du script + anti-routage non vérifiés sur une PR purement déshum). **P2
  (robustesse CI), pas une non-conformité.**

**Aucun runtime / contrat / checker / UI / registre / changelog modifié par ce rapport.** Les pistes
(rattacher R-CALL-DESHUM à un workflow toujours actif ; garder l'`availability` de `etat_commande`) sont
**classées, non prescrites** — arbitrage propriétaire.

---

## 📎 Renvois

- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) (§7 protections impératives)
- Contrats : [`deshumidificateur/autorite_de_domaine.md`](../../../contrats/deshumidificateur/autorite_de_domaine.md) · [`deshumidificateur/guard.md`](../../../contrats/deshumidificateur/guard.md)
- Chantier : [`chantier_autorite_de_domaine_deshumidificateur.md`](../../04_chantiers/deshumidificateur/chantier_autorite_de_domaine_deshumidificateur.md)
- Audits jumeaux : [`../climatisation/audit_autorite_de_domaine_c37.md`](../climatisation/audit_autorite_de_domaine_c37.md) · [`../chauffage/audit_autorite_de_domaine_c39.md`](../chauffage/audit_autorite_de_domaine_c39.md) · [`../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md`](../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md)
