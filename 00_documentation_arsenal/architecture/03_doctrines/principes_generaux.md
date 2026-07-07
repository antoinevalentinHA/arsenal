# Principes généraux Arsenal

Ce document énonce les invariants universels d'Arsenal.
Ils s'appliquent à tous les domaines, tous les composants,
toutes les versions du système.

Chaque principe est normatif : toute conception, tout refactor,
toute revue doit pouvoir être confrontée à cette liste.

Les règles d'implémentation spécifiques à une plateforme
(Home Assistant, MQTT, shell, etc.) sont traitées dans
des documents dédiés qui citent ces principes et les instancient.

---

## 1. Contrat avant YAML

**Doctrine.** Aucune entité, automation ou script n'est créé
avant que son contrat d'interface soit explicite : entrées,
sorties, invariants, régimes de fonctionnement.

**Justification.** Le YAML est la matérialisation d'une intention
architecturale, pas sa source ; sans contrat préalable,
l'implémentation devient l'unique source de vérité et la dérive
devient inévitable.

---

## 2. Autorité unique par domaine

**Doctrine.** Un domaine fonctionnel (chauffage, ECS, VMC, vacances,
présence, climatisation…) possède une et une seule entité
responsable de la décision. Un domaine se définit par la grandeur
physique ou l'effet observable qu'il contrôle (température d'un
volume, production d'ECS, débit d'air, état de présence…), pas
par le périmètre du code qui le gère.

**Justification.** Deux décideurs en parallèle produisent des conflits
silencieux, non reproductibles et non diagnostiquables ;
l'unicité du décideur est la condition de la traçabilité.

---

## 3. Séparation perception / décision / exécution

**Doctrine.** Toute entité appartient à une seule des trois couches :
perception (capteurs, dérivés, synthèses), décision (automations
et scripts de choix), exécution (actuateurs et ponts physiques).

**Justification.** Le mélange des couches crée des boucles implicites
où un capteur agit ou un actuateur mesure, rendant le système
impossible à raisonner domaine par domaine.

---

## 4. Idempotence structurelle

**Doctrine.** Toute action doit pouvoir être rejouée sans effet
de bord ; tout état doit pouvoir être recalculé depuis ses sources.

**Justification.** Sans idempotence, un redémarrage, une reprise
après incident ou un double déclenchement produisent des états
divergents ; l'idempotence est la condition de la réconciliation
automatique.

---

## 5. Robustesse au redémarrage comme critère d'acceptation

**Doctrine.** Un composant n'est validé que s'il se reconstruit
proprement après un reload YAML ou un redémarrage complet
de Home Assistant ; le fonctionnement nominal ne suffit pas.

**Justification.** Un système robuste ne se juge pas à son régime
courant mais à sa capacité à atteindre un état cohérent depuis
n'importe quelle condition initiale.

---

## 6. Traitement explicite des trois régimes d'un état externe

**Doctrine.** Tout consommateur d'un état (entité HA, topic MQTT,
retour d'API, lecture capteur) doit définir explicitement son
comportement dans trois régimes : valeur nominale, valeur absente,
valeur incohérente.

**Justification.** Une dépendance à un état non garanti sans
traitement des trois régimes est une fragilité structurelle ;
aucun des trois régimes n'est optionnel, même si l'un d'eux
est jugé improbable.

---

## 7. Nommage par représentation, jamais par calcul

**Doctrine.** Une entité est nommée par ce qu'elle représente
(grandeur physique, qualificatif fonctionnel, zone), jamais par
la méthode utilisée pour la produire. Le nom est stable dans le
temps et ne dépend pas de son implémentation.

**Justification.** Un nom qui décrit le calcul devient faux dès
le premier refactor de l'implémentation ; un nom qui décrit
la représentation survit à toutes les évolutions techniques.

---

## 8. Disponibilité explicite plutôt qu'état factice

**Doctrine.** Un composant qui ne peut pas produire de valeur valide
doit déclarer explicitement son indisponibilité (`availability`),
jamais retourner une valeur de substitution (`0`, chaîne vide,
`unknown` forcé, dernière valeur connue silencieuse).

**Justification.** Une valeur factice propage une fausse certitude
dans toute la chaîne décisionnelle ; l'indisponibilité déclarée
force chaque consommateur à traiter explicitement le cas absent,
conformément au principe 6.

---

## 9. Traçabilité des décisions

**Doctrine.** Toute décision prise par le système doit laisser une
trace observable permettant de reconstituer, a posteriori, les
états d'entrée et la règle qui l'a produite.

**Justification.** Un système non traçable est indéboguable et non
auditable ; la traçabilité transforme un comportement correct en
comportement maîtrisé, et c'est cette maîtrise qui distingue un
système opérationnel d'un système qui marche par accident.

---

## 10. Autorisation de source par périmètre

**Doctrine.** L'autorisation d'une source pour une décision est
**relative au périmètre du domaine consommateur**, jamais absolue.
Une source correcte, stable et canonique **dans son propre périmètre**
(géographique ou fonctionnel) n'est **pas** de ce seul fait autorisée
pour une décision d'un **autre périmètre**. Une décision ne consomme
qu'une source **représentative de son périmètre** et **explicitement
autorisée** pour son domaine — en pratique, l'**interface canonique**
de ce domaine.

**Justification.** Une source peut être exploitable là où elle est
mesurée tout en étant non représentative ailleurs ; sans règle
d'autorisation par périmètre, une entité au nom plausible mais issue
d'un autre site ou d'une autre fonction peut alimenter silencieusement
une décision qu'elle ne décrit pas. La représentativité spatiale et
fonctionnelle d'une entrée est une **condition d'admissibilité** de la
décision, pas une propriété acquise par ressemblance de nom (cf.
principe 7). Un incident réel a matérialisé ce risque : une décision du
domicile a consommé une source extérieure d'un site distant, non
représentative du domicile (audit
[`audits/01_rapports/architecture/audit_frontiere_maison_imprimerie_sources_exterieures.md`](../../audits/01_rapports/architecture/audit_frontiere_maison_imprimerie_sources_exterieures.md)).

---

## Invariant synthétique

> Arsenal est un système **contractuel**, **stratifié**, **idempotent**,
> **traçable** et **honnête sur son état** — toute dérogation à l'un
> de ces cinq axes est une dette de conception, pas un compromis
> acceptable.
