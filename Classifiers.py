import numpy as np
import math



class KNN:
    def __init__(self, k):
        self.k = k

    # returns the unique classes found in the neighbors of a class
    def unique_classes(self, X):
        unique = []
        for i in X:
            if i not in unique:
                unique.append(i)
        return sorted(unique)

    # calculates which neighbors have the majority label
    def max_instances(self, neighbors, column):
        max = 0
        neighbor_labels = [t[column] for t in neighbors]
        for i in self.unique_classes(neighbor_labels):
            count = neighbor_labels.count(i)
            if count > max:
                max = count
                best_label = i
        return best_label

    def average_instance(self, neighbors, column):
        aver = 0
        for i in neighbors[column]:
            print(i)
            aver += i
        return aver/len(neighbors)


    def predict_regression(self, train, test, y):
        neighbors = self.find_neighbors(train, test)
        prediction = self.average_instance(neighbors, y)
        return prediction

    def knn_regression(self, train, test, y):
        predictions = []
        for row in test:
            output = self.predict_regression(train, row, y)
            predictions.append(output)
        return predictions

    # predicts what class a new data instance should be applied to
    # by finding the k nearest neighbors then returning the class with the highest number of instances
    def predict_classification(self, train, test, y):
        neighbors = self.find_neighbors(train, test)
        prediction = self.max_instances(neighbors, y)
        return prediction

    # driver function that goes through every row of the test set and designates what class is should go to
    def k_nearest_neighbors(self, train, test,y):
        predictions = []
        for row in test:
            output = self.predict_classification(train, row, y)
            predictions.append(output)
        return predictions

    # calculates the euclidean distance of two vectors
    def distance(self, p1, p2):
        sum = 0
        for i in range(len(p1)-1):
            sum += (p2[i]-p1[i])**2
        return math.sqrt(sum)

    # Returns the k closest neighbors
    def find_neighbors(self, trained, test):
        neighbor = []
        for p in trained:
            dist = self.distance(p, test)
            neighbor.append([p, dist])
        neighbor.sort(key = lambda x: x[1])
        return [neighbor[i][0] for i in range(self.k)]


class Naive_Bayes:
    def __init__(self):
        self.trained = []

    # used to train the data set by separating each data set by label
    # then calculates and stores the variance matrix, the mean, p, and the class label of
    # the class separated data set
    def naive(self, D,col):
        size = len(D)
        y = D[:, col]
        uniq = self.unique_classes(y)
        for i in uniq:
            D_i = self.classes(D, i, col)
            n = len(D_i)
            p = n / size
            size_D_i = len(D_i[0])
            ui = np.array([(1 / n) * sum(D_i[:, j]) for j in range(size_D_i)])
            Z = np.array([(D_i[t] - ui) for t in range(n)])
            var = np.array([np.matmul(Z[:, s].T, Z[:, s]) / n for s in range(size_D_i)])
            self.trained.append(np.array([p, var, ui, i]))

    # calculates c for every new data instance and applies a class label based on the largest value of c
    def predict(self, x):
        max = 0
        max_class = 0
        predicted_class = []
        for i in x:
            for sample in self.trained:
                c = self.predict_helper(i,sample[0], sample[1], sample[2])
                if c> max:
                    max =c
                    max_class = sample[3]
            predicted_class.append(max_class)
            max = 0
            max_class = 0
        return predicted_class


    # returns the value of c
    def predict_helper(self, x, pc, sigma, u):
        c = 1
        for i in range(len(sigma)):
            if sigma[i] == 0:
                return 0
            # calculates c
            c *= (1 / (math.sqrt(2 * math.pi * sigma[i]))) * math.exp((-1 * (x[i] - u[i]) ** 2) / (2 * sigma[i]))
        return c * pc

    # Returns all unique class labels
    def unique_classes(self, X):
        unique = []
        for i in X:
            if i not in unique:
                unique.append(i)
        return unique

    # Seperates the data by their class
    def classes(self, X, y, col):
        c = []
        for i in X:
            if i[col] == y:
                c += [i]
        c=np.array(c)
        c=np.delete(c, col,axis=1)
        return np.array(c)

def label_encoder(matrix):
    n = []

    # finding all categorical variables for each attribute
    [n.append(str(i)) for i in matrix if str(i) not in n]
    num = np.array(range(0, len(n)))

    # creating a dictionary of each string and giving it a corresponding integer value
    di = dict((zip(n, num)))
    matrix[:] = [di.get(e, '') for e in matrix]
    return matrix

def one_hot_encoding(matrix):
    n = []

    # finding all categorical variables for each attribute
    [n.append(str(i)) for i in matrix if str(i) not in n]
    num = np.array(range(0, len(n)))
    di = dict((zip(n, num)))
    thing = np.full((len(matrix), len(di)), 0)
    s = 0
    #
    for i in matrix:
        di.get(i, '')
        thing[s][di.get(i, '')] = 1
        s+=1
    return thing

# fills any missing values from the row above
def forward_fill(matrix):
    cnt = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] =='':
                matrix[i][j] = matrix[i-1][j]
                cnt +=1
    print("Missing",cnt)
    return matrix

# calculates the accuracy of a classifier algorithm
def accuracy(self, actual, predicted):
    accuracy = 0
    size = len(actual)
    for i in range(size):
        if actual[i] == predicted[i]:
            accuracy += 1
    return accuracy/size
