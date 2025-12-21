
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
    CColor getFloorColorExp1(const CVector2& c_position_on_plane);
    CColor getFloorColorExp2(const CVector2& c_position_on_plane);
    CColor getFloorColorExp3(const CVector2& c_position_on_plane);
    CColor getFloorColorExp4(const CVector2& c_position_on_plane);

    bool IsExperimentFinished() override;
    void PostStep() override;
    void postStepRandom();
    void postStepLattice();
    void randomFormation(CFootBotEntity* pcFB);
    void latticeFormation(CFootBotEntity* pcFB, int i, int j);

private:

    CFloorEntity* m_pcFloor;
    float m_sqrtRobots;
    uint m_iterations;
    int m_arenaLayout;
    float m_nest;
    float m_food;
    float m_offset;
    float m_gap;
    int m_commsRange;
    uint m_experimentLength;
    uint m_count;
    CRandom::CRNG* m_pcRNG;

    std::vector<CFootBotEntity*> m_footbots;

    std::chrono::milliseconds m_ms; 
};

