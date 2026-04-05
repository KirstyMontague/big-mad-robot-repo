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
    m_commsRange(0),
    m_currentIteration(0),
    m_numIterations(0),
    m_experimentLength(0),
    m_formation("random"),
    m_arenaLayout(0),
    m_nest(0.0),
    m_food(0.0),
    m_offset(0.0),
    m_gap(0.0),
    m_error(false),
    m_message("")
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

    m_pcRNG = CRandom::CreateRNG("argos");

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

    std::string repertoireFilename = "";
    std::string project = "";
    std::string chromosome = "";
    float velocity = 0.0;

    if (readConfigFile(path, project, repertoireFilename, velocity) &&
        readSeedAndGap(path+"/seed"+std::to_string(index)+".txt") &&
        readChromosome(path+"/"+filename, chromosome) &&
        generateArenas())
    {
        std::map<std::string, std::vector<std::string>> subBehaviours;
        tokeniseSubbehaviors(repertoireFilename, subBehaviours);

        std::vector<std::string> tokens;

        if (project == "multi_food_foraging_with_subbehaviours")
        {
            tokeniseAgnosticChromosome(subBehaviours, chromosome, tokens);
        }
        else
        {
            tokeniseChromosome(subBehaviours, chromosome, tokens);
        }

        addRobots(tokens, project, velocity, (filename == "best.txt"));
    }
    else
    {
        m_error = true;
        std::cout << "error - "+m_message << "\n";
    }
}

bool CBTLoopFunctions::generateArenas()
{
    if (m_arenaLayout == 2)
    {
        std::vector<CFootBotBT::Poi> arena;

        CFootBotBT::Poi nest = CFootBotBT::Poi();
        nest.m_x = 0.0;
        nest.m_y = m_gap;
        nest.m_r = m_nest;
        arena.push_back(nest);

        CFootBotBT::Poi food = CFootBotBT::Poi();
        food.m_x = 0.0;
        food.m_y = m_gap * -1;
        food.m_r = m_food;
        arena.push_back(food);

        m_arenas.push_back(arena);
    }

    if (m_arenaLayout == 3)
    {
        std::vector<CFootBotBT::Poi> arena;

        CFootBotBT::Poi nest = CFootBotBT::Poi();
        nest.m_x = 0.0;
        nest.m_y = 0.0;
        nest.m_r = m_nest;
        arena.push_back(nest);

        CFootBotBT::Poi food = CFootBotBT::Poi();
        food.m_x = 0.0;
        food.m_y = (m_gap + m_food + m_nest);
        food.m_r = m_food;
        arena.push_back(food);

        m_arenas.push_back(arena);
    }

    if (m_arenaLayout == 5)
    {
        float x = 0.0;
        float y = 0.0;
        float gap = (m_gap / 2) + m_food;

        std::vector<CFootBotBT::Poi> arena;

        CFootBotBT::Poi nest = CFootBotBT::Poi();
        nest.m_x = x - gap;
        nest.m_y = y + gap;
        nest.m_r = m_food;
        arena.push_back(nest);

        CFootBotBT::Poi food1 = CFootBotBT::Poi();
        food1.m_x = x + gap;
        food1.m_y = y - gap;
        food1.m_r = m_food;
        arena.push_back(food1);

        CFootBotBT::Poi food2 = CFootBotBT::Poi();
        food2.m_x = x - gap;
        food2.m_y = y - gap;
        food2.m_r = m_food;
        arena.push_back(food2);

        CFootBotBT::Poi food3 = CFootBotBT::Poi();
        food3.m_x = x + gap;
        food3.m_y = y + gap;
        food3.m_r = m_food;
        arena.push_back(food3);

        m_arenas.push_back(arena);
    }

    if (!usingDynamicArena())
    {
        return true;
    }

    std::string filename = "./arena"+std::to_string(m_arenaLayout)+".txt";
    std::ifstream arenasFile(filename);
    std::string line = "";
    bool found = false;

    while( getline(arenasFile, line) )
    {
        if (line == "" || line.substr(0, 6) == "layout")
        {
            found = true;
            continue;
        }

        if (line.substr(0, 5) == "arena")
        {
            std::vector<CFootBotBT::Poi> arena;
            m_arenas.push_back(arena);
            continue;
        }

        int delimiter1 = line.find(" ");
        int delimiter2 = delimiter1 + line.substr(delimiter1 + 1).find(" ");

        std::string x = line.substr(0, delimiter1);
        std::string y = line.substr(delimiter1 + 1, delimiter2);
        std::string r = line.substr(delimiter2 + 1);

        CFootBotBT::Poi pf = CFootBotBT::Poi();
        pf.m_x = std::stod(x);
        pf.m_y = std::stod(y);
        pf.m_r = std::stod(r);
        m_arenas.back().push_back(pf);
    }

    if (!found)
    {
        m_message = "no arena";
    }

    return found;
}

