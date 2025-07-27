#include "footbot_nn.h"

#include <algorithm>

/****************************************/
/****************************************/

static CRange<Real> NN_OUTPUT_RANGE(0.0f, 1.0f);
static CRange<Real> LEFT_WHEEL_ACTUATION_RANGE(-5.0f, 5.0f);
static CRange<Real> RIGHT_WHEEL_ACTUATION_RANGE(-5.0f, 5.0f);

/****************************************/
/****************************************/

CFootBotNNController::CFootBotNNController() :
    m_pcLEDs(NULL),
    m_pcPosition(NULL),
    m_rWheelVelocity(5.0f),
    m_lWheelVelocity(5.0f),
    m_count(0),
    m_params(0.5),
    m_carryingFood(false),
    m_food(0)
{}

CFootBotNNController::~CFootBotNNController()
{
    std::cout << "result " << GetId();

    std::vector<int> x{0,1,2,3,4,5,6,7,8,9};
    for (int i : x)
    {
        for (float s : m_scores[i])
        {
            std::cout << " " << std::to_string(s);
        }
    }

    std::cout << "\n";
}

/****************************************/
/****************************************/

void CFootBotNNController::Init(TConfigurationNode& t_node)
{
   /*
    * Get sensor/actuator handles
    */
    m_node = t_node;
    try
    {
        m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
        m_pcRABA      = GetActuator<CCI_RangeAndBearingActuator>("range_and_bearing");
        m_pcLEDs      = GetActuator<CCI_LEDsActuator>("leds");

        m_pcProximity = GetSensor<CCI_FootBotProximitySensor>("footbot_proximity");
        m_pcLight     = GetSensor<CCI_FootBotLightSensor>("footbot_light");
        m_pcPosition  = GetSensor<CCI_PositioningSensor>("positioning");
        m_pcRABS      = GetSensor<CCI_RangeAndBearingSensor>("range_and_bearing");
    }
    catch(CARGoSException& ex)
    {
        THROW_ARGOSEXCEPTION_NESTED("Error initializing sensors/actuators", ex);
    }

    /* Initialize the perceptron */
    try
    {
        m_cPerceptron.Init(m_node);
    }
    catch(CARGoSException& ex)
    {
        THROW_ARGOSEXCEPTION_NESTED("Error initializing the perceptron network", ex);
    }

    Real wheelVelocity;
    GetNodeAttributeOrDefault(t_node, "velocity", wheelVelocity, wheelVelocity);
    
    GetNodeAttributeOrDefault(t_node, "trackingID", m_trackingID, m_trackingID);
    m_trackingIDs.push_back(m_trackingID);

    setDefaultLEDs(inTrackingIDs());

    Real noise;
    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    Real rightWheelVelocity = wheelVelocity * noise;
    m_rWheelVelocity = wheelVelocity * noise;

    noise = (std::rand() % 20);
    noise = (noise + 90) / 100;
    Real leftWheelVelocity = wheelVelocity * noise;
    m_lWheelVelocity = wheelVelocity * noise;
    
    LEFT_WHEEL_ACTUATION_RANGE.SetMin(leftWheelVelocity * -1);
    LEFT_WHEEL_ACTUATION_RANGE.SetMax(leftWheelVelocity);
    RIGHT_WHEEL_ACTUATION_RANGE.SetMin(rightWheelVelocity * -1);
    RIGHT_WHEEL_ACTUATION_RANGE.SetMax(rightWheelVelocity);
    
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
    m_scores.push_back(std::vector<float>());
}

void CFootBotNNController::InitNN(const Real* chromosome)
{
    m_cPerceptron.Load(chromosome, inTrackingIDs());
}

void CFootBotNNController::createBlackBoard(int numRobots)
{
    m_blackBoard = new CBlackBoard(numRobots);
}

void CFootBotNNController::setParams(float gap)
{
    m_params = gap;
}

/****************************************/
/****************************************/

void CFootBotNNController::sensing(bool tracking) 
{
    double r = position(tracking);
    rangeAndBearing(r, tracking);
}

double CFootBotNNController::position(bool tracking) 
{
    // position data
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();	
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();

    // distance from the centre of the arena
    double r = sqrt((x * x) + (y * y));

    // update the blackboard to reflect whether the robot is in the food region
    m_blackBoard->setDetectedFood(m_count, r >= .5 + m_params, (tracking ? std::stoi(GetId()) : -1));
    m_blackBoard->setCarryingFood(m_blackBoard->getCarryingFood() || r >= .5 + m_params);

    // update the blackboard to reflect whether the robot is in the nest region
    m_blackBoard->setInNest(m_count, r < 0.5, (tracking ? std::stoi(GetId()) : -1));

    if (r < .5 && m_blackBoard->getCarryingFood())
    {
        m_food++;
        m_blackBoard->setCarryingFood(false);
        setDefaultLEDs(tracking);
    }

    if (r >= .5 + m_params)
    {
        setFoodLEDs(tracking);
    }

    if (m_count == 1)
    {
        // record absolute position
        m_blackBoard->setInitialAbsoluteDistanceFromFood(r, 0.5 + m_params, tracking ? std::stoi(GetId()) : -1);
    }
    

    return r;
}

