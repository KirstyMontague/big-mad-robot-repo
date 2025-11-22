#include "footbot_bt.h"
#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/core/utility/math/vector2.h>

#include <iostream>
#include <algorithm>
#include <cstring>

CFootBotBT::CFootBotBT() :
    m_pcWheels(NULL),
    m_pcLEDs(NULL),
    m_pcProximity(NULL),
    m_pcPosition(NULL),
    m_pcRABA(NULL),
    m_pcRABS(NULL),
    m_rWheelVelocity(5.0f),
    m_lWheelVelocity(5.0f),
    m_gap(0.0),
    m_trialLength(0),
    m_trackingID(0),
    m_count(0),
    m_food(0)
{}

CFootBotBT::~CFootBotBT()
{
    std::cout << "result " << GetId();

    //0 density
    //1 nest
    //2 food
    //3 inverse density
    //4 inverse nest
    //5 inverse food
    //6 movement
    //7 rotation
    //8 conditionality
    //9 food collected
    
    std::vector<int> x{0,1,2,3,4,5,6,7,8,9};
    for (int i : x)
    {
        for (float s : m_scores[i])
        {
            std::cout << " " << std::to_string(s);
        }
    }
    
    std::cout << std::endl;
}

void CFootBotBT::Init(TConfigurationNode& t_node) 
{
    m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
    m_pcRABA      = GetActuator<CCI_RangeAndBearingActuator     >("range_and_bearing"    );
    m_pcLEDs      = GetActuator<CCI_LEDsActuator                >("leds"                 );
    
    m_pcProximity = GetSensor  <CCI_FootBotProximitySensor      >("footbot_proximity"    );
    m_pcPosition  = GetSensor  <CCI_PositioningSensor           >("positioning"          );
    m_pcRABS      = GetSensor  <CCI_RangeAndBearingSensor       >("range_and_bearing"    );
    m_pcLight     = GetSensor  <CCI_FootBotLightSensor          >("footbot_light"        );
    m_pcGround    = GetSensor  <CCI_FootBotMotorGroundSensor    >("footbot_motor_ground" );

    Real wheelVelocity;
    Real noise;
    GetNodeAttributeOrDefault(t_node, "velocity", wheelVelocity, wheelVelocity);
    GetNodeAttributeOrDefault(t_node, "trackingID", m_trackingID, m_trackingID);
    GetNodeAttributeOrDefault(t_node, "verbose", m_verbose, m_verbose);
    
    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    m_rWheelVelocity = wheelVelocity * noise;
    
    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    m_lWheelVelocity = wheelVelocity * noise;
    
    m_trackingIDs.push_back(m_trackingID);
    
    // sometimes it's handy to be able to highlight a particular robot
    if (inTrackingIDs() && m_verbose) m_pcLEDs->SetAllColors(CColor::YELLOW);

    for (uint i = 0; i < 10; ++i)
    {
        m_scores.push_back(std::vector<float>());
    }
}

void CFootBotBT::buildTree(std::vector<std::string> tokens)
{
    m_rootNode = new CNode(tokens, std::stoi(GetId()));
}

void CFootBotBT::createBlackBoard(int numRobots)
{
    m_blackBoard = new CBlackBoard(numRobots);
}

void CFootBotBT::calculateDistances(double x, double y)
{
    double distanceFromCentre = sqrt((x * x) + (y * y));

    double distNest = distanceFromCentre - m_nestRadius;
    double distFood = (m_gap + 0.5) - distanceFromCentre;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotBT::setColour()
{
    if (m_blackBoard->getCarryingFood())
    {
        m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::ORANGE : CColor::GREEN);
    }
    else
    {
        m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::BLACK);
    }
}

void CFootBotBT::setParams(float nest, float food, float gap, int trialLength)
{
    m_nestRadius = nest;
    m_foodRadius = food;
    m_gap = gap;
    m_trialLength = trialLength;
}

void CFootBotBT::setPlayback(bool playback)
{
    m_playback = playback;
}

