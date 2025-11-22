
class Objectives():

    def __init__(self):

        with open("../path.txt", "r") as f:
            for line in f:
                data = line.split(":")
                if data[0] == "input": input_path = data[1][0:-1]
                if data[0] == "subbehaviours": subbehaviours_dir = data[1][0:-1]
                if data[0] == "foraging": foraging_dir = data[1][0:-1]

        gp_subbehaviours = input_path+"/gp/"+subbehaviours_dir
        qdpy_subbehaviours = input_path+"/qdpy/"+subbehaviours_dir
        foraging = input_path+"/gp/"+foraging_dir

        self.index = ["density", "nest", "food", "idensity", "inest", "ifood", "foraging"]

        self.info = {
            "density" : {
                "name" : "density",
                "description" : "Increase neighbourhood density",
                "index" : 0,
                "identifier" : "d",
                "gp_url" : gp_subbehaviours+"/density/",
                "qdpy_url": qdpy_subbehaviours+"/density/",
                "mtc_url" : gp_subbehaviours+"/density-nest-ifood/",
                "mti_url" : gp_subbehaviours+"/density-nest-food/",
            },
            "nest" : {
                "name" : "nest",
                "description" : "Go to nest",
                "index" : 1,
                "identifier" : "n",
                "gp_url" : gp_subbehaviours+"/nest/",
                "qdpy_url": qdpy_subbehaviours+"/nest/",
                "mtc_url" : gp_subbehaviours+"/density-nest-ifood/",
                "mti_url" : gp_subbehaviours+"/density-nest-food/",
            },
            "food" : {
                "name" : "food",
                "description" : "Go to food",
                "index" : 2,
                "identifier" : "f",
                "gp_url" : gp_subbehaviours+"/food/",
                "qdpy_url": qdpy_subbehaviours+"/food/",
                "mtc_url" : gp_subbehaviours+"/food-idensity-inest/",
                "mti_url" : gp_subbehaviours+"/density-nest-food/",
            },
            "idensity" : {
                "name" : "idensity",
                "description" : "Reduce density",
                "index" : 3,
                "identifier" : "id",
                "gp_url" : gp_subbehaviours+"/idensity/",
                "qdpy_url": qdpy_subbehaviours+"/idensity/",
                "mtc_url" : gp_subbehaviours+"/food-idensity-inest/",
                "mti_url" : gp_subbehaviours+"/idensity-inest-ifood/",
            },
            "inest" : {
                "name" : "inest",
                "description" : "Go away from nest",
                "index" : 4,
                "identifier" : "in",
                "gp_url" : gp_subbehaviours+"/inest/",
                "qdpy_url": qdpy_subbehaviours+"/inest/",
                "mtc_url" : gp_subbehaviours+"/food-idensity-inest/",
                "mti_url" : gp_subbehaviours+"/idensity-inest-ifood/",
            },
            "ifood" : {
                "name" : "ifood",
                "description" : "Go away from food",
                "index" : 5,
                "identifier" : "if",
                "gp_url" : gp_subbehaviours+"/ifood/",
                "qdpy_url": qdpy_subbehaviours+"/ifood/",
                "mtc_url" : gp_subbehaviours+"/density-nest-ifood/",
                "mti_url" : gp_subbehaviours+"/idensity-inest-ifood/",
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
                "index" : 6,
                "identifier" : "",
                "foraging_baseline_url":    foraging+"/nest50/baseline/",
                "foraging_qd1_url":         foraging+"/nest50/qd1/",
                "foraging_qd8_url":         foraging+"/nest50/qd8/",
                "foraging_qd64_url":        foraging+"/nest50/qd64/",
                "foraging_mt1_url":         foraging+"/nest50/mt1/",
                "foraging_mt8_url":         foraging+"/nest50/mt8/",
                "foraging_mt64_url":        foraging+"/nest50/mt64/",
                "foraging_baseline_04_url": foraging+"/nest40/baseline/",
                "foraging_qd1_04_url":      foraging+"/nest40/qd1/",
                "foraging_qd8_04_url":      foraging+"/nest40/qd8/",
                "foraging_qd64_04_url":     foraging+"/nest40/qd64/",
                "foraging_baseline_06_url": foraging+"/nest60/baseline/",
                "foraging_qd1_06_url":      foraging+"/nest60/qd1/",
                "foraging_qd8_06_url":      foraging+"/nest60/qd8/",
                "foraging_qd64_06_url":     foraging+"/nest60/qd64/",
            },
        }
