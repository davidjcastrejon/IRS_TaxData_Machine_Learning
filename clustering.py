import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize variables
svd = None
tfidf_pc = None
tfidf_km = None

# Open desc.csv and make corpus a list of strings from desc.csv
with open('/Users/davidcastrejon/Documents/Projects/Clustering/desc.csv') as f:
    corpus = f.readlines()

# Create tf-idf sparse matrix
tf = TfidfVectorizer()
tfidf = tf.fit_transform(corpus)
print("Dimensions of sparse tf-idf matrix: " + str(tfidf.shape))

# Matrix reduction with Principal Components
def pcomponents(dimensions, matrix):
    svd = TruncatedSVD(dimensions, random_state = 230)
    svd.fit(matrix)
    pc = svd.transform(matrix)
    print("Dimensions of truncated matrix: " + str(pc.shape))
    plt.scatter(range(dimensions), np.cumsum(svd.explained_variance_ratio_))
    plt.xlabel('Number of dimensions')
    plt.ylabel('Proportion of variance explained')
    plt.show()

# K-means clustering
def kmeans(clusters, matrix):
    if clusters > 10:
        print("You inputted more than 10 clusters. Number of clusters has been reset to 10.")
        clusters = 10
    svd2 = TruncatedSVD(2, random_state = 230)
    reduced = svd2.fit_transform(matrix)
    km = KMeans(clusters, random_state = 500000)
    tfidf_km = km.fit_predict(reduced)

    # Print 5 descriptions from each cluster
    for i in range(clusters):
        descriptions = []
        counter = 0
        print("5 descriptions in cluster #" + str(i + 1))
        for j in range(len(corpus)):
            if tfidf_km[j] == i and counter < 5:
                descriptions.append(corpus[j])
                counter += 1
        for k in range(5):
            print(descriptions[k])

    # Plot up to 10 clusters
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'gray', 'orange', 'purple']
    plt.figure()
    for i in range(clusters):
        plt.scatter(reduced[tfidf_km == i, 0], reduced[tfidf_km == i, 1], c=colors[i], label='Cluster {}'.format(i + 1))
    plt.title('KMeans Clustering')
    plt.legend(loc='upper right')
    plt.show()

print("Analysis:"
      "It appears that roughly the first 1000 principle components show most of the variance in the data."
      "After 1000 principal components, the graph levels out more and less variance is explained with more"
      "principal components. The graph also appears to be logarithmic in nature. About 1400 principle"
      "components are necessary to represent 50% of the total variation in the data. The clustering appears"
      "to be working very well. The clusters are well spaced and there is not one cluster dominating the "
      "scatter plot. Each cluster is well made with k values ranging from 2 to 10.")

# To generate k-means clustering plots, call this method replacing k with a value from 1-10
# kmeans(k, tfidf)

# To calculate the amount of variance explained with p principal components
# pcomponents(p, tfidf)







