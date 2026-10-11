# 🔁 ARSENAL — DETTE C56 · Résilience des intégrations — tentative inhibée sans reprise

## 📌 Statut

- **Dette identifiée (2026-10-11), non ouverte — délibérément non ordonnancée. Aucune correction engagée.**
- **Identifiant global** : **C56** — attribué selon la règle de gouvernance du registre (plus grand identifiant existant + 1, après attribution de `C55`), unicité contrôlée sur le dépôt, le registre et l'historique des pull requests GitHub.
- **Domaine** : transverse — résilience des intégrations (contrat [`resilience_integrations.md`](../../../contrats/resilience_integrations.md) §5 invariants 8 et 11, §11).
- **Priorité** : P2 — défaut de reprise borné par le retour constaté, sans incident observé.
- **Origine** : relevé pendant le diagnostic du chantier [C55](c55_rechargement_entrees_entry_id.md), **explicitement exclu de son périmètre** (arbitrage opérateur du 2026-10-11).

---

## 1. Constat (lecture du code, non observé en conditions réelles)

Dans [`10_scripts/system/resilience_integration_recover.yaml`](../../../../10_scripts/system/resilience_integration_recover.yaml), les gardes **panne secteur** (`binary_sensor.panne_secteur_en_cours`) et **contexte WAN** (`wan_entity`, chaînes `cloud_wan`) arrêtent une tentative (`op: attempt`) **avant toute action**. C'est conforme aux invariants 8 et 11.

Lorsque la tentative ainsi inhibée provient de l'**expiration du timer de backoff** d'un épisode ouvert :

- le timer n'est pas réarmé ;
- le compteur reste supérieur à 0 ;
- le binaire de gel ou d'indisponibilité reste `on`, donc ne produit **aucune nouvelle transition**.

Les déclencheurs des automatisations de chaîne étant le gel, l'indisponibilité, l'expiration du backoff et le retour OK, **aucun déclencheur ne relance l'épisode à la levée de la garde**.

## 2. Conséquence

- Si l'intégration récupère d'elle-même à la levée de la garde (cas nominal attendu pour une coupure WAN ou secteur) : `retour_ok` referme l'épisode — **aucun effet**.
- Sinon : l'épisode reste ouvert **sans relance automatique** jusqu'au retour constaté, à une nouvelle transition des axes ou, après le lot 1 de C55, au prochain redémarrage de HA (reprise après stabilisation).

## 3. Ce qui n'est pas décidé

- Le mécanisme de reprise à la levée d'une garde : déclencheur sur la retombée de `binary_sensor.panne_secteur_en_cours` ou de `binary_sensor.contexte_wan_indisponible`, ou réarmement du timer par le script au moment de l'inhibition.
- Son articulation avec le contrat `pannes/internet/30` (stabilisation du retour WAN) et avec la reprise après stabilisation introduite par C55.

## 4. Réveil

Décision opérateur d'ordonnancer, ou constat terrain d'un épisode resté ouvert après la levée d'une garde. Toute correction suit le contrat de résilience (§11) et ne réutilise pas le périmètre de C55.
