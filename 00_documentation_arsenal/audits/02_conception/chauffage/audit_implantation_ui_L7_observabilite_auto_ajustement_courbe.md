# Audit d'implantation UI — Supervision auto-ajustement courbe (P7 / L7)

| Champ | Valeur |
|---|---|
| **Type** | Audit d'implantation UI (lecture seule) — **emplacement, pas contenu** |
| **Domaine** | Chauffage / Observabilité auto-ajustement courbe — phase P7 (supervision) |
| **Statut** | Audit — aucune conception de carte, aucun YAML, aucun patch |
| **Version** | 1.0 |
| **Date** | 2026-07-02 |
| **Cadre** | Lecture seule. Ne traite **pas** les 8 questions Q1–Q8 (relèvent du futur dossier de conception L7). Répond à : *« où poser la supervision, et cette page est-elle une synthèse ou un hub ? »* |

---

## 1. Cartographie Lovelace chauffage (état réel)

### 1.1 Dashboards (clés `dashboards.yaml`)

| Clé de dashboard | Fichier | Rôle |
|---|---|---|
| `chauffage-dashboard` | `dashboards/chauffage/principal.yaml` | Dashboard chauffage **principal** |
| `reglages-chauffage-dashboard` | `dashboards/chauffage/reglages.yaml` | **Pilotage / réglages** (toggles, sliders) |
| `diagnostics-chauffage-dashboard` | `dashboards/chauffage/diagnostic.yaml` | **HUB diagnostic** (synthèse **+** hub) |
| `diagnostics-vannes-dashboard` | `dashboards/chauffage/vannes_thermo.yaml` | Sous-diagnostic **vannes** (mono-vue focalisée) |
| `diagnostics-thermiques-dashboard` | `dashboards/chauffage/diagnostic_thermique.yaml` | Sous-diagnostic **thermique** (multi-sections) |

### 1.2 Graphe de navigation (après résolution `!include`)

```
chauffage-dashboard (principal)
   └─(nav)→ diagnostics-chauffage-dashboard  [HUB : synthèse + hub]
              ├─(badge nav)→ diagnostics-vannes-dashboard      ─(retour)→ hub
              └─(badge nav)→ diagnostics-thermiques-dashboard  ─(retour)→ hub
   (hub ─(retour)→ principal)
```

### 1.3 Nature du hub `diagnostic.yaml` — **hybride**

- **Badges** : Accueil · Navigation · Retour (→ principal) · **Vannes thermostatiques** (→ sous-dashboard) · **Diagnostics thermiques** (→ sous-dashboard) = **5 badges**.
- **Corps (synthèse)** : Capacité d'exécution (Boiler Bridge/brûleur), Mode économique, État global, Météo, Poêle, Aération, Réglage thermique, **et une section « 🔁 Auto-ajustement courbe de chauffe » réduite à UNE carte** (`chauffage_auto_courbe_status_72`, « Dernier ajustement »).

### 1.4 Constats structurants

- **C1 — Le pattern « sous-diagnostic = dashboard autonome rattaché au hub par nav + retour » est déjà établi** (vannes, thermiques). Ce ne sont pas des vues internes mais des dashboards déclarés, reliés au hub par badges.
- **C2 — L'auto-ajustement courbe a déjà une amorce** dans la synthèse du hub : une seule carte « Dernier ajustement ». L'observabilité L1–L6 a depuis produit **~20 entités** (complétude, statut apprenant, cause/épisodes de gel, dérive pente/parallèle, réversions, refus consécutifs, persistance, effet par régime) — **hors de proportion** avec une carte inline.
- **C3 — Le hub est déjà long** (7 sections de synthèse) : la marge d'empilement inline est faible, surtout sur mobile.
- **C4 — Contrat CI `R-LL-NAV-1`** : tout `navigation_path` interne cible une **clé de dashboard** canonique (`/<dashboard-key>`, sans segment de vue) ; **pas de cul-de-sac** ; **retour cohérent** avec les prédécesseurs. → un nouveau sous-dashboard doit être **déclaré** dans `dashboards.yaml` **et** porter un **badge retour** vers le hub.

---

## 2. Comparaison des trois scénarios

> Rappel Arsenal : en pratique, **B et C se ressemblent techniquement** (un sous-diagnostic *est* déjà un dashboard). La vraie différence est le **rattachement** : **B = rattaché au hub** diagnostic (nav + retour, comme vannes/thermiques) ; **C = point d'entrée indépendant** (hors hub).

### A. Intégration inline dans le hub Diagnostics Chauffage