void CFootBotNNController::rangeAndBearing(double r, bool tracking) 
{
    // range and bearing data
    const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();	

    // map for density of robots and defaults for distance to food or nest
    std::map<int, double> IDs;
    float nestRange = (r < .5) ? 0 : 500;
    float foodRange = (r < .5 + m_params) ? 500 : 0;
    CRadians closestNestDirection;
    CRadians closestFoodDirection;
    CRadians closestNeighbourDirection;
    float closestNeighbourDistance = 0.0;

    // for each range and bearing signal received 
    for(size_t i = 0; i < tPackets.size(); ++i)
    {
        if (std::rand() % 20 == 0)
        {
            continue;
        }

        if (tPackets[i].Range > 100)
        {
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
        
        //if (tracking && id == 0) std::cout << id << " - " << nest << " - " << food << " - " << tPackets[i].Range << std::endl;
        
        // if we haven't already received a signal from this robot in the current timestep	
        if (IDs.find(id) == IDs.end())
        {
            if (closestNeighbourDistance == 0.0 || tPackets[i].Range < closestNeighbourDistance)
            {
                closestNeighbourDistance = tPackets[i].Range;
                closestNeighbourDirection = bearing;
            }
            if (nest + tPackets[i].Range < nestRange)
            {
                nestRange = nest + tPackets[i].Range;
                closestNestDirection = bearing;
            }
            if (food + tPackets[i].Range < foodRange)
            {
                foodRange = food + tPackets[i].Range;
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
    m_blackBoard->updateDistNestVector(nestRange, tracking ? std::stoi(GetId()) : -1);
    if (m_count == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistNest((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
    }

    // save distance to food and change in distance
    m_blackBoard->updateDistFoodVector(foodRange, (tracking ? std::stoi(GetId()) : -1));
    if (m_count == 2 || m_count % 4 == 0)
    {
        m_blackBoard->setDistFood((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
    }

    // navigation
    Real nestDirectionDegrees = closestNestDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    Real foodDirectionDegrees = closestFoodDirection.GetValue() * CRadians::RADIANS_TO_DEGREES;
    m_blackBoard->setNestToRight(nestRange < 500 && nestRange > 0 && nestDirectionDegrees < 0.0);
    m_blackBoard->setNestToLeft(nestRange < 500 && nestRange > 0 && nestDirectionDegrees > 0.0);
    m_blackBoard->setFoodToRight(foodRange < 500 && foodRange > 0 && foodDirectionDegrees < 0.0);
    m_blackBoard->setFoodToLeft(foodRange < 500 && foodRange > 0 && foodDirectionDegrees > 0.0);
}

void CFootBotNNController::actuation(bool tracking)
{
    short int id = std::stoi(GetId());
    short int distNest = m_blackBoard->getDistNest() * 500;
    short int distFood = m_blackBoard->getDistFood() * 500;
    short int sendSignal = 0;

    // write robot ID, distance to nest, distance to food and signal to buffer
    CByteArray cBuf;
    cBuf << std::stoi(GetId());
    cBuf << distNest;
    cBuf << distFood;
    cBuf << sendSignal;

    // send range and bearing signal
    m_pcRABA->ClearData();
    m_pcRABA->SetData(cBuf);

    // should probably be in control step instead of here
    m_cPerceptron.SetInput(0, static_cast<float>(m_blackBoard->getInNest()));
    m_cPerceptron.SetInput(1, static_cast<float>(m_blackBoard->getDetectedFood()));
    m_cPerceptron.SetInput(2, static_cast<float>(m_blackBoard->getCarryingFood()));
    m_cPerceptron.SetInput(3, static_cast<float>(m_blackBoard->getNestToLeft()));
    m_cPerceptron.SetInput(4, static_cast<float>(m_blackBoard->getNestToRight()));
    m_cPerceptron.SetInput(5, static_cast<float>(m_blackBoard->getFoodToLeft()));
    m_cPerceptron.SetInput(6, static_cast<float>(m_blackBoard->getFoodToRight()));
    m_cPerceptron.SetInput(7, static_cast<float>(m_blackBoard->getNearestNeighbourToLeft()));
    m_cPerceptron.SetInput(8, static_cast<float>(m_blackBoard->getNearestNeighbourToRight()));
        
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

void CFootBotNNController::sendInitialSignal() 
{
    // position data
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();	
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();

    // distance from the centre of the arena
    double r = sqrt((x * x) + (y * y));

    // update the blackboard to reflect whether the robot is in the food / nest region
    m_blackBoard->setDetectedFood(m_count, r >= .5 + m_params);
    m_blackBoard->setInNest(m_count, r < 0.5);

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

void CFootBotNNController::recordInitialPositions(bool tracking) 
{
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();

    double radius = sqrt((x * x) + (y * y));
    double threshold = 0.5 + m_params;

    m_blackBoard->setInitialAbsoluteDistanceFromFood(radius, threshold, tracking ? std::stoi(GetId()) : -1);
}

void CFootBotNNController::recordFinalPositions(bool tracking) 
{
    const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();	
    Real x = pos.Position.GetX();
    Real y = pos.Position.GetY();

    double radius = sqrt((x * x) + (y * y));
    double threshold = 0.5 + m_params;

    m_blackBoard->setFinalAbsoluteDistanceFromFood(radius, threshold, tracking ? std::stoi(GetId()) : -1);
}

/****************************************/
/****************************************/

void CFootBotNNController::ControlStep()
{
    bool tracking = inTrackingIDs();

    m_count++;

    if ((m_count % 160) == 1)
    {
        sendInitialSignal();
        recordInitialPositions(tracking);
    }
    else
    {
        sensing(tracking);
    }

    if (m_count % 4 == 0)
    {
        // should probably be here instead of in actuation()
        
        // m_cPerceptron.SetInput(0, static_cast<float>(m_blackBoard->getInNest()));
        // m_cPerceptron.SetInput(1, static_cast<float>(m_blackBoard->getDetectedFood()));
        // m_cPerceptron.SetInput(2, static_cast<float>(m_blackBoard->getCarryingFood()));
        // m_cPerceptron.SetInput(3, static_cast<float>(m_blackBoard->getNestToLeft()));
        // m_cPerceptron.SetInput(4, static_cast<float>(m_blackBoard->getNestToRight()));
        // m_cPerceptron.SetInput(5, static_cast<float>(m_blackBoard->getFoodToLeft()));
        // m_cPerceptron.SetInput(6, static_cast<float>(m_blackBoard->getFoodToRight()));
        // m_cPerceptron.SetInput(7, static_cast<float>(m_blackBoard->getNearestNeighbourToLeft()));
        // m_cPerceptron.SetInput(8, static_cast<float>(m_blackBoard->getNearestNeighbourToRight()));
        
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
    
    if (m_count > 1)
    {
        actuation(tracking);
    }

    if (m_blackBoard->getMotors() > 0 && m_count % 4 == 0)
    {
        m_blackBoard->addMovement();
        m_blackBoard->addRotation();
        // if (tracking) std::cout << m_blackBoard->getMovement() << " " << m_blackBoard->getRotations() << std::endl;
    }

    if ((m_count - 16) % 160 == 0)
    {
        m_blackBoard->setInitialDensity(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setInitialDistanceFromNest(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setInitialDistanceFromFood(tracking ? std::stoi(GetId()) : -1);
    }

    if (m_count % 160 == 0)
    {
        recordFinalPositions(tracking);

        m_blackBoard->setFinalDensity(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setFinalDistanceFromNest(tracking ? std::stoi(GetId()) : -1);
        m_blackBoard->setFinalDistanceFromFood(tracking ? std::stoi(GetId()) : -1);
        
        // sub-behaviours
        m_scores[0].push_back(m_blackBoard->getDifferenceInDensity());	
        m_scores[1].push_back(m_blackBoard->getDifferenceInDistanceFromNest());	
        m_scores[2].push_back(m_blackBoard->getDifferenceInDistanceFromFood());
        m_scores[3].push_back(m_blackBoard->getDifferenceInDensityInverse());
        m_scores[4].push_back(m_blackBoard->getDifferenceInDistanceFromNestInverse());
        m_scores[5].push_back(m_blackBoard->getAbsoluteDifferenceInDistanceFromFoodInverse(0.5 + m_params, tracking ? std::stoi(GetId()) : -1));
        
        // foraging
        m_scores[6].push_back(static_cast<float>(m_food));
        
        // qdpy 
        m_scores[7].push_back(static_cast<float>(m_blackBoard->getMovement()));
        m_scores[8].push_back(static_cast<float>(m_blackBoard->getRotations()));
        m_scores[9].push_back(static_cast<float>(m_blackBoard->getConditionality()));
        
        m_blackBoard->setMovement(0);
        m_blackBoard->setRotations(0);
        m_blackBoard->setConditions(0);
        m_blackBoard->setActions(0);
        
        // reset
        m_blackBoard->setCarryingFood(false);
        m_food = 0;
        setDefaultLEDs(tracking);
    }
}

/****************************************/
/****************************************/

bool CFootBotNNController::inTrackingIDs()
{
    return (std::find(m_trackingIDs.begin(), m_trackingIDs.end(), std::stoi(GetId())) != m_trackingIDs.end());
}

void CFootBotNNController::setDefaultLEDs(bool tracking)
{
    m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::YELLOW : CColor::BLUE);
}

void CFootBotNNController::setFoodLEDs(bool tracking)
{
    m_pcLEDs->SetAllColors(inTrackingIDs() ? CColor::RED : CColor::GREEN);
}

/****************************************/
/****************************************/

void CFootBotNNController::Reset()
{
   m_cPerceptron.Reset();
}

void CFootBotNNController::Destroy()
{
   m_cPerceptron.Destroy();
}

/****************************************/
/****************************************/

REGISTER_CONTROLLER(CFootBotNNController, "footbot_nn")
