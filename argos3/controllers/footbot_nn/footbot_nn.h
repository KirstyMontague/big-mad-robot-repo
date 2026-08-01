#ifndef FOOTBOT_NN
#define FOOTBOT_NN

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>

#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>
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

    void Init(TConfigurationNode& t_node) override;
    void ControlStep() override;
    void Reset() override;
    void Destroy() override;

    void InitNN(const Real* chromosome, UInt32 numInputs, UInt32 numHidden, UInt32 numOutputs);
    void setParams(float gap, int trialLength, bool isForaging);

    void calculateDistances(double x, double y);
    void calculateDistancesExp1(double x, double y);

private:

    void setColour() const;

    void stop() {m_pcWheels->SetLinearVelocity(0.0f, 0.0f);}
    void forward() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, m_rWheelVelocity);}
    void forwardLeft() {m_pcWheels->SetLinearVelocity(0.0f, m_rWheelVelocity);}
    void forwardRight() {m_pcWheels->SetLinearVelocity(m_lWheelVelocity, 0.0f);}
    void reverse() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, -m_rWheelVelocity);}
    void reverseLeft() {m_pcWheels->SetLinearVelocity(0.0f, -m_rWheelVelocity);}
    void reverseRight() {m_pcWheels->SetLinearVelocity(-m_lWheelVelocity, 0.0f);}

    void sendInitialSignal() const;
    void recordInitialPositions(bool tracking);
    void recordFinalPositions(bool tracking);
    std::pair<Real, Real> getLocation(bool tracking);

    void sensing();
    void actuation();
    void position(bool tracking);
    void rangeAndBearing(bool tracking);

    void createAndSendPayload(const std::vector<uint64_t> distances) const;
    void decomposePayload(uint64_t concatenated, std::vector<uint64_t>& food, uint64_t& nest) const;
    void recordRangeAndBearingData(const Real distance, const CRadians bearing, float& shortestDistance, CRadians& shortestDirection) const;

    bool inTrackingIDs() const;
    uint numFoodRegions() const;

private:

    CPerceptronMulti m_cPerceptron;
    TConfigurationNode m_node;

    CBlackBoard* m_blackBoard;

    std::vector<int> m_trackingIDs;
    bool m_verbose;
    int m_count;

    float m_gap;
    int m_commsRange;
    int m_trialLength;
    bool m_isForaging;

    float m_nestRadius;
    float m_foodRadius;
    std::vector<float> m_distFood;
    float m_distNest;

    std::vector<std::vector<float>> m_scores;

    Real m_rWheelVelocity;
    Real m_lWheelVelocity;

    // sensors / actuators

    CCI_DifferentialSteeringActuator* m_pcWheels;  /* Pointer to the differential steering actuator */
    CCI_PositioningSensor* m_pcPosition;           /* Pointer to the foot-bot position sensor */
    CCI_RangeAndBearingActuator* m_pcRABA;         /* Pointer to the range and bearing actuator */
    CCI_RangeAndBearingSensor* m_pcRABS;           /* Pointer to the range and bearing sensor */
    CCI_LEDsActuator* m_pcLEDs;                    /* Pointer to the leds actuator */
};

#endif
