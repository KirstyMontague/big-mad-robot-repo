#include "bt_loop_functions.h"

#include <argos3/plugins/simulator/entities/box_entity.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>

#include <controllers/footbot_bt/footbot_bt.h>

#include <sstream>
#include <list>
#include <algorithm>
#include <string>
#include <math.h>

using namespace std::chrono;

CBTLoopFunctions::CBTLoopFunctions() :
    m_pcFloor(NULL),
    m_count(0),
    m_sqrtRobots(0),
    m_iterations(0.0),
    m_nest(0.0),
    m_food(0.0),
    m_offset(0.0),
    m_commsRange(0),
    m_arenaLayout(0),
    m_gap(0.0),
    m_experimentLength(0)
{
    m_ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
    //std::cout << "start " << m_ms.count() << std::endl;
}

CBTLoopFunctions::~CBTLoopFunctions() 
{
    milliseconds ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
    //std::cout << ms.count() << std::endl;
    milliseconds cost = ms - m_ms;
    std::cout << "duration " << cost.count() << std::endl;
}

void CBTLoopFunctions::Init(TConfigurationNode& t_tree) 
{
    m_pcFloor = &GetSpace().GetFloorEntity();

    m_pcRNG = CRandom::CreateRNG("argos");;

    // get the filename for chromosome (best/chromosome)
    std::string filename;
    int index = 0;
    std::string path;
    TConfigurationNodeIterator itDistr;
    for(itDistr = itDistr.begin(&t_tree); itDistr != itDistr.end(); ++itDistr) 
    {
        TConfigurationNode& tDistr = *itDistr;
        GetNodeAttribute(tDistr, "name", filename);
        GetNodeAttribute(tDistr, "index", index);
        GetNodeAttribute(tDistr, "path", path);
    }

    // get configuration from file
    std::string configFilename = path+"/configuration.txt";
    std::ifstream configFile(configFilename);
    std::string line = "";
    std::string repertoireFilename = "";
    while( getline(configFile, line) )
    {
        int delimiter = line.find(":");
        std::string key = line.substr(0, delimiter);
        std::string value = line.substr(delimiter + 1);

        if (key == "sqrtRobots")
        {
            m_sqrtRobots = std::stoi(value);
        }
        if (key == "iterations")
        {
            m_iterations = std::stoi(value);
        }
        if (key == "experimentLength")
        {
            // eight ticks per second
            m_experimentLength = std::stoi(value) * 8;
        }
        if (key == "repertoireFilename")
        {
            repertoireFilename = value;
        }
        if (key == "arenaLayout")
        {
            m_arenaLayout = std::stoi(value);
        }
        if (key == "nestRadius")
        {
            m_nest = std::stof(value);
        }
        if (key == "foodRadius")
        {
            m_food = std::stof(value);
        }
        if (key == "commsRange")
        {
            m_commsRange = std::stoi(value);
        }
    }

    if (m_sqrtRobots == 0 || m_iterations == 0 || m_experimentLength == 0 || repertoireFilename == "" ||
        m_arenaLayout == 0 || m_nest == 0.0 || m_food == 0.0 || m_commsRange == 0)
    {
        std::cout << "cancelled\n";
        std::cout << "m_sqrtRobots: " << std::to_string(m_sqrtRobots) << "\n";
        std::cout << "iterations: " << std::to_string(m_iterations) << "\n";
        std::cout << "experimentLength: " << std::to_string(m_experimentLength) << "\n";
        std::cout << "repertoireFilename: " << repertoireFilename << "\n";
        std::cout << "arenaLayout: " << std::to_string(m_arenaLayout) << "\n";
        std::cout << "nestRadius: " << std::to_string(m_nest) << "\n";
        std::cout << "foodRadius: " << std::to_string(m_food) << "\n";
        std::cout << "commsRange: " << std::to_string(m_commsRange) << "\n";
        m_experimentLength = 0;
        return;
    }

    // get random seed and environmental parameters from file
    std::string seedFilename = path+"/seed"+std::to_string(index)+".txt";
    std::ifstream seedFile(seedFilename);
    line = "";
    int seed = -1;
    while( getline(seedFile, line) )
    {
        (seed == -1)
            ? seed = std::stoi(line)
            : m_gap = std::stof(line);
    }
    m_pcRNG->SetSeed(seed);
    m_pcRNG->Reset();

    if (seed == -1 || m_gap == 0.0)
    {
        std::cout << "cancelled\n";
        std::cout << "seed: " << std::to_string(seed) << "\n";
        std::cout << "gap: " << std::to_string(m_gap) << "\n";
        m_experimentLength = 0;
        return;
    }

    // read chromosome from file
    std::string chromosomeFilename = path+"/"+filename;
    std::ifstream chromosomeFile(chromosomeFilename);
    line = "";
    std::string chromosome;
    while( getline(chromosomeFile, line) )
    {
        //std::cout << line << std::endl;
        line.erase(std::remove(line.begin(), line.end(), ','), line.end());

        std::replace( line.begin(), line.end(), '(', ' ');
        std::replace( line.begin(), line.end(), ')', ' ');

        chromosome = line;
        std::cout << chromosome << std::endl;
    }

    if (chromosome == "")
    {
        std::cout << "cancelled\n";
        std::cout << "chromosome: " << chromosome << "\n";
        m_experimentLength = 0;
        return;
    }

    // unpack sub-behaviours

    std::ifstream subBehavioursFile(repertoireFilename);
    std::vector<std::string> subBehaviourTrees;
    while( getline(subBehavioursFile, line) )
    {
        //std::cout << line << std::endl;
        line.erase(std::remove(line.begin(), line.end(), ','), line.end());
        
        std::replace( line.begin(), line.end(), '(', ' ');
        std::replace( line.begin(), line.end(), ')', ' ');
        
        subBehaviourTrees.push_back(line);
    }

    // tokenize subbehaviours

    std::vector<std::pair<std::string, std::vector<std::string>>> subBehaviours;
    for (std::string chromosome : subBehaviourTrees)
    {
        std::string name;
        std::vector<std::string> tokens;
        uint i = 0;
        
        std::stringstream ss(chromosome); 
        std::string token;
        while (std::getline(ss, token, ' ')) 
        {
            if (token.length() > 0)
            {
                if (i == 0)
                {
                    name = token;
                    i = 1;
                }
                else
                {
                    tokens.push_back(token);
                }
            }
        }
        std::pair<std::string, std::vector<std::string>> subBehaviour(name, tokens);
        subBehaviours.push_back(subBehaviour);
    }

    // tokenize chromosome
    std::stringstream ss(chromosome); 
    std::string token;
    std::vector<std::string> tokens;
    while (std::getline(ss, token, ' ')) 
    {
        if (token.length() > 0)
        {
            bool subBehaviour = false;
            
            for (auto node : subBehaviours)
            {
                if (token == node.first)
                {
                    subBehaviour = true;
                    tokens.push_back("successd");
                    for (std::string subToken : node.second)
                    {
                        tokens.push_back(subToken);
                    }
                }
                     
            }
            
            if (!subBehaviour)
            {
                tokens.push_back(token);
            }
        }
    }   

    // add robots
    for (int i = 0; i < m_sqrtRobots; ++i)
    {
        for (int j = 0; j < m_sqrtRobots; ++j)
        {
            //std::cout << "add robots " << j << std::endl;
            CFootBotEntity* pcFB = new CFootBotEntity(std::to_string(i*m_sqrtRobots+j), "fswc");
            m_footbots.push_back(pcFB);
            AddEntity(*pcFB);

            //latticeFormation(pcFB, i, j);
            randomFormation(pcFB);

            // create robot
            CFootBotBT& controller = dynamic_cast<CFootBotBT&>(pcFB->GetControllableEntity().GetController());
            controller.buildTree(tokens);
            controller.createBlackBoard(m_sqrtRobots * m_sqrtRobots);
            controller.setParams(m_arenaLayout, m_nest, m_food, m_gap, m_commsRange, m_experimentLength / m_iterations);

            if (filename == "best.txt")
            {
                controller.setPlayback(true);
            }
        }
    }
}

