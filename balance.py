"""
file: balance.py
description: this program reads an input text file and encrypt/decrypt it
each line by another instruction text file
language: python3
author: Chenghui Zhu, Dongyu Wu
"""
from turtle import *
import sys

INITIAL_SCALE = 20    # The initial scale for all beams are set at 20 pixel
VERTICAL_LENGTH = 40  # The vertical length of a weight or a beam held by the
                      # upper beam drawn by turtle
VERTICAL_GAP = 15     # The vertical gap between a weight value and the beam
                      # holding it drawn by turtle

class Weight:
    """
    The Weight class represents a single weight on with a value and a
    relative position to its upper beam
    """
    __slots__ = "position", "value"

    def __init__(self, position, value):
        """
        Initialize a Weight class
        :param position: the relative position to its upper beam
        :param value: the mass of the weight
        """
        self.position = int(position)
        self.value = int(value)

    def total(self):
        """
        Calculating the total mass of the weight
        :return: the mass value
        """
        return self.value

    def is_unknow(self):
        """
        Determine if the weight is imply as an unknown weight (mass of -1)
        :return: true if this weight mass is unknown
        """
        return self.value == -1

    def length(self):
        """
        Caluculate the length of the weight (default as 0)
        :return: 0
        """
        return 0

    def right_length(self):
        """
        Caluculate the right part length of the weight (default as 0)
        :return: 0
        """
        return 0

    def left_length(self):
        """
        Caluculate the left part length of the weight (default as 0)
        :return: 0
        """
        return 0

    def draw(self):
        """
        Using turtle to draw the weight (a vertical line and
        an integer representing its mass) from its upper beam
        pre condition: pendown, the relative position of
        its upper beam, face down
        post condition: penup, the relative position of
        its upper beam, face down
        :return: None
        """
        pendown()
        forward(VERTICAL_LENGTH)
        penup()
        forward(VERTICAL_GAP)
        write(self.value, False, "center")
        backward(VERTICAL_LENGTH + VERTICAL_GAP)