void CFootBotBT::sendInitialSignal() 
{
    // send an initial range and bearing signal so the
    // distances don't get thrown off by empty values
    
    short int id = std::stoi(GetId());
    int distNest = (m_blackBoard->getInNest()) ? 0 : 500;
    int distFood = (m_blackBoard->getDetectedFood()) ? 0 : 500;

    // fill buffer
    CByteArray cBuf;
    cBuf << std::stoi(GetId());
    cBuf << (short int) distNest;
    cBuf << (short int) distFood;
    cBuf << (short int) 0;
    
    // send signal
    m_pcRABA->ClearData();
    m_pcRABA->SetData(cBuf);
}

void CFootBotBT::recordInitialPositions(bool tracking) 
{
    m_blackBoard->setInitialAbsoluteDistanceFromFood(m_distFood, tracking ? std::stoi(GetId()) : -1);
}

void CFootBotBT::recordFinalPositions(bool tracking) 
{
    m_blackBoard->setFinalAbsoluteDistanceFromFood(m_distFood, tracking ? std::stoi(GetId()) : -1);
}

void CFootBotBT::proximity(bool tracking) 
{
    const CCI_FootBotProximitySensor::TReadings& proximity = m_pcProximity->GetReadings();
    std::vector<CCI_FootBotProximitySensor::SReading> proximityData = proximity;
    
    bool collision = false;
    bool objectAhead = false;
    bool objectToLeft = false;
    bool objectToRight = false;
    
    for (CCI_FootBotProximitySensor::SReading p : proximity)
    {
        if (p.Value > 0)
        {
            Real angle = p.Angle.GetValue() * CRadians::RADIANS_TO_DEGREES;
            
            if (angle > -30.0 && angle < 30.0)
            {
                objectAhead = true;
            }
            
            else if (angle > 30.0 && angle < 120.0)
            {
                objectToLeft = true;
            }
            
            else if (angle < -30.0 && angle > -120.0)
            {
                objectToRight = true;
            }
        }
            
        if (p.Value > 0.8)
        {
            collision = true;
        }
    }
    
    if (collision)
    {
        m_blackBoard->addCollision();
    }
    
    m_blackBoard->setObjectAhead(objectAhead);
    m_blackBoard->setObjectToLeft(objectToLeft);
    m_blackBoard->setObjectToRight(objectToRight);
}

void CFootBotBT::position(bool tracking)
{
    // position data
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();
    calculateDistances(x, y);

    // update the blackboard to reflect whether the robot is in the food region
    m_blackBoard->setDetectedFood(m_count, m_distFood <= 0.0, (tracking ? std::stoi(GetId()) : -1));
    m_blackBoard->setCarryingFood(m_blackBoard->getCarryingFood() || m_blackBoard->getDetectedFood());

    // update the blackboard to reflect whether the robot is in the nest region
    m_blackBoard->setInNest(m_count, m_distNest <= 0.0, (tracking ? std::stoi(GetId()) : -1));
    m_blackBoard->incrementTimeInNest(m_blackBoard->getInNest());
    
    if (m_blackBoard->getInNest() && m_blackBoard->getCarryingFood())
    {
        m_food++;
        m_blackBoard->setCarryingFood(false);
    }
}

