# CONTRAT ARSENAL — CLIMATISATION
## 02 — Architecture Arsenal — Invariants

**Version contrat :** v1.3

---

## Principe général

Le système de climatisation Arsenal est structuré en couches strictement séparées et NON NÉGOCIABLES.

Chaque couche a un rôle unique, des entrées explicites et des interdictions formelles.

**Aucune couche ne peut empiéter sur une autre.**

---

## Couche Décision — Production des candidats (PURE)

**Rôle :** Pour chaque mode ∈ {cool, dry, heat}, déterminer si le mode est requis et si le mode est applicable.

**Entrées :**
- Besoins thermiques et hygrométriques
- Autorisations physiques et métier
- Contraintes environnementales

**Sortie :** Ensemble de candidats `{ mode : { requis, applicable } }`

- `requis` exprime un besoin thermique ou hygrométrique.
- `applicable` exprime la possibilité locale d'un mode (autorisation physique ou métier), jamais sa priorité ni sa sélection finale.

**Garanties :**
- Aucune action
- Aucune temporisation
- Aucune mémoire implicite
- Aucune priorité inter-mode
- Aucun choix final

La Décision ne sélectionne jamais un mode cible. Elle produit uniquement des états candidats.

---

## Couche Arbitrage — Sélection du mode cible

**Rôle :** Sélectionner un mode cible unique à partir des candidats produits par la Décision.

**Entrées :**
- Ensemble de candidats `{ mode : { requis, applicable } }`
- Politique d'arbitrage active

**Sortie canonique :** `sensor.clim_target_mode` ∈ {cool, dry, heat, off}

**Garanties :**
- Ne déclenche aucune action
- Ne lit aucun état d'exécution
- Ne produit aucune vérité persistante
- Applique une politique d'arbitrage versionnée et substituable

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

Les Guards n'appartiennent pas à la chaîne Décision → Arbitrage → Exécution.  
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

Aucun capteur d'observation ne déclenche directement une action de confort ou d'exécution.  
Les capteurs d'observation alimentent exclusivement la couche Décision, ou la voie Sécurité dans le cas des Guards / Watchdog.  
Ils n'interagissent jamais directement avec l'Arbitrage ni avec l'Exécution.

> Il n'existe qu'un seul résultat de décision : celui produit par l'Arbitrage selon la politique active.
