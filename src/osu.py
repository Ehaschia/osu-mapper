class osu:
    def __init__(self, filename):
        self.filename = filename

    def global_feature(self):  # return a feature vector(including .osu file feature and .mp3 feature)
        pass

    def interval_features(self):  # return an array of vectors
        pass

    def loss(self, kth, state_vector):  # given k-th state vector, return (loss, grad vector)
        pass
