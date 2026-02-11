# ==========================================================
# 🧠 ARSENAL — NOTE D’ARCHITECTURE  
#     Zigbee — Réseau critique (ouvrants thermiques)  
# ==========================================================

## 📌 STATUT

- Nature : NOTE D’ARCHITECTURE — RÉFÉRENCE STRUCTURANTE  
- Domaine : Zigbee / Radio 2.4 GHz / Topologie / Fiabilité événements  
- Portée : Ouvrants thermiquement bloquants  
- Objectif :
  Fiabiliser **quasi-industriellement** la remontée d’événements OFF
  des ouvrants critiques (Aqara),
  **sans aucune modification applicative**
  (ni HA, ni pipeline, ni décision centrale).

---

## 🎯 FINALITÉ

Dans Arsenal, un événement Zigbee perdu peut :

- créer un état ON persistant non physique,
- générer une cause NIVEAU 2 zombie,
- bloquer thermiquement la maison sans sortie canonique.

Cette note définit :

- les causes RF plausibles,
- les invariants Zigbee “critique”,
- les règles de design réseau,
- les critères de conformité,
- la stratégie cible de durcissement radio.

---

## 🧱 PÉRIMÈTRE & INTERDICTIONS

### Inclus
- Zigbee2MQTT  
- topologie mesh  
- parentage, routage, sauts  
- LQI / RSSI / stabilité  
- interférences Wi-Fi 2.4 GHz  
- placement coordinateur & routeurs  

### Interdictions absolues
- polling applicatif  
- watchdog logiciel HA  
- auto-heal métier  
- corrections dans pipeline ou décision centrale  
- “réparations” logicielles  

➡️ Le problème est **radio / réseau**, jamais applicatif.

---

## 🧩 CONTEXTE RÉEL OBSERVÉ (CAS DE RÉFÉRENCE)

Symptôme historique reproductible :

- ouverture réelle brève  
- fermeture réelle  
- événement OFF manqué  
- état HA reste ON  
- résolution immédiate en rouvrant / refermant  

Interprétation RF :

- OFF bien émis par l’Aqara  
- perdu entre end-device → parent → mesh → coordinateur  
- Zigbee n’ayant aucun mécanisme correctif, l’état reste figé  

➡️ Comportement strictement conforme au protocole Zigbee.

---

## 🧠 INVENTAIRE TECHNIQUE (RÉSEAU ACTUEL — POST MIGRATION)

### Orchestration & Stack radio
- Middleware : Zigbee2MQTT  
- Coordinateur : **SONOFF ZBDongle-E**  
- Chipset : **EFR32MG21**  
- Stack : **EZSP v8**  
- Firmware coordinateur : **6.10.3.0 build 297**  
- Zigbee2MQTT : v22.16.0  
- Transport : MQTT v4 (`core-mosquitto:1883`)  
- Architecture : monocoordinateur, maillage unique  

- Canal Zigbee actuel : **25**  
  ➜ hors lobe Wi-Fi principal  
  ➜ séparation spectrale quasi complète  

---

### Environnement Wi-Fi 2.4 GHz réel

- Canaux dominants observés : **1 → 5**  
- Largeur effective : **40 MHz**  
- Occupation : **élevée et permanente**  
- Niveau de champ : ~ **-60 dBm** (fort)  

Spectre effectif :
- lobe Wi-Fi principal : 2412 → ~2437 MHz  
- Zigbee ch25 : ~2475 MHz  

➡️ **Aucun chevauchement spectral significatif résiduel**  
➡️ Collisions Zigbee / Wi-Fi désormais marginales.

---

### Placement & assainissement coordinateur

- Coordinateur désormais :
  - déporté via **rallonge USB 1 m**  
  - éloigné :
    - box Internet  
    - borne Deco principale  
    - onduleur  
    - Raspberry Pi  
  - position :
    - dégagée  
    - hors volume métallique  
    - environnement RF calme  

Effets observés :
- LQI coordinateur homogènes  
- disparition erreurs EZSP récurrentes  
- stabilité globale du mesh accrue  

➡️ Coordinateur désormais **point fort** du réseau  
(et non plus point faible structurel).

---

### Taille & typologie du réseau

- **48 nœuds actifs**  
- **18 routeurs secteur**  
- **30 end devices sur pile**  
- **12 ouvrants Aqara critiques**  

Répartition fonctionnelle :

