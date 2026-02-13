# 🧠 ARSENAL — UI Uniformisation
# Synthese exploitable (V1) : taxonomie + catalogue de modeles + couverture

## 1) Taxonomie canonique (categories UI)
- NAV_BAR                 : barre d’icones (navigation / raccourcis)
- SECTION_HEADER          : en-tete de section (pilule titre + icone)
- TILE_KPI                : tuile valeur (value + unit)
- TILE_STATUS             : tuile etat (texte court : Ferme / Verrouille / Veille / Desactive…)
- TILE_ACTION             : tuile action (bouton / commande)
- CARD_TEXT_LIST          : carte texte liste (puces / lignes “Komori : temperature …”)
- GRAPH_LINE_STAT         : graphe ligne (stats / historique, bande min-max optionnelle)
- GRAPH_BAR_EVENTS        : graphe barres (intensite / impulsions)
- GRAPH_CUMUL_PERIODIC    : graphe cumul periodique (hebdo / mensuel / annuel)
- TIMELINE_STATE          : timeline etats (barre en bas : Humide / Desactive / Normal…)
- CARD_DIAGNOSTIC         : carte diagnostic structuree (etat + bullets + raison)
- CARD_TOOL_FORM          : carte outil (select + bouton + sortie)

---

## 2) Catalogue de modeles (templates a construire)
> Objectif : 12 modeles maximum, variantes par "etat severite" + options.

### TPL-01 — tpl_nav_bar (NAV_BAR)
- Usage : toutes vues (icones rondes en haut)
- Inputs : items[] = {icon, tap_path|tap_action, badge_entity?, visible_if?}

### TPL-02 — tpl_section_header (SECTION_HEADER)
- Usage : titres "Precipitations", "Jardin", "RDC", "Chambres", "Securite", "Historique"…
- Inputs : title, icon, right_slot? (optionnel : bouton/icone)

### TPL-03 — tpl_tile_kpi (TILE_KPI)
- Usage : temperature, humidite, co2, km, dB, g/m3, %
- Inputs : name, value_entity, unit, icon, secondary_line? (optionnel)
- Variantes severite : ok | info | warn | ko | off | unknown
  - Palette Arsenal (rappel) : vert OK / bleu info / jaune attention / orange warn / rouge KO / gris off / gris unknown

### TPL-04 — tpl_tile_kpi_primary (TILE_KPI “primary”)
- Usage : tuile mise en avant (ex : "Aujourd’hui 7.0 mm", "Eau chaude 32.6°C")
- Inputs : idem TPL-03 + emphasis=true

### TPL-05 — tpl_tile_status (TILE_STATUS)
- Usage : "Ferme", "Verrouille", "Veille", "Desactive", "A l'arret", "Reduit actif"
- Inputs : name, state_entity, icon, state_map? (optionnel : mapping FR)

### TPL-06 — tpl_tile_action (TILE_ACTION)
- Usage : "Charge", "Vaisselle", "Bouclage", toggles clim ("Ventilation silencieuse")
- Inputs : name, icon, tap_action(service|navigate), state_entity? (si retour etat)

### TPL-07 — tpl_card_text_list (CARD_TEXT_LIST)
- Usage : cartes "Conditions actuelles", "Stockage", listes temps reveils, historiques texte
- Inputs : title?, lines[] (ou entities[]), icon?

### TPL-08 — tpl_graph_line_stat (GRAPH_LINE_STAT)
- Usage : bruit dB, autonomie batterie, humidite (4 jours), ECS (temperature)
- Inputs : entity, window, show_minmax?, header_title, icon?

### TPL-09 — tpl_graph_bar_events (GRAPH_BAR_EVENTS)
- Usage : "Intensite (7 jours)" precipitation
- Inputs : entity, window, header_title, icon?

### TPL-10 — tpl_graph_cumul_periodic (GRAPH_CUMUL_PERIODIC)
- Usage : "Cumul hebdo (52 semaines)"
- Inputs : entity, period, span, header_title, icon?

### TPL-11 — tpl_timeline_state (TIMELINE_STATE)
- Usage : barres bas de page (Humide / Desactive / Normal / Chauffe ECS…)
- Inputs : entity, window, state_colors_map?

