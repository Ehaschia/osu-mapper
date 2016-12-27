__author__ = "Ehaschia"
import re


class HitObjects:
    def __init__(self):
        self.offset = 0
        self.x = 0
        self.y = 0
        self.obj_type = 1
        self.hit_sound = 0

    def get_offset(self):
        return self.offset


class Circle(HitObjects):
    def __init__(self, s):
        HitObjects.__init__(self)
        self.x = int(s[0])
        self.y = int(s[1])
        self.offset = int(s[2])
        self.obj_type = int(s[3])
        self.hit_sound = int(s[4])

    def get_featrue(self):
        res = [0.0 for i in range(10)]
        res[0] = float(self.x/512.0)
        res[1] = float(self.y/384.0)
        res[5] = 1.0

class Slider(HitObjects):
    def __init__(self, s):
        if s.find('\n') != -1:
            s = s[:-1]
        HitObjects.__init__(self)
        str_split = s.split('|')
        self.origin_trace = []
        for i in range(0, len(str_split)):
            # load the basic information of slider
            if i == 0:
                main_slider = str_split[i].split(',')
                if len(main_slider) != 6:
                    raise NameError("Maybe some verson wrong")
                self.x = int(main_slider[0])
                self.y = int(main_slider[1])
                self.offset = int(main_slider[2])
                self.obj_type = int(main_slider[3])
                self.hit_sound = int(main_slider[4])
                self.slider_type = str(main_slider[5])
            else:
                curve_point = re.split(':|,', str_split[i])
                if len(curve_point) == 2:
                    # is a curve point
                    self.origin_trace.append((int(curve_point[0]), int(curve_point[1])))
                elif len(curve_point) >= 5:
                    # is a end part
                    self.end_x = int(curve_point[0])
                    self.end_y = int(curve_point[1])
                    self.repeat = int(curve_point[2])
                    self.slider_length = float(curve_point[3])
                    self.end_hitsound = int(curve_point[4])
                elif len(curve_point) == 4:
                    # in version 12 or small than 12 there are 4 elements in the end part
                    self.end_x = int(curve_point[0])
                    self.end_y = int(curve_point[1])
                    self.repeat = int(curve_point[2])
                    self.slider_length = float(curve_point[3])
                    self.end_hitsound = 0

    def check_validation(self):
        if self.slider_length > 0.0:
            return True
        else:
            return False


class Spinner(HitObjects):
    def __init__(self, s):
        HitObjects.__init__(self)
        self.x = int(s[0])
        self.y = int(s[1])
        self.offset = int(s[2])
        self.obj_type = int(s[3])
        self.hit_sound = int(s[4])
        self.end_time = int(s[5])


class HintObjectsTable:
    object_list = []
    time_table = []

    def __init__(self):
        pass

    def add_object(self, s):
        if s is None:
            raise NameError("No Objects!")
        # ignore the last \n
        if s[:-1] == '\n':
            s = s[:-1]
        # judge its a slider or not
        if s.find('|') != -1:
            tmp_slider = Slider(s)
            # CHECK
            self.object_list.append(tmp_slider)
            self.time_table.append(tmp_slider.get_offset())
            tmp_slider.check_validation()

        else:
            if s.find('\n') != -1:
                s = s[:-1]
            split_list = s.split(',')
            if len(split_list) == 7:
                tmp_spinner = Spinner(split_list)
                self.object_list.append(tmp_spinner)
                self.time_table.append(tmp_spinner.get_offset())
            elif len(split_list) == 6:
                tmp_circle = Circle(split_list)
                self.object_list.append(tmp_circle)
                self.time_table.append(tmp_circle.get_offset())
            else:
                raise LookupError("the length of object is wrong!")
