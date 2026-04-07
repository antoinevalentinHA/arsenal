# CONTRAT ARSENAL — CLIMATISATION
## 02 — Architecture Arsenal — Invariants

**Version contrat :** v1.3

---

## Principe général

Le système de climatisation Arsenal est structuré en couches strictement séparées et NON NÉGOCIABLES.

Chaque couche a un rôle unique, des entrées explicites et des interdictions formelles.

**Aucune couche ne peut empiéter sur une autre.**

---

## Couche Besoin — Expression du fait physique brut

**Rôle :** Pour chaque mode ∈ {cool, dry, heat}, exprimer si un besoin thermique ou hygrométrique est actif.

**Entrées :**
- Franchissements de seuils thermiques et hygrométriques (couche observation)

**Sortie :**
- `binary_sensor.besoin_clim_cool`
- `binary_sensor.besoin_clim_dry`
- `binary_sensor.besoin_clim_heat`

**Garanties :**
- Exprime un fait physique brut — indépendant de toute autorisation
- Aucune logique d'autorisation
- Aucune action
- Aucune décision

Un besoin brut a le droit de survivre à une interdiction. Il n'est pas consommable directement par la Décision.

---

## Couche Admissibilité — Requalification décisionnelle

**Rôle :** Pour chaque mode ∈ {cool, dry, heat}, produire un besoin admissible — c'est-à-dire né dans un contexte d'autorisation valide.

**Entrées :**
- Besoins bruts (`binary_sensor.besoin_clim_*`)
- Autorisations physiques et métier (`binary_sensor.autorisation_clim_*`)

**Sortie :**
- `binary_sensor.besoin_clim_cool_admissible`
- `binary_sensor.besoin_clim_dry_admissible`
- `binary_sensor.besoin_clim_heat_admissible`

**Mécanisme :** Verrou de requalification — l'admissibilité naît sur front montant du besoin brut, sous autorisation déjà active. Un besoin brut préexistant à une interdiction ne peut jamais devenir admissible par le simple retour de l'autorisation. Il doit s'éteindre puis renaître.

**Nature :** L'admissibilité est une mémoire décisionnelle, indépendante de l'état courant du besoin brut.

**Garanties :**
- Aucune logique thermique propre
- Aucune hystérésis propre
- Aucune mémoire thermique
- Aucune action
- Aucune décision

---

## Couche Décision — Sélection du mode cible (PURE)

**Rôle :** Sélectionner un mode cible unique à partir des besoins admissibles et de la politique d'arbitrage active.

**Entrées :**
- Besoins admissibles (`binary_sensor.besoin_clim_*_admissible`)
- Politique d'arbitrage active

**Sortie canonique :** `sensor.clim_target_mode` ∈ {cool, dry, heat, off}

**Garanties :**
- Ne déclenche aucune action
- Ne lit aucun état d'exécution
- Ne produit aucune vérité persistante
- Applique une politique d'arbitrage versionnée et substituable
- Ne consomme jamais un besoin brut directement

L'arbitre est structurellement stable. Seule la politique d'arbitrage peut évoluer.

---

## Couche Exécution — Application idempotente

**Rôle :**
- Appliquer `sensor.clim_target_mode`
- Mettre le système réel en conformité avec le mode cible

**Garanties :**
- N'embarque aucune logique métier
- N'effectue aucun arbitrage
- N'envoie aucune commande redondante au sein d'une même exécution
- Ne peut ni modifier ni requalifier la décision canonique
- Ne conserve aucune mémoire locale interne au script
- La mémoire de résilience, si présente, est externalisée via des helpers dédiés et n'altère pas la nature idempotente de l'exécution

---

## Couche Sécurité — Invariants et reconvergence

### Guards
- Imposent des invariants non négociables
- Peuvent forcer l'arrêt ou la coupure
- **Priorité absolue sur toute autre couche**

### Watchdog
- Observe les divergences persistantes entre décision et état réel
- Ne choisit jamais un mode
- Ne produit aucune décision
- Ré-applique exclusivement la décision canonique courante (ré-assertion)
- Intervient en complément de la couche Exécution : il ne duplique pas les mécanismes de reprise courte de l'Exécution et n'agit qu'en cas de divergence persistante non résolue par ces mécanismes

Les Guards n'appartiennent pas à la chaîne Besoin → Admissibilité → Décision → Exécution.  
Ils constituent une **voie de sécurité orthogonale**, prioritaire sur toute autre couche, et limitée strictement à l'imposition d'un état sûr.

---

## Couche Observabilité — Lisibilité humaine

La couche Observabilité expose des états explicatifs : intention, action réelle, raison de la décision.

**Garanties :**
- Aucun impact décisionnel
- Aucune action
- Aucune rétro-influence

---

## Invariants globaux de déclenchement

Toute action du système climatique est déclenchée exclusivement par l'un des mécanismes suivants :

**1. Transition explicite de la sortie canonique de décision**  
`sensor.clim_target_mode` → application du mode cible par la couche d'Exécution.

**2. Watchdog de sécurité**  
Uniquement pour ré-appliquer la décision canonique courante en cas de divergence persistante non résolue par la résilience courte de l'Exécution (ré-assertion), sans aucune logique métier.

**3. Guard de sécurité**  
Uniquement pour imposer un état sûr (arrêt logique et/ou coupure physique), sans sélection de mode de confort, sans logique thermique, et hors de tout arbitrage.

Un Guard de sécurité :
- NE MODIFIE JAMAIS `sensor.clim_target_mode`,
- ne choisit jamais un mode climatique,
- n'exprime aucune intention de confort,
- n'interagit pas avec l'arbitrage.

Il court-circuite temporairement l'exécution pour imposer une contrainte de sécurité non négociable.

---

Les capteurs d'observation alimentent exclusivement les couches Besoin,
Admissibilité (indirectement via les autorisations), ou la voie Sécurité dans le cas des Guards / Watchdog.  
Ils n'interagissent jamais directement avec la Décision ni avec l'Exécution.

> Il n'existe qu'un seul résultat de décision : `sensor.clim_target_mode`, déterminé exclusivement à partir des besoins admissibles et de la politique active.