bool CBTLoopFunctions::readConfigFile(const std::string& path, std::string& project, std::string& repertoireFilename, float& velocity)
{
    std::string configFilename = path+"/configuration.txt";
    std::ifstream configFile(configFilename);
    std::string line = "";
    while( getline(configFile, line) )
    {
        int delimiter = line.find(":");
        std::string key = line.substr(0, delimiter);
        std::string value = line.substr(delimiter + 1);

        if (key == "project")
        {
            project = value;
        }
        if (key == "sqrtRobots")
        {
            m_sqrtRobots = std::stoi(value);
        }
        if (key == "iterations")
        {
            m_numIterations = std::stoi(value);
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
        if (key == "formation")
        {
            m_formation = value;
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
        if (key == "velocity")
        {
            velocity = std::stof(value);
        }
    }

    if (project == "" || m_sqrtRobots == 0 || m_numIterations == 0 || m_experimentLength == 0 || repertoireFilename == "" ||
        m_arenaLayout == 0 || m_nest == 0.0 || m_food == 0.0 || m_commsRange == 0 || velocity == 0.0 ||
        (m_formation != "random" && m_formation != "lattice" && m_formation != "localised" && m_formation != "nest" && m_formation != "two_robots"))
    {
        std::cout << "cancelled\n";
        std::cout << "project: " << project << "\n";
        std::cout << "m_sqrtRobots: " << std::to_string(m_sqrtRobots) << "\n";
        std::cout << "iterations: " << std::to_string(m_numIterations) << "\n";
        std::cout << "experimentLength: " << std::to_string(m_experimentLength) << "\n";
        std::cout << "repertoireFilename: " << repertoireFilename << "\n";
        std::cout << "arenaLayout: " << std::to_string(m_arenaLayout) << "\n";
        std::cout << "nestRadius: " << std::to_string(m_nest) << "\n";
        std::cout << "foodRadius: " << std::to_string(m_food) << "\n";
        std::cout << "commsRange: " << std::to_string(m_commsRange) << "\n";
        std::cout << "velocity: " << std::to_string(velocity) << "\n";
        std::cout << "formation: " << m_formation << "\n";

        m_message = "config file";
        m_experimentLength = 0;
        return false;
    }

    if (m_arenaLayout == 1 && m_formation == "localised")
    {
        m_message = "localised formation is not compatible with arena 1";
        m_experimentLength = 0;
        return false;
    }

    if (m_arenaLayout == 4 && m_formation == "localised")
    {
        m_message = "localised formation is not compatible with arena 4";
        m_experimentLength = 0;
        return false;
    }
    if (m_arenaLayout == 4 && m_formation == "nest")
    {
        m_message = "in nest formation is not compatible with arena 4";
        m_experimentLength = 0;
        return false;
    }

    if (m_arenaLayout == 5 && m_nest != m_food)
    {
        m_message = "nest and food radii must match for arena 5";
        m_experimentLength = 0;
        return false;
    }


    return true;
}

bool CBTLoopFunctions::readSeedAndGap(const std::string& filename)
{
    // get random seed and environmental parameters from file
    std::ifstream seedFile(filename);
    std::string line = "";
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
        m_message = "seed file error";
        m_experimentLength = 0;
        return false;
    }

    return true;
}

bool CBTLoopFunctions::readChromosome(const std::string& filename, std::string& chromosome)
{
    // read chromosome from file
    std::ifstream chromosomeFile(filename);
    std::string line = "";
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
        m_message = "chromosome file error";
        m_experimentLength = 0;
        return false;
    }

    return true;
}

