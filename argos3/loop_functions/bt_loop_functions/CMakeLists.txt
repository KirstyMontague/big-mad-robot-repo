link_directories(${CMAKE_BINARY_DIR}/controllers/footbot_bt)

set(bt_loop_functions_SOURCES bt_loop_functions.h bt_loop_functions.cpp)

add_library(bt_loop_functions MODULE  ${bt_loop_functions_SOURCES})

target_link_libraries(bt_loop_functions
                       footbot_bt
							  argos3core_simulator
							  argos3plugin_simulator_entities
							  argos3plugin_simulator_footbot)

