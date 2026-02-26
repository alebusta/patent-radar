"""
Strategic Patent Radar — Dashboard Generator v2
Generates a self-contained HTML dashboard with light/dark toggle and tooltips.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_DIR

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_dashboard():
    """Generate HTML dashboard from consolidated data."""
    json_path = os.path.join(DATA_DIR, "consolidated_radar.json")
    
    if not os.path.exists(json_path):
        print("❌ consolidated_radar.json not found. Run consolidate.py first.")
        return
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Deduplicate patents by ID (keep latest)
    seen_ids = set()
    unique_patents = []
    for p in reversed(data.get("all_patents", [])):
        if p["id"] not in seen_ids:
            seen_ids.add(p["id"])
            unique_patents.append(p)
    unique_patents.reverse()
    data["all_patents"] = unique_patents
    data["stats"]["total_patents"] = len(unique_patents)
    
    json_inline = json.dumps(data, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategic Patent Radar — QAI Labs</title>
    <meta name="description" content="Dashboard de vigilancia tecnológica para retail: análisis de patentes globales">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
    <style>
        /* ═══════════════════════════════════════════
           THEME VARIABLES
        ═══════════════════════════════════════════ */
        [data-theme="dark"] {{
            --bg-primary: #0a0e1a;
            --bg-secondary: #111827;
            --bg-card: rgba(17, 24, 39, 0.7);
            --bg-card-solid: #111827;
            --bg-table-header: rgba(17, 24, 39, 0.5);
            --border-color: rgba(99, 102, 241, 0.2);
            --border-glow: rgba(99, 102, 241, 0.4);
            --border-row: rgba(99, 102, 241, 0.08);
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-blue: #6366f1;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --hover-row: rgba(99, 102, 241, 0.06);
            --chart-border: rgba(10, 14, 26, 0.8);
            --chart-grid: rgba(99, 102, 241, 0.06);
            --gradient-primary: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            --scrollbar-track: #0a0e1a;
            --scrollbar-thumb: rgba(99, 102, 241, 0.3);
            --toggle-bg: rgba(99, 102, 241, 0.2);
            --toggle-border: rgba(99, 102, 241, 0.3);
            --tooltip-bg: #1e293b;
            --tooltip-border: rgba(99, 102, 241, 0.3);
            --tooltip-text: #cbd5e1;
            --radial-1: rgba(99, 102, 241, 0.08);
            --radial-2: rgba(6, 182, 212, 0.06);
            --radial-3: rgba(16, 185, 129, 0.05);
            --shadow-card: rgba(99, 102, 241, 0.15);
        }}

        [data-theme="light"] {{
            --bg-primary: #f8fafc;
            --bg-secondary: #ffffff;
            --bg-card: rgba(255, 255, 255, 0.85);
            --bg-card-solid: #ffffff;
            --bg-table-header: rgba(241, 245, 249, 0.9);
            --border-color: rgba(99, 102, 241, 0.15);
            --border-glow: rgba(99, 102, 241, 0.35);
            --border-row: rgba(99, 102, 241, 0.06);
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --accent-blue: #6366f1;
            --accent-cyan: #0891b2;
            --accent-emerald: #059669;
            --accent-amber: #d97706;
            --accent-rose: #e11d48;
            --hover-row: rgba(99, 102, 241, 0.04);
            --chart-border: rgba(255, 255, 255, 0.9);
            --chart-grid: rgba(99, 102, 241, 0.08);
            --gradient-primary: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            --scrollbar-track: #f1f5f9;
            --scrollbar-thumb: rgba(99, 102, 241, 0.25);
            --toggle-bg: rgba(99, 102, 241, 0.1);
            --toggle-border: rgba(99, 102, 241, 0.2);
            --tooltip-bg: #ffffff;
            --tooltip-border: rgba(99, 102, 241, 0.2);
            --tooltip-text: #475569;
            --radial-1: rgba(99, 102, 241, 0.04);
            --radial-2: rgba(6, 182, 212, 0.03);
            --radial-3: rgba(16, 185, 129, 0.025);
            --shadow-card: rgba(99, 102, 241, 0.08);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            transition: background 0.4s ease, color 0.4s ease;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(ellipse at 20% 50%, var(--radial-1) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, var(--radial-2) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 80%, var(--radial-3) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
            transition: background 0.4s ease;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 24px;
            position: relative;
            z-index: 1;
        }}

        /* ═══════════════════════════════════════════
           THEME TOGGLE
        ═══════════════════════════════════════════ */
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 24px;
            z-index: 100;
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 16px;
            background: var(--toggle-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--toggle-border);
            border-radius: 100px;
            cursor: pointer;
            transition: all 0.3s ease;
            user-select: none;
        }}

        .theme-toggle:hover {{
            border-color: var(--accent-blue);
            box-shadow: 0 4px 16px var(--shadow-card);
            transform: translateY(-1px);
        }}

        .toggle-track {{
            width: 44px;
            height: 24px;
            background: var(--border-color);
            border-radius: 12px;
            position: relative;
            transition: background 0.3s;
        }}

        .toggle-thumb {{
            width: 18px;
            height: 18px;
            background: var(--accent-blue);
            border-radius: 50%;
            position: absolute;
            top: 3px;
            left: 3px;
            transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}

        [data-theme="light"] .toggle-thumb {{
            transform: translateX(20px);
        }}

        .toggle-icon {{
            font-size: 16px;
            line-height: 1;
        }}

        /* ═══════════════════════════════════════════
           TOOLTIP SYSTEM
        ═══════════════════════════════════════════ */
        .has-tooltip {{
            position: relative;
            cursor: help;
        }}

        .tooltip-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: var(--toggle-bg);
            border: 1px solid var(--border-color);
            font-size: 10px;
            font-weight: 700;
            color: var(--text-muted);
            cursor: help;
            transition: all 0.2s;
            flex-shrink: 0;
            margin-left: 6px;
        }}

        .tooltip-icon:hover {{
            background: var(--accent-blue);
            border-color: var(--accent-blue);
            color: white;
            transform: scale(1.1);
        }}

        .tooltip-bubble {{
            visibility: hidden;
            opacity: 0;
            position: absolute;
            z-index: 999;
            bottom: calc(100% + 10px);
            left: 50%;
            transform: translateX(-50%) translateY(4px);
            background: var(--tooltip-bg);
            border: 1px solid var(--tooltip-border);
            border-radius: 10px;
            padding: 10px 14px;
            width: max-content;
            max-width: 300px;
            font-size: 0.75rem;
            font-weight: 400;
            line-height: 1.5;
            color: var(--tooltip-text);
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            backdrop-filter: blur(12px);
            transition: all 0.2s ease;
            pointer-events: none;
        }}

        .tooltip-bubble::after {{
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: var(--tooltip-border);
        }}

        .tooltip-icon:hover + .tooltip-bubble,
        .tooltip-bubble:hover {{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(0);
            pointer-events: auto;
        }}

        /* ═══════════════════════════════════════════
           HEADER
        ═══════════════════════════════════════════ */
        .header {{
            padding: 40px 0 20px;
            text-align: center;
            position: relative;
        }}

        .header-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            background: var(--toggle-bg);
            border: 1px solid var(--toggle-border);
            border-radius: 100px;
            font-size: 12px;
            font-weight: 500;
            color: var(--accent-blue);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 16px;
        }}

        .header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }}

        .header .subtitle {{
            font-size: 1rem;
            color: var(--text-secondary);
            margin-top: 8px;
            font-weight: 300;
        }}

        .header .timestamp {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 12px;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* ═══════════════════════════════════════════
           KPI CARDS
        ═══════════════════════════════════════════ */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }}

        .kpi-card {{
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--gradient-primary);
            opacity: 0;
            transition: opacity 0.3s;
        }}

        .kpi-card:hover {{
            border-color: var(--border-glow);
            transform: translateY(-2px);
            box-shadow: 0 8px 32px var(--shadow-card);
        }}

        .kpi-card:hover::before {{ opacity: 1; }}

        .kpi-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .kpi-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
        }}

        .kpi-value {{
            font-size: 2.25rem;
            font-weight: 800;
            margin: 8px 0 4px;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .kpi-detail {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}

        /* ═══════════════════════════════════════════
           SECTIONS
        ═══════════════════════════════════════════ */
        .section {{
            margin: 32px 0;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }}

        .section-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section-title span {{ font-size: 1.3rem; }}

        /* ═══════════════════════════════════════════
           CHARTS
        ═══════════════════════════════════════════ */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .chart-card {{
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
        }}

        .chart-card:hover {{
            border-color: var(--border-glow);
            box-shadow: 0 4px 24px var(--shadow-card);
        }}

        .chart-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}

        .chart-header h3 {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .chart-container {{
            position: relative;
            height: 280px;
        }}

        /* ═══════════════════════════════════════════
           CLUSTER FILTERS
        ═══════════════════════════════════════════ */
        .cluster-filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 16px 0;
        }}

        .cluster-btn {{
            padding: 8px 16px;
            border: 1px solid var(--border-color);
            border-radius: 100px;
            background: transparent;
            color: var(--text-secondary);
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .cluster-btn:hover, .cluster-btn.active {{
            background: rgba(99, 102, 241, 0.15);
            border-color: var(--accent-blue);
            color: var(--text-primary);
        }}

        .cluster-btn.active {{
            background: rgba(99, 102, 241, 0.25);
        }}

        /* ═══════════════════════════════════════════
           PATENT TABLE
        ═══════════════════════════════════════════ */
        .patent-table-wrap {{
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            overflow: hidden;
        }}

        .patent-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .patent-table thead th {{
            padding: 14px 16px;
            text-align: left;
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid var(--border-color);
            background: var(--bg-table-header);
        }}

        .patent-table tbody tr {{
            border-bottom: 1px solid var(--border-row);
            transition: background 0.2s;
        }}

        .patent-table tbody tr:hover {{
            background: var(--hover-row);
        }}

        .patent-table tbody td {{
            padding: 12px 16px;
            font-size: 0.82rem;
            color: var(--text-secondary);
            vertical-align: top;
        }}

        .patent-table td:first-child {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--accent-cyan);
        }}

        .patent-table td:nth-child(2) {{
            color: var(--text-primary);
            font-weight: 500;
            max-width: 300px;
        }}

        .patent-table a {{
            color: var(--accent-cyan);
            text-decoration: none;
            transition: color 0.2s;
        }}

        .patent-table a:hover {{
            color: var(--accent-blue);
            text-decoration: underline;
        }}

        .cluster-tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.65rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .cluster-tag.drones_ultima_milla {{ background: rgba(99, 102, 241, 0.2); color: #818cf8; }}
        .cluster-tag.robotica_warehouse {{ background: rgba(16, 185, 129, 0.2); color: #34d399; }}
        .cluster-tag.retail_media {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; }}
        .cluster-tag.sostenibilidad {{ background: rgba(6, 182, 212, 0.2); color: #22d3ee; }}
        .cluster-tag.fintech_checkout {{ background: rgba(244, 63, 94, 0.2); color: #fb7185; }}

        [data-theme="light"] .cluster-tag.drones_ultima_milla {{ background: rgba(99, 102, 241, 0.12); color: #4f46e5; }}
        [data-theme="light"] .cluster-tag.robotica_warehouse {{ background: rgba(16, 185, 129, 0.12); color: #059669; }}
        [data-theme="light"] .cluster-tag.retail_media {{ background: rgba(245, 158, 11, 0.12); color: #b45309; }}
        [data-theme="light"] .cluster-tag.sostenibilidad {{ background: rgba(6, 182, 212, 0.12); color: #0e7490; }}
        [data-theme="light"] .cluster-tag.fintech_checkout {{ background: rgba(244, 63, 94, 0.12); color: #be123c; }}

        /* ═══════════════════════════════════════════
           SEARCH
        ═══════════════════════════════════════════ */
        .search-box {{
            width: 100%;
            padding: 12px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.3s, box-shadow 0.3s;
            margin-bottom: 16px;
        }}

        .search-box:focus {{
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
        }}

        .search-box::placeholder {{ color: var(--text-muted); }}

        /* ═══════════════════════════════════════════
           FOOTER
        ═══════════════════════════════════════════ */
        .footer {{
            text-align: center;
            padding: 40px 0;
            color: var(--text-muted);
            font-size: 0.75rem;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }}

        .footer a {{
            color: var(--accent-blue);
            text-decoration: none;
        }}

        /* ═══════════════════════════════════════════
           RESPONSIVE & SCROLLBAR
        ═══════════════════════════════════════════ */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.6rem; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .charts-grid {{ grid-template-columns: 1fr; }}
            .patent-table {{ font-size: 0.75rem; }}
            .theme-toggle {{ top: 10px; right: 12px; padding: 6px 12px; }}
        }}

        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: var(--scrollbar-track); }}
        ::-webkit-scrollbar-thumb {{ background: var(--scrollbar-thumb); border-radius: 3px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--accent-blue); }}
    </style>
</head>
<body>
    <!-- Theme Toggle -->
    <div class="theme-toggle" id="themeToggle" title="Cambiar entre modo claro y oscuro">
        <span class="toggle-icon" id="themeIcon">🌙</span>
        <div class="toggle-track">
            <div class="toggle-thumb"></div>
        </div>
        <span class="toggle-icon" id="themeIcon2">☀️</span>
    </div>

    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-badge">🛰️ QAI Labs — AREA_51</div>
            <h1>Strategic Patent Radar</h1>
            <p class="subtitle">Vigilancia Tecnológica — Retail 2026</p>
            <p class="timestamp" id="timestamp"></p>
        </header>

        <!-- KPIs -->
        <div class="section">
            <div class="section-header">
                <div class="section-title"><span>🎯</span> Indicadores Clave</div>
                <span class="tooltip-icon">?</span>
                <div class="tooltip-bubble">Métricas principales del análisis. Reflejan el alcance total de la extracción: cuántas patentes, clusters temáticos, inventores y cobertura de datos se obtuvieron.</div>
            </div>
            <div class="kpi-grid" id="kpis"></div>
        </div>

        <!-- Charts -->
        <div class="section">
            <div class="section-header">
                <div class="section-title"><span>📊</span> Análisis Visual</div>
                <span class="tooltip-icon">?</span>
                <div class="tooltip-bubble">Visualizaciones interactivas del panorama de patentes. Pase el cursor sobre los gráficos para ver detalles de cada segmento.</div>
            </div>
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Distribución por Cluster</h3>
                        <span class="tooltip-icon">?</span>
                        <div class="tooltip-bubble">Proporción de patentes por vertical de innovación. Cada cluster agrupa patentes relacionadas con un área estratégica para Walmart (ej: drones, robótica, retail media).</div>
                    </div>
                    <div class="chart-container"><canvas id="clusterChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Timeline de Publicación</h3>
                        <span class="tooltip-icon">?</span>
                        <div class="tooltip-bubble">Evolución temporal de las patentes por año de publicación. Permite identificar tendencias y picos de actividad inventiva en el sector retail.</div>
                    </div>
                    <div class="chart-container"><canvas id="timelineChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Top Clasificaciones CPC</h3>
                        <span class="tooltip-icon">?</span>
                        <div class="tooltip-bubble">Cooperative Patent Classification (CPC): sistema estándar para clasificar patentes por área tecnológica. Ej: B25J = Robótica, B64 = Aeronaves, G06Q = Comercio electrónico.</div>
                    </div>
                    <div class="chart-container"><canvas id="cpcChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Distribución por País</h3>
                        <span class="tooltip-icon">?</span>
                        <div class="tooltip-bubble">País de origen de las patentes según su identificador. Muestra dónde se concentra la actividad inventiva en las áreas analizadas.</div>
                    </div>
                    <div class="chart-container"><canvas id="countryChart"></canvas></div>
                </div>
            </div>
        </div>

        <!-- Patent Table -->
        <div class="section">
            <div class="section-header">
                <div class="section-title"><span>📋</span> Explorador de Patentes</div>
                <span class="tooltip-icon">?</span>
                <div class="tooltip-bubble">Tabla interactiva con todas las patentes extraídas. Use la barra de búsqueda para filtrar por título, inventor, ID o abstract. Los botones de cluster filtran por vertical. Click en el ID para ver la patente completa en Google Patents.</div>
            </div>
            <input type="text" class="search-box" id="searchBox" placeholder="🔍  Buscar por título, assignee, ID o abstract...">
            <div class="cluster-filters" id="clusterFilters"></div>
            <div class="patent-table-wrap">
                <table class="patent-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Título</th>
                            <th>Inventor</th>
                            <th>Fecha</th>
                            <th>Cluster</th>
                        </tr>
                    </thead>
                    <tbody id="patentTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- Footer -->
        <footer class="footer">
            <p>🛰️ Strategic Patent Radar v0.3 — <a href="https://qai.cl" target="_blank">QAI Labs</a></p>
            <p style="margin-top:4px;">Datos extraídos de Google Patents · Dashboard generado automáticamente</p>
        </footer>
    </div>

    <script>
    // ═══════════════════════════════════════════
    // THEME TOGGLE
    // ═══════════════════════════════════════════
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    let chartInstances = [];

    // Load saved theme
    const savedTheme = localStorage.getItem('patent-radar-theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {{
        const current = html.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('patent-radar-theme', next);
        updateThemeIcon(next);
        rebuildCharts();
    }});

    function updateThemeIcon(theme) {{
        document.getElementById('themeIcon').textContent = theme === 'dark' ? '🌙' : '🌙';
        document.getElementById('themeIcon2').textContent = theme === 'dark' ? '☀️' : '☀️';
    }}

    function getChartColors() {{
        const theme = html.getAttribute('data-theme');
        const isDark = theme === 'dark';
        return {{
            text: isDark ? '#94a3b8' : '#64748b',
            grid: isDark ? 'rgba(99,102,241,0.06)' : 'rgba(99,102,241,0.08)',
            border: isDark ? 'rgba(10, 14, 26, 0.8)' : 'rgba(255, 255, 255, 0.9)',
        }};
    }}

    // ═══════════════════════════════════════════
    // DATA
    // ═══════════════════════════════════════════
    const DATA = {json_inline};

    const seenIds = new Set();
    const patents = DATA.all_patents.filter(p => {{
        if (seenIds.has(p.id)) return false;
        seenIds.add(p.id);
        return true;
    }});

    const clusterColors = {{
        'drones_ultima_milla': '#818cf8',
        'robotica_warehouse': '#34d399',
        'retail_media': '#fbbf24',
        'sostenibilidad': '#22d3ee',
        'fintech_checkout': '#fb7185',
    }};

    const clusterLabels = {{
        'drones_ultima_milla': '🛸 Drones / Última Milla',
        'robotica_warehouse': '🤖 Robótica / Warehouse',
        'retail_media': '📺 Retail Media',
        'sostenibilidad': '🌱 Sostenibilidad',
        'fintech_checkout': '💳 Fintech / Checkout',
    }};

    // CPC label descriptions
    const cpcDescriptions = {{
        'B25J': 'Robótica / Manipuladores',
        'B64C': 'Aeronaves (Drones)',
        'B64D': 'Carga aérea',
        'B64F': 'Infraestructura aeronáutica',
        'B64U': 'Vehículos aéreos no tripulados',
        'B65G': 'Logística / Transporte',
        'B65B': 'Empaquetado',
        'G06Q': 'Comercio / Finanzas',
        'G06T': 'Procesamiento de imagen',
        'B01D': 'Separación / Filtrado',
        'G01C': 'Navegación / Medición',
        'B07C': 'Clasificación de objetos',
        'B23K': 'Soldadura',
        'B60L': 'Vehículos eléctricos',
        'A01M': 'Capturas / Trampas',
        'A47G': 'Equipamiento del hogar',
        'G08B': 'Señalización / Alarmas',
        'H05K': 'Circuitos impresos',
        'A61B': 'Diagnóstico médico',
        'B60P': 'Carrocerías de vehículos',
        'B64D1': 'Carga aérea',
        'B27B': 'Sierras / Corte de madera',
        'B23D': 'Corte / Cepillado',
    }};

    // === Timestamp ===
    document.getElementById('timestamp').textContent = 
        'Generado: ' + new Date(DATA.generated).toLocaleString('es-CL');

    // === KPIs ===
    const kpiContainer = document.getElementById('kpis');
    const uniqueClusters = [...new Set(patents.map(p => p.cluster))];
    const uniqueAssignees = [...new Set(patents.map(p => p.assignee).filter(a => a && a !== 'N/A'))];
    
    const kpis = [
        {{ label: 'Patentes Totales', value: patents.length, detail: 'Extraídas de Google Patents', tooltip: 'Número total de patentes únicas extraídas del repositorio de Google Patents mediante el sistema de extracción automatizado.' }},
        {{ label: 'Clusters Analizados', value: uniqueClusters.length, detail: 'Verticales de innovación', tooltip: 'Cada cluster agrupa patentes por área estratégica: Drones, Robótica, Retail Media, Sostenibilidad y Fintech.' }},
        {{ label: 'Inventores Únicos', value: uniqueAssignees.length, detail: 'Identificados en las patentes', tooltip: 'Inventores principales listados en las patentes. Nota: en v0.2, este campo muestra inventores, no empresas titulares.' }},
        {{ label: 'Con Abstract', value: patents.filter(p => p.abstract && p.abstract.trim()).length, detail: 'Cobertura de datos', tooltip: 'Porcentaje de patentes que incluyen el resumen técnico (abstract). Un indicador de la calidad de los datos extraídos.' }},
    ];

    kpis.forEach(kpi => {{
        const card = document.createElement('div');
        card.className = 'kpi-card';
        card.innerHTML = `
            <div class="kpi-header">
                <div class="kpi-label">${{kpi.label}}</div>
                <span class="tooltip-icon">?</span>
                <div class="tooltip-bubble">${{kpi.tooltip}}</div>
            </div>
            <div class="kpi-value">${{kpi.value}}</div>
            <div class="kpi-detail">${{kpi.detail}}</div>
        `;
        kpiContainer.appendChild(card);
    }});

    // ═══════════════════════════════════════════
    // CHARTS (with theme support)
    // ═══════════════════════════════════════════
    function buildCharts() {{
        const colors = getChartColors();

        // === Clusters (Doughnut) ===
        const clusterData = {{}};
        patents.forEach(p => {{
            const c = p.cluster || 'unknown';
            clusterData[c] = (clusterData[c] || 0) + 1;
        }});

        chartInstances.push(new Chart(document.getElementById('clusterChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(clusterData).map(k => clusterLabels[k] || k),
                datasets: [{{
                    data: Object.values(clusterData),
                    backgroundColor: Object.keys(clusterData).map(k => clusterColors[k] || '#666'),
                    borderColor: colors.border,
                    borderWidth: 3,
                    hoverOffset: 8,
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{
                            color: colors.text,
                            font: {{ family: 'Inter', size: 11 }},
                            padding: 12,
                            usePointStyle: true,
                            pointStyleWidth: 10,
                        }}
                    }}
                }}
            }}
        }}));

        // === Timeline ===
        const yearData = {{}};
        patents.forEach(p => {{
            if (p.date && p.date !== 'N/A' && p.date.length >= 4) {{
                const year = p.date.substring(0, 4);
                if (!isNaN(year)) yearData[year] = (yearData[year] || 0) + 1;
            }}
        }});
        const sortedYears = Object.keys(yearData).sort();

        chartInstances.push(new Chart(document.getElementById('timelineChart'), {{
            type: 'bar',
            data: {{
                labels: sortedYears,
                datasets: [{{
                    label: 'Patentes publicadas',
                    data: sortedYears.map(y => yearData[y]),
                    backgroundColor: sortedYears.map((_, i) => {{
                        const t = i / (sortedYears.length - 1 || 1);
                        return `rgba(${{Math.round(99 + (6-99)*t)}}, ${{Math.round(102 + (182-102)*t)}}, ${{Math.round(241 + (212-241)*t)}}, 0.7)`;
                    }}),
                    borderColor: sortedYears.map((_, i) => {{
                        const t = i / (sortedYears.length - 1 || 1);
                        return `rgba(${{Math.round(99 + (6-99)*t)}}, ${{Math.round(102 + (182-102)*t)}}, ${{Math.round(241 + (212-241)*t)}}, 1)`;
                    }}),
                    borderWidth: 1,
                    borderRadius: 6,
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{
                        grid: {{ color: colors.grid }},
                        ticks: {{ color: colors.text, font: {{ family: 'Inter', size: 11 }} }}
                    }},
                    y: {{
                        beginAtZero: true,
                        grid: {{ color: colors.grid }},
                        ticks: {{ color: colors.text, stepSize: 1, font: {{ family: 'Inter', size: 11 }} }}
                    }}
                }}
            }}
        }}));

        // === CPC ===
        const cpcData = {{}};
        patents.forEach(p => {{
            (p.cpc_codes || []).forEach(c => {{
                if (c && c.length > 3 && c.includes('/')) {{
                    const top = c.substring(0, c.indexOf('/'));
                    cpcData[top] = (cpcData[top] || 0) + 1;
                }}
            }});
        }});
        const topCpc = Object.entries(cpcData).sort((a,b) => b[1]-a[1]).slice(0, 10);

        chartInstances.push(new Chart(document.getElementById('cpcChart'), {{
            type: 'bar',
            data: {{
                labels: topCpc.map(c => c[0] + (cpcDescriptions[c[0]] ? ' · ' + cpcDescriptions[c[0]] : '')),
                datasets: [{{
                    label: 'Patentes con esta clasificación',
                    data: topCpc.map(c => c[1]),
                    backgroundColor: 'rgba(16, 185, 129, 0.5)',
                    borderColor: 'rgba(16, 185, 129, 1)',
                    borderWidth: 1,
                    borderRadius: 6,
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        grid: {{ color: colors.grid }},
                        ticks: {{ color: colors.text, stepSize: 1, font: {{ family: 'Inter', size: 11 }} }}
                    }},
                    y: {{
                        grid: {{ display: false }},
                        ticks: {{ color: colors.text, font: {{ family: 'Inter', size: 10 }} }}
                    }}
                }}
            }}
        }}));

        // === Countries ===
        const countryData = {{}};
        patents.forEach(p => {{
            if (p.country && p.country !== 'N/A') {{
                countryData[p.country] = (countryData[p.country] || 0) + 1;
            }}
        }});
        const topCountries = Object.entries(countryData).sort((a,b) => b[1]-a[1]).slice(0, 8);
        const countryFlags = {{'US':'🇺🇸','CN':'🇨🇳','JP':'🇯🇵','KR':'🇰🇷','DE':'🇩🇪','FR':'🇫🇷','GB':'🇬🇧','EP':'🇪🇺','WO':'🌐','CA':'🇨🇦','AU':'🇦🇺','IN':'🇮🇳'}};

        chartInstances.push(new Chart(document.getElementById('countryChart'), {{
            type: 'doughnut',
            data: {{
                labels: topCountries.map(c => (countryFlags[c[0]]||'🏳️') + ' ' + c[0]),
                datasets: [{{
                    data: topCountries.map(c => c[1]),
                    backgroundColor: ['#6366f1','#06b6d4','#10b981','#f59e0b','#f43f5e','#8b5cf6','#ec4899','#14b8a6'],
                    borderColor: colors.border,
                    borderWidth: 3,
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {{
                    legend: {{
                        position: 'right',
                        labels: {{
                            color: colors.text,
                            font: {{ family: 'Inter', size: 12 }},
                            padding: 14,
                            usePointStyle: true,
                        }}
                    }}
                }}
            }}
        }}));
    }}

    function rebuildCharts() {{
        chartInstances.forEach(c => c.destroy());
        chartInstances = [];
        buildCharts();
    }}

    buildCharts();

    // ═══════════════════════════════════════════
    // CLUSTER FILTERS
    // ═══════════════════════════════════════════
    let activeCluster = 'all';
    const filtersContainer = document.getElementById('clusterFilters');

    const allBtn = document.createElement('button');
    allBtn.className = 'cluster-btn active';
    allBtn.textContent = 'Todos';
    allBtn.onclick = () => {{ activeCluster = 'all'; renderTable(); updateFilters(); }};
    filtersContainer.appendChild(allBtn);

    Object.keys(clusterLabels).forEach(key => {{
        const btn = document.createElement('button');
        btn.className = 'cluster-btn';
        btn.textContent = clusterLabels[key];
        btn.onclick = () => {{ activeCluster = key; renderTable(); updateFilters(); }};
        filtersContainer.appendChild(btn);
    }});

    function updateFilters() {{
        document.querySelectorAll('.cluster-btn').forEach((btn, i) => {{
            if (i === 0) btn.classList.toggle('active', activeCluster === 'all');
            else {{
                const key = Object.keys(clusterLabels)[i - 1];
                btn.classList.toggle('active', activeCluster === key);
            }}
        }});
    }}

    // ═══════════════════════════════════════════
    // PATENT TABLE
    // ═══════════════════════════════════════════
    const tableBody = document.getElementById('patentTableBody');
    const searchBox = document.getElementById('searchBox');

    function renderTable() {{
        const query = searchBox.value.toLowerCase();
        let filtered = patents;

        if (activeCluster !== 'all') {{
            filtered = filtered.filter(p => p.cluster === activeCluster);
        }}

        if (query) {{
            filtered = filtered.filter(p =>
                (p.title || '').toLowerCase().includes(query) ||
                (p.assignee || '').toLowerCase().includes(query) ||
                (p.id || '').toLowerCase().includes(query) ||
                (p.abstract || '').toLowerCase().includes(query)
            );
        }}

        tableBody.innerHTML = filtered.map(p => `
            <tr>
                <td><a href="${{p.url}}" target="_blank" title="Ver patente completa en Google Patents">${{p.id}}</a></td>
                <td title="${{(p.abstract || '').replace(/"/g, '&quot;').substring(0, 200)}}...">${{p.title || 'N/A'}}</td>
                <td>${{p.assignee || 'N/A'}}</td>
                <td>${{p.date || 'N/A'}}</td>
                <td><span class="cluster-tag ${{p.cluster}}">${{(clusterLabels[p.cluster] || p.cluster).replace(/^[^ ]+ /, '')}}</span></td>
            </tr>
        `).join('');
    }}

    searchBox.addEventListener('input', renderTable);
    renderTable();
    </script>
</body>
</html>"""
    
    output_path = os.path.join(BASE_DIR, "dashboard.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Dashboard v0.3 generado: {output_path}")
    print(f"   Patentes: {len(unique_patents)} (deduplicadas)")
    print(f"   Features: Light/Dark toggle + Tooltips informativos")
    return output_path


if __name__ == "__main__":
    generate_dashboard()