- Ouvrants critiques (Aqara MCCGQ11LM) : 12  
- Mouvements (SNZB-03P) : 6  
- Température / humidité (SNZB-02D) : 5  
- Boutons Aqara : 4  
- Claviers alarme Develco : 2  
- Sirène Develco : 1  
- Capteur pluie : 1  

Routeurs principaux :
- Prises Nous TS011F : 14  
- Prises Innr SP240 : 2  
- Prise Innr OSP240 : 1  
- Sirène Develco SIRZB-111 : 1  

➡️ Réseau dense mais désormais :
- hiérarchisé  
- redondant  
- spectralement propre  
- topologiquement maîtrisé  

---

### Diversité fournisseur & résilience stack

Répartition fournisseurs :

- **LUMI (Aqara)** : 15  
- **_TZ3000 (Tuya / Nous)** : 14  
- **eWeLink** : 7  
- **SONOFF** : 5  
- **friient / Develco** : 3  
- **Innr** : 3  
- **Inconnu** : 1  

Propriétés :

- multi-firmware  
- multi-stacks  
- absence de monopole radio  
- résilience élevée face à bugs firmware isolés  

➡️ Architecture **fortement tolérante aux défauts**.

---

### Hiérarchie radio implicite (post migration)

Routeurs pivots identifiés (Gold Layer effectif) :

- `sirene` (Develco SIRZB-111) — pivot principal  
- `prise_cage_escalier_rdc`  
- `prise_onduleur`  
- `prise_buanderie`  
- `prise_palier`  

Propriétés communes :
- visibilité directe coordinateur  
- LQI élevés  
- nombreux voisins  
- stabilité parentage  

➡️ Mise en place effective d’une **couche GOLD**  
dédiée aux ouvrants thermiques critiques.

---

### État global du réseau

- maillage stable  
- routes multiples disponibles  
- parentage majoritairement contrôlé  
- ouvrants critiques :
  - parents propres  
  - profondeur ≤ 2  
  - LQI majoritairement > 100  
  - last_seen cohérents  

➡️ Réseau désormais **apte à usage critique thermique**  
sans correctif applicatif.

---

## 🔥 DIAGNOSTIC RF STRUCTURANT (HISTORIQUE & RÉSOLUTION)

### 1) Chevauchement spectral historique

Ancienne situation :

- Zigbee ch11 ≈ 2405 MHz  
- Wi-Fi ch1→5 en 40 MHz  
- chevauchement **direct et massif**

Conséquences :

- collisions fréquentes  
- retries limités  
- drops ponctuels OFF  

➡️ Cause racine principale identifiée.

---

### 2) Coordinateur historiquement bruité

Anciennes sources cumulées :

- proximité Raspberry  
- onduleur  
- box / Deco  
- bruit USB  

Effet :

- sensibilité effective réduite  
- mesh fragilisé  
- pertes OFF silencieuses  

➡️ Point faible structurel historique.

---

### 3) Parentage non maîtrisé (avant migration)

Ouvrants parentés à :

- frigo  
- radiateur  
- prises contextuelles  
- routeurs thermiquement / électriquement bruités  

Chaîne typique :

Aqara  
→ parent moyen  
→ mesh multi-sauts  
→ coordinateur bruité  

➡️ Une seule perte suffisait à créer un zombie.

---

## 🧷 ÉTAT POST-MIGRATION — SYNTHÈSE RÉSEAU

### Décisions appliquées (v8.2.2)

- Migration Zigbee vers **canal 25**  
- Réappairage complet du parc (48 devices)  
- Repositionnement physique coordinateur  
- Réorganisation des routeurs critiques  
- Parc prises homogénéisé (Innr / Nous maîtrisés)  

### Effets observés

- Plus aucun îlot isolé  
- Maillage dense et redondant  
- Sirène Develco pivot principal  
- Prises « cage escalier / onduleur / buanderie » piliers verticaux  
- Tous ouvrants :
  - parent stables  
  - profondeur ≤ 2  
  - LQI majoritairement > 100  

➡️ Réseau désormais **structurellement sain**.

---

## 🧭 INVARIANTS ZIGBEE “CRITIQUE” (ARSENAL)

### I1 — Coordinateur propre
Un coordinateur bruité dégrade **tout** le mesh.

### I2 — Canal choisi contre le Wi-Fi réel
Le bon canal est **celui qui évite le lobe Wi-Fi dominant**, pas un canal théorique.

### I3 — Parentage contrôlé
Un ouvrant critique ne doit **jamais** tomber sur un parent contextuel ou bruité.

