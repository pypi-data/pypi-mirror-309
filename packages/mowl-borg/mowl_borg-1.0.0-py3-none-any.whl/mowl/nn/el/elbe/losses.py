import torch as th
import numpy as np


def class_assertion_loss(data, class_embed, class_offset, ind_embed, margin, neg=False):
    c = class_embed(data[:, 0])
    off_c = th.abs(class_offset(data[:, 0]))
    i = ind_embed(data[:, 1])

    euc = th.abs(c - i)
    dst = th.reshape(th.linalg.norm(th.relu(euc - off_c + margin), axis=1), [-1, 1])
    return dst

def object_property_assertion_loss(data, rel_embed, ind_embed, margin, neg=False):
    subj = ind_embed(data[:, 0])
    rel = rel_embed(data[:, 1])
    obj = ind_embed(data[:, 2])
                                    
    euc = th.abs(subj + rel - obj)
    dst = th.reshape(th.linalg.norm(th.relu(euc + margin), axis=1), [-1, 1])
    return dst


    
def gci0_loss(data, class_embed, class_offset, margin, neg=False):
    c = class_embed(data[:, 0])
    d = class_embed(data[:, 1])

    off_c = th.abs(class_offset(data[:, 0]))
    off_d = th.abs(class_offset(data[:, 1]))

    euc = th.abs(c - d)
    dst = th.reshape(th.linalg.norm(th.relu(euc + off_c - off_d + margin), axis=1), [-1, 1])

    return dst

def gci0_bot_loss(data, class_offset, neg=False):
    off_c = th.abs(class_offset(data[:, 0]))
    loss = th.linalg.norm(off_c, axis=1)
    return loss

def gci1_loss(data, class_embed, class_offset, margin, neg=False):
    c = class_embed(data[:, 0])
    d = class_embed(data[:, 1])
    e = class_embed(data[:, 2])
    off_c = th.abs(class_offset(data[:, 0]))
    off_d = th.abs(class_offset(data[:, 1]))
    off_e = th.abs(class_offset(data[:, 2]))

    startAll = th.maximum(c - off_c, d - off_d)
    endAll = th.minimum(c + off_c, d + off_d)

    new_offset = th.abs(startAll - endAll) / 2

    cen1 = (startAll + endAll) / 2
    euc = th.abs(cen1 - e)

    dst = th.reshape(th.linalg.norm(th.relu(euc + new_offset - off_e + margin), axis=1),
                     [-1, 1]) + th.linalg.norm(th.relu(startAll - endAll), axis=1)
    return dst


def gci1_bot_loss(data, class_embed, class_offset, margin, neg=False):
    c = class_embed(data[:, 0])
    d = class_embed(data[:, 1])

    off_c = th.abs(class_offset(data[:, 0]))
    off_d = th.abs(class_offset(data[:, 1]))

    euc = th.abs(c - d)
    dst = th.reshape(th.linalg.norm(th.relu(-euc + off_c + off_d + margin), axis=1), [-1, 1])
    return dst


def gci2_loss(data, class_embed, class_offset, rel_embed, margin, neg=False):
    if neg:
        return gci2_loss_neg(data, class_embed, class_offset, rel_embed, margin)
    else:
        c = class_embed(data[:, 0])
        r = rel_embed(data[:, 1])
        d = class_embed(data[:, 2])

        off_c = th.abs(class_offset(data[:, 0]))
        off_d = th.abs(class_offset(data[:, 2]))

        euc = th.abs(c + r - d)
        dst = th.reshape(th.linalg.norm(th.relu(euc + off_c - off_d + margin), axis=1), [-1, 1])
        return dst

def gci2_score(*args, **kwargs):
    return gci2_loss(*args, **kwargs)

def gci2_loss_neg(data, class_embed, class_offset, rel_embed, margin):
    c = class_embed(data[:, 0])
    r = rel_embed(data[:, 1])
    d = class_embed(data[:, 2])

    off_c = th.abs(class_offset(data[:, 0]))
    off_d = th.abs(class_offset(data[:, 2]))

    euc = th.abs(c + r - d)
    dst = th.reshape(th.linalg.norm(th.relu(euc - off_c - off_d - margin), axis=1), [-1, 1])
    return dst


def gci3_loss(data, class_embed, class_offset, rel_embed, margin, neg=False):
    r = rel_embed(data[:, 0])
    c = class_embed(data[:, 1])
    d = class_embed(data[:, 2])

    off_c = th.abs(class_offset(data[:, 1]))
    off_d = th.abs(class_offset(data[:, 2]))

    euc = th.abs(c - r - d)
    dst = th.reshape(th.linalg.norm(th.relu(euc - off_c - off_d + margin), axis=1), [-1, 1])
    return dst



def gci3_bot_loss(data, class_offset, neg=False):
    off_c = th.abs(class_offset(data[:, 1]))
    loss = th.linalg.norm(off_c, axis=1)
    return loss
