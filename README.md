# research-NetworkCitation_Edduba
**"Bibliographic Networks of Knowledge Transmission in Edubba Scholarship"** 

---
#### Description: 
How knowledge about scribal schools circulates within academic discourse? 
This project analyses the epistemic structure of academic scholarship on Edubba scribal schools of the Old Babylonian period through citation network analysis.
*****
**Project Status:**
**🟡 in Process** / 🟢 Complete / 🔴 On a Wait
##### About Project: 
This project does not aim to reinterpret Edubba history directly. Instead, it treats scholarly publications as a citation network in order to analyse how knowledge about Edubba is structurally produced, transmitted, and stabilised within academic discourse. The focus is therefore not on what is known about Edubba, but on how that knowledge is organised across the scholarly ecosystem. 
To make these structures visible, the study combines network analysis with a systematic data collection and visualisation pipeline. Citation relations are modelled as directed edges between publications, enabling the construction of a multi-layered epistemic network.
A directed citation graph of 2,103 sources was constructed from a seed corpus of approximately 150 anchor publications, expanded via a snowball bibliographic method. Network metrics — including in-degree, betweenness centrality, eigenvector centrality, and a custom step-distance model — were applied to classify sources by their epistemic role.
The guiding assumption is that epistemic structure becomes observable only when translated into visual form, where relational properties such as mediation, centrality, and fragmentation can be directly perceived.

***
##### Research Questions and Hypotheses:
- **RQ1** How is scholarly knowledge about Edubba schools structurally organised within the academic citation network and what role do primary archaeological sources play within this structure?
- **RQ2** Which sources can be identified as epistemically reliable based on their structural position relative to primary data  and do the most reliable sources coincide with the most cited ones?

---
**H1 Network Topology Hypothesis**    
The dissemination of knowledge about Edubba in the citation network has a hierarchical (tree-like) structure: primary sources are the roots, interpretive and authoritative works are the branches?

---
**H2 Structural Gap Hypothesis**   
Primary archaeological sources are structurally isolated from the most cited authoritative works, there are no direct or indirect citational links between them?

---
**H3 Bottleneck Hypothesis**   
The only structural bridge between the primary sources (Step 1) and the authoritative literature (Step 3) is an extremely small layer of mediators (Step 2), which forms a bottleneck. This effect is a structural property of the network, not an artifact of the classification method.

---
**H4 Epistemic Displacement Hypothesis**     Structural influence in the network (eigenvector centrality) is concentrated in Step 3, not Step 1 primary sources are rarely involved in dense, interconnected clusters. Significance is formed not where the data originates, but where interpretations are repeatedly cited?

---
**H5 Epistemic Reliability Rarity Hypothesis**    
Sources that simultaneously satisfy all three criteria of trustworthiness (connection to primary data, high in-degree, and mutual reinforcement via the Trust Triangle) are structurally rare (less 1% of the corpus) and belong to mediators (Step 2) rather than authorities (Step 3)?   
**Reference:**[`/1-intro/`](./1-intro/)
***
##### Repository Structure:
- intro/
- datasets/
- notebooks/
- scripts/
- images/
- bibliography/
- documentation/
- outputs_Modul1/
- outputs_Modul2/
***
#### How To Use:
***
#### Methodology:    
To assess the reliability and epistemic role of sources in the corpus, this study employs a custom **Step-Distance Model** [`/7-documentations/`](./7-documentations/). Full operational definitions and assignment criteria of Step-Distance Model  are provided in the Methods section and in description of the structure of the method. Due to which it became possible to carry out a quantitative analysis of several hypotheses. Each hypothesis emerges from the result of the previous one, forming a chain of evidence rather than a set of independent tests.    
**Reference:** [`/1-intro/`](./1-intro/)
***
#### Data:
Custom dataset manually compiled from archaeological reports and scholarly bibliographic sources.    
**Reference:**  [`/docDataAbstraction/`](./7-documentations/).  
**Reference:** [`/docDataCollection/`](./2-dataset/)   
**Reference:** [`/2-dataset/`](./2-dataset/)
***
#### Sources: 
**Reference:** [`/6-bibliography/`](./6-bibliography/)
***
#### Format: 
**input-pdf -> txt -> json -> network graph-> analyse data -> .png visualisation output**  
***
#### Language: Enlish 
*** 
#### Period: Jenuary - May 2026
***
#### Software and Digital Tools
- **Python** — data processing and analysis  
  https://www.python.org
- **igraph** — network construction and analysis  
  https://igraph.org
- **AnyStyle** — bibliographic reference extraction  
  https://anystyle.io
- **pdfplumber** — PDF text extraction  
  https://github.com/jsvine/pdfplumber
- **pytesseract** — OCR for scanned documents  
  https://github.com/madmaze/pytesseract
