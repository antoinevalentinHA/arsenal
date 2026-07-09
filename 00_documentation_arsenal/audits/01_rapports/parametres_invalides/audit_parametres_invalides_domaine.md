# 🧮 ARSENAL — AUDIT — Domaine transverse **Paramètres invalides** (intégrité des réglages)

> **Trace d'audit documentaire, lecture seule.** Aucune correction runtime : ni template, ni contrat, ni checker modifiés.
> Convention : **[FAIT]** observé · **[HYP]** hypothèse · **[RECO]** recommandation.
> Source normative : [`../../../contrats/parametres_invalides.md`](../../../contrats/parametres_invalides.md) (v1.1, NORMATIF). Vérification mécanique : `scripts/arsenal_contracts/check_parametres_invalides_contracts.py` (T1–T12, workflow `contracts_parametres_invalides.yml`).

---

## Verdict

**Architecture 4 couches saine et structurellement bien gardée, avec un trou fail-closed réel isolé.** La sentinelle d'intégrité (capteurs domaine → groupe → sentinelle globale → carte UI conditionnelle) est correctement construite : checker **vert 12/12**, fail-closed **correctement appliqué sur 7 des 8 capteurs** (`chauffage` et `vacances` sont exemplaires). Mais :

1. **[FAIT] Un trou fail-closed (P2)** sur `climatisation` — invariant « blocage horaire » (inv9) : ses 3 sources non-numériques (2 `input_datetime` + 1 `input_boolean`) sont **hors de la garde d'indisponibilité**. Une borne horaire absente n'est **pas signalée** (fail-**open**) — exactement la faille que le contrat entend proscrire.
2. **[FAIT] Deux dérogations (P3)** : comparaison directe de chaînes ISO temporelles (interdit explicite du contrat) dans `eclairage` et `modes_maison` — fail-closed préservé, auto-justifiées en-tête, mais fragiles.
3. **[FAIT] Angles morts du checker (P3)** : les 12 tests gardent la **structure** et 2 formes littérales de fallback, mais **pas la sémantique fail-closed** — d'où le trou climatisation invisible en CI.

**Gravité globale : P2.** Domaine d'**observabilité pure** (aucun actionnement) : l'impact est une **cécité de diagnostic** ponctuelle, pas une action dangereuse. Mais comme la raison d'être du domaine *est* le fail-closed, le trou climatisation touche le cœur de la promesse.

---

## 1. Périmètre & méthode

- **Périmètre :** les 9 fichiers `12_template_sensors/system/integrite_reglages/` (8 capteurs domaine + `global.yaml`), le groupe `02_groups/parametres_invalides.yaml`, la carte UI `18_lovelace/includes/alerte_configuration_invalide.yaml`, croisés avec le contrat et le checker.
- **Méthode :** lecture du contrat + checker → recensement fail-closed des 8 capteurs (chaque invariant force-t-il la violation quand une source manque ?) → recherche de fallbacks non-littéraux et de comparaisons ISO → vérification `cause` priorisée et cohérence en-tête↔implémentation → exécution du checker.

**Doctrine centrale [FAIT].** « Si une source est indisponible, on considère par défaut tous les invariants qui en dépendent comme **violés** — pas d'optimisme silencieux » (contrat §Doctrine d'expression). Interdits : tout fallback numérique silencieux (`float(0)`…) et la comparaison directe de chaînes ISO. Le gabarit prescrit `float(none)` + garde `is none`, et `as_datetime(...)` gardé pour les `input_datetime`.

---

## 2. Ce qui est sain (à préserver)

- **[FAIT] Fail-closed correct sur 7/8 capteurs.** `bouclage`, `chauffage`, `deshumidificateur`, `eclairage`, `modes_maison`, `vacances`, `vmc` : chaque invariant est de la forme `indisponible or not (comparaison)`, forçant la violation si une source manque. Aucun fallback silencieux littéral **ni non-littéral** (`float(n≠0)`, `default(...)`, `or '0'`) trouvé.
- **[FAIT] `vacances` — modèle exemplaire.** Garde d'indisponibilité explicite puis `as_datetime(fin) > as_datetime(debut)` ; `cause` priorisant `helpers_indisponibles`.
- **[FAIT] Structure gardée par le checker.** Cohérence groupe↔capteurs (T3, 8↔8), sentinelle ne lisant que le groupe (T4), attributs + icônes (T5/T6/T7), UI incluse sur les 2 dashboards (T10), UI ne lisant que le global (T12), règle liste `helpers_indisponibles` > 5 sources appliquée (chauffage 12, eclairage 14).

