#include "CBlackBoard.h"


void CBlackBoard::reset()
{
    m_distNestVector.clear();

    for (uint i = 0; i < 1; ++i)
    {
        m_food[i] = 0;
        m_distFoodVectors[i].clear();
        m_carryingFood[i] = false;
    }
}

// =================================== NEST =================================== //

void CBlackBoard::updateDistNestVector(float distance, bool tracking)
{
    distance = distance / 500;
    
    if (m_distNestVector.size() > 6)
    {
        m_distNestVector.erase(m_distNestVector.begin());
    }
    
    m_distNestVector.push_back(distance);
}

void CBlackBoard::setInitialDistanceFromNest(bool tracking)
{
    m_initialDistanceFromNest = 0.0;
    for (float d : m_distNestVector)
    {
        m_initialDistanceFromNest += d;
    }
    m_initialDistanceFromNest /= m_distNestVector.size();

    //if (tracking)
    //{
        //std::cout << "m_initialDistanceFromNest = " << m_initialDistanceFromNest << "\n";
    //}
}

void CBlackBoard::setDistNest(bool tracking)
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

void CBlackBoard::setFinalDistanceFromNest(bool tracking)
{
    float distance = 0.0;
    for (auto d : m_distNestVector)
    {
        distance += d;
    }
    distance /= m_distNestVector.size();
    m_finalDistanceFromNest = distance;

    //if (tracking) std::cout << "m_finalDistanceFromNest = " << distance << "\n";
}


// =================================== FOOD =================================== //

void CBlackBoard::setDetectedFood(uint type, bool detected, bool tracking)
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

void CBlackBoard::updateDistFoodVector(uint type, float distance, bool tracking)
{
    distance = distance / 500;
    
    if (m_distFoodVectors[type].size() > 6)
    {
        m_distFoodVectors[type].erase(m_distFoodVectors[type].begin());
    }
    
    m_distFoodVectors[type].push_back(distance);
}

void CBlackBoard::setInitialDistanceFromFood(bool tracking)
{
    float initialDistanceFromFood = 0.0;
    for (float d : m_distFoodVectors[0])
    {
        initialDistanceFromFood += d;
    }

    initialDistanceFromFood /= m_distFoodVectors[0].size();

    m_initialDistanceFromFood[0] = initialDistanceFromFood;

    //if (tracking) std::cout << "m_initialDistanceFromFood = " << m_initialDistanceFromFood[0] << std::endl;
}

void CBlackBoard::setDistFood(uint type, bool tracking)
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

float CBlackBoard::getDifferenceInDistanceFromFoodInverse(bool tracking)
{
    //if (tracking) std::cout << "\tperceived difference\t" << getFinalDistanceFromFood() << " - " << getInitialDistanceFromFood() << "\n";
    float difference = getFinalDistanceFromFood() - getInitialDistanceFromFood();
    
    float result = (difference + 1) / 2;
    //if (tracking) std::cout << "\tresult\t" << result << "\n";
    return (difference + 1) / 2;
}

void CBlackBoard::setFinalDistanceFromFood(bool tracking)
{
    float distance = 0.0;
    for (auto d : m_distFoodVectors[0])
    {
        distance += d;
    }
    distance /= m_distFoodVectors[0].size();
    m_finalDistanceFromFood[0] = distance;

    //if (tracking) std::cout << "m_finalDistanceFromFood = " << distance << "\n";
}


// =================================== DENSITY =================================== //

void CBlackBoard::updateDensityVector(float density, bool tracking)
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

void CBlackBoard::setInitialDensity(bool tracking)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    //if (tracking) std::cout << "m_initialDensity: " << density << std::endl;
    m_initialDensity = density;
}

void CBlackBoard::setFinalDensity(bool tracking)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    m_finalDensity = density;
    m_densityVector.clear();

    //if (tracking) std::cout << "m_finalDensity: " << density << std::endl;
}

float CBlackBoard::getDifferenceInDensity(bool tracking)
{
    float difference = getFinalDensity() - getInitialDensity();
    return (difference + 1) / 2;
}

float CBlackBoard::getDifferenceInDensityInverse(bool tracking)
{
    float difference = getInitialDensity() - getFinalDensity();
    return (difference + 1) / 2;
}

void CBlackBoard::setDensity(bool tracking)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    
    m_density = density;
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

float CBlackBoard::getAbsoluteDifferenceInDistanceFromFoodInverse(bool tracking)
{
    float difference = m_absoluteDistanceFromFoodEnd - m_absoluteDistanceFromFoodStart;

    // from kilobots arena experiments, adds a 0.5 offset, giving 0.5 + (difference / 2r)
    //difference = difference + radius;
    //difference = difference / (radius * 2);

    // this should guarantee values between 0 and 1 because the maximum
    // distance a robot can travel in one 20s trial is 1m
    difference = (difference + 1) / 2;

    //if (tracking) std::cout << "\tabsolute difference\t" << difference << "\n";

    return difference;
}

void CBlackBoard::setInitialAbsoluteDistanceFromFood(double distance, bool tracking)
{
    m_absoluteDistanceFromFoodStart = distance;

    //if (tracking)
    //{
        //std::cout << m_robotId;
        //std::cout << " initial distance from food = ";
        //std::cout << m_absoluteDistanceFromFoodStart << "\n";
    //}
}

void CBlackBoard::setFinalAbsoluteDistanceFromFood(double distance, bool tracking)
{
    m_absoluteDistanceFromFoodEnd = distance;

    //if (tracking)
    //{
        //std::cout << "final distance from food = ";
        //std::cout << m_absoluteDistanceFromFoodEnd << "\n";
    //}
}

// =================================== multi-food foraging =================================== //

void CBlackBoard::incrementFood(uint type, bool tracking)
{
    //if (tracking) std::cout << "incrementing food " << std::to_string(type) << "\n";
    m_food[type] += 1;
}

uint CBlackBoard::getFoodOfType(uint type)
{
    return m_food[type];
}
