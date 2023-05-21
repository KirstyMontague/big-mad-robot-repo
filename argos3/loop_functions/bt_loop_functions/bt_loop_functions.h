
#include <argos3/core/simulator/loop_functions.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>
#include <chrono>

using namespace argos;

class CBTLoopFunctions : public CLoopFunctions {

public:

   CBTLoopFunctions();
   ~CBTLoopFunctions();

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

