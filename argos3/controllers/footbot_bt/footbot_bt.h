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

    struct Poi
    {
        double m_x;
        double m_y;
        double m_r;
    };

    CFootBotBT();
    virtual ~CFootBotBT();

    void Init(TConfigurationNode& t_node) override;
    void ControlStep() override;
    void Reset() override {}
    void Destroy() override {}

    void buildTree(std::vector<std::string> tokens);
    void setParams(int commsRange, float velocity, int trialLength, uint robotType);
    void setArenaParams(int arenaLayout, float nest, float food, float gap);

    void setArenaPOIs(std::vector<Poi> arena) {m_arena = arena;}

    void calculateDistances(double x, double y);
    void calculateDistancesExp1(double x, double y);
    void calculateDistancesExp2(double x, double y);
    void calculateDistancesExp3(double x, double y);
    void calculateDistancesExp4(double x, double y);
    void calculateDistancesExp5(double x, double y);
    void calculateDistancesExp6(double x, double y);
    void calculateDistancesExp7(double x, double y);

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
    void proximity(bool tracking);
    void position(bool tracking);
    void rangeAndBearing(bool tracking);
    void groundSensor(bool tracking);

    void createAndSendPayload(const std::vector<uint64_t> distances) const;
    void decomposePayload(uint64_t concatenated, std::vector<uint64_t>& food, uint64_t& nest) const;
    void recordRangeAndBearingData(const Real distance, const CRadians bearing, float& shortestDistance, CRadians& shortestDirection) const;

    float hypotenuseSquared(float x1, float y1, float x2, float y2) const;

    bool inTrackingIDs() const;

private:

    CNode* m_rootNode;
    CBlackBoard* m_blackBoard;

    std::vector<int> m_trackingIDs;
    bool m_verbose;
    int m_count;

    std::string m_project;

    float m_gap;
    int m_commsRange;
    int m_trialLength;
    uint m_robotType;

    int m_arenaLayout;
    std::vector<Poi> m_arena;
    float m_nestRadius;
    float m_foodRadius;
    std::vector<float> m_distFood;
    float m_distNest;

    std::vector<std::vector<float>> m_scores;

    Real m_rWheelVelocity;
    Real m_lWheelVelocity;

    // sensors / actuators

    CCI_DifferentialSteeringActuator* m_pcWheels;  /* Pointer to the differential steering actuator */
    CCI_FootBotProximitySensor* m_pcProximity;     /* Pointer to the foot-bot proximity sensor */
    CCI_PositioningSensor* m_pcPosition;           /* Pointer to the foot-bot position sensor */
    CCI_RangeAndBearingActuator* m_pcRABA;         /* Pointer to the range and bearing actuator */
    CCI_RangeAndBearingSensor* m_pcRABS;           /* Pointer to the range and bearing sensor */
    CCI_LEDsActuator* m_pcLEDs;                    /* Pointer to the leds actuator */
    CCI_FootBotLightSensor* m_pcLight;             /* Pointer to the light sensor */
    CCI_FootBotMotorGroundSensor* m_pcGround;      /* Pointer to the ground sensor */
};

#endif
