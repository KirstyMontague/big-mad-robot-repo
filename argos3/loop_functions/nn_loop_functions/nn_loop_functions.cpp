#include "nn_loop_functions.h"

#include <argos3/plugins/simulator/entities/box_entity.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>

#include <controllers/footbot_nn/footbot_nn.h>

#include <sstream>
#include <list>
#include <algorithm>
#include <string>
#include <math.h>

using namespace std::chrono;

CNNLoopFunctions::CNNLoopFunctions() :
    m_pcFloor(NULL),
    m_count(0),
    m_experimentLength(0),
    m_gap(0.0)
{
    m_ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
}

CNNLoopFunctions::~CNNLoopFunctions() 
{
    milliseconds ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
    milliseconds cost = ms - m_ms;
    std::cout << "duration " << cost.count() << std::endl;

}

void CNNLoopFunctions::Init(TConfigurationNode& t_tree) 
{
    m_pcFloor = &GetSpace().GetFloorEntity();

    m_pcRNG = CRandom::CreateRNG("argos");;

    // get the filename for chromosome (best/chromosome)
    std::string filename;
    int index = 0;
    TConfigurationNodeIterator itDistr;
    for(itDistr = itDistr.begin(&t_tree); itDistr != itDistr.end(); ++itDistr) 
    {
        TConfigurationNode& tDistr = *itDistr;
        GetNodeAttribute(tDistr, "name", filename);
        GetNodeAttribute(tDistr, "index", index);
    }

    // get paths
    std::string pathFilename = "../path.txt";
    std::ifstream pathFile(pathFilename);
    std::string line = "";
    std::string hostPath = "";
    std::string localPath = "";
    while( getline(pathFile, line) )
    {
        int delimiter = line.find(":");
        std::string key = line.substr(0, delimiter);
        std::string value = line.substr(delimiter + 1);

        if (key == "host")
        {
            hostPath = value;
        }
        if (key == "local")
        {
            localPath = value;
        }
    }

    if (hostPath == "" || localPath == "")
    {
        std::cout << "hostPath: " << hostPath << "\n";
        std::cout << "localPath: " << localPath << "\n";
        return;
    }

     // get configuration from file
    std::string configFilename = hostPath+"/"+localPath+"/configuration.txt";
    std::ifstream configFile(configFilename);
    line = "";
    int numInputs = 0;
    int numHidden = 0;
    int numOutputs = 0;
    int trialLength = 0;
    int sqrtRobots = 0;
    while( getline(configFile, line) )
    {
        int delimiter = line.find(":");
        std::string key = line.substr(0, delimiter);
        std::string value = line.substr(delimiter + 1);

        if (key == "numInputs")
        {
            numInputs = std::stoi(value);
        }
        else if (key == "numHidden")
        {
            numHidden = std::stoi(value);
        }
        else if (key == "numOutputs")
        {
            numOutputs = std::stoi(value);
        }
        else if (key == "experimentLength")
        {
            m_experimentLength = std::stoi(value) * 8; // eight ticks per second
            trialLength = (std::stoi(value) * 8) / 5; // five trials per experiment
        }
        else if (key == "sqrtRobots")
        {
            sqrtRobots = std::stoi(value);
        }
    }

    if (numInputs == 0 || numOutputs == 0 || m_experimentLength == 0 || sqrtRobots == 0)
    {
        std::cout << "numInputs: " << std::to_string(numInputs) << "\n";
        std::cout << "numOutputs: " << std::to_string(numOutputs) << "\n";
        std::cout << "experimentLength: " << std::to_string(m_experimentLength) << "\n";
        std::cout << "sqrtRobots: " << std::to_string(sqrtRobots) << "\n";
        return;
    }

    size_t genomeSize = (numInputs * numHidden) + numHidden + (numHidden * numOutputs) + numOutputs;

    // get random seed and environmental parameters from file
    std::string seedFilename = hostPath+"/"+localPath+"/seed"+std::to_string(index)+".txt";
    std::ifstream seedFile(seedFilename);
    line = "";
    int seed = -1;
    while( getline(seedFile, line) )
    {
        if (seed == -1)
        {
            seed = std::stoi(line);
        }
        else
        {
            m_gap = std::stof(line);
        }
    }

    if (seed == -1 || m_gap == 0.0)
    {
        std::cout << "seed: " << std::to_string(seed) << "\n";
        std::cout << "m_gap: " << std::to_string(m_gap) << "\n";
        return;
    }

    m_pcRNG->SetSeed(seed);
    m_pcRNG->Reset();

    // read chromosome from file
    std::string chromosomeFilename = hostPath+"/"+localPath+"/"+filename;
    std::ifstream chromosomeFile(chromosomeFilename);
    line = "";
    Real* chromosome = new Real[genomeSize + 1];
    while( getline(chromosomeFile, line) )
    {
        {
            std::stringstream ss(line);
            std::string weight;
            std::vector<double> weights;
            while (std::getline(ss, weight, ' ')) 
            {
                weights.push_back(stod(weight));
            }
            for (size_t i = 0; i < weights.size(); ++i)
            {
                chromosome[i] = weights[i];
            }
        }
    }

    // add robots
    for (int i = 0; i < sqrtRobots; ++i)
    {
        for (int j = 0; j < sqrtRobots; ++j)
        {
            CFootBotEntity* pcFB = new CFootBotEntity(std::to_string(i*sqrtRobots+j), "fswc");
            m_footbots.push_back(pcFB);
            AddEntity(*pcFB);
            
            CVector3 cFBPos;
            CQuaternion cFBRot;	
        
            // rotation
            auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
            cFBRot.FromAngleAxis(r, CVector3::Z);
            
            // random positions
            CRange<Real> areaRange(-1.0, 1.0);
            for (int k = 0; k < 10; ++k)
            {
                double x = m_pcRNG->Uniform(areaRange) + 0.0;
                double y = m_pcRNG->Uniform(areaRange) + 0.0;
                cFBPos.Set(x, y, 0.0f);	
                
                // place robot
                if (MoveEntity(pcFB->GetEmbodiedEntity(), cFBPos, cFBRot))
                {
                    break;
                }
            }

            // create robot
            CFootBotNNController& controller = dynamic_cast<CFootBotNNController&>(pcFB->GetControllableEntity().GetController());
            controller.InitNN(chromosome, numInputs, numHidden, numOutputs);
            controller.createBlackBoard(sqrtRobots * sqrtRobots);
            controller.setParams(m_gap, trialLength);
        }
    }
}