| Critère | Appréciation |
|---|---|
| Cohérence Arsenal | **Faible** — ferait de l'auto-ajustement la seule exception inline, alors que vannes/thermiques sont des sous-dashboards. Rompt l'homogénéité. |
| Lisibilité PC/mobile | **Dégradée** — la synthèse (déjà 7 sections) deviendrait interminable ; illisible sur mobile. |
| Surcharge | **Forte** — hub surchargé (C3). |
| Confusion diag/supervision/pilotage | **Élevée** — noyer une supervision d'apprentissage (8 réponses) dans une synthèse d'état courant brouille les rôles. |
| Maintenance | **Médiocre** — fichier hub géant, includes nombreux. |
| Navigation | Inchangée (0 badge ajouté), mais au prix de la lisibilité. |
| **Verdict** | **À écarter** — sauf pour conserver un *teaser* minimal. |

### B. Sous-dashboard dédié, rattaché au hub *(miroir vannes/thermiques)*

| Critère | Appréciation |
|---|---|
| Cohérence Arsenal | **Forte** — épouse exactement le pattern sous-diagnostic établi (C1). |
| Lisibilité PC/mobile | **Bonne** — page dédiée respirante, sections par question, comme `diagnostic_thermique`. |
| Surcharge | **Nulle sur le hub** — la supervision vit ailleurs ; l'amorce du hub se réduit à un badge/teaser. |
| Confusion | **Faible** — séparation nette : la page dédiée **est** la supervision, distincte de la synthèse (état) et des réglages (pilotage). |
| Maintenance | **Bonne** — un fichier ciblé, homogène avec les deux sous-dashboards existants. |
| Navigation | **+1 badge** sur le hub → 3 sous-diagnostics + 3 badges système = **6 badges** (limite raisonnable) ; `R-LL-NAV-1` satisfait (déclaration + retour). |
| **Verdict** | **RECOMMANDÉ.** |

### C. Dashboard autonome (hors hub)

| Critère | Appréciation |
|---|---|
| Cohérence Arsenal | **Moyenne** — techniquement faisable, mais rompt le **rattachement diagnostic** : un dashboard « hors hub » ne serait plus un sous-diagnostic du chauffage. |
| Lisibilité PC/mobile | **Bonne** (page dédiée). |
| Surcharge | **Nulle**. |
| Confusion | **Risque** — un dashboard « auto-ajustement » autonome peut être **pris pour du pilotage/réglage** (ambiguïté avec `reglages-chauffage-dashboard`), pas de la supervision. |
| Maintenance | **Correcte**, mais **plus d'entrées** de gouvernance (point d'entrée à définir, risque d'orphelin R-LL-NAV). |
| Navigation | Exige un **point d'entrée à décider** (d'où y accède-t-on ?) — plus de latitude, plus de risque de cul-de-sac/orphelin. |
| **Verdict** | **Possible mais moins cohérent que B** — justifié seulement si la supervision devait être partagée **hors** du domaine chauffage (ce n'est pas le cas). |

---

## 3. Verdict d'implantation recommandé

**Scénario B — un sous-dashboard dédié « Diagnostics — Auto-ajustement courbe », rattaché au hub Diagnostics Chauffage par un 3ᵉ badge de navigation (miroir exact de Vannes / Thermiques), avec badge retour vers le hub.**

Justifications :
1. **Homogénéité** : c'est le pattern déjà en place (C1) ; on n'invente rien, on **complète une série**.
2. **Réponse à la question « synthèse ou hub ? »** : le hub **reste hybride** (synthèse + hub) ; l'auto-ajustement en devient le **3ᵉ sous-diagnostic**. Le « bouton de plus » **n'empile pas un contrôle** — il **promeut une amorce déjà présente** (la carte « Dernier ajustement ») vers sa page dédiée. C'est cohérent, non redondant.
3. **Rôles préservés** : la page dédiée est **supervision** (lecture seule, les 8 réponses), **distincte** de `reglages-chauffage` (**pilotage**) et de la synthèse diagnostic (**état courant**). Ne pas y placer de contrôle.
4. **Charge maîtrisée** : 6 badges sur le hub restent lisibles PC/mobile ; `R-LL-NAV-1` respecté (déclaration `dashboards.yaml` + retour).

### Recommandations complémentaires *(pour le futur dossier de conception L7, hors périmètre de cet audit)*

- **Réduire l'amorce inline** du hub (« Auto-ajustement courbe ») à un **teaser compact** (statut + complétude) **pointant vers le sous-dashboard**, pour éviter la double maintenance et le doublon d'affichage (écueil déjà relevé par les suivis d'audit dashboards existants).
- **Tenir la frontière supervision ≠ pilotage** : aucune action/écriture sur la page dédiée ; les toggles restent dans `reglages-chauffage`.
- **Nom de clé** pressenti à confirmer en conception : `diagnostics-courbe-dashboard` (aligné sur `diagnostics-vannes-dashboard` / `diagnostics-thermiques-dashboard`).

---

*Audit d'implantation UI — 2026-07-02. Emplacement uniquement. Aucune conception de carte, aucun YAML, aucun patch. La conception des vues (Q1–Q8, effet borné, bandeau complétude) relève du dossier de conception de lot L7.*
