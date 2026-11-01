# AI-Assisted Automated Compliance Checker

### Exploring BIM, IFC and Large Language Models for UK Building Regulation Compliance

A research prototype investigating how **Building Information Modelling (BIM)** and **Large Language Models (LLMs)** can assist architectural compliance checking.

Developed as part of an MSc Artificial Intelligence for Engineering and Design placement project, this workflow combines Python, IfcOpenShell and Google Gemini to explore automated rule extraction and preliminary accessibility checks against **Approved Document M, Volume 2, Section 5**.

## Project Overview

Building regulation compliance checking is traditionally performed manually, requiring architects to interpret regulatory documents and compare requirements against drawings and BIM models.

This project investigates whether parts of this process can be supported by combining:

1. **BIM data extraction:** Reading IFC building elements and properties with IfcOpenShell.
2. **Rule-based compliance checks:** Applying preliminary Python checks to measurable model attributes and derived geometry.
3. **AI-assisted rule extraction:** Using Google Gemini 2.5 Flash to convert regulatory text into structured JSON rules.
4. **Rule-to-BIM mapping:** Linking selected regulatory requirements to available IFC information and identifying where manual review remains necessary.

## Technologies Used

- Python
- IfcOpenShell
- pandas and openpyxl
- pypdf
- Google Gemini API (Gemini 2.5 Flash)
- Jupyter Notebook
- Autodesk Revit (IFC export)

## Repository Structure

```text
automated-compliance-checker/
├── docs/
│   └── rule_extraction_prompt.txt
├── notebooks/
│   ├── 01_IFC_Exploration.ipynb
│   └── 02_PartM_Rule_Extraction.ipynb
├── src/
│   ├── read_ifc.py
│   └── test_setup.py
├── tools/
│   └── create_partm_visuals.py
├── .gitignore
├── requirements.txt
└── README.md
```

The original case-study BIM model, project-derived outputs and other confidential practice information are intentionally excluded.

## Methodology

### 1. IFC Exploration

An architectural Revit model was exported to IFC and inspected using Python and IfcOpenShell.

The workflow explored IFC spaces, doors, geometric information and sanitary-related building elements to determine what information could support compliance checking.

### 2. Preliminary Compliance Checks

Python was used to investigate object-based and dimension-based checks.

The prototype included:

- Door width inspection.
- Identification of accessibility-related rooms.
- Approximate room dimension extraction using IFC geometry.
- Simplified minimum-dimension checks.
- Exploration of sanitary fittings and accessibility equipment.

Bounding-box dimensions were used as a preliminary geometric proxy and do not establish actual wheelchair turning clearance or regulatory compliance.

### 3. AI-Assisted Regulatory Rule Extraction

Approved Document M, Volume 2, Section 5 was processed using Python's `pypdf` library.

Relevant regulatory text was supplied to Google Gemini 2.5 Flash using a structured extraction prompt.

The model generated **34 structured rules** in JSON format, including information about the regulatory reference, requirement, relevant space types, IFC entities, check types and potential for automation.

The rules were compared with an initial manually prepared rule table.

### 4. Rule-to-BIM Mapping

Five selected regulatory rules were mapped to prototype IFC checks.

The mapping distinguished between preliminary automated results, partial checks and requirements needing professional review.

This stage demonstrated that extracting a regulatory requirement does not necessarily mean the BIM model contains sufficient information to verify it.

## Key Findings

- IFC can provide structured building information for selected preliminary accessibility checks.
- Object-based and measurable checks are more straightforward to automate than complex spatial requirements.
- Gemini supported rule discovery and conversion of regulatory text into structured data.
- BIM naming conventions, object classification and missing property information affect checking reliability.
- Diagram-based accessibility requirements and detailed spatial clearances require further development and professional judgement.

## Getting Started

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Provide your own IFC model

Create a local `data/ifc/` directory and place an IFC model named `sample_model.ifc` inside it.

The original case-study IFC model is not distributed.

### 3. Download Approved Document M

Download **Approved Document M, Volume 2: Buildings other than dwellings**, using the relevant edition and amendments, from the [official UK Government website](https://www.gov.uk/government/publications/access-to-and-use-of-buildings-approved-document-m).

Save the PDF locally as:

`docs/Approved_Document_M_Volume_2.pdf`

### 4. Configure the Gemini API key

Set the `GEMINI_API_KEY` environment variable in your local environment.

Never commit API credentials to GitHub.

### 5. Explore the notebooks

Open the notebooks in the `notebooks/` directory and run them using a suitable local Python environment.

The workflow depends on the structure and completeness of the supplied IFC model, and results may vary between models.

## Limitations

This is an experimental research prototype, not a certified compliance assessment system.

The implementation does not perform full spatial clearance verification, automated interpretation of regulatory diagrams or comprehensive validation of all Approved Document M requirements.

Any results produced by the workflow require professional review before use in architectural design decisions.

## Confidentiality

This repository contains research code and methodology only. Confidential BIM models, original case-study datasets and identifying project information are not distributed. The architectural practice is acknowledged as the professional placement context.

## Future Development

Potential improvements include better IFC semantic classification, spatial geometry analysis, diagram interpretation, validation of AI-extracted rules and comparison with direct Revit API data extraction.

## Disclaimer

This project is intended for academic research and exploratory decision support. It does not establish statutory building regulation compliance and is not a substitute for professional judgement.
