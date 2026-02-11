# 📑 FICHE DE COMMISSIONING — RÉGLAGES ARSENAL

Ce document consigne les réglages optimaux validés après tests. Il sert de base de restauration en cas de défaillance logicielle.

## 🌡️ 1. CONSIGNES ET SEUILS THERMIQUES
| Paramètre | Valeur | Rôle |
| :--- | :--- | :--- |
| **Consigne Confort** | **19,0 °C** | Cible nominale en période d'occupation. |
| **Consigne Réduite** | **15,0 °C** | Cible d'économie (Nuit / Absence). |
| **Seuil Chauffage (Ext) ON** | **15,0 °C** | Autorisation de chauffe si $T_{ext} < 15^\circ$. |
| **Seuil Chauffage (Ext) OFF** | **18,0 °C** | Coupe totale du système si $T_{ext} > 18^\circ$. |

## 📐 2. LOI D'EAU (COURBE DE CHAUFFE)
| Paramètre | Valeur | État |
| :--- | :--- | :--- |
| **Pente** | **1,8** | Réactivité forte au froid extérieur. |
| **Parallèle** | **1,0 °C** | Offset de base pour caler la courbe. |
| **Ajustement Auto** | **ACTIF** | Expertise statistique en service. |
| **Mode Simulation** | **DÉSACTIVÉ** | Les corrections sont réellement appliquées. |

## 🛡️ 3. HYSTÉRÉSIS ET PROTECTION
| Paramètre | Valeur | Rôle |
| :--- | :--- | :--- |
| **Hystérésis (Offset ON)** | **0,2 °C** | Déclenche si $T < Consigne - 0,2$. |
| **Hystérésis (Offset OFF)**| **0,5 °C** | Coupe si $T > Consigne + 0,5$. |
| **Protection Absence** | **ACTIF** | Protection thermique en mode absence activée. |
| **Offset ON Protection** | **0,6 °C** | Seuil de déclenchement en protection. |
| **Offset OFF Protection** | **0,0 °C** | Seuil d'arrêt en protection. |

## 🔒 4. DÉLAIS DE SÉCURITÉ (BLOCAGES)
| Paramètre | Valeur | Rôle |
| :--- | :--- | :--- |
| **Délai Aération** | **15 min** | Temps de stabilisation après fermeture fenêtre. |
| **Délai Poêle** | **45 min** | Maintien du blocage après extinction poêle. |
| **Système Blocage** | **ACTIF** | Priorité absolue aux capteurs d'ouverture. |
