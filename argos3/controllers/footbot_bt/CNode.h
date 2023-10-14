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
			ifOnFood, // carrying food bug
			ifGotFood,
			ifInNest,
			ifNestToLeft,
			ifNestToRight,
			ifFoodToLeft,
			ifFoodToRight,
			ifRobotAhead,
			ifRobotToLeft,
			ifRobotToRight,
			ifOnFood1,
			ifOnFood2,
			ifOnFood3,
			ifOnFood4,
			ifOnFood5,
			ifOnFood6,
			ifOnFood7,
			ifOnFood8,
			ifGotFood1,
			ifGotFood2,
			ifGotFood3,
			ifGotFood4,
			ifGotFood5,
			ifGotFood6,
			ifGotFood7,
			ifGotFood8,
			ifInNest1,
			ifInNest2,
			ifInNest3,
			ifInNest4,
			ifInNest5,
			ifInNest6,
			ifInNest7,
			ifInNest8,
			ifNestToLeft1,
			ifNestToLeft2,
			ifNestToLeft3,
			ifNestToLeft4,
			ifNestToLeft5,
			ifNestToLeft6,
			ifNestToLeft7,
			ifNestToLeft8,
			ifNestToRight1,
			ifNestToRight2,
			ifNestToRight3,
			ifNestToRight4,
			ifNestToRight5,
			ifNestToRight6,
			ifNestToRight7,
			ifNestToRight8,
			ifFoodToLeft1,
			ifFoodToLeft2,
			ifFoodToLeft3,
			ifFoodToLeft4,
			ifFoodToLeft5,
			ifFoodToLeft6,
			ifFoodToLeft7,
			ifFoodToLeft8,
			ifFoodToRight1,
			ifFoodToRight2,
			ifFoodToRight3,
			ifFoodToRight4,
			ifFoodToRight5,
			ifFoodToRight6,
			ifFoodToRight7,
			ifFoodToRight8,
			ifRobotAhead1,
			ifRobotAhead2,
			ifRobotAhead3,
			ifRobotAhead4,
			ifRobotAhead5,
			ifRobotAhead6,
			ifRobotAhead7,
			ifRobotAhead8,
			ifRobotToLeft1,
			ifRobotToLeft2,
			ifRobotToLeft3,
			ifRobotToLeft4,
			ifRobotToLeft5,
			ifRobotToLeft6,
			ifRobotToLeft7,
			ifRobotToLeft8,
			ifRobotToRight1,
			ifRobotToRight2,
			ifRobotToRight3,
			ifRobotToRight4,
			ifRobotToRight5,
			ifRobotToRight6,
			ifRobotToRight7,
			ifRobotToRight8,
			
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
	
		//static int getRandomNumber(int id, bool set);
		float normaliseBlackBoardValue(CBlackBoard* blackBoard, int index);
		int m_ptr;
		std::vector<CNode*> m_children;
		nodetype m_type;
		float m_data;
	
};

#endif
