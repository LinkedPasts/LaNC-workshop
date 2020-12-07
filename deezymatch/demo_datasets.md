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


### Pre-trained DeezyMatch model is provided in `./models/wikigaz_en_brit` for:

* Pre-trained on the alternate names of locations in the British Isles, extracted from the English version of Wikipedia.
See https://github.com/Living-with-machines/lwm_GIR19_resolving_places/tree/master/gazetteer_construction

### Further training data is provided in `./dataset` for:

* British Library IAMS place names matched to Geonames
This could be used to create a new model or for fine-tuning wikigaz_en_brit.


Thanks to Alan Turing Institute, British Library, Historic Environment Scotland and Historic England for the datasets.

Contains Historic Environment Scotland and Ordnance Survey data © Historic Environment Scotland - Scottish Charity No. SC045925 © Crown copyright and database right 2020

© Historic England 2020. Contains Ordnance Survey data © Crown copyright and database right 2020 The Historic England GIS Data contained in this material was obtained on 28/8/20. The most publicly available up to date Historic England GIS Data can be obtained from http://www.HistoricEngland.org.uk.
