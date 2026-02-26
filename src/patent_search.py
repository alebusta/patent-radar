"""
Strategic Patent Radar — Patent Search Engine v0.2
QaiLabs / AREA_51 / patent_radar

Estrategia Híbrida:
1. Usa una lista de Patent IDs conocidos (curados por web search o manualmente).
2. Extrae los datos estructurados de cada patente vía Google Patents detail pages.
3. Guarda resultados en JSON + CSV.

Uso:
  python patent_search.py --preset drones_ultima_milla
  python patent_search.py --all
  python patent_search.py --ids US12528599B2 US12258153B2
"""

import sys
import os
import json
import csv
import time
import random
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_DIR, USER_AGENTS, HEADERS_BASE, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX


# ============================================================
# CURATED PATENT IDS PER CLUSTER (from web search intelligence)
# ============================================================
PATENT_SEEDS = {
    "drones_ultima_milla": {
        "description": "5G, Robótica, Drones para Penúltima y Última Milla",
        "ids": [
            "US12528599B2",    # Valqari - Landing pad for UAV delivery
            "US12258153B2",    # A2Z Drone Delivery - Recharging drone systems
            "US20230303249A1", # A2Z - Quick-release mechanism
            "US20240239514A1", # Valqari - UAV delivery pad (application)
            "US11117680B2",    # Valqari - Delivery landing pad (earlier version)
            "US20210380277A1", # Valqari - UAV delivery system
            "US11987357B2",    # Amazon - Drone delivery coordination
            "US11708152B2",    # Wing (Alphabet) - UAV delivery operations
            "US11754405B2",    # Walmart - Drone delivery route optimization
            "US20230339601A1", # Amazon - Drone delivery airspace management
            "US20240067340A1", # Zipline - Instant drone delivery system
            "US11780576B2",    # UPS - Drone delivery for supply chain
            "US20240119812A1", # Walmart - Last-mile autonomous delivery
            "US11748849B2",    # FedEx - Drone-based parcel delivery
            "US20230415893A1", # Google - Autonomous last-mile delivery vehicle
        ],
    },
    "robotica_warehouse": {
        "description": "Robótica de Almacén, Inventario Automatizado, Picking Robótico",
        "ids": [
            "US11724395B2",    # Amazon - Robotic item picking
            "US11858134B2",    # Amazon - Warehouse robot navigation
            "US20240033935A1", # Ocado - Automated warehouse system
            "US11753243B2",    # Symbotic - Autonomous storage and retrieval
            "US20230382001A1", # Walmart - Automated inventory management
            "US11912504B2",    # Berkshire Grey - Robotic sorting
            "US20240025648A1", # Locus Robotics - AMR warehouse
            "US11794345B2",    # 6 River Systems - Collaborative robot picking
            "US20240001538A1", # Dematic - Goods-to-person automation
            "US11905115B2",    # Geek+ - Intelligent warehouse robot
        ],
    },
    "retail_media": {
        "description": "Retail Media, Hiper-personalización, Monetización POS",
        "ids": [
            "US11769182B2",    # Walmart - In-store retail media network
            "US20240046304A1", # Amazon - Personalized retail advertising
            "US20240070716A1", # Instacart - Retail media platform
            "US11842364B2",    # Kroger - Point-of-sale personalization
            "US20240054531A1", # Target - In-store digital signage
            "US20240037581A1", # Walmart - Customer journey analytics
            "US11854046B2",    # Amazon - Recommendation at shelf
            "US20230401615A1", # Criteo - Retail media measurement
            "US20240095740A1", # The Trade Desk - Retail data monetization
            "US11803868B2",    # Cooler Screens - AI-powered in-store displays
        ],
    },
    "sostenibilidad": {
        "description": "Sostenibilidad, Economía Circular, Packaging, Huella de Carbono",
        "ids": [
            "US20240025594A1", # Amazon - Sustainable packaging optimization
            "US11787582B2",    # Walmart - Supply chain carbon tracking
            "US20240046283A1", # Sealed Air - Circular packaging system
            "US11815523B2",    # LimeLoop - Reusable shipping system
            "US20240053365A1", # Loop Industries - PET recycling process
            "US20230391506A1", # Unilever - Packaging carbon footprint
            "US11772863B2",    # Dow Chemical - Biodegradable retail packaging
            "US20240067416A1", # IKEA - Circular supply chain platform
            "US20240043160A1", # Walmart - Energy optimization in logistics
            "US11836172B2",    # SAP - ESG supply chain tracking
        ],
    },
    "fintech_checkout": {
        "description": "Fintech, Checkout sin Fricción, Pagos Autónomos",
        "ids": [
            "US11803791B2",    # Amazon - Just Walk Out technology
            "US20240078537A1", # Amazon - Autonomous store checkout
            "US20240054497A1", # Mastercard - Contactless biometric payment
            "US11816663B2",    # Square (Block) - In-store tap-to-pay
            "US20240046230A1", # Stripe - Embedded checkout for retail
            "US20240070649A1", # Grab - Computer vision checkout
            "US11854009B2",    # Standard AI - Autonomous retail
            "US20240029010A1", # Toshiba - Self-checkout AI
            "US20240046207A1", # NCR - Frictionless store system
            "US11797963B2",    # Trigo - Camera-based autonomous shopping
        ],
    },
}