---

## 3. Constats

| Code | Objet | Écart | Prio |
|---|---|---|---|
| **PARAM-01** | Trou fail-closed — `climatisation` inv9 (blocage horaire) | Les 3 sources non-numériques (`clim_heure_blocage_autom_on`/`_off`, `clim_blocage_horaire_actif`) sont **hors** de la garde `indispo` (`climatisation.yaml:104-105`). Une borne `unavailable` (longueur 11 ≥ 5) est tronquée `[:5]` en `'unava'` (`:102-103`) et traitée comme une heure : `inv9 = blocage and h_on!='' and h_off!='' and h_on==h_off` (`:114`) rend **False** (non signalé, fail-open) si une seule borne manque, et **True à tort** (« blocage permanent ») si les deux manquent. Non-déterministe. Aucun attribut `_indisponible` ni branche `cause` pour ces 3 sources. | **P2** |
| **PARAM-02** | Comparaison directe de chaînes ISO temporelles (interdit contrat) | `eclairage.yaml` (7×, `:135-148`), `modes_maison.yaml` (`:73`), et le slicing d'égalité de `climatisation`. Le contrat interdit explicitement ce pattern et prescrit `as_datetime(...)`. Fail-closed **préservé** ; auto-justifié en-tête (helpers `HH:MM:SS` time-only) pour eclairage/modes_maison ; **fragile** si un helper passe en date+heure. | P3 |
| **PARAM-03** | `climatisation` — en-tête non canonique | Sections hors canevas imposé et **absence de la section obligatoire `📊 ATTRIBUTS EXPOSÉS`** (`climatisation.yaml:1-83`). Les 9 invariants listés sont bien tous évalués (pas d'écart de couverture). | P3 |
| **PARAM-04** | Angles morts du checker (couverture, pas défaut runtime) | T8 ne capte que `\| float(0)` / `\| int(0)` **littéraux**. Il ne détecte NI la sémantique fail-closed (source lue dans un invariant mais absente de la garde `indispo` — PARAM-01), NI les comparaisons de chaînes ISO (PARAM-02), NI l'en-tête non canonique (PARAM-03). D'où un trou invisible en CI (checker vert). | P3 |

### Détail porteur — PARAM-01 (scénarios vérifiés)

[FAIT] `climatisation.yaml` : `indispo` (`:104-105`) = OR des 8 `input_number is none` **seulement**. `inv9` (`:114`) dépend de `blocage`, `h_on`, `h_off` — non couverts.

- **Scénario fail-open (dangereux) :** `clim_blocage_horaire_actif=on`, `..._on=unavailable`, `..._off=08:00:00`. Alors `h_on='unava'`, `h_off='08:00'` → `inv9 = on and True and True and ('unava'=='08:00')` = **False**. Le blocage est actif avec une borne absente — incohérence réelle **non signalée**, `cause`=`none`.
- **Scénario faux positif :** les deux bornes `unavailable` → `h_on='unava'`, `h_off='unava'` → `inv9` = **True** → signalé « blocage_horaire_permanent » (24 h) à tort.

[RECO] Intégrer les 3 sources à une garde d'indisponibilité forçant `inv9` (et l'état) à vrai quand une borne manque, exposer leur indisponibilité (`cause` + attribut `_indisponible`), et remplacer le slicing par `as_datetime(...)` gardé (modèle `vacances`).

---

## 4. Priorisation des suites (aucune appliquée — arbitrage propriétaire requis)

**P2 :**
1. **PARAM-01** : réparer le fail-closed de `climatisation` inv9 (garde d'indisponibilité des 3 sources non-numériques).

**P3 :**
2. **PARAM-04** : durcir le checker — détecter toute source lue dans un invariant mais absente de la garde d'indisponibilité ; interdire les comparaisons de chaînes datetime brutes. Aurait capté PARAM-01 et PARAM-02.
3. **PARAM-02** : migrer eclairage/modes_maison/climatisation vers `as_datetime(...)` (ou acter formellement la dérogation `HH:MM:SS`).
4. **PARAM-03** : réaligner l'en-tête de `climatisation` sur le canevas normatif.

---

## 5. Statut

- Audit : **lecture seule** — aucun runtime, contrat ou checker modifié.
- Domaine : **sain, non clôturé** ; constats `PARAM-01…04` ouverts, arbitrage propriétaire requis.
