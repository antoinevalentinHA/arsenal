# 🧠 ARSENAL — CONTRAT CAPTEURS DE PARAMÉTRAGE CANONIQUE · Références thermiques métier — Consignes durables (confort / réduite / vacances)
# Domaine : Chauffage / Paramétrage durable & références thermiques
# Couche  : Réglages non causaux du moteur thermique (role = parametre)
# Statut  : STRUCTURANT — FRONTIÈRE DES RÉFÉRENCES THERMIQUES MÉTIER
#
# 🎯 Rôle global :
#   Définir la COUCHE DE PARAMÉTRAGE CANONIQUE du moteur Chauffage Arsenal.
#
#   Cette couche regroupe exclusivement les RÉFÉRENCES THERMIQUES MÉTIER
#   DURABLES, c'est-à-dire les consignes-cibles stockées de manière
#   persistante et lues par les pipelines thermiques :
#     - la consigne de régime CONFORT,
#     - la consigne de régime RÉDUIT,
#     - la consigne de régime VACANCES.
#
#   Elle constitue la FRONTIÈRE OFFICIELLE ENTRE :
#     - le STOCKAGE persistant d'une valeur-cible métier,
#     - et toute INTERPRÉTATION, DÉCISION ou ACTION qui s'appuie sur elle.
#
# 🧱 Frontière d'autorité protégée :
#   RÉFÉRENCES THERMIQUES MÉTIER DURABLES (valeurs-cibles persistantes)
#
#   Cette couche :
#     - ne décide jamais d'un régime,
#     - n'autorise jamais une chauffe,
#     - ne bloque jamais une exécution,
#     - ne calcule rien,
#     - ne pilote aucun matériel,
#     - n'interprète pas sa propre valeur,
#   mais FOURNIT des valeurs-cibles stables à la chaîne décisionnelle.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Confondre stockage et décision
#   - Interpréter implicitement la valeur stockée
#   - Considérer une consigne comme un ordre direct de chauffe
#   - Déclencher le chauffage depuis ces helpers
#   - Implémenter une logique d'arbitrage thermique dans cette couche
#   - Écrire une consigne hors d'une autorité identifiée / gouvernée
#   - Porter une causalité métier autonome (role = parametre)
#
# 🔒 Garanties exigées :
#   - Stockage persistant uniquement (mémoire de réglage)
#   - Valeurs-cibles thermiques bornées et exprimées en °C
#   - Aucun calcul, aucune logique locale, aucun comportement autonome
#   - Écriture par une autorité identifiée et gouvernée
#   - Reload-safe / restart-safe / runtime-safe
#   - Absence totale d'effet matériel direct
#
# 🔗 Autorités amont légitimes (écriture gouvernée) :
#   - Réglage utilisateur via le dashboard réglages chauffage (confort / réduite / vacances)
#   - Pipeline d'adaptation Vacances (consigne vacances) — voir 66 / 80
#
# 🔗 Autorités aval autorisées (lecture seule) :
#   - Décision centrale Chauffage (30) et table canonique (80)
#   - Autorisation thermostat (70) et hystérésis confort
#   - Sémantique des régimes comfort / reduced (90)
#   - Auto-ajustement supervisé (06) — lecture comme référence amont
#   - Diagnostics structurants (07) et observabilité
#
# ⚠️ Risques systémiques surveillés :
#   - Glissement « stockage → décision » (consigne traitée comme ordre)
#   - Écriture par une autorité non identifiée ou non gouvernée
#   - Dérive sémantique entre consigne stockée et régime appliqué
#   - Logique d'arbitrage introduite clandestinement dans la couche
#   - Écriture par une autorité d'apprentissage (06 ne doit que proposer)
#
# 🔒 Statut d'autorité :
#   FRONTIÈRE DES RÉFÉRENCES THERMIQUES MÉTIER
#   Toute altération impacte directement la cible de tous les régimes thermiques.
#
# ==========================================================

## 🎯 Objet du document

Ce contrat définit la **frontière d'autorité « Paramétrage canonique »** du
moteur thermique Arsenal, telle qu'inscrite à la ligne 05 de
[`index.md`](index.md) (« Paramétrage durable » / « Références thermiques
métier »).

Il formalise, de manière opposable, le statut des **consignes thermiques de
référence** : des **paramètres de réglage persistants**, lus par la chaîne
décisionnelle mais **dépourvus de toute causalité métier autonome**.

Ce document ne crée aucune entité, n'introduit aucune règle runtime nouvelle,
et ne modifie aucune doctrine existante. Il documente le périmètre déjà porté
par les helpers définis dans `03_input_numbers/chauffage/consignes.yaml` et
classés `role: parametre` dans
[`ci/registres_entites.yaml`](../ci/registres_entites.yaml).

### Distinction norme / preuve

