class osu:
    def __init__(self, filename):
        self.filename = filename

    def global_feature(self):  # return a feature vector(including .osu file feature and .mp3 feature)
        pass

    def interval_features(self):  # return an array of vectors
        pass

    def loss(self, kth, state_vector):  # given k-th state vector, return (loss, grad vector)
        pass

    def get_music_info(self):
        return [['E:/osu!/Songs/- PUNCHMINDHAPPINESS/audio.mp3', 0.0, [3635.0, 41989.0, 52242.0], [94.936708860759495, 189.87341772151899, 94.936708860759495]],
                ['E:/osu!/Songs/-TV Size-/audio.mp3', 0.0, [3031.0, 9459.95834461996], [82.417582417582494, 82.417582417582494]]]