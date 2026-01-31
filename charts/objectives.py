
class Objectives():

    def __init__(self):

        self.index = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.info = {
            "density" : {
                "name" : "density",
                "description" : "Increase neighbourhood density",
                "index" : 0,
            },
            "nest" : {
                "name" : "nest",
                "description" : "Go to nest",
                "index" : 1,
            },
            "food" : {
                "name" : "food",
                "description" : "Go to food",
                "index" : 2,
            },
            "idensity" : {
                "name" : "idensity",
                "description" : "Reduce neighbourhood density",
                "index" : 3,
            },
            "inest" : {
                "name" : "inest",
                "description" : "Go away from nest",
                "index" : 4,
            },
            "ifood" : {
                "name" : "ifood",
                "description" : "Go away from food",
                "index" : 5,
            },
            "ifood-perceived-position" : {
                "name" : "ifood-perceived-position",
                "description" : "Go away from food",
                "index" : 5,
            },
            "ifood-absolute-position" : {
                "name" : "ifood-absolute-position",
                "description" : "Go away from food",
                "index" : 5,
            },
            "foraging" : {
                "name" : "foraging",
                "description" : "Foraging",
                "index" : 6,
            },
        }
