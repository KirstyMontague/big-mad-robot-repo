link_directories(${CMAKE_BINARY_DIR}/controllers/footbot_nn)

set(nn_loop_functions_SOURCES nn_loop_functions.h nn_loop_functions.cpp)

add_library(nn_loop_functions MODULE  ${nn_loop_functions_SOURCES})

target_link_libraries(nn_loop_functions
                      footbot_nn
                      argos3core_simulator
                      argos3plugin_simulator_entities
                      argos3plugin_simulator_footbot)

