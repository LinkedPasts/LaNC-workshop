# DeezyMatch Tutorial @ LinkedPasts6


## Monday hands-on session schedule

- Introduction (10min), Katie, Kasra
    - Motivation, architecture and main features. [Link to the presentation.](https://docs.google.com/presentation/d/14wRL9vGIfNc_xHa4gR_I5hL9_ChVHDacfXUQ6DLeKP0/edit?usp=sharing)
- Demo 1: How to use the candidate ranker (uses a realistic model), [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LinkedPasts/LaNC-workshop/HEAD?filepath=deezymatch%2Fdemos)
- Architecture and main functionalities (Kasra), datasets/inputs
- Demo 2 (hands-on): Train a model (pair classifier) from scratch using 100/1000-row dataset
- **How to adapt DeezyMatch, Tips (Mariona)**, 20mins before the end

- Demo 3: Provide a realistic dataset and notebook with outputs.
- Real case toponym matching application (30min)
    - Input file: options and recommendations.
    - How to prepare a training dataset for DeezyMatch.
    - Dataset for fine-tuning, and options.
    - How to format candidates and queries.
    - Ranking options and recommendations.

## DeezyMatch demos

To run the demos, you can either:

1. Directly use the Binder link: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/LinkedPasts/LaNC-workshop/HEAD?filepath=deezymatch%2Fdemos)
2. or manually install DeezyMatch on your machines ([see](https://github.com/Living-with-machines/DeezyMatch#installation)) and run the demos on your machine.

- Advanced user setup (to train your own model and use your own data): install on your local machines  
- Follow DeezyMatch's tutorial [here](https://living-with-machines.github.io/DeezyMatch/) for local install instructions an explanation of the notebook.
- Download a new dataset from [the sharepoint folder](https://thealanturininstitute-my.sharepoint.com/:f:/g/personal/mcollardanuy_turing_ac_uk/Eo20kXuHZFhMpBC3Tvg_CGEBwpCSO76jHGPE7eQFFItuOQ?e=6RaGZN) and train a realistic model from scratch.

## Useful links

* [DeezyMatch github repo](https://github.com/Living-with-machines/DeezyMatch)
* Instructions for using DeezyMatch can be found [here](https://living-with-machines.github.io/DeezyMatch/).
* Models/datasets are stored [in a sharepoint folder.](https://thealanturininstitute-my.sharepoint.com/:f:/g/personal/mcollardanuy_turing_ac_uk/Eo20kXuHZFhMpBC3Tvg_CGEBwpCSO76jHGPE7eQFFItuOQ?e=6RaGZN)

# DeezyMatch demo datasets

Living with Machines have provided several datasets.
Locating a National Collection has provided datasets from North Britain.

### Query scenarios are provided in `./query_scenarios` for:

* British Library medieval manuscripts that include locations in the Anglo-Welsh and Scottish borders `./query_scenarios/BL_med_locations.tsv`.
* Historic Environment Scotland, Scheduled monuments from southern Scotland and World Heritage sites `./query_scenarios/HES_Scheduled_Monuments.tsv`,`./query_scenarios/HES_World_Heritage_Sites.tsv`
* Historic England Scheduled monuments from northern England and World Heritage sites `./query_scenarios/HE_ScheduledMonuments_28Aug2020.tsv`, `./query_scenarios/HE_WorldHeritageSites_28Aug2020.tsv`

Although these query scenarios are in the correct format for DeezyMatch they are direct exports from institutional systems. Therefore the strings require some processing or wrangling for effective matching with candidate scenarios. We would be interested in feedback on this process.

### Candidate scenario is provided in `./candidate_scenarios` for:

* Wikipedia gazetteer
https://github.com/Living-with-machines/LwM_SIGSPATIAL2020_ToponymMatching
https://zenodo.org/record/4034819#.X8Yx36r7TOQ

* Do we need an extra eg https://geoportal.statistics.gov.uk/datasets/a6c138d17ac54532b0ca8ee693922f10_0

### Pre-trained DeezyMatch model is provided in `./models/wikigaz_en_brit` for:

* Pre-trained on the alternate names of locations in the British Isles, extracted from the English version of Wikipedia.
See https://github.com/Living-with-machines/lwm_GIR19_resolving_places/tree/master/gazetteer_construction

### Further training data is provided in `./dataset` for:

* British Library IAMS place names matched to Geonames
This could be used to create a new model or for fine-tuning wikigaz_en_brit.


Thanks to Alan Turing Institute, British Library, Historic Environment Scotland and Historic England for the datasets.

Contains Historic Environment Scotland and Ordnance Survey data © Historic Environment Scotland - Scottish Charity No. SC045925 © Crown copyright and database right 2020

© Historic England 2020. Contains Ordnance Survey data © Crown copyright and database right 2020 The Historic England GIS Data contained in this material was obtained on 28/8/20. The most publicly available up to date Historic England GIS Data can be obtained from http://www.HistoricEngland.org.uk.