- **Norme** = le présent contrat (et la doctrine des registres dont il dérive).
- **Preuve d'exposition utilisateur** = le dashboard réglages chauffage
  (`18_lovelace/dashboards/chauffage/reglages.yaml`), qui **expose** les
  consignes à l'utilisateur mais **ne fait pas autorité**. Le dashboard est une
  surface ; il prouve l'existence d'un point de réglage, il ne définit aucune
  règle.

---

## 🧱 Population canonique de la frontière

Les entités ci-dessous sont les **références thermiques métier durables** du
domaine Chauffage. Toutes sont des `input_number` persistants, exprimés en
`°C`, sans logique locale. Les bornes citées reflètent leur définition runtime
actuelle (réglage, non normatif au sens causal).

### 🔒 `input_number.chauffage_consigne_confort`

- Domaine : Paramétrage durable — référence du régime **comfort**
- Autorité : PARAMÈTRE (réglage, non causal)
- Régime associé : `comfort` (voir [`90_semantique_thermique.md`](../90_semantique_thermique.md) §3.1)

🎯 Rôle :
Stocker la **valeur-cible de température en régime confort**. Lue par la chaîne
de décision et l'autorisation thermostat ; jamais interprétée localement.

🧭 Périmètre :
- Bornes runtime : `min 17` / `max 25` / `step 1` °C
- Écriture : réglage utilisateur via le dashboard réglages chauffage (autorité gouvernée)
- Lecture : décision centrale (30/80), autorisation thermostat (70)

### 🔒 `input_number.chauffage_consigne_reduite`

- Domaine : Paramétrage durable — référence du régime **reduced**
- Autorité : PARAMÈTRE (réglage, non causal)
- Régime associé : `reduced` (voir [`90_semantique_thermique.md`](../90_semantique_thermique.md) §3.2)

🎯 Rôle :
Stocker la **valeur-cible de température en régime réduit** (sobriété nominale).

🧭 Périmètre :
- Bornes runtime : `min 12` / `max 20` / `step 1` °C
- Écriture : réglage utilisateur via le dashboard réglages chauffage (autorité gouvernée)
- Lecture : décision centrale (30/80), autorisation thermostat (70)

### 🔒 `input_number.chauffage_consigne_vacances`

- Domaine : Paramétrage durable — référence du régime **vacances**
- Autorité : PARAMÈTRE (réglage, non causal)
- Contrat causal de référence : `80_table_decision_canonique__reecriture_partielle.md` §Vacances, [`66_adaptation_consigne_vacances.md`](../66_adaptation_consigne_vacances.md)

🎯 Rôle :
Stocker la **valeur-cible de température applicable en mode Vacances**.

🧭 Périmètre :
- Bornes runtime : `min 12` / `max 20` / `step 1` °C
- Écriture : **pipeline d'adaptation Vacances gouverné** (66 / 80) ; réglable aussi via le dashboard réglages chauffage
- Lecture : décision centrale (30/80)

> **Note de frontière.** Les autres entités `role: parametre` du domaine
> (offsets d'hystérésis `chauffage_offset_on/off`, seuils extérieurs
> `chauffage_seuil_ext_on/off`) partagent exactement la **même doctrine
> non-causale**, mais relèvent de la **frontière d'autorisation** :
> leur contrat causal est [`70_autorisation_thermostat.md`](../70_autorisation_thermostat.md).
> Ils ne sont pas des « références thermiques métier » et ne sont donc **pas**
> régis par le présent document. Énumération souveraine :
> section `parametres:` de [`ci/registres_entites.yaml`](../ci/registres_entites.yaml).

---

## 🧷 Slot connexe — sauvegarde de la consigne réduite (aligné au registre)

L'entité `input_number.chauffage_consigne_reduite_sauvegarde` existe réellement
dans `03_input_numbers/chauffage/consignes.yaml` (`min 0` / `max 20` / `step 1`
°C) et sert de **slot de sauvegarde** de la consigne réduite (sentinelle `0` =
aucune sauvegarde active). Son contrat causal souverain est
[`66_adaptation_consigne_vacances.md`](../66_adaptation_consigne_vacances.md) ;
elle est écrite par `consigne_vacances` et lue/réinitialisée par
`consigne_fin_vacances`.

Elle est désormais **déclarée** dans la section `parametres:` de
[`ci/registres_entites.yaml`](../ci/registres_entites.yaml) avec
`role: parametre` (réglage non causal), au même titre que les trois consignes
de régime.

Elle n'appartient toutefois **pas** à la population canonique des **références
thermiques métier** de la frontière 05 : ce n'est pas une cible de régime mais
une **mémoire interne de sauvegarde/restauration**, et elle n'est **pas
exposée** dans le dashboard réglages chauffage.

**Statut retenu :** slot de sauvegarde **aligné au registre** (`role:
parametre`), hors population canonique des références de régime.

---

## 🧠 Nature doctrinale — `role: parametre`

Conformément à la section `parametres:` du registre canonique, ces entités :

- portent le rôle **`parametre`** (réglage), et **non** un registre décisionnel ;
- sont **`exclus_invariants_registre: true`** : exclues des motifs D1/D3 et de la
  notion de niveau ;
