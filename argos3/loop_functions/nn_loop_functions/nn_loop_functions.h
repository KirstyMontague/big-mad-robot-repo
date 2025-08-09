#ifndef NN_LOOP_FUNCTIONS_H
#define NN_LOOP_FUNCTIONS_H

#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <argos3/core/simulator/loop_functions.h>
#include <chrono>

using namespace argos;

class CNNLoopFunctions : public CLoopFunctions {

public:

    CNNLoopFunctions();
    ~CNNLoopFunctions();

    void Init(TConfigurationNode& t_tree) override;

    CColor GetFloorColor(const CVector2& c_position_on_plane) override;
    bool IsExperimentFinished() override;
    void PostStep() override;

private:

    CFloorEntity* m_pcFloor;
    float m_gap;
    uint m_count;
    uint m_experimentLength;
    CRandom::CRNG* m_pcRNG;

    std::vector<CFootBotEntity*> m_footbots;

    std::chrono::milliseconds m_ms;
};


#endif
