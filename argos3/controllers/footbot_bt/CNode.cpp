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
    }
}

void CNode::decoratorNode(std::vector<std::string>& chromosome, int id)
{
    switch (m_type)
    {
        case nodetype::successd:
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
        case nodetype::ifOnFood:
        case nodetype::ifGotFood:
        case nodetype::ifInNest:
        case nodetype::ifNestToLeft:
        case nodetype::ifNestToRight:
        case nodetype::ifFoodToLeft:
        case nodetype::ifFoodToRight:
        case nodetype::ifRobotAhead:
        case nodetype::ifRobotToLeft:
        case nodetype::ifRobotToRight:
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
        
        case CNode::nodetype::ifOnFood:
        case CNode::nodetype::ifGotFood:
        case CNode::nodetype::ifInNest:
        case CNode::nodetype::ifNestToLeft:
        case CNode::nodetype::ifNestToRight:
        case CNode::nodetype::ifFoodToLeft:
        case CNode::nodetype::ifFoodToRight:
        case CNode::nodetype::ifRobotAhead:
        case CNode::nodetype::ifRobotToLeft:
        case CNode::nodetype::ifRobotToRight:
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
        case CNode::nodetype::successd:
        {
            output += "successd ";
            std::string result = m_children[0]->evaluate (blackBoard, output);
            return (result == "failure") ? "success" : result;
        }
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
        case CNode::nodetype::ifOnFood:
        {
            std::string result = (blackBoard->getDetectedFood()) ? "success" : "failure";
            output += "ifOnFood(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifGotFood:
        {
            std::string result = (blackBoard->getCarryingFood()) ? "success" : "failure";
            output += "ifGotFood(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifInNest:
        {
            std::string result = (blackBoard->getInNest()) ? "success" : "failure";
            output += "ifInNest(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifNestToLeft:
        {
            std::string result = (blackBoard->getNestToLeft()) ? "success" : "failure";
            output += "ifNestToLeft(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifNestToRight:
        {
            std::string result = (blackBoard->getNestToRight()) ? "success" : "failure";
            output += "ifNestToRight(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifFoodToLeft:
        {
            std::string result = (blackBoard->getFoodToLeft()) ? "success" : "failure";
            output += "ifFoodToLeft(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifFoodToRight:
        {
            std::string result = (blackBoard->getFoodToRight()) ? "success" : "failure";
            output += "ifFoodToRight(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifRobotToLeft:
        {
            std::string result = (blackBoard->getNearestNeighbourToLeft()) ? "success" : "failure";
            output += "ifRobotToLeft(" + result + ") ";
            return result;
        }
        
        case CNode::nodetype::ifRobotToRight:
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
        m_ptr++;
        blackBoard->addAction();
        return "running";
    }    
    else
    {
        m_ptr--;
        return "success";
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
         node == nodetype::ifOnFood ||
         node == nodetype::ifGotFood ||
         node == nodetype::ifInNest ||
         node == nodetype::ifNestToLeft ||
         node == nodetype::ifNestToRight ||
         node == nodetype::ifFoodToLeft ||
         node == nodetype::ifFoodToRight ||
         node == nodetype::ifRobotAhead ||
         node == nodetype::ifRobotToLeft ||
         node == nodetype::ifRobotToRight)
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
    
    nodes.insert({"successd", CNode::nodetype::successd});
    
    nodes.insert({"ifOnFood", CNode::nodetype::ifOnFood});
    nodes.insert({"ifGotFood", CNode::nodetype::ifGotFood});
    nodes.insert({"ifInNest", CNode::nodetype::ifInNest});
    nodes.insert({"ifNestToLeft", CNode::nodetype::ifNestToLeft});
    nodes.insert({"ifNestToRight", CNode::nodetype::ifNestToRight});
    nodes.insert({"ifFoodToLeft", CNode::nodetype::ifFoodToLeft});
    nodes.insert({"ifFoodToRight", CNode::nodetype::ifFoodToRight});
    nodes.insert({"ifRobotAhead", CNode::nodetype::ifRobotAhead});
    nodes.insert({"ifRobotToLeft", CNode::nodetype::ifRobotToLeft});
    nodes.insert({"ifRobotToRight", CNode::nodetype::ifRobotToRight});
    
    nodes.insert({"stop", CNode::nodetype::stop});
    nodes.insert({"f", CNode::nodetype::f});
    nodes.insert({"fl", CNode::nodetype::fl});
    nodes.insert({"fr", CNode::nodetype::fr});
    nodes.insert({"r", CNode::nodetype::r});
    nodes.insert({"rl", CNode::nodetype::rl});
    nodes.insert({"rr", CNode::nodetype::rr});
    
    return nodes;
}
