# BAKU Lead Package Generator

Motor de generación de paquetes de leads B2B para Agencia BAKU.

## Setup

```bash
pip install -r requirements.txt
export APOLLO_API_KEY="your_key_here"
```

## Uso

```bash
# Generar un paquete predefinido
python generate_package.py --package starter_saas

# Con filtro de ubicación
python generate_package.py --package growth_tech --location "United States"

# Filtrar por score mínimo
python generate_package.py --package enterprise_pack --min-score 50

# Custom: industria + cantidad + tier
python generate_package.py --custom --industry fintech --count 200 --tier premium

# Solo preview (sin gastar créditos)
python generate_package.py --package starter_saas --dry-run

# Listar paquetes e industrias disponibles
python generate_package.py --list-packages
python generate_package.py --list-industries
```

## Estructura

```
backend/
├── generate_package.py     # Entry point principal
├── config/
│   ├── packages.json       # Definiciones de paquetes (precio, tier, leads)
│   └── industries.json     # Templates por industria (filtros Apollo)
├── core/
│   ├── apollo_client.py    # Wrapper Apollo API (rate limiting, retry)
│   ├── lead_search.py      # Búsqueda de leads
│   ├── lead_enrich.py      # Enriquecimiento por tier
│   ├── lead_scorer.py      # Scoring y grading (A/B/C/D)
│   └── lead_export.py      # Export CSV/JSON
└── output/                 # Paquetes generados (CSV + JSON)
```

## Pipeline

1. **Search** — Busca leads en Apollo según industria/tier/ubicación
2. **Enrich** — Enriquece según nivel (basic/full/enterprise)
3. **Score** — Asigna score 0-100 y grade A/B/C/D
4. **Export** — Genera CSV + JSON con metadata

## Tiers

| Tier | Enrichment | Créditos/lead | Datos |
|------|-----------|---------------|-------|
| Standard | basic | ~1 | Nombre, email, empresa, cargo |
| Premium | full | ~2 | + LinkedIn, teléfono, intención |
| Enterprise | enterprise | ~3 | + Tecnografía, funding, org chart |
