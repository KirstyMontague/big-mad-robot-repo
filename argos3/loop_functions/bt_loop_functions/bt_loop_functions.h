
#include <argos3/core/simulator/loop_functions.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <chrono>

using namespace argos;

class CBTLoopFunctions : public CLoopFunctions {

public:

    CBTLoopFunctions();
    ~CBTLoopFunctions();

    void Init(TConfigurationNode& t_tree) override;

    CColor GetFloorColor(const CVector2& c_position_on_plane) override;
    bool IsExperimentFinished() override;
    void PostStep() override;

private:

    CFloorEntity* m_pcFloor;
    float m_nest;
    float m_food;
    float m_gap;
    uint m_experimentLength;
    uint m_count;
    CRandom::CRNG* m_pcRNG;

    std::vector<CFootBotEntity*> m_footbots;

    std::chrono::milliseconds m_ms; 
};

