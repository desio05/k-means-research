import random

import numpy as np
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt


def generateClusters(number, features):
    numberOfElements = number * features
    cluster1 = np.random.uniform(-50000000, 0, numberOfElements * 6).reshape((-1, features))
    cluster2 = np.random.uniform(10000000, 60000000, numberOfElements).reshape((-1, features))
    cluster3 = np.random.uniform(100000000, 150000000, numberOfElements).reshape((-1, features))
    cluster4 = np.random.uniform(170000000, 200000000, numberOfElements).reshape((-1, features))
    cluster5 = np.random.uniform(220000000, 250000000, numberOfElements).reshape((-1, features))
    cluster6 = np.random.uniform(270000000, 300000000, numberOfElements).reshape((-1, features))

    return np.concatenate((cluster1, cluster2, cluster3, cluster4, cluster5, cluster6))
    # return cluster1


def lk_norm(x, y, k):
    return (sum([np.math.fabs(x_i - y_i) ** k for x_i, y_i in zip(x, y)])) ** (1 / k)


def split_clusters(objs, clusters_number, centers, k):
    clusters = [[] for i in range(clusters_number)]
    obj_distrib = [-1] * len(objs)
    for i, obj in enumerate(objs):
        distances = [lk_norm(center, obj, k) for center in centers]
        clust_number = np.argmin(distances)
        clusters[clust_number].append(obj)
        obj_distrib[i] = clust_number
    return clusters, obj_distrib


def generate_centers(objs, clusters_number, k, method='kmeans++'):
    if method == 'random':
        return random.sample(list(objs), clusters_number)
    elif method == 'kmeans++':
        init_center = random.choice(objs)
        # init_distances = list(map(lambda obj: lk_norm(obj, init_center, k), objs))
        centers = [init_center]
        while len(centers) < clusters_number:
            distances = np.array([min([lk_norm(obj, center, k) for center in centers]) for obj in objs])
            sum_distances = np.sum(distances)
            new_center_index = np.random.choice(range(len(objs)), 1, p=distances / sum_distances)[0]
            centers.append(objs[new_center_index])
        return centers


def kmeans(objs, clusters_number, k, centers=None):
    if centers is None:
        # avoid the situation when any cluster is empty
        while True:
            centers = generate_centers(objs, clusters_number, k, method='kmeans++')
            # centers = np.random.uniform(np.min(objs), np.max(objs), clusters_number * dimension) \
            #     .reshape((-1, dimension))
            clusters, obj_distrib = split_clusters(objs, clusters_number, centers, k)
            print("Finding clusters")
            if all([len(cluster) > 0 for cluster in clusters]):
                break
    else:
        clusters, obj_distrib = split_clusters(objs, clusters_number, centers, k)

    i = 0
    while i < 50:
        # cluster and centers are already initialized
        new_centers = [np.mean(cluster, axis=0) for cluster in clusters]
        if np.equal(centers, new_centers).all():
            return centers, clusters, obj_distrib
        centers = new_centers
        clusters, obj_distrib = split_clusters(objs, clusters_number, centers, k)
        i += 1

    return centers, clusters, obj_distrib


def do_test(objs, elems_number, features, k):
    def compute_error(clusters, centres):
        error = 0
        for index, result_center in enumerate(centres):
            # print(result_center)
            for obj in clusters[index]:
                error += np.sum((obj - result_center) ** 2)

        return error

    # sk_kmeans = KMeans(n_clusters=6, init="random").fit(objs)
    # sk_result_clusters, sk_obj_distrib = split_clusters(objs, 6, sk_kmeans.cluster_centers_, k)
    # sk_error = compute_error(sk_result_clusters, sk_kmeans.cluster_centers_)
    # sk_metric = metrics.calinski_harabaz_score(objs, sk_obj_distrib)
    # print("sk learn: euclidian. Features: " + str(features) + ". n_iter=" + str(sk_kmeans.n_iter_) + ". Error: " +
    #       str(sk_error) + ". Calinski&Harabaz score: " + str(sk_metric))

    errors = []
    for i in range(1):
        result_centers, result_clusters, obj_distrib = kmeans(objs, 6, k)
        errors.append(compute_error(result_clusters, result_centers))
    # metric = metrics.calinski_harabaz_score(objs, obj_distrib)

    # correct_distr = 0
    # for i in range(0, len(result_clusters)):
    #     for j in range(0, elems_number):
    #         if obj_distrib[i * 100 + j] == i:
    #             correct_distr += 1

    qual = silhouette_samples(objs, obj_distrib)


    # print("k-value:" + str(k) + ". Features: " + str(features) + ". Error: " + str(error)
    #       + ". Calinski&Harabaz score: " + str(metric))

    colors = ["r", "b", "g", "y", "c", "m"]
    for i, clust in enumerate(result_clusters):
        plt.plot(np.array(clust)[:, :1], np.array(clust)[:,1:2], colors[i] + "+")

    plt.show()
    print("k-value:" + str(k) + ". Features: " + str(features) + ". Error: " + str(np.mean(errors)) + ". Accuracy: " + str(np.mean(qual)))


if __name__ == '__main__':
    # for i in range(15, 20):
    # do_test(700, 20, 0.3)
    objs = generateClusters(500, 20)
    do_test(objs, 500, 20, 0.3)
    do_test(objs, 500, 20, 0.5)
    do_test(objs, 500, 20, 1)
    do_test(objs, 500, 20, 2)
    do_test(objs, 500, 20, 3)
    print()