***
#### Outputs
1. Citation Network Dataset  [`/2-dataset/`](./2-dataset/)
2. Visualisations of the Network Analysis  [`/5-visualisation/`](./5-visualisation/)
3. Research Report: Citation Network Analysis Perspective [`/8-output_Modul1/`](./8-output_Modul1/)
4. Research Report: Information Visualisation Perspective [`/8-output_Modul2/`](./8-output_Modul2/) 
5. Project Presentation [`/8-output_Modul1/`](./8-output_Modul1/) 
#### Author:
Aim Batalova — Ca'Foscari University — email: aim.b14.04git@gmail.com
***
#### License:



## Project Status
🟡 in Process  / 🟢 Complete / 🔴 On a Wait 

## About Project
[2-3 sentences: what was developed? what reason? what the methods?]
This project analyses the epistemic structure of academic scholarship on Edubba scribal schools of the Old Babylonian period through citation network analysis. 
Edubba is a scribal school of the Old Babylonian period (20th–17th centuries BCE), considered one of the earliest institutions with structured educational organisation. Despite the significance of these institutions, modern scholarship lacks a unified understanding of their structure, spatial distribution, and operating principles.
The concept of "school" in the Old Babylonian context remains ambiguous: it has been interpreted as a formal institution, a social space, or a set of educational practices not necessarily tied to a fixed location. Archaeological data is fragmentary — while thousands of educational tablets have been documented, only rarely does find context allow for confident identification of a school building.
A key methodological problem is that scholarly literature reproduces established interpretations without making visible the origin of specific claims. Much knowledge about Edubba is reconstructed from interpretive chains rather than from primary evidence. This study aims to map these chains formally: not to interpret the history of Edubba itself, but to analyse how knowledge about it circulates within academic discourse.
The project's goal is thus aligned with the aim of information visualisation: to make visible a structure that is otherwise invisible — the epistemic architecture of a scholarly field. As defined in this course, a good visualisation should help discover patterns not apparent from raw data, and present findings to a broad audience in a trustworthy and accessible way
### Research Questions and Hypotheses
**RQ1** - How is scholarly knowledge about Edubba schools structurally organised within the academic citation network and what role do primary archaeological sources play within this structure?
**RQ2** - Which sources can be identified as epistemically reliable based on their structural position relative to primary data  and do the most reliable sources coincide with the most cited ones?
To assess the reliability and epistemic role of sources in the corpus, this study employs a custom Step-Distance Model.  Full operational definitions and assignment criteria are provided in the Methods section and in description of the structure of the method.

**H1**. Network Topology Hypothesis -The dissemination of knowledge about Edubba in the citation network has a hierarchical (tree-like) structure: primary sources are the roots, interpretive works are the branches, and authoritative works are the crown.
**H2**.Structural Gap Hypothesis - Primary archaeological sources(Step 1) are structurally isolated from the most cited authoritative works (Step 2), there are no direct or indirect citational links between them.
**H3**.Bottleneck Hypothesis - The only structural bridge between the primary sources (Step 1) and the authoritative literature (Step 3) is an extremely small layer of mediators (Step 2), which forms a bottleneck. This effect is a structural property of the network, not an artifact of the classification method.
**H4.** Epistemic Displacement Hypothesis - Structural influence in the network (eigenvector centrality) is concentrated in Step 3, not Step 1 primary sources are rarely involved in dense, interconnected clusters. Significance is formed not where the data originates, but where interpretations are repeatedly cited.
**H5.**Epistemic Reliability Rarity Hypothesis - Sources that simultaneously satisfy all three criteria of trustworthiness—connection to primary data, high in-degree, and mutual reinforcement via the Trust Triangle—are structurally rare (<1% of the corpus) and belong to mediators (Step 2) rather than authorities (Step 3).

## Repository Structure
- paper/          
- datasets/       
- notebooks/     
- cripts/         
- visualizations/ 
- bibliography/   
- documentation/  
- presentations/  
- outputs/        

## Methodology
Network metrics — including in-degree, betweenness centrality, eigenvector centrality, and a custom step-distance model — were applied to classify sources by their epistemic role. Visualisations reveal a structurally sparse network in which primary archaeological sources are systematically decoupled from high-centrality clusters.

## Data
- Sources: Archaeological Report and Scholar Editions about Scribal School in Old Babylonian Period. 
- Format: Pdf format
- Language: English, French, German
- Period: 1890 - 2024 

## Tools
- Python 3.x
- [список библиотек]

## How To Use
[2-3 шага если нужно]

## Status and Result
[Что уже сделано]

## Author
[Aim Batalova] — [Ca'Foscari University] — [email: aim.b14.04git@gmail.com]

## License
MIT License

