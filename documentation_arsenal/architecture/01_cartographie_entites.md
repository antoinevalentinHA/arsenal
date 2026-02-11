# 📊 Arsenal — Cartographie des entités (audit structurel)

## Source

Données extraites directement depuis :
- core.entity_registry (registre officiel HA)
- via sauvegarde + analyse jq

---

## Chiffre fondamental

- Entités persistantes structurées : **3066**

Ce chiffre représente :
- uniquement les entités enregistrées
- hors entités temporaires
- hors runtime

---

## Répartition principale par plateforme

| Plateforme | Volume |
|-----------|--------|
| template | 928 |
| mobile_app | 486 |
| mqtt | 429 |
| automation | 180 |
| input_number | 137 |
| netatmo | 125 |
| input_boolean | 82 |
| script | 67 |
| input_text | 56 |
| input_datetime | 54 |
| hassio | 49 |
| switchbot_cloud | 48 |
| statistics | 46 |
| roborock | 41 |
| withings | 40 |
| vicare | 38 |
| synology_dsm | 38 |
| overkiz | 25 |
| timer | 16 |
| fujitsu_airstage | 8 |
| ...

---

## Répartition modèle vs perception

### Couche perception (terrain / cloud)

≈ 900 entités

### Couche modèle (calcul / état / dérivation)

- sensor template : 899  
- binary_sensor template : 29  
- statistics : 46  
- helpers persistants : 340  

👉 Total modèle ≈ **1330 entités**

---

## Ratio fondamental

- Modèle logiciel : ~43 %
- Perception terrain : ~30 %
- Orchestration / contrôle : ~27 %

Conclusion :
Arsenal est un système **MODEL-DRIVEN DOMINANT**