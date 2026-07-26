# Cadrage — Mode manuel supervisé pour le déshumidificateur cave (autorité de domaine)

**Type :** note de décision (conception). **Chantier :** C40 — Autorité de domaine appliquée au
déshumidificateur cave. **Doctrine :** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md).
**Patrons :** pilotes VMC (C36), climatisation (C37), chauffage (C39) — tous clos, terrain validé.
**Statut :** décisions **actées propriétaire (2026-07-26)** ; contrat spécifié (§2). **Aucun runtime
modifié par ce document.**

---

## 0. Objet

L'ouverture C40 ([`chantier_autorite_de_domaine_deshumidificateur.md`](../../04_chantiers/deshumidificateur/chantier_autorite_de_domaine_deshumidificateur.md))
a posé la contradiction (souveraineté d'observation permanente implicite, **sans** doc de gouvernance
des autorités) et tranché le **pivot §5.1 = OUI**. Ce cadrage **acte les décisions D1–D10** et **spécifie
le contrat à écrire** (§2). Il précède le contrat ; il ne l'écrit pas.

---

## 1. Décisions d'arbitrage

### D1 (§5.1) — Le déshumidificateur reçoit un mode manuel supervisé. **OUI.** *(propriétaire)*
Régime manuel conforme aux invariants INV-AUT-1..7 : l'utilisateur devient **titulaire**, sa commande
devient la **décision exécutoire**, la décision machine (`demarrage_recommande`) se rétrograde en
**décision théorique non exécutoire** (INV-AUT-4), sans casser l'unicité ni permettre de reprise
silencieuse.

### D2 (§5.2) — Surface = **binaire `{marche, arrêt}`** (`{on, off}`). *(propriétaire)*
Aucun mode/vitesse (l'appareil n'en a pas).

### D3 (§5.3) — Portée = **mono-appareil (cave)**. *(propriétaire)*
Un seul `switch.deshumidificateur`, une seule vérité `binary_sensor.deshumidificateur_actif`.

### D4 (§5) — Modèle d'autorité = **instanciation du patron Arsenal validé** (pas ex nihilo libre).
Titulaire · consigne manuelle `{on, off}` · décision automatique théorique
(`demarrage_recommande`) · décision exécutoire dérivée anti-fallback · transitions atomiques ·
retour explicite à l'automatique · consommateur exécutoire unique · écrivain physique unique. La
**gouvernance d'autorité absente est créée** par le contrat (instanciation du patron, modèle
[`ecs/02_gouvernance_autorites_et_chaine.md`](../../../contrats/ecs/02_gouvernance_autorites_et_chaine.md)).

### D5 (§5.5) — Min-off = **politique d'usage, NON opposable au manuel.** *(qualifié par preuve corpus)*
Le contrat classe le délai et le timer de blocage en « politique d'usage — non invariante », « Autorité :
aucune », réglable de 0 à 180 min. **Aucune** protection matérielle démontrée. ⟹ reste dans la décision
**automatique** (catégorie B) et **ne contraint pas le titulaire manuel**. **Requalification future =
preuve matérielle explicite** (datasheet / contrainte compresseur).

### D5-bis (précision 1) — Min-on = **politique d'usage, NON opposable au manuel.** *(même méthode/preuve)*
`timer.deshumidificateur_cycle` / `duree_mini_cycle` : mêmes clauses (« politique d'usage — non
invariante », « Autorité : aucune », réglable) ; aucune protection matérielle démontrée. ⟹ **Une
commande manuelle d'arrêt pendant le cycle minimal de marche est exécutoire immédiatement.** Le min-on
ne maintient jamais l'appareil en marche contre une commande manuelle d'arrêt. Symétrique de D5 ;
requalification future = preuve matérielle.

### D6 (§5) — Écrivain physique canonique = **`script.set_deshumidificateur_state`.**
Déjà l'écrivain unique contractuel (guard + retry + conformité). Aucun changement d'écrivain.

### D7 (§5.8, précision 3-écrivain) — `bot_transaction_execute` : **retrait du support déshumidificateur.**
Couche switchbot générique **dormante / non câblée** (sert `bot_chambre_parents`) ; le déshum figure au
registre mais n'est jamais invoqué. Cible : **retirer les branches `is_deshumidificateur`** + les
helpers dormants associés (`input_boolean.bot_tx_lock_deshumidificateur`,
`timer.bot_tx_cooldown_deshumidificateur`, `counter.bot_tx_failures_deshumidificateur`), **+ garde CI**
interdisant tout routage déshum via cet exécuteur. Résultat : **une seule primitive physique légitime**.
*(Exécuté au pass runtime.)*