### TPL-12 — tpl_card_diagnostic (CARD_DIAGNOSTIC)
- Usage : Diagnostics alarme / aeration (etat + bullets + raison)
- Inputs : status (ok|warn|ko), title, bullets[], details? (optionnel)

### TPL-13 — tpl_card_tool_form (CARD_TOOL_FORM)
- Usage : "Creation d'ID pour automatisations"
- Inputs : title, select_entity, button_entity|tap_action, output_entity

---

## 3) Couverture (screenshots -> categories / templates)

### Meteo — Precipitations
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x1)
- KPI : TPL-03 (x2) + TPL-04 (x1)
- Graphs : TPL-09 (x1) + TPL-10 (x1)
- Timeline : TPL-11 (x1)

### Meteo — Temperature
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (multi : Jardin, RDC / Palier, Chambres, Salles de bains, Cave & Garage)
- Grilles tuiles : TPL-03 (majoritaire) + TPL-04 (occasionnel : “Jardin” full width)

### Meteo — Humidite Relative / Humidite Absolue / Humidex / CO2
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (multi : Jardin, RDC, Chambres, SDB, Cave & Garage…)
- Grilles tuiles : TPL-03 (majoritaire) + TPL-04 (occasionnel : “Exterieur” full width)

### Meteo — Bruit (chambres) + Reveils nocturnes
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x2 : “Bruit Chambres”, “Reveils nocturnes”)
- KPI : TPL-03 (x4 : 2x dB + 2x compte reveils)
- Graphs : TPL-08 (x2)
- Texte : TPL-07 (x2 : listes heures)

### Meteo — Backups (comparatifs Netatmo / Zigbee / Switchbot)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (par piece)
- KPI : TPL-03 (tuiles sources) + besoin “delta_line” via secondary_line (dans TPL-03)

### Modes
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x3 : “Modes”, “Decision Vacances”, “Historique”)
- Status : TPL-05 (x4 : Mode maison, Babysitting, Vacances, Justification)
- Timeline : TPL-11 (x1)

### VMC
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x3 : “Etat general”, “Conditions actuelles”, “Historique”)
- Status : TPL-05 (x2 : Intention VMC + VMC)
- KPI/Conditions : TPL-03 (x5)
- Timeline : TPL-11 (x1)

### Ouvertures
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x4 : Entree, Sejour, Chambre Parents, Chambre enfants)
- KPI (tuiles ouverture) : TPL-03 (x12)

### Mouvements
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x3 : Garage, Entree, Sejour)
- KPI (tuiles mouvement) : TPL-03 (x6)

### Volets
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x7 : Tous, Sejour, Chambres, Sejour Gauche, Sejour Droit, Chambre Arnaud, Chambre Matthieu)
- Actions : TPL-06 (x14 : Ouvrir/Fermer par section)

### Prises / Relais / Electromenager
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x5 : Maison – Reseau & Energie, Lumieres, Electromenager, Cave, Prises relais)
- Actions/Status : TPL-06 (majoritaire) + TPL-05 (occasionnel selon etat)
- Tuiles : TPL-06 (x17)

### NAS
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x6 : Etat general, Ressources systeme, Volume 1, Disque 1, Disque 2, Commandes systeme)
- KPI/Status : TPL-03 (x16)
- Actions : TPL-06 (x2 : Redemarrer / Eteindre)

### Systeme (Raspberry Pi / Integrations critiques)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x4 : Raspberry Pi, Systemes critiques, Integrations critiques, Connectivite Netatmo Homekit)
- KPI/Status : TPL-03 (x20)

### Navigation (menu principal)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x2 : Navigation, Systeme)
- Navigation tiles / Actions : TPL-06 (x33)

### Sante
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (x3 : Sommeil & recuperation, Sante / activite physiologique, Activite physique)
- KPI primary : TPL-04 (x2)
- KPI : TPL-03 (x5)
- Graph : TPL-08 (x1)

### Chauffage / Climatisation (decision systeme)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (Chauffiere/Climatiseur, Decision, Conditions, Historique)
- Status : TPL-05 (etats : “Attente+protection”, “Reduit actif”, “A l’arret”)
- KPI/Conditions : TPL-03
- Timeline : TPL-11 (historique / programme)

### ECS
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02
- KPI primary : TPL-04 (“Eau chaude …”)
- Actions : TPL-06 (Vaisselle, Bouclage)
- Graph : TPL-08 (temperature ECS)
- Timeline : TPL-11 (chauffe ECS)

