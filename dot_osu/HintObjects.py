__author__ = "Ehaschia"
import re


class HitObjects:
    def __init__(self):
        self.offset = 0
        self.x = 0
        self.y = 0
        self.obj_type = 1
        self.hit_sound = 0
        self.hit_type = ''

    def get_offset(self):
        return self.offset

    def parse_hit_type(self, s):
        return int(s.split(":")[0])

    def parse_hit_sound(self, s):
        self.hit_sound /= 2

        # divide 2, 1 3 5 7 whistal; 2 3 6 7 finish; 4 5 6 7 clap;
        if self.hit_sound == 0:
            pass
        elif self.hit_sound == 1:
            s[11] = 1
        elif self.hit_sound == 2:
            s[12] = 1
        elif self.hit_sound == 3:
            s[11] = s[12] = 1
        elif self.hit_sound == 4:
            s[13] = 1
        elif self.hit_sound == 5:
            s[11] = s[13] = 1
        elif self.hit_sound == 6:
            s[12] = s[13] = 1
        elif self.hit_sound == 7:
            s[11] = s[12] = s[13]
        else:
            raise ValueError("Hit Sound parse ERROR!")


class Circle(HitObjects):
    def __init__(self, s):
        HitObjects.__init__(self)
        self.x = int(s[0])
        self.y = int(s[1])
        self.offset = int(s[2])
        self.obj_type = int(s[3])
        self.hit_sound = int(s[4])

    """
    the meaning of every cell in feature:
    res[0] : x of circle
    res[1] : y of circle
    res[2] : x of slider
    res[3] : y of slider
    res[4] : is null object?
    res[5] : is circle object?
    res[6] : is slider object?
    res[7] : is spinner object?
    res[8] : if is slider object ,is it connect with the last one?
    res[9] : is it a begin of a stream?
    res[10]: sound type -- noraml -1 soft 0 drum 1
    res[11]: is whistel?
    res[12]: is finish?
    res[13]: is clap:
    """

    def get_featrue(self):
        res = [0.0 for i in range(13)]
        res[0] = float(self.x / 512.0)
        res[1] = float(self.y / 384.0)
        res[5] = 1.0
        res[9] = 1 if self.obj_type - 4 == 1 else 0
        res[10] = self.parse_hit_type(self.hit_type)
        self.parse_hit_sound(res)
        return res


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
        if not (self.obj_type == 8 or self.obj_type == 12):
            print("object parse error!")

    def get_featrue(self):
        res = [0.0 for i in range(15)]
        res[7] = 1.0
        res[10] = self.parse_hit_type(self.hit_type)
        self.parse_hit_sound(res)
        return res


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
            # it is a spinner
            if len(split_list) == 7:
                tmp_spinner = Spinner(split_list)
                self.object_list.append(tmp_spinner)
                self.time_table.append(tmp_spinner.get_offset())
            # it is a circle
            elif len(split_list) == 6:
                tmp_circle = Circle(split_list)
                self.object_list.append(tmp_circle)
                self.time_table.append(tmp_circle.get_offset())
            else:
                raise LookupError("the length of object is wrong!")


class NoneObject:
    def __init__(self):
        pass

    def get_featu0re(self):
        res = [0 for i in range(13)]
        res[4] = 1
        return res