CColor CBTLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
    if (m_arenaLayout == 2)
    {
        return getFloorColorExp2(c_position_on_plane);
    }
    else if (m_arenaLayout == 3)
    {
        return getFloorColorExp3(c_position_on_plane);
    }
    else if (m_arenaLayout == 4)
    {
        return getFloorColorExp4(c_position_on_plane);
    }
    else
    {
        return getFloorColorExp1(c_position_on_plane);
    }
}

CColor CBTLoopFunctions::getFloorColorExp1(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    // distance from centre
    double r = sqrt((x * x) + (y * y));

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }
    else if (r < m_nest)
    {
        return CColor::GRAY50; // nest
    }
    else if (r < 0.5f + m_gap)
    {
        return CColor::WHITE; // gap
    }

    return CColor::GRAY50; // food
}

CColor CBTLoopFunctions::getFloorColorExp2(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    double rNest = sqrt((x * x) + ((y - m_gap) * (y - m_gap)));
    double rFood = sqrt((x * x) + ((y + m_gap) * (y + m_gap)));

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (rNest < m_nest)
    {
        return CColor::RED; // nest
    }

    else if (rFood < m_food)
    {
        return CColor::GREEN; // food
    }

    return CColor::GRAY90; // remaining space
}

CColor CBTLoopFunctions::getFloorColorExp3(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    double foodX = x > 0.0 ? m_gap : m_gap * -1;
    double foodY = y > 0.0 ? m_gap : m_gap * -1;
    double rFood = sqrt(((x - foodX) * (x - foodX)) + ((y - foodY) * (y - foodY)));

    double rNest = sqrt((x * x) + (y * y));

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (rNest < m_nest)
    {
        return CColor::RED; // nest
    }

    else if (rFood < m_food)
    {
        return CColor::GREEN; // food
    }

    return CColor::GRAY90; // remaining space
}