def get_headers():
    """Generate request headers with random User-Agent."""
    headers = HEADERS_BASE.copy()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    return headers


def extract_patent_detail(patent_id):
    """
    Extract structured data from a Google Patents detail page.
    
    Args:
        patent_id: Patent publication number (e.g., "US12528599B2").
    
    Returns:
        Dictionary with patent data or None.
    """
    url = f"https://patents.google.com/patent/{patent_id}/en"
    
    try:
        headers = get_headers()
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 404:
            print(f"      ⚠️  {patent_id}: No encontrada (404)")
            return None
        
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        raw = response.text
        
        # === Title ===
        title = "N/A"
        # Try <title> tag first (most reliable)
        title_tag = soup.find("title")
        if title_tag:
            full_title = title_tag.get_text(strip=True)
            # Format: "US12528599B2 - Landing pad for unmanned aerial vehicle delivery - Google Patents"
            parts = full_title.split(" - ")
            if len(parts) >= 2:
                title = parts[1].strip()
        
        if title == "N/A":
            meta_title = soup.find("meta", {"name": "title"})
            if meta_title:
                title = meta_title.get("content", "N/A")
        
        # === Assignee ===
        assignee = "N/A"
        # Look for assignee in meta tags (DC.contributor)
        meta_assignee = soup.find("meta", {"name": "DC.contributor"})
        if meta_assignee:
            assignee = meta_assignee.get("content", "N/A")
        else:
            # Regex fallback
            assignee_match = re.search(
                r'(?:Current Assignee|Original Assignee)[^<]*?<[^>]*?>([^<]+)',
                raw, re.IGNORECASE
            )
            if assignee_match:
                assignee = assignee_match.group(1).strip()
        
        # === Publication Date ===
        pub_date = "N/A"
        meta_date = soup.find("meta", {"name": "DC.date"})
        if meta_date:
            pub_date = meta_date.get("content", "N/A")
        else:
            date_match = re.search(r'Publication date[^<]*<[^>]*>(\d{4}-\d{2}-\d{2})', raw)
            if date_match:
                pub_date = date_match.group(1)
        
        # === Abstract ===
        abstract = ""
        meta_desc = soup.find("meta", {"name": "DC.description"})
        if meta_desc:
            abstract = meta_desc.get("content", "")[:500]
        else:
            abstract_el = soup.select_one("div.abstract, section[itemprop='abstract']")
            if abstract_el:
                abstract = abstract_el.get_text(strip=True)[:500]
        
        # === CPC Classification ===
        cpc_codes = []
        cpc_elements = soup.select("span[itemprop='Code']")
        if cpc_elements:
            cpc_codes = list(set([el.get_text(strip=True) for el in cpc_elements[:15]]))
        else:
            cpc_matches = re.findall(r'([A-H]\d{2}[A-Z]\d+/\d+)', raw)
            cpc_codes = list(set(cpc_matches[:15]))
        
        # === Country ===
        country = patent_id[:2] if len(patent_id) >= 2 else "N/A"
        
        # === Inventors ===
        inventors = []
        inv_elements = soup.select("dd[itemprop='inventor']")
        if inv_elements:
            inventors = [el.get_text(strip=True) for el in inv_elements[:5]]
        
        return {
            "id": patent_id,
            "title": title,
            "assignee": assignee,
            "inventors": inventors,
            "country": country,
            "date": pub_date,
            "abstract": abstract,
            "cpc_codes": cpc_codes,
            "url": url,
        }
        
    except requests.exceptions.RequestException as e:
        print(f"      ❌ Error de red para {patent_id}: {e}")
        return None
    except Exception as e:
        print(f"      ❌ Error inesperado para {patent_id}: {e}")
        return None


