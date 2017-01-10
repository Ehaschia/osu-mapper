from __future__ import division
import math
import librosa
import python_speech_features

from dot_osu import load_map
import os
import re


class osu:
    beatmap_list = []
    def __init__(self, filename):
        self.filename = filename

    def global_feature(self):  # return a feature vector(including .osu file feature and .mp3 feature)
        pass

    def interval_features(self):
        infos = self.get_music_info()
        for info in infos:
            yield info[0], self.interval_features_single_song(info)

    def interval_features_single_song(self, music_info, K=5):  # return an array of vectors of a single song.
        path, osu_path ,start_time_points, ms_per_beat = music_info

        y, sr = librosa.load(path)

        intervals = start_time_points
        sample_per_ms = sr // 1000
        win_step = 10  # ms

        feat_spans = []
        time_spans = []

        end_time = intervals[-1]

        i = 0  # Current Timing Period
        start = intervals[i]
        while start < end_time:
            end = start + ms_per_beat[i]
            if start < intervals[i + 1]:
                beat_start_index = int(math.floor(start * sample_per_ms))
                beat_end_index = int(math.ceil(end * sample_per_ms))

                feat = python_speech_features.mfcc(y[beat_start_index:beat_end_index], samplerate=sr,
                                                   winstep=win_step / 1000.)

                n_frames = feat.shape[0]

                if n_frames > K:
                    every_k = n_frames // K
                    feat = feat[::every_k][:K]
                elif n_frames < K:
                    if start > math.floor((K - n_frames) / 2) * win_step:
                        i_start = int(start - math.floor((K - n_frames) / 2) * win_step)
                        i_end = int(end + math.ceil((K - n_frames) / 2) * win_step)
                    else:
                        i_start = start
                        i_end = end + (K - n_frames) * 10

                    beat_start_index = int(math.floor(i_start * sample_per_ms))
                    beat_end_index = int(math.ceil(i_end * sample_per_ms))
                    feat = python_speech_features.mfcc(y[beat_start_index:beat_end_index], samplerate=sr,
                                                       winstep=win_step / 1000.)

                time_spans.append((start, end))
                feat_spans.append(feat)
                start = end
            else:
                start = intervals[i + 1]
                i += 1

        return feat_spans, time_spans

    def loss(self, kth, state_vector):  # given k-th state vector, return (loss, grad vector)
        pass

    def get_music_info(self):
        # find all map and songs
        file_dir = "/home/ehaschia/songs/"
        map_list = []
        tmp_sep = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                tmp_file = os.path.join(root, file)
                if re.search('\.osu', tmp_file):
                    tmp_sep.append(os.path.dirname(tmp_file))
                    map_list.append(tmp_file.replace('\\', '/'))
        # load a map
        self.beatmap_list = []
        map_paser = load_map.load_osu()
        for i in range(0, 1):
            tmp_parser = map_paser.load_map(map_list[i])
            if tmp_parser == {}:
                continue

            self.beatmap_list.append(tmp_parser)
            length = len(self.beatmap_list) - 1
            self.beatmap_list[length]["OsuFilePath"] = map_list[i]
            if self.beatmap_list[length]['AudioFilename'][0] == ' ':
                self.beatmap_list[length]['AudioFilename'] = self.beatmap_list[length]['AudioFilename'][1:]
            self.beatmap_list[length]["SongFilePath"] = tmp_sep[i] + "/" + self.beatmap_list[length]['AudioFilename'].strip()


        music_info = load_map.generator_music_info(self.beatmap_list)
        return music_info

    def get_beatmap_list(self):
        return self.beatmap_list

if __name__ == '__main__':
    oo = osu('test')
    for x in oo.interval_features():
        load_map.generator_objects_lists(x, oo.get_beatmap_list())
