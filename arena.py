import argparse
import math
import pprint
import random

class Arena:

    def __init__(self):

        self.arena = 6
        self.num_points = 4

        self.parseArguments()

        filename = "argos3/arena"+str(self.arena)+".txt"

        with open(filename, "w") as f:
            f.write("\n")
            f.write("layout "+str(self.arena)+" with "+str(self.num_points)+" points\n")
            f.write("\n")

        for i in range(10):

            self.points = []

            self.getPoints(i)
            self.getRadii()

            pprint.pprint(self.points)

            with open(filename, "a") as f:
                f.write("arena "+str(i)+"\n")
                for point in self.points:
                    f.write(str(point["x"])+" "+str(point["y"])+" "+str(point["r"])+"\n")

    def parseArguments(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--arena', type=int, default=None, help="Arena layout")
        parser.add_argument('--qty', type=int, default=None, help="How many POIs")
        args = parser.parse_args()

        if args.arena != None:
            self.arena = args.arena

        if args.qty != None:
            self.num_points = args.qty

    def getPoints(self, i):

        random.seed(i)

        limit = 20;
        valid = False

        for j in range(self.num_points):

            if self.arena == 6:
                x = (random.random() * 3.0) - 1.5
                y = (random.random() * 3.0) - 1.5
            else:
                x = (random.random() * 2.0) - 1.0
                y = (random.random() * 2.0) - 1.0
            
            counter = 0;
            valid = False
            while (not valid and counter < limit):

                counter += 1
                valid = True

                for k in range(len(self.points)):
                    hpt = self.hptSq(x, y, self.points[k]["x"], self.points[k]["y"])
                    if hpt < 1.5:
                        valid = False

                if not valid:
                    x = (random.random() * 3.0) - 1.5
                    y = (random.random() * 3.0) - 1.5

            if valid:
                self.points.append({"x":x, "y":y})

    def getRadii(self):

        for i in range(len(self.points)):

            radius = 5.0

            for j in range(len(self.points)):
                if i != j:
                    hpt = math.sqrt(self.hptSq(self.points[i]["x"], self.points[i]["y"], self.points[j]["x"], self.points[j]["y"]))
                    if (hpt / 2) + 0.2 < radius:
                        radius = hpt / 2
                self.points[i]["r"] = radius

        for i in range(len(self.points)):

            radius = 5.0

            for j in range(len(self.points)):
                if i != j:
                    hpt = math.sqrt(self.hptSq(self.points[i]["x"], self.points[i]["y"], self.points[j]["x"], self.points[j]["y"]))
                    remainder = (hpt - self.points[j]["r"]) - 0.2
                    if remainder < radius:
                        radius = remainder
            self.points[i]["r"] = radius

    def hptSq(self, x1, y1, x2, y2):
        horizontal = x2 - x1
        vertical = y2 - y1
        return (horizontal * horizontal) + (vertical * vertical)

if __name__ == "__main__":
    arena = Arena()

