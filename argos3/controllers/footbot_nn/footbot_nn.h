#ifndef FOOTBOT_NN
#define FOOTBOT_NN

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_light_sensor.h>

#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_positioning_sensor.h>

#include "nn/perceptron_multi.h"
#include "CBlackBoard.h"

using namespace argos;

/*
 * Virtual inheritance so that matching methods in the CCI_Controller
 * and CPerceptron don't get messed up.
 * 
 * Also using Introduction to Deep Learning and Neural Networks with Python, 
 * Ahmed Fawzy Gad and Fatima Ezzahra Jarmouni chapters 2 & 5
 * 
 */
class CFootBotNNController : public CCI_Controller {

public:

    CFootBotNNController();
    virtual ~CFootBotNNController();

    void Init(TConfigurationNode& t_node);
    void ControlStep();
    void Reset();
    void Destroy();

    void InitNN(const Real* chromosome, UInt32 numInputs, UInt32 numHidden, UInt32 numOutputs);
    void createBlackBoard(int numRobots);
    void setParams(float gap, int trialLength);

private:

    void stop() {m_pcWheels->SetLinearVelocity(0.0f, 0.0f);}
    void forward() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, m_rWheelVelocity);}
    void forwardLeft() {m_pcWheels->SetLinearVelocity(0.0f, m_rWheelVelocity);}
    void forwardRight() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, 0.0f);}
    void reverse() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, -m_rWheelVelocity);}
    void reverseLeft() {m_pcWheels->SetLinearVelocity(0.0f, -m_rWheelVelocity);}
    void reverseRight() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, 0.0f);}

    void sensing(bool tracking);
    void actuation(bool tracking);
    double position(bool tracking);
    void rangeAndBearing(double r, bool tracking);
    void setDefaultLEDs(bool tracking);
    void setFoodLEDs(bool tracking);

    void sendInitialSignal();
    void recordInitialPositions(bool tracking);
    void recordFinalPositions(bool tracking);

    bool inTrackingIDs();

    CCI_FootBotLightSensor* m_pcLight;
    CCI_PositioningSensor* m_pcPosition;
    CCI_FootBotProximitySensor* m_pcProximity;
    CCI_RangeAndBearingSensor* m_pcRABS;

    CCI_LEDsActuator* m_pcLEDs;
    CCI_RangeAndBearingActuator* m_pcRABA;
    CCI_DifferentialSteeringActuator* m_pcWheels;

    Real m_lWheelVelocity;
    Real m_rWheelVelocity;

    int m_count = 0;

    CPerceptronMulti m_cPerceptron;
    TConfigurationNode m_node;

    CBlackBoard* m_blackBoard;

    float m_params;
    int m_trialLength;

    std::vector<std::vector<float>> m_scores;
    bool m_carryingFood = false;
    int m_food = 0;

    int m_trackingID;
    std::vector<int> m_trackingIDs;
};

#endif
