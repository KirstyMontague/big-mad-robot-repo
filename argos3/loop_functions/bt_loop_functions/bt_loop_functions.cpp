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
   m_count(0) {
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
	TConfigurationNodeIterator itDistr;
	for(itDistr = itDistr.begin(&t_tree); itDistr != itDistr.end(); ++itDistr) 
	{
		TConfigurationNode& tDistr = *itDistr;
		GetNodeAttribute(tDistr, "name", filename);
		GetNodeAttribute(tDistr, "index", index);
	}

	// get random seed and environmental parameters from file
	std::cout << "../txt/seed"+std::to_string(index)+".txt" << std::endl;
	std::ifstream seedFile("../txt/seed"+std::to_string(index)+".txt");
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
	//std::cout << filename << std::endl;
	//std::cout << std::to_string(index) << std::endl;
	//std::cout << std::to_string(seed) << std::endl;
	//std::cout << std::to_string(m_gap) << std::endl;
		
	// read number of robots and chromosome from file
    std::ifstream chromosomeFile("../txt/"+filename);      
	int sqrtRobots = 0;
	std::string chromosome;
    while( getline(chromosomeFile, line) )
	{
		// number of robots
		if (sqrtRobots == 0)
		{
			sqrtRobots = std::stoi(line);
		}		
		// chromosome
		else
		{
			//std::cout << line << std::endl;
			line.erase(std::remove(line.begin(), line.end(), ','), line.end());
			
			std::replace( line.begin(), line.end(), '(', ' ');
			std::replace( line.begin(), line.end(), ')', ' ');
			
			chromosome = line;
			std::cout << chromosome << std::endl;
		}
	}
	
	// unpack sub-behaviours
	
    std::ifstream subBehavioursFile("../txt/sub-behaviours.txt");
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
	
	for (auto t : tokens)
	{
		std::cout << t << " ";
	}
	std::cout << std::endl;
	
	// add robots
	for (int i = 0; i < sqrtRobots; ++i)
	{
		for (int j = 0; j < sqrtRobots; ++j)
		{
			//std::cout << "add robots " << j << std::endl;
			CFootBotEntity* pcFB = new CFootBotEntity(std::to_string(i*sqrtRobots+j), "fswc");
			m_footbots.push_back(pcFB);
			AddEntity(*pcFB);
			
			CVector3 cFBPos;
			CQuaternion cFBRot;	
			
			// position
			//double x = ((double) i - floor(sqrtRobots / 2)) / 4;
			//double y = ((double) j - floor(sqrtRobots / 2)) / 4;
			//cFBPos.Set(x, y, 0.0f);	
			//cFBPos.Set(-1.0f,0.0f,0.0f); --- uncomment to hard code robot position
			
			// rotation
			auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
			cFBRot.FromAngleAxis(r, CVector3::Z);
			// cFBRot.FromAngleAxis(CRadians(), CVector3::Z); --- uncomment to hard code robot orientation
			
			// random positions
			CRange<Real> areaRange(-1.0, 1.0);
			for (int k = 0; k < 10; ++k)
			{
				//std::cout << std::to_string(k) << std::endl;
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
			CFootBotBT& controller = dynamic_cast<CFootBotBT&>(pcFB->GetControllableEntity().GetController());
			controller.buildTree(tokens);
			controller.createBlackBoard(sqrtRobots * sqrtRobots);
			controller.setParams(m_gap);
			//std::cout << filename << std::endl;
			if (filename == "best.txt")
			{
				controller.setPlayback(true);
			}
		}
	}

}

CColor CBTLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
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

void CBTLoopFunctions::PostStep()
{
	m_count++;
	if (m_count % 800 == 0) // evaluation time 160 for subbehaviours, 800 for foraging
	{      
		//std::cout <s< "poststep " << m_count << std::endl;
		for (CFootBotEntity* footbot : m_footbots)
		{
			CVector3 cFBPos;
			CQuaternion cFBRot;	
			
			// rotation
			auto r = m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
			cFBRot.FromAngleAxis(r, CVector3::Z);
			// cFBRot.FromAngleAxis(CRadians(), CVector3::Z); --- uncomment to hard code robot orientation
			
			// random positions
			CRange<Real> areaRange(-1.0, 1.0);
			for (int k = 0; k < 10; ++k)
			{
				//std::cout << std::to_string(k) << std::endl;
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

	
REGISTER_LOOP_FUNCTIONS(CBTLoopFunctions, "bt_loop_functions");
