# 🛰️ Strategic Patent Radar — AREA_51

> **Codename**: `patent_radar`  
> **Misión**: Mapeo automatizado de patentes globales para vigilancia tecnológica retail.  
> **Cliente Prospecto**: Walmart Chile (vía Centro de Innovación UC / Iliana Alzurutt).  
> **Estado**: ✅ v0.3 — MVP funcional con Dashboard interactivo.

---

## 📄 Documentación

| Doc | Descripción |
|:---|:---|
| [PRD.md](docs/PRD.md) | Problema, oportunidad, stack, alcance y roadmap |
| [WALKTHROUGH.md](docs/WALKTHROUGH.md) | Estado actual, resultados, cómo ejecutar y cómo retomar |

---

## 🛠️ Stack

- **Python 3.x** + `requests` + `BeautifulSoup4` + `pandas`
- **Fuente**: Google Patents (extracción de detail pages vía HTTP)
- **Dashboard**: HTML autocontenido + Chart.js (sin servidor)
- **Output**: JSON + CSV + Dashboard HTML

---

## 📊 Datos actuales

| Cluster | Patentes |
|:---|:---:|
| 🛸 Drones / Última Milla | 13 |
| 🤖 Robótica / Warehouse | 10 |
| 📺 Retail Media | 10 |
| 🌱 Sostenibilidad | 10 |
| 💳 Fintech / Checkout | 10 |
| **Total** | **53** |

---

## 🚀 Cómo Ejecutar

```bash
# Desde la raíz del repo (TheQaiCo/)

# 1. Extraer todos los clusters
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_search.py --all

# 2. Extraer un solo cluster
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_search.py --preset drones_ultima_milla

# 3. Análisis CLI
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\patent_analyzer.py

# 4. Regenerar dashboard
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\consolidate.py
QaiCore\qrun.bat QaiLabs\AREA_51\patent_radar\src\generate_dashboard.py
```

## 🌐 Dashboard

Abrir `dashboard.html` en cualquier browser. Features:
- 4 gráficos interactivos (clusters, timeline, CPC, países)
- Toggle día/noche
- Tooltips informativos
- Explorador con búsqueda y filtros

---

*QaiLabs / AREA_51 — Zona Experimental*
