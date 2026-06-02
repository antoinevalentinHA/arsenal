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
| **CH-1** | `ALM-CRIT-1`, `ALM-CRIT-2`, `ALM-MIN-5` | **Clôture conditionnelle acquise** — réserve : test positif `S3` | `812f2cf`, `5dda40b`, `fe57c73` |

- **CH-2** : le cerveau est écrivain exclusif de `input_text.alarme_raison` ; code mort retiré.
- **CH-6** : clavier PIN opérant (armement + désarmement validés terrain), plus de notification « badge inconnu » sur saisie PIN. Un armement clavier en **présence active** est immédiatement suivi d'un **désarmement par la logique de présence** — comportement **attendu**, non un échec du flux clavier. Résidus non bloquants : champ « badge » porteur de la valeur PIN (**R1**, cosmétique) ; flux **badge RFID sans évènement observable** (**R2**, observation distincte d'`ALM-CRIT-3`).
- **CH-1** : arbitrage A1+B2+C1 appliqué (ouvrants d'entrée hors chemin immédiat ; `timer.finished` = preuve d'intrusion ; chemin sonore unique). **Validé statiquement + protégé CI (`N5`-`N7`)** ; **garanties négatives observées en production** (entrée réelle sans faux positif `S1`, désarmement annulant le délai `S2`). **Réserve unique** : test positif d'expiration volontaire (`S3`).

---

## 2. Ce qui reste

### Constats ouverts

**Critiques — corrigés au runtime, à confirmer en terrain :**
- `ALM-CRIT-1` *(CH-1)* — garantie négative acquise (statique + CI + terrain observé). `ALM-CRIT-2` *(CH-1)* — détection à l'échéance non établie par l'observation : clôture définitive conditionnée au **seul test positif `S3`**.

**Importants :**
- `ALM-IMP-1` — babysitting demi-intégré *(CH-3)*

**Mineurs :**
- `ALM-MIN-1` — désync déclencheurs/entrées (contexte visite) *(CH-3)*
- `ALM-MIN-2` — double bip désarmement + garde mode test absente *(CH-4-A : implémenté + déployé `5892d35` ; validation terrain en attente)*
- `ALM-MIN-3` — durée de blocage incohérente (5 min / 3 min) *(CH-5)*
- `ALM-MIN-6` — mismatch nom de fichier ↔ identifiant d'entité *(CH-5)*
- `ALM-MIN-5` — *corrigé au runtime (CH-1)*, à confirmer en terrain
- `ALM-IMP-3` — *requalifié Important → Mineur (post-V4)* : auto-extinction réelle côté device, **reboot-safe** ; résidu = code mort + dette de représentation *(CH-4)*

**Documentaires :**
- `ALM-DOC-1` — décalage en-têtes/chemins contrats 20/30/40 *(CH-5)*
- `ALM-DOC-2` — notification visiteur documentée mais inexistante *(CH-5)*

**Observation nouvelle (hors catalogue initial) :**
- **R2** — flux badge RFID inerte (aucun évènement observable) ; distinct d'`ALM-CRIT-3`, à trier.

### Chantiers ouverts

- **CH-1** — **clôture conditionnelle acquise** ; réserve unique : test positif `S3` (amont CH-2 satisfait).
- **CH-3** — non démarré ; amont CH-2 satisfait ; **gated V3** (couverture présence babysitting).
- **CH-4** — **engagé, non clôturé**. Dépendance latérale CH-1 **satisfaite** ; **V4 réalisée** → `ALM-IMP-3` requalifié Mineur. **Lot CH-4-A (`ALM-MIN-2`)** : **implémenté + déployé** (`5892d35`, pull + reload) ; **validation terrain opportuniste en attente**. **Lot CH-4-B (`ALM-IMP-3`, dette/gouvernance)** : **restant**.
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

1. 🔴 **Critique** — **test positif `S3` de CH-1** : seule garantie (positive, `ALM-CRIT-2`) non confirmée ; garanties négatives déjà acquises (statique + CI + terrain observé).
2. 🟠 **Important** — **CH-3** (babysitting, occupants vulnérables).
3. 🟡 **Mineur** — MIN-1 (CH-3), MIN-2 (CH-4-A implémenté/déployé, validation en attente), MIN-3 / MIN-6 (CH-5), MIN-5 (CH-1, terrain) ; **`ALM-IMP-3` requalifié post-V4 (CH-4, dette/gouvernance)**.
4. ⚪ **Documentaire** — DOC-1, DOC-2 + dettes nouvelles → CH-5.
5. ❓ **Observation à trier** — **R2** (RFID inerte) : criticité fonction de l'usage RFID attendu.

---

## 4. Ordre recommandé des travaux

1. **Préalable — test positif `S3` de CH-1** (expiration volontaire du délai → `triggered` + sirène unique en mode test). Seul élément restant pour la clôture définitive ; les garanties négatives sont déjà acquises (statique + CI + terrain observé). Coût faible, gain de criticité maximal.
2. **CH-4 — Sirène & feedback sonore** *(MIN-2 ; `ALM-IMP-3` requalifié Mineur post-V4)*. **V4 réalisée** : auto-extinction device reboot-safe confirmée → IMP-3 sans enjeu sécurité (dette technique : retrait du code mort `stop.yaml` / entité fantôme + documentation du mécanisme device). MIN-2 (double bip / fuite mode test / bip sur auto-désarmement) **traité en lot CH-4-A** : **implémenté + déployé** (`5892d35`), **validation terrain en attente**. Reste le **lot CH-4-B** (IMP-3 : retrait du code mort + documentation de la durée device). Chantier **bas risque, ~100 % distant**, **non clôturé**.
3. **CH-3 — Contextes humains** *(IMP-1, MIN-1)*. À débloquer via **V3** (couverture présence babysitting) ; amont CH-2 déjà satisfait.
4. **CH-5 — Cohérence documentaire** *(DOC-1, DOC-2, MIN-3, MIN-6)*. Traiter tôt les **quick wins indépendants** (DOC-2, MIN-6, MIN-3) ; y rattacher les dettes nouvelles (en-tête `delai_entree_fin`, alignement contrats 50/51/60/70, dette §9, R1). Lots de réalignement contractuel **en aval** des chantiers runtime.
5. **En parallèle — trancher R2** (RFID) : décider si l'usage RFID est attendu ; si oui, ouvrir une investigation dédiée (appairage / exposition Zigbee2MQTT), distincte d'`ALM-CRIT-3`.

---

## 5. Synthèse

Sur 6 chantiers : **CH-2 et CH-6 soldés**, **CH-1 en clôture conditionnelle acquise** (réserve : test positif `S3`), **CH-3 / CH-4 / CH-5 ouverts**. Le domaine **n'est pas clôturé**. La prochaine action à plus forte valeur est le **test positif `S3`** ; **CH-4 est engagé** (désormais **dette technique / gouvernance + hygiène feedback** après requalification d'`ALM-IMP-3`) : **lot CH-4-A (`ALM-MIN-2`) implémenté + déployé** (`5892d35`), **validation terrain en attente** ; **lot CH-4-B (`ALM-IMP-3`) restant**. CH-4 **non clôturé**.

---

*Note d'état post-CH-6. Établie en lecture du dépôt (`origin/main` = `8477062`). Synthèse de pilotage — aucune modification runtime ni contractuelle.*
