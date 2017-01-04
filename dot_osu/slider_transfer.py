import numpy as np
from scipy.misc import comb


class slider_transfer:
    def __init__(self, slider):
        self.slider_object = slider
        self.points = []

    def split_slider(self):
        start_point = (self.slider_object.x, self.slider_object.y)
        self.points.append(start_point)
        for i in self.slider_object.origin_traces:
            self.points.append(i)
        end_points = (self.slider_object.end_x, self.slider_object.end_y)
        self.points.append(end_points)

    def transfer(self, speed, beat_time):
        sample_point = int(self.slider_object.slider_length / speed / beat_time) + 2
        self.split_slider()
        return self.bezier_curve(self.points, nTimes=sample_point)

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
    test = slider_transfer(1)

    xvals, yvals = test.bezier_curve(points, nTimes=1000)
    plt.plot(xvals, yvals)
    plt.plot(xpoints, ypoints, "ro")
    for nr in range(len(points)):
        plt.text(points[nr][0], points[nr][1], nr)

    plt.show()
