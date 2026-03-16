# contrat_fallback.md
# Arsenal — Contrat de fallback des sources de données
# Version : 1.1
# Statut : normatif
# Dépend de : contrat_validation.md
# Consommateurs : contrat_meteo.md, contrats locaux par axe

---

## 1. Objet

Définir la stratégie appliquée par Arsenal pour sélectionner ou
retenir une valeur publiée, après que la validation des sources a
été effectuée.

> Le fallback ne valide jamais.
> Il ne traite que des sources dont la recevabilité a été tranchée
> par contrat_validation.md.

---

## 2. Définitions

**Source primaire**
Source explicitement déclarée comme principale pour un axe donné.

**Source de secours**
Source explicitement déclarée comme fallback de la source primaire
pour un axe donné. Aucune substitution implicite n'est autorisée.

**Valeur consolidée**
Valeur publiée par le capteur Arsenal à l'issue du mécanisme de
fallback.

**Mémoire de continuité**
Dernière valeur consolidée publiée, retenue temporairement en
l'absence de source valide. Ce n'est pas une source.

**TTL (Time To Live)**
Durée maximale pendant laquelle la mémoire de continuité peut être
publiée en l'absence de source valide.

**Abstention**
État publié par le capteur Arsenal lorsqu'aucune source valide
n'est disponible et que la mémoire de continuité est expirée
ou inexistante.

---

## 3. Hiérarchie normative

Le fallback évalue les niveaux dans l'ordre strict suivant :

| Niveau | Nature                | Condition de déclenchement                                           |
|--------|-----------------------|----------------------------------------------------------------------|
| 1      | Sélection de source   | Source primaire = valide (selon contrat_validation.md)               |
| 2      | Sélection de source   | Source primaire = invalide, source de secours = valide               |
| 3      | Rétention de résultat | Sources 1 et 2 invalides, valeur consolidée existante, age ≤ TTL    |
| 4      | Abstention            | Sources 1 et 2 invalides, valeur consolidée absente ou age > TTL    |

Les niveaux 1–2 sont des opérations de **sélection de source**.
Le niveau 3 est une opération de **rétention de résultat**.
Ce sont deux natures distinctes. Le contrat les traite séparément.

Aucun saut de niveau n'est autorisé.

---

## 4. Description des niveaux

### Niveau 1 — Source primaire

Condition :
  source_primaire = valide (selon contrat_validation.md)

Action :
  → publication de la valeur primaire.

### Niveau 2 — Source de secours

Condition :
  source_primaire = invalide
  source_secours = valide (selon contrat_validation.md)

Action :
  → publication de la valeur de secours.

### Niveau 3 — Mémoire de continuité

Condition :
  source_primaire = invalide
  source_secours = invalide
  une valeur consolidée a déjà été publiée
  age(dernière_valeur_consolidée) ≤ TTL_effectif

Action :
  → publication de la dernière valeur consolidée.

> Le niveau 3 ne constitue pas une source.
> Il retient temporairement un résultat déjà produit.
> Il ne peut pas corriger, lisser ou modifier ce résultat.

### Niveau 4 — Abstention

Condition :
  source_primaire = invalide
  source_secours = invalide
  ET : aucune valeur consolidée n'a encore été publiée
       OU age(dernière_valeur_consolidée) > TTL_effectif

Action :
  → aucune valeur publiée.
  → état du capteur Arsenal : `unknown` ou `unavailable`
    selon les conventions de l'implémentation.

---

## 5. Conditions de rétention — TTL

La mémoire de continuité est strictement bornée dans le temps.

**TTL_DEFAULT = 30 minutes**

**TTL_effectif =**
  TTL_override si explicitement défini dans le contrat d'axe,
  sinon TTL_DEFAULT.

Toute dérogation au TTL_DEFAULT doit être explicitement motivée
dans le contrat d'axe concerné.

**Condition d'évaluation du TTL :**
L'âge de la dernière valeur consolidée est calculé comme :

  now() − last_updated(capteur_consolidé)

**Cas particulier — première initialisation :**
Si aucune valeur consolidée n'a encore été publiée par le capteur
(ex. : premier démarrage HA), last_updated est indéfini.
Le niveau 3 est alors inapplicable. Le système passe directement
au niveau 4.

**Exigence d'implémentation :**
Dans Home Assistant, un trigger-based template sensor ne réévalue
son état que lors du déclenchement d'un trigger. Le TTL ne peut
donc expirer que si un trigger temporel est déclaré.

> Tout capteur Arsenal utilisant le niveau 3 DOIT embarquer
> un trigger time_pattern dont la période est ≤ TTL_effectif.

Sans ce trigger, le TTL est déclaratif mais jamais évalué.

---

## 6. Résultat du fallback

| Résultat | Condition                                          | Valeur publiée             |
|----------|----------------------------------------------------|----------------------------|
| Niveau 1 | Primaire valide                                    | Valeur primaire            |
| Niveau 2 | Secours valide                                     | Valeur de secours          |
| Niveau 3 | Aucune source valide, valeur existante, age ≤ TTL  | Dernière valeur consolidée |
| Niveau 4 | Aucune source valide, valeur absente ou age > TTL  | `unknown` / `unavailable`  |

---

## 7. Interdictions normatives

- Le fallback **ne valide jamais** une source.
- Le fallback **ne calcule pas**, ne dérive pas, ne lisse pas une valeur.
- Le fallback **ne modifie jamais** la valeur retenue au niveau 3.
- Le fallback **ne réhabilite jamais** une source invalide.
- Le fallback **ne connaît pas** les plages de plausibilité.
- La mémoire de continuité **ne constitue pas** une source de données.
- Une dérogation au TTL_DEFAULT **ne peut pas** être implicite.

---

## 8. Renvois contractuels

- Recevabilité des sources → `contrat_validation.md`
- Plages de plausibilité par axe → contrats locaux d'axe
- Application au domaine météo → `contrat_meteo.md`
