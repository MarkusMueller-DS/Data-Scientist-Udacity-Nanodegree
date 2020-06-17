## Capstone Project: Create a Customer Segmentation Report for Arvato Financial Services
##### by Markus Müller

This is the last project from the Udacity Data Scientist Nanodegree.
The first goal of this project is to perform an unsupervised learning algorithm to uncover differences between customers and the general population. The second goal was to perform a supervised learning algorithm to predict if an individual became a customer and the last goal was to use this trained model to predict on unseen data and upload the results to Kaggle.

### Content of the Notebook
1. Part 0: Get to know the data
    - data cleaning
2. Part 1: Customer Segmentation Report
    - PCA to reduce the features
    - KMeans to cluster the data
3. Part 2: Supervised Learning Model
    - Tested different binary classification alforithms 
    - Hyperparameter tuning
    - final model= GradientBoostingClassifier()
4. Part 3: Kaggle Competition
    - used final model to make predictions
    - uploaded prediction to Kaggle
        
### Limitations
My final score is relatively low, compared to others on Kaggle. I looked at a few other notebooks on github to get an idea why. It seems that my approach to only keep the columns that are in the dataset and in the excel file is quite unique. To recap, I dropped roughly 100 columns that weren't in both files, with the idea that I can only use attributes for which I have the description. After the analysis I inspected the excel file and noticed that some Attributes are just spelled differently between the excel file and the DataFrame. So all in all I probably dropped some columns that would increase my score.

### Libraries
- numpy
- pandas
- marplotlib
- slearn
