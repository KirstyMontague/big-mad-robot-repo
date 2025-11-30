
class eaParams():

    def __init__(self):

        self.objectives = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        with open("/home/tests/skeleton/path.txt", "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "home": self.home_path = data[1][0:-1]
                if data[0] == "local": self.local_path = data[1][0:-1]
                if data[0] == "shared": self.shared_path = data[1][0:-1]