### I4 — Minimisation des sauts
- cible : 1 saut  
- tolérance : 2 (routeurs premium)  
- interdit : ≥3  

### I5 — Densité maîtrisée
Trop de routeurs hétérogènes augmente :
- instabilité  
- re-parentage  
- routes toxiques  

---

## 🥇 ARCHITECTURE CIBLE — “GOLD LAYER” (DÉSORMAIS ATTEINTE)

### Principe

Créer une couche radio dédiée aux ouvrants critiques :

- routeurs premium  
- positionnés volontairement  
- servant de parents préférentiels  

### Routeurs GOLD effectifs

- sirène Develco (pivot central)  
- prise cage escalier RDC  
- prise onduleur  
- prise buanderie  

Propriétés vérifiées :

- radio propre  
- LQI élevés  
- forte visibilité coordinateur  
- charge maîtrisée  

À exclure définitivement :

- frigo  
- radiateur  
- prises thermiques  
- box / Deco / onduleur en proximité RF  

---

## 📐 RÈGLES DE PLACEMENT — NON NÉGOCIABLES

### Coordinateur

- rallonge USB : **1 à 2 m**  
- distance minimale :
  - > 1.5 m box / Deco  
  - > 1.5 m onduleur  
  - > 1 m Raspberry  
- position :
  - dégagée  
  - hauteur ~1 m  

### Routeurs GOLD

- même discipline RF  
- jamais collés à sources parasites  
- jamais en environnement métallique / thermique  

---

## 📻 STRATÉGIE DE CANAL — RÉVISION POST MIGRATION

### Constat réel

- Wi-Fi occupe massivement 1→5  
- Zigbee ch11 historiquement catastrophique  

### Décision effective

- Zigbee migré en **canal 25**  

Avantages :

- totalement hors lobe Wi-Fi principal  
- bruit RF minimal  
- stabilité excellente observée  
- LQI élevés généralisés  

➡️ Canal 25 devient **canal de référence Arsenal**.

---

## 🧪 CRITÈRES DE CONFORMITÉ — OUVRANT CRITIQUE

Un ouvrant est conforme si :

- parent = routeur GOLD ou coordinateur  
- LQI stable :
  - cible : >100  
  - vigilance : 70–100  
  - risque : <70  
- profondeur ≤ 2  
- re-parentage rare  
- last_seen cohérent  
- aucun parent toxique  

---

## 🔍 MÉTHODOLOGIE D’AUDIT PÉRIODIQUE

### A — RF
- Wi-Fi : canal + largeur  
- Zigbee : canal 25 maintenu  

### B — Coordinateur
- rallonge USB toujours en place  
- isolement RF maintenu  
- qualité globale liens  

### C — Ouvrants critiques
- parent  
- profondeur  
- LQI  
- stabilité  
- last_seen  

### D — Routeurs toxiques
- charge excessive  
- LQI erratique  
- proximité bruit  
- contexte thermique / métal  

---

## 🧾 SCHÉMAS CONCEPTUELS

### Situation historique (avant migration)

Wi-Fi ch1→5 ████████████  
Zigbee ch11 ─────██████████────────  

Aqara  
 → parent moyen  
    → mesh multi-sauts  
       → coordo bruité  

↳ OFF unique perdu possible  

---

### Situation actuelle (réseau cible atteint)

Wi-Fi ch1→5 ████████████  
Zigbee ch25 ────────────────  

Aqara  
 → routeur GOLD  
    → coordo propre  

↳ OFF fiable, perte hautement improbable  

---

## ✅ DÉCISIONS D’ARCHITECTURE VALIDÉES

### D1 — Assainissement coordinateur  
**Appliqué** (rallonge + isolement RF)

### D2 — Migration canal Zigbee  
**Appliquée** → canal 25 retenu

### D3 — Mise en place Gold Layer  
**Appliquée** :
- sirène Develco pivot  
- 3 routeurs structurels  
- élimination parents toxiques  

---

## 📌 NOTES ARSENAL — INVARIANTS À CONSERVER

- Une perte OFF unique est un phénomène **réseau normal**  
- La fiabilité critique repose d’abord sur :
  1) coordinateur propre  
  2) canal cohérent  
  3) parentage contrôlé  
  4) routeurs GOLD stables  

Aucune correction applicative ne peut garantir ce niveau de sûreté.

---

# ==========================================================
# 📌 FIN NOTE — Zigbee réseau critique (révision post v8.2.2)
# ==========================================================
