
import sys 
import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)
import typing
from sklearn.cluster import KMeans




def HeadChopper(src):

    
    # Loads an image
    
    blank_img = np.zeros(src.shape, dtype = np.uint8)
    data = src[~np.all(src == 0, axis=1)]

    idx = np.argwhere(np.all(data[..., :] == 0, axis=0))
    trimmed = np.delete(data, idx, axis=1)
    column_sums = np.sum(trimmed, axis=0)
    row_sums = np.sum(trimmed, axis=1)

    slicer = column_sums.shape[0]


    def head_or_not(column_sums=column_sums, density_threshold=20000, slicer=slicer)-> bool: 
        if np.any(column_sums[:-slicer+20] >density_threshold): 
            return True
        return False


    def long_neck(column_sums=column_sums,slicer = slicer)-> bool or int: 
        rate_of_change = abs(np.diff(column_sums[:-slicer+30]).astype(np.int16))
        rate_of_change_bool = rate_of_change<100
        total = rate_of_change_bool.sum()
        if (total/rate_of_change_bool.shape[0])>.1:
            return True
        return False



    def neck_removal(column_sums=column_sums, slicer=slicer)-> tuple: 

        indexer = column_sums.shape[0]
        upper_bound = column_sums[indexer-70:indexer-10]
        lower_bound = column_sums[indexer-10:indexer]
        opt_bool = True
        adjuster =0
        while opt_bool: 
            if np.sum(upper_bound)>2000*np.sum(lower_bound):
                adjuster+=2
                upper_bound = upper_bound[adjuster:]
            else:
                opt_bool=False
                print(np.sum(upper_bound))
                print(np.sum(lower_bound))
                print(upper_bound)
                cv.imshow('upper_bound', trimmed[:,:-upper_bound.shape[0]-lower_bound.shape[0]])
                cv.waitKey(0)
        return  trimmed[:,:-upper_bound.shape[0]-lower_bound.shape[0]]


    def cluster_removal(column_sums,slicer)-> np.matrix: 
        indexs = np.arange(0,column_sums[slicer:].shape[0],1)
        indexed_matrix = np.vstack((indexs, column_sums[slicer:])).T

        kmeans = KMeans(
            init="random",
            n_clusters=2,
            n_init=10,
            max_iter=300,
            random_state=42
        )

        kmeans.fit(indexed_matrix)
        assignments = kmeans.labels_
        #plt.scatter(indexs,column_sums[slicer:], c=assignments)
        #plt.show()

        reshaped_assignments = assignments.reshape(-1,1)

        Matrix_with_labels = np.vstack((indexed_matrix.T,reshaped_assignments.T))
        print(Matrix_with_labels.shape)
        Matrix_with_labels.T[np.all(Matrix_with_labels!=1, axis=0)]=0
        print(Matrix_with_labels.T)
        plt.scatter(Matrix_with_labels.T[:,0],Matrix_with_labels.T[:,1], c = Matrix_with_labels.T[:,2])
        plt.show()
        return np.where(~Matrix_with_labels.T.any(axis=1))[0][0]


    if head_or_not()==True or long_neck()==True : 
        head_removed = cluster_removal(column_sums, slicer-250)
        B = trimmed[:,:slicer-250 + head_removed]
        r,c =0,0
        blank_img[r:r+B.shape[0], c:c+B.shape[1]] += B
        cv.imshow('full', blank_img)
        cv.waitKey(0)
        return blank_img


    else: 

        B = neck_removal()
        r,c =0,0
        blank_img[r:r+B.shape[0], c:c+B.shape[1]] += B
        cv.imshow('full', blank_img)
        cv.waitKey(0)
        return blank_img





tail_tests = ['FarmVisit4Cow#15_result44.jpg','FarmVisit4Cow#35_result103.jpg', 'FarmVisit3Cow#6_result16.jpg','FarmVisit4Cow#126_result376.jpg','FarmVisit4Cow#103_result307.jpg']





       





