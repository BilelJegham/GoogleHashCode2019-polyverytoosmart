# -*- coding: utf-8 -*-

class Library:


    def __init__(self,id, bs, time, skipCapacity, r=0 ):
        self.id = id
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

    def resetRatio(self, allBooks,dayMax, dayActuel):
        s,x = 0,0
        for j in range((dayMax-(self.timeSignup+dayActuel))*self.skipCapacity):
            if x < len(self.booksId):
                s += allBooks[self.booksId[x]]
                x+=1
            else:
                self.ratio = s
                return

        self.ratio = s