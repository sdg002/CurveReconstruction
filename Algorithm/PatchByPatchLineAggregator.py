import numpy as np
from Common import ConnectedLines
from typing import Union, Any, List, Optional, cast, Dict
from Common import RansacPatchInfo
from Common import RansacLineInfo
from Common import PolarLineModel
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.cluster import DBSCAN
from .ConnectedNodesHelper import ConnectedNodesHelper

class PatchByPatchLineAggregator():
    """traverses the patches that were discovered by patch by patch RANSAC and attempts to connect the lines"""
    def __init__(self, patches:np.ndarray, image_width:float, image_height:float):
        self.__patches:np.ndarray=patches
        self.distribution_threshold=0
        self.theta_threshold=0 #angle made by the perpendicular of the ransac line with the positive X axis
        self.rho_threshold=0 #distance of the ransac line from the origin
        self.__minmax_scaler=None
        self._image_width=float(image_width)
        self._image_height=float(image_height)
        self._epsilon=0
    
    @property
    def epsilon(self):
        """ The epsilon property used for DBSCAN.
            Attention! Not right to take just normalize the 'rho_threshold' OR 'theta_threshold' directly , 
            You will need to take the difference between normalized values some_rho and (some_rho+rho_threshold), 
            The value of 'some_rho' can be anything suitable in the range of existing values. e.g. 0
        """
        if (self._epsilon != 0):
            return self._epsilon
        scaler=self.min_max_scaler
        normalized_zero_zero=scaler.transform([[0,0]])
        normalized_thresholds=scaler.transform([[self.rho_threshold,self.theta_threshold]])
        delta_rho_threshold=normalized_thresholds[0][0]-normalized_zero_zero[0][0]
        delta_theta_threshold=normalized_thresholds[0][1]-normalized_zero_zero[0][1]
        self._epsilon=math.sqrt(delta_rho_threshold**2 + delta_theta_threshold**2)
        return self._epsilon

    @property
    def min_max_scaler(self)->MinMaxScaler:
        """Creates a Min Max scaler object using the maximum extents possible"""
        if (self.__minmax_scaler != None):
            return self.__minmax_scaler

        scaler = MinMaxScaler(feature_range=(1,100))
        diagonal=math.sqrt(self._image_width**2 + self._image_height**2)
        rho_theta_used_normalization=[[+diagonal,+math.pi/2],[-diagonal,-math.pi/2]]
        scaler.fit(rho_theta_used_normalization)
        self.__minmax_scaler=scaler
        return self.__minmax_scaler

    def find_connected_lines_in_adjacent_patches(self)->np.ndarray:
        """ 
        Collects all ransac lines in 2X2 adjacent patches and connects them via clustering of polar coordinates 
        Returns a 2d array of objects where every item represents a collection of clustered ransac lines in a 2X2 patch matrix
        """
        y_max=self.__patches.shape[0]
        x_max=self.__patches.shape[1]
        result=np.empty((y_max-1,x_max-1),dtype='object')
        for x in range(0,x_max-1):
            for y in range(0,y_max-1):
                patch_top_left  =self.__patches[y][x]
                patch_top_right =self.__patches[y][x+1]
                patch_bot_left  =self.__patches[y+1][x]
                patch_bot_right =self.__patches[y+1][x+1]
                connected_lines:List[ConnectedLines]=self.__find_connected_lines_in_2X2_patches(patch_top_left,patch_top_right, patch_bot_left,patch_bot_right)
                result[y][x]=connected_lines
        return result

    def find_connected_lines_in_across_all_patches(self,array_adjacent_patches)->List[ConnectedLines]:
        """
        Takes an numpy array where every member is a List of ConnectedLines objects
        The input  represents a cluster of lines in a 2x2 patch region

        The function collects all the RansacLineInfo objects and builds a connectivity matrix
        which spans all the cells of the input array
        """
        line_cluster_lookup=dict() #the ransac_line is the key, value is a List of 1 or more cluster objects which contains this ransac_line
        all_ransac_lines:List[RansacLineInfo]=list()
        #for cell in np.nditer(array_adjacent_patches,["refs_ok"]):
        for row in array_adjacent_patches:
            for cell in row:
                if ((cell == None) or (len(cell)==0)):
                    continue
                for connected_lines in cell:
                    for ransac_line in connected_lines.ransac_lines:
                        if ((ransac_line in all_ransac_lines) == False):
                            all_ransac_lines.append(ransac_line)
                        if ((ransac_line in line_cluster_lookup.keys()) ==False):
                            line_cluster_lookup[ransac_line]=set()
                        line_cluster_lookup[ransac_line].add(connected_lines)
                
        path_finder=ConnectedNodesHelper(all_ransac_lines)
        for x in range(0,len(all_ransac_lines)):
            line_x=all_ransac_lines[x]
            clusters_with_line_x=line_cluster_lookup[line_x]
            for connected_lines in clusters_with_line_x:
                for line_y in connected_lines.ransac_lines:
                    y=all_ransac_lines.index(line_y)
                    path_finder.connect_pair(line_x,line_y)
                    path_finder.connect_pair(line_y,line_x)

        results:[ConnectedLines]=[]
        paths=path_finder.find_paths()
        for path in paths:
            new_cluster=ConnectedLines()
            #cluster_members=[all_ransac_lines[line_index] for line_index in path]
            new_cluster.add_ransac_lines(path)
            results.append(new_cluster)
        return results

    @property
    def patches(self)->List[np.ndarray]:
        """The Numpy array of RansacPatchInfo objects """
        return self.__patches

    def __find_connected_lines_in_2X2_patches(self,patch_top_left:List[RansacLineInfo],patch_top_right:List[RansacLineInfo], patch_bot_left:List[RansacLineInfo],patch_bot_right:List[RansacLineInfo]):
        all_ransac_lines=[]
        all_ransac_lines.extend(patch_top_left)
        all_ransac_lines.extend(patch_top_right)
        all_ransac_lines.extend(patch_bot_left)
        all_ransac_lines.extend(patch_bot_right)
        if (len(all_ransac_lines) == 0):
            return []

        all_standard_lines=list(map(lambda  ransac: ransac.line,all_ransac_lines))
        all_polar_lines=list(map(lambda line: PolarLineModel.generate_polar_equation_hough(line),all_standard_lines))
        list_rho_theta=list(map(lambda  p:[p.rho, p.theta],all_polar_lines))
        

        
        scaler:MinMaxScaler = self.min_max_scaler
        normalized_rho_theta=scaler.transform(list_rho_theta)

        epsilon=self.epsilon
        db=DBSCAN(eps=epsilon, min_samples=2)
        db.fit(normalized_rho_theta)
        labels = db.labels_ #An array which is the same length as data vectors array. Each item in the array 

        count_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        count_noise_ = list(labels).count(-1)

        unique_labels = set(labels)

        results:List[ConnectedLines]=[]
        for cluster_index in range(0,count_clusters_):
            new_connected_lines=ConnectedLines()
            #fill in the patches
            results.append(new_connected_lines)
        for ransac_line_index in range(0,len(labels)):
            if (labels[ransac_line_index]==-1):
                #think
                pass
            else:
                ransac_line=all_ransac_lines[ransac_line_index]
                cluster_index=labels[ransac_line_index]
                results[cluster_index].add_ransac_line(ransac_line)



        return results

    def __create_min_max_scaler(self,list_rho_theta):
        scaler = MinMaxScaler()
        rho_theta_used_normalization=list(list_rho_theta)        
        rho_theta_used_normalization.append([self.rho_threshold,self.theta_threshold]) #needed for fair normalization
        scaler.fit(rho_theta_used_normalization)
        return scaler
