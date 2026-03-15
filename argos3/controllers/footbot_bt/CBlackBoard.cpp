#include "CBlackBoard.h"


void CBlackBoard::reset()
{
    m_absoluteDistanceFromFoodTotal = 0.0;
    m_absoluteDistanceFromNestTotal = 0.0;
    m_nearestNeighbourTotal = 0.0;

    m_distNestVector.clear();

    for (uint i = 0; i < 3; ++i)
    {
        m_food[i] = 0;
        m_distFoodVectors[i].clear();
        m_carryingFood[i] = false;
    }
}

// =================================== NEST =================================== //

void CBlackBoard::updateDistNestVector(float distance, int robotID)
{
    distance = distance / 500;
    
    if (m_distNestVector.size() > 6)
    {
        m_distNestVector.erase(m_distNestVector.begin());
    }
    
    m_distNestVector.push_back(distance);
}

void CBlackBoard::setInitialDistanceFromNest(int robotID)
{
    m_initialDistanceFromNest = 0.0;
    for (float d : m_distNestVector)
    {
        m_initialDistanceFromNest += d;
    }
    m_initialDistanceFromNest /= m_distNestVector.size();

    //if (robotID != -1)
    //{
        //std::cout << "m_initialDistanceFromNest = " << m_initialDistanceFromNest << "\n";
    //}
}

void CBlackBoard::setDistNest(int robotID)
{
    float distance = 0.0;
    for (auto d : m_distNestVector)
    {
        distance += d;
    }
    distance /= m_distNestVector.size();
    
    m_distNest = distance;
}

float CBlackBoard::getDifferenceInDistanceFromNest()
{
    if (getFinalDistanceFromNest() == 0.0)
    {
        return 1.0;
    }
    else
    {
        float difference = getInitialDistanceFromNest() - getFinalDistanceFromNest();
        return (difference + 1) / 2;
    }
}

float CBlackBoard::getDifferenceInDistanceFromNestInverse()
{
    float difference = getFinalDistanceFromNest() - getInitialDistanceFromNest();
    return (difference + 1) / 2;
}

void CBlackBoard::setFinalDistanceFromNest(int robotID)
{
    float distance = 0.0;
    for (auto d : m_distNestVector)
    {
        distance += d;
    }
    distance /= m_distNestVector.size();
    m_finalDistanceFromNest = distance;

    //if (robotID != -1) std::cout << "m_finalDistanceFromNest = " << distance << "\n";
}


// =================================== FOOD =================================== //

void CBlackBoard::setDetectedFood(uint type, bool detected, int robotID)
{
    if (!detected)
    {
        m_detectedFood[type] = false;
    }
    else
    {
        m_detectedFood[type] = true;
        m_carryingFood[type] = true;
    }
}

void CBlackBoard::updateDistFoodVector(uint type, float distance, int robotID)
{
    distance = distance / 500;
    
    if (m_distFoodVectors[type].size() > 6)
    {
        m_distFoodVectors[type].erase(m_distFoodVectors[type].begin());
    }
    
    m_distFoodVectors[type].push_back(distance);
}

void CBlackBoard::setInitialDistanceFromFood(int robotID)
{
    float initialDistanceFromFood = 0.0;
    for (float d : m_distFoodVectors[0])
    {
        initialDistanceFromFood += d;
    }

    initialDistanceFromFood /= m_distFoodVectors[0].size();

    m_initialDistanceFromFood[0] = initialDistanceFromFood;

    //if (robotID != -1)
    //{
        //std::cout << "m_initialDistanceFromFood = " << m_initialDistanceFromFood[0] << "\n";
    //}
}

void CBlackBoard::setDistFood(uint type, int robotID)
{
    float distance = 0.0;
    for (auto d : m_distFoodVectors[type])
    {
        distance += d;
    }
    distance /= m_distFoodVectors[type].size();

    m_distFood[type] = distance;
}

float CBlackBoard::getDifferenceInDistanceFromFood()
{
    if (getFinalDistanceFromFood() == 0.0)
    {
        return 1.0;
    }
    else
    {
        float difference = getInitialDistanceFromFood() - getFinalDistanceFromFood();
        return (difference + 1) / 2;
    }
}

