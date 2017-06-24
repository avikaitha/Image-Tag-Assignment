
class Generator:

    def __init__(self, X1, X2, Y):
        self.X1 = X1
        self.X2 = X2
        self.Y = Y
        self.start = 0
        self.num_samples = X1.shape[0]
    
    
    def next_batch(self, batch_size):
        end = self.start+batch_size
        if end>=self.num_samples:
            end = self.num_samples
        X1 = self.X1[self.start:end,:]
        X2 = self.X2[self.start:end,:]
        Y = self.Y[self.start:end,:]
        self.start = end
        return X1,X2,Y
    
    
    def reset(self):
        self.start = 0     
    
    def shuffle(self, X1, X2, Y):
        self.X1 = X1
        self.X2 = X2
        self.Y = Y
        self.start = 0
        
