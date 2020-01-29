# Question Answering system for sub-routines

## Stage 0 - Programmer Assisted QA Synthesis (PAQS) - Data Synthesis 

We use data from from the funcom dataset of 2.1m filtered java methods
(Their raw data was downloaded from: http://leclair.tech/data/funcom/)

The data was then processed in qasynth.py file using the following datasets :

1. srcml funcom files - /srcmldat/.
2. pre-filtered file created during this project that removed function ids with duplicate and some bad comments -- goodcoms.pkl
3. set of paraphrases written to serve as tempelate for questions - questions.pkl 

Due to github data limations the dataset with these data files processed in the python scripts can be found here :
```

```
after downloading the dataset zip, unzip it, all the python files are also included in the folder paqs2020. To recreate the datset synthesized in qasynth.py just run 

```
python3 qasynth.py
```
The files context.pkl and qatypeA.pkl will be placed in qadatasetKstudy.

There are several python files in my main git/directory that can process the data including tokenization and train-test-val splits to recreate the format required by the funcom model from LeClair et al.

This has already been done and all data exists with qadatasetKstudy/output if you do not wish to recreate.

## Stage 1 - Training the data 
To train the model please make sure to create a child directory as qadatasetKstudy/outdir/models , then in /paqs_dev/ run 
```
time python3 train.py --model-type=ast-attendgru --gpu=X --batch-size=50
```
X is replaced by your gpu number here. The model takes 15 gigs of space on a P5000 GPU at batch size 50 for 2 days per epoch, you can adjust the batch size up or down according to your GPU availability. This was made possible only because we use ~1% of the required vocabulary size to train this model, a full vocabulary size does not fit on a single gpu even at batch size 1. Vocabulary size can be changed in tokenru.py when recompiling the dataset. 

We already have the model trained to 10 epochs in the dataset zip dowloaded if you wish to use those. Also each epoch's result is saved as a checkpoint standalone model.

## Stage 2 - Predictions 
To get predictions of the 67k test split created, simply run this script from paqs_dev as well after training
```
time python3 predict.py /qadatasetKstudy/outdir/models/ast-attendgru-EZZ-YZY.h5 --gpu=X
```
Here X is replaced by the GPU number, ZZ is replaced by the epoch number of the model you wish to use for predictions, and YZY is replaced by the time stamp of when the model started training ( found in outdir/models directory after training or using our existing trained models)

You can also repurpose the prediction script to predict using user provided question and base context as we do in the user study (script is not provided as it is web hosted in another format, a link to the interface is below ) 

## Stage 3 - User Study Data
The data aquired by the user study monitored by us is available in raw text format in ftagged.txt
The format is as follows :-
```
User: Subject1
Function: fid#
QueryQ : < insert question here > ( for eg. What is the return type?)
Reponse : < answer from the model prediction> (for eg. the return type for this method is void)
Rating 1: p
Rating 2: p
Rating 3: p
Rating 4: p
```
Here Q is replaced by the type of question they asked, which is manually tagged and is plain Query for questions that are not relevant to the study parameters such as greetings and banter. The 4 ratings are the Quality prompts P1-P4 in the paper 
```
Rating 1 = Relevance | Rating 2 = Accuracy | Rating 3 = Completeness | Rating 4 = Concision
```
Grades 'p' are placeholder for prompts rated by study participants are  as 
```
sa = strongly agree | a = agree | sd = strongly disagree | d = disagree | u = unsure/neutral/cannot decide
```
## Stage 4 - Stats calculated for the paper
Before calculating the stats please run make_pkl.py to separate each participant for iterative processing. The scripts that calculate the stats are available in the calculations directory as two distinct scripts 
1.stats.calc.py - Thresholded calculation where for P1 and P2 only 'sa' and 'a' are considered a positive result while neutral and disagreements are given to the negative hence using a highly conservative approach.
2.stats_raw.py - bare calculation of grades from 1 = strongly agree to 5= strongly disagree weights assigned to each rating.

## Stage 5 - Activations
There are additional activations inside the activations directory with text files offering explanation of what is seen in the activations, this is as an appendix to the one activation we show in the paper for concision. You can also generate activations for any function id ( we suggest only the test set)  by running the following command in paqs_dev 
```
time python3 my_get_activations.py /qadatasetKstudy/outdir/models/x.h5 /qadatasetKstudy/outdir/models/y.h5 --fid=zzz
```
Here x replaced one epoch model while y replaces the other. You may pass the same epoch to both as this script was built for comparison purposes. 
