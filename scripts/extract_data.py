#!/usr/bin/env python3
"""
Extract reign duration data from analysis scripts and export as clean CSV files.
This script produces the datasets used in:
  "Global Weibull Analysis of Sovereign Reign Durations:
   A Reliability Engineering Approach to Quantifying Historical Political Stability"
"""

import csv
import os
import sys

# Add parent directory to path so we can import data
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# =============================================================================
# REIGN DURATION DATA
# Each polity: list of reign durations (years), region, succession type,
# temporal scope, and notes.
# =============================================================================

POLITIES = {
    "Roman Empire": {
        "durations": [
            41, 23, 4, 14, 1,
            1, 0.5, 0.5, 10, 2,
            15, 2, 1, 21, 23,
            19, 8, 13, 1, 4,
            4, 13, 6, 3, 0.25,
            2, 3, 0.5, 3, 15,
            5, 1, 6, 2, 1,
            2, 1, 21, 1, 13,
            24, 2, 3, 2, 8,
            16, 4, 13, 1, 15,
            5, 1, 5, 1, 1,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "27 BCE - 476 CE",
        "notes": "Western Roman emperors, Augustus to Romulus Augustulus",
    },
    "England/Britain": {
        "durations": [
            21, 13, 35, 19, 10,
            10, 17, 3, 56, 20,
            50, 22, 2, 13, 10,
            22, 2, 22, 24, 38,
            6, 5, 45, 22, 6,
            11, 25, 3, 13, 12,
            13, 33, 60, 10, 26,
            64, 9, 26, 16, 70,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "1066 - 2022",
        "notes": "William I to Elizabeth II",
    },
    "France": {
        "durations": [
            9, 26, 29, 29, 48,
            43, 44, 3, 17, 6,
            29, 6, 6, 5, 33,
            22, 14, 42, 39, 3,
            22, 15, 33, 12, 72,
            1, 14, 19, 22, 4,
            72, 5, 59, 16, 10,
            6, 10, 18,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "987 - 1870",
        "notes": "Hugh Capet to Napoleon III",
    },
    "Ottoman Empire": {
        "durations": [
            27, 36, 23, 10, 2,
            30, 31, 2, 31, 8,
            46, 8, 21, 3, 20,
            14, 1, 4, 18, 4,
            39, 8, 27, 24, 3,
            27, 17, 3, 16, 24,
            4, 31, 1, 15, 33,
            33, 9, 6, 4,
        ],
        "region": "Middle East",
        "succession": "hereditary",
        "period": "1299 - 1922",
        "notes": "Osman I to Mehmed VI",
    },
    "China (Tang)": {
        "durations": [
            9, 23, 1, 22, 34,
            6, 2, 29, 6, 14,
            26, 1, 15, 1, 7,
            14, 6, 13, 1, 16,
            15, 4,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "618 - 907",
        "notes": "Tang dynasty emperors",
    },
    "China (Ming)": {
        "durations": [
            31, 4, 22, 1, 10,
            14, 8, 23, 6, 18,
            16, 45, 6, 48, 29,
            7, 17,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "1368 - 1644",
        "notes": "Ming dynasty emperors",
    },
    "China (Qing)": {
        "durations": [
            18, 8, 61, 13, 45,
            25, 7, 30, 11, 2,
            3,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "1644 - 1912",
        "notes": "Qing dynasty emperors",
    },
    "Korea (Joseon)": {
        "durations": [
            6, 18, 32, 22, 4,
            2, 13, 1, 25, 12,
            38, 12, 2, 34, 8,
            16, 27, 10, 15, 46,
            4, 52, 15, 3, 14,
            34, 10, 13,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "1392 - 1910",
        "notes": "Joseon dynasty kings",
    },
    "Papacy (post-1000)": {
        "durations": [
            4, 12, 1, 8, 6,
            12, 1, 9, 23, 13,
            6, 2, 12, 1, 0.5,
            13, 16, 0.5, 1, 8,
            5, 14, 8, 3, 4,
            1, 5, 22, 0.5, 5,
            6, 18, 11, 1, 15,
            14, 2, 0.5, 3, 4,
            3, 10, 3, 2, 2,
            3, 4, 2, 9, 11,
            9, 1, 7, 19, 2,
            10, 1, 9, 16, 12,
            2, 12, 3, 14, 8,
            3, 6, 13, 0.5, 26,
            8, 11, 10, 2, 21,
            11, 15, 5, 0.3, 4,
            6, 13, 1, 6, 15,
            1, 8, 26, 3, 2,
            21, 10, 7, 2, 13,
            13, 2, 5, 21, 8,
            6, 10, 8, 17, 6,
            23, 7, 2, 32, 4,
            32, 25, 3, 10, 17,
            19, 5, 15, 34, 8,
            11,
        ],
        "region": "Europe",
        "succession": "elective",
        "period": "1000 - present",
        "notes": "Post-1000 CE popes; College of Cardinals established 1059",
    },
    "Mughal Empire": {
        "durations": [
            4, 10, 13, 49, 22,
            49, 1, 17, 0.5, 8,
            29, 6, 1, 7, 19,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "1526 - 1857",
        "notes": "Mughal emperors, Babur to Bahadur Shah II",
    },
    "Persia/Iran": {
        "durations": [
            24, 10, 52, 14, 17,
            17, 13, 5, 7, 2,
            11, 0.5, 1,
            16, 37, 48, 1, 16,
            6, 16, 16, 38,
        ],
        "region": "Middle East",
        "succession": "hereditary",
        "period": "1501 - 1979",
        "notes": "Safavid, Afsharid, Qajar, Pahlavi dynasties",
    },
    "Byzantine Empire": {
        "durations": [
            11, 27, 8, 9, 12,
            9, 27, 38, 3, 4,
            20, 8, 2, 13, 33,
            17, 6, 1, 31, 7,
            34, 5, 5, 10, 5,
            7, 9, 2, 25, 23,
            26, 6, 46, 2, 49,
            6, 3, 14, 12, 25,
            7, 4, 6, 2, 23,
            3, 3, 37, 3, 7,
            37, 25, 5, 3, 33,
            9, 4, 1, 57, 6,
            33, 18, 3, 24, 6,
            6, 9, 5, 21, 4,
            4,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "395 - 1453",
        "notes": "Eastern Roman / Byzantine emperors",
    },
    "Mamluk Sultanate": {
        "durations": [
            7, 17, 2, 1, 12,
            1, 9, 42, 1, 0.5,
            2, 3, 6, 2, 1,
            13, 1, 6, 21, 1,
            7, 1, 5, 15, 1,
            16, 1,
        ],
        "region": "Middle East",
        "succession": "elective",
        "period": "1250 - 1517",
        "notes": "Mamluk sultans of Egypt",
    },
    "Islamic Caliphate": {
        "durations": [
            2, 10, 12, 5,
            19, 3, 1, 21, 4,
            20, 2, 3, 20, 1,
            19, 1, 1, 1, 6,
            4, 22, 10, 10, 23,
            5, 20, 1, 15, 14,
            1, 6, 0.5, 10, 23,
            9, 15, 24, 1, 6,
            4, 1, 2, 5, 29,
            41, 13, 23, 12, 35,
            17, 12, 1, 36,
            1, 17,
        ],
        "region": "Middle East",
        "succession": "hereditary",
        "period": "632 - 1258",
        "notes": "Rashidun, Umayyad, and Abbasid caliphs",
    },
    "Denmark": {
        "durations": [
            28, 27, 8, 42, 5,
            7, 22, 25, 23, 18,
            17, 3, 13, 8, 16,
            20, 12, 9, 7, 9,
            19, 33, 20, 43, 16,
            16, 18, 31, 24, 17,
            11, 26, 24, 3, 11,
            29, 31, 12, 20, 40,
            31, 9, 28, 17, 57,
            6, 35, 27, 52,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "936 - present",
        "notes": "Danish monarchs, Gorm the Old to Frederick X",
    },
    "Sweden": {
        "durations": [
            37, 29, 3, 43, 25,
            21, 6, 38, 5, 21,
            36, 20, 19, 23, 28,
            5, 26, 37, 57, 23,
            43, 23, 52,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "1523 - present",
        "notes": "Swedish monarchs, Gustav I Vasa to Carl XVI Gustaf",
    },
    "Portugal": {
        "durations": [
            28, 27, 38, 6, 46,
            46, 6, 12, 38, 28,
            5, 6, 38, 14, 3,
            26, 37, 4, 3, 22,
            16, 13, 27, 44, 5,
            10, 21, 7, 2, 19,
            2,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "1139 - 1910",
        "notes": "Portuguese monarchs, Afonso I to Manuel II",
    },
    "Poland": {
        "durations": [
            33, 34, 13, 6, 13,
            36, 8, 24, 44, 8,
            32, 7, 33, 37, 3,
            14, 2, 48, 6, 5,
            42, 24, 5, 20, 24,
            16, 20, 5, 22, 31,
            30, 31,
        ],
        "region": "Europe",
        "succession": "elective",
        "period": "960 - 1795",
        "notes": "Polish rulers including elected kings under Golden Liberty",
    },
    "Egypt (New Kingdom)": {
        "durations": [
            21, 13, 22, 54, 9,
            22, 54, 10, 26, 38,
            17, 3, 1, 10, 67,
            11, 67, 10, 34, 6,
            2, 19, 7, 32, 25,
            8, 7, 8, 1, 9,
            27,
        ],
        "region": "Africa/Middle East",
        "succession": "hereditary",
        "period": "1550 - 1077 BCE",
        "notes": "New Kingdom pharaohs",
    },
    "Ethiopia": {
        "durations": [
            15, 14, 6, 29, 2,
            5, 10, 1, 15, 33,
            4, 16, 1, 12, 2,
            19, 7, 23, 3, 38,
            5, 11, 24, 9, 7,
            4, 44,
        ],
        "region": "Africa",
        "succession": "hereditary",
        "period": "1270 - 1974",
        "notes": "Solomonic dynasty emperors",
    },
    "Khmer Empire": {
        "durations": [
            48, 35, 13, 7, 6,
            28, 30, 12, 15, 50,
            37, 25, 4, 10, 2,
            16, 5, 8, 12, 20,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "802 - 1431",
        "notes": "Khmer empire kings",
    },
    "Thailand (Chakri)": {
        "durations": [
            27, 15, 27, 47, 16,
            15, 9, 18, 70, 7,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "1782 - present",
        "notes": "Chakri dynasty, Rama I to Rama X",
    },
    "Spain": {
        "durations": [
            12, 26, 40, 42, 23,
            35, 5, 13, 46, 23,
            21, 5, 25, 35, 2,
            17, 41, 39,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "1479 - present",
        "notes": "Spanish monarchs, Ferdinand/Isabella to Felipe VI",
    },
    "Russia": {
        "durations": [
            43, 3, 51, 3, 5,
            2, 0.5, 32, 8, 3,
            7, 36, 2, 25, 20,
            1, 21, 6, 34, 5,
            25, 30, 13, 26, 23,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "1462 - 1917",
        "notes": "Russian tsars/emperors, Ivan III to Nicholas II",
    },
    "Holy Roman Empire": {
        "durations": [
            37, 23, 22, 2, 17,
            17, 39, 20, 18, 2,
            38, 7, 18, 4, 37,
            2, 17, 6, 37, 12,
            32, 1, 10, 53, 27,
            3, 53, 12, 10, 6,
            12, 25, 5, 20, 7,
            47, 6, 1, 29, 5,
            10, 2, 14,
        ],
        "region": "Europe",
        "succession": "elective",
        "period": "962 - 1806",
        "notes": "Holy Roman Emperors, Otto I to Francis II",
    },
    "Scotland": {
        "durations": [
            24, 19, 16, 15, 8,
            9, 43, 5, 9, 12,
            4, 25, 8, 29, 17,
            17, 24, 35, 16, 4,
            17, 25, 11, 36, 19,
            35, 4, 23, 42, 28,
            16, 11, 13, 25, 26,
            29, 26, 19, 6, 37,
        ],
        "region": "Europe",
        "succession": "hereditary",
        "period": "843 - 1603",
        "notes": "Scottish monarchs, Kenneth I to James VI",
    },
    "USA (Presidents)": {
        "durations": [
            8, 4, 8, 8, 4,
            4, 4, 8, 4, 4,
            4, 3, 4, 8, 4,
            4, 4, 8, 4, 4,
            4, 4, 4, 8, 7,
            4, 8, 4, 12, 4,
            8, 8, 3, 5, 4,
            4, 8, 4, 8, 8,
            4, 4,
        ],
        "region": "Americas",
        "succession": "elective",
        "period": "1789 - present",
        "notes": "US presidents, Washington to Biden",
    },
    "Japan (Emperors)": {
        "durations": [
            32, 14, 4, 32, 36,
            5, 10, 14, 10, 8,
            2, 15, 6, 3, 11,
            19, 25, 7, 9, 4,
            8, 7, 2, 4, 33,
            9, 23, 10, 5, 9,
            3, 8, 3, 20, 4,
            5, 2, 2, 22, 10,
            2, 10, 7, 2, 4,
            16, 7, 2, 3, 2,
            4, 4, 5, 3, 3,
            10, 3, 3, 4, 5,
            5, 3, 21, 10, 20,
            11, 5, 14, 17, 9,
            14, 10, 9, 9, 3,
            19, 22, 19, 13, 5,
            21, 7, 14, 6, 4,
            20, 3, 4, 12, 63,
            15, 64,
        ],
        "region": "Asia",
        "succession": "hereditary",
        "period": "539 - present",
        "notes": "Japanese emperors from Emperor Kinmei (29th) onwards, excluding legendary emperors",
    },
    "Venice (Doges)": {
        "durations": [
            3, 18, 13, 12, 6,
            3, 7, 2, 5, 14,
            11, 5, 9, 12, 16,
            2, 17, 6, 5, 14,
            24, 16, 5, 10, 1,
            2, 17, 7, 1, 5,
            5, 11, 8, 3, 6,
            16, 2, 7, 16, 8,
            11, 5, 2, 6, 11,
            8, 3, 14, 5, 14,
            20, 14, 7, 10, 8,
            10, 9, 1, 4, 8,
            5, 9, 3, 6, 3,
            19, 11, 8, 3, 4,
            10, 6, 3, 12, 18,
            11, 7, 3, 6, 6,
            2, 16, 6,
        ],
        "region": "Europe",
        "succession": "elective",
        "period": "726 - 1797",
        "notes": "Venetian doges",
    },
    "Aztec Empire": {
        "durations": [
            51, 40, 26, 14, 18,
            17, 14, 9, 2,
        ],
        "region": "Americas",
        "succession": "elective",
        "period": "1325 - 1521",
        "notes": "Aztec tlatoanis",
    },
    "Inca Empire": {
        "durations": [
            30, 25, 30, 35, 40,
            30, 36, 35, 33, 20,
            5, 1,
        ],
        "region": "Americas",
        "succession": "hereditary",
        "period": "1200 - 1572",
        "notes": "Inca emperors (Sapa Incas)",
    },
}


def export_reign_durations():
    """Export all reign duration data as CSV."""
    filepath = os.path.join(OUTPUT_DIR, "reign_durations.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "polity", "reign_index", "duration_years", "region",
            "succession_type", "temporal_scope", "notes"
        ])
        for polity, info in sorted(POLITIES.items()):
            for i, dur in enumerate(info["durations"], 1):
                writer.writerow([
                    polity, i, dur, info["region"],
                    info["succession"], info["period"], info["notes"]
                ])
    print(f"Exported: {filepath} ({sum(len(v['durations']) for v in POLITIES.values())} reign records)")


# =============================================================================
# VIOLENT SUCCESSION DATA
# =============================================================================

VIOLENT_SUCCESSIONS = {
    "Roman Empire": {"violent": 32, "total": 55, "civil_wars": 12},
    "England/Britain": {"violent": 8, "total": 40, "civil_wars": 4},
    "France": {"violent": 4, "total": 38, "civil_wars": 8},
    "Ottoman Empire": {"violent": 12, "total": 38, "civil_wars": 5},
    "China (Tang)": {"violent": 5, "total": 22, "civil_wars": 3},
    "China (Ming)": {"violent": 2, "total": 17, "civil_wars": 2},
    "China (Qing)": {"violent": 0, "total": 11, "civil_wars": 3},
    "Korea (Joseon)": {"violent": 4, "total": 28, "civil_wars": 2},
    "Papacy (post-1000)": {"violent": 4, "total": 121, "civil_wars": 0},
    "Mughal Empire": {"violent": 5, "total": 15, "civil_wars": 6},
    "Persia/Iran": {"violent": 5, "total": 22, "civil_wars": 4},
    "Byzantine Empire": {"violent": 29, "total": 71, "civil_wars": 11},
    "Mamluk Sultanate": {"violent": 15, "total": 27, "civil_wars": 3},
    "Islamic Caliphate": {"violent": 18, "total": 52, "civil_wars": 7},
    "Denmark": {"violent": 5, "total": 44, "civil_wars": 2},
    "Sweden": {"violent": 2, "total": 23, "civil_wars": 1},
    "Portugal": {"violent": 3, "total": 31, "civil_wars": 3},
    "Poland": {"violent": 3, "total": 32, "civil_wars": 4},
    "Ethiopia": {"violent": 8, "total": 27, "civil_wars": 5},
    "Spain": {"violent": 2, "total": 18, "civil_wars": 3},
    "Russia": {"violent": 7, "total": 25, "civil_wars": 3},
    "Holy Roman Empire": {"violent": 5, "total": 43, "civil_wars": 4},
    "Scotland": {"violent": 11, "total": 40, "civil_wars": 3},
    "USA (Presidents)": {"violent": 4, "total": 42, "civil_wars": 1},
    "Japan (Emperors)": {"violent": 5, "total": 96, "civil_wars": 4},
    "Venice (Doges)": {"violent": 5, "total": 83, "civil_wars": 0},
    "Aztec Empire": {"violent": 2, "total": 9, "civil_wars": 1},
    "Inca Empire": {"violent": 3, "total": 12, "civil_wars": 2},
    "Khmer Empire": {"violent": 6, "total": 20, "civil_wars": 3},
}


def export_violent_successions():
    """Export violent succession data as CSV."""
    filepath = os.path.join(OUTPUT_DIR, "violent_successions.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "polity", "violent_successions", "total_successions",
            "violent_rate", "civil_wars"
        ])
        for polity in sorted(VIOLENT_SUCCESSIONS.keys()):
            v = VIOLENT_SUCCESSIONS[polity]
            rate = v["violent"] / v["total"] if v["total"] > 0 else 0
            writer.writerow([
                polity, v["violent"], v["total"],
                f"{rate:.3f}", v["civil_wars"]
            ])
    print(f"Exported: {filepath}")


# =============================================================================
# ERA CLASSIFICATION
# =============================================================================

ERA_DEFINITIONS = {
    "Ancient": "Before 476 CE (Fall of Western Roman Empire)",
    "Medieval": "476 - 1453 CE (Fall of Constantinople)",
    "Early Modern": "1453 - 1789 CE (French Revolution)",
    "Modern": "1789 - 1945 CE (End of World War II)",
    "Contemporary": "1945 CE - present",
}


def export_era_definitions():
    """Export era classification definitions."""
    filepath = os.path.join(OUTPUT_DIR, "era_definitions.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["era", "definition"])
        for era, defn in ERA_DEFINITIONS.items():
            writer.writerow([era, defn])
    print(f"Exported: {filepath}")


# =============================================================================
# VARIABLE DEFINITIONS
# =============================================================================

def export_variable_definitions():
    """Export variable definitions and coding schemes."""
    filepath = os.path.join(OUTPUT_DIR, "variable_definitions.csv")
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["variable", "description", "type", "values"])
        rows = [
            ["polity", "Name of sovereign polity or dynasty", "categorical", "See reign_durations.csv"],
            ["reign_index", "Sequential index of reign within polity", "integer", "1, 2, 3, ..."],
            ["duration_years", "Reign duration in years", "continuous", ">0"],
            ["region", "Geographic region", "categorical", "Europe, Asia, Middle East, Africa, Americas, Africa/Middle East"],
            ["succession_type", "Predominant succession mechanism", "binary", "elective, hereditary"],
            ["temporal_scope", "Time period analysed for this polity", "text", "Start - End"],
            ["k", "Weibull shape parameter", "continuous", ">0; k<1=decreasing hazard, k=1=constant, k>1=increasing"],
            ["lambda", "Weibull scale parameter (years)", "continuous", ">0"],
            ["violent_successions", "Count of violent successions (assassination, deposition, coup)", "integer", ">=0"],
            ["total_successions", "Total number of successions in polity", "integer", ">0"],
            ["violent_rate", "Proportion of violent successions", "continuous", "0-1"],
            ["civil_wars", "Count of major internal armed conflicts", "integer", ">=0"],
            ["era", "Historical era classification", "categorical", "Ancient, Medieval, Early Modern, Modern, Contemporary"],
        ]
        for row in rows:
            writer.writerow(row)
    print(f"Exported: {filepath}")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    export_reign_durations()
    export_violent_successions()
    export_era_definitions()
    export_variable_definitions()
    print("\nAll data exported successfully.")