float CBlackBoard::getDifferenceInDistanceFromFoodInverse(int robotID)
{
    //if (robotID != -1) std::cout << "\tperceived difference\t" << getFinalDistanceFromFood() << " - " << getInitialDistanceFromFood() << "\n";
    float difference = getFinalDistanceFromFood() - getInitialDistanceFromFood();
    
    float result = (difference + 1) / 2;
    //if (robotID != -1) std::cout << "\tresult\t" << result << "\n";
    return (difference + 1) / 2;
}

void CBlackBoard::setFinalDistanceFromFood(int robotID)
{
    float distance = 0.0;
    for (auto d : m_distFoodVectors[0])
    {
        distance += d;
    }
    distance /= m_distFoodVectors[0].size();
    m_finalDistanceFromFood[0] = distance;

    //if (robotID != -1) std::cout << "m_finalDistanceFromFood = " << distance << "\n";
}


// =================================== DENSITY =================================== //

void CBlackBoard::updateDensityVector(float density, int robotID)
{
    // 1107 is the maximum density value that can be contributed by a single
    // robot and 6 is the number of robots that can fit around a single robot
    density = density / (1107 * 6);
    
    if (m_densityVector.size() == 6)
    {
        setInitialDensity();
    }
    
    if (m_densityVector.size() > 6)
    {
        m_densityVector.erase(m_densityVector.begin());
    }
    
    m_densityVector.push_back(density);    
    m_totalDensity += density;
}

float CBlackBoard::getAvgDensity(int count)
{
    return m_totalDensity / count;
}

void CBlackBoard::setInitialDensity(int robotID)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    //if (robotID != -1) std::cout << "m_initialDensity: " << density << std::endl;
    m_initialDensity = density;
}

void CBlackBoard::setFinalDensity(int robotID)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    m_finalDensity = density;
    m_densityVector.clear();

    //if (robotID != -1) std::cout << "m_finalDensity: " << density << std::endl;
}

float CBlackBoard::getDifferenceInDensity(int robotID)
{
    float difference = getFinalDensity() - getInitialDensity();
    return (difference + 1) / 2;
}

float CBlackBoard::getDifferenceInDensityInverse(int robotID)
{
    float difference = getInitialDensity() - getFinalDensity();
    return (difference + 1) / 2;
}

void CBlackBoard::setDensity(int robotID)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    
    m_density = density;
}

// =================================== NEIGHBOURS =================================== //

void CBlackBoard::setInitialNeighbourDistance(double distance, int robotID)
{
    m_nearestNeighbourStart = distance;
    
    //if (robotID != -1)
    //{
        //std::cout << std::to_string(robotID);
        //std::cout << " initial distance from robot = ";
        //std::cout << m_nearestNeighbourStart << "\n";
    //}
}

void CBlackBoard::accumulateNeighbourDistances(float distance, int robotID)
{
    //if (robotID != -1)
    //{
        //std::cout << std::to_string(robotID);
        //std::cout << " adding ";
        //std::cout << std::to_string(distance) << "\n";
    //}
    m_nearestNeighbourTotal += distance;
}

void CBlackBoard::setNeighbourDistanceAvg(int count, int robotID)
{
    // returns values between -1.0 and 1.0
    
    float nearestNeighbourAverage = m_nearestNeighbourTotal / count;
    float nearestNeighbourDelta = nearestNeighbourAverage - m_nearestNeighbourStart;
    float nearestNeighbourNormalised = nearestNeighbourDelta / 100;
    m_nearestNeighbourAverage = nearestNeighbourNormalised;
    
    //if (robotID != -1)
    //{
        //std::cout << "nearestNeighbourAverage = " << std::to_string(m_nearestNeighbourTotal) << " / " << std::to_string(count) << "\n";
        //std::cout << "nearestNeighbourDelta = " << std::to_string(nearestNeighbourAverage) << " - " << std::to_string(m_nearestNeighbourStart) << "\n";
        //std::cout << "nearestNeighbourNormalised = " << std::to_string(nearestNeighbourDelta) << " / 100\n\n";

        //std::cout << std::to_string(robotID);
        //std::cout << " avg to robot ";
        //std::cout << std::to_string(m_nearestNeighbourAverage) << "\n\n";
    //}
}


