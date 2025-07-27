
from ea import EA
ea = EA()

def main():
    #  ea.evaluateOneIndividual()
    pop = ea.eaInit(cxpb=0.6, mutpb=0.3)
    return

if __name__ == "__main__":
    main()
