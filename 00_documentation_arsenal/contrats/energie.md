# 🔒 Sources autorisées — Dashboard Énergie

### Intention

Le dashboard Énergie doit refléter une **consommation physique réelle,
cohérente et exploitable sur le long terme**.

Toute source utilisée doit garantir :
- l’absence de valeurs négatives
- l’absence de régression
- la continuité après redémarrage
- la compatibilité avec les statistiques long terme

---

### Règle fonctionnelle

Le dashboard Énergie consomme **exclusivement des capteurs énergie
strictement monotones et persistants**.

Sont interdits comme sources Energy :
- capteurs matériels bruts (prises, modules Zigbee, etc.)
- capteurs journaliers, mensuels ou annuels
- toute entité susceptible de revenir à zéro ou de régresser

---

### Invariant

Toute modification de source Energy sur un appareil existant
nécessite sa **suppression puis sa recréation complète**.

Cette règle est non négociable.