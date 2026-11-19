# Honeypot Ethics Review Dataset

A systematic ethics analysis of honeypot systems, combining peer-reviewed scientific papers and open-source honeypot tools. It supports the SoK "The Ethics of Honeypots" and follows one pipeline: literature -> dataset -> qualitative coding -> taxonomy.

---

## Overview

The unified dataset evaluates **239 honeypot entries** across 18 ethical dimensions, including IRB / ethics committee mention, consent model, data sensitivity, jurisdiction awareness and deception framing.

| Source | Count | Description |
|---|---|---|
| **Scientific** | 38 | Peer-reviewed papers proposing actual honeypot systems |
| **Non-Scientific** | 201 | Open-source honeypot tools from the [awesome-honeypots](https://github.com/paralax/awesome-honeypots) list and the [Honeynet Project](https://www.honeynet.org/projects/) |
| **Total** | **239** | |

Current dataset version: **v3.1** (values aligned with the final open coding of 2026-11-16, deployment-independent data-sensitivity rubric, documentation quantity by word count).

---

## Repository Contents

```
Honeypot-Ethics-Review/
├── dataset/
│   └── honeypot_ethics_dataset.csv          # Unified dataset (239 rows x 49 columns), v3.1
├── analysis/
│   ├── honeypot_ethics_analysis_v2.ipynb    # Current analysis: paper-style figures (under review)
│   └── honeypot_ethics_analysis.ipynb       # Earlier analysis, kept until v2 is approved
├── taguette/                                # Qualitative open-coding artifacts
│   ├── docs/                                # 239 plain-text documents (SCI_001-SCI_038, NS_039-NS_239)
│   ├── codebook.csv                         # Codebook with 69 open codes
│   ├── scientific-pdf-coding-final-2026-11-16.sqlite3     # Final coding of the 38 paper PDFs
│   ├── ns-tool-documentation-final-2026-11-16.sqlite3     # Final coding of the 201 tools' documentation
│   ├── scientific-open-coding-2026-10-25.sqlite3          # Earlier round (dataset justifications), papers
│   └── non-scientific-open-coding-2026-10-25.sqlite3      # Earlier round (dataset justifications), tools
├── taxonomy/                                # Ethics taxonomy v0.1: SQLite database + browser GUI
│   ├── taxonomy.sqlite
│   ├── index.html                           # List view
│   ├── tree.html                            # Tree view
│   ├── taxonomy_content.py
│   ├── build_taxonomy.py
│   └── README.md
├── requirements.txt
└── README.md
```

---

## Dataset Structure

`dataset/honeypot_ethics_dataset.csv` has **49 columns** in three groups.

### 1. Identity Columns (all entries)

| Column | Description |
|---|---|
| `source_type` | `Scientific` or `Non-Scientific` |
| `identifier` | Full paper title (Scientific) or tool name (Non-Scientific) |
| `link` | Paper URL or GitHub / project link |

### 2. Documentation Columns (Non-Scientific only, empty for papers)

| Column | Description |
|---|---|
| `platform` | Hosting platform (GitHub, GitLab, Website, etc.) |
| `stars` | GitHub star count at time of collection, or `N/A` for non-GitHub |
| `readme_present` | Yes / No |
| `docs_folder` | Yes / No |
| `wiki_present` | Yes / No |
| `external_docs_link` | Yes / No |
| `primary_doc_location` | README / Docs Folder / Wiki / External / None |
| `doc_level` | Documentation quantity by word count of the harvested docs: None (< 50 words) / Minimal (< 500) / Moderate (< 2,000) / Extensive (>= 2,000) |
| `docs_url` | URL of primary documentation |
| `tool_notes` | Short factual description of the tool |

### 3. Shared Ethics Columns (both source types - 36 columns)

Each of the 18 dimensions below has a **value column** and a **justification column** with evidence taken directly from the paper or repository.

| Dimension | Value Column | Values |
|---|---|---|
| Security domain | `domain` | IT / ICS / CPS / IoT / Industrial IoT (IIoT) / Space / UAV / Other |
| Interaction level | `interaction_level` | Low / Medium / High / Hybrid / Not applicable / Not available |
| Threat model | `threat_model` | Textual |
| IRB / ethics committee | `irb_mentioned` | Yes / No |
| Consent model | `consent_model` | Explicit / Implicit / None |
| Data types collected | `data_types_collected` | Textual |
| Network protocols & ports | `protocols_ports` | Textual |
| Data sensitivity | `data_sensitivity` | Low / Medium / High / Not available (rubric below) |
| Data minimization | `data_minimization` | Yes (Partial) / Not discussed |
| Data retention policy | `data_retention_policy` | Textual |
| Data sharing / release | `data_sharing` | Textual |
| Jurisdiction / legal | `jurisdiction_legal` | Textual |
| Containment & harm prevention | `containment_measures` | Textual |
| Deception framing | `deception_framing` | Purely technical / Ethical discussion / Not available |
| Researcher responsibility | `researcher_responsibility` | Textual |
| Ethical gaps / red flags | `ethical_gaps` | Textual |
| Relevance to project | `relevance_to_project` | Textual |
| Deployment context | `deployment` | Textual |

All `*_justification` columns contain direct quotes or precise references to the source material (page numbers, sections or README content).

**Data-sensitivity rubric (deployment-independent).** The level reflects what the honeypot is built to collect, not where it was deployed:

- **High** - credentials, personal or third-party data, or control-system data (ICS / IIoT / Space domains)
- **Medium** - attacker identifiers (IP addresses), sessions, network traffic or malware
- **Low** - nothing identifiable

Each `data_sensitivity_justification` starts with the rubric level and the collected data, and states whether attacker behaviour is captured.

> Note for pandas users: the value `None` (for example in `consent_model` and `doc_level`) is read as missing by default. Use `pd.read_csv(path, keep_default_na=False, na_values=[''])` to keep it as a string.

---

## Qualitative Coding

The `taguette/docs/` folder contains 239 plain-text documents, one per dataset entry, prepared for open coding in [Taguette](https://www.taguette.org).

Coding was done in two rounds:

1. **Dataset round (2026-10-25)** - coding of the dataset justifications (`*-open-coding-2026-10-25.sqlite3`).
2. **Final round (2026-11-16)** - coding of the full paper PDFs and of each tool's collected documentation (README, docs folder, wiki and project website): `scientific-pdf-coding-final-2026-11-16.sqlite3` and `ns-tool-documentation-final-2026-11-16.sqlite3`. Dataset v3 / v3.1 values were aligned with this round.

`taguette/codebook.csv` holds the **69 open codes**, grouped as follows:

| Group | Example Codes |
|---|---|
| IRB / Oversight | `IRB-Absent`, `IRB-Present`, `Ethics-Committee` |
| Consent | `Consent-None`, `Consent-Implicit`, `Consent-Explicit`, `User-Notification-Absent` |
| Data Collection | `Credential-Collection`, `Session-Recording`, `Malware-Capture`, `ICS-Data-Capture`, `Medical-Data-Risk` |
| Data Governance | `Data-Retention-Absent`, `Data-Minimization-Absent`, `Data-Sharing-Third-Party`, `Data-Sharing-Controlled` |
| Privacy | `GDPR-Concern`, `IP-Address-Privacy`, `Consumer-Privacy`, `Privacy-Risk` |
| Legal & Jurisdiction | `Jurisdiction-Absent`, `Jurisdiction-Present`, `Radio-Frequency-Regulation` |
| Containment & Harm | `Containment-Absent`, `Containment-Active`, `Containment-Gap`, `Real-Backend-Risk`, `Third-Party-Harm` |
| Deception Ethics | `Deception-Technical-Only`, `Deception-Ethical-Discussion`, `Active-Deception`, `LLM-Deception` |
| Researcher Responsibility | `Researcher-Responsibility-Absent`, `Researcher-Responsibility-Present`, `Responsible-Disclosure` |
| AI & Automation | `LLM-Third-Party-API`, `AI-Governance-Absent`, `Automated-Response` |
| Deployment Context | `Internet-Facing-Deployment`, `Critical-Infrastructure-Deployment`, `Consumer-Distribution`, `Simulation-Only` |
| Domain-Specific | `ICS-Ethics-Absent`, `Healthcare-Ethics-Absent`, `Space-Ethics-Absent`, `IoT-Ethics-Absent` |

---

## Domains Covered

| Domain | Entries | Example entries |
|---|---|---|
| **IT** | 192 | Cowrie, HoneyGPT, HoneyWin, LLMHoney |
| **ICS** | 19 | HoneyPLC, ICSLure, LLMPot, HoneyICS |
| **CPS** | 9 | TwinPot, Cyber-Twin based honeypot, AIIPot |
| **IoT** | 6 | HoneyIoT, SweetCam |
| **Industrial IoT (IIoT)** | 1 | SAGE |
| **Space** | 1 | HoneySat |
| **UAV** | 1 | UAV active-defense honeypot |
| **Other** | 10 | medpot (HL7/FHIR), dicompot (DICOM), Shadow Daemon |

---

## Quick Start

### Requirements

```bash
pip install -r requirements.txt
```

### Load the dataset

```python
import pandas as pd

df   = pd.read_csv('dataset/honeypot_ethics_dataset.csv', low_memory=False)
sci  = df[df['source_type'] == 'Scientific']
nons = df[df['source_type'] == 'Non-Scientific']

print(f"Total: {len(df)} | Scientific: {len(sci)} | Non-Scientific: {len(nons)}")
print(df['domain'].value_counts())
print(df['irb_mentioned'].value_counts())
```

### Run the notebooks

The notebooks read `../dataset/honeypot_ethics_dataset.csv`, so start Jupyter from the `analysis/` folder:

```bash
cd analysis
jupyter notebook honeypot_ethics_analysis_v2.ipynb
```

`honeypot_ethics_analysis_v2.ipynb` (current) produces 21 figures in a paper style (matplotlib, serif font, column and full-width sizes). Set `SAVE_FIGS = True` to write each figure to `figures/` as PDF and PNG. Sections:

| Section | Analysis |
|---|---|
| 1 | Composition: domain and interaction level |
| 2 | Ethics governance discussion rate across 9 dimensions (paper figure 1) |
| 3 | Consent model |
| 4 | Data sensitivity and attacker behaviour (paper figure 2) |
| 5 | Containment and data sharing (paper figure 3) |
| 6 | Data minimization, retention and deployment |
| 7 | Open-source tools: documentation quantity (paper figure 4, candidate) |
| 8 | Interaction level vs data sensitivity |
| 9 | Non-IT domains (ICS, CPS, IoT / IIoT, Space, UAV) |
| 10 | Summary table and five key results |

`honeypot_ethics_analysis.ipynb` is the earlier version (uses seaborn); it is kept until v2 is approved.

### Browse the taxonomy

```bash
cd taxonomy
python -m http.server 8000
```

Then open http://localhost:8000. See [taxonomy/README.md](taxonomy/README.md) for the database tables and how to rebuild it.

---

## Key Findings

Based on dataset v3.1 (38 papers, 201 tools). Counts describe what papers and tool documentation report, not what authors did in practice.

- **IRB / ethics committee**: mentioned by 2 of 38 papers and by no tool documentation.
- **Consent**: only 1 of 38 papers (HoneySat) gives any attacker-facing notice (an "authorized use only" banner, coded Implicit); all other papers and all tools obtain no consent.
- **Data sensitivity**: 24 of 38 papers and 89 of 201 tools collect High-sensitivity data under the deployment-independent rubric.
- **Data governance**: 4 papers and 4 tools state any (partial) data minimization; no paper states a retention policy.
- **Containment**: 9 of the 25 papers with an Internet-facing deployment describe no containment.
- **Responsibility and deception**: researcher responsibility is explicit in 6 of 38 papers and 19 of 201 tools; deception is discussed as an ethical issue in 1 of 38 papers and in no tool.
- **Open-source practice**: 27 tools share collected data with third parties, and 122 of 201 tools have minimal or no documentation.

---

## Data Collection Methodology

### Scientific Papers

- Source: Systematic literature search across IEEE Xplore, ACM Digital Library, USENIX, Springer, and arXiv
- Filter: Only papers proposing, implementing, or deploying an actual honeypot system (not purely detection, evaluation, or survey papers)
- Coverage: Papers from 2013-2026, spanning IT, ICS, CPS, Space, and CAV domains

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