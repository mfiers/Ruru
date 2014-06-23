
import matplotlib as mpl

class View(object):
    def __init__(self, ax, start, stop, padding=0.1,
                 score_cmap=None, score_min=0, score_max=1):
        self.ax = ax
        self.start = start
        self.stop = stop
        self.ax.set_xlim(start, stop)
        self.width = stop - start
        self.rows = []
        self.padding = padding
        if score_cmap is None:
            self.score_cmap = mpl.cm.hot
            self.score_cmap.set_bad('#aaaaaa', 1)
        else:
            self.score_cmap = score_cmap

        self.score_min = score_min
        self.score_max = score_max

    def get_color(self, val):
        s = (float(val) - self.score_min) \
             / (self.score_max - self.score_min)
        s = min(1, max(0, s))
        return self.score_cmap(s)


    def fit_row(self, feature, rowno):
        rmarg = (self.stop - self.start) * self.padding
        for oldfeat in self.rows[rowno]:
            if feature.start - rmarg < oldfeat.stop and \
                    feature.stop + rmarg > oldfeat.start:
                return False
        return True

    def find_row(self, feature):
        for i, r in enumerate(self.rows):
            if self.fit_row(feature, i):
                return i
        self.rows.append([])
        return len(self.rows)-1

    def place(self, features):
        self.rows = []
        for f in features:
            rowno = self.find_row(f)
            self.rows[rowno].append(f)

    def draw(self, features):
        features = sorted(features)
        self.place(features)
        self.ax.set_ylim(0, len(self.rows))
        self.ax.set_yticks([],[])
        for i, row in enumerate(self.rows):
            ymin, ymax = i, i+(1-self.padding)
            for feature in row:
                feature.draw(self, ymin, ymax)
        return self.ax