// =================================== QD =================================== //

void CBlackBoard::addMovement()
{
    if (m_motors == 1)
    {
        m_movement++;
    }
    if (m_motors == 4)
    {
        m_movement--;
    }
}

void CBlackBoard::addRotation()
{
    if (m_motors == 2 || m_motors == 6)
    {
        m_rotation++;
    }
    if (m_motors == 3 || m_motors == 5)
    {
        m_rotation--;
    }
}

float CBlackBoard::getConditionality()
{
    if (m_conditions > 0 || m_actions > 0)
    {
        float conditions = static_cast<float>(m_conditions);
        float actions = static_cast<float>(m_actions);
        return conditions / (conditions + actions);
    }
    return 1.0;
}


// =================================== USING ABSOLUTE POSITION =================================== //

void CBlackBoard::setInitialAbsolutePosition(float x, float y)
{
    //std::cout << "initial pos " << std::to_string(x) << " " << std::to_string(y) << "\n";
    m_initialAbsolutePosition = std::make_pair(x, y);
}

void CBlackBoard::setFinalAbsolutePosition(float x, float y)
{
    //std::cout << "final pos " << std::to_string(x) << " " << std::to_string(y) << "\n";
    m_finalAbsolutePosition = std::make_pair(x, y);
}

float CBlackBoard::getAbsoluteDelta()
{
    float x1 = m_initialAbsolutePosition.first;
    float y1 = m_initialAbsolutePosition.second;
    float x2 = m_finalAbsolutePosition.first;
    float y2 = m_finalAbsolutePosition.second;
    float squaredX = (x2 - x1) * (x2 - x1);
    float squaredY = (y2 - y1) * (y2 - y1);

    const float distance = sqrt(squaredX + squaredY);
    return distance;
}

// ======

void CBlackBoard::setInitialAbsoluteDistanceFromNest(double distance, int robotID)
{
    m_absoluteDistanceFromNestStart = distance;

    //if (robotID != -1)
    //{
        //std::cout << std::to_string(robotID);
        //std::cout << " initial distance from nest = ";
        //std::cout << m_absoluteDistanceFromNestStart << "\n";
    //}
}

void CBlackBoard::setFinalAbsoluteDistanceFromNest(double distance, int robotID)
{
    m_absoluteDistanceFromNestEnd = distance;
    //std::cout << "final distance from nest = ";
    //std::cout << m_absoluteDistanceFromNestEnd << "\n";
}

float CBlackBoard::getAbsoluteDifferenceInDistanceFromNest(int robotID)
{
    float distance = m_absoluteDistanceFromNestStart - m_absoluteDistanceFromNestEnd;
    //std::cout << "nest delta " << std::to_string(distance) << "\n";
    return distance;
}

float CBlackBoard::getAbsoluteDifferenceInDistanceFromNestInverse(int robotID)
{
    return m_absoluteDistanceFromNestEnd - m_absoluteDistanceFromNestStart;
}

void CBlackBoard::accumulateAbsoluteDistanceToNest(float distance)
{
    m_absoluteDistanceFromNestTotal += distance;
}

void CBlackBoard::setAbsoluteDistanceToNestAvg(int count, int robotID)
{
    float distanceToNestAverage = m_absoluteDistanceFromNestTotal / count;
    float distanceToNestDelta = distanceToNestAverage - m_absoluteDistanceFromNestStart;
    float distanceToNestNormalised = distanceToNestDelta * 2;
    m_absoluteDistanceFromNestAvg = distanceToNestNormalised;

    //if (robotID != -1)
    //{
        //std::cout << "distanceToNestAverage = " << std::to_string(m_absoluteDistanceFromNestTotal) << " / " << std::to_string(count) << "\n";
        //std::cout << "distanceToNestDelta = " << std::to_string(distanceToNestAverage) << " - " << std::to_string(m_absoluteDistanceFromNestStart) << "\n";
        //std::cout << "distanceToNestNormalised = " << std::to_string(distanceToNestDelta) << " * 2\n\n";

        //std::cout << std::to_string(robotID);
        //std::cout << " avg to nest ";
        //std::cout << std::to_string(m_absoluteDistanceFromNestAvg) << "\n";
    //}
}

