import numpy as np
from Common import ConnectedLines
from typing import Union, Any, List, Optional, cast, Dict
from Common import RansacPatchInfo
from Common import RansacLineInfo
from Common import PolarLineModel
from sklearn.preprocessing import MinMaxScaler
import math
from sklearn.cluster import DBSCAN

class PatchByPatchLineAggregator():
    """traverses the patches that were discovered by patch by patch RANSAC and attempts to connect the lines"""
    def __init__(self, patches:np.ndarray):
        self.__patches:np.ndarray=patches
        self.distribution_threshold=0
        self.theta_threshold=0 #angle made by the perpendicular of the ransac line with the positive X axis
        self.rho_threshold=0 #distance of the ransac line from the origin

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
                
        connectivity_matrix=np.zeros((len(all_ransac_lines),len(all_ransac_lines)),dtype='int')
        
        for x in range(0,len(all_ransac_lines)):
            line_x=all_ransac_lines[x]
            clusters_with_line_x=line_cluster_lookup[line_x]
            for connected_lines in clusters_with_line_x:
                for line_y in connected_lines.ransac_lines:
                    y=all_ransac_lines.index(line_y)
                    connectivity_matrix[y,x]=1
                    connectivity_matrix[x,y]=1

        results:[ConnectedLines]=[]
        already_added_line_indices=set()
        for line_index in range(0,len(all_ransac_lines)):
            #array_of_connected_indices=connectivity_matrix[line_index]
            if (line_index in already_added_line_indices):
                continue
            connected_lines=set()
            self.__recursively_find_all_connected_lines(connectivity_matrix,line_index,connected_lines)
            if (len(connected_lines) != 0):
                new_cluster=ConnectedLines()
                cluster_members=[all_ransac_lines[i] for i in connected_lines]
                new_cluster.add_ransac_lines(cluster_members)
                already_added_line_indices.update(connected_lines)
                results.append(new_cluster)
        return results

    def __recursively_find_all_connected_lines(self,connectivity_matrix:np.ndarray,lineindex:int, resulting_connected_lines:set)->int:
        arr=connectivity_matrix[lineindex]
        count_of_connections_before=len(resulting_connected_lines)
        for new_lineindex in range(0,len(arr)):
            if (new_lineindex == lineindex):
                continue
            cell_value=arr[new_lineindex].item()
            if (cell_value == 0):
                #no connection, this line can be ignore
                continue
            if (new_lineindex in resulting_connected_lines):
                #already added to cluster
                continue
            else:
                resulting_connected_lines.add(new_lineindex)
            self.__recursively_find_all_connected_lines(connectivity_matrix,new_lineindex,resulting_connected_lines)
        count_of_connections_after=len(resulting_connected_lines)
        return (count_of_connections_after-count_of_connections_before)

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

        all_standard_lines=list(map(lambda  ransac: ransac.line,all_ransac_lines))
        all_polar_lines=list(map(lambda line: PolarLineModel.generate_polar_equation_hough(line),all_standard_lines))
        list_rho_theta=list(map(lambda  p:[p.rho, p.theta],all_polar_lines))
        

        scaler:MinMaxScaler = self.__create_min_max_scaler(list_rho_theta)
        normalized_rho_theta=scaler.transform(list_rho_theta)
        normalized_thresholds=scaler.transform([[self.rho_threshold,self.theta_threshold]])
        epsilon=math.sqrt(normalized_thresholds[0][0]**2 + normalized_thresholds[0][1]**2)


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
