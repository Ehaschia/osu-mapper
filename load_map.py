__author__ = "Ehaschia"
import os
import re
from HintObjects import HitObjects, HintObjectsTable
from Timing import TimingTable
import Timing

GENETAL = ['AudioFilename', 'AudioLeadIn', 'PreviewTime', 'Countdown', 'SampleSet', 'StackLeniency', 'Mode',
           'LetterboxInBreaks', 'StoryFireInFront', 'EpilepsyWarning', 'CountdownOffset', 'WidescreenStoryboard']

EDITOR = ['Bookmarks', 'DistanceSpacing', 'BeatDivisor', 'GridSize', 'TimelineZoom']

METADATA = ['Title', 'TitleUnicode', 'Artist', 'ArtistUnicode', 'Creator', 'Version', 'Source', 'Tags', 'BeatmapID',
            'BeatmapSetID']

DIFFICULTY = ['HPDrainRate', 'CircleSize', 'OverallDifficulty', 'ApproachRate', 'SliderMultiplier', 'SliderTickRate']


def add_dic(name, dic, file_text, i):
    if file_text[i].find(name) != -1:
        dic[name] = file_text[i].split(':')[-1][:-1]


def general_info(file_text, begin_row, end_row, dic):
    for i in range(begin_row, end_row):
        for j in GENETAL:
            add_dic(j, dic, file_text, i)


def editor_info(file_text, begin_row, end_row, dic):
    for i in range(begin_row, end_row):
        for j in EDITOR:
            add_dic(j, dic, file_text, i)


def metadata_info(file_text, begin_row, end_row, dic):
    for i in range(begin_row, end_row):
        for j in METADATA:
            add_dic(j, dic, file_text, i)


def difficulty_info(file_text, begin_row, end_row, dic):
    for i in range(begin_row, end_row):
        for j in DIFFICULTY:
            add_dic(j, dic, file_text, i)


def events_info(file_text, begin_row, end_row, dic):
    tmp_list = []
    flag = False
    for i in range(begin_row, end_row):
        if re.search('Break Periods', file_text[i]):
            for j in range(i + 1, end_row):
                if file_text[j].find('//') != -1:
                    flag = True
                    break
                else:
                    tmp_list.append(file_text[j])
        if flag:
            break

    if len(tmp_list) != 0:
        dic['Break Periods'] = tmp_list


def timing_info(file_text, begin_row, end_row, dic):
    timing_table = TimingTable()

    for i in range(begin_row, end_row):
        timing_table.__add__(file_text[i])
    timing_table.slider_speed_amend()
    timing_table.music_seperate()


def object_info(file_text, begin_row, end_row, dic):
    obj_table = HintObjectsTable()
    for i in range(begin_row, end_row):
        obj_table.add_object(file_text[i])
    dic['hitobjects'] = obj_table


def text_to_dic(file_text):
    dic = {}
    row = 0
    line_cnt = len(file_text)
    # get the osu file format
    dic['format'] = int(re.search('\d+', file_text[row]).group(0))
    if dic['format'] < 10:
        return {}
    row += 1
    print "file format is v" + str(dic['format'])
    split_row = {}
    for row in range(1, line_cnt):
        if re.search('\[General\]', file_text[row]):
            split_row['General'] = row + 1
        if re.search('\[Editor\]', file_text[row]):
            split_row['Editor'] = row + 1
        if re.search('\[Metadata\]', file_text[row]):
            split_row['Metadata'] = row + 1
        if re.search('\[Difficulty\]', file_text[row]):
            split_row['Difficulty'] = row + 1
        if re.search('\[Events\]', file_text[row]):
            split_row['Events'] = row + 1
        if re.search('\[TimingPoints\]', file_text[row]):
            split_row['TimingPoints'] = row + 1
        if re.search('Colour', file_text[row]):
            split_row['Colours'] = row + 1
        if re.search('\[HitObjects\]', file_text[row]):
            split_row['HitObjects'] = row + 1
    split_row['End'] = line_cnt
    general_info(file_text, split_row['General'], split_row['Editor'] - 1, dic)
    if int(dic['Mode']) != 0:
        return {}
    editor_info(file_text, split_row['Editor'], split_row['Metadata'] - 1, dic)
    metadata_info(file_text, split_row['Metadata'], split_row['Difficulty'] - 1, dic)
    difficulty_info(file_text, split_row['Difficulty'], split_row['Events'] - 1, dic)
    events_info(file_text, split_row['Events'], split_row['TimingPoints'] - 1, dic)
    if split_row.has_key('Colours'):
        timing_info(file_text, split_row['TimingPoints'], split_row['Colours'] - 1, dic)
    else:
        timing_info(file_text, split_row['TimingPoints'], split_row['HitObjects'] - 1, dic)
    object_info(file_text, split_row['HitObjects'], split_row['End'], dic)
    return dic


def load_map(file_name):
    f = open(file_name, 'r')
    file_text = []
    try:
        for line in f:
            if len(line) <= 2:
                if line != '\n':
                    print(line)
                continue
            file_text.append(line)
    except Exception:
        raise ("read" + file_name + "fail.")
    finally:
        f.close()

    beatmap = text_to_dic(file_text)


if __name__ == '__main__':
    # find all map and songs
    file_dir = "E:/osu!/Songs/"
    map_list = []
    music_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            tmp_file = os.path.join(root, file)
            if re.search('\.osu', tmp_file):
                map_list.append(tmp_file.replace('\\', '/'))
            if re.search('\.mp3', tmp_file):
                music_list.append(tmp_file.replace('\\', '/'))
    # load a map
    for i in map_list:
        load_map(i)