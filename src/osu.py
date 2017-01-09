from dot_osu import load_map
import os
import re

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
    # find all map and songs
        file_dir = "E:/osu!/Songs/"
        map_list = []
        tmp_sep = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                tmp_file = os.path.join(root, file)
                if re.search('\.osu', tmp_file):
                    tmp_sep.append(tmp_file.split("\\")[0])
                    map_list.append(tmp_file.replace('\\', '/'))
        # load a map
        beatmap_list = []
        map_paser = load_map.load_osu()
        for i in range(0, len(map_list)):
            tmp_parser = map_paser.load_map(map_list[i])
            if tmp_parser == {}:
                continue

            beatmap_list.append(tmp_parser)
            length = len(beatmap_list) - 1
            beatmap_list[length]["OsuFilePath"] = map_list[i]
            if beatmap_list[length]['AudioFilename'][0] == ' ':
                beatmap_list[length]['AudioFilename'] = beatmap_list[length]['AudioFilename'][1:]
            beatmap_list[length]["SongFilePath"] = tmp_sep[i] + "/" + beatmap_list[length]['AudioFilename']
        music_info = load_map.generator_music_info(beatmap_list)
