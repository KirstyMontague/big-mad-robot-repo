
#include <iostream>
#include <fstream>
 
int main(int argc, char* argv[])
{
    std::string path = argv[argc - 2];
    std::string seed = argv[argc - 1];

    std::string chromosomeFilename = path+"/chromosome"+seed+".txt";
    std::ifstream chromosomeFile(chromosomeFilename);
    std::string line = "";
    std::string result = "";
    while( getline(chromosomeFile, line) )
    {
        result = line;
    }

    std::cout << result << "\n";
}

