import numpy as np

class ConnectedNodesHelper():
    """
    Given N objects ,some of which are connected to each other, this class helps in finding all unique paths
    A path in this context can be defined as the largest path 
    No two paths have any overlapping nodes
    """
    def __init__(self, anyobjects:[]):
        self.__anyobjects=anyobjects
        self.__2darray = np.zeros((len(anyobjects),len(anyobjects)),dtype="int")
    
    def connect_pair(self, object1:any,object2:any):
        """
        Registers a connection between object1 and object2
        object1 and object2 are elements in the original array used for construction of this 
        """
        index1=self.__anyobjects.index(object1)
        index2=self.__anyobjects.index(object2)
        self.__2darray[index1][index2]=1
        self.__2darray[index2][index1]=1

    def is_object_pair_connected(self,object1:any, object2:any):
        index1=self.__anyobjects.index(object1)
        index2=self.__anyobjects.index(object2)
        cell_value=self.__2darray[index1][index2].item()
        retval= True if cell_value==1 else False
        return retval

    def find_paths(self)->[[]]:
        """
        Returns a list of list
        Each list contains the indices of the elements which form a connected path
        """
        already_added_line_indices=set()
        results:[]=[] #list of lists. Each inner list contains the 

        for line_index in range(0,len(self.anyobjects)):
            if (line_index in already_added_line_indices):
                continue
            connected_lines=set()
            self.__recursively_find_all_connected_lines(line_index,connected_lines)
            if (len(connected_lines) != 0):
                new_cluster=[]
                cluster_members=[self.anyobjects[i] for i in connected_lines]
                new_cluster.extend(cluster_members)
                already_added_line_indices.update(connected_lines)
                results.append(new_cluster)
        return results

    def __recursively_find_all_connected_lines(self,lineindex:int, resulting_connected_lines:set)->int:
        arr=self.__2darray[lineindex]
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
            self.__recursively_find_all_connected_lines(new_lineindex,resulting_connected_lines)
        count_of_connections_after=len(resulting_connected_lines)
        return (count_of_connections_after-count_of_connections_before)

    @property
    def anyobjects(self):
        """Returns the list of objects used for finding paths"""
        return self.__anyobjects
