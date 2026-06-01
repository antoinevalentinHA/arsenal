# Clôture de chantier — CH-1 Alarme

> **Statut :** clôture de **chantier** — CH-1 **implémenté au runtime** et **validé statiquement** ; **validation terrain NON réalisée** ; clôture définitive **conditionnée** ; domaine **Alarme NON clôturé**
> **Domaine :** `alarme` — détection d'intrusion sur la voie d'accès principale (porte d'entrée, garage)
> **Destination d'archivage :** `00_documentation_arsenal/audits/05_clotures/alarme/cloture_ch1_alarme.md`
> **Documents de référence (en dépôt) :**
> - `00_documentation_arsenal/audits/01_rapports/alarme/audit_alarme_rapport_officiel.md`
> - `00_documentation_arsenal/audits/03_plans_action/alarme/plan_action_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/backlog_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/dossier_conception_CH1_alarme.md`
> - `00_documentation_arsenal/audits/04_chantiers/alarme/plan_implementation_CH1_alarme.md`
> **État du dépôt à la rédaction :** `origin/main` = `fe57c73`. Runtime CH-1 intégré — commits `812f2cf` (A1 / ALM-CRIT-1), `5dda40b` (B2 / ALM-CRIT-2), `fe57c73` (C1 / ALM-MIN-5).
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Acter la clôture documentaire du chantier **CH-1** (sémantique des ouvrants d'entrée & confirmation d'intrusion), après implémentation runtime et validation statique. La **validation terrain n'ayant pas été réalisée**, ce document **ne prononce pas** la clôture définitive de CH-1 ni celle du domaine Alarme (cf. §6 et §9).

---

## 2. Constats traités

| Constat | Gravité | Énoncé |
|---------|---------|--------|
| **ALM-CRIT-1** | 🔴 Critique | Ouvrants d'entrée (porte, garage) présents dans le chemin de déclenchement **immédiat** (`autres.yaml`), protégés seulement par un garde sujet à une **course** avec la chaîne du timer → faux positif non déterministe à l'entrée légitime. |
| **ALM-CRIT-2** | 🔴 Critique | Le garde de **fin de délai** exigeait `ouverture_qualifiee_maison == on`, capteur excluant structurellement porte et garage (sémantique aération/M5) → **faux négatif** : intrusion par la voie principale non sanctionnée à l'expiration. |
| **ALM-MIN-5** | 🟡 Mineur | Double invocation de `sirene_brutale` en fin de délai (appel direct **plus** chemin `triggered → sirene_forte`). |

---

## 3. Arbitrage retenu

**A1 + B2 + C1** (fixé en amont, non rediscuté) :
- **A1** — Sortir la porte d'entrée et le garage du **chemin immédiat** ; ils ne sont plus couverts que par le **délai d'entrée**.
- **B2** — `timer.finished` (sur `timer.delai_entree`) constitue **à lui seul** la preuve d'une intrusion non désarmée ; le garde d'ouverture instantanée disparaît de la fin de délai (gardes `systeme_stable` + `armed_away` conservées). Socle de validité : `timer_cancel` annule le timer au désarmement.
- **C1** — Chemin sonore **unique** via l'état `triggered → sirene_forte` ; suppression de l'appel direct à `sirene_brutale` en fin de délai.

---

## 4. Travaux réalisés

| Lot | Objet | Constat | Commit |
|-----|-------|---------|--------|
| **A1** | Retrait des déclencheurs `contact_entree_porte` / `contact_garage` du chemin immédiat | ALM-CRIT-1 | `812f2cf` |
| **B2** | Retrait du garde `ouverture_qualifiee_maison` en fin de délai | ALM-CRIT-2 | `5dda40b` |
| **C1** | Suppression de l'appel sirène direct (chemin sonore unique) | ALM-MIN-5 | `fe57c73` |

Fichiers runtime concernés (2) : `11_automations/alarme/intrusion/ouverture/autres.yaml` (`1002000000007`), `11_automations/alarme/intrusion/ouverture/delai_entree_fin.yaml` (`10020000000032`). Aucun helper créé/supprimé, aucun capteur modifié, aucun timer modifié. `binary_sensor.ouverture_qualifiee_maison` conservé (consommateurs aération/M5 intacts).

---

## 5. Validations réalisées

**Statiques — réalisées :**
- Parse YAML OK ; `yamllint` (config dépôt) OK (seuls des avertissements `trailing-spaces` **préexistants** dans le corps des notifications d'`autres.yaml`, hors diff).
- Application **séquentielle** des trois patchs sur base propre (`git apply --check` puis `git apply`) OK.
- **IDs d'automatisation inchangés** : `1002000000007`, `10020000000032`.
- **Arbitrage respecté exactement** : ouvrants d'entrée absents des déclencheurs immédiats ; garde `ouverture_qualifiee_maison` fonctionnel supprimé ; appel `sirene_brutale` fonctionnel supprimé (appelant unique restant : `sirene_forte`).
- **Aucune modification parasite** : exactement 2 fichiers runtime, aucun fichier documentaire/contrat/audit/index touché par les patchs.

**Terrain — NON réalisée :** les scénarios `S1`–`S8` du plan d'implémentation restent à exécuter (entrée légitime sans déclenchement immédiat ; désarmement à temps ; expiration sans désarmement → sirène unique ; garage ; ouvrant non-entrée toujours immédiat ; mode test sans sirène réelle ; non-régression mouvement ; bords reboot/concurrence).

---

## 6. Statut de CH-1

**Implémenté au runtime et validé statiquement ; validation terrain en attente.** Le chantier **n'est pas clôturé définitivement** : sa clôture est **conditionnée** à l'exécution favorable des scénarios terrain `S1`–`S8`.

---

## 7. Élimination des constats (au plan statique/structurel)

- **ALM-CRIT-1 — éliminé par A1** : la porte et le garage ne sont plus des déclencheurs du chemin immédiat ; la course n'a plus d'objet. *Confirmation comportementale = `S1`/`S4`.*
- **ALM-CRIT-2 — éliminé par B2** : la fin de délai ne dépend plus du capteur aveugle ; `timer.finished` (avec `systeme_stable` + `armed_away`) suffit. *Confirmation = `S3`.*
- **ALM-MIN-5 — éliminé par C1** : appelant unique de `sirene_brutale` = `sirene_forte`. *Confirmation = `S6`.*
- **Aucune nouvelle fenêtre aveugle** au plan d'analyse (grâce pendant le délai inchangée, déclenchement à l'échéance, ouvrants non-entrée et mouvement inchangés, garde reboot conservée). *Confirmation = `S5`/`S8`.*

---

## 8. Reste à faire & impacts

- **Condition de clôture définitive de CH-1** : validation terrain `S1`–`S8`.
- **Dette documentaire en attente (hors périmètre runtime CH-1)** : l'en-tête commenté de `delai_entree_fin.yaml` (sections ROBUSTESSE / DETTE §9) référence encore `ouverture_qualifiee_maison` et `sirene_brutale` (supprimés du corps) ; à réaligner avec les contrats `50`/`51`/`60`/`70` au titre du lot documentaire **CH-5**.
- **Dette §9 résiduelle, inchangée** : le court-circuit **panneau** (`alarm_trigger` appelé directement par `…007`, `…009`, `…032`) n'est **pas** dans le périmètre A1+B2+C1 ; C1 n'a supprimé que le doublon **sonore**.
- **Chantiers restants du domaine** : **CH-3** (`ALM-IMP-1` babysitting), **CH-4** (`ALM-IMP-3` sirène / auto-extinction), **CH-5** (documentaire — dont `ALM-DOC-1`), **CH-6** (`ALM-CRIT-3` PIN clavier).

---

## 9. Verdict

**CH-1 implémenté au runtime et validé statiquement — validation terrain en attente — chantier non clôturé définitivement.** Le domaine **Alarme reste NON clôturé**. Conformément au principe directeur, le runtime est la référence ; l'alignement des contrats et des en-têtes suivra (CH-5).

---

*Clôture de chantier CH-1 Alarme. Établie en lecture du dépôt (`origin/main` = `fe57c73`) ; acte documentaire sans modification du runtime ni des contrats. Validation terrain non réalisée : clôture conditionnée.*
