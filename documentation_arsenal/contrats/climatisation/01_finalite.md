# CONTRAT ARSENAL — CLIMATISATION
## 01 — Finalité du système

**Version contrat :** v1.3

---

## Objectif

Le système de climatisation a pour objectif de garantir
un confort thermique et hygrométrique cohérent, stable
et maîtrisé, sans oscillation inutile ni pilotage implicite.

La finalité du système porte sur la détermination d'un
état cible pertinent, non sur son application immédiate.

---

## États exclusifs

Le système repose sur quatre états exclusifs :

| État | Rôle |
|---|---|
| **COOL** | Refroidissement actif |
| **DRY** | Déshumidification active |
| **HEAT** | Chauffage léger d'appoint |
| **OFF** | Repos volontaire |

**OFF est un état NORMAL et volontaire, jamais une erreur.**

---

## Principes directeurs

Le système vise à :

- répondre uniquement à des besoins thermiques admissibles,
- respecter les contraintes physiques du logement,
- éviter toute action « par principe »,
- rester explicable, traçable et compréhensible par un humain.

Un besoin thermique n'est pris en compte que s'il est admissible,
c'est-à-dire s'il est né dans un contexte d'autorisation valide.
