# Arsenal — Changelog du chantier CH-5

**Chantier** : CH-5 — Cartographie des dépendances inter-domaines (Chauffage)
**Domaine** : Chauffage
**Date** : 2026-05-30
**État** : clos — document de référence livré, 0 invariant CI (liaison différée), 0 modification du runtime Chauffage

---

## Résumé architectural

CH-5 solde la dette D8 : l'absence de document transversal recensant les
couplages d'entités qui franchissent la frontière du domaine Chauffage. Un
refactor Chauffage pouvait jusqu'ici casser un consommateur situé dans un autre
domaine — ou l'inverse — sans qu'aucun fichier du domaine ne le signale. CH-5
supprime cet angle mort par une **cartographie de référence**, descriptive et
non doctrinale.

Le chantier est **purement documentaire**. Il ne touche ni le runtime, ni les
contrats d'autorité, ni la CI. Il n'introduit aucun invariant : la liaison CI
(`R-DEP-x`) est explicitement différée. La règle métier de chaque couplage
demeure portée par son contrat d'autorité ; ce document **renvoie** sans jamais
redéfinir.

Le livrable établit un fait de gouvernance que la description d'origine de D8
sous-estimait : la surface de couplage boiler ↔ chauffage n'est pas réductible à
un seul `binary_sensor.boiler_bridge_online`, mais englobe toute la surface
transactionnelle d'ACK régie par les contrats `boiler/`.

---

## 1. Livrable

### Document de cartographie (`contrats/chauffage/dependances_inter_domaines.md`)
Cartographie de référence du domaine Chauffage, subordonnée à
`00_gouvernance_chauffage.md`. Nature explicite : **descriptive, non
normative**. En cas de divergence avec un contrat d'autorité, le contrat prime ;
en cas de divergence avec le runtime, le runtime prime et la cartographie est à
corriger.

Deux directions documentées :

- **Direction A** — entités possédées par le Chauffage, lues par d'autres
  domaines (aération, climatisation, poêle, boiler, météo).
- **Direction B** — entités possédées par d'autres domaines, lues par le
  Chauffage (boiler transactionnel, poêle, météo, présence, ouvertures, modes).

La propriété d'une entité est établie par l'arborescence de **définition**
(`unique_id` / déclaration de l'helper), pas par son nom. Plusieurs entités au
nom trompeur sont requalifiées en conséquence.

---

## 2. Couplages recensés

### Couplages critiques (chemin de décision ou d'exécution)
- `input_boolean.chauffage_blocage_aeration` — chauffage → aération **et**
  climatisation. Point de couplage le plus dense du domaine, et entité reclassée
  par CH-2 (Niveau 1 → Niveau 2). Tout changement de sémantique impacte
  simultanément la production (aération) et un consommateur tiers (climatisation).
- Surface transactionnelle boiler (ACK `request_id` / status / reason,
  `boiler_bridge_online`, setpoint) — boiler → chauffage. Régie intégralement par
  les contrats `boiler/` ; recensée ici, jamais redéfinie.
- `input_boolean.blocage_chauffage_poele` — poêle → chauffage, au niveau de la
  décision centrale.
- `sensor.temperature_consigne_appliquee_locale` — chauffage → climatisation.
  Couplage unidirectionnel : la clim aligne ses seuils on/off en mode chaud sur
  la consigne appliquée par le chauffage ; le chauffage ne lit aucune entité clim.

### Absence de couplage consignée
Les domaines **ECS**, **bouclage** et **bluetti / énergie** figuraient dans le
périmètre d'arbitrage de CH-5. Le dépôt établit qu'aucune entité Chauffage n'y
est lue, et réciproquement : les occurrences du mot « chauffage » y sont
textuelles (commentaires, homonymies de scripts). L'absence de couplage est
consignée comme information de gouvernance au même titre que sa présence.

---

## 3. Décisions de gouvernance

- **Pas d'invariant CI.** Décision de chantier : aucun `R-DEP-x` n'est construit.
  Le document n'est lié à aucune garde mécanique et peut donc dériver ; il doit
  être relu à chaque refactor de frontière. La liaison CI éventuelle relève d'un
  chantier ultérieur.
- **Primauté du contrat d'autorité** sur la cartographie pour toute règle métier.
- **Primauté du runtime** sur la cartographie en cas de divergence factuelle.
- **Nature d'instantané.** Le document reflète l'état du dépôt à
  `HEAD = 961f1e6` (post CH-1 → CH-4) au moment de sa rédaction.

---

## 4. Hors périmètre

- **Runtime Chauffage** : aucun fichier de `10_scripts/chauffage/`,
  `11_automations/chauffage/` ni `12_template_sensors/chauffage/` modifié.
- **Contrats d'autorité** : aucun n'est redéfini ; le document renvoie à l'index
  des contrats référencés.
- **CI** : aucune règle, aucun test, aucun job ajouté.
- **Lectures de présentation et d'infrastructure générique** (Lovelace,
  button-card, soleil, horloge, date) : exclues par le critère d'inclusion
  inter-domaines.

---

## État de validation

- Document livré et versionné (commit de tête du domaine au moment de la
  clôture).
- Aucun test (chantier documentaire) ; arbre de travail propre.
- Runtime, contrats existants, CI : intacts.

---

## Clôture du chantier CH-5

CH-5 est clos. La dette D8 est soldée : le domaine Chauffage dispose d'une
cartographie de référence de ses couplages inter-domaines dans les deux
directions, renvoyant aux contrats d'autorité sans en dupliquer la règle. La
surface transactionnelle boiler, sous-estimée par la description d'origine de
D8, est désormais recensée explicitement.

Le chantier laisse deux frontières ouvertes : la liaison CI (`R-DEP-x`),
volontairement différée ; et la nature d'instantané du document, qui impose une
relecture à chaque refactor de frontière tant qu'aucune garde mécanique ne le
soutient.