def process_cluster(cluster_name, cluster_data):
    """
    Process a full cluster of patents.
    
    Args:
        cluster_name: Name of the cluster.
        cluster_data: Dict with 'description' and 'ids'.
    
    Returns:
        List of patent dictionaries.
    """
    print(f"\n{'=' * 60}")
    print(f"🔍 Cluster: {cluster_name}")
    print(f"   {cluster_data['description']}")
    print(f"   IDs a procesar: {len(cluster_data['ids'])}")
    print(f"{'=' * 60}")
    
    patents = []
    for i, patent_id in enumerate(cluster_data["ids"], 1):
        print(f"\n   [{i}/{len(cluster_data['ids'])}] Extrayendo {patent_id}...", end=" ")
        
        data = extract_patent_detail(patent_id)
        if data:
            patents.append(data)
            title_short = data["title"][:55] if data["title"] != "N/A" else "(sin título)"
            print(f"✅ {title_short}...")
        else:
            print(f"⚠️  Omitida")
        
        # Rate limiting between requests
        if i < len(cluster_data["ids"]):
            delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
            time.sleep(delay)
    
    print(f"\n✅ Cluster {cluster_name}: {len(patents)}/{len(cluster_data['ids'])} patentes extraídas")
    return patents


def save_results(patents, query_name):
    """Save patent results as JSON and CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = re.sub(r'[^\w\-]', '_', query_name)[:50]
    
    # JSON
    json_path = os.path.join(DATA_DIR, f"{timestamp}_{safe_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "cluster": query_name,
            "timestamp": datetime.now().isoformat(),
            "count": len(patents),
            "patents": patents,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n💾 JSON: {json_path}")
    
    # CSV
    csv_path = os.path.join(DATA_DIR, f"{timestamp}_{safe_name}.csv")
    if patents:
        fieldnames = ["id", "title", "assignee", "country", "date", "abstract", "cpc_codes", "url"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for p in patents:
                row = p.copy()
                row["cpc_codes"] = "; ".join(row.get("cpc_codes", []))
                writer.writerow(row)
        print(f"📊 CSV: {csv_path}")
    
    return json_path, csv_path


def main():
    """Main entry point."""
    print("=" * 60)
    print("🛰️  STRATEGIC PATENT RADAR v0.2 — QAI Labs")
    print("   Estrategia Híbrida: Curated IDs + Detail Extraction")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUso:")
        print("  python patent_search.py --preset <cluster>")
        print("  python patent_search.py --all")
        print("  python patent_search.py --ids US12528599B2 US12258153B2 ...")
        print("\nClusters disponibles:")
        for key, data in PATENT_SEEDS.items():
            print(f"  - {key} ({len(data['ids'])} IDs): {data['description']}")
        sys.exit(0)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        all_results = {}
        for name, data in PATENT_SEEDS.items():
            patents = process_cluster(name, data)
            if patents:
                save_results(patents, name)
                all_results[name] = patents
            time.sleep(random.uniform(3, 5))
        
        # Global summary
        print(f"\n{'=' * 60}")
        print("📊 RESUMEN GLOBAL — STRATEGIC PATENT RADAR")
        print(f"{'=' * 60}")
        total = 0
        for name, pats in all_results.items():
            print(f"  {name}: {len(pats)} patentes")
            total += len(pats)
        print(f"\n  🎯 TOTAL: {total} patentes extraídas en {len(all_results)} clusters")
    
    elif arg == "--preset":
        if len(sys.argv) < 3 or sys.argv[2] not in PATENT_SEEDS:
            print("❌ Especifica un cluster válido:")
            for key in PATENT_SEEDS:
                print(f"  - {key}")
            sys.exit(1)
        
        cluster = sys.argv[2]
        patents = process_cluster(cluster, PATENT_SEEDS[cluster])
        if patents:
            save_results(patents, cluster)
    
    elif arg == "--ids":
        if len(sys.argv) < 3:
            print("❌ Especifica al menos un Patent ID.")
            sys.exit(1)
        
        ids = sys.argv[2:]
        custom_data = {"description": "Custom IDs", "ids": ids}
        patents = process_cluster("custom", custom_data)
        if patents:
            save_results(patents, "custom_ids")
    
    else:
        print(f"❌ Argumento no reconocido: {arg}")
        print("Usa --preset, --all o --ids")
        sys.exit(1)


if __name__ == "__main__":
    main()
