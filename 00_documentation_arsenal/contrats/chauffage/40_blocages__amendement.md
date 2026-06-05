# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — BLOCAGES & INTERDICTIONS HIÉRARCHIQUES V3 · Amendement : poêle comme blocage de stabilisation corroboré
#
# 📌 STATUT :
#   AMENDEMENT au contrat de domaine [`40_blocages.md`](40_blocages.md)
#
# 🎯 OBJET :
#   Requalifier le blocage poêle à la lumière de la doctrine des
#   registres (`01`) : le poêle est un mécanisme de STABILISATION
#   (anti-empilement thermique), non une sécurité système. Son
#   conflit avec l'exception Vacances / pré-confort se résout par
#   la QUALITÉ DU SIGNAL (corroboration non thermique), non par
#   l'ordre hiérarchique.
#
#   Cet amendement fige la décision A (portée de la corroboration).
#
# ==========================================================

---

## A1. Reclassement du blocage poêle

Le blocage poêle est reclassé comme **blocage de stabilisation thermique**,
de finalité **anti-empilement** : éviter qu'une seconde source de chaleur
(la chaudière) ne s'ajoute à une source indépendante déjà active (le poêle),
et laisser se dissiper l'apport thermique du poêle.

Le poêle n'est **pas** une sécurité système : aucune intégrité matérielle
n'est en jeu si chaudière et poêle fonctionnent ensemble. C'est une qualité
de régulation, pas une protection d'intégrité.

Conséquence (D1) : le poêle ne peut pas être traité par dominance
hiérarchique absolue au même titre qu'une interdiction de sécurité. Son effet
demeure fort en exploitation normale, mais il se résout par le signal (D2).

---

## A2. Nature événementielle confirmée

Les caractéristiques architecturales établies par `40 §5.3` sont confirmées :

- le capteur poêle est strictement **événementiel** ;
- le passage OFF est volontairement ignoré ;
- le blocage est maintenu exclusivement par la durée du timer ;
- aucune lecture thermique continue, aucune estimation d'inertie, aucune
  mémoire inter-cycle dans le blocage décisionnel lui-même.

---

## A3. Corroboration du signal (D-POELE)

> **D-POELE-1 — Définition décisionnelle du poêle actif.**
> « Poêle actif », au sens d'une décision ou d'un blocage thermique, signifie
> **poêle corroboré** : une signature thermique compatible **ET** un signal
> indépendant de la chauffe (présence humaine non thermique, p. ex. hausse
> CO2). Une signature thermique seule ne constitue jamais un poêle actif au
> sens décisionnel.

> **D-POELE-2 — Exigence structurelle de corroboration.**
> Toute qualification poêle qui **influence une décision ou un blocage**
> thermique doit exiger un signal de corroboration non thermique. La
> qualification décisionnelle ne doit jamais être satisfiable par la seule
> signature thermique.

> **D-POELE-3 — Priorité de l'anti-empilement en zone transitoire.**
> Dans la fenêtre transitoire où la corroboration peut subsister par
> hystérésis (CO2 résiduel, délais de relâchement), l'anti-empilement
> prévaut : le système s'abstient de relancer le confort. C'est le côté sûr
> de l'erreur — un poêle réel non encore retombé prime sur une relance.

Justification de D-POELE-1/2 : la signature thermique est un signal
mono-source qui peut être produit par la chauffe elle-même (préchauffage,
montée vigoureuse). S'y fier seule exposerait le système à une
auto-inhibition (une chauffe légitime se coupant sur sa propre signature). Le
signal de corroboration non thermique (CO2) lève cette ambiguïté : en maison
vide, pas de CO2, donc pas de faux poêle ; en maison occupée, le poêle réel
est correctement détecté.

---

## A4. Résolution du conflit poêle / exception Vacances — pré-confort

Le conflit historique « le poêle est-il prioritaire sur l'exception Vacances
+ pré-confort, ou l'inverse ? » est **dissous**, non tranché par l'ordre.

