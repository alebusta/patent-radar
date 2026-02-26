# Walkthrough: Strategic Patent Radar v0.3

> **Fecha**: 25-Feb-2026  
> **Autor**: Nzero (Arquitecto QAI)  
> **Sesión**: Sesión inicial — Construcción completa del MVP + Dashboard  
> **Estado**: ✅ Funcional — Listo para iterar

---

## 1. Qué se construyó

Un sistema de **vigilancia tecnológica de patentes** enfocado en el vertical retail (Walmart Chile), compuesto por:

1. **Extractor de patentes** (Python) que obtiene datos estructurados de Google Patents
2. **Analizador CLI** que genera estadísticas de los datos extraídos
3. **Dashboard interactivo** (HTML autocontenido) con gráficos Chart.js, toggle día/noche y tooltips

### Estructura del proyecto

```
QaiLabs/AREA_51/patent_radar/
├── dashboard.html              ← Dashboard interactivo (abrir en browser)
├── README.md                   ← Este archivo
├── requirements.txt            ← Dependencias Python
├── docs/
│   ├── PRD.md                  ← Product Requirements Document
│   └── WALKTHROUGH.md          ← Este documento
├── src/
│   ├── config.py               ← Configuración, seeds y queries
│   ├── patent_search.py        ← Motor de extracción v0.2 (estrategia híbrida)
│   ├── patent_analyzer.py      ← Análisis CLI con estadísticas
│   ├── consolidate.py          ← Consolida JSONs de clusters en uno solo
│   └── generate_dashboard.py   ← Genera dashboard.html desde datos consolidados
└── data/
    ├── consolidated_radar.json ← Datos maestros (todos los clusters)
    ├── *_drones_ultima_milla.json / .csv
    ├── *_robotica_warehouse.json / .csv
    ├── *_retail_media.json / .csv
    ├── *_sostenibilidad.json / .csv
    └── *_fintech_checkout.json / .csv
```

---

## 2. Arquitectura técnica

### Estrategia de extracción: Modelo Híbrido

Se intentó inicialmente scraping directo de la búsqueda de Google Patents, pero **Google Patents renderiza vía JavaScript client-side**, lo que hace inviable el scraping con `requests`.

**Solución implementada (Estrategia Híbrida):**

```
[ Web Search Intelligence ]  →  [ Patent IDs curados ]  →  [ Detail Page HTTP ]  →  [ HTML Parsing ]  →  [ JSON/CSV ]
        (manual/auto)              (55 seeds en 5 clusters)    (requests + BS4)       (meta tags + regex)
```

1. **Fase 1 — Curación de IDs**: Se usan búsquedas web para identificar IDs reales de patentes relevantes
2. **Fase 2 — Extracción**: Las páginas de detalle de Google Patents (`/patent/USXXXXXXX/en`) sí son accesibles vía HTTP y contienen datos estructurados en meta tags `<meta>` y `<span>` con clases específicas

### Campos extraídos por patente

| Campo | Fuente HTML | Notas |
|:---|:---|:---|
| `id` | Input (seed) | Ej: `US12528599B2` |
| `title` | `<meta name="DC.title">` | Título completo |
| `assignee` | `<meta name="DC.contributor">` | ⚠️ Actualmente es el inventor, no la empresa |
| `inventors` | `<meta name="DC.contributor">` (múltiples) | Lista completa |
| `country` | Prefijo del ID | `US`, `EP`, `WO`, etc. |
| `date` | `<meta name="DC.date">` | Fecha de publicación |
| `abstract` | `<meta name="DC.description">` | Resumen técnico |
| `cpc_codes` | `<span itemprop="Code">` | Clasificaciones CPC |
| `url` | Construida | Link directo a Google Patents |

---

## 3. Resultados de la sesión

### Extracción ejecutada

