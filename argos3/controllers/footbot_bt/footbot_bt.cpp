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
    m_verbose(false),
    m_arenaLayout(0),
    m_nestRadius(0.0),
    m_foodRadius(0.0),
    m_commsRange(0),
    m_distNest(0.0),
    m_gap(0.0),
    m_trialLength(0),
    m_robotType(0),
    m_count(0),
    m_project("")
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
    //6 food collected
    //7 movement
    //8 rotation
    //9 conditionality
    
    bool usingAllObjectives = (m_project == "objectives_in_fitness_function" ||
                               m_project == "generic_subbehaviours_in_fitness_function");
    uint numScores = (usingAllObjectives) ? 10 : 4;

    for (uint i = 0; i < numScores; ++i)
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

    int trackingID;
    GetNodeAttributeOrDefault(t_node, "trackingID", trackingID, trackingID);
    GetNodeAttributeOrDefault(t_node, "verbose", m_verbose, m_verbose);
    
    m_trackingIDs.push_back(trackingID);
    
    for (uint i = 0; i < 10; ++i)
    {
        m_scores.push_back(std::vector<float>());
    }

    uint foodRegions = (m_arenaLayout == 6) ? 3 : 1;
    for (uint i = 0; i < foodRegions; ++i)
    {
        m_distFood.push_back(0.0);
    }

    m_blackBoard = new CBlackBoard(std::stoi(GetId()));

    m_project = "objectives_in_fitness_function";
}

void CFootBotBT::buildTree(std::vector<std::string> tokens)
{
    m_rootNode = new CNode(tokens, std::stoi(GetId()));
}

void CFootBotBT::calculateDistances(double x, double y)
{
    if (m_arenaLayout == 2)
    {
        calculateDistancesExp2(x, y);
    }
    else if (m_arenaLayout == 3)
    {
        calculateDistancesExp3(x, y);
    }
    else if (m_arenaLayout == 4)
    {
        calculateDistancesExp4(x, y);
    }
    else if (m_arenaLayout == 5)
    {
        calculateDistancesExp5(x, y);
    }
    else if (m_arenaLayout == 6)
    {
        calculateDistancesExp6(x, y);
    }
    else if (m_arenaLayout == 7)
    {
        calculateDistancesExp7(x, y);
    }
    else
    {
        calculateDistancesExp1(x, y);
    }
}

