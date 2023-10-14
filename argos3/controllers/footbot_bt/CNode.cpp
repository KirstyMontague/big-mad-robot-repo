#include "CNode.h"

#include <sstream>
#include <bits/stdc++.h> 
#include <stdlib.h> 



CNode::CNode(std::string word)
{
	m_data = std::stof(word);
}

CNode::CNode(std::vector<std::string>& chromosome, int id) : m_ptr(0), m_type(nodetype::blank)
{
	//getRandomNumber(id, true);
	
	if (chromosome.size() > 0)
	{
		std::string word = chromosome.at(0);
		//std::cout << word << std::endl;
		//std::cout << word << " - ";
		
		m_type = getNodeFromText(word);
		nodetypes type = getNodeType(m_type);
		
		//std::cout << getNodeText(m_type) << std::endl;
		
		
		chromosome.erase(chromosome.begin());
			
		switch (type)
		{
			case nodetypes::composition:
			{
				compositionNode(chromosome, id);
				break;
			}
			case nodetypes::decorator:
			{
				decoratorNode(chromosome, id);
				break;
			}
			case nodetypes::condition:
			{
				conditionNode(chromosome);
				break;
			}
			case nodetypes::action:
			{
				actionNode(chromosome);
				break;
			}
			default: {
				std::cout << "node error (constructor)" << std::endl;
			}
		}
	}
}

//int CNode::getRandomNumber(int id, bool set)
//{
	//if (set)
	//{
		//std::srand(id);
	//}
	//int r = std::rand();
	//std::cout << r << std::endl;
	//return r;
//}

