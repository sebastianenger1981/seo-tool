# -*- coding: utf-8 -*-
"""
================================================================================
MODULE NAME: [unaique_algorithm_mvp.py]
================================================================================

DESCRIPTION:
    MVP of 2023 Pitch Deck: "The UNAIQUE Algorithm"

AUTHOR:
    Sebastian Enger <Sebastian.Enger@ArtikelSchreiber.com>

COMPANY:
    ArtikelSchreiber.com

VERSION:
    1.6.3

CREATED:
    2025-06-08

LAST MODIFIED:
    2025-06-19 by Sebastian Enger - ArtikelSchreiber.com and Unaique.com Prototype integrated

PYTHON VERSION:
    3.8+

DEPENDENCIES:
    - Standard Library: logging, sys, os, json, datetime, copy
    - Third Party: 
    - Internal: AIlify.py>=1.0.0

LICENSE:
    Copyright (c) 2025 ArtikelSchreiber.com. All rights reserved.
    
    For licensing information, contact: Sebastian.Enger@ArtikelSchreiber.com

SECURITY CLASSIFICATION:
    [TOP SECRET]    # GDPR/DSGVO -> PROFILING

CHANGELOG:
    v1.3.2 - [2025-06-14] - AIlify.py change, added OpenAIHandler Functionality
    v1.5.1 - [2025-06-15] - First successfull PERSONA Test
    v1.6.2 - [2025-06-17] - Fixed that Persona JSON from ArtikelSchreiber.com is not properbly handled over to write_persona_text function
    v1.6.3 - [2025-06-19] - Improved analyze_persona() function in AIlity.py with more comprehensive data points
    
TODO:
    - [ ] Implement feature X
    - [ ] Optimize performance for large datasets
    - [ ] Add comprehensive unit tests
    - [ ] Improve error handling for edge cases

KNOWN ISSUES:
    - Issue #: 

ARCHITECTURE NOTES:
    This module follows the Single Responsibility Principle and implements
    the Strategy pattern for extensibility. All external dependencies are
    injected to ensure testability and loose coupling.

PERFORMANCE NOTES:
    - 

SECURITY NOTES:
    - 

TESTING NOTES:
    - 

API COMPATIBILITY:
    - 

CONFIGURATION:
    Environment variables required:
    - 

MONITORING:
    - 

DEPLOYMENT NOTES:
    - 

EXAMPLES:
    Basic usage:
       

    Advanced usage:
       

RELATED MODULES:
    - 

EXTERNAL REFERENCES:
    - 

COMPLIANCE:
    - PCI DSS: 
    - GDPR: NOT Compliant with data protection requirements
    - SOX: 
    - ISO 27001: 

SUPPORT:
    For technical support, contact: Sebastian.Enger@ArtikelSchreiber.com
    For business questions, contact: Sebastian.Enger@ArtikelSchreiber.com
    Emergency escalation: Sebastian.Enger@ArtikelSchreiber.com

================================================================================
"""

#print("Working Folder is '/home/unaique/library3'!")
# Standard library imports
import time
start_time = time.time()
import logging
import sys
import os
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pathlib import Path

# Third-party imports
# import requests
# import pandas as pd
# import numpy as np

# Local/internal imports
# from .config import settings
# from .utils import helper_functions
# from .exceptions import CustomException

# Module-level constants
__version__ = "1.6.3"
__author__ = "Sebastian Enger, M.Sc."
__email__ = "Sebastian.Enger@ArtikelSchreiber.com"
__status__ = "Production"  # Development, Testing, Production
__maintainer__ = "Sebastian Enger"

"""
John 14:6
Jesus answered, "I am the way and the truth and the life. No one comes to the Father except through me."

John 8:31-32
Jesus said, "If you hold to my teaching, you are really my disciples. Then you will know the truth, and the truth will set you free."
"""

# Configure module-level logging
logger = logging.getLogger(__name__)

import json
import sys
import os
import subprocess
#sys.path.append('/home/unaique/library3')
sys.path.append('/home/unaique/library3/persona/library3')

from AIlify import AI
myAI 	        = AI()

content_tel2    = {}
content_tel     = {}
teler           = {}
teler1          = {}
teler2          = {}
ip_obj          = {}
persona_data    = {}
persona_unaique_dict = {}
MainKeyword     = "Hundefutter selber kochen"
SubKeywords     = "oder doch lieber Hundefutter einkaufen gehen"
myLanguage      = "Deutsch"

datafile1 		= "/home/unaique/library3/persona/unaique_algorithm_output_results_artikelschreibercom.json"
datafile2 		= "/home/unaique/library3/persona/unaique_algorithm_output_results_unaiquecom.json"

content_tel['text']                                 = ""
content_tel['language']                             = myLanguage
content_tel['persona_type']                         = "casual" # "business", "academic", "casual", "scientific", "creative", "marketing"
content_tel['use_textsample']                       = True
content_tel['persona_json_obj_artikelschreiber']    = ""

