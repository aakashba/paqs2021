# Question Answering system for sub-routines

## Stage 0 - Programmer Assisted QA Synthesis (PAQS) - Data Synthesis 

We use data from from the funcom dataset of 2.1m filtered java methods
(Their raw data was downloaded from: http://leclair.tech/data/funcom/)

The data was then processed in qasynth.py file using the following datasets :
1. srcml funcom files
2. pre-filtered file created during this project that removed function ids with duplicate and some bad comments -- goodcoms.pkl

Due to github data limations the dataset with these data files processed in the python scripts can be found here :
```
s3://paqs2020/paqs2020.zip
```
after downloading the dataset zip, unzip it, all the python files are also included in the folder paqs2020. To recreate the datset synthesized in qasynth.py just run 

```
python3 qasynth.py
```
