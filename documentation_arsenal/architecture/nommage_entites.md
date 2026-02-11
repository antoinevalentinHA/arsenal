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

Température moyenne Séjour Humidité absolue Seuil Bas Chambre Arnaud Température min jour Jardin

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
- Chambre Arnaud  
- Chambre Matthieu  
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

## 🔍 COMPORTEMENT ATTENDU À LA RECHERCHE

### Exemple : recherche utilisateur

température moyenne

### Résultat attendu

Température moyenne Séjour Température moyenne Chambre Arnaud Température moyenne Jardin Température moyenne Direction Température moyenne Komori ...

➡️ Aucun bruit parasite  
➡️ Aucun terme technique (statistics, filtre, proxy, local, etc.)
