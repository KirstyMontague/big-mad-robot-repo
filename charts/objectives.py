
class Objectives():

    def __init__(self):

        self.index = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.info = {
            "density" : {
                "name" : "density",
                "description" : "Increase neighbourhood density",
                "index" : 0,
                "identifier" : "d",
                "gp_url" : "../gp/results/density/",
                "qdpy_url": "../qdpy/test/density/",
                "mtc_url" : "../gp/results/density-nest-ifood/",
                "mti_url" : "../gp/results/density-nest-food/",
            },
            "nest" : {
                "name" : "nest",
                "description" : "Go to nest",
                "index" : 1,
                "identifier" : "n",
                "gp_url" : "../gp/results/nest/",
                "qdpy_url": "../qdpy/test/nest/",
                "mtc_url" : "../gp/results/density-nest-ifood/",
                "mti_url" : "../gp/results/density-nest-food/",
            },
            "food" : {
                "name" : "food",
                "description" : "Go to food",
                "index" : 2,
                "identifier" : "f",
                "gp_url" : "../gp/results/food/",
                "qdpy_url": "../qdpy/test/food/",
                "mtc_url" : "../gp/results/food-idensity-inest/",
                "mti_url" : "../gp/results/density-nest-food/",
            },
            "idensity" : {
                "name" : "idensity",
                "description" : "Reduce density",
                "index" : 3,
                "identifier" : "id",
                "gp_url" : "../gp/results/idensity/",
                "qdpy_url": "../qdpy/test/idensity/",
                "mtc_url": "../gp/results/food-idensity-inest/",
                "mti_url" : "../gp/results/idensity-inest-ifood/",
            },
            "inest" : {
                "name" : "inest",
                "description" : "Go away from nest",
                "index" : 4,
                "identifier" : "in",
                "gp_url" : "../gp/results/inest/",
                "qdpy_url": "../qdpy/test/inest/",
                "mtc_url": "../gp/results/food-idensity-inest/",
                "mti_url" : "../gp/results/idensity-inest-ifood/",
            },
            "ifood" : {
                "name" : "ifood",
                "description" : "Go away from food",
                "index" : 5,
                "identifier" : "if",
                "gp_url": "../gp/results/ifood/",
                "qdpy_url": "../qdpy/test/ifood/",
                "mtc_url": "../gp/results/density-nest-ifood/",
                "mti_url": "../gp/results/idensity-inest-ifood/",
            },
            "density-nest-food" : {
                "name" : "density-nest-food",
                "names" : ["density","nest","food"],
                "description" : ["Increase neighbourhood density", "Go to nest", "Go to food"],
                "mt_url": "../gp/test/density-nest-food/",
            },
            "foraging" : {
                "name" : "foraging",
                "description" : "Foraging",
                "identifier" : "",
                "foraging_baseline_url": "../gp/results/foraging/baseline/",
                "foraging_qd1_url": "../gp/results/foraging/repertoire-qd1-1000gen/",
                "foraging_qd8_url": "../gp/results/foraging/repertoire-qd8-1000gen/",
                "foraging_mt1_url": "../gp/results/foraging/repertoire-mt1-1000gen/",
                "foraging_mt8_url": "../gp/results/foraging/repertoire-mt8-1000gen/",
            },
        }