ip_obj["ip_address"] 	= str("79.198.31.232").strip()
ip_obj["ip_iso_code"] 	= str("DE").strip()
ip_obj["ip_country"] 	= str("Germany").strip()
ip_obj["ip_city"] 		= str("Brandenburg an der Havel").strip()
ip_obj["ip_postalcode"] = str("14776").strip()
ip_obj["ip_latitude"] 	= str("52.414167").strip()
ip_obj["ip_longitude"] 	= str("12.554167").strip()
ip_obj["ip_region"] 	= str("Brandenburg").strip()
#empty_json		= json.dumps({}, ensure_ascii=False)
encoding		= str('utf-8')
max_file_size	= int(5 * 1024 * 1024)	# 5MB

#############
### ArtikelSchreiber.com Version of 2023 UNAIQUE Algorithm Implementation
# Function: take input from MainKeyword and SubKeywords and build a persona profile over it, after that write a text for that Persona
persona_data                                        = myAI.analyze_persona(MainKeyword, SubKeywords, myLanguage, ip_obj)
if persona_data is not None and isinstance(persona_data, dict) and bool(persona_data) and len(persona_data) > 0 and persona_data != {} and persona_data:
    print(f"DEBUG: Lenght of persona_data: {len(persona_data)}")
    if "persona_unaique" in persona_data:
        persona_unaique_dict                        = persona_data.get("persona_unaique", {}) #persona_data["persona_unaique"]
else:
    print(f"DEBUG 1: {bool(persona_data)}")
    print(f"DEBUG 2: {type(persona_data)}")
    print(f"DEBUG 3: {persona_data}")
    sys.exit(1)
content_tel['text']                                 = MainKeyword + "," + SubKeywords
content_tel['persona_json_obj_artikelschreiber']    = json.dumps(persona_unaique_dict,ensure_ascii=False)
teler                                               = myAI.write_persona_text(content_tel)
p_datastorage1		                                = json.dumps(teler, ensure_ascii=False)
if os.path.exists(datafile1):
    os.unlink(datafile1)
myAI.safe_write_filecontent(datafile1, p_datastorage1)

persona_content     = teler.get("persona_content",'')
persona_title       = persona_content.get("persona_title",'')
persona_summary     = persona_content.get("persona_summary",'')
persona_text        = persona_content.get("persona_text",'')[:500]
persona_h1          = persona_content.get("persona_h1",'')
persona_h2          = persona_content.get("persona_h2",'')
persona_h3          = persona_content.get("persona_h3",'')
persona_paragraph   = persona_content.get("persona_paragraph",'')
persona_description = persona_content.get("persona_description",'')
persona_list        = persona_content.get("persona_list",'')

print("####### ArtikelSchreiber.com Implementation of UNAIQUE Algorithm #######")
print(f"PERSONA SPECIFIC TITLE: {persona_title}")
print(f"PERSONA SPECIFIC SUMMARY: {persona_summary}")
print(f"PERSONA SPECIFIC TEXT[:500]: {persona_text}")
print("####### ArtikelSchreiber.com Implementation of UNAIQUE Algorithm #######")

persona_article = f"""
<title>{persona_title}</title>
<p>{persona_summary}</p>
<h1>{persona_h1}</h1>
<p>{persona_paragraph}</p>
<h2>{persona_h2}</h2>
<p>{persona_list}</p>
<h3>{persona_h3}</h3>
<p>{persona_text}</p>
<p>{persona_description}</p>
"""

end_time = time.time()
elapsed_time = end_time - start_time

# Convert to human-readable format
minutes, seconds = divmod(elapsed_time, 60)
print(f"Elapsed time ArtikelSchreiber.com: {int(minutes)} minutes, {seconds:.3f} seconds")

print("####### #######")
print("####### #######")
print("####### #######")
print("####### #######")

start_time2 = time.time()

