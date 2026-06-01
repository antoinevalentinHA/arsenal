# État du domaine Alarme — post-CH-6

> **Nature :** note d'état (synthèse de pilotage) — chantiers Alarme après CH-6
> **État du dépôt à la rédaction :** `origin/main` = `8477062`
> **Sources :** `01_rapports/alarme/audit_alarme_rapport_officiel.md`, `04_chantiers/alarme/backlog_alarme.md`, clôtures `05_clotures/alarme/{cloture_ch1,cloture_ch2,cloture_ch6}_alarme.md`
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Ce qui est soldé

| Chantier | Constats | Statut | Commits runtime |
|----------|----------|--------|-----------------|
| **CH-2** | `ALM-IMP-2`, `ALM-MIN-4` | **SOLDÉ** | `dc8667e`, `99cbc0b` |
| **CH-6** | `ALM-CRIT-3` | **SOLDÉ — validé terrain** | `139640b`, `5f56ee7` |
| **CH-1** | `ALM-CRIT-1`, `ALM-CRIT-2`, `ALM-MIN-5` | **Implémenté au runtime — validation terrain en attente** (clôture conditionnée) | `812f2cf`, `5dda40b`, `fe57c73` |

- **CH-2** : le cerveau est écrivain exclusif de `input_text.alarme_raison` ; code mort retiré.
- **CH-6** : clavier PIN opérant (armement + désarmement validés terrain), plus de notification « badge inconnu » sur saisie PIN. Résidus non bloquants : champ « badge » porteur de la valeur PIN (**R1**, cosmétique) ; flux **badge RFID sans évènement observable** (**R2**, observation distincte d'`ALM-CRIT-3`).
- **CH-1** : arbitrage A1+B2+C1 appliqué (ouvrants d'entrée hors chemin immédiat ; `timer.finished` = preuve d'intrusion ; chemin sonore unique). Validé statiquement ; **scénarios terrain S1–S8 non encore exécutés**.

---

## 2. Ce qui reste

### Constats ouverts

**Critiques — corrigés au runtime, à confirmer en terrain :**
- `ALM-CRIT-1`, `ALM-CRIT-2` *(CH-1)* — clôture définitive conditionnée à la validation terrain.

**Importants :**
- `ALM-IMP-1` — babysitting demi-intégré *(CH-3)*
- `ALM-IMP-3` — auto-extinction sirène : entité non définie + `delay` long *(CH-4)*

**Mineurs :**
- `ALM-MIN-1` — désync déclencheurs/entrées (contexte visite) *(CH-3)*
- `ALM-MIN-2` — double bip désarmement + garde mode test absente *(CH-4)*
- `ALM-MIN-3` — durée de blocage incohérente (5 min / 3 min) *(CH-5)*
- `ALM-MIN-6` — mismatch nom de fichier ↔ identifiant d'entité *(CH-5)*
- `ALM-MIN-5` — *corrigé au runtime (CH-1)*, à confirmer en terrain

**Documentaires :**
- `ALM-DOC-1` — décalage en-têtes/chemins contrats 20/30/40 *(CH-5)*
- `ALM-DOC-2` — notification visiteur documentée mais inexistante *(CH-5)*

**Observation nouvelle (hors catalogue initial) :**
- **R2** — flux badge RFID inerte (aucun évènement observable) ; distinct d'`ALM-CRIT-3`, à trier.

### Chantiers ouverts

- **CH-1** — implémenté, **validation terrain en attente** (amont CH-2 satisfait).
- **CH-3** — non démarré ; amont CH-2 satisfait ; **gated V3** (couverture présence babysitting).
- **CH-4** — non démarré ; dépendance latérale CH-1 **satisfaite** ; **gated V4** (existence de `switch.sirene_alarm`).
- **CH-5** — non démarré ; documentaire ; lots indépendants (DOC-2, MIN-6, MIN-3) + lots de réalignement contractuel en aval.

### Dettes documentaires restantes

- `ALM-DOC-1`, `ALM-DOC-2`, `ALM-MIN-6`, `ALM-MIN-3` *(périmètre CH-5)*.
- **Issues des chantiers livrés, à porter par CH-5 :**
  - en-tête de `delai_entree_fin.yaml` désaligné (sections ROBUSTESSE / DETTE §9 citant `ouverture_qualifiee_maison` et `sirene_brutale`, retirés par CH-1) ;
  - alignement des contrats `50`/`51`/`60`/`70` sur l'arbitrage A1+B2+C1 (CH-1) ;
  - dette §9 résiduelle : court-circuit `alarm_trigger` direct (`…007` / `…009` / `…032`), hors arbitrage, documentée et inchangée ;
  - **R1** : champ « badge » porteur de la valeur PIN (dette sémantique de nommage).

---

## 3. Classement par criticité (travail résiduel)

1. 🔴 **Critique** — **validation terrain de CH-1** : seul critique non confirmé ; risque sécurité résiduel n°1 (voie d'entrée).
2. 🟠 **Important** — **CH-4** (sirène, actionneur terminal) ; **CH-3** (babysitting, occupants vulnérables).
3. 🟡 **Mineur** — MIN-1 (CH-3), MIN-2 (CH-4), MIN-3 / MIN-6 (CH-5), MIN-5 (CH-1, terrain).
4. ⚪ **Documentaire** — DOC-1, DOC-2 + dettes nouvelles → CH-5.
5. ❓ **Observation à trier** — **R2** (RFID inerte) : criticité fonction de l'usage RFID attendu.

---

## 4. Ordre recommandé des travaux

1. **Préalable — validation terrain de CH-1** (scénarios S1–S8 déjà rédigés). Clôt `ALM-CRIT-1`/`CRIT-2`/`MIN-5` et fige la voie d'entrée. Coût faible, gain de criticité maximal.
2. **CH-4 — Sirène & feedback sonore** *(IMP-3, MIN-2)*. Continuité directe de la convergence sonore posée par CH-1 ; actionneur terminal ; défaut concret (entité d'extinction non définie). Préalable léger : **V4**.
3. **CH-3 — Contextes humains** *(IMP-1, MIN-1)*. À débloquer via **V3** (couverture présence babysitting) ; amont CH-2 déjà satisfait.
4. **CH-5 — Cohérence documentaire** *(DOC-1, DOC-2, MIN-3, MIN-6)*. Traiter tôt les **quick wins indépendants** (DOC-2, MIN-6, MIN-3) ; y rattacher les dettes nouvelles (en-tête `delai_entree_fin`, alignement contrats 50/51/60/70, dette §9, R1). Lots de réalignement contractuel **en aval** des chantiers runtime.
5. **En parallèle — trancher R2** (RFID) : décider si l'usage RFID est attendu ; si oui, ouvrir une investigation dédiée (appairage / exposition Zigbee2MQTT), distincte d'`ALM-CRIT-3`.

---

## 5. Synthèse

Sur 6 chantiers : **CH-2 et CH-6 soldés**, **CH-1 implémenté** (terrain en attente), **CH-3 / CH-4 / CH-5 ouverts**. Le domaine **n'est pas clôturé**. La prochaine action à plus forte valeur est la **validation terrain de CH-1** ; le prochain chantier à engager est **CH-4**.

---

*Note d'état post-CH-6. Établie en lecture du dépôt (`origin/main` = `8477062`). Synthèse de pilotage — aucune modification runtime ni contractuelle.*
