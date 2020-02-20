# -*- coding: utf-8 -*-

class Library:


    def __init__(self, bs, time, skipCapacity, r=0 ):
        self.booksId = bs
        self.timeSignup = time
        self.skipCapacity = skipCapacity
        self.ratio = r

    def __str__(self):
        representation = str(self.booksId)
        representation += '\n'+str(self.timeSignup)
        representation +='\n'+str(self.skipCapacity)
        representation += '\n'+str(self.ratio)

        return representation
