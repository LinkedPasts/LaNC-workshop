# DeezyMatch Tutorial @ LinkedPasts6

## Useful links

* [DeezyMatch github repo](https://github.com/Living-with-machines/DeezyMatch)
* Instructions for using DeezyMatch can be found [here](https://living-with-machines.github.io/DeezyMatch/).
* Models/datasets are stored [in a sharepoint folder.](https://thealanturininstitute-my.sharepoint.com/:f:/g/personal/mcollardanuy_turing_ac_uk/Eo20kXuHZFhMpBC3Tvg_CGEBwpCSO76jHGPE7eQFFItuOQ?e=6RaGZN)
*

## Monday hands-on session

- Talk about the other tutorials (Gethin)
- Motivation (Katie)
- Demo 1: How to use the candidate ranker (uses a realistic model), Binder
- Architecture and main functionalities (Kasra), datasets/inputs
- Demo 2 (hands-on): Train a model (pair classifier) from scratch using 100/1000-row dataset
- **How to adapt DeezyMatch, Tips (Mariona)**, 20mins before the end
- (Demo 3: Provide a realistic dataset and notebook with outputs)
- Other datasets (Gethin)

- Introduction (10min), Katie, Kasra
    - Motivation, architecture and main features. [Link to the presentation.](https://docs.google.com/presentation/d/14wRL9vGIfNc_xHa4gR_I5hL9_ChVHDacfXUQ6DLeKP0/edit?usp=sharing)

- If we have time:
- DeezyMatch main functionalities, hands-on session (20min)
- Install DeezyMatch
      - Beginning user setup (basic model): use [the Binder link](https://mybinder.org/v2/gh/Living-with-machines/DeezyMatch/HEAD?filepath=examples)
      - Advanced user setup (to train your own model and use your own data): install on your local machines  
    - Follow DeezyMatch's tutorial [here](https://living-with-machines.github.io/DeezyMatch/) for local install instructions an explanation of the notebook.
    - Download a new dataset from [the sharepoint folder](https://thealanturininstitute-my.sharepoint.com/:f:/g/personal/mcollardanuy_turing_ac_uk/Eo20kXuHZFhMpBC3Tvg_CGEBwpCSO76jHGPE7eQFFItuOQ?e=6RaGZN) and train a realistic model from scratch.
        - XXX can we have a real deezymodel, and one that we build on the fly, and the same for the candidates file, one that we use to show how good resuls we get, and one so that they can see how it's used? I can prepare them.
- Real case toponym matching application (30min)
    - Input file: options and recommendations.
    - How to prepare a training dataset for DeezyMatch.
    - Dataset for fine-tuning, and options.
    - How to format candidates and queries.
    - Ranking options and recommendations.


# DeezyMatch demo datasets

Living with Machines have provided datasets ???
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
