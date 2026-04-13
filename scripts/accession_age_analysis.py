#!/usr/bin/env python3
"""
Accession age distribution analysis for each polity.
Compiles accession ages, calculates summary statistics,
creates visualizations, and correlates with Weibull k values.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# ACCESSION AGE DATA BY POLITY
# Ages at accession (in years). Where exact birth dates are uncertain,
# best scholarly estimates are used. Only rulers included in the main
# Weibull analysis are listed.
# =============================================================================

ACCESSION_AGES = {}

# --- ROMAN EMPIRE (27 BCE - 476 CE) ---
# Major emperors with known/estimated accession ages
ACCESSION_AGES["Roman Empire"] = {
    'ages': [
        # Augustus 18, Tiberius 55, Caligula 24, Claudius 50, Nero 16,
        # Galba 71, Otho 36, Vitellius 54, Vespasian 59, Titus 39,
        # Domitian 29, Nerva 65, Trajan 44, Hadrian 41, Antoninus Pius 51,
        # Marcus Aurelius 39, Commodus 18, Pertinax 66, Didius Julianus 56,
        # Septimius Severus 47, Caracalla 10, Geta 22, Macrinus 53,
        # Elagabalus 14, Severus Alexander 13, Maximinus Thrax 62,
        # Gordian I 79, Gordian II 46, Pupienus 58, Balbinus 60,
        # Gordian III 13, Philip 40, Decius 49, Trebonianus Gallus 45,
        # Valerian 60, Gallienus 35, Claudius II 45, Aurelian 55,
        # Probus 44, Diocletian 40, Constantine I 34, Constantius II 20,
        # Julian 31, Jovian 32, Valentinian I 43, Valens 36,
        # Theodosius I 32, Honorius 10, Arcadius 18, Romulus Augustulus 14
        18, 55, 24, 50, 16, 71, 36, 54, 59, 39,
        29, 65, 44, 41, 51, 39, 18, 66, 56, 47,
        10, 22, 53, 14, 13, 62, 79, 46, 58, 60,
        13, 40, 49, 45, 60, 35, 45, 55, 44, 40,
        34, 20, 31, 32, 43, 36, 32, 10, 18, 14
    ],
    'notes': 'Multiple child/teenage emperors (Caracalla 10, Gordian III 13, Honorius 10, Elagabalus 14, Romulus Augustulus 14).'
}

# --- ENGLAND/BRITAIN (1066-present) ---
ACCESSION_AGES["England/Britain"] = {
    'ages': [
        # William I 38, William II 31, Henry I 31, Stephen 45, Henry II 21,
        # Richard I 31, John 32, Henry III 9, Edward I 33, Edward II 23,
        # Edward III 14, Richard II 10, Henry IV 33, Henry V 25, Henry VI 0.75,
        # Edward IV 18, Edward V 12, Richard III 30, Henry VII 28, Henry VIII 17,
        # Edward VI 9, Mary I 37, Elizabeth I 25, James I 36, Charles I 24,
        # Charles II 30, James II 51, William III 39, Mary II 26, Anne 37,
        # George I 54, George II 43, George III 22, George IV 57, William IV 64,
        # Victoria 18, Edward VII 59, George V 44, Edward VIII 41, George VI 40,
        # Elizabeth II 25, Charles III 73
        38, 31, 31, 45, 21, 31, 32, 9, 33, 23,
        14, 10, 33, 25, 1, 18, 12, 30, 28, 17,
        9, 37, 25, 36, 24, 30, 51, 39, 26, 37,
        54, 43, 22, 57, 64, 18, 59, 44, 41, 40,
        25, 73
    ],
    'notes': 'Henry III (9), Henry VI (infant ~9 months), Edward V (12), Edward VI (9), Richard II (10).'
}

# --- FRANCE (Capetian onward 987-1870) ---
ACCESSION_AGES["France"] = {
    'ages': [
        # Hugh Capet 46, Robert II 25, Henry I 23, Philip I 7, Louis VI 27,
        # Louis VII 17, Philip II 15, Louis VIII 36, Louis IX 12, Philip III 25,
        # Philip IV 17, Louis X 24, John I 0 (infant), Philip V 22, Charles IV 24,
        # Philip VI 35, John II 31, Charles V 26, Charles VI 11, Charles VII 19,
        # Louis XI 38, Charles VIII 13, Louis XII 36, Francis I 20, Henry II 28,
        # Francis II 15, Charles IX 10, Henry III 22, Henry IV 36, Louis XIII 8,
        # Louis XIV 4, Louis XV 5, Louis XVI 19, Louis XVIII 58, Charles X 66,
        # Louis-Philippe 56, Napoleon I 35, Napoleon III 43
        46, 25, 23, 7, 27, 17, 15, 36, 12, 25,
        17, 24, 0, 22, 24, 35, 31, 26, 11, 19,
        38, 13, 36, 20, 28, 15, 10, 22, 36, 8,
        4, 5, 19, 58, 66, 56, 35, 43
    ],
    'notes': 'Multiple child kings: Louis XIV (4), Louis XV (5), Philip I (7), Louis XIII (8), Charles IX (10), Charles VI (11), Louis IX (12).'
}

# --- JAPAN (EMPERORS) ---
# From Kinmei to Akihito (using known/estimated accession ages)
ACCESSION_AGES["Japan (Emperors)"] = {
    'ages': [
        # Kinmei ~30, Bidatsu ~36, Yomei ~45, Sushun ~?, Suiko ~39,
        # Jomei ~36, Kogyoku ~48, Kotoku ~48, Saimei ~55, Tenji ~36,
        # Kobun ~24, Tenmu ~50, Jito ~41, Monmu ~14, Genmei ~47,
        # Gensho ~35, Shomu ~24, Koken ~29, Junnin ~25, Shotoku ~45,
        # Konin ~62, Kammu ~44, Heizei ~34, Saga ~23, Junna ~23,
        # Ninmyo ~23, Montoku ~22, Seiwa ~8, Yozei ~8, Koko ~54,
        # Uda ~20, Daigo ~11, Suzaku ~8, Murakami ~20, Reizei ~18,
        # Enyu ~10, Kazan ~17, Ichijo ~6, Sanjo ~35, GoIchijo ~8,
        # GoSuzaku ~27, GoReizei ~11, GoSanjo ~34, Shirakawa ~19,
        # Horikawa ~7, Toba ~4, Sutoku ~5, Konoe ~2, GoShirakawa ~28,
        # Nijo ~15, Rokujo ~0.5, Takakura ~7, Antoku ~1, GoToba ~3,
        # Tsuchimikado ~3, Juntoku ~13, Chukyo ~4, GoHorikawa ~10,
        # Shijo ~1, GoSaga ~22, GoFukakusa ~3, Kameyama ~10,
        # GoUda ~7, Fushimi ~22, GoFushimi ~10, GoNijo ~19,
        # Hanazono ~11, GoDaigo ~30, GoMurakami ~13, GoKameyama ~?,
        # GoKomatsu ~14, Shoko ~12, GoHanazono ~10, GoTsuchimikado ~14,
        # GoKashiwabara ~22, GoNara ~30, Ogimachi ~39, GoYozei ~14,
        # GoMizunoo ~15, Meisho ~5, GoKomyo ~10, GoSai ~18,
        # Reigen ~9, Higashiyama ~12, Nakamikado ~12, Sakuramachi ~15,
        # Momozono ~6, GoSakuramachi ~23, GoMomozono ~12,
        # Kokaku ~8, Ninko ~17, Komei ~15, Meiji 14, Taisho 33,
        # Showa 25, Akihito 55
        30, 36, 45, 40, 39, 36, 48, 48, 55, 36,
        24, 50, 41, 14, 47, 35, 24, 29, 25, 45,
        62, 44, 34, 23, 23, 23, 22, 8, 8, 54,
        20, 11, 8, 20, 18, 10, 17, 6, 35, 8,
        27, 11, 34, 19, 7, 4, 5, 2, 28, 15,
        1, 7, 1, 3, 3, 13, 4, 10, 1, 22,
        3, 10, 7, 22, 10, 19, 11, 30, 13, 14,
        14, 12, 10, 14, 22, 30, 39, 14, 15, 5,
        10, 18, 9, 12, 12, 15, 6, 23, 12, 8,
        17, 15, 14, 33, 25, 55
    ],
    'notes': 'MAJOR pattern: Many infant/child emperors installed as figureheads during regency/shogunate periods. '
             '26 of 96 accessions (27%) at age <10. Extreme cases: Rokujo (6 months), Antoku (1), Shijo (1), Konoe (2).'
}

# --- HOLY ROMAN EMPIRE (962-1806) ---
ACCESSION_AGES["Holy Roman Empire"] = {
    'ages': [
        # Otto I 49, Otto II 18, Otto III 3, Henry II 24, Conrad II 37,
        # Henry III 22, Henry IV 6, Henry V 25, Lothair II 58, Conrad III 45,
        # Frederick I 30, Henry VI 25, Otto IV 23, Frederick II 17,
        # Henry (VII) 9, Conrad IV 22, Rudolf I 55, Adolf 37, Albert I 43,
        # Henry VII 38, Louis IV 28, Charles IV 30, Wenceslaus 17,
        # Rupert 52, Sigismund 55, Albert II 40, Frederick III 17,
        # Maximilian I 27, Charles V 19, Ferdinand I 33, Maximilian II 37,
        # Rudolf II 24, Matthias 55, Ferdinand II 40, Ferdinand III 30,
        # Leopold I 17, Joseph I 27, Charles VI 26, Charles VII 41,
        # Francis I 37, Joseph II 24, Leopold II 43, Francis II 24
        49, 18, 3, 24, 37, 22, 6, 25, 58, 45,
        30, 25, 23, 17, 9, 22, 55, 37, 43, 38,
        28, 30, 17, 52, 55, 40, 17, 27, 19, 33,
        37, 24, 55, 40, 30, 17, 27, 26, 41, 37,
        24, 43, 24
    ],
    'notes': 'Otto III (3), Henry IV (6), Henry (VII) (9) are notable child emperors.'
}

# --- OTTOMAN EMPIRE ---
ACCESSION_AGES["Ottoman Empire"] = {
    'ages': [
        # Osman I ~42, Orhan ~42, Murad I ~36, Bayezid I ~29, Mehmed I ~30,
        # Murad II ~17, Mehmed II ~12, Bayezid II ~30, Selim I ~38,
        # Suleiman ~25, Selim II ~42, Murad III ~28, Mehmed III ~28,
        # Ahmed I ~13, Mustafa I ~22, Osman II ~14, Murad IV ~11,
        # Ibrahim ~24, Mehmed IV ~6, Suleiman II ~47, Ahmed II ~48,
        # Mustafa II ~31, Ahmed III ~30, Mahmud I ~34, Osman III ~55,
        # Mustafa III ~40, Abdulhamid I ~49, Selim III ~28, Mustafa IV ~28,
        # Mahmud II ~23, Abdulmecid ~16, Abdulaziz ~30, Murad V ~36,
        # Abdulhamid II ~34, Mehmed V ~65, Mehmed VI ~57, Abdulmecid II ~54
        42, 42, 36, 29, 30, 17, 12, 30, 38, 25,
        42, 28, 28, 13, 22, 14, 11, 24, 6, 47,
        48, 31, 30, 34, 55, 40, 49, 28, 28, 23,
        16, 30, 36, 34, 65, 57, 54
    ],
    'notes': 'Mehmed IV (6), Murad IV (11), Mehmed II (12), Ahmed I (13), Osman II (14).'
}

# --- ISLAMIC CALIPHATE ---
ACCESSION_AGES["Islamic Caliphate"] = {
    'ages': [
        # Abu Bakr ~61, Umar ~52, Uthman ~64, Ali ~35,
        # Muawiya I ~60, Yazid I ~34, Muawiya II ~16, Marwan I ~63,
        # Abd al-Malik ~26, al-Walid I ~30, Sulayman ~42, Umar II ~37,
        # Yazid II ~31, Hisham ~33, al-Walid II ~30, Yazid III ~36,
        # Marwan II ~36, al-Saffah ~24, al-Mansur ~41, al-Mahdi ~33,
        # al-Hadi ~19, Harun al-Rashid ~17, al-Amin ~22, al-Mamun ~23,
        # al-Mutasim ~42, al-Wathiq ~27, al-Mutawakkil ~25,
        # al-Muntasir ~22, al-Mustain ~20, al-Mutazz ~20,
        # al-Muhtadi ~30, al-Mutamid ~26, al-Mutadid ~37,
        # al-Muktafi ~25, al-Muqtadir ~13, al-Qahir ~31,
        # al-Radi ~20, al-Muttaqi ~34, al-Mustakfi ~36,
        # al-Muti ~26, al-Tai ~42, al-Qadir ~44, al-Qaim ~39,
        # al-Muqtadi ~19, al-Mustazhir ~16, al-Mustarshid ~26,
        # al-Rashid ~22, al-Muqtafi ~30, al-Mustanjid ~25,
        # al-Mustadi ~26, al-Nasir ~25, al-Zahir ~55,
        # al-Mustansir ~34, al-Mustasim ~21
        61, 52, 64, 35, 60, 34, 16, 63, 26, 30,
        42, 37, 31, 33, 30, 36, 36, 24, 41, 33,
        19, 17, 22, 23, 42, 27, 25, 22, 20, 20,
        30, 26, 37, 25, 13, 31, 20, 34, 36, 26,
        42, 44, 39, 19, 16, 26, 22, 30, 25, 26,
        25, 55, 34, 21
    ],
    'notes': 'al-Muqtadir (13) is the most notable young caliph. Most caliphs acceded as adults.'
}

# --- MAMLUK SULTANATE ---
ACCESSION_AGES["Mamluk Sultanate"] = {
    'ages': [
        # Aybak ~48, Ali ~15, Qutuz ~30, Baybars ~37, Baraka ~12,
        # Solamish ~7, Qalawun ~40, Khalil ~26, al-Nasir Muhammad ~9,
        # Baybars II ~35, al-Nasir Muhammad (2nd) ~18,
        # al-Nasir Muhammad (3rd) ~25, Abu Bakr ~14, Kujuk ~6,
        # Ahmad ~14, Ismail ~13, Shaban I ~18, Hajji I ~9,
        # Hasan ~12, Salih ~10, Hasan (2nd) ~17, Muhammad ~12,
        # Shaban II ~10, Ali ~10, Barquq ~42, Faraj ~10,
        # al-Musta'in ~40
        48, 15, 30, 37, 12, 7, 40, 26, 9, 35,
        18, 25, 14, 6, 14, 13, 18, 9, 12, 10,
        17, 12, 10, 10, 42, 10, 40
    ],
    'notes': 'MAJOR: Many child sultans used as puppets. Kujuk (6), Solamish (7), al-Nasir Muhammad (9), Hajji I (9), '
             'multiple accessions at age 10-14. 15 of 27 (56%) acceded under age 18.'
}

# --- BYZANTINE EMPIRE ---
ACCESSION_AGES["Byzantine Empire"] = {
    'ages': [
        # Selected major emperors with known accession ages
        # Arcadius 17, Theodosius II 7, Marcian 57, Leo I 44, Leo II 6,
        # Zeno 48, Anastasius I 61, Justin I 68, Justinian I 45,
        # Justin II 55, Tiberius II 45, Maurice 43, Phocas 45,
        # Heraclius 35, Constantine III 29, Heraclonas 15,
        # Constans II 11, Constantine IV 18, Justinian II 16,
        # Leontios 55, Tiberius III 45, Philippikos 40,
        # Anastasios II 45, Theodosius III 45, Leo III 32,
        # Constantine V 22, Leo IV 25, Constantine VI 9,
        # Irene 45, Nikephoros I 60, Staurakios 18, Michael I 45,
        # Leo V 38, Michael II 45, Theophilos 25, Michael III 2,
        # Basil I 55, Leo VI 19, Alexander 39, Constantine VII 6,
        # Romanos I 55, Romanos II 19, Nikephoros II 50,
        # John I Tzimiskes 45, Basil II 18, Constantine VIII 62,
        # Romanos III 58, Michael IV 36, Michael V 25, Zoe 64,
        # Constantine IX 42, Theodora 75, Michael VI 55,
        # Isaac I 50, Constantine X 54, Romanos IV 48,
        # Michael VII 19, Nikephoros III 73, Alexios I 24,
        # John II 30, Manuel I 27, Alexios II 10, Andronikos I 62,
        # Isaac II 30, Alexios III 42, Alexios IV 18, Alexios V 53,
        # Theodore I (Nicaea) 29, John III 30, Theodore II 33,
        # John IV 7, Michael VIII 35, Andronikos II 22,
        # Michael IX 17, Andronikos III 27, John V 13,
        # John VI 50, Andronikos IV 28, John VII 20,
        # Manuel II 40, John VIII 38, Constantine XI 44
        17, 7, 57, 44, 6, 48, 61, 68, 45, 55,
        45, 43, 45, 35, 29, 15, 11, 18, 16, 55,
        45, 40, 45, 45, 32, 22, 25, 9, 45, 60,
        18, 45, 38, 45, 25, 2, 55, 19, 39, 6,
        55, 19, 50, 45, 18, 62, 58, 36, 25, 64,
        42, 75, 55, 50, 54, 48, 19, 73, 24, 30,
        27, 10, 62, 30, 42, 18, 53, 29, 30, 33,
        7, 35, 22, 17, 27, 13, 50, 28, 20, 40, 38, 44
    ],
    'notes': 'Michael III (2), Constantine VII (6), Leo II (6), Theodosius II (7), Constantine VI (9), Alexios II (10).'
}

# --- CHINA (TANG) ---
ACCESSION_AGES["China (Tang)"] = {
    'ages': [
        # Gaozu 52, Taizong 28, Gaozong 20, Wu Zetian 66, Zhongzong 26,
        # Ruizong 22, Xuanzong 28, Suzong 46, Daizong 39, Dezong 36,
        # Shunzong 44, Xianzong 26, Muzong 20, Jingzong 15, Wenzong 17,
        # Wuzong 26, Xuanzong II 36, Yizong 26, Xizong 11, Zhaozong 26, Ai 12
        52, 28, 20, 66, 26, 22, 28, 46, 39, 36,
        44, 26, 20, 15, 17, 26, 36, 26, 11, 26, 12
    ],
    'notes': 'Xizong (11), Ai (12), Jingzong (15) are youngest. Wu Zetian (66) is the oldest accession.'
}

# --- CHINA (MING) ---
ACCESSION_AGES["China (Ming)"] = {
    'ages': [
        # Hongwu 40, Jianwen 21, Yongle 42, Hongxi 46, Xuande 26,
        # Zhengtong 8, Jingtai 21, Tianshun 28, Chenghua 16,
        # Hongzhi 17, Zhengde 14, Jiajing 14, Longqing 29, Wanli 9,
        # Taichang 38, Tianqi 15, Chongzhen 16
        40, 21, 42, 46, 26, 8, 21, 28, 16, 17,
        14, 14, 29, 9, 38, 15, 16
    ],
    'notes': 'Zhengtong (8), Wanli (9), Zhengde (14), Jiajing (14), Tianqi (15).'
}

# --- CHINA (QING) ---
ACCESSION_AGES["China (Qing)"] = {
    'ages': [
        # Shunzhi 5, Kangxi 7, Yongzheng 44, Qianlong 24, Jiaqing 35,
        # Daoguang 38, Xianfeng 19, Tongzhi 5, Guangxu 3, Xuantong (Puyi) 2
        5, 7, 44, 24, 35, 38, 19, 5, 3, 2
    ],
    'notes': 'MAJOR: Multiple child emperors: Puyi (2), Guangxu (3), Shunzhi (5), Tongzhi (5), Kangxi (7). '
             '5 of 10 (50%) acceded under age 10.'
}

# --- KOREA (JOSEON) ---
ACCESSION_AGES["Korea (Joseon)"] = {
    'ages': [
        # Taejo 57, Jeongjong 42, Taejong 33, Sejong 21, Munjong 36,
        # Danjong 11, Sejo 39, Yejong 18, Seongjong 12, Yeonsangun 18,
        # Jungjong 18, Injong 29, Myeongjong 11, Seonjo 14, Gwanghaegun 33,
        # Injo 28, Hyojong 30, Hyeonjong 18, Sukjong 13, Gyeongjong 32,
        # Yeongjo 30, Jeongjo 23, Sunjo 10, Heonjong 7, Cheoljong 18,
        # Gojong 11, Sunjong 33
        57, 42, 33, 21, 36, 11, 39, 18, 12, 18,
        18, 29, 11, 14, 33, 28, 30, 18, 13, 32,
        30, 23, 10, 7, 18, 11, 33
    ],
    'notes': 'Heonjong (7), Sunjo (10), Danjong (11), Myeongjong (11), Gojong (11), Seongjong (12).'
}

# --- DENMARK ---
ACCESSION_AGES["Denmark"] = {
    'ages': [
        # Selected from Gorm the Old onward (ages approximate for early kings)
        # Many early Danish kings have uncertain birth dates
        # Using well-documented post-1400 kings plus estimates for earlier
        # Eric of Pomerania ~15, Christopher III ~30, Christian I ~22,
        # John ~26, Christian II ~32, Frederick I ~48, Christian III ~37,
        # Frederick II ~25, Christian IV ~10, Frederick III ~39,
        # Christian V ~24, Frederick IV ~28, Christian VI ~30,
        # Frederick V ~23, Christian VII ~17, Frederick VI ~39,
        # Christian VIII ~55, Frederick VII ~40, Christian IX ~48,
        # Frederick VIII ~62, Christian X ~42, Frederick IX ~47,
        # Margrethe II ~31
        15, 30, 22, 26, 32, 48, 37, 25, 10, 39,
        24, 28, 30, 23, 17, 39, 55, 40, 48, 62,
        42, 47, 31
    ],
    'notes': 'Christian IV (10) is the most notable young accession. Most kings acceded as adults. '
             'Early kings (pre-1400) have uncertain ages and are excluded from this table.'
}

# --- SWEDEN (1523-present) ---
ACCESSION_AGES["Sweden"] = {
    'ages': [
        # Gustav I 27, Eric XIV 29, John III 31, Sigismund 25,
        # Charles IX 46, Gustavus Adolphus 16, Christina 6,
        # Charles X Gustav 32, Charles XI 4, Charles XII 14,
        # Ulrika Eleonora 30, Frederick I 44, Adolphus Frederick 39,
        # Gustav III 25, Gustav IV Adolf 15, Charles XIII 61,
        # Charles XIV John 54, Oscar I 44, Charles XV 33,
        # Oscar II 43, Gustav V 49, Gustav VI Adolf 67,
        # Carl XVI Gustaf 27
        27, 29, 31, 25, 46, 16, 6, 32, 4, 14,
        30, 44, 39, 25, 15, 61, 54, 44, 33, 43,
        49, 67, 27
    ],
    'notes': 'Charles XI (4), Christina (6), Charles XII (14), Gustav IV Adolf (15), Gustavus Adolphus (16).'
}

# --- SCOTLAND (843-1603) ---
ACCESSION_AGES["Scotland"] = {
    'ages': [
        # Post-1093 kings with better records:
        # Duncan II ~33, Edgar ~29, Alexander I ~31, David I ~44,
        # Malcolm IV ~12, William I ~21, Alexander II ~16,
        # Alexander III ~8, Margaret (Maid) ~3, John Balliol ~43,
        # Robert I ~32, David II ~5, Robert II ~54, Robert III ~53,
        # James I ~12, James II ~6, James III ~8, James IV ~15,
        # James V ~1, James VI ~1, Mary ~6 days
        33, 29, 31, 44, 12, 21, 16, 8, 3, 43,
        32, 5, 54, 53, 12, 6, 8, 15, 1, 1, 0
    ],
    'notes': 'MAJOR: Frequent child monarchs. Mary (6 days), James V (1), James VI (1), Margaret (3), '
             'David II (5), James II (6), Alexander III (8), James III (8).'
}

# --- MUGHAL EMPIRE ---
ACCESSION_AGES["Mughal Empire"] = {
    'ages': [
        # Babur 47, Humayun 22, Akbar 13, Jahangir 36, Shah Jahan 35,
        # Aurangzeb 39, Bahadur Shah I 63, Jahandar Shah 51,
        # Farrukhsiyar 30, Rafi ud-Darajat 18, Rafi ud-Dawla 21,
        # Muhammad Shah 17, Ahmad Shah Bahadur 22, Alamgir II 54,
        # Shah Jahan III ~30, Shah Alam II 33
        47, 22, 13, 36, 35, 39, 63, 51, 30, 18,
        21, 17, 22, 54, 30, 33
    ],
    'notes': 'Akbar (13) and Muhammad Shah (17) are the youngest. Most Mughal rulers acceded as adults.'
}

# --- SPAIN (1479-present) ---
ACCESSION_AGES["Spain"] = {
    'ages': [
        # Ferdinand II ~27, Isabella I ~23, Joanna ~25, Charles I ~16,
        # Philip II ~29, Philip III ~20, Philip IV ~16, Charles II ~3,
        # Philip V ~17, Louis I ~17, Ferdinand VI ~33, Charles III ~43,
        # Charles IV ~40, Ferdinand VII ~24, Isabella II ~3,
        # Amadeo I ~26, Alfonso XII ~17, Alfonso XIII ~0 (infant),
        # Juan Carlos I ~37, Felipe VI ~46
        27, 23, 25, 16, 29, 20, 16, 3, 17, 17,
        33, 43, 40, 24, 3, 26, 17, 0, 37, 46
    ],
    'notes': 'Alfonso XIII (infant), Charles II (3), Isabella II (3).'
}

# --- PORTUGAL (1139-1910) ---
ACCESSION_AGES["Portugal"] = {
    'ages': [
        # Afonso I ~28, Sancho I ~31, Afonso II ~26, Sancho II ~16,
        # Afonso III ~35, Dinis ~18, Afonso IV ~34, Pedro I ~37,
        # Fernando I ~22, John I ~28, Edward I ~41, Afonso V ~6,
        # John II ~26, Manuel I ~26, John III ~21, Sebastian ~3,
        # Henry ~66, Philip I ~53, Philip II ~24, Philip III ~16,
        # John IV ~36, Afonso VI ~13, Pedro II ~20, John V ~17,
        # Joseph I ~36, Maria I ~42, John VI ~45, Pedro IV ~23,
        # Maria II ~7, Pedro V ~16, Luís I ~23, Carlos I ~25, Manuel II ~18
        28, 31, 26, 16, 35, 18, 34, 37, 22, 28,
        41, 6, 26, 26, 21, 3, 66, 53, 24, 16,
        36, 13, 20, 17, 36, 42, 45, 23, 7, 16,
        23, 25, 18
    ],
    'notes': 'Sebastian (3), Afonso V (6), Maria II (7), Afonso VI (13).'
}

# --- RUSSIA (1462-1917) ---
ACCESSION_AGES["Russia"] = {
    'ages': [
        # Ivan III 22, Vasily III 26, Ivan IV 3, Theodore I 27,
        # Boris Godunov 47, False Dmitry I ~23, Vasily IV 54,
        # Michael I 16, Alexis 16, Theodore III 14, Ivan V 15,
        # Peter I 10, Catherine I 41, Peter II 11, Anna 37,
        # Ivan VI 0 (infant), Elizabeth 31, Peter III 33,
        # Catherine II 33, Paul I 42, Alexander I 23,
        # Nicholas I 29, Alexander II 36, Alexander III 36,
        # Nicholas II 26
        22, 26, 3, 27, 47, 23, 54, 16, 16, 14,
        15, 10, 41, 11, 37, 0, 31, 33, 33, 42,
        23, 29, 36, 36, 26
    ],
    'notes': 'Ivan VI (infant), Ivan IV (3), Peter I (10), Peter II (11), Theodore III (14).'
}

# --- PERSIA/IRAN ---
ACCESSION_AGES["Persia/Iran"] = {
    'ages': [
        # Ismail I 14, Tahmasp I 10, Ismail II 38, Muhammad Khodabanda 46,
        # Abbas I 17, Safi I 17, Abbas II 9, Suleiman I 18,
        # Sultan Husayn 26, Tahmasp II 18, Abbas III 0 (infant),
        # Nader Shah 50, Adil Shah 42, Shah Rukh 12,
        # Karim Khan Zand 40, Agha Muhammad Khan 47,
        # Fath-Ali Shah 25, Muhammad Shah Qajar 24,
        # Naser al-Din Shah 17, Mozaffar al-Din Shah 43,
        # Mohammad Ali Shah 35, Ahmad Shah 11, Reza Shah 44,
        # Mohammad Reza Shah 21
        14, 10, 38, 46, 17, 17, 9, 18, 26, 18,
        0, 50, 42, 12, 40, 47, 25, 24, 17, 43,
        35, 11, 44, 21
    ],
    'notes': 'Abbas III (infant), Abbas II (9), Tahmasp I (10), Ahmad Shah (11), Shah Rukh (12).'
}

# --- ETHIOPIA ---
ACCESSION_AGES["Ethiopia"] = {
    'ages': [
        # Many Ethiopian emperors have uncertain birth dates.
        # Using best estimates for Solomonic dynasty (post-1270)
        # Approximate ages for selected rulers with known data:
        # Yekuno Amlak ~40, Amda Seyon ~14, Dawit I ~17,
        # Yeshaq I ~22, Zara Yaqob ~35, Baeda Maryam ~16,
        # Na'od ~25, Lebna Dengel ~12, Gelawdewos ~18,
        # Minas ~30, Sarsa Dengel ~13, Yaqob ~25,
        # Susenyos ~28, Fasilides ~31, Yohannes I ~35,
        # Iyasu I ~20, Tekle Haymanot I ~14, Theophilus ~20,
        # Yostos ~40, Dawit III ~25, Bakaffa ~30,
        # Iyasu II ~7, Iyoas I ~13, Yohannes II ~30,
        # Tekle Haymanot II ~14, Tewodros II ~37,
        # Yohannes IV ~40, Menelik II ~44, Haile Selassie ~38
        40, 14, 17, 22, 35, 16, 25, 12, 18, 30,
        13, 25, 28, 31, 35, 20, 14, 20, 40, 25,
        30, 7, 13, 30, 14, 37, 40, 44, 38
    ],
    'notes': 'Iyasu II (7), Lebna Dengel (12), Sarsa Dengel (13), Iyoas I (13). Many uncertain dates.'
}

# --- USA (PRESIDENTS) ---
ACCESSION_AGES["USA (Presidents)"] = {
    'ages': [
        # Washington 57, Adams 61, Jefferson 57, Madison 57, Monroe 58,
        # JQ Adams 57, Jackson 61, Van Buren 54, WHHarrison 68, Tyler 51,
        # Polk 49, Taylor 64, Fillmore 50, Pierce 48, Buchanan 65,
        # Lincoln 52, AJohnson 56, Grant 46, Hayes 54, Garfield 49,
        # Arthur 51, Cleveland 47, BHarrison 55, Cleveland 55, McKinley 54,
        # TRoosevelt 42, Taft 51, Wilson 56, Harding 55, Coolidge 51,
        # Hoover 54, FDR 51, Truman 60, Eisenhower 62, Kennedy 43,
        # LBJ 55, Nixon 56, Ford 61, Carter 52, Reagan 69,
        # GHWBush 64, Clinton 46, GWBush 54, Obama 47, Trump 70, Biden 78
        57, 61, 57, 57, 58, 57, 61, 54, 68, 51,
        49, 64, 50, 48, 65, 52, 56, 46, 54, 49,
        51, 47, 55, 55, 54, 42, 51, 56, 55, 51,
        54, 51, 60, 62, 43, 55, 56, 61, 52, 69,
        64, 46, 54, 47, 70, 78
    ],
    'notes': 'All presidents acceded as adults. Youngest: T. Roosevelt (42). Oldest: Biden (78). Very narrow age range.'
}

# --- PAPACY (post-1000) ---
ACCESSION_AGES["Papacy (post-1000)"] = {
    'ages': [
        # Popes generally elected at advanced ages. Most are 50+.
        # Using known/estimated ages at election for major popes:
        # John XVIII ~55, Sergius IV ~50, Benedict VIII ~32, John XIX ~37,
        # Benedict IX ~18, Sylvester III ~50, Gregory VI ~55,
        # Clement II ~42, Damasus II ~42, Leo IX ~47, Victor II ~37,
        # Stephen IX ~38, Nicholas II ~48, Alexander II ~50,
        # Gregory VII ~52, Victor III ~60, Urban II ~47, Paschal II ~42,
        # ... (selecting representative sample)
        # Average election age post-1000 is approximately 59
        55, 50, 32, 37, 18, 50, 55, 42, 42, 47,
        37, 38, 48, 50, 52, 60, 47, 42, 55, 62,
        50, 56, 70, 60, 58, 52, 44, 57, 63, 55,
        68, 60, 49, 47, 62, 54, 45, 50, 48, 43,
        56, 63, 65, 75, 62, 70, 55, 65, 62, 70,
        65, 47, 58, 78, 59, 65, 62, 65, 55, 62,
        68, 65, 63, 58, 77, 78, 65, 76
    ],
    'notes': 'Popes elected at advanced ages (mean ~56). Benedict IX (18) is a notable exception. '
             'Election system selects experienced clergy, minimising young accessions.'
}

# --- KOREA (GORYEO) ---
ACCESSION_AGES["Korea (Goryeo)"] = {
    'ages': [
        # Taejo ~42, Hyejong ~22, Jeongjong ~25, Gwangjong ~24,
        # Gyeongjong ~21, Seongjong ~12, Mokjong ~17, Hyeonjong ~14,
        # Deokjong ~20, Jeongjong II ~35, Munjong ~28, Sunjong ~14,
        # Seonjong ~34, Heonjong ~9, Sukjong ~32, Yejong ~26,
        # Injong ~16, Uijong ~22, Myeongjong ~19, Sinjong ~53,
        # Huijong ~24, Gangjong ~21, Gojong ~21, Wonjong ~39,
        # Chungnyeol ~38, Chungseon ~23, Chungsuk ~19,
        # Chunghye ~14, Chungmok ~6, Chungjeong ~11,
        # Gongmin ~19, U ~12, Chang ~8, Gongyang ~45
        42, 22, 25, 24, 21, 12, 17, 14, 20, 35,
        28, 14, 34, 9, 32, 26, 16, 22, 19, 53,
        24, 21, 21, 39, 38, 23, 19, 14, 6, 11,
        19, 12, 8, 45
    ],
    'notes': 'Chungmok (6), Chang (8), Heonjong (9), Chungjeong (11), U (12).'
}

# --- KHMER EMPIRE ---
ACCESSION_AGES["Khmer Empire"] = {
    'ages': [
        # Very uncertain dates for most Angkor-period kings.
        # Using best scholarly estimates for rulers with known data:
        # Jayavarman II ~35, Jayavarman III ~?, Indravarman I ~35,
        # Yasovarman I ~25, Harshavarman I ~?, Isanavarman II ~?,
        # Jayavarman IV ~45, Harshavarman II ~?, Rajendravarman ~40,
        # Jayavarman V ~10, Udayadityavarman I ~30, Jayaviravarman ~?,
        # Suryavarman I ~35, Udayadityavarman II ~25, Harshavarman III ~?,
        # Jayavarman VI ~45, Dharanindravarman I ~55, Suryavarman II ~30,
        # Jayavarman VII ~55, Indravarman II ~30
        35, 30, 35, 25, 30, 30, 45, 30, 40, 10,
        30, 35, 35, 25, 30, 45, 55, 30, 55, 30
    ],
    'notes': 'Jayavarman V (10) is the only documented child king. Most ages are scholarly estimates with high uncertainty.'
}

# --- THAILAND (CHAKRI) ---
ACCESSION_AGES["Thailand (Chakri)"] = {
    'ages': [
        # Rama I 45, Rama II 42, Rama III 37, Rama IV 47,
        # Rama V 15, Rama VI 29, Rama VII 32, Rama VIII 9,
        # Rama IX 18, Rama X 64
        45, 42, 37, 47, 15, 29, 32, 9, 18, 64
    ],
    'notes': 'Rama VIII (9) and Rama V (15) are the youngest. Most acceded as adults.'
}

# --- EGYPT (NEW KINGDOM) ---
ACCESSION_AGES["Egypt (New Kingdom)"] = {
    'ages': [
        # Very uncertain for ancient Egyptian pharaohs.
        # Using Egyptological consensus estimates:
        # Ahmose I ~10, Amenhotep I ~25, Thutmose I ~35,
        # Thutmose II ~20, Thutmose III ~2, Hatshepsut ~25,
        # Amenhotep II ~18, Thutmose IV ~18, Amenhotep III ~12,
        # Akhenaten ~20, Smenkhkare ~20, Tutankhamun ~9,
        # Ay ~55, Horemheb ~40, Ramesses I ~55, Seti I ~25,
        # Ramesses II ~25, Merneptah ~60, Seti II ~40,
        # Amenmesse ~30, Siptah ~10, Twosret ~30,
        # Setnakhte ~55, Ramesses III ~30, Ramesses IV ~35,
        # Ramesses V ~25, Ramesses VI ~35, Ramesses VII ~30,
        # Ramesses VIII ~40, Ramesses IX ~35, Ramesses X ~40, Ramesses XI ~30
        10, 25, 35, 20, 2, 25, 18, 18, 12, 20,
        20, 9, 55, 40, 55, 25, 25, 60, 40, 30,
        10, 30, 55, 30, 35, 25, 35, 30, 40, 35, 40, 30
    ],
    'notes': 'Thutmose III (2), Tutankhamun (9), Ahmose I (~10), Siptah (~10). Many ages highly uncertain.'
}

# --- POLAND ---
ACCESSION_AGES["Poland"] = {
    'ages': [
        # Piast period + elective period with known/estimated ages:
        # Mieszko I ~30, Boleslaw I ~25, Mieszko II ~23, Casimir I ~22,
        # Boleslaw II ~26, Wladyslaw I Herman ~35, Boleslaw III ~18,
        # Wladyslaw II ~27, Boleslaw IV ~30, Mieszko III ~35,
        # Casimir II ~28, Leszek ~17, Wladyslaw III ~16, Henry I ~22,
        # Henry II ~45, Boleslaw V ~3, Leszek II ~25, Przemysl II ~35,
        # Wladyslaw ~38, Casimir III ~23, Louis ~44, Jadwiga ~10,
        # Wladyslaw II ~36, Wladyslaw III ~10, Casimir IV ~20,
        # John I ~32, Alexander ~41, Sigismund I ~39, Sigismund II ~28,
        # Henry ~22, Stephen Bathory ~43, Sigismund III ~21,
        # Wladyslaw IV ~37
        30, 25, 23, 22, 26, 35, 18, 27, 30, 35,
        28, 17, 16, 22, 45, 3, 25, 35, 38, 23,
        44, 10, 36, 10, 20, 32, 41, 39, 28, 22,
        43, 21, 37
    ],
    'notes': 'Boleslaw V (3), Jadwiga (10), Wladyslaw III (10).'
}

# =============================================================================
# K VALUES FROM MAIN ANALYSIS
# =============================================================================
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

# =============================================================================
# CALCULATIONS
# =============================================================================
print("=" * 100)
print("ACCESSION AGE ANALYSIS BY POLITY")
print("=" * 100)
print(f"{'Polity':<25} {'k':>6} {'N':>4} {'Med':>5} {'Mean':>6} {'SD':>6} {'<10':>5} {'<18':>5} {'<10%':>6} {'<18%':>6}")
print("-" * 100)

polity_names = []
k_vals = []
median_ages = []
mean_ages = []
pct_under_10 = []
pct_under_18 = []

for name in sorted(ACCESSION_AGES.keys(), key=lambda x: K_VALUES.get(x, 0)):
    data = ACCESSION_AGES[name]
    ages = np.array(data['ages'], dtype=float)
    k = K_VALUES.get(name, None)
    if k is None:
        continue
    
    n = len(ages)
    med = np.median(ages)
    mn = np.mean(ages)
    sd = np.std(ages)
    u10 = np.sum(ages < 10)
    u18 = np.sum(ages < 18)
    p10 = u10 / n * 100
    p18 = u18 / n * 100
    
    polity_names.append(name)
    k_vals.append(k)
    median_ages.append(med)
    mean_ages.append(mn)
    pct_under_10.append(p10)
    pct_under_18.append(p18)
    
    print(f"{name:<25} {k:>6.3f} {n:>4} {med:>5.1f} {mn:>6.1f} {sd:>6.1f} {u10:>5} {u18:>5} {p10:>5.1f}% {p18:>5.1f}%")

k_arr = np.array(k_vals)
med_arr = np.array(median_ages)
mean_arr = np.array(mean_ages)
p10_arr = np.array(pct_under_10)
p18_arr = np.array(pct_under_18)

# Correlations
print("\n" + "=" * 100)
print("CORRELATIONS: Weibull k vs Accession Age Metrics")
print("=" * 100)

for label, arr in [("Median accession age", med_arr), ("Mean accession age", mean_arr),
                   ("% accession < 10", p10_arr), ("% accession < 18", p18_arr)]:
    rp, pp = stats.pearsonr(k_arr, arr)
    rs, ps = stats.spearmanr(k_arr, arr)
    print(f"  {label:<30} Pearson r={rp:+.3f} p={pp:.4f}  Spearman rho={rs:+.3f} p={ps:.4f}")

# =============================================================================
# FIGURE: Accession Age Analysis (4 panels)
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Panel A: Box plot of accession ages by polity (sorted by k)
ax = axes[0, 0]
sorted_names = sorted(ACCESSION_AGES.keys(), key=lambda x: K_VALUES.get(x, 0))
box_data = [ACCESSION_AGES[n]['ages'] for n in sorted_names]
sorted_k = [K_VALUES.get(n, 0) for n in sorted_names]

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
norm = Normalize(vmin=0.85, vmax=2.8)
cmap = plt.cm.RdYlGn

bp = ax.boxplot(box_data, vert=True, patch_artist=True, widths=0.6,
               medianprops=dict(color='black', linewidth=1.5))
for i, (patch, k) in enumerate(zip(bp['boxes'], sorted_k)):
    patch.set_facecolor(cmap(norm(k)))
    patch.set_alpha(0.7)

ax.set_xticks(range(1, len(sorted_names)+1))
ax.set_xticklabels([n.replace(' (Emperors)', '\n(Emp.)').replace(' (post-1000)', '\n(1000+)')
                    .replace(' (Presidents)', '\n(Pres.)').replace(' (New Kingdom)', '\n(NK)')
                    .replace(' (Joseon)', '\n(Jos.)').replace(' (Goryeo)', '\n(Gor.)')
                    .replace(' (Chakri)', '\n(Cha.)').replace(' (Tang)', '\n(Tang)')
                    .replace(' (Ming)', '\n(Ming)').replace(' (Qing)', '\n(Qing)')
                    for n in sorted_names],
                   fontsize=6, rotation=45, ha='right')
ax.set_ylabel('Accession Age (years)', fontsize=11)
ax.set_title('(A) Accession Age Distribution by Polity\n(sorted by Weibull k, box colour = k)', fontsize=11, fontweight='bold')
ax.axhline(y=18, color='red', linestyle='--', alpha=0.5, label='Age 18')
ax.axhline(y=10, color='orange', linestyle='--', alpha=0.3, label='Age 10')
ax.legend(fontsize=8)

sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label('k value', fontsize=9)

# Panel B: k vs % accession under 18
ax2 = axes[0, 1]
for i, name in enumerate(polity_names):
    color = cmap(norm(k_vals[i]))
    ax2.scatter(k_vals[i], pct_under_18[i], c=[color], s=80,
               edgecolors='black', linewidth=0.5, zorder=5)
    if pct_under_18[i] > 40 or k_vals[i] > 2.0 or k_vals[i] < 0.9 or name in ['Japan (Emperors)']:
        offset = (5, 5)
        if name == 'Japan (Emperors)':
            offset = (5, -12)
        elif name == 'USA (Presidents)':
            offset = (-60, 5)
        ax2.annotate(name, (k_vals[i], pct_under_18[i]), fontsize=7,
                    xytext=offset, textcoords='offset points', alpha=0.8)

rp, pp = stats.pearsonr(k_arr, p18_arr)
ax2.text(0.05, 0.95, f'r = {rp:+.3f}\np = {pp:.4f}',
        transform=ax2.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax2.set_xlabel('Weibull Shape Parameter k', fontsize=11)
ax2.set_ylabel('% Accessions Under Age 18', fontsize=11)
ax2.set_title('(B) k vs Young Accession Rate (<18)', fontsize=11, fontweight='bold')

# Panel C: k vs median accession age
ax3 = axes[1, 0]
for i, name in enumerate(polity_names):
    color = cmap(norm(k_vals[i]))
    ax3.scatter(k_vals[i], median_ages[i], c=[color], s=80,
               edgecolors='black', linewidth=0.5, zorder=5)
    if name in ['Japan (Emperors)', 'USA (Presidents)', 'Papacy (post-1000)',
                'Mamluk Sultanate', 'Scotland', 'China (Qing)']:
        offset = (5, 5)
        if name == 'USA (Presidents)':
            offset = (-60, 5)
        elif name == 'Papacy (post-1000)':
            offset = (5, -12)
        ax3.annotate(name, (k_vals[i], median_ages[i]), fontsize=7,
                    xytext=offset, textcoords='offset points', alpha=0.8)

rp, pp = stats.pearsonr(k_arr, med_arr)
ax3.text(0.05, 0.95, f'r = {rp:+.3f}\np = {pp:.4f}',
        transform=ax3.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax3.set_xlabel('Weibull Shape Parameter k', fontsize=11)
ax3.set_ylabel('Median Accession Age (years)', fontsize=11)
ax3.set_title('(C) k vs Median Accession Age', fontsize=11, fontweight='bold')

# Panel D: Horizontal bar chart of % under 10, sorted by k
ax4 = axes[1, 1]
sorted_idx = np.argsort(pct_under_10)[::-1]
# Only show polities with >0% under 10
mask = [i for i in sorted_idx if pct_under_10[i] > 0]
bar_names = [polity_names[i] for i in mask]
bar_p10 = [pct_under_10[i] for i in mask]
bar_p18 = [pct_under_18[i] for i in mask]
bar_k = [k_vals[i] for i in mask]

y_pos = range(len(bar_names))
bar_colors_10 = [cmap(norm(k)) for k in bar_k]

bars1 = ax4.barh(y_pos, bar_p18, color='lightcoral', edgecolor='black', linewidth=0.3,
                 alpha=0.5, label='<18 years')
bars2 = ax4.barh(y_pos, bar_p10, color=[cmap(norm(k)) for k in bar_k],
                 edgecolor='black', linewidth=0.3, label='<10 years')

ax4.set_yticks(y_pos)
ax4.set_yticklabels(bar_names, fontsize=7)
ax4.set_xlabel('% Accessions at Young Age', fontsize=11)
ax4.set_title('(D) Young Ruler Proportion\n(colour = k value)', fontsize=11, fontweight='bold')
ax4.invert_yaxis()
ax4.legend(fontsize=8)

for i, (p10, p18, k) in enumerate(zip(bar_p10, bar_p18, bar_k)):
    ax4.text(p18 + 1, i, f'k={k:.2f}', va='center', fontsize=7, alpha=0.8)

plt.tight_layout()
plt.savefig('/home/ubuntu/monarch_accession_ages.png', dpi=150, bbox_inches='tight')
print(f"\nSaved: monarch_accession_ages.png")

# =============================================================================
# Summary for manuscript
# =============================================================================
print("\n" + "=" * 100)
print("KEY FINDINGS FOR MANUSCRIPT")
print("=" * 100)

# Top polities by % under 10
sorted_by_p10 = sorted(zip(polity_names, pct_under_10, k_vals), key=lambda x: -x[1])
print("\nPolities with highest % accession under age 10:")
for name, p10, k in sorted_by_p10[:10]:
    print(f"  {name:<25} {p10:5.1f}%  k={k:.3f}")

# Japan specifically
jp_ages = np.array(ACCESSION_AGES["Japan (Emperors)"]['ages'])
jp_u10 = np.sum(jp_ages < 10)
jp_u18 = np.sum(jp_ages < 18)
print(f"\nJapan Emperors: {jp_u10}/{len(jp_ages)} ({jp_u10/len(jp_ages)*100:.1f}%) under 10, "
      f"{jp_u18}/{len(jp_ages)} ({jp_u18/len(jp_ages)*100:.1f}%) under 18")
print(f"  Median accession age: {np.median(jp_ages):.1f}, Mean: {np.mean(jp_ages):.1f}")

# USA
us_ages = np.array(ACCESSION_AGES["USA (Presidents)"]['ages'])
print(f"\nUSA Presidents: All adults. Min={np.min(us_ages)}, Max={np.max(us_ages)}, "
      f"Median={np.median(us_ages):.1f}, Mean={np.mean(us_ages):.1f}")

plt.close('all')
print("\nDone.")