class Beam:
    """
    The beam class represents a beam that can hold one or multiple
    beams or weight on its lower level
    """
    __slots__ = "name", "position", "scale", "hooks", "total_weight"

    def __init__(self, name, position = 0):
        """
        Initialize a beam class with the name and a default relative position
        of 0. The initial scale as how many pixels per unit of beam length
        (position) is set default but can be re-calculate. An empty list of
        hooks is used to hold all weights and beams on its lower level as its
        children. The initial total weight is set default as 0 but can be
        re-calculated.
        :param name: The name of the beam
        :param position: the relative position to the upper beam
        """
        self.name = name
        self.position = int(position)
        self.scale = INITIAL_SCALE
        self.hooks = []
        self.total_weight = 0

    def add(self, item):
        """
        The method of adding a weight or a beam to its lower level
        (the children list), based on the relative position to this beam
        :param item: the added weight or beam
        :return: None
        """
        if len(self.hooks) == 0 or item.position > self.hooks[-1].position:
            self.hooks.append(item)
        else:
            for i in range(len(self.hooks)):
                if item.position <= self.hooks[i].position:
                    self.hooks.insert(i, item)
                    break

    def total(self):
        """
        The method of calculating the total mass of its children
        beams and weights
        :return: the calculated total mass of the beam
        """
        self.total_weight = 0
        for item in self.hooks:
            self.total_weight += item.total()
        return self.total_weight

    def check_balance(self):
        """
        The method of checking if the beam is balanced (if its lower level
        children hold the balance)
        :return: true if the beam is balanced
        """
        check = 0
        for item in self.hooks:
            check += item.position * item.total()
        return check == 0

    def has_unknown(self):
        """
        The method to find if one of the children in its lower level is
        considered with an unknown value
        :return: true if one of the children is an unknown weight
        """
        result = False
        for item in self.hooks:
            if type(item) is Weight and item.is_unknow():
                result = True
                break
        return result

    def cal_unknown(self):
        """
        The method to calculate the mass value of the unknown weight
        :return: the regulated mass value
        """
        temp = 0
        unknown = None
        for item in self.hooks:
            if type(item) is Weight and item.is_unknow():
                unknown = item
                item.value = 0
            temp += item.position * item.total()
        unknown.value = int(abs(temp/unknown.position))
        return unknown.value

    def length(self):
        """
        The method of calculating the entire length of the beam, including the
        oversized length of its children (if have)
        :return: the total length of the beam
        """
        if len(self.hooks) > 1:
            return self.hooks[0].left_length() + self.scale * \
                   (self.hooks[-1].position - self.hooks[0].position) + \
                   self.hooks[-1].right_length()
        elif len(self.hooks) == 1:
            if self.hooks[0].position < 0 and self.hooks[0].right_length() >= \
                    -self.hooks[0].position * self.scale:
                return self.hooks[0].length()
            elif self.hooks[0].position < 0 and self.hooks[0].right_length() <\
                    -self.hooks[0].position * self.scale:
                return self.hooks[0].left_length() - \
                       self.hooks[0].position * self.scale
            elif self.hooks[0].position > 0 and self.hooks[0].left_length() >=\
                    self.hooks[0].position * self.scale:
                return self.hooks[0].length()
            elif self.hooks[0].position > 0 and self.hooks[0].left_length() < \
                    self.hooks[0].position * self.scale:
                return self.hooks[0].right_length() + \
                       self.hooks[0].position * self.scale

    def left_length(self):
        """
        The method of calculating the left half length of the beam, including
        the oversized length of its children (if have)
        :return: the left half length of the beam
        """
        return abs(self.scale * self.hooks[0].position) + \
               self.hooks[0].left_length()

    def right_length(self):
        """
        The method of calculating the right half length of the beam, including
        the oversized length of its children (if have)
        :return: the right half length of the beam
        """
        return abs(self.scale * self.hooks[-1].position) + \
               self.hooks[-1].right_length()

    def cal_scale(self):
        """
        The method of re-calculating the scale of the beam to ensure it did not
        overlap with other beam in turtle
        :return: None
        """
        gapList = []
        if len(self.hooks) > 1:
            for child in self.hooks:
                if type(child) is Beam:
                    child.cal_scale()
            for i in range(0, len(self.hooks)-1):
                gapList.append((self.hooks[i].right_length() +
                                self.hooks[i+1].left_length() + INITIAL_SCALE)
                               / (self.hooks[i+1].position -
                                  self.hooks[i].position))
            self.scale = max(gapList)
        elif len(self.hooks) == 1:
            self.scale = INITIAL_SCALE / abs(self.hooks[0].position)
        #return max(gapList)

    def is_root(self):
        """
        The method to determine if the beam is the root beam
        :return: true if the beam is root
        """
        return self.name.isalpha()

    def draw(self):
        """
        The method to draw from the beam to all its children weights and beams
        :return: None
        """
        #right(90)
        pendown()
        forward(VERTICAL_LENGTH)
        if len(self.hooks) > 1:
            right(90)
            forward(abs(self.scale * self.hooks[0].position))
            left(90)
            for i in range(0, len(self.hooks)-1):
                self.hooks[i].draw()
                left(90)
                pendown()
                forward(self.scale * (self.hooks[i+1].position -
                                      self.hooks[i].position))
                right(90)
            self.hooks[-1].draw()
            penup()
            right(90)
            forward(abs(self.scale * self.hooks[-1].position))
            left(90)
            backward(VERTICAL_LENGTH)
        elif len(self.hooks) == 1:
            if self.hooks[0].position <= 0:
                right(90)
                forward(abs(self.scale * self.hooks[0].position))
                left(90)
                self.hooks[0].draw()
                penup()
                left(90)
                forward(abs(self.scale * self.hooks[0].position))
                right(90)
                backward(VERTICAL_LENGTH)
            if self.hooks[0].position > 0:
                left(90)
                forward(abs(self.scale * self.hooks[0].position))
                right(90)
                self.hooks[0].draw()
                penup()
                right(90)
                forward(abs(self.scale * self.hooks[0].position))
                left(90)
                backward(VERTICAL_LENGTH)



    def __str__(self):
        result = "name: " + self.name + "\nitems: "
        for i in self.hooks:
            if type(i) is Weight:
                result += "\n" + str(i.position) + ", " + str(i.value)
            elif type(i) is Beam:
                result += "\n" + str(i.position) + ", " + i.name
        return result


def main():
    assert len(sys.argv) == 2, \
        "please provide a txt file for balance drawing"
    inputList = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line.strip()
            line = line.split(" ")
            assert len(line) % 2 != 0, "not valid input of weights and beams"
            inputList.append(line)
    tempList = []
    nameSet = set()
    for singleBeam in inputList:
        temp = None
        if singleBeam[0] in nameSet:
            for t in tempList:
                if t.name == singleBeam[0]:
                    temp = t
                    break
        else:
            temp = Beam(singleBeam[0])
            tempList.append(temp)
            nameSet.add(singleBeam[0])
        for i in range(1, len(singleBeam), 2):
            if not singleBeam[i + 1][0] == "B":
                temp.add(Weight(singleBeam[i], singleBeam[i + 1]))
            else:
                if singleBeam[i + 1] in nameSet:
                    for b in tempList:
                        if b.name == singleBeam[i + 1]:
                            b.position = int(singleBeam[i])
                            temp.add(b)
                            break
                else:
                    b = Beam(singleBeam[i + 1], singleBeam[i])
                    temp.add(b)
                    tempList.append(b)
                    nameSet.add(singleBeam[i + 1])
    for beam in tempList:
        if beam.has_unknown():
            print("the unknown weight is calculated as:", beam.cal_unknown())
    for i in tempList:
        if i.is_root():
            i.cal_scale()
            if i.check_balance():
                print("The puzzle is balanced!")
            else:
                print("The puzzle is unbalanced!")
            right(90)
            i.draw()
            mainloop()



if __name__ == "__main__":
    main()