void CBTLoopFunctions::tokeniseSubbehaviors(const std::string& filename, std::map<std::string, std::vector<std::string>>& subBehaviours)
{
    // unpack sub-behaviours

    std::ifstream subBehavioursFile(filename);
    std::vector<std::string> subBehaviourTrees;
    std::string line;
    while( getline(subBehavioursFile, line) )
    {
        //std::cout << line << std::endl;
        line.erase(std::remove(line.begin(), line.end(), ','), line.end());
        
        std::replace( line.begin(), line.end(), '(', ' ');
        std::replace( line.begin(), line.end(), ')', ' ');
        
        subBehaviourTrees.push_back(line);
    }

    // tokenize subbehaviours

    for (std::string subbehaviour : subBehaviourTrees)
    {
        std::string name;
        std::vector<std::string> tokens;
        uint i = 0;
        
        std::stringstream ss(subbehaviour);
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
        subBehaviours.insert(subBehaviour);
    }
}

void CBTLoopFunctions::tokeniseChromosome(const std::map<std::string, std::vector<std::string>>& subBehaviours, const std::string& chromosome, std::vector<std::string>& tokens)
{
    std::stringstream ss(chromosome); 
    std::string token;
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
}

void CBTLoopFunctions::tokeniseAgnosticChromosome(std::map<std::string, std::vector<std::string>>& subBehaviours, const std::string& chromosome, std::vector<std::string>& tokens)
{
    std::stringstream ss(chromosome);
    std::string token;
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

            if (token.substr(0, 8) == "gotoFood")
            {
                std::string foodIndex = token.substr(8, 1);
                std::string version = token.substr(9);

                subBehaviour = true;
                tokens.push_back("successd");

                for (std::string subToken : subBehaviours["gotoNest" + version])
                {
                    subToken = (subToken == "ifInNest") ? "ifGotFood"+foodIndex : subToken;
                    subToken = (subToken == "ifNestToLeft") ? "ifFoodToLeft"+foodIndex : subToken;
                    subToken = (subToken == "ifNestToRight") ? "ifFoodToRight"+foodIndex : subToken;
                    tokens.push_back(subToken);
                }
            }

            if (!subBehaviour)
            {
                tokens.push_back(token);
            }
        }
    }
}

void CBTLoopFunctions::addRobots(const std::vector<std::string> tokens, const std::string& project, const uint velocity, bool playback)
{
    for (int i = 0; i < m_sqrtRobots; ++i)
    {
        for (int j = 0; j < m_sqrtRobots; ++j)
        {
            CFootBotEntity* pcFB = new CFootBotEntity(std::to_string(i*m_sqrtRobots+j), "fswc");
            m_footbots.push_back(pcFB);
            AddEntity(*pcFB);

            if (m_formation == "lattice")
            {
                latticeFormation(pcFB, i, j);
            }
            else if (m_formation == "localised")
            {
                localisedFormation(pcFB, i * m_sqrtRobots + j);
            }
            else if (m_formation == "nest")
            {
                inNestFormation(pcFB);
            }
            else if (m_formation == "two_robots")
            {
                twoRobotFormation(pcFB, j);
            }
            else
            {
                randomFormation(pcFB);
            }

            // create robot
            CFootBotBT& controller = dynamic_cast<CFootBotBT&>(pcFB->GetControllableEntity().GetController());
            controller.buildTree(tokens);
            controller.setArenaParams(m_arenaLayout, m_nest, m_food, m_gap);
            setArenaPOIs(pcFB);

            uint robotType = (i * m_sqrtRobots + j) % 2;
            //robotType = playback ? 0 : robotType;
            controller.setParams(project, m_commsRange, velocity, m_experimentLength / m_numIterations, robotType);

            if (m_formation == "two_robots" && j == 1)
            {
                break;
            }
        }
        if (m_formation == "two_robots")
        {
            break;
        }
    }
}

