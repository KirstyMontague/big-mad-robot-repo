#include "CBlackBoard.h"


// =================================== NEST =================================== //

void CBlackBoard::setInNest(int count, bool nest, int robotID)
{
    if (!nest)
    {
        m_inNest = false;
    }
    
    else
    {
        if (!m_inNest && m_firstEnteredNest == -1 && count > 2)
        {
            m_firstEnteredNest = count;
            if (robotID != -1) std::cout << "m_firstEnteredNest = " << std::to_string(count) << std::endl;
        }
        
        m_inNest = true;
        
    }
}

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
    m_initialDistanceFromNest /= 7;
    if (robotID != -1) std::cout << "m_initialDistanceFromNest = " << m_initialDistanceFromNest << "\n";
}

void CBlackBoard::setDistNest(bool first, int robotID)
{
    //if (robotID != -1) std::cout << "nest ";
    
    float distance = 0.0;
    for (auto d : m_distNestVector)
    {
        distance += d;
        //if (robotID != -1) std::cout << d << " ";
    }
    distance /= m_distNestVector.size();
    //if (robotID != -1) std::cout << " | " << distance;
    
    if (!first) m_distNestChange = distance - m_distNest;
    //if (robotID != -1) std::cout << " | " << m_distNestChange;
    
    //if (robotID != -1) std::cout << std::endl;
    
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
        //if (robotID != -1) std::cout << d << " ";
    }
    distance /= m_distNestVector.size();
    m_finalDistanceFromNest = distance;
    if (robotID != -1) std::cout << "m_finalDistanceFromNest = " << distance << "\n";
}




// =================================== FOOD =================================== //

void CBlackBoard::setDetectedFood(int count, bool detected, int robotID)
{
    if (!detected)
    {
        m_detectedFood = false;
    }
    else
    {
        if (!m_detectedFood && m_firstDetectedFood == -1 && count > 2)
        {
            m_firstDetectedFood = count;
            if (robotID != -1) std::cout << "m_firstDetectedFood = " << std::to_string(count) << std::endl;
        }
        
        m_detectedFood = true;
        
        if (!m_carryingFood)
        {
            m_carryingFood = true;
        }
    }
}

void CBlackBoard::updateDistFoodVector(float distance, int robotID)
{
    distance = distance / 500;
    
    if (m_distFoodVector.size() > 6)
    {
        m_distFoodVector.erase(m_distFoodVector.begin());
    }
    
    m_distFoodVector.push_back(distance);
}

void CBlackBoard::setInitialDistanceFromFood(int robotID)
{
    m_initialDistanceFromFood = 0.0;
    for (float d : m_distFoodVector)
    {
        m_initialDistanceFromFood += d;
    }
    m_initialDistanceFromFood /= 7;
    if (robotID != -1) std::cout << "m_initialDistanceFromFood = " << m_initialDistanceFromFood << std::endl;
}

void CBlackBoard::setInitialAbsoluteDistanceFromFood(double radius, double threshold, int robotID)
{
    if (radius >= threshold)
    {
        m_initialAbsoluteDistanceFromFood = 0.0;
    }
    else
    {
        m_initialAbsoluteDistanceFromFood = threshold - radius;
    }
    if (robotID != -1) 
    {
        std::cout << "m_initialAbsoluteDistanceFromFood = ";
        std::cout << threshold << " - " << radius << " = ";
        std::cout << m_initialAbsoluteDistanceFromFood << "\n";
    }
}

void CBlackBoard::setDistFood(bool first, int robotID)
{
    //if (robotID != -1) std::cout << "food ";
    
    float distance = 0.0;
    for (auto d : m_distFoodVector)
    {
        distance += d;
        //if (robotID != -1) std::cout << d << " ";
    }
    distance /= m_distFoodVector.size();
    //if (robotID != -1) std::cout << " | " << distance;
    
    if (!first) m_distFoodChange = distance - m_distFood;
    //if (robotID != -1) std::cout << " | " << m_distFoodChange;
    
    //if (robotID != -1) std::cout << std::endl;
    
    m_distFood = distance;
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
    if (robotID != -1) std::cout << "\t" << getFinalDistanceFromFood() << " - " << getInitialDistanceFromFood() << "\n";
    float difference = getFinalDistanceFromFood() - getInitialDistanceFromFood();
    
    float result = (difference + 1) / 2;
    if (robotID != -1) std::cout << "\t" << result << "\n";
    return (difference + 1) / 2;
}

float CBlackBoard::getAbsoluteDifferenceInDistanceFromFoodInverse(float radius, int robotID)
{
    if (robotID != -1) std::cout << "\t" << m_finalAbsoluteDistanceFromFood << " - " << m_initialAbsoluteDistanceFromFood << "\n";
    float difference = m_finalAbsoluteDistanceFromFood - m_initialAbsoluteDistanceFromFood;
    
    float max = radius;
    float min = radius * -1;
    difference = difference - min;
    difference = difference / (max * 2);
    float result = difference;

    if (robotID != -1) std::cout << "\t" << result << "\n";

    return result;
}

void CBlackBoard::setFinalDistanceFromFood(int robotID)
{
    float distance = 0.0;
    for (auto d : m_distFoodVector)
    {
        distance += d;
        //if (robotID != -1) std::cout << d << " ";
    }
    distance /= m_distFoodVector.size();
    m_finalDistanceFromFood = distance;
    if (robotID != -1) std::cout << "m_finalDistanceFromFood = " << distance << "\n";
}

void CBlackBoard::setFinalAbsoluteDistanceFromFood(double radius, double threshold, int robotID)
{
    if (radius >= threshold)
    {
        m_finalAbsoluteDistanceFromFood = 0.0;
    }
    else
    {
        m_finalAbsoluteDistanceFromFood = threshold - radius;
    }
    if (robotID != -1) 
    {
        std::cout << "m_finalAbsoluteDistanceFromFood = ";
        std::cout << threshold << " - " << radius << " = ";
        std::cout << m_finalAbsoluteDistanceFromFood << "\n";
    }
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
    //if (robotID != -1) std::cout << density << std::endl;
    
}

void CBlackBoard::setInitialDensity(int robotID)
{
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
    }
    density /= m_densityVector.size();
    if (robotID != -1) std::cout << "m_initialDensity: " << density << std::endl;
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
    if (robotID != -1) std::cout << "m_finalDensity: " << density << std::endl;
    m_finalDensity = density;
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

void CBlackBoard::setDensity(bool first, int robotID)
{
    //if (robotID != -1) std::cout << "density ";
    
    float density = 0;
    for (auto d : m_densityVector)
    {
        density += d;
        //if (robotID != -1) std::cout << d << " ";
    }
    density /= m_densityVector.size();
    //if (robotID != -1) std::cout << " | " << density;
    
    if (!first) m_densityChange = density - m_density;
    //if (robotID != -1) std::cout << " | " << m_densityChange << std::endl;
    
    m_density = density;
}

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