void CFootBotBT::calculateDistancesExp1(double x, double y)
{
    double distanceFromCentre = sqrt((x * x) + (y * y));

    double distNest = distanceFromCentre - m_nestRadius;
    double distFood = (m_gap + 0.5) - distanceFromCentre;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotBT::calculateDistancesExp2(double x, double y)
{
    double distNest = sqrt((x * x) + ((y - m_gap) * (y - m_gap))) - m_nestRadius;
    double distFood = sqrt((x * x) + ((y + m_gap) * (y + m_gap))) - m_foodRadius;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotBT::calculateDistancesExp3(double x, double y)
{
    double foodX = x > 0.0 ? m_gap : m_gap * -1;
    double foodY = y > 0.0 ? m_gap : m_gap * -1;
    double distFood = sqrt(((x - foodX) * (x - foodX)) + ((y - foodY) * (y - foodY))) - m_foodRadius;

    double distNest = sqrt((x * x) + (y * y)) - m_nestRadius;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotBT::calculateDistancesExp4(double x, double y)
{
    double distNest = (m_gap / 2) - y;
    double distFood = (m_gap / 2) + y;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotBT::calculateDistancesExp5(double x, double y)
{
    double x_plus_gap_sq = (x + m_gap + 0.05) * (x + m_gap + 0.05);
    double y_plus_gap_sq = (y + m_gap + 0.05) * (y + m_gap + 0.05);
    double x_minus_gap_sq = (x - (m_gap + 0.05)) * (x - (m_gap + 0.05));
    double y_minus_gap_sq = (y - (m_gap + 0.05)) * (y - (m_gap + 0.05));

    double distNest = sqrt((x * x) + y_minus_gap_sq) - m_nestRadius;  // red
    double distFood1 = sqrt((x * x) + y_plus_gap_sq) - m_foodRadius;  // green
    double distFood2 = sqrt(x_plus_gap_sq + (y * y)) - m_foodRadius;  // blue
    double distFood3 = sqrt(x_minus_gap_sq + (y * y)) - m_foodRadius; // purple

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood1 < 0.0 ? 0.0 : distFood1;
    m_distFood[1] = distFood2 < 0.0 ? 0.0 : distFood2;
    m_distFood[2] = distFood3 < 0.0 ? 0.0 : distFood3;
}

void CFootBotBT::calculateDistancesExp6(double x, double y)
{
    Poi nest = m_arena[0];
    Poi food1 = m_arena[1];
    Poi food2 = m_arena[2];
    Poi food3 = m_arena[3];

    double distNest  = sqrt(hypotenuseSquared(x, y, nest.m_x,  nest.m_y))  - nest.m_r;
    double distFood1 = sqrt(hypotenuseSquared(x, y, food1.m_x, food1.m_y)) - food1.m_r;
    double distFood2 = sqrt(hypotenuseSquared(x, y, food2.m_x, food2.m_y)) - food2.m_r;
    double distFood3 = sqrt(hypotenuseSquared(x, y, food3.m_x, food3.m_y)) - food3.m_r;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood1 < 0.0 ? 0.0 : distFood1;
    m_distFood[1] = distFood2 < 0.0 ? 0.0 : distFood2;
    m_distFood[2] = distFood3 < 0.0 ? 0.0 : distFood3;
}

void CFootBotBT::calculateDistancesExp7(double x, double y)
{
    Poi target;
    Poi other;

    if (m_robotType == 0) // red/blue - targeting red
    {
        target = m_arena[0];
        other = m_arena[1];
    }
    else // green/yellow - targeting green
    {
        target = m_arena[1];
        other = m_arena[0];
    }

    double distTarget = sqrt(hypotenuseSquared(x, y, target.m_x,  target.m_y))  - target.m_r;
    double distOther  = sqrt(hypotenuseSquared(x, y, other.m_x, other.m_y)) - other.m_r;

    m_distNest = distTarget < 0.0 ? 0.0 : distTarget;
    m_distFood[0] = distOther < 0.0 ? 0.0 : distOther;
}

float CFootBotBT::hypotenuseSquared(float x1, float y1, float x2, float y2) const
{
    float horizontal = x2 - x1;
    float vertical = y2 - y1;
    return (horizontal * horizontal) + (vertical * vertical);
}

void CFootBotBT::setColour() const
{
    if (m_project == "straight_to_foraging" ||
        m_project == "multi_food_foraging_with_subbehaviours")
    {
        if (m_blackBoard->getCarryingFood(0))
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::GREEN);
        }
        else if (m_blackBoard->getCarryingFood(1))
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::BLUE);
        }
        else if (m_blackBoard->getCarryingFood(2))
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::PURPLE);
        }
        else
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::RED : CColor::BLACK);
        }
    }

    else if (m_project == "generic_objectives_cast_to_grid")
    {
        if (m_blackBoard->getCarryingFood(0))
        {
            m_pcLEDs->SetAllColors(m_robotType == 0 ? CColor::GREEN : CColor::YELLOW);
        }
        else
        {
            m_pcLEDs->SetAllColors(m_robotType == 0 ? CColor::BLUE : CColor::RED);
        }
    }

    else if (m_project == "generic_subbehaviours_in_fitness_function")
    {
        m_pcLEDs->SetAllColors(m_robotType == 0 ? CColor::RED : CColor::YELLOW);
    }

    else
    {
        if (m_blackBoard->getCarryingFood(0))
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::GREEN);
        }
        else
        {
            m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::RED : CColor::BLACK);
        }
    }
}

void CFootBotBT::setParams(const std::string project, int commsRange, float velocity, int trialLength, uint robotType)
{
    m_project = project;
    m_commsRange = commsRange;
    m_trialLength = trialLength;
    m_robotType = robotType;

    Real noise;
    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    m_rWheelVelocity = velocity * noise;

    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    m_lWheelVelocity = velocity * noise;
}

