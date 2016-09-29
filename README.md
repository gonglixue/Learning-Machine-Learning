# Learning-Machine-Learning
some exercise for learning machine learning

## 1.Hierarchical Clustering for 25 English Articles
This program uses "word vectors" to count the words in an article. And by calculating the [Pearson Correlation Score](https://en.wikipedia.org/wiki/Correlation_and_dependence) of two vectors to judge the closeness between two clusters. In every loop, the function will find the best matching clusters and merge them into a new cluster. This process will repeat until there is only one cluster left. Finally we can generate a picture of [dendrogram](https://en.wikipedia.org/wiki/Dendrogram) to represent the hierarchical clustering by usint [PIL](http://pythonware.com/products/pil/).
