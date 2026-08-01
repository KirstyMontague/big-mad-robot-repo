#include "footbot_nn.h"

#include <algorithm>

CFootBotNNController::CFootBotNNController() :
    m_pcWheels(NULL),
    m_pcLEDs(NULL),
    m_pcPosition(NULL),
    m_pcRABA(NULL),
    m_pcRABS(NULL),
    m_rWheelVelocity(5.0f),
    m_lWheelVelocity(5.0f),
    m_verbose(false),
    m_nestRadius(0.5),
    m_foodRadius(0.5),
    m_commsRange(100.0),
    m_distNest(0.0),
    m_gap(0.0),
    m_trialLength(0),
    m_count(0),
    m_isForaging(false)
{}

CFootBotNNController::~CFootBotNNController()
{
    std::cout << "result " << GetId();

    for (uint i = 0; i < 10; ++i)
    {
        for (float s : m_scores[i])
        {
            std::cout << " " << std::to_string(s);
        }
    }

    std::cout << "\n";
}

void CFootBotNNController::Init(TConfigurationNode& t_node)
{
    m_node = t_node;

    m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
    m_pcRABA      = GetActuator<CCI_RangeAndBearingActuator     >("range_and_bearing"    );
    m_pcLEDs      = GetActuator<CCI_LEDsActuator                >("leds"                 );

    m_pcPosition  = GetSensor  <CCI_PositioningSensor           >("positioning"          );
    m_pcRABS      = GetSensor  <CCI_RangeAndBearingSensor       >("range_and_bearing"    );

    int trackingID;
    GetNodeAttributeOrDefault(t_node, "trackingID", trackingID, trackingID);
    m_trackingIDs.push_back(trackingID);

    Real wheelVelocity;
    GetNodeAttributeOrDefault(t_node, "velocity", wheelVelocity, wheelVelocity);
    
    GetNodeAttributeOrDefault(t_node, "verbose", m_verbose, m_verbose);

    Real noise;
    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    Real rightWheelVelocity = wheelVelocity * noise;
    m_rWheelVelocity = wheelVelocity * noise;

    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    Real leftWheelVelocity = wheelVelocity * noise;
    m_lWheelVelocity = wheelVelocity * noise;
    
    for (uint i = 0; i < 10; ++i)
    {
        m_scores.push_back(std::vector<float>());
    }

    uint foodRegions = numFoodRegions();
    for (uint i = 0; i < foodRegions; ++i)
    {
        m_distFood.push_back(0.0);
    }

    m_blackBoard = new CBlackBoard(std::stoi(GetId()));
}

void CFootBotNNController::InitNN(const Real* chromosome, UInt32 numInputs, UInt32 numHidden, UInt32 numOutputs)
{
    try
    {
        m_cPerceptron.Init(m_node, numInputs, numHidden, numOutputs);
    }
    catch(CARGoSException& ex)
    {
        THROW_ARGOSEXCEPTION_NESTED("Error initializing the perceptron network", ex);
    }

    m_cPerceptron.Load(chromosome, inTrackingIDs());
}

void CFootBotNNController::calculateDistances(double x, double y)
{
   calculateDistancesExp1(x, y);
}

void CFootBotNNController::calculateDistancesExp1(double x, double y)
{
    double distanceFromCentre = sqrt((x * x) + (y * y));

    double distNest = distanceFromCentre - m_nestRadius;
    double distFood = (m_gap + 0.5) - distanceFromCentre;

    m_distNest = distNest < 0.0 ? 0.0 : distNest;
    m_distFood[0] = distFood < 0.0 ? 0.0 : distFood;
}

void CFootBotNNController::setColour() const
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

void CFootBotNNController::setParams(float gap, int trialLength, bool isForaging)
{
    m_trialLength = trialLength;
    m_gap = gap;
    m_isForaging = isForaging;
}

