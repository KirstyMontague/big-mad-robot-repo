
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu

class Analysis():

    def getBestFromCSV(self):
        
        filename = "./results/density/gen1000.csv"
        f = open(filename, "r")

        data = [[]]
        fitness_index = -1
        

        for line in f:
            
            if len(data[-1]) >= 15:
                data.append([])
            
            columns = line.split(",")

            if columns[0] == "description":
                for i in range(len(columns)):
                    if columns[i] == "fitness":
                        fitness_index = i
                        print(fitness_index)

            else:
                if fitness_index != -1:
                    data[-1].append(float(columns[fitness_index]))
                    
        return data

    def checkHypothesis(self, data1, data2):
        
        data1_normal = shapiro(data1)
        data2_normal = shapiro(data2)
        
        both_normal = True if data1_normal.pvalue > 0.05 and data2_normal.pvalue > 0.05 else False
        
        if both_normal:
            ttest = ttest_ind(data1, data2)
            print ("ttest "+str(ttest.pvalue))
        else:
            ttest = mannwhitneyu(data1, data2)
            print ("mwu "+str(ttest.pvalue))

        return ttest


    def drawBestOneGeneration(self):

        data = self.getBestFromCSV()
        
        for d in data:
            print(len(d))
        
        if len(data) == 2: ttest = self.checkHypothesis(data[0], data[1])
        
        if len(data) > 2:
            print ("")
            for i in range(1, len(data)):
                self.checkHypothesis(data[0], data[i])
                ttest = ttest_ind(data[0], data[i])
            print ("")

        title = "CMA-ES to 1000 gen \n\n"
        labels = ["NN", "BT"]


        plot_width = 4 + len(data)
        
        fig, ax = plt.subplots(figsize=(plot_width, 6))
        plt.subplots_adjust(wspace=.3, hspace=0.4, bottom=0.1, top=0.99, left=0.15)
        
        plots = ax.boxplot(data, medianprops=dict(color='#000000'), patch_artist=True, labels=labels)
        
        ax.tick_params(axis='x', labelsize=14)
        ax.tick_params(axis='y', labelsize=13)

        #  plt.savefig(filename)
        plt.show()

    def getGPresults(self):
        
        # print results from a csv generated with gp to the console, they need
        # added to the same csv file as the nn results for drawBestOneGeneration
        
        filename = "../gp/results/density/best1000.csv"
        f = open(filename, "r")

        data = [[]]
        fitness_index = -1
        

        for line in f:
            
            columns = line.split(",")

            if columns[0] == "Type":
                for i in range(len(columns)):
                    if columns[i] == "1000":
                        fitness_index = i
                        print(fitness_index)

            else:
                if fitness_index != -1:
                    data[-1].append(float(columns[fitness_index]))
                    
        for d in data[0]:
            print(d)


analysis = Analysis()

# analysis.drawBestOneGeneration()
analysis.getGPresults()
