import sh
from collections import defaultdict

import ruru.feature as ruf
import ruru.view as ruv


class Simple_gtf_feat(object):

    def __init__(self, line):
        self.line = line
        ls = line.strip().split("\t")
        self.chrom = ls[0]
        self.start = int(ls[3])
        self.orient = ls[6]
        self.stop = int(ls[4])
        self.type = ls[2]
        self.attrs = {}
        for kv in ls[8].strip().split(';'):
            kvs = kv.strip().split(" ", 1)
            if len(kvs) != 2:
                continue
            k, v = kvs
            v = v.strip('"')
            self.attrs[k] = v
        self.gene_id = self.attrs.get('transcript_id', '')
        self.gene_name = self.attrs.get('gene_name', '')

    def __str__(self):
        return ("%(chrom)s:%(type)s:%(start)d-%(stop)d:" +
                "%(orient)s (%(gene_id)s)") % self.__dict__


def featurelist_from_gtf(gtf_file, region):

    children = defaultdict(list)
    genes = {}

    for line in sh.tabix(gtf_file, region):
        f = Simple_gtf_feat(line)
        gid = f.gene_id
        if not gid:
            continue

        if f.type == 'gene':
            fg = ruf.FeatureGene(gid, f.start, f.stop, f.orient,
                                 label=True, gene_name=f.gene_name)
            genes[gid] = fg
        elif f.type == 'exon':
            fe = ruf.FeatureExon('', f.start, f.stop, linewidth=0.1,
                                 facecolor="green", gene_name=f.gene_name)
            children[gid].append(fe)
        elif f.type == 'UTR':
            fu = ruf.FeatureUTR('', f.start, f.stop, facecolor='lightgreen',
                                linewidth=0.1, gene_name=f.gene_name)
            children[gid].append(fu)

    for c in children:
        if not c in genes:
            #no gene found - create one!
            coords = []
            ori = '.'
            for ch in children[c]:
                coords.extend([ch.start, ch.stop])
                ori = ch.orientation
            gene = ruf.FeatureGene(c, min(coords), max(coords), ori,
                                   label=True,
                                   gene_name = children[c][0].gene_name)
            gene.children = children[c]
            genes[c] = gene
        else:
            genes[c].children = children[c]

    return genes.values()