// ======

float CBlackBoard::getAbsoluteDifferenceInDistanceFromFood(int robotID)
{
    float distance = m_absoluteDistanceFromFoodStart - m_absoluteDistanceFromFoodEnd;
    //std::cout << "food delta " << std::to_string(distance) << "\n";
    return distance;
}

float CBlackBoard::getAbsoluteDifferenceInDistanceFromFoodInverse(int robotID)
{
    float difference = m_absoluteDistanceFromFoodEnd - m_absoluteDistanceFromFoodStart;

    // from kilobots arena experiments, adds a 0.5 offset, giving 0.5 + (difference / 2r)
    //difference = difference + radius;
    //difference = difference / (radius * 2);

    // this should guarantee values between 0 and 1 because the maximum
    // distance a robot can travel in one 20s trial is 1m
    difference = (difference + 1) / 2;

    //if (robotID != -1) std::cout << "\tabsolute difference\t" << difference << "\n";

    return difference;
}

void CBlackBoard::setInitialAbsoluteDistanceFromFood(double distance, int robotID)
{
    m_absoluteDistanceFromFoodStart = distance;

    //if (robotID != -1)
    //{
        //std::cout << std::to_string(robotID);
        //std::cout << " initial distance from food = ";
        //std::cout << m_absoluteDistanceFromFoodStart << "\n";
    //}
}

void CBlackBoard::setFinalAbsoluteDistanceFromFood(double distance, int robotID)
{
    m_absoluteDistanceFromFoodEnd = distance;

    //if (robotID != -1)
    //{
        //std::cout << "final distance from food = ";
        //std::cout << m_finalAbsoluteDistanceFromFood << "\n";
    //}
}

void CBlackBoard::accumulateAbsoluteDistanceToFood(float distance, int robotID)
{
    m_absoluteDistanceFromFoodTotal += distance;

    //if (robotID != -1)
    //{
        //std::cout << std::to_string(robotID);
        //std::cout << " adding ";
        //std::cout << std::to_string(distance);
        //std::cout << " for ";
        //std::cout << std::to_string(m_absoluteDistanceFromFoodTotal) << "\n";
    //}
}

void CBlackBoard::setAbsoluteDistanceToFoodAvg(int count, int robotID)
{
    float distanceToFoodAverage = m_absoluteDistanceFromFoodTotal / count;
    float distanceToFoodDelta = distanceToFoodAverage - m_absoluteDistanceFromFoodStart;
    float distanceToFoodNormalised = distanceToFoodDelta * 2;
    m_absoluteDistanceFromFoodAvg = distanceToFoodNormalised;

    //if (robotID != -1)
    //{
        //std::cout << "distanceToFoodAverage = " << std::to_string(m_absoluteDistanceFromFoodTotal) << " / " << std::to_string(count) << "\n";
        //std::cout << "distanceToFoodDelta = " << std::to_string(distanceToFoodAverage) << " - " << std::to_string(m_absoluteDistanceFromFoodStart) << "\n";
        //std::cout << "distanceToFoodNormalised = " << std::to_string(distanceToFoodDelta) << " * 2\n";

        //std::cout << std::to_string(robotID);
        //std::cout << " avg to food ";
        //std::cout << std::to_string(m_absoluteDistanceFromFoodAvg) << "\n\n";
    //}
}


// =================================== multi-food foraging =================================== //

void CBlackBoard::incrementFood(uint type, int robotID)
{
    //if (robotID != -1) std::cout << "incrementing food " << std::to_string(type) << "\n";
    m_food[type] += 1;
}

uint CBlackBoard::getFoodOfType(uint type)
{
    return m_food[type];
}

uint CBlackBoard::getTotalFood()
{
    uint totalFood = 0;
    for (const auto& food : m_food)
    {
        totalFood += food;
    }
    return totalFood;
}
