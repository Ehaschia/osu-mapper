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


class InheritedTiming(Timing):

    def __init__(self, timing_str):
        self.slider_multiply = 1.0
        Timing.__init__(self, timing_str)

    def get_real_speed(self):
        # 1/slider_multiply * -100 = mbp
        self.slider_multiply *= (-100.0) / self.mpb


class TimingTable:
    def __init__(self):
        self.timing_table = []
        self.ni_time_table = []
        self.i_time_table = []

    def __add__(self, timing_str):
        timing_point = InheritedTiming(timing_str)
        if not timing_point.inherited_type():
            timing_point.get_real_speed()
        else:
            timing_point.__class__ = Timing

        self.timing_table.append(timing_point)

    def music_seperate(self):
        for i in range(0, len(self.timing_table)):
            if self.timing_table[i].inherited_type():
                pass
            else:
                self.ni_time_table.append(self.timing_table[i].get_offset())
            self.i_time_table.append(self.timing_table[i].get_offset())

    def get_a_timing(self, i):
        return self.timing_table[i]

    def slider_speed_amend(self):
        for i in self.timing_table:
            if not i.inherited_type():
                i.get_real_speed()