CColor CBTLoopFunctions::getFloorColorExp4(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    if (y > m_gap / 2)
    {
        return CColor::RED; // nest
    }

    else if (y < m_gap / 2 * -1)
    {
        return CColor::GREEN; // food
    }

    return CColor::GRAY90; // remaining space
}

void CBTLoopFunctions::PostStep()
{
    postStepRandom();
}

void CBTLoopFunctions::postStepRandom()
{
    m_count++;
    if (m_count % (m_experimentLength / m_iterations) == 0)
    {
        for (CFootBotEntity* footbot : m_footbots)
        {
            randomFormation(footbot);
        }
    }
}

void CBTLoopFunctions::randomFormation(CFootBotEntity* footbot)
{
    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(r, CVector3::Z);

    CRange<Real> areaRange(-1.0, 1.0);
    for (int k = 0; k < 10; ++k)
    {
        double x = m_pcRNG->Uniform(areaRange) + 0.0;
        double y = m_pcRNG->Uniform(areaRange) + 0.0;
        cFBPos.Set(x, y, 0.0f);

        if (MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot))
        {
            break;
        }
    }
}

void CBTLoopFunctions::postStepLattice()
{
    m_count++;
    if (m_count % (m_experimentLength / m_iterations) == 0)
    {
        for (int i = 0; i < m_sqrtRobots; ++i)
        {
            for (int j = 0; j < m_sqrtRobots; ++j)
            {
                CFootBotEntity* footbot = m_footbots[i * m_sqrtRobots + j];
                latticeFormation(footbot, i, j);
            }
        }
    }
}

void CBTLoopFunctions::latticeFormation(CFootBotEntity* footbot, int i, int j)
{
    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(r, CVector3::Z);
    // cFBRot.FromAngleAxis(CRadians(), CVector3::Z); --- uncomment to hard code robot orientation

    double x = ((double) i - floor(m_sqrtRobots / 2)) / 1.2;
    double y = ((double) j - floor(m_sqrtRobots / 2)) / 1.2;
    cFBPos.Set(x, y, 0.0f);
    //cFBPos.Set(-1.0f,0.0f,0.0f); // --- uncomment to hard code robot position

    //std::cout << "add robots " << std::to_string(x) << " " << std::to_string(y) << std::endl;

    MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot);
}

bool CBTLoopFunctions::IsExperimentFinished()
{
    return (m_count >= m_experimentLength);
}

REGISTER_LOOP_FUNCTIONS(CBTLoopFunctions, "bt_loop_functions");
