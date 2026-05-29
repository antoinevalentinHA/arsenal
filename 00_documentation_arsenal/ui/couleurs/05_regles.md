# ⚖️ ARSENAL — Couleurs UI : Règles transversales

## Objet

Ce document définit les **règles transversales** applicables à l'ensemble
des couleurs UI Arsenal : priorités sémantiques, interdits globaux,
traitement des données indisponibles et principe de validation contractuelle.

Ces règles s'imposent à tous les fichiers de cette charte
et à toute carte UI Arsenal sans exception.

---

## Priorités sémantiques

L'ordre de priorité entre couleurs est contractuel et non négociable.
```text
🔴 Rouge       ← prime toujours
🟠 Orange      ← ne masque jamais un rouge
🟡 Jaune       ← ne masque jamais un orange ni un rouge
🟢 Vert        ← n'apparaît que s'il n'existe aucune anomalie
🔵 Bleu        ← informatif, jamais prioritaire sur une alerte
⚪ Gris neutre ← ne masque jamais un problème connu
⚪ Gris indispo← prime sur toute couleur si la donnée est indisponible
```

### Règles dérivées

| Règle | Formulation |
|-------|-------------|
| R1 | Le rouge prime toujours sur toute autre couleur |
| R2 | L'orange ne masque jamais un rouge |
| R3 | Le jaune ne masque jamais un orange ni un rouge |
| R4 | Le vert n'apparaît que s'il n'existe aucune anomalie active |
| R5 | Le gris neutre ne masque jamais un problème connu |
| R6 | Le gris indisponibilité prime sur toute couleur sémantique |
| R7 | Les couleurs d'exception (HVAC, thermique, NAV) ne modifient
       pas cette hiérarchie |

---

## Traitement des données indisponibles

| État entité | Couleur obligatoire |
|-------------|-------------------|
| `unknown` | `rgba(158, 158, 158, 0.1)` — gris indisponibilité |
| `unavailable` | `rgba(158, 158, 158, 0.1)` — gris indisponibilité |
| Entité absente | `rgba(158, 158, 158, 0.1)` — gris indisponibilité |
| Valeur non exploitable | `rgba(158, 158, 158, 0.1)` — gris indisponibilité |
| Donnée invalide critique | `rgba(244, 67, 54, 0.2)` — rouge |

Le gris indisponibilité est le **seul fallback visuel autorisé**
pour les états non exploitables.
Il prime sur toute couleur sémantique ou d'exception.

---

## Interdits globaux

Ces interdits s'appliquent à l'ensemble de l'UI Arsenal,
sans exception et sans dérogation possible hors charte.

| Interdit | Raison |
|----------|--------|
| Couleur non documentée dans cette charte | Invalide par définition |
| Variation d'opacité non documentée | Rompt la cohérence sémantique |
| Couleurs purement décoratives | La couleur n'est jamais esthétique |
| Multiplication de nuances intermédiaires | Crée une sémantique implicite non contractuelle |
| Couleurs pleines opaques sur fonds de cartes | Sauf exceptions documentées dans `03_exceptions.md` |
| Masquer `unknown` / `unavailable` par une couleur sémantique | Interdit absolu |
| Couleur encodant une décision UI autonome | Le backend décide, pas l'UI |
| Mélanger palette sémantique et palette d'exception | Hors périmètre documenté |

---

## Principe de validation contractuelle

Toute carte UI Arsenal doit pouvoir répondre immédiatement à :

> **« Quelle réalité métier cette couleur est-elle en train de traduire ? »**

Si la réponse n'est **pas unique, claire et documentée** :
👉 **la couleur est invalide.**

Ce critère s'applique :
- lors de toute création de carte
- lors de tout audit UI
- lors de tout refactor ou harmonisation

Il constitue la **référence absolue** avant toute correction UI Arsenal.