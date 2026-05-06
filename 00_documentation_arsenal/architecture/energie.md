## 🧱 Architecture Énergie — Séparation des couches

Le sous-système Énergie repose sur une séparation stricte
entre acquisition, sécurisation et exposition.

### Chaîne de traitement

Capteur matériel brut  
→ Proxy énergie sécurisé  
→ Dashboard Énergie  
→ Utility_meter (découpes temporelles)

---

### Rôle des proxys énergie

Les proxys énergie constituent une **couche technique intermédiaire**
chargée de garantir l’intégrité des données :

- rejet des états invalides
- rejet des valeurs négatives
- interdiction de toute régression
- continuité au redémarrage

Ils produisent un compteur **strictement monotone**,
compatible avec les exigences du dashboard Énergie.

---

### Principe architectural fondamental

Le dashboard Énergie ne consomme **jamais directement**
un capteur matériel brut.

Toute source exposée à Energy doit avoir été préalablement
sécurisée par une couche proxy dédiée.