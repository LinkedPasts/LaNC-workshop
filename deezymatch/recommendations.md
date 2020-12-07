# How to adapt DeezyMatch for your project

## Tips and recommendations

DeezyMatch can be a powerful tool for candidate ranking, if used appropriately: if used incorrectly, it can hinder rather than help. Knowing the best settings is not always easy and requires testing different options and knowing your data and resources well.

To support new users, we have been collecting some recommendations of those components that can make a huge impact on the performance of DeezyMatch in downstream tasks. You will find below a series of suggestions to make the most out of our tool. We are aware that it may not always be possible to follow all the suggestions. We have tested DeezyMatch extensively in English and Spanish, but very little on other languages. We would be very happy if this document could be expanded with additional tips and pieces of advice you have learned while using DeezyMatch in your research.

### Creating toponym matching training datasets

A DeezyMatch model is trained to capture transformations present in the input data, and therefore your training dataset should reflect your expected linking as much as possible. The toponym matching training dataset can have a big impact on the performance of DeezyMatch.

A toponym matching training dataset consists of positive- and negative-matching string pairs. There are several ways that these can be created. 
> [In this directory](https://github.com/LinkedPasts/LaNC-workshop/tree/main/deezymatch/create_topmatching_dataset) we provide the code to generate a WikiGazetteer (that is, a gazetteer generated from Wikipedia entries with coordinates), and build from it a toponym matching training set for DeezyMatch.
> 
> See some examples of toponym matching training sets [here](https://github.com/LinkedPasts/LaNC-workshop/tree/main/deezymatch/dataset).

These are our recommendations:
* The size of the dataset will have an impact in the accuracy of the resulting DeezyMatch model. We recommend a dataset of at least 50,000 rows if possible (i.e. 25,000 positive pairs and 25.000 negative pairs). However, you should also be aware that an unnecessarily large dataset may take unnecessarily long to train.
* The dataset should have the same number of positive and negative pairs.
* Ideally, there should be negative pairs that are trivial (for example, `Guadiana` and `Valle de Mudá`, which are clearly different) and negative pairs that are challenging (for example, `Guadiana` and `Guadiamar`, which are quite similar). Ideally, there should be positive pairs that are quite similar and even exact (for example, `Guadiana` and `Guadiana`) and positive pairs that are more distant (for example, `Guadiana` and `Uadi Anna` or `Río Guadiana`). This combination of trivial/challenging negative matchings and trivial/challenging positive matchings will ensure that more nuanced transformations are learned, while at the same time DeezyMatch does not get too carried away with learning new transformations.
* The dataset provided [here](https://github.com/ruipds/Toponym-Matching/tree/master/dataset) consists of 5M rows (2.5M positive pairs and 2.5M negative pairs), with toponyms from around the world and in multiple languages and alphabets. If you want to use DeezyMatch for transliteration transformations or you want to have a generic DeezyMatch model, this is the optimal dataset to use. However, if your use case is more specific, we would suggest narrowing it down, to the extent possible:
    > For example:
    > If your project is on linking toponyms from a [17th Century Argentinian dataset in Spanish](https://arounddh.org/en/la-argentina-manuscrita), DeezyMatch will be more accurate if the training dataset has been narrowed down to alternate names obtained using a Spanish resource, such as the Spanish version of Wikipedia, or even narrowed down geographically, by selecting, for example, toponyms of entities located in Latin America. Keep in mind that narrowing it down too much may result in a dataset that is too small.
* Make sure you don't have empty strings (['', 'Firenze', 'True']): you may get an error.
* Try to avoid duplicates (including reverse duplicates such as ['Florence', 'Firenze', 'True'] and ['Firenze', 'Florence', True']).

### DeezyMatch input file

DeezyMatch was designed with flexibility in mind, and to be adaptable to the characteristics and requirements of different projects.

Main decisions can be configured in an input file without requiring the user to modify the code. The values that can be configured are related to:
* Training decisions and fine-tuning (neural network architecture, hyperparameters, etc)
* Preprocessing decisions
* Computing device selection
* Data splitting (training, validation, and evaluation)

In our DeezyMatch repository, we provide an [input file](https://github.com/Living-with-machines/DeezyMatch/blob/master/inputs/input_dfm.yaml) filled with default parameters based on our experiments. However, these may not be the best performing parameters for your scenario. 

For example:

> * By default, the `lowercase` parameter is True. It may be the case that you want to distinguish between upper and lower case, in which case you should set it to False.
> 
> * Tokenization is the process of separating a piece of text into smaller units called tokens, which can be words, characters, or subwords (n-grams). By default, the value of `gru_lstm/mode/tokenize` is `[char]`. This means that the toponym is represented in terms of these characters, which is relevant if we want to learn character-level transformations (i.e. "Firenze" becomes "F", "i", "r", "e", "n", "z", "e"). We may want to preserve word-level tokens as units (i.e. "Yelvertoft and Stanford Park railway station" becomes "Yelvertoft", "and", "Stanford", "Park", "railway", "station"), or use n-grams as a middle ground. **DeezyMatch allows you to have more than one tokenization mode.** For example, if you want to tokenize by both character and word, the value of `gru_lstm/mode/tokenize` should be `[char,word]`.

### Formatting candidate and query input

Both input files for candidates and queries have the following **tab-separated format**:

```
Bedfordshire	0	false
Buckinghamshire	0	false
Cambridgeshire	0	false
Cheshire	0	false
Cleveland	0	false
Cornwall	0	false
Cumbria	0	false
Derbyshire	0	false
```

In the **queries input file**, the first column lists the queries (i.e. the toponyms to be linked, such as 'Ashton-cnder-Ltne').

In the **candidates input file**, the first column lists the candidates (i.e. all the alternate names in a gazetteer, which DeezyMatch will rank according to their vector similarity with the query vector, such as 'Ashton-under-Lyne' given the query 'Ashton-cnder-Ltne').

In both files, the second and third column are currently dummy columns, but they are required: you will get an error if one of the columns is missing. This is a known issue, and we plan to change this in a future version of DeezyMatch. 
> To avoid issues with special characters, one way to create a three-columned `.tsv` is using google spreadsheets to add the dummy columns (fill them with `0` and `false` respectively), and save as a `.tsv` (`File > Download > Tab-separated values (.tsv, current sheet)`).

See here examples of [candidate scenarios](https://github.com/LinkedPasts/LaNC-workshop/tree/main/deezymatch/candidate_scenarios) and of [query scenarios](https://github.com/LinkedPasts/LaNC-workshop/tree/main/deezymatch/query_scenarios).

### Candidate ranking parameters

A DeezyMatch model is used to generate vectors for the input quer(y/ies) and the candidates, and the candidate ranker component ranks the candidates according to their vector similarity with the query vector. There are several parameters that can affect the ranking of the candidates for a given query. They are explained in detail in the documentation [here](https://github.com/Living-with-machines/DeezyMatch/#candidateranker) and [here](https://github.com/Living-with-machines/DeezyMatch/#tips--suggestions-on-deezymatch-functionalities). The optimal thresholds may vary depending on your linking scenario.