- **ne portent aucune causalité métier autonome** : elles sont lues, jamais
  obéies en tant qu'ordre ;
- sont déclarées au registre **uniquement** pour que le lint structurel (META-1)
  ne les traite pas comme entités fantômes.

En cas de divergence entre le registre `.yaml` et un contrat markdown, **le
contrat markdown fait foi** (règle D-REG-7). Le présent contrat est la référence
markdown opposable de la couche de paramétrage thermique.

---

## 🔒 Invariants normatifs

Ces invariants formalisent, sans les étendre, les interdits déjà déclarés par
`consignes.yaml` et la doctrine des registres.

- **INV-PARAM-1 — Stockage ≠ décision.** Une consigne est une valeur-cible
  stockée ; elle ne constitue jamais, par elle-même, un ordre de chauffe ni une
  décision de régime.
- **INV-PARAM-2 — Non-interprétation locale.** Aucune logique d'arbitrage,
  aucun calcul et aucun comportement autonome ne résident dans cette couche.
- **INV-PARAM-3 — Causalité interdite.** Aucune entité de paramétrage ne
  déclenche directement le chauffage ni n'autorise une exécution.
- **INV-PARAM-4 — Écriture gouvernée.** Toute écriture d'une consigne s'effectue
  via une **autorité identifiée et gouvernée** (réglage utilisateur du dashboard
  réglages chauffage, ou pipeline d'adaptation Vacances), à l'exclusion de toute
  écriture opportuniste ou anonyme.
- **INV-PARAM-5 — Lecture seule en aval.** Les couches décision (30/80),
  autorisation (70) et apprentissage (06) **lisent** ces références sans les
  écrire ; l'auto-ajustement supervisé (06) ne fait que **proposer**.
- **INV-PARAM-6 — Cohérence sémantique.** Chaque consigne est rattachée au
  régime qu'elle paramètre (`comfort`, `reduced`, `vacances`) tel que défini par
  [`90_semantique_thermique.md`](../90_semantique_thermique.md) ; aucune
  redéfinition de régime n'a lieu ici.

> **Note de prudence (traçabilité).** `consignes.yaml` déclare parmi ses
> interdits « écrire sans traçabilité vers l'auteur de l'écriture ». Il s'agit
> d'un **objectif déclaré par le helper**, non d'une garantie runtime vérifiée :
> aucun mécanisme de traçabilité d'auteur n'est constaté dans le code à ce jour.
> Le présent contrat exige donc une écriture par autorité **identifiée et
> gouvernée** (INV-PARAM-4), sans présumer d'une journalisation d'auteur tant
> qu'elle n'est pas implémentée.

---

## 🧭 Frontières d'autorité

| Sens | Autorité | Droit |
|---|---|---|
| Amont (écriture) | Réglage utilisateur — dashboard réglages chauffage | Consignes confort / réduite / vacances |
| Amont (écriture) | Pipeline Vacances (66 / 80) | Consigne vacances |
| Aval (lecture) | Décision centrale (30) / table canonique (80) | Lecture seule |
| Aval (lecture) | Autorisation thermostat (70) | Lecture seule |
| Aval (lecture) | Auto-ajustement supervisé (06) | Lecture seule (proposition) |
| Aval (lecture) | Diagnostics / observabilité (07) | Lecture seule |

Toute écriture par une autorité non listée en amont, ou tout usage de ces
helpers comme déclencheur direct, constitue une **violation de gouvernance
thermique** au sens de [`index.md`](index.md).

---

## 🔗 Renvois canoniques

- Sémantique des régimes : [`90_semantique_thermique.md`](../90_semantique_thermique.md)
- Décision centrale : [`30_decision_centrale.md`](../30_decision_centrale.md), [`80_table_decision_canonique.md`](../80_table_decision_canonique.md)
- Autorisation & hystérésis (paramètres voisins) : [`70_autorisation_thermostat.md`](../70_autorisation_thermostat.md)
- Adaptation Vacances : [`66_adaptation_consigne_vacances.md`](../66_adaptation_consigne_vacances.md)
- Apprentissage supervisé (consommateur aval) : [`06_capteurs_auto_ajustement_calibration.md`](06_capteurs_auto_ajustement_calibration.md)
- Classification souveraine des entités : [`ci/registres_entites.yaml`](../ci/registres_entites.yaml) (section `parametres:`)
- Table d'orientation : [`index.md`](index.md)
- **Preuve d'exposition utilisateur (runtime/UI, non normative)** : `18_lovelace/dashboards/chauffage/reglages.yaml`

---

## 🔒 Statut

- **Document NORMATIF — frontière d'autorité unique** (paramétrage canonique).
- Ne crée aucune entité, ne modifie aucun code, n'étend aucune règle runtime.
- Source de vérité markdown opposable pour la couche `role: parametre` thermique
  (D-REG-7).
