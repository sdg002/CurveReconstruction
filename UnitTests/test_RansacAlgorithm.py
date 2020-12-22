import unittest


class Test_testRansac(unittest.TestCase):
    """Unit tests for Ransac algorithm """


    def test_blah(self):
        y=100+200
        self.assertEqual(y, 300, 'some message from unit test')
        pass

    def test_decrement(self):
        self.assertEqual(4, 4)
        #you were here, unit tests are not running, you conifgured unittest, was pytest before

    
if __name__ == '__main__':
    unittest.main()
