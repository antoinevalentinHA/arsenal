# 🧱 Arsenal — Convention de nommage des entités Home Assistant

---

## 🎯 OBJECTIF

Garantir que toute entité Arsenal soit :

- **retrouvable instantanément** via la recherche Home Assistant
- **cohérente sémantiquement**
- **prévisible à la frappe**
- **stable dans le temps**
- **indépendante de son implémentation technique**

Cette convention est **normative**.

---

## 🧠 PRINCIPE FONDAMENTAL

> **Le nom d’une entité décrit ce qu’elle représente,
> pas comment elle est calculée.**

La recherche utilisateur est prioritaire sur toute autre considération.

---

## 🧩 STRUCTURE CANONIQUE D’UN NOM D’ENTITÉ

### Ordre STRICT des mots (obligatoire)

### Exemple générique

Température moyenne Séjour Humidité absolue Seuil Bas Chambre Enfants Température min jour Jardin

---

## 🌡️ GRANDEURS AUTORISÉES (préfixe obligatoire)

| Grandeur | Usage |
|--------|------|
| Température | °C |
| Humidité relative | % |
| Humidité absolue | g/m³ |
| Humidex | indice |
| CO₂ | ppm |
| Bruit | dB |
| Énergie | kWh |
| Gaz | kWh |
| Électricité | kWh |
| Autonomie | km |
| Tension | V |

➡️ Toujours **au singulier**, toujours en **premier**.

---

## 🧠 QUALIFICATIFS FONCTIONNELS NORMALISÉS

### 📊 Statistiques / calculs

| Terme | Signification |
|----|----|
| moyenne | moyenne glissante ou périodique |
| min jour | minimum glissant 24 h |
| max jour | maximum glissant 24 h |
| moyenne 7 j | moyenne glissante 7 jours |
| moyenne 30 j | moyenne glissante 30 jours |

---

### 🎚️ Seuils

| Terme | Usage |
|----|----|
| Seuil Bas | limite basse de confort |
| Seuil Haut | limite haute |
| Seuil Cible | valeur visée |

---

### 🧠 Décision / intention

| Terme | Usage |
|----|----|
| Intention | décision logique calculée |
| Autorisation | feu vert / blocage logique |
| Mode | état fonctionnel |

---

## 🏠 ZONES — POSITION OBLIGATOIRE EN FIN DE NOM

- Séjour  
- Entrée  
- Jardin  
- Palier  
- Chambre Enfants  
- Salle de Jeux  
- Chambre Parents  
- SDB Parents  
- SDB Enfants  
- Cave  
- Garage  
- Petite Maison  
- Direction  
- Compta  
- Qualité  
- Devis  
- Commercial  
- Stock Carton  
- Stock PF  
- Komori  
- Bobst  
- Media  
- Extérieur  

➡️ La **zone est toujours le dernier élément** du nom.

---

## 🧭 ZONES EXTÉRIEURES — DÉSAMBIGUÏSATION DE PÉRIMÈTRE

Deux zones désignent un **extérieur**, sur **deux périmètres géographiques
et fonctionnels distincts**. Elles ne sont **pas interchangeables**.

| Zone (suffixe entité) | Périmètre | Sens |
|---|---|---|
| **Jardin** (`_jardin`) | **Domicile** | Extérieur **local du domicile** / jardin maison |
| **Extérieur** (`_exterieur`) | **Site Imprimerie** (site professionnel distant) | Extérieur **local du site Imprimerie**, distinct du domicile |

⚠️ **Homonymie à connaître.** Le mot « extérieur » a **deux sens** dans le dépôt :

- un **rôle météo générique** — « l'air au-dehors » — qui, pour une décision
  du domicile, désigne l'extérieur **du domicile**, soit la zone **Jardin** ;
- un **périmètre nommé** — la zone **Extérieur** / suffixe `_exterieur` — qui
  désigne l'extérieur **du site Imprimerie**.

Le rôle « température extérieure » d'une décision **Maison** se satisfait donc
par une entité **`_jardin`**, **jamais** par une entité `_exterieur`.

➡️ **Règle.** Une décision **Maison** portant sur une grandeur extérieure locale
consomme la zone **Jardin** (interface canonique du domicile), et **jamais** la
zone **Extérieur** (site Imprimerie). Une entité canonique dans un périmètre
n'est pas autorisée par ce seul fait dans l'autre (cf.
[`principes_generaux.md`](principes_generaux.md) §10 — autorisation de source
par périmètre). La **ressemblance de nom ne vaut pas autorisation** : c'est la
**représentativité du périmètre** qui décide.

> ℹ️ Certaines entités portent « exterieure » dans leur libellé tout en reposant
> sur des sources **domicile** (ex. une moyenne glissante calculée à partir de
> `sensor.temperature_jardin`). Le nom ne suffit donc pas à déterminer le
> périmètre : **vérifier la source**, jamais présumer d'après le suffixe.

---

## 🔍 COMPORTEMENT ATTENDU À LA RECHERCHE

### Exemple : recherche utilisateur

température moyenne

### Résultat attendu

Température moyenne Séjour Température moyenne Chambre Enfants Température moyenne Jardin Température moyenne Direction Température moyenne Komori ...

➡️ Aucun bruit parasite  
➡️ Aucun terme technique (statistics, filtre, proxy, local, etc.)
