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
    m_gap(0.0)
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

    generateArenas();

    std::string repertoireFilename = "";
    float velocity = 0.0;
    readConfigFile(path, repertoireFilename, velocity);

    readSeedAndGap(path+"/seed"+std::to_string(index)+".txt");

    std::string chromosome = "";
    readChromosome(path+"/"+filename, chromosome);

    std::vector<std::string> tokens;
    tokeniseSubbehaviors(repertoireFilename, chromosome, tokens);

    addRobots(tokens, velocity, filename == "best.txt");
}

void CBTLoopFunctions::generateArenas()
{
    std::string arenasFilename = "./arena.txt";
    std::ifstream arenasFile(arenasFilename);
    std::string line = "";

    while( getline(arenasFile, line) )
    {
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
}

bool CBTLoopFunctions::readConfigFile(const std::string path, std::string& repertoireFilename, float& velocity)
{
    std::string configFilename = path+"/configuration.txt";
    std::ifstream configFile(configFilename);
    std::string line = "";
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

    if (m_sqrtRobots == 0 || m_numIterations == 0 || m_experimentLength == 0 || repertoireFilename == "" ||
        m_arenaLayout == 0 || m_nest == 0.0 || m_food == 0.0 || m_commsRange == 0 || velocity == 0.0 ||
        (m_formation != "random" && m_formation != "lattice" && m_formation != "two_robots"))
    {
        std::cout << "cancelled\n";
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
        m_experimentLength = 0;
        return false;
    }

    return true;
}

bool CBTLoopFunctions::readSeedAndGap(const std::string filename)
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
        m_experimentLength = 0;
        return false;
    }

    return true;
}

bool CBTLoopFunctions::readChromosome(const std::string filename, std::string& chromosome)
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
        m_experimentLength = 0;
        return false;
    }

    return true;
}

void CBTLoopFunctions::tokeniseSubbehaviors(const std::string filename, const std::string chromosome, std::vector<std::string>& tokens)
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

    std::vector<std::pair<std::string, std::vector<std::string>>> subBehaviours;
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
        subBehaviours.push_back(subBehaviour);
    }

    // tokenize chromosome
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

void CBTLoopFunctions::addRobots(const std::vector<std::string> tokens, const uint velocity, bool playback)
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
            controller.setArenaPOIs(m_arenas[m_currentIteration]);

            uint robotType = playback ? 0 : (i * m_sqrtRobots + j) % 2;
            controller.setParams(m_commsRange, velocity, m_experimentLength / m_numIterations, robotType);

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

CColor CBTLoopFunctions::getFloorColorExp5(const CVector2& c_position_on_plane)
{
    double x = c_position_on_plane.GetX();
    double y = c_position_on_plane.GetY();

    double x_plus_gap_sq = (x + m_gap + 0.05) * (x + m_gap + 0.05);
    double y_plus_gap_sq = (y + m_gap + 0.05) * (y + m_gap + 0.05);
    double x_minus_gap_sq = (x - (m_gap + 0.05)) * (x - (m_gap + 0.05));
    double y_minus_gap_sq = (y - (m_gap + 0.05)) * (y - (m_gap + 0.05));

    //double x_plus_offset_sq = (x + 0.1) * (x + 0.1);
    //double y_plus_offset_sq = (y + 0.1) * (y + 0.1);
    //double x_minus_offset_sq = (x - 0.1) * (x - 0.1);
    //double y_minus_offset_sq = (y - 0.1) * (y - 0.1);

    //double rNest = sqrt(x_minus_offset_sq + y_minus_gap_sq);
    //double rFood1 = sqrt(x_plus_offset_sq + y_plus_gap_sq);
    //double rFood2 = sqrt(x_plus_gap_sq + y_plus_offset_sq);
    //double rFood3 = sqrt(x_minus_gap_sq + y_minus_offset_sq);

    double rNest = sqrt((x * x) + y_minus_gap_sq);
    double rFood1 = sqrt((x * x) + y_plus_gap_sq);
    double rFood2 = sqrt(x_plus_gap_sq + (y * y));
    double rFood3 = sqrt(x_minus_gap_sq + (y * y));

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
        else if (m_formation == "two_robots")
        {
            postStepTwoRobots();
        }
        else
        {
            postStepRandom();
        }
    }
}

void CBTLoopFunctions::postStepRandom()
{
    for (CFootBotEntity* footbot : m_footbots)
    {
        randomFormation(footbot);
        CFootBotBT& controller = dynamic_cast<CFootBotBT&>(footbot->GetControllableEntity().GetController());
        controller.setArenaPOIs(m_arenas[m_currentIteration]);
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
            CFootBotBT& controller = dynamic_cast<CFootBotBT&>(footbot->GetControllableEntity().GetController());
            controller.setArenaPOIs(m_arenas[m_currentIteration]);
        }
    }
}

void CBTLoopFunctions::postStepTwoRobots()
{
    for (int i = 0; i < 2; ++i)
    {
        CFootBotEntity* footbot = m_footbots[i];
        twoRobotFormation(footbot, i);

        CFootBotBT& controller = dynamic_cast<CFootBotBT&>(footbot->GetControllableEntity().GetController());
        controller.setArenaPOIs(m_arenas[m_currentIteration]);
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
            break;
        }
    }
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

bool CBTLoopFunctions::IsExperimentFinished()
{
    return (m_count >= m_experimentLength);
}

REGISTER_LOOP_FUNCTIONS(CBTLoopFunctions, "bt_loop_functions");
