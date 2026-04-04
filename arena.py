import argparse
import math
import pprint
import random

class Arena:

    def __init__(self):

        self.arena = 6
        self.num_points = 4

        self.parseArguments()

        if self.num_points < 4:
            self.spawn_range = 2.5
            self.min_radius_sq = 1.5
            self.minimum_gap = 0.2
        elif self.num_points < 6:
            self.spawn_range = 3.0
            self.min_radius_sq = 1.5
            self.minimum_gap = 0.15
        else:
            self.spawn_range = 4.0
            self.min_radius_sq = 0.5
            self.minimum_gap = 0.1

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
            print()

            if len(self.points) < self.num_points:
                print("\nMissing points\n\n")
                break

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

            x = (random.random() * self.spawn_range) - (self.spawn_range / 2)
            y = (random.random() * self.spawn_range) - (self.spawn_range / 2)

            counter = 0;
            valid = False
            while (not valid and counter < limit):

                counter += 1
                valid = True

                for k in range(len(self.points)):
                    hpt = self.hptSq(x, y, self.points[k]["x"], self.points[k]["y"])
                    if hpt < self.min_radius_sq:
                        valid = False

                if not valid:
                    x = (random.random() * self.spawn_range) - (self.spawn_range / 2)
                    y = (random.random() * self.spawn_range) - (self.spawn_range / 2)

            if valid:
                self.points.append({"x":x, "y":y})

    def getRadii(self):

        for i in range(len(self.points)):

            radius = 5.0

            for j in range(len(self.points)):
                if i != j:
                    hpt = math.sqrt(self.hptSq(self.points[i]["x"], self.points[i]["y"], self.points[j]["x"], self.points[j]["y"]))
                    if (hpt / 2) + self.minimum_gap < radius:
                        radius = hpt / 2
                self.points[i]["r"] = radius

        for i in range(len(self.points)):

            radius = 5.0

            for j in range(len(self.points)):
                if i != j:
                    hpt = math.sqrt(self.hptSq(self.points[i]["x"], self.points[i]["y"], self.points[j]["x"], self.points[j]["y"]))
                    remainder = (hpt - self.points[j]["r"]) - self.minimum_gap
                    if remainder < radius:
                        radius = remainder
            self.points[i]["r"] = radius

    def hptSq(self, x1, y1, x2, y2):
        horizontal = x2 - x1
        vertical = y2 - y1
        return (horizontal * horizontal) + (vertical * vertical)

if __name__ == "__main__":
    arena = Arena()

