
#include <argos3/core/simulator/loop_functions.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <argos3/core/simulator/entity/floor_entity.h>
#include <chrono>

#include <controllers/footbot_bt/footbot_bt.h>

using namespace argos;

class CBTLoopFunctions : public CLoopFunctions {

public:

    CBTLoopFunctions();
    ~CBTLoopFunctions();

    void Init(TConfigurationNode& t_tree) override;
    CColor GetFloorColor(const CVector2& c_position_on_plane) override;
    void PostStep() override;
    bool IsExperimentFinished() override;

private:

    CColor getFloorColorExp1(const CVector2& c_position_on_plane);
    CColor getFloorColorExp2(const CVector2& c_position_on_plane);
    CColor getFloorColorExp3(const CVector2& c_position_on_plane);
    CColor getFloorColorExp4(const CVector2& c_position_on_plane);
    CColor getFloorColorExp5(const CVector2& c_position_on_plane);
    CColor getFloorColorExp6(const CVector2& c_position_on_plane);
    CColor getFloorColorExp7(const CVector2& c_position_on_plane);

    float hypotenuseSquared(const float x1, const float y1, const float x2, const float y2) const;

    bool readConfigFile(const std::string& path, std::string& project, std::string& repertoireFilename, float& velocity);
    void generateArenas(const std::string& filename);
    bool readSeedAndGap(const std::string& filename);
    bool readChromosome(const std::string& filename, std::string& chromosome);

    void tokeniseSubbehaviors(const std::string& filename, std::map<std::string, std::vector<std::string>>& subBehaviours);
    void tokeniseChromosome(const std::map<std::string, std::vector<std::string>>& subBehaviours, const std::string& chromosome, std::vector<std::string>& tokens);
    void tokeniseAgnosticChromosome(std::map<std::string, std::vector<std::string>>& subBehaviours, const std::string& chromosome, std::vector<std::string>& tokens);

    void addRobots(const std::vector<std::string> tokens, const std::string& project, const uint velocity, bool playback);

    void postStepRandom();
    void postStepLattice();
    void postStepLocalised();
    void postStepTwoRobots();

    void randomFormation(CFootBotEntity* pcFB);
    void latticeFormation(CFootBotEntity* pcFB, int i, int j);
    void localisedFormation(CFootBotEntity* footbot, int index);
    void twoRobotFormation(CFootBotEntity* footbot, int index);

    void setArenaPOIs(CFootBotBT& controller);

private:

    CRandom::CRNG* m_pcRNG;
    CFloorEntity* m_pcFloor;
    std::chrono::milliseconds m_ms;

    uint m_count;

    std::vector<CFootBotEntity*> m_footbots;
    uint m_sqrtRobots;
    int m_commsRange;

    uint m_currentIteration;
    uint m_numIterations;
    uint m_experimentLength;

    std::string m_formation;
    int m_arenaLayout;
    std::vector<std::vector<CFootBotBT::Poi>> m_arenas;

    float m_nest;
    float m_food;
    float m_offset;
    float m_gap;
};

