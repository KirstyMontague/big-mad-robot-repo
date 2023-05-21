add_library(footbot_bt SHARED footbot_bt.h footbot_bt.cpp CNode.h CNode.cpp CBlackBoard.h CBlackBoard.cpp)
target_link_libraries(footbot_bt
							 argos3core_simulator
							 argos3plugin_simulator_footbot
							 argos3plugin_simulator_genericrobot)
