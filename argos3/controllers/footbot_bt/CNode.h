#ifndef CNODE_H
#define CNODE_H

#include "CBlackBoard.h"

#include <iostream>
#include <vector>
#include <map>

class CNode
{
    public:
    
        enum nodetypes : int
        {
            composition = 0,
            decorator = 1,
            condition = 2,
            action = 3
        };
    
        enum nodetype : int
        {
            blank,
            seqm2,
            seqm3,
            seqm4,
            selm2,
            selm3,
            selm4,
            probm2,
            probm3,
            probm4,
            stop,
            f,
            fl,
            fr,
            r,
            rl,
            rr,
            repeat,
            successd,
            failured,
            ifOnFood,
            ifGotFood,
            ifInNest,
            ifNestToLeft,
            ifNestToRight,
            ifFoodToLeft,
            ifFoodToRight,
            ifRobotAhead,
            ifRobotToLeft,
            ifRobotToRight,
        };

        CNode(std::vector<std::string>& chromosome, int id);
        CNode(std::string word);
        
        void compositionNode(std::vector<std::string>& chromosome, int id);
        void decoratorNode(std::vector<std::string>& chromosome, int id);
        void conditionNode(std::vector<std::string>& chromosome);
        void actionNode(std::vector<std::string>& chromosome);
        
        std::string evaluate(CBlackBoard* blackBoard, std::string& output);
        std::string evaluateCompositionNode(CBlackBoard* blackBoard, std::string& output);
        std::string evaluateDecoratorNode(CBlackBoard* blackBoard, std::string& output);
        std::string evaluateConditionNode(CBlackBoard* blackBoard, std::string& output);
        std::string evaluateActionNode(CBlackBoard* blackBoard, std::string& output);
        
        float getData() {return m_data;}
        
        std::string getNodeText(nodetype node);
        nodetype getNodeFromText(std::string text);
        nodetypes getNodeType(nodetype node);
        std::map<std::string, nodetype> getNodeSet();
    
    private:
    
        int m_ptr;
        std::vector<CNode*> m_children;
        nodetype m_type;
        float m_data;
};

#endif
