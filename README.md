# Honeypot Ethics Review Dataset

A systematic ethics analysis dataset for honeypot systems, combining peer-reviewed scientific papers and open-source honeypot tools. Created as part of a literature review on honeypot ethics, with a focus on cybersecurity.

---

## Overview

This repository contains a unified dataset that evaluates **239 honeypot entries** across 18 ethical dimensions including IRB/ethics committee mention, consent model, data sensitivity, jurisdiction awareness, and deception framing.

The dataset covers two source types:

| Source | Count | Description |
|---|---|---|
| **Scientific** | 38 | Peer-reviewed papers proposing actual honeypot systems |
| **Non-Scientific** | 201 | Open-source honeypot tools from the [awesome-honeypots](https://github.com/paralax/awesome-honeypots) list and [Honeynet Project](https://www.honeynet.org/projects/) |
| **Total** | **239** | |

---

## Repository Contents

```
Honeypot-Ethics-Review/
├── honeypot_ethics_dataset.csv         # Unified dataset (239 rows × 50 columns)
├── honeypot_ethics_analysis.ipynb      # Jupyter Notebook — 24-cell step-by-step analysis
├── taguette_codebook.csv               # Codebook with 71 open codes for qualitative coding
├── taguette_docs/                      # 239 plain-text documents for Taguette coding
│   ├── SCI_001 to SCI_038              # Scientific honeypot papers (38 files)
│   └── NS_039 to NS_239                # Non-scientific open-source tools (201 files)
├── requirements.txt
└── README.md
```

---

## Dataset Structure

The CSV file (`honeypot_ethics_dataset.csv`) has **50 columns** organised into three groups:

### 1. Identity Columns (all entries)

| Column | Description |
|---|---|
| `source_type` | `Scientific` or `Non-Scientific` |
| `identifier` | Full paper citation (Scientific) or tool name (Non-Scientific) |
| `link` | Paper URL or GitHub/project link |

### 2. Documentation Columns (Non-Scientific only, empty for papers)

| Column | Description |
|---|---|
| `platform` | Hosting platform (GitHub, SourceForge, Commercial, etc.) |
| `stars` | GitHub star count at time of collection, or `N/A` for non-GitHub |
| `readme_present` | Yes / No |
| `docs_folder` | Yes / No |
| `wiki_present` | Yes / No |
| `external_docs_link` | Yes / No |
| `primary_doc_location` | README / Docs Folder / Wiki / External / None |
| `doc_level` | None / Minimal / Moderate / Extensive |
| `docs_url` | URL of primary documentation |
| `tool_notes` | Short factual description of the tool |

### 3. Shared Ethics Columns (both source types — 37 columns)

Each of the 18 dimensions below has a **value column** and a **justification column** containing text evidence directly from the paper or repository.

| Dimension | Value Column | Values |
|---|---|---|
| Security domain | `domain` | IT / ICS / CPS / Space / CAV / Other |
| Interaction level | `interaction_level` | Low / Medium / High / Not available |
| Threat model | `threat_model` | Textual |
| IRB / ethics committee | `irb_mentioned` | Yes / No / Not available |
| Consent model | `consent_model` | Explicit / Implicit / None / Not documented |
| Data types collected | `data_types_collected` | Textual |
| Network protocols & ports | `protocols_ports` | Textual |
| Data sensitivity | `data_sensitivity` | Low / Medium / High / Not available |
| Data minimization | `data_minimization` | Yes / No / Not discussed |
| Data retention policy | `data_retention_policy` | Textual |
| Data sharing / release | `data_sharing` | Textual |
| Jurisdiction / legal | `jurisdiction_legal` | Textual |
| Containment & harm prevention | `containment_measures` | Textual |
| Deception framing | `deception_framing` | Purely technical / Ethical discussion / None |
| Researcher responsibility | `researcher_responsibility` | Textual |
| Ethical gaps / red flags | `ethical_gaps` | Textual |
| Relevance to project | `relevance_to_project` | Textual |
| Deployment context | `deployment` | Textual |
| No external deployment | `no_external_deployment` | Yes / No / Not documented |

All `*_justification` columns contain direct quotes or precise references to the source material (page numbers, sections, or README content).

---
## Qualitative Coding

The `taguette_docs/` folder contains 239 plain-text documents, one per dataset entry, prepared for qualitative open coding in [Taguette](https://www.taguette.org). Each document contains the assessed values for context and the full justification text for each of the 18 ethical dimensions as the coding target.

The `taguette_codebook.csv` file contains the initial codebook with **71 open codes** identifying recurring ethical concepts across the dataset. The codes are organised around the following concept groups:

| Group | Example Codes |
|---|---|
| IRB / Oversight | `IRB-Absent`, `IRB-Present` |
| Consent | `Consent-None`, `Consent-Implicit`, `Attacker-Notification` |
| Data Collection | `Credential-Collection`, `Session-Recording`, `Malware-Capture`, `ICS-Data-Capture`, `Medical-Data-Risk` |
| Data Governance | `Data-Retention-Absent`, `Data-Minimization-Absent`, `Data-Sharing-Third-Party` |
| Privacy | `GDPR-Concern`, `IP-Address-Privacy`, `Consumer-Privacy` |
| Legal & Jurisdiction | `Jurisdiction-Absent`, `Radio-Frequency-Regulation`, `Terms-of-Service` |
| Containment & Harm | `Containment-Gap`, `Real-Backend-Risk`, `Physical-Domain-Risk`, `Third-Party-Harm` |
| Deception Ethics | `Deception-Technical-Only`, `Active-Deception`, `LLM-Deception`, `Dual-Use-Risk` |
| Researcher Responsibility | `Researcher-Responsibility-Absent`, `Responsible-Disclosure` |
| AI & Automation | `LLM-Third-Party-API`, `AI-Governance-Absent`, `Technology-Driven-Ethical-Lag` |
| Deployment Context | `Internet-Facing-Deployment`, `Critical-Infrastructure-Deployment`, `Consumer-Distribution` |
| Threat Intelligence | `Threat-Intel-Sharing`, `Threat-Intel-No-Governance`, `Victim-Data-Risk` |
| Ethics-by-Containment | `Ethics-by-Containment`, `No-Ethical-Framing` |
| Domain-Specific | `ICS-Ethics`, `Healthcare-Ethics`, `Space-Ethics`, `IoT-Ethics` |

---

## Domains Covered

| Domain | Description | Example entries |
|---|---|---|
| **IT** | General IT / network security | Cowrie, Glastopf, Kippo, dionaea |
| **ICS** | Industrial Control Systems | Conpot, GasPot, gridpot, HoneyPLC |
| **CPS** | Cyber-Physical Systems | SIoTpot, RIoTPot, SweetCam, TwinPot |
| **Space** | Satellite / space systems | HoneySat |
| **CAV** | Connected & Autonomous Vehicles | Entries from UAV/vehicle domain |
| **Other** | Healthcare, specialised | dicompot (DICOM), medpot (HL7/FHIR) |

---

## Quick Start

### Requirements

```bash
pip install -r requirements.txt
```

### Run the analysis script

```python
import pandas as pd

df   = pd.read_csv('honeypot_ethics_dataset.csv', low_memory=False)
sci  = df[df['source_type'] == 'Scientific']
nons = df[df['source_type'] == 'Non-Scientific']

print(f"Total: {len(df)} | Scientific: {len(sci)} | Non-Scientific: {len(nons)}")
print(df['domain'].value_counts())
print(df['irb_mentioned'].value_counts())
```

### Run the Jupyter Notebook

```bash
jupyter notebook honeypot_ethics_analysis.ipynb
```

The notebook contains **24 self-contained analysis cells** covering:

| Cell | Analysis |
|---|---|
| 1–2 | Imports and load dataset |
| 3 | Sample rows overview |
| 4 | Dataset composition (Scientific vs Non-Scientific) |
| 5–6 | Domain distribution |
| 7 | Interaction level distribution |
| 8 | IRB mention rate |
| 9 | Consent model breakdown |
| 10 | Data sensitivity distribution |
| 11 | Data minimization discussion rate |
| 12 | Deception framing breakdown |
| 13 | Ethics governance heatmap (6 dimensions) |
| 14 | GitHub stars distribution (tools only) |
| 15 | Documentation quality (tools only) |
| 16 | Platform breakdown (tools only) |
| 17 | Interaction level × Data sensitivity cross-tab |
| 18 | Ethics governance radar chart |
| 19 | Ethics coverage score by domain |
| 20 | Top 15 most-starred tools |
| 21 | ICS / CPS / Space deep dive |
| 22 | Scientific papers domain distribution |
| 23 | Full summary statistics table |
| 24 | Key findings |

---

## Key Findings

Based on the full dataset of 239 entries:

- **IRB / Ethics committee**: mentioned in fewer than 5% of all entries - nearly universally absent across both scientific papers and open-source tools
- **Consent model**: documented (Explicit or Implicit) in fewer than 10% of scientific papers and 0% of open-source tools
- **Data minimization**: discussed in fewer than 15% of scientific papers, 0% of tools
- **Deception ethics**: only a small minority of scientific papers frame deception beyond a purely technical mechanism - no open-source tools do
- **High data sensitivity** (keystrokes, medical data, ICS protocol data, credentials): present in ~25% of all entries, without corresponding governance documentation
- **Dominant domain**: IT (82%), followed by ICS (8%) and CPS (7%)
- **Most common interaction level**: Low (69%), Medium (17%), High (11%)

---

## Data Collection Methodology

### Scientific Papers

- Source: Systematic literature search across IEEE Xplore, ACM Digital Library, USENIX, Springer, and arXiv
- Filter: Only papers proposing, implementing, or deploying an actual honeypot system (not purely detection, evaluation, or survey papers)
- Coverage: Papers from 2013–2026, spanning IT, ICS, CPS, Space, and CAV domains

### Non-Scientific Tools

- Primary source: [paralax/awesome-honeypots](https://github.com/paralax/awesome-honeypots) (community-curated list)
- Secondary source: [Honeynet Project](https://www.honeynet.org/projects/)
- Each tool was individually verified by visiting the GitHub repository, SourceForge page, or project website
- Documentation quality assessed from live verification (README, /docs folder, Wiki, external site)
- GitHub star counts collected at time of audit

### Ethics Analysis

All 18 ethics dimensions were assessed per entry by:
1. Reading the full paper (for scientific entries) or README/documentation (for tools)
2. Recording the value (e.g., `Yes` / `No` / `Not discussed`)
3. Recording the justification with direct quotes or section/page references

## Repository Context

This dataset was created to support a literature review examining the ethics gap in honeypot research. The central research question is:

> *To what extent do existing honeypot systems - both in academic research and open-source practice - address ethical dimensions such as IRB oversight, informed consent, data governance, and responsible deception?*

The dataset supports the development of an ethics framework for honeypot deployment in critical infrastructure contexts, with particular focus on space and satellite systems (HoneySat).

---

## Collaborators



## Citation



## Licence