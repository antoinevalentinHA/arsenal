# meteo.md
# Arsenal — Contrat du domaine météo
# Version : 1.1
# Statut : normatif
# Dépend de : validation.md, fallback.md
# Consommateurs : contrats locaux par axe météo

---

## 1. Objet

Définir le cadre normatif applicable à l'ensemble des données
du domaine météo dans Arsenal.

Ce contrat est un contrat de raccordement.
Il n'introduit pas de règles de validation ni de fallback.
Il impose leur application et en délègue la paramétrisation
aux contrats locaux par axe.

---

## 2. Périmètre

Le domaine météo couvre l'ensemble des mesures physiques
d'environnement consolidées par Arsenal :

- température
- humidité
- tout autre axe physique déclaré dans un contrat d'axe

Chaque axe constitue un domaine de mesure indépendant.
Aucune substitution entre axes n'est autorisée.

---

## 3. Cadre normatif obligatoire

Tout capteur Arsenal du domaine météo DOIT appliquer :

| Opération  | Contrat de référence    |
|------------|-------------------------|
| Validation | `validation.md` |
| Fallback   | `fallback.md`   |

Aucune implémentation ne peut contourner ces deux contrats.

Seuls les paramètres explicitement déclarés comme surchargeables
par les contrats de référence peuvent être précisés localement
dans un contrat d'axe.

---

## 4. Responsabilités déléguées aux contrats d'axe

Chaque contrat d'axe DOIT définir :

- la source primaire
- la source de secours
- la plage de plausibilité (min / max)
- les dépendances critiques éventuelles
- le TTL_override si dérogation au TTL_DEFAULT
- l'autorisation ou l'interdiction explicite du niveau 3

---

## 5. Interdictions normatives

- Un axe météo **ne peut pas** servir de source de secours
  pour un autre axe météo.
- Les bornes de plausibilité **ne peuvent pas** être définies
  dans ce contrat.
- La hiérarchie de fallback **ne peut pas** être redéfinie
  localement — seul le TTL est surchargeable.
- Un contrat d'axe qui interdit le niveau 3 **ne peut pas**
  publier de mémoire de continuité, même si l'implémentation
  technique le permettrait.

---

## 6. Renvois contractuels

- Validation des sources → [`validation.md`](validation.md)
- Stratégie de fallback  → [`fallback.md`](fallback.md)
- Paramètres par axe     → contrats locaux d'axe