## Capstone Project: Create a Customer Segmentation Report for Arvato Financial Services
##### by Markus Müller

This is the last project from the Udacity Data Scientist Nanodegree.
The first goal of this project is to perform an unsupervised learning algorithm to uncover differences between customers and the general population. The second goal was to perform a supervised learning algorithm to predict if an individual became a customer and the last goal was to use the trained model to predict on unseen data and upload the results to Kaggle.

Link to <a href='https://medium.com/@markusmller_92879/udacity-data-scientist-nanodegree-capstone-project-using-unsupervised-and-supervised-algorithms-c1740532820a'>Medium article</a> 


### Content of the Notebook
1. Part 0: Get to know the data
    - data cleaning
2. Part 1: Customer Segmentation Report
    - PCA to reduce the features
    - KMeans to cluster the data
3. Part 2: Supervised Learning Model
    - Tested different binary classification alforithms 
    - Hyperparameter tuning
    - final model= GradientBoostingClassifier
4. Part 3: Kaggle Competition
    - used final model to make predictions
    - uploaded prediction to Kaggle
        
### Limitations
My final score is compared to others on Kaggle relatively low. I looked at a few other notebooks on github to get an idea why. It seems that my approach, to only keep the columns that are in the dataset and in the excel file is quite unique. To recap, I dropped 94 columns that weren't in both files, with the idea that I can only use attributes for which I have the description. After the analysis I inspected the excel file and noticed that some Attributes are just spelled differently between the excel file and the dataset. So, all in all I probably dropped some columns that meight would increase my score.

Another thing that I noticed is that I dropped rows in the supervised learning part. Which is debatable because the variable of interest is highly imbalanced and one can argue that it would be better to keep rows with missing values, so that there is a higher chance for the imbalanced value to appear.

#### All in all, here are some things that could be checked to enhance the final score:
- get a better understanding of the attributes and check if you can use more attributes without dropping them (keep attributes with more than 10 items)
- don't drop attributes because they aren't in the Excel file
- use more advanced methods to impute missing values (imputations based on distributions ore even use a learning algorithm to predict the missing value)
- use more advanced techniques to deal with imbalanced data (resampling to get more balanced data, weighted classes / cost sensitive learning).

### Libraries
- numpy
- pandas
- marplotlib
- slearn
