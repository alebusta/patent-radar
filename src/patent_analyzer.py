"""
Strategic Patent Radar — Patent Analyzer
QaiLabs / AREA_51 / patent_radar

Analiza los resultados de patent_search.py y genera estadísticas.
Uso: python patent_analyzer.py [archivo.json]
     python patent_analyzer.py  (analiza el más reciente)
"""

import sys
import os
import json
import glob
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_DIR


def load_latest_results(filepath=None):
    """Load the most recent JSON results file, or a specific one."""
    if filepath:
        path = filepath
    else:
        json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
        if not json_files:
            print("❌ No se encontraron archivos de resultados en data/")
            print(f"   Directorio: {DATA_DIR}")
            print("   Ejecuta primero: python patent_search.py \"query\"")
            sys.exit(1)
        path = max(json_files, key=os.path.getmtime)
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"📂 Archivo cargado: {os.path.basename(path)}")
    print(f"   Query: {data.get('query', 'N/A')}")
    print(f"   Fecha: {data.get('timestamp', 'N/A')}")
    print(f"   Patentes: {data.get('count', 0)}")
    
    return data


def analyze_patents(data):
    """
    Generate analysis from patent data.
    
    Returns dict with analysis results.
    """
    patents = data.get("patents", [])
    
    if not patents:
        print("\n⚠️  No hay patentes para analizar.")
        return None
    
    analysis = {}
    
    # --- Top Assignees ---
    assignees = [p.get("assignee", "N/A") for p in patents if p.get("assignee") and p.get("assignee") != "N/A"]
    analysis["top_assignees"] = Counter(assignees).most_common(10)
    
    # --- Country Distribution ---
    countries = [p.get("country", "N/A") for p in patents if p.get("country") and p.get("country") != "N/A"]
    analysis["countries"] = Counter(countries).most_common(10)
    
    # --- Year Distribution ---
    years = []
    for p in patents:
        date_str = p.get("date", "")
        if date_str and date_str != "N/A":
            try:
                year = date_str[:4]
                if year.isdigit():
                    years.append(int(year))
            except (ValueError, IndexError):
                pass
    analysis["years"] = Counter(years).most_common(10)
    
    # --- CPC Codes ---
    all_cpc = []
    for p in patents:
        cpc = p.get("cpc_codes", [])
        if isinstance(cpc, list):
            all_cpc.extend(cpc)
        elif isinstance(cpc, str):
            all_cpc.extend([c.strip() for c in cpc.split(";")])
    analysis["cpc_codes"] = Counter(all_cpc).most_common(15)
    
    # --- Stats ---
    analysis["total"] = len(patents)
    analysis["with_abstract"] = sum(1 for p in patents if p.get("abstract"))
    analysis["unique_assignees"] = len(set(assignees))
    analysis["unique_countries"] = len(set(countries))
    
    return analysis


def print_report(analysis, query_name=""):
    """Print a formatted analysis report."""
    if not analysis:
        return
    
    print("\n" + "=" * 60)
    print(f"📊 ANÁLISIS: STRATEGIC PATENT RADAR")
    if query_name:
        print(f"   Cluster: {query_name}")
    print("=" * 60)
    
    # Summary
    print(f"\n📈 Resumen General:")
    print(f"   • Total de patentes: {analysis['total']}")
    print(f"   • Con abstract: {analysis['with_abstract']}")
    print(f"   • Assignees únicos: {analysis['unique_assignees']}")
    print(f"   • Países únicos: {analysis['unique_countries']}")
    
    # Top Assignees
    if analysis["top_assignees"]:
        print(f"\n🏢 Top Assignees (Quién Patenta Más):")
        for i, (name, count) in enumerate(analysis["top_assignees"], 1):
            bar = "█" * count
            print(f"   {i:2}. {name[:40]:<40} {bar} ({count})")
    
    # Countries
    if analysis["countries"]:
        print(f"\n🌍 Distribución por País:")
        for code, count in analysis["countries"]:
            flag = get_flag(code)
            bar = "█" * count
            print(f"   {flag} {code}: {bar} ({count})")
    
    # Years
    if analysis["years"]:
        years_sorted = sorted(analysis["years"], key=lambda x: x[0])
        print(f"\n📅 Timeline (Año de Publicación):")
        for year, count in years_sorted:
            bar = "█" * count
            print(f"   {year}: {bar} ({count})")
    
    # CPC Codes
    if analysis["cpc_codes"]:
        print(f"\n🏷️  Top Clasificaciones CPC:")
        for code, count in analysis["cpc_codes"][:8]:
            if code.strip():
                print(f"   • {code}: ({count} patentes)")
    
    print("\n" + "=" * 60)
    print("🛰️  Análisis completado — Strategic Patent Radar / QAI Labs")
    print("=" * 60)


def get_flag(country_code):
    """Get emoji flag for a country code."""
    flags = {
        "US": "🇺🇸", "CN": "🇨🇳", "JP": "🇯🇵", "KR": "🇰🇷",
        "DE": "🇩🇪", "FR": "🇫🇷", "GB": "🇬🇧", "EP": "🇪🇺",
        "WO": "🌐", "CA": "🇨🇦", "AU": "🇦🇺", "IN": "🇮🇳",
        "BR": "🇧🇷", "CL": "🇨🇱", "IL": "🇮🇱", "TW": "🇹🇼",
    }
    return flags.get(country_code, "🏳️")


def analyze_all_files():
    """Analyze all JSON files in data directory."""
    json_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    
    if not json_files:
        print("❌ No se encontraron archivos de resultados.")
        return
    
    print(f"\n📂 Encontrados {len(json_files)} archivos de resultados\n")
    
    for filepath in json_files:
        data = load_latest_results(filepath)
        analysis = analyze_patents(data)
        print_report(analysis, data.get("query", ""))
        print()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--all":
            analyze_all_files()
        elif os.path.isfile(arg):
            data = load_latest_results(arg)
            analysis = analyze_patents(data)
            print_report(analysis, data.get("query", ""))
        else:
            print(f"❌ Archivo no encontrado: {arg}")
            print("Uso: python patent_analyzer.py [archivo.json]")
            print("     python patent_analyzer.py --all")
    else:
        # Default: analyze most recent file
        data = load_latest_results()
        analysis = analyze_patents(data)
        print_report(analysis, data.get("query", ""))


if __name__ == "__main__":
    main()
