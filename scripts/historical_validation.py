#!/usr/bin/env python3
"""
Historical validation: violent succession events, civil wars, data scope rationale.
Creates Table 3 (violent succession rates) and Figure 6 (k vs violent succession rate).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# HISTORICAL VIOLENT SUCCESSION DATA
# For each polity: total successions, violent successions (coup, assassination,
# deposition by force, civil war outcome), and notable events
# =============================================================================

VALIDATION = {}

# --- EUROPE ---
VALIDATION["Roman Empire"] = {
    'total': 55, 'violent': 36,
    'scope_rationale': 'Principate and Dominate periods (27 BCE - 476 CE). Excludes the Republic, '
                       'as the political structure differed fundamentally (consuls, not emperors).',
    'events': [
        'Year of the Four Emperors (69 CE): civil war, 3 emperors killed',
        'Crisis of the Third Century (235-284): 26 emperors in 49 years, most assassinated',
        'Year of the Five Emperors (193 CE): civil war following assassination of Commodus',
        'Year of the Six Emperors (238 CE): civil war and multiple assassinations',
        'Assassination of Julius Caesar\'s heir system led to chronic instability',
    ],
    'civil_wars': 15,
    'puppet_note': 'Several child emperors (e.g., Elagabalus age 14, Gordian III age 13) served as figureheads.',
}

VALIDATION["England/Britain"] = {
    'total': 40, 'violent': 6,
    'scope_rationale': 'Norman Conquest (1066) to present. Pre-1066 Anglo-Saxon kings excluded due to '
                       'fragmented record-keeping and fundamentally different political structure (multiple kingdoms).',
    'events': [
        'Wars of the Roses (1455-1487): dynastic civil war, 2 kings deposed',
        'English Civil War (1642-1651): Charles I executed',
        'Glorious Revolution (1688): James II deposed (bloodless)',
        'Deposition of Edward II (1327) and Richard II (1399)',
    ],
    'civil_wars': 3,
    'puppet_note': 'Henry VI (infant accession) and Edward V (child king, likely murdered) are included.',
}

VALIDATION["France"] = {
    'total': 38, 'violent': 4,
    'scope_rationale': 'Capetian dynasty onward (987-1870). Merovingian and Carolingian periods excluded '
                       'due to fragmented political structure and unreliable reign duration records.',
    'events': [
        'French Revolution (1789): Louis XVI executed',
        'Assassination of Henri III (1589) and Henri IV (1610)',
        'July Revolution (1830): Charles X abdicated under threat',
        'Franco-Prussian War (1870): Napoleon III deposed',
    ],
    'civil_wars': 2,
    'puppet_note': 'Several child kings under regency (e.g., Louis IX age 12, Louis XIV age 4).',
}

VALIDATION["Holy Roman Empire"] = {
    'total': 43, 'violent': 8,
    'scope_rationale': 'From Otto I (962) to dissolution (1806). Full period of the elective imperial institution.',
    'events': [
        'Investiture Controversy (1076-1122): multiple anti-kings',
        'Great Interregnum (1254-1273): no universally recognised emperor',
        'Thirty Years War (1618-1648): devastating religious-political conflict',
        'Multiple contested elections leading to rival claimants',
    ],
    'civil_wars': 5,
    'puppet_note': None,
}

VALIDATION["Denmark"] = {
    'total': 49, 'violent': 5,
    'scope_rationale': 'From Gorm the Old (936) to present. Full documented monarchical period.',
    'events': [
        'Civil war between Sweyn III and Valdemar I (1146-1157)',
        'Stockholm Bloodbath aftermath (1520)',
        'Transition to absolute monarchy (1660, peaceful)',
    ],
    'civil_wars': 2,
    'puppet_note': None,
}

VALIDATION["Sweden"] = {
    'total': 23, 'violent': 3,
    'scope_rationale': 'From Gustav I Vasa (1523) to present. Pre-Vasa period excluded due to union '
                       'complications (Kalmar Union) and fragmented records.',
    'events': [
        'Assassination of Gustav III (1792)',
        'Deposition of Eric XIV (1568)',
        'Revolution of 1809: Gustav IV Adolf deposed',
    ],
    'civil_wars': 1,
    'puppet_note': None,
}

VALIDATION["Scotland"] = {
    'total': 40, 'violent': 11,
    'scope_rationale': 'From Kenneth MacAlpin (843) to Union of Crowns (1603). Full independent Scottish monarchy.',
    'events': [
        'Wars of Scottish Independence (1296-1357)',
        'Multiple regicides: James I (1437), James III (1488)',
        'Forced abdication of Mary Queen of Scots (1567)',
        'Frequent minority reigns leading to noble factionalism',
    ],
    'civil_wars': 4,
    'puppet_note': 'Multiple child monarchs (James V age 1, Mary age 6 days) under regency.',
}

VALIDATION["Spain"] = {
    'total': 18, 'violent': 3,
    'scope_rationale': 'From Ferdinand and Isabella (1479) to present. Unified Spanish monarchy only.',
    'events': [
        'War of Spanish Succession (1701-1714)',
        'Napoleonic deposition of Ferdinand VII (1808)',
        'Spanish Civil War (1936-1939, affected monarchy indirectly)',
    ],
    'civil_wars': 2,
    'puppet_note': 'Joseph Bonaparte as imposed king (excluded from data).',
}

VALIDATION["Portugal"] = {
    'total': 31, 'violent': 5,
    'scope_rationale': 'From Afonso Henriques (1139) to end of monarchy (1910). Full Portuguese monarchical period.',
    'events': [
        '1383-1385 Crisis: succession war',
        'Portuguese Restoration War (1640): independence from Spain',
        'Assassination of Carlos I (1908)',
        'Republican Revolution (1910): Manuel II deposed',
    ],
    'civil_wars': 3,
    'puppet_note': None,
}

VALIDATION["Poland"] = {
    'total': 32, 'violent': 5,
    'scope_rationale': 'From Mieszko I (960) to Third Partition (1795). Includes both Piast dynasty and elective monarchy period.',
    'events': [
        'The Deluge (1655-1660): Swedish invasion devastated Poland',
        'Multiple contested royal elections after 1572',
        'Partitions of Poland (1772, 1793, 1795)',
    ],
    'civil_wars': 3,
    'puppet_note': 'Late elective period kings often had limited real power.',
}

VALIDATION["Russia"] = {
    'total': 25, 'violent': 8,
    'scope_rationale': 'From Ivan III (1462) to Nicholas II (1917). Muscovite and Imperial Russia.',
    'events': [
        'Time of Troubles (1598-1613): civil war, foreign intervention, multiple pretenders',
        'Palace coups of 18th century: Peter III (1762), Ivan VI (1741), Paul I (1801) assassinated/deposed',
        'Russian Revolution (1917): Nicholas II forced to abdicate, later executed',
        'Decembrist Revolt (1825)',
    ],
    'civil_wars': 2,
    'puppet_note': 'Ivan VI (infant emperor, overthrown at age 1).',
}

# --- MIDDLE EAST ---
VALIDATION["Ottoman Empire"] = {
    'total': 39, 'violent': 12,
    'scope_rationale': 'From Osman I (1299) to abolition of sultanate (1922). Full Ottoman period.',
    'events': [
        'Ottoman Interregnum (1402-1413): civil war among sons of Bayezid I',
        'Fratricide as state policy (Fatih Kanunnamesi): new sultans killed brothers',
        'Janissary revolts deposing sultans (e.g., Osman II 1622, Selim III 1807)',
        'Young Turk Revolution (1908-1909): Abdul Hamid II deposed',
    ],
    'civil_wars': 4,
    'puppet_note': 'Late Ottoman sultans (post-1876) increasingly figureheads under constitutional constraints.',
}

VALIDATION["Islamic Caliphate"] = {
    'total': 55, 'violent': 28,
    'scope_rationale': 'Rashidun, Umayyad, and Abbasid caliphates (632-1258 CE). Excludes post-Mongol '
                       'shadow caliphates in Cairo as they held no real political power.',
    'events': [
        'First Fitna (656-661): civil war, Ali assassinated',
        'Second Fitna (680-692): Battle of Karbala, multiple claimants',
        'Abbasid Revolution (750): overthrow of Umayyads, mass executions',
        'Third Fitna (744-747): Umayyad civil war',
        'Anarchy at Samarra (861-870): four caliphs murdered by Turkish soldiers',
    ],
    'civil_wars': 6,
    'puppet_note': 'Late Abbasid caliphs (after ~940s) were largely puppets of Buyid and Seljuk warlords.',
}

VALIDATION["Mamluk Sultanate"] = {
    'total': 27, 'violent': 18,
    'scope_rationale': 'Full Mamluk period (1250-1517). System inherently based on military slave-soldiers seizing power.',
    'events': [
        'Chronic factional violence among Mamluk amirs',
        'Assassination of Qutuz (1260) by Baybars',
        'Multiple sultans deposed within months of accession',
        'Near-constant palace coups, especially in Burji period (1382-1517)',
    ],
    'civil_wars': 8,
    'puppet_note': 'Multiple child sultans installed as figureheads by powerful amirs.',
}

VALIDATION["Persia/Iran"] = {
    'total': 22, 'violent': 9,
    'scope_rationale': 'Safavid dynasty onward (1501-1979). Pre-Safavid dynasties excluded as they represent '
                       'fundamentally different political entities with fragmentary succession records.',
    'events': [
        'Afghan invasion (1722): collapse of Safavid dynasty',
        'Nader Shah assassinated (1747)',
        'Qajar civil wars and palace coups',
        'Constitutional Revolution (1905-1911)',
        'Iranian Revolution (1979): Mohammad Reza Shah deposed',
    ],
    'civil_wars': 4,
    'puppet_note': 'Late Qajar shahs had limited power under constitutional and foreign constraints.',
}

# --- ASIA ---
VALIDATION["Japan (Emperors)"] = {
    'total': 86, 'violent': 3,
    'scope_rationale': 'From Emperor Kinmei (539 CE) to Emperor Akihito (abdicated 2019). Excludes legendary/mythological '
                       'emperors (Jimmu through Ingyo) whose historicity and reign dates are uncertain.',
    'events': [
        'Jinshin War (672): succession dispute between Prince Oama and Prince Otomo',
        'Hogen Rebellion (1156) and Heiji Rebellion (1159): affected imperial succession indirectly',
        'Kenmu Restoration (1333): brief imperial rule before Ashikaga takeover',
    ],
    'civil_wars': 3,
    'puppet_note': 'MAJOR: From Fujiwara regency (~858) through Edo period (~1868), most emperors were ceremonial '
                   'figureheads. Real power held by regents (sessho/kampaku), cloistered emperors (insei), '
                   'shoguns (Kamakura, Muromachi, Tokugawa). This substantially affects interpretation of k value: '
                   'the high k (1.648) may reflect the stability of figurehead succession rather than true political stability.',
}

VALIDATION["China (Tang)"] = {
    'total': 22, 'violent': 7,
    'scope_rationale': 'Full Tang dynasty (618-907 CE).',
    'events': [
        'An Lushan Rebellion (755-763): nearly destroyed the dynasty',
        'Xuanzong forced to flee and abdicate',
        'Eunuch domination in late Tang: multiple emperors installed/deposed by eunuchs',
        'Huang Chao Rebellion (874-884)',
    ],
    'civil_wars': 3,
    'puppet_note': 'Late Tang emperors (after 820) were largely puppets of eunuch factions.',
}

VALIDATION["China (Ming)"] = {
    'total': 17, 'violent': 2,
    'scope_rationale': 'Full Ming dynasty (1368-1644).',
    'events': [
        'Jingnan Campaign (1399-1402): Yongle Emperor usurped throne from nephew',
        'Fall to Manchu invasion (1644): Chongzhen Emperor committed suicide',
    ],
    'civil_wars': 1,
    'puppet_note': 'Several emperors dominated by eunuchs (e.g., Tianqi Emperor under Wei Zhongxian).',
}

VALIDATION["China (Qing)"] = {
    'total': 11, 'violent': 1,
    'scope_rationale': 'Full Qing dynasty (1644-1912). Small N reflects the dynasty\'s relatively few rulers.',
    'events': [
        'Xinhai Revolution (1911-1912): Puyi forced to abdicate',
        'Taiping Rebellion (1850-1864): massive civil war but succession continued',
        'Boxer Rebellion (1899-1901)',
    ],
    'civil_wars': 2,
    'puppet_note': 'Empress Dowager Cixi effectively ruled behind child emperors (Tongzhi, Guangxu). '
                   'Puyi acceded at age 2.',
}

VALIDATION["Korea (Joseon)"] = {
    'total': 28, 'violent': 4,
    'scope_rationale': 'Full Joseon dynasty (1392-1897) plus Korean Empire (1897-1910).',
    'events': [
        'First Strife of Princes (1398): Yi Bang-won killed rivals',
        'Second Strife of Princes (1400)',
        'Coup of 1453: Sejo seized throne from nephew Danjong',
        'Japanese annexation (1910): forced end of monarchy',
    ],
    'civil_wars': 2,
    'puppet_note': 'Late Joseon kings increasingly constrained by factional politics (sarim/bungdang).',
}

VALIDATION["Korea (Goryeo)"] = {
    'total': 33, 'violent': 8,
    'scope_rationale': 'Full Goryeo dynasty (918-1392).',
    'events': [
        'Mongol invasions (1231-1270): kings became Mongol vassals',
        'Military coup by Choe family (1170-1270): kings reduced to puppets',
        'Multiple king depositions by powerful military families',
    ],
    'civil_wars': 3,
    'puppet_note': 'Goryeo kings were puppets of Choe military dictatorship (1196-1258) and later Mongol overlords.',
}

VALIDATION["Mughal Empire"] = {
    'total': 15, 'violent': 7,
    'scope_rationale': 'Full Mughal period (1526-1857). Small N reflects the empire\'s relatively brief span.',
    'events': [
        'War of Succession (1658): Aurangzeb imprisoned father Shah Jahan, killed brothers',
        'Rapid succession after Aurangzeb (1707): 7 emperors in 12 years',
        'Nadir Shah\'s invasion (1739): sack of Delhi',
        'British deposition of Bahadur Shah II (1858)',
    ],
    'civil_wars': 5,
    'puppet_note': 'Post-Aurangzeb emperors (after 1707) were increasingly puppets of powerful nobles and later the British.',
}

VALIDATION["Khmer Empire"] = {
    'total': 20, 'violent': 8,
    'scope_rationale': 'Angkor period (802-1431). Post-Angkor records too fragmentary for reliable analysis.',
    'events': [
        'Frequent usurpations and regicides throughout Angkor period',
        'Cham invasion (1177): sack of Angkor',
        'Multiple succession disputes among royal princes',
    ],
    'civil_wars': 4,
    'puppet_note': None,
}

VALIDATION["Thailand (Chakri)"] = {
    'total': 10, 'violent': 1,
    'scope_rationale': 'Chakri dynasty only (1782-present). Previous dynasties (Ayutthaya etc.) analysed separately would yield too few reigns per dynasty.',
    'events': [
        'Revolution of 1932: transition to constitutional monarchy (king retained)',
        'Boworadet Rebellion (1933): failed royalist counter-coup',
    ],
    'civil_wars': 0,
    'puppet_note': 'Post-1932 kings are constitutional monarchs with limited political power.',
}

# --- AFRICA ---
VALIDATION["Ethiopia"] = {
    'total': 27, 'violent': 10,
    'scope_rationale': 'Solomonic dynasty restoration (1270) to end of monarchy (1974). Earlier Zagwe dynasty excluded '
                       'due to unreliable chronology.',
    'events': [
        'Era of the Princes (Zemene Mesafint, 1769-1855): emperors as puppets of regional warlords',
        'Italian invasion (1936): Haile Selassie exiled',
        'Derg revolution (1974): Haile Selassie deposed and killed',
        'Multiple regional rebellions and succession wars',
    ],
    'civil_wars': 5,
    'puppet_note': 'During Zemene Mesafint (1769-1855), emperors were figureheads controlled by regional ras.',
}

VALIDATION["Egypt (New Kingdom)"] = {
    'total': 31, 'violent': 6,
    'scope_rationale': 'New Kingdom only (1550-1077 BCE). Other Egyptian periods (Old Kingdom, Middle Kingdom, etc.) '
                       'analysed separately would yield too few reigns per period with reliable chronology. '
                       'New Kingdom has the best-documented succession records.',
    'events': [
        'Harem conspiracy against Ramesses III (1155 BCE)',
        'Hatshepsut\'s seizure of power from Thutmose III',
        'Akhenaten\'s religious revolution and subsequent reversal',
        'End of 18th dynasty succession crisis',
    ],
    'civil_wars': 2,
    'puppet_note': 'Some pharaohs may have been dominated by powerful priests of Amun in late New Kingdom.',
}

# --- EUROPE (continued) ---
VALIDATION["Byzantine Empire"] = {
    'total': 71, 'violent': 33,
    'scope_rationale': 'From Arcadius (395 CE, east-west division) to Fall of Constantinople (1453). '
                       'Full Eastern Roman/Byzantine period.',
    'events': [
        'Nika Riots (532): nearly overthrew Justinian',
        'Twenty Years\' Anarchy (695-717): 7 emperors in 22 years',
        'Iconoclasm disputes causing political instability (726-843)',
        'Fourth Crusade (1204): Latin conquest, empire fragmented',
        'Chronic palace coups and blinding/mutilation of deposed emperors',
    ],
    'civil_wars': 12,
    'puppet_note': 'Multiple child emperors under regency or co-emperor arrangements.',
}

VALIDATION["Papacy (post-1000)"] = {
    'total': 121, 'violent': 4,
    'scope_rationale': 'Post-1000 CE only. Pre-1000 papacy excluded for three reasons: (1) the College of Cardinals '
                       'was established in 1059 (In Nomine Domini), creating the modern electoral system - prior papal '
                       'selection was dominated by Roman aristocratic factions and imperial appointment; (2) pre-1000 '
                       'records are less reliable with disputed dates for many early popes; (3) frequent anti-popes '
                       '(over 30 before 1000 CE) make it difficult to define "legitimate" reign durations.',
    'events': [
        'Western Schism (1378-1417): multiple rival popes',
        'Avignon Papacy (1309-1377): popes under French influence',
        'Borgia papacy and Renaissance political intrigue',
        'Conclaves occasionally involved political pressure but rarely violence post-1000',
    ],
    'civil_wars': 0,
    'puppet_note': 'Some popes elected as compromise candidates with limited personal authority.',
}

# --- AMERICAS ---
VALIDATION["USA (Presidents)"] = {
    'total': 42, 'violent': 4,
    'scope_rationale': 'All presidents from Washington (1789) to present. Complete record.',
    'events': [
        'Assassination of Lincoln (1865), Garfield (1881), McKinley (1901), Kennedy (1963)',
        'American Civil War (1861-1865): did not disrupt presidential succession',
        'Contested election of 1876 (Hayes-Tilden)',
        'January 6 Capitol attack (2021): attempted disruption of transition',
    ],
    'civil_wars': 1,
    'puppet_note': None,
}

# =============================================================================
# CALCULATIONS AND VISUALIZATION
# =============================================================================

# k values from main analysis
K_VALUES = {
    "Roman Empire": 0.880, "England/Britain": 1.308, "France": 1.235,
    "Holy Roman Empire": 1.171, "Denmark": 1.788, "Sweden": 1.897,
    "Scotland": 1.937, "Spain": 1.791, "Portugal": 1.285, "Poland": 1.552,
    "Russia": 1.015, "Ottoman Empire": 1.240, "Islamic Caliphate": 1.004,
    "Mamluk Sultanate": 0.851, "Persia/Iran": 1.079, "Japan (Emperors)": 1.648,
    "China (Tang)": 1.140, "China (Ming)": 1.338, "China (Qing)": 1.140,
    "Korea (Joseon)": 1.262, "Korea (Goryeo)": 1.324, "Mughal Empire": 0.936,
    "Khmer Empire": 1.381, "Thailand (Chakri)": 1.492, "Ethiopia": 1.150,
    "Egypt (New Kingdom)": 1.132, "Byzantine Empire": 1.113,
    "Papacy (post-1000)": 1.163, "USA (Presidents)": 2.721,
}

REGION_CATEGORIES = {
    "Roman Empire": "Europe", "England/Britain": "Europe", "France": "Europe",
    "Holy Roman Empire": "Europe", "Denmark": "Europe", "Sweden": "Europe",
    "Scotland": "Europe", "Spain": "Europe", "Portugal": "Europe", "Poland": "Europe",
    "Russia": "Europe", "Ottoman Empire": "Middle East", "Islamic Caliphate": "Middle East",
    "Mamluk Sultanate": "Middle East", "Persia/Iran": "Middle East",
    "Japan (Emperors)": "Asia", "China (Tang)": "Asia", "China (Ming)": "Asia",
    "China (Qing)": "Asia", "Korea (Joseon)": "Asia", "Korea (Goryeo)": "Asia",
    "Mughal Empire": "Asia", "Khmer Empire": "Asia", "Thailand (Chakri)": "Asia",
    "Ethiopia": "Africa", "Egypt (New Kingdom)": "Africa/Middle East",
    "Byzantine Empire": "Europe", "Papacy (post-1000)": "Europe",
    "USA (Presidents)": "Americas",
}

# Calculate violent succession rates
names = []
k_vals = []
violent_rates = []
civil_war_counts = []
categories = []

print("=" * 90)
print("HISTORICAL VALIDATION: Violent Succession Rates vs Weibull k")
print("=" * 90)
print(f"{'Polity':<30} {'k':>6} {'Total':>6} {'Violent':>8} {'Rate':>8} {'Civil Wars':>11}")
print("-" * 90)

for name in sorted(VALIDATION.keys(), key=lambda x: K_VALUES.get(x, 0)):
    v = VALIDATION[name]
    k = K_VALUES.get(name, None)
    if k is None:
        continue
    rate = v['violent'] / v['total'] if v['total'] > 0 else 0
    names.append(name)
    k_vals.append(k)
    violent_rates.append(rate)
    civil_war_counts.append(v['civil_wars'])
    categories.append(REGION_CATEGORIES.get(name, 'Other'))
    print(f"{name:<30} {k:>6.3f} {v['total']:>6} {v['violent']:>8} {rate:>8.1%} {v['civil_wars']:>11}")

k_arr = np.array(k_vals)
vr_arr = np.array(violent_rates)

# Correlation
r_pearson, p_pearson = stats.pearsonr(k_arr, vr_arr)
r_spearman, p_spearman = stats.spearmanr(k_arr, vr_arr)

print(f"\nPearson correlation (k vs violent rate):  r = {r_pearson:.3f}, p = {p_pearson:.4f}")
print(f"Spearman correlation (k vs violent rate): rho = {r_spearman:.3f}, p = {p_spearman:.4f}")

# Civil war correlation
cw_arr = np.array(civil_war_counts)
r_cw, p_cw = stats.spearmanr(k_arr, cw_arr)
print(f"Spearman correlation (k vs civil wars):   rho = {r_cw:.3f}, p = {p_cw:.4f}")

# =============================================================================
# FIGURE 6: k vs Violent Succession Rate
# =============================================================================

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Panel A: k vs violent succession rate (scatter)
ax = axes[0]
cat_colors = {'Europe': '#4477AA', 'Asia': '#EE6677', 'Middle East': '#CCBB44',
              'Africa': '#228833', 'Africa/Middle East': '#66CCEE', 'Americas': '#AA3377'}

for name, k, vr, cat in zip(names, k_vals, violent_rates, categories):
    color = cat_colors.get(cat, 'gray')
    ax.scatter(k, vr, c=color, s=80, alpha=0.8, edgecolors='black', linewidth=0.5, zorder=5)
    # Label select points
    if k < 1.0 or k > 1.7 or vr > 0.55 or name in ['Japan (Emperors)', 'USA (Presidents)']:
        offset = (5, 5)
        if name == 'USA (Presidents)':
            offset = (-60, 10)
        elif name == 'Japan (Emperors)':
            offset = (5, -12)
        elif name == 'Mamluk Sultanate':
            offset = (5, -12)
        ax.annotate(name, (k, vr), fontsize=7, xytext=offset,
                   textcoords='offset points', alpha=0.8)

# Regression line
slope, intercept, r_val, p_val, se = stats.linregress(k_arr, vr_arr)
x_line = np.linspace(0.8, 2.8, 100)
y_line = slope * x_line + intercept
ax.plot(x_line, y_line, 'k--', alpha=0.5, linewidth=1)
ax.text(0.05, 0.95, f'r = {r_pearson:.3f}\np = {p_pearson:.4f}',
       transform=ax.transAxes, fontsize=9, verticalalignment='top',
       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.set_xlabel('Weibull Shape Parameter k', fontsize=11)
ax.set_ylabel('Violent Succession Rate', fontsize=11)
ax.set_title('(A) k vs Violent Succession Rate', fontsize=12, fontweight='bold')
ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.3)
ax.axvline(x=1.0, color='gray', linestyle=':', alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, label=l, edgecolor='black', linewidth=0.5)
                   for l, c in cat_colors.items()]
ax.legend(handles=legend_elements, fontsize=7, loc='upper right')

# Panel B: k vs civil war count
ax2 = axes[1]
for name, k, cw, cat in zip(names, k_vals, civil_war_counts, categories):
    color = cat_colors.get(cat, 'gray')
    ax2.scatter(k, cw, c=color, s=80, alpha=0.8, edgecolors='black', linewidth=0.5, zorder=5)
    if cw >= 5 or k < 1.0 or k > 2.0:
        offset = (5, 5)
        if name == 'USA (Presidents)':
            offset = (-60, 5)
        ax2.annotate(name, (k, cw), fontsize=7, xytext=offset,
                    textcoords='offset points', alpha=0.8)

ax2.text(0.05, 0.95, f'rho = {r_cw:.3f}\np = {p_cw:.4f}',
        transform=ax2.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax2.set_xlabel('Weibull Shape Parameter k', fontsize=11)
ax2.set_ylabel('Number of Civil Wars / Major Conflicts', fontsize=11)
ax2.set_title('(B) k vs Civil Wars', fontsize=12, fontweight='bold')
ax2.axvline(x=1.0, color='gray', linestyle=':', alpha=0.3)

# Panel C: Horizontal bar chart of violent rate, colored by k
ax3 = axes[2]
sorted_idx = np.argsort(violent_rates)[::-1]
sorted_names = [names[i] for i in sorted_idx]
sorted_vr = [violent_rates[i] for i in sorted_idx]
sorted_k = [k_vals[i] for i in sorted_idx]

# Color by k value
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
norm = Normalize(vmin=0.85, vmax=2.8)
cmap = plt.cm.RdYlGn

bar_colors = [cmap(norm(k)) for k in sorted_k]
bars = ax3.barh(range(len(sorted_names)), sorted_vr, color=bar_colors, edgecolor='black', linewidth=0.3)
ax3.set_yticks(range(len(sorted_names)))
ax3.set_yticklabels(sorted_names, fontsize=7)
ax3.set_xlabel('Violent Succession Rate', fontsize=11)
ax3.set_title('(C) Violent Succession Rate\n(bar color = k value)', fontsize=12, fontweight='bold')
ax3.invert_yaxis()

# Add k values as text
for i, (vr, k) in enumerate(zip(sorted_vr, sorted_k)):
    ax3.text(vr + 0.01, i, f'k={k:.2f}', va='center', fontsize=7, alpha=0.8)

# Colorbar
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax3, shrink=0.8, pad=0.02)
cbar.set_label('k value', fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/monarch_historical_validation.png', dpi=150, bbox_inches='tight')
print("\nSaved: monarch_historical_validation.png")

# =============================================================================
# Print scope rationale summary
# =============================================================================
print("\n" + "=" * 90)
print("DATA SCOPE RATIONALE BY POLITY")
print("=" * 90)
for name in sorted(VALIDATION.keys()):
    v = VALIDATION[name]
    print(f"\n{name}:")
    print(f"  Scope: {v['scope_rationale']}")
    if v.get('puppet_note'):
        print(f"  Puppet/figurehead note: {v['puppet_note']}")

# =============================================================================
# Print puppet king summary
# =============================================================================
print("\n" + "=" * 90)
print("PUPPET/FIGUREHEAD RULERS - LIMITATION SUMMARY")
print("=" * 90)
puppet_polities = [(n, v) for n, v in VALIDATION.items() if v.get('puppet_note')]
for name, v in sorted(puppet_polities, key=lambda x: x[0]):
    print(f"\n{name} (k={K_VALUES.get(name, '?')}):")
    print(f"  {v['puppet_note']}")

plt.close('all')
print("\nDone.")