> **Règle de comportement opposable.**
> Aucune décision `comfort` n'est émise en présence d'un **poêle corroboré**,
> y compris dans le contexte Vacances + pré-confort. Le pré-confort ne crée
> aucune exception à l'anti-empilement par poêle corroboré.
>
> Réciproquement, un poêle **non corroboré** (signature seule) ne constitue
> pas un poêle actif (D-POELE-1) et ne bloque donc pas le pré-confort.

Conséquence architecturale (D2) : **l'ordre d'évaluation des branches poêle
et Vacances dans l'implémentation devient indifférent.** Dès lors que
« poêle » signifie « poêle corroboré », placer la branche poêle avant ou
après la branche Vacances produit le même comportement. Le faux débat
« qui gagne dans les `elif` » disparaît.

Cette règle remplace, dans `40` et dans la table canonique `80`, toute
formulation antérieure exprimée en termes de rang ou de priorité d'ordre
entre poêle et Vacances.

---

## A5. Portée de la corroboration — calibration conservatrice (Décision A figée)

La corroboration exigée par D-POELE-2 s'applique à toute qualification
**décisionnelle ou bloquante**. Elle ne s'applique pas de la même manière à la
**mémoire de calibration long terme** (`input_boolean.poele_recent`), sous
condition stricte.

> **D-POELE-CALIB — Tolérance mono-source bornée à la calibration
> conservatrice.**
> Une qualification poêle **mono-source** (signature thermique seule) reste
> acceptable pour la seule mémoire de calibration, **si et seulement si** son
> effet :
>
> 1. ne peut **jamais relâcher** une protection ou un blocage ;
> 2. ne peut **jamais autoriser** une chauffe ni produire un `comfort` ;
> 3. reste **strictement conservateur** : il ne peut que figer / stabiliser
>    un réglage (p. ex. empêcher un ajustement à la baisse de la courbe de
>    chauffe), jamais l'assouplir.
>
> Dès qu'une qualification poêle mono-source aurait un effet décisionnel,
> bloquant, ou non conservateur, D-POELE-2 s'applique pleinement et la
> corroboration devient obligatoire.

Justification : la mémoire de calibration sur signature seule produit, au pire,
un faux positif **conservateur** — figer la courbe à tort. Cette erreur va
dans le sens de la prudence (ne pas calibrer sur des données thermiques
potentiellement polluées). Exiger la corroboration pour cette mémoire
risquerait au contraire de manquer des poêles réels lors de courtes absences
et de relâcher la garde de calibration — effet non conservateur, donc
indésirable. La tolérance est donc justifiée précisément parce qu'elle est
asymétriquement sûre.

---

## A6. Invariants exposés (CI)

- **INV-POELE-1** — Aucune branche produisant `comfort` n'est atteignable sans
  condition excluant le poêle corroboré (préconfort inclus).
- **INV-POELE-2** — La qualification poêle consommée par la décision ou par un
  blocage exige un signal non thermique ; elle n'est jamais satisfiable par la
  seule signature thermique.
- **INV-POELE-CALIB** — Toute qualification poêle mono-source n'a qu'un effet
  conservateur (figer/stabiliser), ne relâche aucune protection, n'autorise
  aucune chauffe.

---

## A7. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) · [`01_doctrine_registres.md`](01_doctrine_registres.md)

**Utilisé par :** [`30_decision_centrale.md`](30_decision_centrale.md) · [`80_table_decision_canonique.md`](80_table_decision_canonique.md)

**Complémentaire de :** [`45_aeration.md`](45_aeration.md) ·
[`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) · [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)

---

## A8. Portée

Cet amendement reclasse le blocage poêle et fige la décision A. Il précède et
gouverne la réécriture partielle de `80` (la table canonique implémente la
définition du poêle posée ici).

# ==========================================================
