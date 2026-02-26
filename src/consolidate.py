"""
Strategic Patent Radar — Data Consolidator
Combina todos los JSONs de clusters en un solo archivo para el dashboard.
"""

import os
import sys
import json
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA_DIR


def consolidate():
    """Merge all cluster JSON files into a single dashboard data file."""
    json_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.json")))
    
    # Exclude the consolidated file itself
    json_files = [f for f in json_files if "consolidated" not in os.path.basename(f)]
    
    if not json_files:
        print("❌ No JSON files found in data/")
        return
    
    all_data = {
        "title": "Strategic Patent Radar: Retail 2026",
        "subtitle": "Vigilancia Tecnológica para Walmart Chile",
        "generated": "",
        "clusters": {},
        "all_patents": [],
        "stats": {},
    }
    
    from datetime import datetime
    all_data["generated"] = datetime.now().isoformat()
    
    total = 0
    all_assignees = {}
    all_countries = {}
    all_years = {}
    all_cpc = {}
    
    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cluster_name = data.get("cluster", os.path.basename(filepath))
        patents = data.get("patents", [])
        
        all_data["clusters"][cluster_name] = {
            "count": len(patents),
            "patents": patents,
        }
        
        for p in patents:
            p["cluster"] = cluster_name
            all_data["all_patents"].append(p)
            total += 1
            
            # Aggregate stats
            assignee = p.get("assignee", "N/A")
            if assignee and assignee != "N/A":
                all_assignees[assignee] = all_assignees.get(assignee, 0) + 1
            
            country = p.get("country", "N/A")
            if country and country != "N/A":
                all_countries[country] = all_countries.get(country, 0) + 1
            
            date = p.get("date", "")
            if date and date != "N/A" and len(date) >= 4:
                year = date[:4]
                if year.isdigit():
                    all_years[year] = all_years.get(year, 0) + 1
            
            for cpc in p.get("cpc_codes", []):
                if cpc and len(cpc) > 3:
                    all_cpc[cpc] = all_cpc.get(cpc, 0) + 1
    
    # Sort stats
    all_data["stats"] = {
        "total_patents": total,
        "total_clusters": len(all_data["clusters"]),
        "top_assignees": sorted(all_assignees.items(), key=lambda x: -x[1])[:15],
        "countries": sorted(all_countries.items(), key=lambda x: -x[1]),
        "years": sorted(all_years.items(), key=lambda x: x[0]),
        "top_cpc": sorted(all_cpc.items(), key=lambda x: -x[1])[:20],
    }
    
    # Save consolidated
    output_path = os.path.join(DATA_DIR, "consolidated_radar.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Datos consolidados: {output_path}")
    print(f"   {total} patentes en {len(all_data['clusters'])} clusters")
    
    return output_path


if __name__ == "__main__":
    consolidate()
