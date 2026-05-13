## Data Collection  
A core corpus of approximately 150 anchor sources was compiled to define the thematic scope(sourcesAnchor.csv). Sources were selected based on two criteria:   
1.Exclusive academic affiliation with the topic of scribal education in the Old Babylonian period.  
2.And unique DOI identifiers ensuring verifiability.  
Large monographs covering heterogeneous topics were excluded, with exceptions for works focused exclusively on Mesopotamian scribal practices.  
In parallel, archaeological excavation reports were collected as primary sources (Step 1) and stored in a structured CSV file(sourcesArchaeologicalRelies.csv) including site information, excavation metadata, tablet counts, and references. These were entered manually.

---
#### Data Preparation
PDF documents were converted to text using pdfplumber for digital files and pytesseract OCR for scanned materials. Texts were manually cleaned and structured into standardised sections:   
 #Metadata  
 #Text  
 #Figures  
 #Bibliography   
 Metadata were normalised and each source assigned a unique global identifier, resulting in 50 anchor sources with bibliography.

---
#### Bibliographic Expansion (Snowball Method)
Bibliographies were automatically extracted with AnyStyle, converted to structured JSON, and matched to identify citing–cited relationships (references.json). The snowball expansion grew the dataset from ~150 anchor sources to 2,103 unique nodes and 2,524 edges (sources_all_normalized.csv).