| Cluster | Seeds | Extraídas | Success Rate |
|:---|:---:|:---:|:---:|
| 🛸 Drones / Última Milla | 15 | 13 | 87% |
| 🤖 Robótica / Warehouse | 10 | 10 | 100% |
| 📺 Retail Media | 10 | 10 | 100% |
| 🌱 Sostenibilidad | 10 | 10 | 100% |
| 💳 Fintech / Checkout | 10 | 10 | 100% |
| **TOTAL** | **55** | **53** | **96%** |

### Datos consolidados
- **53 patentes** únicas (deduplicadas)
- **100% con abstract** disponible
- **Timeline**: 2018 → 2024
- **CPC dominantes**: B25J (Robótica), B64 (Aeronaves), G06Q (Comercio), B65G (Logística)
- **País**: 100% US (limitación del seed actual)

### Dashboard v0.3
- 4 gráficos Chart.js (clusters, timeline, CPC, países)
- Toggle día/noche con persistencia en localStorage
- Tooltips informativos en cada sección
- Explorador de patentes con búsqueda full-text y filtros por cluster
- Descripciones CPC en español

---

## 4. Cómo ejecutar (Guía rápida)

### Prerrequisitos
```bash
# Instalar dependencias (ya instaladas en .venv)
pip install requests beautifulsoup4 lxml pandas
```

### Extracción

```bash
# Extraer un cluster específico
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_search.py --preset drones_ultima_milla

# Extraer todos los clusters
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_search.py --all

# Extraer IDs específicos
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_search.py --ids US12528599B2 US12258153B2
```

### Análisis CLI

```bash
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_analyzer.py
```

### Dashboard (regenerar)

```bash
# 1. Consolidar datos de todos los clusters
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\consolidate.py

# 2. Generar dashboard HTML
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\generate_dashboard.py

# 3. Abrir
start patent_radar\dashboard.html
```

---

## 5. Limitaciones conocidas (v0.3)

| Limitación | Impacto | Solución propuesta |
|:---|:---|:---|
| `assignee` muestra inventor, no empresa | Medio | Extraer `<dd itemprop="assigneeOriginal">` del HTML |
| Seeds parcialmente incorrectos | Medio | Curar IDs con búsquedas más específicas por empresa |
| Solo patentes US | Bajo | Agregar seeds con prefijos EP, WO, CN |
| Sin análisis de texto NLP | Bajo | Agregar resumen con Gemini API en v1.0 |
| Browser tool bloqueado ($HOME env) | Bajo | Bug del entorno, no del código |

---

## 6. Próximos pasos (Roadmap)

| Fase | Entregable | Prioridad |
|:---|:---|:---:|
| **v0.4** | Refinar seeds con IDs verificados por empresa (Walmart, Amazon, Wing, Ocado) | 🔴 |
| **v0.4** | Extraer empresa assignee real (no inventor) | 🔴 |
| **v0.5** | Agregar más seeds por cluster (target: 50 por cluster = 250 total) | 🟡 |
| **v1.0** | Deploy dashboard en Netlify + CI automático | 🟡 |
| **v1.0** | Resumen NLP de abstracts con Gemini API | 🟢 |
| **v1.1** | Deck Premium para presentación a Walmart | 🟡 |

---

## 7. Archivos clave para retomar

| Archivo | Qué contiene | Cuándo leerlo |
|:---|:---|:---|
| `docs/PRD.md` | Problema, oportunidad, stack, alcance | Para contexto estratégico |
| `docs/WALKTHROUGH.md` | Este documento — estado actual | Para retomar la sesión |
| `src/config.py` | Seeds, headers, rate limiting | Para agregar nuevos clusters o IDs |
| `src/patent_search.py` | Motor de extracción (PATENT_SEEDS dict) | Para modificar extracción |
| `data/consolidated_radar.json` | Datos maestros | Para análisis adicional |
| `dashboard.html` | Dashboard autocontenido | Para demo/presentación |

---

*QaiLabs / AREA_51 — "La IA es el combustible, pero la curiosidad es el motor."*