void CNode::compositionNode(std::vector<std::string>& chromosome, int id)
{
	switch (m_type)
	{
		case nodetype::seqm2:
		case nodetype::selm2:
		case nodetype::probm2:
		{
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		case nodetype::seqm3:
		case nodetype::selm3:
		case nodetype::probm3:
		{
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		case nodetype::seqm4:
		case nodetype::selm4:
		case nodetype::probm4:
		{
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		default: {
			std::cout << "node error (compositionNode)" << std::endl;
		}
	}
	
	if (m_type == nodetype::probm2 || m_type == nodetype::probm3 || m_type == nodetype::probm4)
	{
		m_ptr = 0;
		//m_ptr = std::rand() % m_children.size();
		//m_ptr = getRandomNumber(0, false) % m_children.size();
	}
}

void CNode::decoratorNode(std::vector<std::string>& chromosome, int id)
{
	switch (m_type)
	{
		case nodetype::repeat:
		{
			m_children.push_back(new CNode(chromosome, id));			
			m_children.push_back(new CNode(chromosome.at(0)));
			chromosome.erase(chromosome.begin());
			break;
			
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		case nodetype::successd:
		{
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		case nodetype::failured:
		{
			m_children.push_back(new CNode(chromosome, id));
			break;
		}
		default: {
			std::cout << "node error (decoratorNode)" << std::endl;
		}
	}
}

void CNode::conditionNode(std::vector<std::string>& chromosome)
{
	switch (m_type)
	{
		case nodetype::ifOnFood: // carrying food bug
		case nodetype::ifGotFood:
		case nodetype::ifInNest:
		case nodetype::ifNestToLeft:
		case nodetype::ifNestToRight:
		case nodetype::ifFoodToLeft:
		case nodetype::ifFoodToRight:
		case nodetype::ifRobotAhead:
		case nodetype::ifRobotToLeft:
		case nodetype::ifRobotToRight:
		case nodetype::ifOnFood1:
		case nodetype::ifOnFood2:
		case nodetype::ifOnFood3:
		case nodetype::ifOnFood4:
		case nodetype::ifOnFood5:
		case nodetype::ifOnFood6:
		case nodetype::ifOnFood7:
		case nodetype::ifOnFood8:
		case nodetype::ifGotFood1:
		case nodetype::ifGotFood2:
		case nodetype::ifGotFood3:
		case nodetype::ifGotFood4:
		case nodetype::ifGotFood5:
		case nodetype::ifGotFood6:
		case nodetype::ifGotFood7:
		case nodetype::ifGotFood8:
		case nodetype::ifInNest1:
		case nodetype::ifInNest2:
		case nodetype::ifInNest3:
		case nodetype::ifInNest4:
		case nodetype::ifInNest5:
		case nodetype::ifInNest6:
		case nodetype::ifInNest7:
		case nodetype::ifInNest8:
		case nodetype::ifNestToLeft1:
		case nodetype::ifNestToLeft2:
		case nodetype::ifNestToLeft3:
		case nodetype::ifNestToLeft4:
		case nodetype::ifNestToLeft5:
		case nodetype::ifNestToLeft6:
		case nodetype::ifNestToLeft7:
		case nodetype::ifNestToLeft8:
		case nodetype::ifNestToRight1:
		case nodetype::ifNestToRight2:
		case nodetype::ifNestToRight3:
		case nodetype::ifNestToRight4:
		case nodetype::ifNestToRight5:
		case nodetype::ifNestToRight6:
		case nodetype::ifNestToRight7:
		case nodetype::ifNestToRight8:
		case nodetype::ifFoodToLeft1:
		case nodetype::ifFoodToLeft2:
		case nodetype::ifFoodToLeft3:
		case nodetype::ifFoodToLeft4:
		case nodetype::ifFoodToLeft5:
		case nodetype::ifFoodToLeft6:
		case nodetype::ifFoodToLeft7:
		case nodetype::ifFoodToLeft8:
		case nodetype::ifFoodToRight1:
		case nodetype::ifFoodToRight2:
		case nodetype::ifFoodToRight3:
		case nodetype::ifFoodToRight4:
		case nodetype::ifFoodToRight5:
		case nodetype::ifFoodToRight6:
		case nodetype::ifFoodToRight7:
		case nodetype::ifFoodToRight8:
		case nodetype::ifRobotToLeft1:
		case nodetype::ifRobotToLeft2:
		case nodetype::ifRobotToLeft3:
		case nodetype::ifRobotToLeft4:
		case nodetype::ifRobotToLeft5:
		case nodetype::ifRobotToLeft6:
		case nodetype::ifRobotToLeft7:
		case nodetype::ifRobotToLeft8:
		case nodetype::ifRobotToRight1:
		case nodetype::ifRobotToRight2:
		case nodetype::ifRobotToRight3:
		case nodetype::ifRobotToRight4:
		case nodetype::ifRobotToRight5:
		case nodetype::ifRobotToRight6:
		case nodetype::ifRobotToRight7:
		case nodetype::ifRobotToRight8:
		{
			break;
		}
		default: {
			std::cout << "node error (conditionNode)" << std::endl;
		}
	}
}

void CNode::actionNode(std::vector<std::string>& chromosome)
{
	switch (m_type)
	{
		case nodetype::stop:
		case nodetype::f:
		case nodetype::fl:
		case nodetype::fr:
		case nodetype::r:
		case nodetype::rl:
		case nodetype::rr:
		{
			break;
		}		
		default: {
			std::cout << "node error (actionNode)" << std::endl;
		}
	}
}

std::string CNode::evaluate(CBlackBoard* blackBoard, std::string& output)
{	
	switch (m_type)
	{
		case CNode::nodetype::seqm2:
		case CNode::nodetype::seqm3:
		case CNode::nodetype::seqm4:
		case CNode::nodetype::selm2:
		case CNode::nodetype::selm3:
		case CNode::nodetype::selm4:
		case CNode::nodetype::probm2:
		case CNode::nodetype::probm3:
		case CNode::nodetype::probm4:
		{
			return evaluateCompositionNode(blackBoard, output);
		}
		
		case CNode::nodetype::successd:
		{
			return evaluateDecoratorNode(blackBoard, output);
		}
		
		case CNode::nodetype::stop:
		case CNode::nodetype::f:
		case CNode::nodetype::fl:
		case CNode::nodetype::fr:
		case CNode::nodetype::r:
		case CNode::nodetype::rl:
		case CNode::nodetype::rr:
		{
			return evaluateActionNode(blackBoard, output);
		}
		
		case CNode::nodetype::ifOnFood: // carrying food bug
		case CNode::nodetype::ifGotFood:
		case CNode::nodetype::ifInNest:
		case CNode::nodetype::ifNestToLeft:
		case CNode::nodetype::ifNestToRight:
		case CNode::nodetype::ifFoodToLeft:
		case CNode::nodetype::ifFoodToRight:
		case CNode::nodetype::ifRobotAhead:
		case CNode::nodetype::ifRobotToLeft:
		case CNode::nodetype::ifRobotToRight:
		case nodetype::ifOnFood1:
		case nodetype::ifOnFood2:
		case nodetype::ifOnFood3:
		case nodetype::ifOnFood4:
		case nodetype::ifOnFood5:
		case nodetype::ifOnFood6:
		case nodetype::ifOnFood7:
		case nodetype::ifOnFood8:
		case nodetype::ifGotFood1:
		case nodetype::ifGotFood2:
		case nodetype::ifGotFood3:
		case nodetype::ifGotFood4:
		case nodetype::ifGotFood5:
		case nodetype::ifGotFood6:
		case nodetype::ifGotFood7:
		case nodetype::ifGotFood8:
		case nodetype::ifInNest1:
		case nodetype::ifInNest2:
		case nodetype::ifInNest3:
		case nodetype::ifInNest4:
		case nodetype::ifInNest5:
		case nodetype::ifInNest6:
		case nodetype::ifInNest7:
		case nodetype::ifInNest8:
		case nodetype::ifNestToLeft1:
		case nodetype::ifNestToLeft2:
		case nodetype::ifNestToLeft3:
		case nodetype::ifNestToLeft4:
		case nodetype::ifNestToLeft5:
		case nodetype::ifNestToLeft6:
		case nodetype::ifNestToLeft7:
		case nodetype::ifNestToLeft8:
		case nodetype::ifNestToRight1:
		case nodetype::ifNestToRight2:
		case nodetype::ifNestToRight3:
		case nodetype::ifNestToRight4:
		case nodetype::ifNestToRight5:
		case nodetype::ifNestToRight6:
		case nodetype::ifNestToRight7:
		case nodetype::ifNestToRight8:
		case nodetype::ifFoodToLeft1:
		case nodetype::ifFoodToLeft2:
		case nodetype::ifFoodToLeft3:
		case nodetype::ifFoodToLeft4:
		case nodetype::ifFoodToLeft5:
		case nodetype::ifFoodToLeft6:
		case nodetype::ifFoodToLeft7:
		case nodetype::ifFoodToLeft8:
		case nodetype::ifFoodToRight1:
		case nodetype::ifFoodToRight2:
		case nodetype::ifFoodToRight3:
		case nodetype::ifFoodToRight4:
		case nodetype::ifFoodToRight5:
		case nodetype::ifFoodToRight6:
		case nodetype::ifFoodToRight7:
		case nodetype::ifFoodToRight8:
		case nodetype::ifRobotToLeft1:
		case nodetype::ifRobotToLeft2:
		case nodetype::ifRobotToLeft3:
		case nodetype::ifRobotToLeft4:
		case nodetype::ifRobotToLeft5:
		case nodetype::ifRobotToLeft6:
		case nodetype::ifRobotToLeft7:
		case nodetype::ifRobotToLeft8:
		case nodetype::ifRobotToRight1:
		case nodetype::ifRobotToRight2:
		case nodetype::ifRobotToRight3:
		case nodetype::ifRobotToRight4:
		case nodetype::ifRobotToRight5:
		case nodetype::ifRobotToRight6:
		case nodetype::ifRobotToRight7:
		case nodetype::ifRobotToRight8:
		{
			return evaluateConditionNode(blackBoard, output);
		}
		
		default: 
			std::cout << "evaluation error (evaluate)" << std::endl;
	}

	return 0;
}

std::string CNode::evaluateCompositionNode(CBlackBoard* blackBoard, std::string& output)
{
	switch (m_type)
	{
		case CNode::nodetype::seqm2:
		case CNode::nodetype::seqm3:
		case CNode::nodetype::seqm4:
		{
			output += "seqm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
		
			while (m_ptr < m_children.size())
			{
				std::string result = m_children[m_ptr]->evaluate(blackBoard, output);
			
				if (result == "failure")
				{
					m_ptr = 0;
					return "failure";
				}
				
				else if (result == "running")
				{
					return "running";
				}
				
				else
				{
					m_ptr++;
				}
			}
			m_ptr = 0;
			return "success";
		}
		
		case CNode::nodetype::selm2:
		case CNode::nodetype::selm3:
		case CNode::nodetype::selm4:
		{
			output += "selm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
			
			while (m_ptr < m_children.size())
			{
				std::string result = m_children[m_ptr]->evaluate(blackBoard, output);
			
				if (result == "success")
				{
					m_ptr = 0;
					return "success";
				}
				
				else if (result == "running")
				{
					return "running";
				}
				
				else
				{
					m_ptr++;
				}
			}
			
			m_ptr = 0;
			return "failure";
		}
		
		case CNode::nodetype::probm2:
		case CNode::nodetype::probm3:
		case CNode::nodetype::probm4:
		{
			output += "probm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
			
			std::string result = m_children[m_ptr]->evaluate (blackBoard, output);
			
			if (result != "running")
			{
				m_ptr = std::rand() % m_children.size();
				//m_ptr = getRandomNumber(0, false) % m_children.size();
			}
			
			return result;
		}
		
		default:
		{
			std::cout << "evaluation error (composition)" << std::endl;
		}
	}

	return 0;
}

std::string CNode::evaluateDecoratorNode(CBlackBoard* blackBoard, std::string& output)
{
	switch (m_type)
	{	
		//case CNode::nodetype::repeat:
		//{
			
			//output += "repeat " + std::to_string(m_ptr) + "/" + std::to_string((int) m_children[1]->getData()) + " ";
			
			//std::string result = m_children[0]->evaluate(blackBoard, output);
			//if (result == "failure")
			//{
				//m_ptr = 0;
				//return "failure";
			//}
			//else if (result == "success" && m_ptr >= m_children[1]->getData())
			//{
				//m_ptr = 0;
				//return "success";
			//}
			//else
			//{
				//if (result == "success")
				//{
					//m_ptr++;
				//}
				//return "running";
			//}
		//}
		
		case CNode::nodetype::successd:
		{
			output += "successd ";
			std::string result = m_children[0]->evaluate (blackBoard, output);
			return (result == "failure") ? "success" : result;
		}
		
		//case CNode::nodetype::failured:
		//{
			//output += "failured ";
			//std::string result = m_children[0]->evaluate (blackBoard, output);
			//return (result == "success") ? "failure" : result;
		//}
		default:
		{
			std::cout << "evaluation error (condition)" << std::endl;
			return 0;
		}
	}
}	

std::string CNode::evaluateConditionNode(CBlackBoard* blackBoard, std::string& output)
{
	blackBoard->addCondition();
	switch (m_type)
	{	
		case CNode::nodetype::ifOnFood: // carrying food bug
		case CNode::nodetype::ifOnFood1:
		case CNode::nodetype::ifOnFood2:
		case CNode::nodetype::ifOnFood3:
		case CNode::nodetype::ifOnFood4:
		case CNode::nodetype::ifOnFood5:
		case CNode::nodetype::ifOnFood6:
		case CNode::nodetype::ifOnFood7:
		case CNode::nodetype::ifOnFood8:
		{
			std::string result = (blackBoard->getDetectedFood()) ? "success" : "failure";
			output += "ifOnFood(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifGotFood:
		case CNode::nodetype::ifGotFood1:
		case CNode::nodetype::ifGotFood2:
		case CNode::nodetype::ifGotFood3:
		case CNode::nodetype::ifGotFood4:
		case CNode::nodetype::ifGotFood5:
		case CNode::nodetype::ifGotFood6:
		case CNode::nodetype::ifGotFood7:
		case CNode::nodetype::ifGotFood8:
		{
			std::string result = (blackBoard->getCarryingFood()) ? "success" : "failure";
			output += "ifGotFood(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifInNest:
		case CNode::nodetype::ifInNest1:
		case CNode::nodetype::ifInNest2:
		case CNode::nodetype::ifInNest3:
		case CNode::nodetype::ifInNest4:
		case CNode::nodetype::ifInNest5:
		case CNode::nodetype::ifInNest6:
		case CNode::nodetype::ifInNest7:
		case CNode::nodetype::ifInNest8:
		{
			std::string result = (blackBoard->getInNest()) ? "success" : "failure";
			output += "ifInNest(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifNestToLeft:
		case CNode::nodetype::ifNestToLeft1:
		case CNode::nodetype::ifNestToLeft2:
		case CNode::nodetype::ifNestToLeft3:
		case CNode::nodetype::ifNestToLeft4:
		case CNode::nodetype::ifNestToLeft5:
		case CNode::nodetype::ifNestToLeft6:
		case CNode::nodetype::ifNestToLeft7:
		case CNode::nodetype::ifNestToLeft8:
		{
			std::string result = (blackBoard->getNestToLeft()) ? "success" : "failure";
			output += "ifNestToLeft(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifNestToRight:
		case CNode::nodetype::ifNestToRight1:
		case CNode::nodetype::ifNestToRight2:
		case CNode::nodetype::ifNestToRight3:
		case CNode::nodetype::ifNestToRight4:
		case CNode::nodetype::ifNestToRight5:
		case CNode::nodetype::ifNestToRight6:
		case CNode::nodetype::ifNestToRight7:
		case CNode::nodetype::ifNestToRight8:
		{
			std::string result = (blackBoard->getNestToRight()) ? "success" : "failure";
			output += "ifNestToRight(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifFoodToLeft:
		case CNode::nodetype::ifFoodToLeft1:
		case CNode::nodetype::ifFoodToLeft2:
		case CNode::nodetype::ifFoodToLeft3:
		case CNode::nodetype::ifFoodToLeft4:
		case CNode::nodetype::ifFoodToLeft5:
		case CNode::nodetype::ifFoodToLeft6:
		case CNode::nodetype::ifFoodToLeft7:
		case CNode::nodetype::ifFoodToLeft8:
		{
			std::string result = (blackBoard->getFoodToLeft()) ? "success" : "failure";
			output += "ifFoodToLeft(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifFoodToRight:
		case CNode::nodetype::ifFoodToRight1:
		case CNode::nodetype::ifFoodToRight2:
		case CNode::nodetype::ifFoodToRight3:
		case CNode::nodetype::ifFoodToRight4:
		case CNode::nodetype::ifFoodToRight5:
		case CNode::nodetype::ifFoodToRight6:
		case CNode::nodetype::ifFoodToRight7:
		case CNode::nodetype::ifFoodToRight8:
		{
			std::string result = (blackBoard->getFoodToRight()) ? "success" : "failure";
			output += "ifFoodToRight(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifRobotToLeft:
		case CNode::nodetype::ifRobotToLeft1:
		case CNode::nodetype::ifRobotToLeft2:
		case CNode::nodetype::ifRobotToLeft3:
		case CNode::nodetype::ifRobotToLeft4:
		case CNode::nodetype::ifRobotToLeft5:
		case CNode::nodetype::ifRobotToLeft6:
		case CNode::nodetype::ifRobotToLeft7:
		case CNode::nodetype::ifRobotToLeft8:
		{
			std::string result = (blackBoard->getNearestNeighbourToLeft()) ? "success" : "failure";
			output += "ifRobotToLeft(" + result + ") ";
			return result;		
		}
		
		case CNode::nodetype::ifRobotToRight:
		case CNode::nodetype::ifRobotToRight1:
		case CNode::nodetype::ifRobotToRight2:
		case CNode::nodetype::ifRobotToRight3:
		case CNode::nodetype::ifRobotToRight4:
		case CNode::nodetype::ifRobotToRight5:
		case CNode::nodetype::ifRobotToRight6:
		case CNode::nodetype::ifRobotToRight7:
		case CNode::nodetype::ifRobotToRight8:
		{
			std::string result = (blackBoard->getNearestNeighbourToRight()) ? "success" : "failure";
			output += "ifRobotToRight(" + result + ") ";
			return result;		
		}
		
		default:
		{
			std::cout << "evaluation error (condition)" << std::endl;
			return 0;
		}
	}
}	

std::string CNode::evaluateActionNode(CBlackBoard* blackBoard, std::string& output)
{
	switch (m_type)
	{	
		case CNode::nodetype::stop:
		{
			output += "stop("+ std::to_string(m_ptr) + ") ";
			blackBoard->setMotors(0);
			break;
		}
		
		case CNode::nodetype::f:
		{
			output += "f("+ std::to_string(m_ptr) + ") ";
			blackBoard->setMotors(1);
			break;
		}
		
		case CNode::nodetype::fl:
		{
			output += "fl("+ std::to_string(m_ptr) + ") ";			
			blackBoard->setMotors(2);
			break;
		}
		
		case CNode::nodetype::fr:
		{
			output += "fr("+ std::to_string(m_ptr) + ") ";			
			blackBoard->setMotors(3);
			break;
		}
		
		case CNode::nodetype::r:
		{
			output += "r("+ std::to_string(m_ptr) + ") ";
			blackBoard->setMotors(4);
			break;
		}
		
		case CNode::nodetype::rl:
		{
			output += "rl("+ std::to_string(m_ptr) + ") ";
			blackBoard->setMotors(5);
			break;
		}
		
		case CNode::nodetype::rr:
		{
			output += "rr("+ std::to_string(m_ptr) + ") ";
			blackBoard->setMotors(6);
			break;
		}
		
		default: 
			std::cout << "evaluation error (action)" << std::endl;
			return 0;
	
	}
	
	if (m_ptr == 0)
	{
		//if (m_type != CNode::nodetype::stop)
		//{
			//blackBoard->addMovement();
		//}
	
		m_ptr++;
		// qdpy optimisation
		blackBoard->addAction();
		// end qdpy
		return "running";
	}	
	else
	{
		m_ptr--;
		return "success";
	}
}	

float CNode::normaliseBlackBoardValue(CBlackBoard* blackBoard, int index)
{
	if (index == 1) { // values between -1 and 1
		return blackBoard->getScratchpad();
	}
	
	if (index == 2) { // values between -1 and 1
		return blackBoard->getSendSignal();
	}
	
	if (index == 3) { // boolean
		return (!blackBoard->getReceivedSignal()) ? -1 : 1;
	}
	
	if (index == 4) { // boolean
		return (!blackBoard->getDetectedFood()) ? -1 : 1;
	}
	
	if (index == 5) { // boolean
		return (!blackBoard->getCarryingFood()) ? -1 : 1;
	}
	
	if (index == 6) { // values between 0 and 1
		return (blackBoard->getDensity() * 2 - 1);
	}
	
	if (index == 7) { // values between -4/7 and 4/7
		return (blackBoard->getDensityChange() / 4) * 7;
	}
	
	if (index == 8) { // values between -4/7 and 4/7
		return (blackBoard->getNestChange() / 4) * 7;
	}
	
	if (index == 9) { // values between -4/7 and 4/7
		return (blackBoard->getFoodChange() / 4) * 7;
	}	
}

std::string CNode::getNodeText(nodetype node)
{
	auto nodes = getNodeSet();
	for (auto it = nodes.begin(); it != nodes.end(); ++it)
	{
		if (it->second == node)
		{
			return it->first;
		}
	}
}

CNode::nodetype CNode::getNodeFromText(std::string text)
{  
	std::map<std::string, CNode::nodetype> nodes = getNodeSet();
	auto node = nodes.find(text);
	return node->second;
}

CNode::nodetypes CNode::getNodeType(nodetype node)
{
	if (node == nodetype::seqm2 ||
		 node == nodetype::seqm3 ||
		 node == nodetype::seqm4 ||
		 node == nodetype::selm2 ||
		 node == nodetype::selm3 ||
		 node == nodetype::selm4 ||
		 node == nodetype::probm2 ||
		 node == nodetype::probm3 ||
		 node == nodetype::probm4)
	{
		return nodetypes::composition;
	}
	
	if (node == nodetype::repeat ||
		 node == nodetype::successd ||
		 node == nodetype::failured)
	{
		return nodetypes::decorator;
	}
	
	if (
		 node == nodetype::ifOnFood || // carrying food bug
		 node == nodetype::ifGotFood ||
		 node == nodetype::ifInNest ||
		 node == nodetype::ifNestToLeft ||
		 node == nodetype::ifNestToRight ||
		 node == nodetype::ifFoodToLeft ||
		 node == nodetype::ifFoodToRight ||
		 node == nodetype::ifRobotAhead ||
		 node == nodetype::ifRobotToLeft ||
		 node == nodetype::ifRobotToRight ||
		 node == nodetype::ifOnFood1 ||
		 node == nodetype::ifOnFood2 ||
		 node == nodetype::ifOnFood3 ||
		 node == nodetype::ifOnFood4 ||
		 node == nodetype::ifOnFood5 ||
		 node == nodetype::ifOnFood6 ||
		 node == nodetype::ifOnFood7 ||
		 node == nodetype::ifOnFood8 ||
		 node == nodetype::ifGotFood1 ||
		 node == nodetype::ifGotFood2 ||
		 node == nodetype::ifGotFood3 ||
		 node == nodetype::ifGotFood4 ||
		 node == nodetype::ifGotFood5 ||
		 node == nodetype::ifGotFood6 ||
		 node == nodetype::ifGotFood7 ||
		 node == nodetype::ifGotFood8 ||
		 node == nodetype::ifInNest1 ||
		 node == nodetype::ifInNest2 ||
		 node == nodetype::ifInNest3 ||
		 node == nodetype::ifInNest4 ||
		 node == nodetype::ifInNest5 ||
		 node == nodetype::ifInNest6 ||
		 node == nodetype::ifInNest7 ||
		 node == nodetype::ifInNest8 ||
		 node == nodetype::ifNestToLeft1 ||
		 node == nodetype::ifNestToLeft2 ||
		 node == nodetype::ifNestToLeft3 ||
		 node == nodetype::ifNestToLeft4 ||
		 node == nodetype::ifNestToLeft5 ||
		 node == nodetype::ifNestToLeft6 ||
		 node == nodetype::ifNestToLeft7 ||
		 node == nodetype::ifNestToLeft8 ||
		 node == nodetype::ifNestToRight1 ||
		 node == nodetype::ifNestToRight2 ||
		 node == nodetype::ifNestToRight3 ||
		 node == nodetype::ifNestToRight4 ||
		 node == nodetype::ifNestToRight5 ||
		 node == nodetype::ifNestToRight6 ||
		 node == nodetype::ifNestToRight7 ||
		 node == nodetype::ifNestToRight8 ||
		 node == nodetype::ifFoodToLeft1 ||
		 node == nodetype::ifFoodToLeft2 ||
		 node == nodetype::ifFoodToLeft3 ||
		 node == nodetype::ifFoodToLeft4 ||
		 node == nodetype::ifFoodToLeft5 ||
		 node == nodetype::ifFoodToLeft6 ||
		 node == nodetype::ifFoodToLeft7 ||
		 node == nodetype::ifFoodToLeft8 ||
		 node == nodetype::ifFoodToRight1 ||
		 node == nodetype::ifFoodToRight2 ||
		 node == nodetype::ifFoodToRight3 ||
		 node == nodetype::ifFoodToRight4 ||
		 node == nodetype::ifFoodToRight5 ||
		 node == nodetype::ifFoodToRight6 ||
		 node == nodetype::ifFoodToRight7 ||
		 node == nodetype::ifFoodToRight8 ||
		 node == nodetype::ifRobotToLeft1 ||
		 node == nodetype::ifRobotToLeft2 ||
		 node == nodetype::ifRobotToLeft3 ||
		 node == nodetype::ifRobotToLeft4 ||
		 node == nodetype::ifRobotToLeft5 ||
		 node == nodetype::ifRobotToLeft6 ||
		 node == nodetype::ifRobotToLeft7 ||
		 node == nodetype::ifRobotToLeft8 ||
		 node == nodetype::ifRobotToRight1 ||
		 node == nodetype::ifRobotToRight2 ||
		 node == nodetype::ifRobotToRight3 ||
		 node == nodetype::ifRobotToRight4 ||
		 node == nodetype::ifRobotToRight5 ||
		 node == nodetype::ifRobotToRight6 ||
		 node == nodetype::ifRobotToRight7 ||
		 node == nodetype::ifRobotToRight8)
	{
		return nodetypes::condition;
	}
	
	if (node == nodetype::stop ||
		 node == nodetype::f ||
		 node == nodetype::fl ||
		 node == nodetype::fr ||
		 node == nodetype::r ||
		 node == nodetype::rl ||
		 node == nodetype::rr)
	{
		return nodetypes::action;
	}	
}

std::map<std::string, CNode::nodetype> CNode::getNodeSet()
{
	std::map<std::string, CNode::nodetype> nodes;
	nodes.insert({"seqm2", CNode::nodetype::seqm2});
	nodes.insert({"seqm3", CNode::nodetype::seqm3});
	nodes.insert({"seqm4", CNode::nodetype::seqm4});
	nodes.insert({"selm2", CNode::nodetype::selm2});
	nodes.insert({"selm3", CNode::nodetype::selm3});
	nodes.insert({"selm4", CNode::nodetype::selm4});
	nodes.insert({"probm2", CNode::nodetype::probm2});
	nodes.insert({"probm3", CNode::nodetype::probm3});
	nodes.insert({"probm4", CNode::nodetype::probm4});
	
	//nodes.insert({"repeat", CNode::nodetype::repeat});
	nodes.insert({"successd", CNode::nodetype::successd});
	//nodes.insert({"failured", CNode::nodetype::failured});
	
	nodes.insert({"ifOnFood", CNode::nodetype::ifOnFood}); // carrying food bug
	nodes.insert({"ifGotFood", CNode::nodetype::ifGotFood});
	nodes.insert({"ifInNest", CNode::nodetype::ifInNest});
	nodes.insert({"ifNestToLeft", CNode::nodetype::ifNestToLeft});
	nodes.insert({"ifNestToRight", CNode::nodetype::ifNestToRight});
	nodes.insert({"ifFoodToLeft", CNode::nodetype::ifFoodToLeft});
	nodes.insert({"ifFoodToRight", CNode::nodetype::ifFoodToRight});
	nodes.insert({"ifRobotAhead", CNode::nodetype::ifRobotAhead});
	nodes.insert({"ifRobotToLeft", CNode::nodetype::ifRobotToLeft});
	nodes.insert({"ifRobotToRight", CNode::nodetype::ifRobotToRight});
    nodes.insert({"ifOnFood1", CNode::nodetype::ifOnFood1});
    nodes.insert({"ifOnFood2", CNode::nodetype::ifOnFood2});
    nodes.insert({"ifOnFood3", CNode::nodetype::ifOnFood3});
    nodes.insert({"ifOnFood4", CNode::nodetype::ifOnFood4});
    nodes.insert({"ifOnFood5", CNode::nodetype::ifOnFood5});
    nodes.insert({"ifOnFood6", CNode::nodetype::ifOnFood6});
    nodes.insert({"ifOnFood7", CNode::nodetype::ifOnFood7});
    nodes.insert({"ifOnFood8", CNode::nodetype::ifOnFood8});
    nodes.insert({"ifGotFood1", CNode::nodetype::ifGotFood1});
    nodes.insert({"ifGotFood2", CNode::nodetype::ifGotFood2});
    nodes.insert({"ifGotFood3", CNode::nodetype::ifGotFood3});
    nodes.insert({"ifGotFood4", CNode::nodetype::ifGotFood4});
    nodes.insert({"ifGotFood5", CNode::nodetype::ifGotFood5});
    nodes.insert({"ifGotFood6", CNode::nodetype::ifGotFood6});
    nodes.insert({"ifGotFood7", CNode::nodetype::ifGotFood7});
    nodes.insert({"ifGotFood8", CNode::nodetype::ifGotFood8});
    nodes.insert({"ifInNest1", CNode::nodetype::ifInNest1});
    nodes.insert({"ifInNest2", CNode::nodetype::ifInNest2});
    nodes.insert({"ifInNest3", CNode::nodetype::ifInNest3});
    nodes.insert({"ifInNest4", CNode::nodetype::ifInNest4});
    nodes.insert({"ifInNest5", CNode::nodetype::ifInNest5});
    nodes.insert({"ifInNest6", CNode::nodetype::ifInNest6});
    nodes.insert({"ifInNest7", CNode::nodetype::ifInNest7});
    nodes.insert({"ifInNest8", CNode::nodetype::ifInNest8});
    nodes.insert({"ifNestToLeft1", CNode::nodetype::ifNestToLeft1});
    nodes.insert({"ifNestToLeft2", CNode::nodetype::ifNestToLeft2});
    nodes.insert({"ifNestToLeft3", CNode::nodetype::ifNestToLeft3});
    nodes.insert({"ifNestToLeft4", CNode::nodetype::ifNestToLeft4});
    nodes.insert({"ifNestToLeft5", CNode::nodetype::ifNestToLeft5});
    nodes.insert({"ifNestToLeft6", CNode::nodetype::ifNestToLeft6});
    nodes.insert({"ifNestToLeft7", CNode::nodetype::ifNestToLeft7});
    nodes.insert({"ifNestToLeft8", CNode::nodetype::ifNestToLeft8});
    nodes.insert({"ifNestToRight1", CNode::nodetype::ifNestToRight1});
    nodes.insert({"ifNestToRight2", CNode::nodetype::ifNestToRight2});
    nodes.insert({"ifNestToRight3", CNode::nodetype::ifNestToRight3});
    nodes.insert({"ifNestToRight4", CNode::nodetype::ifNestToRight4});
    nodes.insert({"ifNestToRight5", CNode::nodetype::ifNestToRight5});
    nodes.insert({"ifNestToRight6", CNode::nodetype::ifNestToRight6});
    nodes.insert({"ifNestToRight7", CNode::nodetype::ifNestToRight7});
    nodes.insert({"ifNestToRight8", CNode::nodetype::ifNestToRight8});
    nodes.insert({"ifFoodToLeft1", CNode::nodetype::ifFoodToLeft1});
    nodes.insert({"ifFoodToLeft2", CNode::nodetype::ifFoodToLeft2});
    nodes.insert({"ifFoodToLeft3", CNode::nodetype::ifFoodToLeft3});
    nodes.insert({"ifFoodToLeft4", CNode::nodetype::ifFoodToLeft4});
    nodes.insert({"ifFoodToLeft5", CNode::nodetype::ifFoodToLeft5});
    nodes.insert({"ifFoodToLeft6", CNode::nodetype::ifFoodToLeft6});
    nodes.insert({"ifFoodToLeft7", CNode::nodetype::ifFoodToLeft7});
    nodes.insert({"ifFoodToLeft8", CNode::nodetype::ifFoodToLeft8});
    nodes.insert({"ifFoodToRight1", CNode::nodetype::ifFoodToRight1});
    nodes.insert({"ifFoodToRight2", CNode::nodetype::ifFoodToRight2});
    nodes.insert({"ifFoodToRight3", CNode::nodetype::ifFoodToRight3});
    nodes.insert({"ifFoodToRight4", CNode::nodetype::ifFoodToRight4});
    nodes.insert({"ifFoodToRight5", CNode::nodetype::ifFoodToRight5});
    nodes.insert({"ifFoodToRight6", CNode::nodetype::ifFoodToRight6});
    nodes.insert({"ifFoodToRight7", CNode::nodetype::ifFoodToRight7});
    nodes.insert({"ifFoodToRight8", CNode::nodetype::ifFoodToRight8});
    nodes.insert({"ifRobotToLeft1", CNode::nodetype::ifRobotToLeft1});
    nodes.insert({"ifRobotToLeft2", CNode::nodetype::ifRobotToLeft2});
    nodes.insert({"ifRobotToLeft3", CNode::nodetype::ifRobotToLeft3});
    nodes.insert({"ifRobotToLeft4", CNode::nodetype::ifRobotToLeft4});
    nodes.insert({"ifRobotToLeft5", CNode::nodetype::ifRobotToLeft5});
    nodes.insert({"ifRobotToLeft6", CNode::nodetype::ifRobotToLeft6});
    nodes.insert({"ifRobotToLeft7", CNode::nodetype::ifRobotToLeft7});
    nodes.insert({"ifRobotToLeft8", CNode::nodetype::ifRobotToLeft8});
    nodes.insert({"ifRobotToRight1", CNode::nodetype::ifRobotToRight1});
    nodes.insert({"ifRobotToRight2", CNode::nodetype::ifRobotToRight2});
    nodes.insert({"ifRobotToRight3", CNode::nodetype::ifRobotToRight3});
    nodes.insert({"ifRobotToRight4", CNode::nodetype::ifRobotToRight4});
    nodes.insert({"ifRobotToRight5", CNode::nodetype::ifRobotToRight5});
    nodes.insert({"ifRobotToRight6", CNode::nodetype::ifRobotToRight6});
    nodes.insert({"ifRobotToRight7", CNode::nodetype::ifRobotToRight7});
    nodes.insert({"ifRobotToRight8", CNode::nodetype::ifRobotToRight8});
	
	nodes.insert({"stop", CNode::nodetype::stop});
	nodes.insert({"f", CNode::nodetype::f});
	nodes.insert({"fl", CNode::nodetype::fl});
	nodes.insert({"fr", CNode::nodetype::fr});
	nodes.insert({"r", CNode::nodetype::r});
	nodes.insert({"rl", CNode::nodetype::rl});
	nodes.insert({"rr", CNode::nodetype::rr});
	
	return nodes;	
}
	
	
	
