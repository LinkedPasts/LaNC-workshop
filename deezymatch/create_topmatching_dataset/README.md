# Creating a toponym matching dataset

There are different manners to create a toponym matching dataset.

In [`create_training_data.ipynb`](https://github.com/LinkedPasts/LaNC-workshop/tree/main/deezymatch/create_topmatching_dataset/create_training_data.ipynb) we show how to generate a wikigazetteer (that is, a gazetteer generated from wikipedia locations with alternate names), and how to use it to build a toponym matching training set for DeezyMatch.

The resulting dataset will have the following format (tab-separated, one row per line):

Toponym 1 | Toponym 2 | Matching
----------|-----------|---------
Cala Egos | La Fuensanta | False
Cala Egos | Cala Pada | False
Cala Egos | Cala Nova | False
Cala Egos | Cala Egos | True
Cala Egos | Caló de ses Egos | True
Cala Egos | Caló de ses Egües | True

#### Installation

* Install the requirements:

```bash
pip install python-Levenshtein
pip install tqdm
pip install pandas
pip install pathlib
pip install geopy
pip install mysql-connector-python
```

## Alternative approach   

An alternative approach could be to use the toponym matching dataset provided in https://github.com/ruipds/Toponym-Matching, and filter it according to your needs (e.g. only toponyms in certain alphabets, from locations in certain countries, etc). Make sure you have balanced dataset, that is, the same number of positive and negative examples. This dataset, which has 5,000,000 toponym pairs, has the following format:

Toponym 1 | Toponym 2 | Matching | Geonames id 1 | Geonames id 2 | Alphabet 1 | Alphabet 2 | Country 1 | Country 2
--- | --- | --- | --- | --- | --- | --- | --- | --- 
la dom nxy | ลำโดมน้อย | TRUE | 1610905 | 1610905 | LATIN | THAI | TH | TH
Krutoy | Крутой | TRUE | 1501675 | 1501675 | LATIN | CYRILLIC | RU | RU
Sharunyata | Shartjugskij | FALSE | 495626 | 495628 | LATIN | LATIN | RU | RU
Sutangcun | 羊山村 | FALSE | 1552807 | 1552810 | LATIN | CJK | CN | CN
Jowkār-e Shafī‘ | جوکار شفیع | TRUE | 43454 | 43454 | LATIN | ARABIC | IR | IR