#############
### unaique.de Version of 2023 UNAIQUE Algorithm Implementation
# Function: take input from given text and build a persona profile over it (thats one part for "profiling") and then use one of 6 predefined personas to convert that input text to that persona so that 80% of the input text are comprehened by the target persona after the conversion
content_tel2['language']                             = myLanguage
content_tel2['persona_type']                         = "casual" # "business", "academic", "casual", "scientific", "creative", "marketing"
content_tel2['use_textsample']                       = True
content_tel2['persona_json_obj_artikelschreiber']    = ""
content_tel2['text'] = """
Nintendos kleiner Gamechanger

Smarte Verbesserungen, die man sofort spürt: Die Nintendo Switch 2 entpuppt sich als tolles Spieletablet für unterwegs. Auch langfristig?

N64, Gamecube, Wii und Wii U und dann die Switch: In den vergangenen Jahrzehnten hat Nintendo bei jedem Konsolenwechsel auch das Konzept geändert – teils radikal. Diesmal ist die Sache anders, die Switch 2 ist einfach nur ein Nachfolger – allerdings eine sorgfältig verbesserte, rundum modernisierte Version eines bewährten Geräts.

Statt das Rad neu zu erfinden, setzt Nintendo auf Feinschliff und mehr Power, um die bewährte Hybrididee fit für die Zukunft zu machen. Dieser Ansatz zeigt sich nicht nur im Gewicht oder der Haptik, sondern zieht sich durch alle Details: von den festeren Joy-Con über das schärfere Display bis hin zur stärkeren Hardware unter der Haube.

Die Switch 2 bringt etwa 150 Gramm mehr auf die Waage als der Vorgänger. Das fällt besonders beim direkten Vergleich zwischen den beiden Modellen auf – allerdings keineswegs negativ. Im Gegenteil: Durch das zusätzliche Gewicht liegt die neue Konsole insgesamt sogar angenehmer in der Hand.

Das liegt auch am hochwertigeren Gehäusematerial. Der Kunststoff wirkt angenehm samtig, die Verarbeitung macht einen durchdachten und robusten Eindruck. Die überarbeiteten Joy-Con-Controller verbinden sich jetzt magnetisch mit der Konsole und sitzen viel fester als zuvor.

Die erweiterten Dimensionen tragen zur Bedienbarkeit bei. Tasten und Analogsticks lassen sich jetzt präziser und komfortabler steuern. Gerade bei Spielen, die feine Steuerung erfordern, ist das ein Gewinn. Aber: Mit großen Händen kann der rechte Stick weiterhin auf Dauer unbequem werden, weil man den Daumen stark anwinkeln muss.

Bei der internen Hardware geht Nintendo mit der Switch 2 nach sieben Jahren den nächsten Technologieschritt. Während das grundlegende Konzept aus Dock- und Handheld-Betrieb erhalten bleibt, hat sich unter der Haube vieles geändert. Vom Prozessor über die GPU bis zum Arbeitsspeicher bietet die neue Konsole einen Leistungssprung, der in der Praxis spürbar ist.

Herzstück ist ein Nvidia Tegra T239 SoC, entwickelt auf Basis der Ampere-Architektur. Anders als bei der Ur-Switch kommt ein Acht-Kern-CPU-Cluster zum Einsatz: Sechs performante ARM Cortex-A78C-Kerne übernehmen die Spielelast, zwei weitere A78C-Kerne sind für System- und Hintergrundprozesse reserviert.

Im Dock-Modus taktet der Prozessor mit bis zu 998 MHz, im Handheld sind es leicht höhere 1.101 MHz. In kurzen Turbo-Bursts sind bis zu 1,7 GHz möglich. Damit liegen CPU-Leistung und Architektur über der Playstation 4, aber nicht auf dem Niveau aktueller Konsolen wie Playstation 5 oder Xbox Series X.

Auffällig: Dank Nvidias Energiemanagement (Dynamic Voltage and Frequency Scaling, DVFS) skaliert die CPU sehr flexibel zwischen den Modi. Im Handheld steht zudem ein sparsamer Eco-Mode mit einem Takt von 470 MHz zur Verfügung, etwa für alte 2D-Titel oder Emulator-Software.

Der mit Abstand größte Schritt findet bei der Grafik statt: Die neue Ampere-basierte GPU des T239 bietet 1.536 CUDA-Kerne, 24 RT-Cores für Raytracing und 48 Tensor-Cores für KI-Berechnungen und Deep Learning Super Sampling (DLSS).

Laut Nvidia liegt die theoretische Rechenleistung bei rund 3,07 Tflops im Dock-Modus und 1,71 Tflops beim Handheld. Das entspricht etwa einer mobilen RTX 3050 und ist damit rund zehnmal stärker als die 1,0 Tflops der ersten Switch.
""".strip()
# Text Source: https://www.golem.de/news/nintendo-switch-2-im-test-kleiner-gamechanger-statt-grosse-revolution-2506-197118.html

teler2          = myAI.write_persona_text(content_tel2)
p_datastorage1  = json.dumps(teler2, ensure_ascii=False)
if os.path.exists(datafile2):
    os.unlink(datafile2)
myAI.safe_write_filecontent(datafile2, p_datastorage1)

persona_content = teler2.get("persona_content",'')
persona_title   = persona_content.get("persona_title",'')
persona_summary = persona_content.get("persona_summary",'')
persona_text    = persona_content.get("persona_text",'')[:500]

print("####### Unaique.de Implementation of UNAIQUE Algorithm #######")
print(f"PERSONA SPECIFIC TITLE: {persona_title}")
print(f"PERSONA SPECIFIC SUMMARY: {persona_summary}")
print(f"PERSONA SPECIFIC TEXT[:500]: {persona_text}")
print("####### Unaique.de Implementation of UNAIQUE Algorithm #######")

end_time2 = time.time()
elapsed_time2 = end_time2 - start_time2

# Convert to human-readable format
minutes, seconds = divmod(elapsed_time2, 60)
print(f"Elapsed time Unaique.de: {int(minutes)} minutes, {seconds:.3f} seconds")
sys.exit(0)