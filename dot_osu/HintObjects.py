__author__ = "Ehaschia"
import re


class HitObjects:
    offset = 0
    x = 0
    y = 0
    obj_type = 1
    hit_sound = 0

    def __init__(self):
        pass

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


class Slider(HitObjects):
    slider_type = 'L'
    origin_trace = []
    end_x = 0
    end_y = 0
    repeat = 1
    slider_length = 0.0
    end_hitsound = 0

    def __init__(self, s):
        HitObjects.__init__(self)
        str_split = s.split('|')
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
                # just for v 14
                curve_point = re.split(':|,', str_split[i])
                if len(curve_point) == 2:
                    # is a curve point
                    self.origin_trace.append((int(curve_point[0]), int(curve_point[1])))
                elif len(curve_point) == 5:
                    # is a end part
                    self.end_x = int(curve_point[0])
                    self.end_y = int(curve_point[1])
                    self.repeat = int(curve_point[2])
                    self.slider_length = float(curve_point[3])
                    self.end_hitsound = int(curve_point[4])

    def check_validation(self):
        if self.slider_length > 0.0:
            return True
        else:
            return False


class Spinner(HitObjects):
    end_time = 0

    def __init__(self, s):
        HitObjects.__init__(self)
        self.x = int(s[0])
        self.y = int(s[1])
        self.offset = int(s[2])
        self.obj_type = int(s[3])
        self.hit_sound = int(s[4])
        self.end_time = int(s[5])


class HintObjectsTable():
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
            split_list = s.split(',')
            if len(split_list) == 7:
                tmp_spinner =Spinner(split_list)
                self.object_list.append(tmp_spinner)
                self.time_table.append(tmp_spinner.get_offset())
            elif len(split_list) == 6:
                tmp_circle = Circle(split_list)
                self.object_list.append(tmp_circle)
                self.time_table.append(tmp_circle.get_offset())
            else:
                raise LookupError("the length of object is wrong!")
