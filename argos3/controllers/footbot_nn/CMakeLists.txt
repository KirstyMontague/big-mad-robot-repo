add_library(footbot_nn SHARED
            nn/neural_network.h
            nn/neural_network.cpp
            nn/perceptron_multi.h
            nn/perceptron_multi.cpp
            CBlackBoard.h
            CBlackBoard.cpp
            footbot_nn.h
            footbot_nn.cpp
)
target_link_libraries(footbot_nn
                      argos3core_simulator
                      argos3plugin_simulator_footbot
                      argos3plugin_simulator_genericrobot)
