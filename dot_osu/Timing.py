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
    offset = 0
    mpb = 0.0
    meter = 4
    sample_type = 1
    sample_set = 0
    volume = 100
    mode = False
    inherited = False

    def __init__(self, timing_str):

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
        self.inherited = bool(timing_split[6])
        self.mode = bool(timing_split[7])

    def inherited_type(self):
        return self.inherited

    def get_offset(self):
        return self.offset


class InheritedTiming(Timing):
    slider_multiply = 1.0

    def __init__(self, timing_str):
        Timing.__init__(self, timing_str)

    def get_real_speed(self):
        # 1/slider_multiply * -100 = mbp
        self.slider_multiply *= (-100.0) / self.mpb


class NotInheritedIiming(Timing):
    def __init__(self, timing_str):
        Timing.__init__(self, timing_str)


class TimingTable:
    timing_table = []
    ni_time_table = []
    i_time_table = []

    def __init__(self):
        pass

    def __add__(self, timing_str):
        timing_point = Timing(timing_str)
        if timing_point.inherited_type():
            timing_point.__class__ = InheritedTiming
            timing_point.get_real_speed()
        else:
            timing_point.__class__ = NotInheritedIiming

        self.timing_table.append(timing_point)

    def music_seperate(self):
        for i in range(0, len(self.timing_table)):
            if self.timing_table[i].inherited_type:
                pass
            else:
                self.ni_time_table.append(self.timing_table[i].get_offset())
            self.i_time_table.append(self.timing_table[i].get_offset())

    def get_a_timing(self, i):
        return self.timing_table[i]

    def slider_speed_amend(self):
        for i in self.timing_table:
            if i.inherited_type():
                i.get_real_speed()