void CFootBotBT::rangeAndBearing(bool tracking)
{
    // range and bearing data
    const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();
    
    // map for density of robots and defaults for distance to food or nest
    std::map<int, double> IDs;
    float distanceToNest = m_blackBoard->getInNest() ? 0 : 500;
    float distanceToFood = m_blackBoard->getDetectedFood() ? 0 : 500;
    CRadians closestNestDirection;
    CRadians closestFoodDirection;
    CRadians closestNeighbourDirection;
    float closestNeighbourDistance = 0.0;
    
    
    // for each range and bearing signal received 
    for(size_t i = 0; i < tPackets.size(); ++i) {
        
        if (std::rand() % 20 == 0) {
            continue;
        }
        
        if (tPackets[i].Range > 100) {
            continue;
        }
        
        auto data = tPackets[i].Data;
        auto bearing = tPackets[i].HorizontalBearing;
        
        int id;
        short int nest;
        short int food;
        short int signal;
        data >> id;
        data >> nest;
        data >> food;
        data >> signal;
        
        // if we haven't already received a signal from this robot in the current timestep
        if (IDs.find(id) == IDs.end())
        {
            if (closestNeighbourDistance == 0.0 || tPackets[i].Range < closestNeighbourDistance)
            {
                closestNeighbourDistance = tPackets[i].Range;
                closestNeighbourDirection = bearing;
            }
            if (nest + tPackets[i].Range < distanceToNest)
            {
                distanceToNest = nest + tPackets[i].Range;
                closestNestDirection = bearing;
            }
            if (food + tPackets[i].Range < distanceToFood)
            {
                distanceToFood = food + tPackets[i].Range;
                closestFoodDirection = bearing;
            }
            // store density value for the robot sending this signal
            Real density = 1 / (ARGOS_PI * ((tPackets[i].Range / 1000) * (tPackets[i].Range / 1000))); // max = 1107
            IDs.insert(std::pair<int, double>(id, density));
        }
    }
    
    // calculate density and change in density
    float density = 0;
    for (auto it = IDs.begin(); it != IDs.end(); ++it)
    {
        density += it->second;
    }
    m_blackBoard->updateDensityVector(density, (tracking ? std::stoi(GetId()) : -1));
    if (m_count == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDensity((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
    }
    m_blackBoard->setFirstDensityChange(m_count);
    
    // save number of robots in range and nearest robot distance
    //m_blackBoard->saveNumNeighbours(IDs.size(), (tracking ? std::stoi(GetId()) : -1));
    //m_blackBoard->saveDistanceNearestRobot(nearestRobotDistance, (tracking ? std::stoi(GetId()) : -1));
    
    bool closestNeighbourToLeft = false;
    bool closestNeighbourToRight = false;
    Real angle = closestNeighbourDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;

    if (angle < 0)
    {
        closestNeighbourToRight = true;
    } 
    else if (angle >= 0)
    {
        closestNeighbourToLeft = true;
    } 
    m_blackBoard->setNearestNeighbourToLeft(closestNeighbourToLeft);
    m_blackBoard->setNearestNeighbourToRight(closestNeighbourToRight);
    
    // save distance to nest and change in distance
    m_blackBoard->updateDistNestVector(distanceToNest, tracking ? std::stoi(GetId()) : -1);
    if (m_count == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistNest((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
    }
    
    // save distance to food and change in distance
    m_blackBoard->updateDistFoodVector(distanceToFood, (tracking ? std::stoi(GetId()) : -1));
    if (m_count == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistFood((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
    }
    
    // navigation
    Real nestDirectionDegrees = closestNestDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    Real foodDirectionDegrees = closestFoodDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    
    m_blackBoard->setNestToRight(distanceToNest < 500 && distanceToNest > 0 && nestDirectionDegrees < 0.0);
    m_blackBoard->setNestToLeft(distanceToNest < 500 && distanceToNest > 0 && nestDirectionDegrees > 0.0);
    m_blackBoard->setFoodToRight(distanceToFood < 500 && distanceToFood > 0 && foodDirectionDegrees < 0.0);
    m_blackBoard->setFoodToLeft(distanceToFood < 500 && distanceToFood > 0 && foodDirectionDegrees > 0.0);
}

void CFootBotBT::groundSensor(bool tracking) 
{
    // ground sensor data
    const CCI_FootBotMotorGroundSensor::TReadings& floorColour = m_pcGround->GetReadings();
    std::vector<CCI_FootBotMotorGroundSensor::SReading> floorData = floorColour;
    //for (CCI_FootBotMotorGroundSensor::SReading reading : floorData)
    //{
        //Real value = reading.Value;
        //CVector2 offset = reading.Offset;
        //if (tracking) std::cout << std::to_string(value) << "  ";
    //}
    //if (tracking) std::cout <<std::endl;
}

void CFootBotBT::sensing() 
{
    bool tracking = inTrackingIDs() && m_verbose;
    
    position(tracking);
    proximity(tracking);
    rangeAndBearing(tracking);
    
}

void CFootBotBT::actuation() 
{
    bool tracking = inTrackingIDs() && m_verbose;
    
    short int id = std::stoi(GetId());
    short int distNest = m_blackBoard->getDistNest() * 500;
    short int distFood = m_blackBoard->getDistFood() * 500;
    short int sendSignal = 1;
    
    // write robot ID, distance to nest, distance to food and signal to buffer
    CByteArray cBuf;
    cBuf << std::stoi(GetId());
    cBuf << distNest;
    cBuf << distFood;
    cBuf << sendSignal;
    
    // send range and bearing signal
    m_pcRABA->ClearData();
    m_pcRABA->SetData(cBuf);
    
    // send motor commands
    int motors = m_blackBoard->getMotors();
    (motors == 1) ? forward() 
    : (motors == 2) ? forwardLeft() 
    : (motors == 3) ? forwardRight() 
    : (motors == 4) ? reverse() 
    : (motors == 5) ? reverseLeft() 
    : (motors == 6) ? reverseRight() 
    : stop();
}

void CFootBotBT::ControlStep() 
{
    bool tracking = inTrackingIDs() && m_verbose;

    m_count++;
    
    if ((m_count % m_trialLength) == 1)
    {
        position(tracking);
        sendInitialSignal();
        recordInitialPositions(tracking);
    }
    else
    {
        sensing();
    }
    
    if (m_count % 4 == 0)
    {
        m_blackBoard->setMotors(0);
        std::string output;
        std::string result = m_rootNode->evaluate(m_blackBoard, output);
        
        // uncomment to print all nodes traversed on each tick
        //if (m_playback)
        //{
            //if (inTrackingIDs()) std::cout << output << std::endl;
        //}
        
        //if (tracking) std::cout << output << std::endl;
        //if (tracking) std::cout << m_blackBoard->getConditions() << std::endl;
        //if (tracking) std::cout << m_blackBoard->getActions() << std::endl;
        //if (tracking) std::cout << m_blackBoard->getConditionality() << std::endl;
    }
    
    if (m_count > 1)
    {
        actuation();
    }
    
    if (m_blackBoard->getMotors() > 0 && m_count % 4 == 0)
    {
        m_blackBoard->addMovement();
        m_blackBoard->addRotation();
    }
    
    if (m_count % m_trialLength == 16)
    {
        m_blackBoard->setInitialDensity(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setInitialDistanceFromNest(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setInitialDistanceFromFood(tracking ? std::stoi(GetId()) : -1);
    }
    
    if (m_count % m_trialLength == 0)
    {
        recordFinalPositions(tracking);

        m_blackBoard->setFinalDensity(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setFinalDistanceFromNest(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setFinalDistanceFromFood(tracking ? std::stoi(GetId()) : -1);
        
        m_scores[0].push_back(m_blackBoard->getDifferenceInDensity());
        m_scores[1].push_back(m_blackBoard->getDifferenceInDistanceFromNest());
        m_scores[2].push_back(m_blackBoard->getDifferenceInDistanceFromFood());
        m_scores[3].push_back(m_blackBoard->getDifferenceInDensityInverse());
        m_scores[4].push_back(m_blackBoard->getDifferenceInDistanceFromNestInverse());
        m_scores[5].push_back(m_blackBoard->getDifferenceInDistanceFromFoodInverse(tracking ? std::stoi(GetId()) : -1));
        
        m_scores[6].push_back(static_cast<float>(m_food));
        
        m_scores[7].push_back(static_cast<float>(m_blackBoard->getMovement()));
        m_scores[8].push_back(static_cast<float>(m_blackBoard->getRotations()));
        m_scores[9].push_back(static_cast<float>(m_blackBoard->getConditionality()));
        
        m_blackBoard->setMovement(0);
        m_blackBoard->setRotations(0);
        m_blackBoard->setConditions(0);
        m_blackBoard->setActions(0);

        m_blackBoard->setCarryingFood(false);
        m_food = 0;
    }

    setColour();

}

bool CFootBotBT::inTrackingIDs()
{
    return (std::find(m_trackingIDs.begin(), m_trackingIDs.end(), std::stoi(GetId())) != m_trackingIDs.end());
}

REGISTER_CONTROLLER(CFootBotBT, "footbot_bt_controller")