void CBTLoopFunctions::moveRobotsOutOfRange()
{
    for (int i = 0; i < m_sqrtRobots * m_sqrtRobots; ++i)
    {
        CVector3 cFBPos;
        CQuaternion cFBRot;

        cFBRot.FromAngleAxis(CRadians::ZERO - CRadians::PI_OVER_TWO, CVector3::Z);

        double x = 2.3;
        double y = 0.3 * i - 2.3;

        cFBPos.Set(x, y, 0.0f);

        CFootBotEntity* footbot = m_footbots[i];
        MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot);
    }
}

CColor CBTLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
    if (m_error)
    {
        return CColor::GRAY90;
    }

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
    else if (m_arenaLayout == 5)
    {
        return getFloorColorExp5(c_position_on_plane);
    }
    else if (m_arenaLayout == 6)
    {
        return getFloorColorExp6(c_position_on_plane);
    }
    else if (m_arenaLayout == 7)
    {
        return getFloorColorExp7(c_position_on_plane);
    }
    else if (m_arenaLayout == 8)
    {
        return getFloorColorExp8(c_position_on_plane);
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

    double gap = m_gap + m_food + m_nest;

    double x_plus_gap_sq  = (x + gap) * (x + gap);
    double y_plus_gap_sq  = (y + gap) * (y + gap);
    double x_minus_gap_sq = (x - gap) * (x - gap);
    double y_minus_gap_sq = (y - gap) * (y - gap);

    double rNest  = sqrt((x * x) + (y * y));
    double rFood1 = sqrt((x * x) + y_minus_gap_sq);
    double rFood2 = sqrt((x * x) + y_plus_gap_sq);
    double rFood3 = sqrt(x_plus_gap_sq + (y * y));
    double rFood4 = sqrt(x_minus_gap_sq + (y * y));

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (rNest < m_nest)
    {
        return CColor::RED; // nest
    }

    else if (rFood1 < m_food || rFood2 < m_food || rFood3 < m_food || rFood4 < m_food)
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

CColor CBTLoopFunctions::getFloorColorExp5(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    float gap = (m_gap / 2) + m_food;

    double x_plus_gap_sq  = (x + gap) * (x + gap);
    double y_plus_gap_sq  = (y + gap) * (y + gap);
    double x_minus_gap_sq = (x - gap) * (x - gap);
    double y_minus_gap_sq = (y - gap) * (y - gap);

    double rNest  = sqrt(x_plus_gap_sq + y_minus_gap_sq);
    double rFood1 = sqrt(x_minus_gap_sq + y_plus_gap_sq);
    double rFood2 = sqrt(x_plus_gap_sq + y_plus_gap_sq);
    double rFood3 = sqrt(x_minus_gap_sq + y_minus_gap_sq);

    if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (rNest < m_nest)
    {
        return CColor::RED; // nest
    }

    else if (rFood1 < m_food)
    {
        return CColor::GREEN; // food
    }

    else if (rFood2 < m_food)
    {
        return CColor::BLUE; // food
    }

    else if (rFood3 < m_food)
    {
        return CColor::PURPLE; // food
    }

    return CColor::GRAY90; // remaining space
}

CColor CBTLoopFunctions::getFloorColorExp6(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    const auto& points = m_arenas[m_currentIteration];

    CFootBotBT::Poi nest = points[0];
    CFootBotBT::Poi food1 = points[1];
    CFootBotBT::Poi food2 = points[2];
    CFootBotBT::Poi food3 = points[3];

    double distNest  = sqrt(hypotenuseSquared(x, y, nest.m_x,  nest.m_y));
    double distFood1 = sqrt(hypotenuseSquared(x, y, food1.m_x, food1.m_y));
    double distFood2 = sqrt(hypotenuseSquared(x, y, food2.m_x, food2.m_y));
    double distFood3 = sqrt(hypotenuseSquared(x, y, food3.m_x, food3.m_y));

    if (fmod(x*4, 1) == 0 || fmod(y*8, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (distNest < m_arenas[m_currentIteration][0].m_r)
    {
        return CColor::RED; // nest
    }

    else if (distFood1 < m_arenas[m_currentIteration][1].m_r)
    {
        return CColor::GREEN; // food
    }

    else if (distFood2 < m_arenas[m_currentIteration][2].m_r)
    {
        return CColor::BLUE; // food
    }

    else if (distFood3 < m_arenas[m_currentIteration][3].m_r)
    {
        return CColor::PURPLE; // food
    }

    return CColor::GRAY90; // remaining space
}

CColor CBTLoopFunctions::getFloorColorExp7(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    const auto& points = m_arenas[m_currentIteration];

    CFootBotBT::Poi nest = points[0];
    CFootBotBT::Poi food1 = points[1];

    double distNest  = sqrt(hypotenuseSquared(x, y, nest.m_x,  nest.m_y));
    double distFood1 = sqrt(hypotenuseSquared(x, y, food1.m_x, food1.m_y));

    if (fmod(x*4, 1) == 0 || fmod(y*8, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (x > 2.3 || x < -2.3 || y > 2.3 || y < -2.3)
    {
        return CColor::GRAY70; // out of spawn range
    }

    else if (distNest < m_arenas[m_currentIteration][0].m_r)
    {
        return CColor::RED; // nest
    }

    else if (distFood1 < m_arenas[m_currentIteration][1].m_r)
    {
        return CColor::GREEN; // food
    }

    return CColor::GRAY90; // remaining space
}

CColor CBTLoopFunctions::getFloorColorExp8(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    const auto& points = m_arenas[m_currentIteration];

    std::vector<CFootBotBT::Poi> nest;
    std::vector<CFootBotBT::Poi> food;
    for (uint i = 0; i < points.size(); ++i)
    {
        if (i % 2 == 0)
        {
            nest.push_back(points[i]);
        }
        else
        {
            food.push_back(points[i]);
        }
    }

    if (fmod(x*4, 1) == 0 || fmod(y*8, 1) == 0)
    {
        return CColor::GRAY80; // tile edges
    }

    else if (x > 2.3 || x < -2.3 || y > 2.3 || y < -2.3)
    {
        return CColor::GRAY70; // out of spawn range
    }

    else
    {
        for (const auto& point : nest)
        {
            if (hypotenuseSquared(x, y, point.m_x, point.m_y) < point.m_r * point.m_r)
            {
                return CColor::RED;
            }
        }

        for (const auto& point : food)
        {
            if (hypotenuseSquared(x, y, point.m_x, point.m_y) < point.m_r * point.m_r)
            {
                return CColor::GREEN;
            }
        }
    }

    return CColor::GRAY90; // remaining space
}

float CBTLoopFunctions::hypotenuseSquared(const float x1, const float y1, const float x2, const float y2) const
{
    float horizontal = x2 - x1;
    float vertical = y2 - y1;
    return (horizontal * horizontal) + (vertical * vertical);
}

void CBTLoopFunctions::PostStep()
{
    m_count++;

    if (m_count % (m_experimentLength / m_numIterations) == 0 && m_count < m_experimentLength)
    {
        m_currentIteration = floor(m_count / (m_experimentLength / m_numIterations));
        m_pcFloor->SetChanged();

        if (m_formation == "lattice")
        {
            postStepLattice();
        }
        else if (m_formation == "localised")
        {
            postStepLocalised();
        }
        else if (m_formation == "nest")
        {
            postStepInNest();
        }
        else if (m_formation == "two_robots")
        {
            postStepTwoRobots();
        }
        else
        {
            postStepRandom();
        }
    }
    if (m_error)
    {
        for (CFootBotEntity* footbot : m_footbots)
        {
            CFootBotBT& controller = dynamic_cast<CFootBotBT&>(footbot->GetControllableEntity().GetController());
            controller.error(m_message, m_error);
        }
    }
}

void CBTLoopFunctions::postStepRandom()
{
    moveRobotsOutOfRange();

    for (CFootBotEntity* footbot : m_footbots)
    {
        randomFormation(footbot);
        setArenaPOIs(footbot);
    }
}

void CBTLoopFunctions::postStepLattice()
{
    for (int i = 0; i < m_sqrtRobots; ++i)
    {
        for (int j = 0; j < m_sqrtRobots; ++j)
        {
            CFootBotEntity* footbot = m_footbots[i * m_sqrtRobots + j];
            latticeFormation(footbot, i, j);
            setArenaPOIs(footbot);
        }
    }
}

void CBTLoopFunctions::postStepLocalised()
{
    moveRobotsOutOfRange();

    for (int i = 0; i < m_sqrtRobots; ++i)
    {
        for (int j = 0; j < m_sqrtRobots; ++j)
        {
            CFootBotEntity* footbot = m_footbots[i * m_sqrtRobots + j];
            localisedFormation(footbot, i * m_sqrtRobots + j);
            setArenaPOIs(footbot);
        }
    }
}

void CBTLoopFunctions::postStepInNest()
{
    moveRobotsOutOfRange();

    for (CFootBotEntity* footbot : m_footbots)
    {
        inNestFormation(footbot);
        setArenaPOIs(footbot);
    }
}

void CBTLoopFunctions::postStepTwoRobots()
{
    for (int i = 0; i < 2; ++i)
    {
        CFootBotEntity* footbot = m_footbots[i];
        twoRobotFormation(footbot, i);

        setArenaPOIs(footbot);
    }
}

void CBTLoopFunctions::randomFormation(CFootBotEntity* footbot)
{
    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(r, CVector3::Z);

    CRange<Real> areaRange(-1.5, 1.5);
    for (int k = 0; k < 10; ++k)
    {
        double x = m_pcRNG->Uniform(areaRange) + 0.0;
        double y = m_pcRNG->Uniform(areaRange) + 0.0;

        cFBPos.Set(x, y, 0.0f);

        if (MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot))
        {
            return;
        }
    }

    m_error = true;
    std::cout << "Failed to place robot\n";
    m_message = "Failed to place robot";
}

void CBTLoopFunctions::latticeFormation(CFootBotEntity* footbot, int i, int j)
{
    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(r, CVector3::Z);

    double x = (double) i - floor(m_sqrtRobots / 2);
    double y = (double) j - floor(m_sqrtRobots / 2);

    if (m_sqrtRobots % 2 == 0)
    {
        x += 0.5;
        y += 0.5;
    }

    // determines the area covered, use
    // larger numbers for a smaller lattice
    x /= 1.0;
    y /= 1.0;

    cFBPos.Set(x, y, 0.0f);

    MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot);
}

void CBTLoopFunctions::localisedFormation(CFootBotEntity* footbot, int index)
{
    uint robotType = (index % 2 == 0) ? 0 : 1;
    uint iteration = (usingDynamicArena()) ? m_currentIteration : 0;

    CFootBotBT::Poi target = (robotType == 0)
        ? m_arenas[iteration][1]
        : m_arenas[iteration][0];

    double halfBoundaryEdge = std::max(sqrt((target.m_r * target.m_r) / 2), 0.5);

    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto rotation = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(rotation, CVector3::Z);

    double xMax = std::min(target.m_x + halfBoundaryEdge, 2.3);
    double xMin = std::max(target.m_x - halfBoundaryEdge, -2.3);
    double yMax = std::min(target.m_y + halfBoundaryEdge, 2.3);
    double yMin = std::max(target.m_y - halfBoundaryEdge, -2.3);

    CRange<Real> areaRangeX(xMin, xMax);
    CRange<Real> areaRangeY(yMin, yMax);

    for (int i = 0; i < 10; ++i)
    {
        double x = m_pcRNG->Uniform(areaRangeX);
        double y = m_pcRNG->Uniform(areaRangeY);

        cFBPos.Set(x, y, 0.0f);

        if (MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot))
        {
            return;
        }
    }

    m_error = true;
    std::cout << "Failed to place robot\n";
    m_message = "Failed to place robot";
}

void CBTLoopFunctions::inNestFormation(CFootBotEntity* footbot)
{
    CFootBotBT::Poi target = CFootBotBT::Poi();
    target.m_x = 0.0;
    target.m_y = 0.0;
    target.m_r = 0.5;

    if (usingArenaPOIs())
    {
        uint iteration = (usingDynamicArena()) ? m_currentIteration : 0;
        target.m_x = m_arenas[iteration][0].m_x;
        target.m_y = m_arenas[iteration][0].m_y;
        target.m_r = m_arenas[iteration][0].m_r;
    }

    double halfBoundaryEdge = std::max(sqrt((target.m_r * target.m_r) / 2), 0.5);

    CVector3 cFBPos;
    CQuaternion cFBRot;

    auto rotation = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
    cFBRot.FromAngleAxis(rotation, CVector3::Z);

    double xMax = std::min(target.m_x + halfBoundaryEdge, 2.3);
    double xMin = std::max(target.m_x - halfBoundaryEdge, -2.3);
    double yMax = std::min(target.m_y + halfBoundaryEdge, 2.3);
    double yMin = std::max(target.m_y - halfBoundaryEdge, -2.3);

    CRange<Real> areaRangeX(xMin, xMax);
    CRange<Real> areaRangeY(yMin, yMax);

    for (int i = 0; i < 10; ++i)
    {
        double x = m_pcRNG->Uniform(areaRangeX);
        double y = m_pcRNG->Uniform(areaRangeY);

        cFBPos.Set(x, y, 0.0f);

        if (MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot))
        {
            return;
        }
    }

    m_error = true;
    std::cout << "Failed to place robot\n";
    m_message = "Failed to place robot";
}

void CBTLoopFunctions::twoRobotFormation(CFootBotEntity* footbot, int index)
{
    CVector3 cFBPos;
    CQuaternion cFBRot;

    if (index == 0) cFBRot.FromAngleAxis(CRadians::ZERO - CRadians::PI_OVER_TWO, CVector3::Z);
    else cFBRot.FromAngleAxis(CRadians::ZERO + CRadians::PI_OVER_TWO, CVector3::Z);

    double x = -0.3;
    double y = -0.25;

    if (index == 0)
    {
        x = 0.3;
        y = 0.25;
    }

    cFBPos.Set(x, y, 0.0f);

    MoveEntity(footbot->GetEmbodiedEntity(), cFBPos, cFBRot);
}

void CBTLoopFunctions::setArenaPOIs(CFootBotEntity* footbot)
{
    if (usingDynamicArena())
    {
        CFootBotBT& controller = dynamic_cast<CFootBotBT&>(footbot->GetControllableEntity().GetController());
        controller.setArenaPOIs(m_arenas[m_currentIteration]);
    }
}

bool CBTLoopFunctions::usingDynamicArena()
{
    return (m_arenaLayout == 6 || m_arenaLayout == 7 || m_arenaLayout == 8);
}

bool CBTLoopFunctions::usingArenaPOIs()
{
    return (m_arenaLayout == 2 || m_arenaLayout == 3 || m_arenaLayout == 5 ||
            m_arenaLayout == 6 || m_arenaLayout == 7 || m_arenaLayout == 8);
}

bool CBTLoopFunctions::IsExperimentFinished()
{
    return (m_error || m_count >= m_experimentLength);
}

REGISTER_LOOP_FUNCTIONS(CBTLoopFunctions, "bt_loop_functions");
