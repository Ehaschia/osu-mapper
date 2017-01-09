import numpy as np
from scipy.misc import comb
import math


class SliderTransfer:
    def __init__(self, slider):
        self.slider_object = slider
        self.points = []
        self.length = self.slider_object.slider_length/self.slider_object.repeat
    def split_slider(self):
        start_point = (self.slider_object.x, self.slider_object.y)
        self.points.append(start_point)
        for i in self.slider_object.origin_traces:
            self.points.append(i)
        end_points = (self.slider_object.end_x, self.slider_object.end_y)
        self.points.append(end_points)



    def calculate_length(self, curve):
        length = 0.0
        for i in range(1, len(curve)):
            length += math.sqrt((curve[i-1][0]-curve[i][0]) ** 2 + (curve[i-1][1] -curve[i][1])**2)
        return length

    def transfer(self, speed):
        self.split_slider()
        sample_point = int(self.length / speed)
        if self.slider_object.slider_type == "B" or self.slider_object.slider_type == "L":
            points_list = []
            break_point = 0
            # split points sequence
            for i in range(1, len(self.points)):
                if self.points[i-1][0] == self.points[i][0] and self.points[i-1][1] == self.points[i][1]:
                    points_list.append(self.points[break_point : i-1])
                    break_point = i-1
            # no split, a smiple split
            if break_point == 0:
                curve = self.bezier_curve(self.points, nTimes=sample_point)
            else:
                curve = []
                length = []
                length_sum = 0.0
                for i in points_list:
                    curve = self.bezier_curve(i, nTimes=1000)
                    length.append(self.calculate_length(curve))
                    length_sum += length[-1]
                # normalize
                sample_count = 0
                for i in range(0, len(length) - 1):
                    length[i] = round(length[i]/length_sum*sample_point)
                    sample_count += length[i]
                length[-1] = sample_point-sample_count
                # calculate the bezier curve for every curve
                for i in range(0, len(points_list)):
                    tmp_curve = self.bezier_curve(points_list[i], nTimes=length[i])
                    if i == 0:
                        curve = tmp_curve
                    else:
                        curve.extend(tmp_curve[1:-1])

        elif self.slider_object.slider_type == "C" or self.slider_object.slider_type == "P":
            curve = self.difference_curve(points, nTimes=sample_point)
        real_curve = []
        for i in range(0, self.slider_object.repeat):
            if i % 2 == 0:
                real_curve.extend(curve)
            else:
                real_curve.extend(curve[::-1])
        return real_curve

    def calculate_angle2(self, angle):
        if angle < np.pi:
            return angle + np.pi * 2.0
        if angle > np.pi:
            return angle - np.pi * 2.0
        else:
            return angle

    def difference_curve(self, points, nTimes=1000):
        """
            Given a set of points, reruen the three
            difference curve defined by the control
            points.

            points should be a list of lists, or list of tuples
           such as [ [1,1],
                     [2,3],
                     [4,5], ..[Xn, Yn] ]
            nTimes is the number of time steps, defaults to 1000
        :return:
        """
        if len(points) != 3:
            raise ValueError("the size of P slider is wrong!")
        #  calculate the center of circle
        xpoints = [float(points[i][0]for i in range(len(points)))]
        ypoints = [float(points[i][0]for i in range(len(points)))]
        a = 2*(xpoints[1]-xpoints[0])
        b = 2*(ypoints[1]-ypoints[0])
        c = xpoints[1]**2 + ypoints[1]**2 -xpoints[0]**2 -ypoints[0]**2
        d = 2*(xpoints[2] - xpoints[1])
        e = 2*(ypoints[2] - ypoints[1])
        f =xpoints[2]**2 + ypoints[2]**2 - xpoints[1]**2 - ypoints[1]**2
        ccx = (b*f - e*c)/(b*d -e*a)
        ccy = (d*c - a*f)/(b*d - e*a)
        r = np.sqrt((ccx-xpoints[0])**2 + (ccy-ypoints[0])**2)
        # the angle of every points
        angle0 = self.calculate_angle(xpoints[0], ypoints[0], ccx, ccy, r)
        angle1 = self.calculate_angle(xpoints[1], ypoints[1], ccx, ccy, r)
        angle2 = self.calculate_angle(xpoints[2], ypoints[2], ccx, ccy, r)
        # the abs arc of point0->point1->point2
        good_arc = False
        if abs(abs(angle0-angle1) + abs(angle1-angle2) -abs(angle0-angle2)) > 1e-5:
            delta = 2*np.pi - abs(angle0-angle2)
        else:
            delta = abs(angle2-angle0)
        if delta > np.pi:
            good_arc = True
        # determinate the direction from angle0->angle2
        delta /= (nTimes-1)
        angle_list = []
        if good_arc:
            tmp_angle = angle0
            if angle0 > angle2:
                for i in range(0, nTimes+1):
                    angle_list.append(tmp_angle)
                    tmp_angle += delta
                    tmp_angle = self.calculate_angle2(tmp_angle)
            else:
                for i in range(0, nTimes + 1):
                    angle_list.append(tmp_angle)
                    tmp_angle -= delta
                    tmp_angle = self.calculate_angle2(tmp_angle)
        else:
            tmp_angle = angle0
            if angle0 > angle2:
                for i in range(0, nTimes+1):
                    angle_list.append(tmp_angle)
                    tmp_angle -= delta
                    tmp_angle = self.calculate_angle2(tmp_angle)
            else:
                for i in range(0, nTimes+1):
                    angle_list.append(tmp_angle);
                    tmp_angle += delta
                    tmp_angle = self.calculate_angle2(tmp_angle)
        points_list = []
        for i in angle_list:
            points_list.append(self.calculate_point(ccx, ccy, r, i))
        return points_list

    def calculate_point(self, ccx, ccy, r, angle):
        x = ccx + r*np.cos(angle)
        y = ccy + r*np.sin(angle)
        return x, y

    def calculate_angle(self, x, y, ccx, ccy, r):
        return np.arctan2((x-ccx), (y-ccy))

    def bernstein_poly(self, i, n, t):
        """
        The Bernstein polynomial of n, i as a function of t
        """

        return comb(n, i) * (t ** (n - i)) * (1 - t) ** i

    def bezier_curve(self, points, nTimes=1000):
        """
           Given a set of control points, return the
           bezier curve defined by the control points.

           points should be a list of lists, or list of tuples
           such as [ [1,1],
                     [2,3],
                     [4,5], ..[Xn, Yn] ]
            nTimes is the number of time steps, defaults to 1000

            See http://processingjs.nihongoresources.com/bezierinfo/
        """

        nPoints = len(points)
        xPoints = np.array([p[0] for p in points])
        yPoints = np.array([p[1] for p in points])

        t = np.linspace(0.0, 1.0, nTimes)

        polynomial_array = np.array([self.bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])
        xvals = np.dot(xPoints, polynomial_array)
        yvals = np.dot(yPoints, polynomial_array)
        res = list((xvals[i], yvals[i])for i in range(0, nTimes))[::-1]
        return res


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    nPoints = 4
    points = []
    xpoints = [48.0, 240.0, 240.0, 96.0]
    ypoints = [128.0, 80.0, 288.0, 32.0]
    for i in range(0, 4):
        points.append((xpoints[i], ypoints[i]))
    test = SliderTransfer(1)

    xvals, yvals = test.bezier_curve(points, nTimes=1000)
    plt.plot(xvals, yvals)
    plt.plot(xpoints, ypoints, "ro")
    for nr in range(len(points)):
        plt.text(points[nr][0], points[nr][1], nr)

    plt.show()