void CFootBotBT::setArenaParams(int arenaLayout, float nest, float food, float gap)
{
    m_arenaLayout = arenaLayout;
    m_nestRadius = nest;
    m_foodRadius = food;
    m_gap = gap;
}

void CFootBotBT::createAndSendPayload(std::vector<uint64_t> distances) const
{
    short int id = std::stoi(GetId());

    if (id % 2 == 1 && m_project == "generic_subbehaviours_in_fitness_function")
    {
        uint64_t distTemp = distances[0];
        distances[0] = distances[1];
        distances[1] = distTemp;
    }

    uint64_t distNest  = (distances[0] == 0) ? 0 : distances[0] * 1000000000;
    uint64_t distFood1 = (distances[1] == 0) ? 0 : distances[1] * 1000000;
    uint64_t distFood2 = (distances[2] == 0) ? 0 : distances[2] * 1000;
    uint64_t distFood3 = (distances[3] == 0) ? 0 : distances[3] * 1;

    uint64_t concatenated = 1000000000000;

    concatenated = concatenated + distNest;
    concatenated = concatenated + distFood1;
    concatenated = concatenated + distFood2;
    concatenated = concatenated + distFood3;

    // fill buffer
    CByteArray cBuf;
    cBuf << (uint16_t) id;
    cBuf << (uint64_t) concatenated;

    // send signal
    m_pcRABA->ClearData();
    m_pcRABA->SetData(cBuf);
}

void CFootBotBT::decomposePayload(uint64_t concatenated, std::vector<uint64_t>& food, uint64_t& nest) const
{
    concatenated -= 1000000000000;

    nest = std::floor(concatenated / 1000000000);
    concatenated = concatenated - (nest*1000000000);

    uint64_t food1 = std::floor(concatenated / 1000000);
    concatenated = concatenated - (food1*1000000);

    uint64_t food2 = std::floor(concatenated / 1000);
    concatenated = concatenated - (food2*1000);

    uint64_t food3 = concatenated;

    if (std::stoi(GetId()) % 2 == 1 && m_project == "generic_subbehaviours_in_fitness_function")
    {
        uint64_t temp = nest;
        nest = food1;
        food1 = temp;
    }

    food.push_back(food1);
    food.push_back(food2);
    food.push_back(food3);
}

void CFootBotBT::sendInitialSignal() const
{
    // send an initial range and bearing signal so the
    // distances don't get thrown off by empty values

    short int id = std::stoi(GetId());
    uint64_t distNest  = (m_blackBoard->getInNest())        ? 0 : 500;
    uint64_t distFood1 = (m_blackBoard->getDetectedFood(0)) ? 0 : 500;
    uint64_t distFood2 = (m_blackBoard->getDetectedFood(1)) ? 0 : 500;
    uint64_t distFood3 = (m_blackBoard->getDetectedFood(2)) ? 0 : 500;

    createAndSendPayload(std::vector<uint64_t>{distNest, distFood1, distFood2, distFood3});
}

void CFootBotBT::recordInitialPositions(bool tracking) 
{
    std::pair<Real, Real> location = getLocation(tracking);

    m_blackBoard->setInitialAbsolutePosition(location.first, location.second);
    m_blackBoard->setInitialAbsoluteDistanceFromFood(m_distFood[0], tracking);
    m_blackBoard->setInitialAbsoluteDistanceFromNest(m_distNest, tracking);
}

