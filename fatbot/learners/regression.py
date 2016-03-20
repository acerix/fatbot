
from scipy import stats

class RegressionLearner():
    
    def __init__(self):
        self.coefficients = {}
    
    def train(self, x_lists, y_list):
        for i, x_list in enumerate(x_lists):
            print(i)
            self.coefficients[i] = [0, 0]
            self.coefficients[i][1], self.coefficients[i][0], rvalue, pvalue, stderr = stats.linregress(x_list, y_list)
    
    def query(self, x_list):
        r = []
        for x in x_list:
            print(x)
            print( self.coefficients)
            r.append( self.coefficients[x][0] + self.coefficients[x][1] * x )
        return r;