### D8 (précision 2) — Devenir de `activation` / `desactivation`.
Après C40, elles **cessent d'appeler `set_deshumidificateur_state`**. Refonte en **producteurs de
décision auto** : elles conservent la discipline de timing auto (stabilité, min-on/min-off en catégorie
B) et **publient la décision auto** (branche « auto » de la décision exécutoire dérivée), sans commander
l'écrivain. La **nouvelle automation d'application** est l'**unique consommateur exécutoire** et
l'**unique appelant fonctionnel** de l'écrivain. `reconciliation_demarrage` est **absorbée** par la
convergence boot de l'application. **Numerus clausus d'appelants** = **{application, retry_on, retry_off}**.

### D9 (précision 3) — Retry face à une décision exécutoire changée.
Avant toute réémission, le retry **relit la décision exécutoire courante** : si elle a **changé** depuis
l'échec → **annulation du retry périmé** ; sinon → réémission de la **valeur exécutoire courante**,
**jamais** un payload historique. **Aucune réémission d'une commande devenue non souveraine.**

### D10 (précision 4) — Durée = **indéfini + restitution explicite SEULEMENT.**
1er périmètre : régime manuel **indéfini jusqu'à restitution explicite**. **Pas d'expiration.**
L'expiration optionnelle (INV-AUT-7) est une **extension future distincte, explicitement hors périmètre**
du contrat initial — non intégrée implicitement. Porteurs sans `initial:`.

---

## 2. Forme du contrat à écrire (spécification — passe suivante)

Un **nouveau contrat** `deshumidificateur/autorite_de_domaine.md` instanciera le patron, mappé au
domaine : titulaire (`input_select.deshumidificateur_titulaire_autorite`) ; consigne manuelle
(`{on, off}`) ; décision exécutoire dérivée anti-fallback (`sensor.deshumidificateur_etat_commande` :
auto = `demarrage_recommande` ; manuel = consigne ; sinon indisponible → abstention) ; primitives
supervisées entrée/retour ; écrivain unique `set_deshumidificateur_state` + **numerus clausus**
{application, retry_on, retry_off} ; min-on/min-off = catégorie B non opposables au manuel (D5/D5-bis) ;
retry souverain (D9) ; durée indéfinie + restitution explicite (D10) ; gouvernance d'autorité créée
(D4) ; retrait du support déshum de `bot_transaction_execute` (D7). Amendements attendus :
`deshumidificateur.md` (souveraineté d'observation **conservée** ; numerus clausus ajouté), `guard.md`
(inchangé).

---

## 3. Séquencement & prochaines étapes
1. **Contrat** — écrire `autorite_de_domaine.md` + note d'amendement sur `deshumidificateur.md`.
2. **Runtime** — échafaudage (titulaire, consigne, décision exécutoire dérivée, primitives) **puis
   bascule** (application = consommateur exécutoire unique ; `activation`/`desactivation` → producteurs
   de décision ; retry souverain ; retrait support `bot_transaction_execute` + garde CI).
3. **UI** — patron autorité d'intention + affichage conditionnel.
4. **Validation terrain**, puis clôture.

---

## 4. Ce que ce cadrage ne décide PAS
- Il n'écrit **aucun** contrat, ne crée **aucun** helper/capteur/script/UI/checker.
- Il ne fige **pas** les entity_id ni les identifiants d'automation (préfixe `1006`, libres ≥ `…0011`).

---

## 5. Renvois
- Ouverture : [`chantier_autorite_de_domaine_deshumidificateur.md`](../../04_chantiers/deshumidificateur/chantier_autorite_de_domaine_deshumidificateur.md)
- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Précédents : [`vmc.md`](../../../contrats/vmc.md) §16 · [`16_autorite_de_domaine_climatisation.md`](../../../contrats/climatisation/16_autorite_de_domaine_climatisation.md) §16 · [`85_autorite_de_domaine_chauffage.md`](../../../contrats/chauffage/85_autorite_de_domaine_chauffage.md)
- Contrats à réconcilier : [`deshumidificateur.md`](../../../contrats/deshumidificateur/deshumidificateur.md) · [`guard.md`](../../../contrats/deshumidificateur/guard.md)
- Écrivain latent : [`switchbot_transactionnel.md`](../../../contrats/switchbot_transactionnel.md)
- Gouvernance (modèle) : [`ecs/02_gouvernance_autorites_et_chaine.md`](../../../contrats/ecs/02_gouvernance_autorites_et_chaine.md)