void CFootBotBT::recordFinalPositions(bool tracking) 
{
    std::pair<Real, Real> location = getLocation(tracking);

    m_blackBoard->setFinalAbsolutePosition(location.first, location.second);

    m_blackBoard->setFinalAbsoluteDistanceFromFood(m_distFood[0], tracking);
    m_blackBoard->setFinalAbsoluteDistanceFromNest(m_distNest, tracking);

    m_blackBoard->setAbsoluteDistanceToNestAvg(m_trialLength, tracking);
    m_blackBoard->setAbsoluteDistanceToFoodAvg(m_trialLength, tracking);
    m_blackBoard->setNeighbourDistanceAvg(m_trialLength, tracking);
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

std::pair<Real, Real> CFootBotBT::getLocation(bool tracking)
{
    // position data
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();
    return std::make_pair(x, y);
}

void CFootBotBT::position(bool tracking)
{
    uint foodRegions = (m_arenaLayout == 6) ? 3 : 1;

    // position data
    std::pair<Real, Real> location = getLocation(tracking);
    calculateDistances(location.first, location.second);

    // update the blackboard to reflect whether the robot is in the food region
    for (uint i = 0; i < foodRegions; i++)
    {
        m_blackBoard->setDetectedFood(i, m_distFood[i] <= 0.0, tracking);
        m_blackBoard->setCarryingFood(i, m_blackBoard->getCarryingFood(i) || m_blackBoard->getDetectedFood(i));
    }

    // update the blackboard to reflect whether the robot is in the nest region
    m_blackBoard->setInNest(m_distNest <= 0.0);
    
    // if this robot has arrived in the nest with food increment scores and update blackboard
    for (uint i = 0; i < foodRegions; i++)
    {
        if (m_blackBoard->getInNest() && m_blackBoard->getCarryingFood(i))
        {
            m_blackBoard->incrementFood(i, tracking);
            m_blackBoard->setCarryingFood(i, false);
        }
    }
}

void CFootBotBT::recordRangeAndBearingData(const Real distance, const CRadians bearing, float& shortestDistance, CRadians& shortestDirection) const
{
    if (distance < shortestDistance)
    {
        shortestDistance = distance;
        shortestDirection = bearing;
    }
}

void CFootBotBT::rangeAndBearing(bool tracking)
{
    uint foodRegions = (m_arenaLayout == 6) ? 3 : 1;
    float maxDistance = 500;

    // range and bearing data
    const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();

    // map for density of robots
    std::map<int, double> IDs;

    float closestNeighbourDistance = 700.0;
    CRadians closestNeighbourDirection;

    float distanceToNest = m_blackBoard->getInNest() ? 0 : maxDistance;
    CRadians closestNestDirection;

    std::vector<float> distanceToFood;
    std::vector<CRadians> closestFoodDirection;
    for (uint i = 0; i < foodRegions; ++i)
    {
        distanceToFood.push_back(m_blackBoard->getDetectedFood(i) ? 0 : maxDistance);
        closestFoodDirection.push_back(CRadians::ZERO);
    }

    // for each range and bearing signal received 
    for(size_t i = 0; i < tPackets.size(); ++i)
    {
        auto data = tPackets[i].Data;
        auto bearing = tPackets[i].HorizontalBearing;

        if (tPackets[i].Range > m_commsRange || std::rand() % 20 == 0)
        {
            continue;
        }

        uint16_t id;
        uint64_t concatenated;
        data >> id;
        data >> concatenated;

        uint64_t nest = 500;
        std::vector<uint64_t> food;
        decomposePayload(concatenated, food, nest);

        // if we haven't already received a signal from this robot in the current timestep
        if (IDs.find(id) == IDs.end())
        {
            recordRangeAndBearingData(tPackets[i].Range, bearing, closestNeighbourDistance, closestNeighbourDirection);
            recordRangeAndBearingData(nest + tPackets[i].Range, bearing, distanceToNest, closestNestDirection);
            for (uint j = 0; j < foodRegions; ++j)
            {
                recordRangeAndBearingData(food[j] + tPackets[i].Range, bearing, distanceToFood[j], closestFoodDirection[j]);
            }

            // store density value for the robot sending this signal
            Real density = 1 / (ARGOS_PI * ((tPackets[i].Range / 1000) * (tPackets[i].Range / 1000))); // max = 1107
            IDs.insert(std::pair<int, double>(id, density));
        }
    }

    // density

    float density = 0;
    for (auto it = IDs.begin(); it != IDs.end(); ++it)
    {
        density += it->second;
    }
    m_blackBoard->updateDensityVector(density, tracking);
    if (m_count % m_trialLength == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDensity(tracking);
    }

    // neighbours

    bool closestNeighbourToLeft = false;
    bool closestNeighbourToRight = false;
    Real angle = closestNeighbourDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;

    if (closestNeighbourDistance < 700.0)
    {
        if (angle < 0)
        {
            closestNeighbourToRight = true;
        }
        else if (angle >= 0)
        {
            closestNeighbourToLeft = true;
        }
    }
    m_blackBoard->setNearestNeighbourToLeft(closestNeighbourToLeft);
    m_blackBoard->setNearestNeighbourToRight(closestNeighbourToRight);
    m_blackBoard->accumulateNeighbourDistances(closestNeighbourDistance, tracking);
    
    if ((m_count % m_trialLength) == 2)
    {
        m_blackBoard->setInitialNeighbourDistance(closestNeighbourDistance, tracking);
    }

    // nest

    m_blackBoard->updateDistNestVector(distanceToNest, tracking);
    m_blackBoard->accumulateAbsoluteDistanceToNest(m_distNest);
    if (m_count % m_trialLength == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistNest(tracking);
    }

    Real nestDirectionDegrees = closestNestDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    m_blackBoard->setNestToRight(distanceToNest < maxDistance && distanceToNest > 0 && nestDirectionDegrees < 0.0);
    m_blackBoard->setNestToLeft(distanceToNest < maxDistance && distanceToNest > 0 && nestDirectionDegrees > 0.0);

    // food

    m_blackBoard->accumulateAbsoluteDistanceToFood(m_distFood[0], tracking);
    for (uint i = 0; i < foodRegions; ++i)
    {
        m_blackBoard->updateDistFoodVector(i, distanceToFood[i], tracking);
        if (m_count % m_trialLength == 2 || m_count % 4 == 0)
        {
            m_blackBoard->setDistFood(i, tracking);
        }

        Real foodDirectionDegrees = closestFoodDirection[i].GetValue() * CRadians::RADIANS_TO_DEGREES;
        m_blackBoard->setFoodToRight(i, distanceToFood[i] < maxDistance && distanceToFood[i] > 0 && foodDirectionDegrees < 0.0);
        m_blackBoard->setFoodToLeft (i, distanceToFood[i] < maxDistance && distanceToFood[i] > 0 && foodDirectionDegrees > 0.0);
    }
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
    
    uint64_t distNest = m_blackBoard->getDistNest()   * 500;
    uint64_t distFood1 = m_blackBoard->getDistFood(0) * 500;
    uint64_t distFood2 = m_blackBoard->getDistFood(1) * 500;
    uint64_t distFood3 = m_blackBoard->getDistFood(2) * 500;
    
    createAndSendPayload(std::vector<uint64_t>{distNest, distFood1, distFood2, distFood3});
    
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

        // print all nodes traversed on each tick
        // if (tracking) std::cout << output << std::endl;
    }

    if (m_count % m_trialLength != 1)
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
        m_blackBoard->setInitialDensity(tracking);
        m_blackBoard->setInitialDistanceFromNest(tracking);
        m_blackBoard->setInitialDistanceFromFood(tracking);
    }

    if (m_count % m_trialLength == 0)
    {
        recordFinalPositions(tracking);

        m_blackBoard->setFinalDensity(tracking);
        m_blackBoard->setFinalDistanceFromNest(tracking);
        m_blackBoard->setFinalDistanceFromFood(tracking);
    }

    if (m_count % m_trialLength == 0 && m_project == "objectives_in_fitness_function")
    {
        m_scores[0].push_back(m_blackBoard->getDifferenceInDensity());
        m_scores[1].push_back(m_blackBoard->getDifferenceInDistanceFromNest());
        m_scores[2].push_back(m_blackBoard->getDifferenceInDistanceFromFood());
        m_scores[3].push_back(m_blackBoard->getDifferenceInDensityInverse());
        m_scores[4].push_back(m_blackBoard->getDifferenceInDistanceFromNestInverse());
        m_scores[5].push_back(m_blackBoard->getDifferenceInDistanceFromFoodInverse(tracking));
        //m_scores[5].push_back(m_blackBoard->getAbsoluteDifferenceInDistanceFromFoodInverse(tracking));

        m_scores[6].push_back(static_cast<float>(m_blackBoard->getFoodOfType(0)));

        m_scores[7].push_back(static_cast<float>(m_blackBoard->getMovement()));
        m_scores[8].push_back(static_cast<float>(m_blackBoard->getRotations()));
        m_scores[9].push_back(static_cast<float>(m_blackBoard->getConditionality()));

        m_blackBoard->setMovement(0);
        m_blackBoard->setRotations(0);
        m_blackBoard->setConditions(0);
        m_blackBoard->setActions(0);
    }

    if (m_count % m_trialLength == 0 && m_project == "objectives_cast_to_grid")
    {
        int foundFood = m_blackBoard->getCarryingFood(0) ? 1 : 0;
        m_scores[0].push_back(m_blackBoard->getAbsoluteDelta());

        m_scores[1].push_back(m_blackBoard->getNeighbourDistanceAvg());
        m_scores[2].push_back(m_blackBoard->getAbsoluteDistanceToNestAvg());
        m_scores[3].push_back(m_blackBoard->getAbsoluteDistanceToFoodAvg());
    }

    if (m_count % m_trialLength == 0 && m_project == "generic_subbehaviours_in_fitness_function")
    {
        m_scores[0].push_back(m_blackBoard->getDifferenceInDensity());
        m_scores[1].push_back(m_blackBoard->getDifferenceInDistanceFromNest()); // target
        m_scores[2].push_back(m_blackBoard->getDifferenceInDistanceFromFood()); // other
        m_scores[3].push_back(m_blackBoard->getDifferenceInDensityInverse());
        m_scores[4].push_back(m_blackBoard->getDifferenceInDistanceFromNestInverse()); // target
        m_scores[5].push_back(m_blackBoard->getDifferenceInDistanceFromFoodInverse(tracking)); // other
        m_scores[6].push_back(static_cast<float>(m_blackBoard->getFoodOfType(0))); // arbitrary

        m_scores[7].push_back(static_cast<float>(m_blackBoard->getMovement()));
        m_scores[8].push_back(static_cast<float>(m_blackBoard->getRotations()));
        m_scores[9].push_back(static_cast<float>(m_blackBoard->getConditionality()));

        m_blackBoard->setMovement(0);
        m_blackBoard->setRotations(0);
        m_blackBoard->setConditions(0);
        m_blackBoard->setActions(0);
    }

    if (m_count % m_trialLength == 0 && m_project == "generic_objectives_cast_to_grid_perceived")
    {
        m_scores[0].push_back(m_blackBoard->getAbsoluteDelta());

        //m_scores[1].push_back(m_blackBoard->getNeighbourDistanceAvg());
        m_scores[1].push_back(m_blackBoard->getDifferenceInDensity());
        m_scores[2].push_back(m_blackBoard->getDifferenceInDistanceFromNest());
        m_scores[3].push_back(m_blackBoard->getDifferenceInDistanceFromFood());
    }

    if (m_count % m_trialLength == 0 && m_project == "generic_objectives_cast_to_grid_absolute")
    {
        m_scores[0].push_back(m_blackBoard->getAbsoluteDelta());

        //m_scores[1].push_back(m_blackBoard->getNeighbourDistanceAvg());
        m_scores[1].push_back(m_blackBoard->getDifferenceInDensity());
        m_scores[2].push_back(m_blackBoard->getAbsoluteDistanceToNestAvg()); // target
        m_scores[3].push_back(m_blackBoard->getAbsoluteDistanceToFoodAvg()); // other
    }

    if (m_count % m_trialLength == 0 && (m_project == "straight_to_foraging" ||
                                         m_project == "multi_food_foraging_with_subbehaviours"))
    {
        m_scores[0].push_back(m_blackBoard->getTotalFood());

        m_scores[1].push_back(m_blackBoard->getFoodOfType(0));
        m_scores[2].push_back(m_blackBoard->getFoodOfType(1));
        m_scores[3].push_back(m_blackBoard->getFoodOfType(2));
    }

    if (m_count % m_trialLength == 0)
    {
        m_blackBoard->reset();
    }

    setColour();

}

bool CFootBotBT::inTrackingIDs() const
{
    return (std::find(m_trackingIDs.begin(), m_trackingIDs.end(), std::stoi(GetId())) != m_trackingIDs.end());
}

REGISTER_CONTROLLER(CFootBotBT, "footbot_bt_controller")