CColor CNNLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    // distance from centre
    double r = sqrt((x * x) + (y * y));

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }
    else if (r < 0.5f) 
    {
        return CColor::GRAY50; // nest
    }
    else if (r < 0.5f + m_gap)
    {
        return CColor::WHITE; // gap
    }

    return CColor::GRAY50; // food
}

void CNNLoopFunctions::PostStep()
{
    m_count++;
    if (m_count % (m_experimentLength / 5) == 0)
    {
        for (CFootBotEntity* footbot : m_footbots)
        {
            CVector3 cFBPos;
            CQuaternion cFBRot;	
            
            // rotation
            auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
            cFBRot.FromAngleAxis(r, CVector3::Z);
            
            // random positions
            CRange<Real> areaRange(-1.0, 1.0);
            for (int k = 0; k < 10; ++k)
            {
                double x = m_pcRNG->Uniform(areaRange) + 0.0;
                double y = m_pcRNG->Uniform(areaRange) + 0.0;
                cFBPos.Set(x, y, 0.0f);	
                
                // place robot
                if (MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot))
                {
                    break;
                }
            }
        
        }
    }
}

bool CNNLoopFunctions::IsExperimentFinished()
{
    return (m_count >= m_experimentLength);
}

REGISTER_LOOP_FUNCTIONS(CNNLoopFunctions, "nn_loop_functions")
