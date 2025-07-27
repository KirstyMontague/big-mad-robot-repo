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
    m_count(0)
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

    // get random seed and environmental parameters from file
    std::string seedFilename = "../cma-es/txt/seed"+std::to_string(index)+".txt";
    std::ifstream seedFile(seedFilename);
    std::string line = "";
    int seed = -1;
    int sqrtRobots = -1;
    while( getline(seedFile, line) )
    {
        if (seed == -1)
        {
            seed = std::stoi(line);
        }
        else if (sqrtRobots == -1)
        {
            sqrtRobots = std::stoi(line);
        }
        else
        {
            m_gap = std::stof(line);
        }
    }

    m_pcRNG->SetSeed(seed);
    m_pcRNG->Reset();

    // read chromosome from file
    std::ifstream chromosomeFile("../cma-es/txt/"+filename);
    Real* chromosome = new Real[GENOME_SIZE + 1];
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
            controller.InitNN(chromosome);
            controller.createBlackBoard(sqrtRobots * sqrtRobots);
            controller.setParams(m_gap);
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
    if (m_count % 160 == 0) // evaluation time 160 for subbehaviours, 800 for foraging
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

REGISTER_LOOP_FUNCTIONS(CNNLoopFunctions, "nn_loop_functions")
