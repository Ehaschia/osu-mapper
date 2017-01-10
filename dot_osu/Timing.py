__author__ = "Ehaschia"


class Timing:
    """
    @:param offset      (Integer, milliseconds) defines when the Timing Point takes effect.
    @:param mpb         (Float)  Milliseconds per Beat defines the beats per minute of the song. 60*1000/BPM = mpb
    @:param meter       (Integer)  the number of beats in a measure
    @:param sample_type (Integer)  the type of hit sound samples that are used. 1=Normal 2=Soft 3=Drum
    @:param sample_set  (Interger) the set of hit sounds that are used.
    @:param volume      (Integer) a value from 0 - 100 that defines the volume of hit sounds
    @:param mode        (Boolean) whether or not Kiai Time effects are active.
    @:param inherited   (Boolean)  whether or not the Timing Point is an inherited Timing Point.
    """

    def __init__(self, timing_str):
        self.offset = 0
        self.mpb = 0
        self.meter = 0
        self.sample_type = 1
        self.sample_set = 0
        self.volume = 100
        self.mode = False
        self.inherited = False
        self.slider_multiply = 1.0
        if timing_str[:-1] == '\n':
            timing_str = timing_str[:-1]
        timing_split = timing_str.split(',')
        if len(timing_split) != 8:
            raise NameError("the format of Timing point is error!")
        self.offset = float(timing_split[0])
        self.mpb = float(timing_split[1])
        self.meter = int(timing_split[2])
        self.sample_type = int(timing_split[3])
        self.sample_set = int(timing_split[4])
        self.volume = int(timing_split[5])
        # print(int(timing_split[6]) == 1)
        self.inherited = True if int(timing_split[6]) == 1 else False
        self.mode = bool(timing_split[7])

    def inherited_type(self):
        return self.inherited

    def get_offset(self):
        return self.offset

    def cal_real_speed(self):
        # 1/slider_multiply * -100 = mbp
        self.slider_multiply *= (-100.0) / self.mpb

    def get_speed(self):
        return self.slider_multiply



class TimingTable:
    def __init__(self):
        self.timing_table = []
        self.ni_time_table = []
        self.i_time_table = []

    def __add__(self, timing_str, slider_speed):
        timing_point = Timing(timing_str)
        if not timing_point.inherited_type():
            timing_point.cal_real_speed()
        else:
            timing_point.slider_multiply = slider_speed

        self.timing_table.append(timing_point)

    def music_seperate(self):
        for i in range(0, len(self.timing_table)):
            if self.timing_table[i].inherited_type():
                self.i_time_table.append(i)
            else:
                self.ni_time_table.append(i)

    def get_a_timing(self, i):
        return self.timing_table[i]

    def slider_speed_amend(self):
        for i in self.timing_table:
            if not i.inherited_type():
                i.get_real_speed()

    def get_mpb_list(self):
        bmp_list = []
        for i in self.i_time_table:
            bmp_list.append(self.timing_table[i].mpb)
        return bmp_list

    def get_red_timing_list(self):
        timing_list = []
        for i in self.i_time_table:
            timing_list.append(self.timing_table[i].offset)
        return timing_list

    def get_timing_list(self):
        return self.timing_table

    def get_speed_list(self, speed):
        speed_list = []
        for i in self.timing_table:
            if i.inherited_type():
                speed_list.append(speed)
            else:
                speed_list.append(i.get_speed())
        return speed_list
