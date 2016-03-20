
class KnnLearner():
    
    def __init__(self, k=3):
        self.k = k
    
    def train(self, x_lists, y_list):
        self.x_lists = x_lists
        self.y_list = y_list
    
    def query(self, x_list):
        r = []
        for x in x_list:
            r.append( self.y_list[x] )
        return r;
