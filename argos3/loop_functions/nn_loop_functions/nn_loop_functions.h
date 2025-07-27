#ifndef NN_LOOP_FUNCTIONS_H
#define NN_LOOP_FUNCTIONS_H

#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <argos3/core/simulator/loop_functions.h>
#include <chrono>

// Weights = (Inputs * Hidden) + Hidden + (Hidden * Outputs) + Outputs = (9 * 10) + 10 + (10 * 1) + 1 = 111
static const size_t GENOME_SIZE = 111;

using namespace argos;

class CNNLoopFunctions : public CLoopFunctions {

public:

    CNNLoopFunctions();
    ~CNNLoopFunctions();

    virtual void Init(TConfigurationNode& t_tree);

    virtual CColor GetFloorColor(const CVector2& c_position_on_plane);
    virtual void PostStep();

private:

    CFloorEntity* m_pcFloor;
    float m_gap;
    uint m_count;
    CRandom::CRNG* m_pcRNG;

    std::vector<CFootBotEntity*> m_footbots;

    std::chrono::milliseconds m_ms;
};


#endif
