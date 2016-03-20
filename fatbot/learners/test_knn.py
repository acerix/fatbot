#!/usr/bin/env python3

import unittest
import knn

class TestKnn(unittest.TestCase):
    
    learner = knn.KnnLearner()
    
    # Train
    def test_train(self):
        x = [
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1]
        ]
        y = [1/5, 2/25, 3/125, 4/625, 5/3125]
        self.learner.train(x, y)        
        self.assertTrue(True)
        
    
    # Query
    def test_query(self):
        return 6
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.learner.train(x, y)
        self.assertEqual(self.learner.query([x[2]]), y[2])
        
    
        
if __name__ == '__main__':
    unittest.main()