### Cave (deshumidificateur)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (Cave, Conditions, Decision, Historique)
- Graph : TPL-08 (HR 4 jours)
- KPI : TPL-03 (criteres g/m3, HR)
- Status : TPL-05 (etat prise deshumidificateur)
- Timeline : TPL-11

### Aeration — Diagnostics
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (multi)
- Diagnostic : TPL-12 (lignes statut) + TPL-07 (donnees / synthese) selon rendu

### Alarme — Diagnostics
- NAV_BAR : TPL-01
- Diagnostic : TPL-12 (carte principale avec bullets)
- Status : TPL-05 (mode test)

### Eclairage
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02
- Actions/Status : TPL-06 (tuiles lampes) + TPL-05 (intention eclairage)

### Outil — ID automatisations
- NAV_BAR : TPL-01
- Tool form : TPL-13

### Audi (Batterie / Securite / Statistiques)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (Batterie & Autonomie, Securite, Mise a jour, Distance…)
- KPI : TPL-03/04 (batterie, autonomie, odometre, distances)
- Status : TPL-05 (portes/fenetres/coffre)
- Graph : TPL-08 (statistiques autonomie)
- Texte : TPL-07 (historique mensuel)

### Imprimerie (Menu / Meteo / Atelier / Bruit)
- NAV_BAR : TPL-01
- SECTION_HEADER : TPL-02 (Humidex, Bruit, Stockage, Atelier, Bureaux…)
- KPI : TPL-03 (tuiles temp/humidex/bruit)
- Graph : TPL-08 (bruit 24h)
- Texte : TPL-07 (conditions actuelles, min/max, historiques)

---

## Synthese — couverture templates (TPL -> ecrans)
- TPL-01 (NAV_BAR) : tous les ecrans ci-dessus
- TPL-02 (SECTION_HEADER) : tous les ecrans sauf les vues “mono-bloc” (rare)
- TPL-03 (KPI / tuiles) : Meteo (toutes), Ouvertures, Mouvements, Systeme, NAS, Sante, Imprimerie, Chauffage/Clim, ECS, Cave, VMC
- TPL-04 (KPI primary / full width) : Meteo (full width ponctuel), Precipitations (KPI central), Sante (top), ECS (primary)
- TPL-05 (STATUS) : Chauffage/Clim, Cave, VMC, Modes, Eclairage, Alarme, Prises (ponctuel)
- TPL-06 (ACTIONS / nav tiles) : Navigation, Volets, Prises, Eclairage, ECS, NAS (commandes)
- TPL-07 (TEXTE) : Bruit (heures), Audi (historique), Aeration (selon rendu), Imprimerie (blocs texte)
- TPL-08 (GRAPH “standard”) : Bruit, Sante, ECS, Cave, Audi, Imprimerie
- TPL-09 / TPL-10 (GRAPHS “pluie”) : Precipitations
- TPL-11 (TIMELINE) : Precipitations, Chauffage/Clim, ECS, Cave, VMC, Modes
- TPL-12 (DIAGNOSTIC) : Aeration, Alarme
- TPL-13 (TOOL FORM) : Outil — ID automatisations

---

## 4) Noyau minimal (ordre de construction pour uniformiser vite)
1) TPL-03 tpl_tile_kpi (+ variantes severite)  -> 80% des dashboards
2) TPL-02 tpl_section_header                 -> structure partout
3) TPL-01 tpl_nav_bar                        -> navigation coherente
4) TPL-05 tpl_tile_status + TPL-06 action    -> securite / controle
5) TPL-08 graph_line + TPL-11 timeline       -> historique standard
6) TPL-09/10 graph bar/cumul                 -> precipitations
7) TPL-07 text_list + TPL-12 diagnostic       -> diagnostics & syntheses
8) TPL-13 tool_form                          -> outils internes

---

## 5) Contrat d’uniformisation (parametres communs a tous les modeles)
- label / icon / entity (ou value_entity/state_entity)
- severity (ok|info|warn|ko|off|unknown) -> palette Arsenal
- layout_hint (1col | 2col | 3col | full)
- tap_action / hold_action (navigate/service/more-info)
- secondary_line (optionnel : delta, seuil, raison courte)

FIN. v