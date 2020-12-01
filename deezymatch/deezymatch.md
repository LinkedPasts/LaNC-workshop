# DeezyMatch demo datasets

Instructions for using DeezyMatch can be found [here](https://living-with-machines.github.io/DeezyMatch/).

Query scenarios are provided in `./query_scenarios` for:

* British Library medieval manuscripts that include locations in the Anglo-Welsh and Scottish borders `./query_scenarios/BL_med_locations.tsv`.
* Historic Environment Scotland Scheduled monuments and World Heritage sites `./query_scenarios/HES_Scheduled_Monuments.tsv`,
`./query_scenarios/HES_World_Heritage_Sites.tsv`
* Historic England Scheduled monuments and World Heritage sites `./query_scenarios/HE_ScheduledMonuments_28Aug2020.tsv`, `./query_scenarios/HE_WorldHeritageSites_28Aug2020.tsv`

Candidate scenario is provided in `./candidate_scenarios` for:

* Wikipedia gazetteer
https://github.com/Living-with-machines/LwM_SIGSPATIAL2020_ToponymMatching
https://zenodo.org/record/4034819#.X8Yx36r7TOQ

* Do we need an extra eg https://geoportal.statistics.gov.uk/datasets/a6c138d17ac54532b0ca8ee693922f10_0

Pre-trained DeezyMatch model is provided in `./models/wikigaz_en_brit` for:

* Pre-trained on the alternate names of locations in the British Isles, extracted from the English version of Wikipedia.
See https://github.com/Living-with-machines/lwm_GIR19_resolving_places/tree/master/gazetteer_construction

Thanks to British Library, Historic Environment Scotland and Historic England for the datasets.

Contains Historic Environment Scotland and Ordnance Survey data © Historic Environment Scotland - Scottish Charity No. SC045925 © Crown copyright and database right 2020

© Historic England 2020. Contains Ordnance Survey data © Crown copyright and database right 2020 The Historic England GIS Data contained in this material was obtained on 28/8/20. The most publicly available up to date Historic England GIS Data can be obtained from http://www.HistoricEngland.org.uk.
