import regression
import knn
import decision
import svm
from statistics import mean

available_learners = {
    'regression' = RegressionLearner(),
    'knn' = KnnLearner(),
    'decision' = DecisionLearner(),
    'svm' = SvmLearner()
}

class EnsembleLearner():
    
    def __init__(self, learners=[]):
        self.learners = []
        for learner_name in learners:
            self.learners.append( available_learners[learner_name] )
    
    def train(self, x_lists, y_list):
        for learner in self.learners:
            learner.train(x_lists, y_list)
    
    def query(self, x_list):
        y = []
        for learner in self.learners:
            y.append( learner.query(x_list) )
        return mean(y)
