
import numpy as np

import matplotlib as mpl
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

class Feature(object):
    def __init__(self, name, start, stop, orientation='.',
                 gene_name="",
                 children=None, facecolor="green", score=None,
                 linecolor="black", linewidth=1, label=False):
        self.name = name
        self.start = start
        self.stop = stop
        self.orientation = orientation
        self.score = score
        self.facecolor = facecolor
        self.linecolor = linecolor
        self.linewidth = linewidth
        self.label = label
        self.gene_name = gene_name
        if children is None: self.children = []
        else: self.children = children

    def get_fillcolor(self, view):
        if self.score is None:
            return self.facecolor
        else:
            return view.get_color(self.score)

    def draw(self, view, ymin, ymax):
        ax = view.ax
        fillcolor = self.get_fillcolor(view)
        ax.add_patch(Rectangle((self.start, ymin),
                self.stop - self.start, ymax-ymin,
                fc=fillcolor, ec=self.linecolor,
                lw=self.linewidth))


    def __lt__(self, other):
        return self.start < other.start

    def __str__(self):
        return "<{}:{}-{}>".format(self.__class__.__name__,
            self.start, self.stop)

    def __repr__(self):
        return str(self)


class ScoreFeature(Feature):
    def draw(self, view, ymin, ymax):
        nf = (view.ax.figure)

        self.score = self.score / 1.0
        sz = len(self.score)
        x = int(sz / 5)
        y = int(sz / x) + 1

        #prepare score array
        q = self.score
        q.sort()
        q = q[::-1]
        q = np.concatenate((q, [np.nan] * (x*y-sz)))
        q = q.reshape(x,y).T

        #coordinate transformation
        ftc = [(self.start, ymin),
               (self.stop, ymax)]
        print(ftc)
        nwc = view.ax.transData.transform(ftc)
        print(nwc)
        axc = nf.transFigure.inverted().transform(nwc)
            #  self.stop - self.start,
        print(axc)
        print(axc[0][0],
              axc[0][1],
              axc[1][0] - axc[0][0],
              axc[1][1] - axc[0][1])
        nx = nf.add_axes([
            axc[0][0],
            axc[0][1],
            axc[1][0] - axc[0][0],
            axc[1][1] - axc[0][1]],
            frameon=True)

        nx.axis('off')
        nx.autoscale_view('tight')
        pcm = nx.imshow(q, interpolation='none',
                        cmap=view.score_cmap, aspect='auto')

        nxx = nx.get_xlim()
        nxy = nx.get_ylim()
        nx.add_patch(Rectangle((nxx[0],nxy[0]),
                nxx[1]-nxx[0], nxy[1]-nxy[0],
                fc="none", ec="black",
                lw=self.linewidth))


class FeatureGene(Feature):
    def draw(self, view, ymin, ymax):
        ax = view.ax
        ymid = (0.5*(ymax-ymin)) + ymin
        dx = view.width / 120.
        ax.plot([self.start, self.stop], [ymid, ymid], lw=1,
                 color=self.linecolor, zorder=-5)
        if self.orientation == 1:
            ax.plot([self.stop - dx, self.stop, self.stop - dx],
                    [ymid-0.25, ymid, ymid + 0.25], lw=2, alpha=0.4,
                     color=self.linecolor, zorder=-5)
        for c in self.children:
            c.draw(view, ymin, ymax)

        if self.label:
                bbox_props = \
                    dict(boxstyle="round,pad=0.3", fc="#dddddd", ec=None,
                         lw=0, alpha=0.8, clip_on=True, clip_box=ax.bbox)
                ann = ax.annotate(
                    self.name, xy=(self.stop + (view.width / 200.),
                        ymid),  fontsize=6, bbox=bbox_props,
                        verticalalignment='center', clip_on=True)
                ann.set_clip_box(ax.bbox)

                if self.gene_name:
                    ann = ax.annotate(self.gene_name,
                                xy=(self.start - (view.width / 200.),
                                    ymid),
                            fontsize=6, bbox=bbox_props,
                            verticalalignment='center', clip_on=True,
                            horizontalalignment='right')
                    ann.set_clip_box(ax.bbox)


class FeatureExon(Feature):
    pass
#    def __init__(self, *args, **kwargs):
#        kwargs['linewidth'] = 0
#        super(FeatureExon, self).__init__(*args, **kwargs)

class FeatureUTR(Feature):
    pass
