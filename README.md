# WikiNews dataset

Data for PLOS ONE 2024 paper [Breaking News: Unveiling a New Dataset for Portuguese News Classification and Comparative Analysis of Approaches](https://journals.plos.org/plosone/)

WikiNotícias (WikiNews) is a news channel, where articles can be created collaboratively.

Code from this project can be used to leverage this data for text categorization studies.


# Dataset construction procedure


1. Download this repository
2. Install requirements.txt
3. Download content from MediaWiki dump service.\
https://dumps.wikimedia.org/ptwikinews/ \
Select "all pages, current versions only" (ptwikinews-YYYYMMDD-pages-meta-current.xml.bz2) \
On referenced paper, we used the the May 1, 2022 file. \
https://dumps.wikimedia.your.org/ptwikinews/20220401/
4. Uncompress file on folder ./content/raw
5. Convert content to json:
```
    python extractor.py \
           --input content/raw/ptwikinews-20220401-pages-meta-current.xml \
           --output content/json/wikinews_full.json 
```
6. Select articles by category removing articles that fall into more than one of the indicated categories.
```
    python seletor.py \
           --input content/json/wikinews_full.json \
           --output content/json/wikinews_categories.json \
           --categories 'Desporto' 'Crime, Direito e Justiça' 'Saúde' 'Economia e negócios' 'Política'
```

7. Split data into train and test. \
This is done in two steps. In the first one, a file containing the message id and part is generated. It is useful to ensure replication.\
In the second step, the generated file is applied to the data set, producing the partitions.\
Our generated file is available on 'content/json/split ids.csv'. To use it, skip the partition file production step (first command in the following box).
```
    python train_split.py \
           --input content/json/wikinews_categories.json \
           --splitfile content/json/split_ids.csv \
           --operation generate

    python train_split.py \
           --input content/json/wikinews_categories.json \
           --splitfile content/json/split_ids.csv \
           --operation apply --train content/json/wikinews_train.json \
           --test content/json/wikinews_test.json
```