void CFootBotNNController::createAndSendPayload(std::vector<uint64_t> distances) const
{
    short int id = std::stoi(GetId());

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

void CFootBotNNController::decomposePayload(uint64_t concatenated, std::vector<uint64_t>& food, uint64_t& nest) const
{
    concatenated -= 1000000000000;

    nest = std::floor(concatenated / 1000000000);
    concatenated = concatenated - (nest*1000000000);

    uint64_t food1 = std::floor(concatenated / 1000000);
    concatenated = concatenated - (food1*1000000);

    uint64_t food2 = std::floor(concatenated / 1000);
    concatenated = concatenated - (food2*1000);

    uint64_t food3 = concatenated;

    food.push_back(food1);
    food.push_back(food2);
    food.push_back(food3);
}

void CFootBotNNController::sendInitialSignal() const
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

void CFootBotNNController::recordInitialPositions(bool tracking)
{
    std::pair<Real, Real> location = getLocation(tracking);

    m_blackBoard->setInitialAbsoluteDistanceFromFood(m_distFood[0], tracking);
}

void CFootBotNNController::recordFinalPositions(bool tracking)
{
    std::pair<Real, Real> location = getLocation(tracking);

    m_blackBoard->setFinalAbsoluteDistanceFromFood(m_distFood[0], tracking);
}

std::pair<Real, Real> CFootBotNNController::getLocation(bool tracking)
{
    // position data
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();
    return std::make_pair(x, y);
}

void CFootBotNNController::position(bool tracking)
{
    uint foodRegions = numFoodRegions();

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

void CFootBotNNController::recordRangeAndBearingData(const Real distance, const CRadians bearing, float& shortestDistance, CRadians& shortestDirection) const
{
    if (distance < shortestDistance)
    {
        shortestDistance = distance;
        shortestDirection = bearing;
    }
}

void CFootBotNNController::rangeAndBearing(bool tracking)
{
    uint foodRegions = numFoodRegions();
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
        if (tPackets[i].Range > m_commsRange || std::rand() % 20 == 0)
        {
            continue;
        }

        auto data = tPackets[i].Data;
        auto bearing = tPackets[i].HorizontalBearing;

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

    // nest

    m_blackBoard->updateDistNestVector(distanceToNest, tracking);
    if (m_count % m_trialLength == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistNest(tracking);
    }

    Real nestDirectionDegrees = closestNestDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    m_blackBoard->setNestToRight(distanceToNest < maxDistance && distanceToNest > 0 && nestDirectionDegrees < 0.0);
    m_blackBoard->setNestToLeft(distanceToNest < maxDistance && distanceToNest > 0 && nestDirectionDegrees > 0.0);

    // food

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

void CFootBotNNController::sensing()
{
    bool tracking = inTrackingIDs() && m_verbose;

    position(tracking);
    rangeAndBearing(tracking);
}

void CFootBotNNController::actuation()
{
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

void CFootBotNNController::ControlStep()
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
        std::vector<float> inputs;
        inputs.push_back(static_cast<float>(m_blackBoard->getInNest()));
        inputs.push_back(static_cast<float>(m_blackBoard->getDetectedFood(0)));
        if (m_isForaging)
        {
            inputs.push_back(static_cast<float>(m_blackBoard->getCarryingFood(0)));
        }
        inputs.push_back(static_cast<float>(m_blackBoard->getNestToLeft()));
        inputs.push_back(static_cast<float>(m_blackBoard->getNestToRight()));
        inputs.push_back(static_cast<float>(m_blackBoard->getFoodToLeft(0)));
        inputs.push_back(static_cast<float>(m_blackBoard->getFoodToRight(0)));
        inputs.push_back(static_cast<float>(m_blackBoard->getNearestNeighbourToLeft()));
        inputs.push_back(static_cast<float>(m_blackBoard->getNearestNeighbourToRight()));

        for (uint i = 0; i < inputs.size(); ++i)
        {
            m_cPerceptron.SetInput(i, inputs[i]);
        }

        m_blackBoard->setMotors(0);
        m_cPerceptron.ComputeOutputs(tracking);
        
        (m_cPerceptron.GetOutput(0) <= 1.0) ? m_blackBoard->setMotors(0)
        : (m_cPerceptron.GetOutput(0) <= 2.0) ? m_blackBoard->setMotors(1)
        : (m_cPerceptron.GetOutput(0) <= 3.0) ? m_blackBoard->setMotors(2)
        : (m_cPerceptron.GetOutput(0) <= 4.0) ? m_blackBoard->setMotors(3)
        : (m_cPerceptron.GetOutput(0) <= 5.0) ? m_blackBoard->setMotors(4)
        : (m_cPerceptron.GetOutput(0) <= 6.0) ? m_blackBoard->setMotors(5)
        : m_blackBoard->setMotors(6);
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

        m_scores[0].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDensity());
        m_scores[1].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDistanceFromNest());
        m_scores[2].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDistanceFromFood());
        m_scores[3].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDensityInverse());
        m_scores[4].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDistanceFromNestInverse());
        m_scores[5].push_back(m_isForaging ? 0.0 : m_blackBoard->getDifferenceInDistanceFromFoodInverse(tracking));
        //m_scores[5].push_back(m_isForaging ? 0.0 : m_blackBoard->getAbsoluteDifferenceInDistanceFromFoodInverse(tracking));
        m_scores[6].push_back(m_isForaging ? static_cast<float>(m_blackBoard->getFoodOfType(0)) : 0.0);

        m_scores[7].push_back(static_cast<float>(m_blackBoard->getMovement()));
        m_scores[8].push_back(static_cast<float>(m_blackBoard->getRotations()));
        m_scores[9].push_back(static_cast<float>(m_blackBoard->getConditionality()));

        m_blackBoard->setMovement(0);
        m_blackBoard->setRotations(0);
        m_blackBoard->setConditions(0);
        m_blackBoard->setActions(0);
        
        m_blackBoard->reset();
    }

    setColour();

}

bool CFootBotNNController::inTrackingIDs() const
{
    return (std::find(m_trackingIDs.begin(), m_trackingIDs.end(), std::stoi(GetId())) != m_trackingIDs.end());
}

uint CFootBotNNController::numFoodRegions() const
{
    return 1;
}

void CFootBotNNController::Reset()
{
   m_cPerceptron.Reset();
}

void CFootBotNNController::Destroy()
{
   m_cPerceptron.Destroy();
}

REGISTER_CONTROLLER(CFootBotNNController, "footbot_nn")
