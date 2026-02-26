# PRD: Strategic Patent Radar v0.1

> **Producto**: Strategic Patent Radar  
> **Codename**: `patent_radar`  
> **Clasificación**: QaiLabs / AREA_51 (Experimento)  
> **Fecha**: 25-Feb-2026  
> **Autor**: Nzero (Arquitecto QAI)  
> **Sponsor**: Alejandro Bustamante (Founder)

---

## 1. Problema

Las grandes empresas (como Walmart Chile) necesitan mapear el panorama global de patentes e I+D para tomar decisiones estratégicas de inversión e innovación. Actualmente dependen de:

- **Consultoras tradicionales** (ej. iale, subcontratadas por el Centro de Innovación UC) que producen reportes estáticos de 100+ páginas, desactualizados al momento de su entrega.
- **Búsquedas manuales** en Google Patents, WIPO o INAPI que consumen semanas de un analista humano.

**Pain Point**: No existe un servicio ágil que combine velocidad de IA con profundidad de dominio para entregar vigilancia tecnológica "viva" (actualizable) en lugar de reportes estáticos.

---

## 2. Oportunidad

QAI puede posicionarse como el **"Lab de IA"** que ofrece vigilancia tecnológica de siguiente generación. Nuestra ventaja competitiva:

- **Agentic Search**: Agentes de IA que procesan miles de patentes en horas, no semanas.
- **Hub Interactivo**: Dashboard web donde el cliente explora clusters de patentes, filtros geográficos y áreas de oportunidad ("Océanos Azules").
- **Costo Inferior**: ~20% menos que consultoras tradicionales (estructura lean, IA como multiplicador).

### Vertical Inicial (Walmart)
Foco en **Retail & Supply Chain**, con los siguientes clusters de interés:
1. **5G, Robótica y Sensorización** (Penúltima y Última Milla, Drones).
2. **Retail Media & Hiper-personalización** (Monetización de datos POS).
3. **IA aplicada a Operaciones y Merma** (Visión artificial, Inventario en Tiempo Real).
4. **Fintech & Medios de Pago** (Checkout sin fricción).
5. **Sostenibilidad & Economía Circular** (Packaging, Huella de carbono, Eficiencia energética).

---

## 3. Alcance del MVP (Fase 1)

### En Scope (v0.1)
- **Extractor de Patentes**: Script Python que busca patentes en Google Patents (vía scraping web) para un cluster específico (ej. "Drones Última Milla").
- **Datos Extraídos por Patente**:
  - Título
  - Número de publicación
  - Assignee (empresa titular)
  - País de origen
  - Fecha de publicación
  - Abstract / Resumen
  - Clasificación CPC (Cooperative Patent Classification)
- **Output**: Archivo JSON + CSV con los resultados estructurados.
- **Análisis Básico**: Script que genera un resumen textual de los clusters encontrados (top assignees, países, tendencias temporales).

### Fuera de Scope (v0.1)
- Hub Interactivo / Dashboard (→ Fase 2).
- Cruce con datos de startups o M&A.
- Acceso a WIPO SOAP API (requiere suscripción de 600 CHF/año).
- Acceso a INAPI (requiere investigación adicional).

---

## 4. Arquitectura Técnica

### Stack
| Componente | Tecnología | Notas |
|:---|:---|:---|
| Lenguaje | Python 3.x | Consistente con QaiCore |
| Fuente de Datos | Google Patents (web scraping) | Gratis, sin API key |
| Parsing HTML | `requests` + `BeautifulSoup4` | Ligero, sin dependencias pesadas |
| Análisis | `pandas` | Para agregación y estadísticas |
| Output | JSON + CSV | Portable y consumible por futuro Hub |
| IA (Opcional) | Gemini API | Para resumen inteligente de abstracts |

### Estructura del Proyecto
```
QaiLabs/AREA_51/patent_radar/
├── README.md              # Descripción del experimento
├── docs/
│   └── PRD.md             # Este documento
├── src/
│   ├── patent_search.py   # Motor de búsqueda en Google Patents
│   ├── patent_analyzer.py # Análisis y clustering de resultados
│   └── config.py          # Configuración (queries, filtros, etc.)
├── data/
│   └── (resultados .json/.csv)
└── requirements.txt       # Dependencias Python
```

---

## 5. Queries de Búsqueda Inicial (Seed)

Para la validación del MVP, usaremos estas búsquedas iniciales enfocadas en el vertical de Walmart:

| Query | Cluster |
|:---|:---|
| `"drone delivery" OR "last mile drone" retail` | 5G/Robótica/Última Milla |
| `"warehouse robotics" OR "automated inventory" retail` | IA/Operaciones/Merma |
| `"retail media" OR "point of sale personalization" patent` | Retail Media |
| `"sustainable packaging" OR "circular economy" retail` | Sostenibilidad |

---

## 6. Criterios de Éxito (MVP)

| Métrica | Target |
|:---|:---|
| Patentes extraídas por query | ≥ 10 |
| Campos estructurados por patente | ≥ 5 (Título, Assignee, País, Fecha, Abstract) |
| Tiempo de ejecución por query | < 60 segundos |
| Output parseable | JSON válido + CSV limpio |
| Top Assignees identificados | ≥ 3 por cluster |

---

## 7. Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|:---|:---:|:---|
| Google bloquea scraping | 🔴 Alto | Rate limiting (2-3 seg entre requests), User-Agent rotation, fallback a SerpAPI |
| Datos incompletos | 🟡 Medio | Validar campos mínimos, logging de gaps |
| Scope creep (Walmart pide más) | 🟡 Medio | PRD define scope claro; todo fuera de v0.1 va a backlog |

---

## 8. Roadmap

| Fase | Entregable | Timeline |
|:---|:---|:---|
| **v0.1 (MVP)** | ✅ Extractor + CSV/JSON con patentes de 1 cluster | 25 Feb — Completado |
| **v0.2 (Multi-Cluster)** | ✅ Extracción de los 5 clusters (53 patentes) + análisis | 25 Feb — Completado |
| **v0.3 (Dashboard)** | ✅ Dashboard HTML interactivo con Chart.js + toggle día/noche | 25 Feb — Completado |
| **v0.4 (Refinamiento)** | Curar seeds por empresa, extraer assignee real | Próximo |
| **v1.0 (Hub)** | Deploy en Netlify + NLP con Gemini API | Sem 2 Mar |
| **v1.1 (Comercial)** | Deck Premium + Modelo de suscripción para Walmart | Post-Kickoff |

---
*"La IA es el combustible, pero la curiosidad es el motor." — QAI Labs*
