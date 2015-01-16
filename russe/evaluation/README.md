Running evaluation script 
--------------------

This are instructions are for Ubuntu Linux, but the script should work well on Mac OSX and Windows as well (just install required dependencies). 


1. Clone the git repository:

    ```
    git clone https://github.com/nlpub/russe-evaluation.git
    ```

2. Install dependencies:

    ```
    sudo apt-get install python-numpy python-scipy python-pandas python-matplotlib python-sklearn
    ```

3. Go to the evaluation directory:

    ```
    cd ./russe-evaluation/russe/evaluation
    ```

4. Calculate similarities for the test.csv file (fill the sim column of the test.csv file).

5. Run the evaluation:

    ```
    ./evaluation_test.py test-sample.csv
    ./evaluation_test.py ~/path/to/your/test.csv
    ```

Results of the evaluations are printet to stdout. Most essential metrics are also printed to stderr. You should see something like this:


```
~/russe-evaluation/russe/evaluation$ ./evaluate_test.py ~/test.csv 
test.csv: /home/ubuntu/test.csv
golden standard: ./hj-test.csv
test.csv: /home/ubuntu/test.csv
not found 49 of 64
used 15
golden standard + test.csv: /home/ubuntu/hj-test-usim.csv 

golden standard: ./rt-test.csv
test.csv: /home/ubuntu/test.csv
not found 100744 of 104517
used 3773
golden standard + test.csv: /home/ubuntu/rt-test-usim.csv 

golden standard: ./ae-test.csv
test.csv: /home/ubuntu/test.csv
not found 19616 of 20966
used 1350
golden standard + test.csv: /home/ubuntu/ae-test-usim.csv 

golden standard: ./ae2-test.csv
test.csv: /home/ubuntu/test.csv
not found 75044 of 83769
used 8725
golden standard + test.csv: /home/ubuntu/ae2-test-usim.csv 

=======================================================
Evaluation based on correlations with human judgements
See Section 1.1 of http://russe.nlpub.ru/task

Input file: /home/ubuntu/hj-test-usim.csv
Spearman's correlation with human judgements: 0.28816 (p-value = 0.020)
Pearson's correlation with human judgements:  0.01481 (p-value = 0.907)
=======================================================
Evaluation based on correlations with human judgements
See Section 1.1 of http://russe.nlpub.ru/task

Input file: /home/ubuntu/ae-test-usim.csv
Spearman's correlation with human judgements: 0.28245 (p-value = 0.000)
Pearson's correlation with human judgements:  0.07714 (p-value = 0.000)
=======================================================
Evaluation based on correlations with human judgements
See Section 1.1 of http://russe.nlpub.ru/task

Input file: /home/ubuntu/ae2-test-usim.csv
Spearman's correlation with human judgements: 0.44326 (p-value = 0.000)
Pearson's correlation with human judgements:  0.01980 (p-value = 0.000)

=======================================================
Evaluation based on semantic relation classificaton
See Section 1.2 of http://russe.nlpub.ru/task

predict: /home/ubuntu/rt-test-usim-predict.csv
accuracy: 0.510
average_precision: 0.673
roc_auc: 0.545
             precision    recall  f1-score   support

          0       0.64      0.52      0.58     66791
          1       0.37      0.49      0.42     37727

avg / total       0.54      0.51      0.52    104518

precision-recall plot: /home/ubuntu/rt-test-usim-pr.png

=======================================================
Evaluation based on semantic relation classificaton
See Section 1.2 of http://russe.nlpub.ru/task

predict: /home/ubuntu/ae-test-usim-predict.csv
accuracy: 0.541
average_precision: 0.637
roc_auc: 0.574
             precision    recall  f1-score   support

          0       0.71      0.53      0.61     13978
          1       0.37      0.56      0.45      6989

avg / total       0.60      0.54      0.55     20967

precision-recall plot: /home/ubuntu/ae-test-usim-pr.png

=======================================================
Evaluation based on semantic relation classificaton
See Section 1.2 of http://russe.nlpub.ru/task

predict: /home/ubuntu/ae2-test-usim-predict.csv
accuracy: 0.578
average_precision: 0.741
roc_auc: 0.643
             precision    recall  f1-score   support

          0       0.73      0.57      0.64     55055
          1       0.42      0.59      0.49     28715

avg / total       0.62      0.58      0.59     83770

precision-recall plot: /home/ubuntu/ae2-test-usim-pr.png
hj  rt-avep rt-accuracy ae-avep ae-accuracy ae2-avep  ae2-accuracy
0.28816 0.67329 0.51016 0.63725 0.54075 0.74111 0.57833

```


