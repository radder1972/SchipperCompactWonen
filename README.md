# Schipper Compact Wonen

Moderne, conversiegerichte website voor **Schipper Compact Wonen** — specialist in ergonomische sta-op-stoelen en maatwerk zitsystemen in Dordrecht en omgeving.

## Inhoud
- **Homepage (`index.html`)**: Uitgevoerd in de Scandinavische interieurstijl met een frictieloze conversiefunnel:
  - Vaste afspraak CTA en mobiele sticky bar
  - Waarom Wij / USP-stappenpad
  - Zithouding Checklist PDF lead-magnet met directe download
  - Assortimentskaarten gekoppeld aan de collectie
  - Klantervaringen carrousel en fotocitaat bewegingstechnoloog
  - Showroom- en thuisbezoek modals met Google Maps integratie
- **Collectie Catalogus (`collectie.html`)**:
  - Gekoppeld aan de 40+ stoelen uit de `database.json`
  - Automatische fallback / live-sync met de API van Staopstoelen.nl
  - Filters op conditie (*Nieuw* vs *Occasions*), merk, type en sortering
  - Zoekbalk op trefwoord/model
  - Stoel Detail Modal met volledige specificaties, fotogalerij en proefzit-planner
- **Iconen (`assets/icons/`)**:
  - Maatwerk iconenset van 29 coherente SVG-iconen (duotone accent, 24px grid, 1.75 stroke) inclusief overzichtspagina (`assets/icons/overzicht.html`) en inline sprite.
- **Design Varianten (`varianten.html`)**:
  - Vergelijkingstool tussen het Scandinavische design, het Editorial woonmagazine-design (`design-editorial.html`) en het Modern Tailwind-design (`design-modern.html`).

## Lokaal bekijken
Open simpelweg `index.html` in de browser of start een lokale webserver:
```bash
python3 -m http.server 3000
```
Open vervolgens in je browser: [http://localhost:3000](http://localhost:3000)
