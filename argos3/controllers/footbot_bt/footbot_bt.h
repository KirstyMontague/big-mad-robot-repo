#ifndef FOOTBOT_BT_H
#define FOOTBOT_BT_H

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_positioning_sensor.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_light_sensor.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_motor_ground_sensor.h>

#include "CNode.h"


using namespace argos;

class CFootBotBT : public CCI_Controller {

public:

   CFootBotBT();
   virtual ~CFootBotBT();

   virtual void Init(TConfigurationNode& t_node);
   virtual void ControlStep();
   virtual void Reset() {}
   virtual void Destroy() {}
   
   void buildTree(std::vector<std::string> tokens);
   void createBlackBoard(int numRobots);
   void setParams(float nest, float gap, int trialLength);
   void setColour();
   void setPlayback(bool playback);
   
   
private:

	//static int getRandomNumber(int id, bool set);

	void stop() {m_pcWheels->SetLinearVelocity(0.0f, 0.0f);}
	void forward() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, m_rWheelVelocity);}
	void forwardLeft() {m_pcWheels->SetLinearVelocity(0.0f, m_rWheelVelocity);}
	void forwardRight() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, 0.0f);}
	void reverse() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, -m_rWheelVelocity);}
	void reverseLeft() {m_pcWheels->SetLinearVelocity(0.0f, -m_rWheelVelocity);}
	void reverseRight() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, 0.0f);}

	void sendInitialSignal();
	void recordInitialPositions(bool tracking);
	void recordFinalPositions(bool tracking);
	
	void sensing();
	void actuation();
	void proximity(bool tracking);
	double position(bool tracking);
	void rangeAndBearing(double r, bool tracking);
	void groundSensor(bool tracking);
		
	CNode* m_rootNode;
	CBlackBoard* m_blackBoard;
	float m_nest;
	float m_gap;
    int m_trialLength;
	int m_count;
	int m_food;
	int m_trackingID;
	std::vector<int> m_trackingIDs;
	bool m_verbose;

	Real m_rWheelVelocity;
	Real m_lWheelVelocity;
   
   bool inTrackingIDs();
   
   
   bool m_playback = false;
   std::vector<std::vector<float>> m_scores;
   
   // sensors / actuators
   
   CCI_DifferentialSteeringActuator* m_pcWheels;	/* Pointer to the differential steering actuator */
   CCI_FootBotProximitySensor* m_pcProximity;		/* Pointer to the foot-bot proximity sensor */
   CCI_PositioningSensor* m_pcPosition;				/* Pointer to the foot-bot position sensor */
   CCI_RangeAndBearingActuator*  m_pcRABA;			/* Pointer to the range and bearing actuator */
   CCI_RangeAndBearingSensor* m_pcRABS;				/* Pointer to the range and bearing sensor */
   CCI_LEDsActuator* m_pcLEDs;							/* Pointer to the leds actuator */
   CCI_FootBotLightSensor* m_pcLight;					/* Pointer to the light sensor */
   CCI_FootBotMotorGroundSensor* m_pcGround;			/* Pointer to the ground sensor */
};

#endif
