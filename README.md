MOOC-Learner-Curated
---------------------
Translate and curate activities captured from a MOOC learner into a relational database with MOOC-Learner-Curated (MLC)

# Requirements 

<a href="https://www.python.org/" ><img src="https://img.shields.io/badge/Python-blue.svg"></a></a> <a href="https://www.mysql.com/" ><img src="https://img.shields.io/badge/MySQL-blue.svg"></a> 

<a href="https://www.docker.com/" ><img src="https://img.shields.io/badge/Docker-blue.svg"></a> 
(see [MOOC-Learner-Docker/curated_base_img](https://github.com/MOOC-Learner-Project/MOOC-Learner-Docker/tree/master/curated_base_img) )

## Technologies

<a href="https://pandas.pydata.org/" ><img src="https://img.shields.io/badge/Pandas-blue.svg"></a>


# Installation

See [MOOC-Learner-Docker](https://github.com/MOOC-Learner-Project/MOOC-Learner-Docker/tree/master/README.md)

# Tutorial

Entry point is `autorun.py`. Configuration is done with `config/*yml`, see e.g. `config/sample_config.yml`.

Description of MOOC-Learner-Curation execution is in [docs/README.md](docs/README.md)

Two steps of an extension to MLC
- `apipe`: from MySQL db to intermediate CSVs
- `qpipe`: from intermediate CSVs to new MySQL table

If you use data sources other than click-stream, you can follow a simpler track: only `qpipe`

If you rely on features that does not supported by the clickstream `apipe` (e.g. new specifications) you have to add 
patches to `apipe` and debug
 

## Pre-processing Raw Course Files and the Connectors

Course files from open edX servers with different specifications may have different formats. Pre-processing of the raw 
course files and translating them into the correct format is inevitable. Connectors are the pre-processing tools of 
MOOC-Learner-Curated. We do not integrate these into the pipeline of curated since we do not expect curated to identify 
which type of course file it is processing. User should transform the course files in advance of running curated. 
Currently we have to connectors which transform VisMOOC course files and MITx course tables into the `MOOCdb` format. 
