#!/usr/bin/env python3

import unittest
import regression
import pylab

class TestRegression(unittest.TestCase):
    
    learner = regression.RegressionLearner()
    
    # Train
    def test_train(self):
        x = [
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1]
        ]
        y = [1/5, 2/25, 3/125, 4/625, 5/3125]
        self.learner.train(x, y)        
        self.assertEqual(self.learner.coefficients, [0.20352000000000003, -0.047040000000000005])
        
    
    # Query
    def test_query(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.learner.train(x, y)
        self.assertEqual(self.learner.query([x[2]]), y[2])
        
    
    # Plot
    def test_plot(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        self.learner.train(x, y)
        pylab.plot(x, y, 'o')
        predict_y = self.learner.query(x)
        print(predict_y)
        pylab.plot(x, predict_y, 'k-')
        pylab.show()
        
    
    
        
if __name__ == '__main__':
    unittest.main()
