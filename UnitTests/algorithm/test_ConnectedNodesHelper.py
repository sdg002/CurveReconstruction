import unittest
from Algorithm import ConnectedNodesHelper

class test_ConnectedNodesHelper(unittest.TestCase):

    def test_basic_construction(self):
        input_objects=[1,2,3]
        sut=ConnectedNodesHelper(input_objects)
        actual_objects=sut.anyobjects
        self.assertEqual(len(input_objects), len(actual_objects))

    def test_When_constructed_No_Objects_Should_Be_Connected(self):
        obj1=object()
        obj2=object()
        obj3=object()
        sut=ConnectedNodesHelper([obj1,obj2,obj3])
        self.assertEqual(False, sut.is_object_pair_connected(obj1,obj2), 'Objects should not be connected')
        self.assertEqual(False, sut.is_object_pair_connected(obj1,obj3), 'Objects should not be connected')
        self.assertEqual(False, sut.is_object_pair_connected(obj3,obj2), 'Objects should not be connected')

    def test_When_Method_connect_pair_Is_Called_Then_The_Pair_Should_Be_Connected(self):
        obj1=object()
        obj2=object()
        obj3=object()
        sut=ConnectedNodesHelper([obj1,obj2,obj3])
        sut.connect_pair(obj2,obj3)
        self.assertEqual(False, sut.is_object_pair_connected(obj1,obj2), 'Objects should not be connected')
        self.assertEqual(False, sut.is_object_pair_connected(obj1,obj3), 'Objects should not be connected')
        self.assertEqual(True, sut.is_object_pair_connected(obj3,obj2), 'Objects should not be connected')

    def test_When_Method_find_paths_Is_Called_Then_2_Connected_Paths_Should_Be_Returned(self):
        obj1=object()
        obj2=object()
        obj3=object()
        obj4=object()
        obj5=object()
        obj6=object()
        sut=ConnectedNodesHelper([obj1,obj2,obj3, obj4, obj5,obj6])
        sut.connect_pair(obj1,obj2)
        sut.connect_pair(obj2,obj3)

        sut.connect_pair(obj4,obj5)
        sut.connect_pair(obj4,obj6)

        paths=sut.find_paths()
        self.assertEqual(2, len(paths), '2 paths are expected')

        path1=paths[0]
        self.assertEqual(3, len(path1), 'The discovered path must contain the correct members')
        self.assertEqual(True, obj1 in path1, 'The path must contain the correct element')
        self.assertEqual(True, obj2 in path1, 'The path must contain the correct element')
        self.assertEqual(True, obj3 in path1, 'The path must contain the correct element')

        path2=paths[1]
        self.assertEqual(3, len(path2), 'The discovered path must contain the correct members')
        self.assertEqual(True, obj4 in path2, 'The path must contain the correct element')
        self.assertEqual(True, obj5 in path2, 'The path must contain the correct element')
        self.assertEqual(True, obj6 in path2, 'The path must contain the correct element')

    def test_When_Method_find_paths_Is_Called_Then_1_Connected_Paths_Should_Be_Returned(self):
        obj1=object()
        obj2=object()
        obj3=object()
        obj4=object()
        obj5=object()
        obj6=object()
        sut=ConnectedNodesHelper([obj1,obj2,obj3, obj4, obj5,obj6])
        sut.connect_pair(obj1,obj2)
        sut.connect_pair(obj2,obj3)


        paths=sut.find_paths()
        self.assertEqual(1, len(paths), '2 paths are expected')

        path1=paths[0]
        self.assertEqual(3, len(path1), 'The discovered path must contain the correct members')
        self.assertEqual(True, obj1 in path1, 'The path must contain the correct element')
        self.assertEqual(True, obj2 in path1, 'The path must contain the correct element')
        self.assertEqual(True, obj3 in path1, 'The path must contain the correct element')




if __name__ == '__main__':
    unittest.main()
