#ifndef CBLACKBOARD_H
#define CBLACKBOARD_H

#include <vector>
#include <iostream>
#include <math.h>

class CBlackBoard
{
    public:
        CBlackBoard(int robotId) :
            m_robotId(robotId),
            m_motors(0),
            
            // nest
            m_distNest(0.0),
            m_initialDistanceFromNest(-1.0),
            m_finalDistanceFromNest(-1.0),
            m_inNest(false),
            m_nestToLeft(false),
            m_nestToRight(false),

            // density
            m_density(0.0),
            m_totalDensity(0.0),
            m_initialDensity(0.0),
            
            // qd
            m_movement(0),
            m_rotation(0),
            m_conditions(0),
            m_actions(0),

            // absolute position
            m_absoluteDistanceFromFoodStart(0.0),
            m_absoluteDistanceFromFoodEnd(0.0)
        {
            for (uint i = 0; i < 1; ++i)
            {
                m_food.push_back(0);

                m_detectedFood.push_back(false);
                m_carryingFood.push_back(false);
                m_foodToLeft.push_back(false);
                m_foodToRight.push_back(false);

                m_distFood.push_back(0.0);
                m_distFoodVectors.push_back(std::vector<float>());
                m_initialDistanceFromFood.push_back(0.0);
                m_finalDistanceFromFood.push_back(0.0);
            }
        }

        void reset();

        int getMotors() {return m_motors;}
        void setMotors(int motors) {m_motors = motors;}
        
        // food

        bool getCarryingFood(uint type) {return m_carryingFood[type];}
        void setCarryingFood(uint type, bool carryingFood) {m_carryingFood[type] = carryingFood;}

        bool getDetectedFood(uint type) {return m_detectedFood[type];}
        void setDetectedFood(uint type, bool detected, bool tracking = false);

        void updateDistFoodVector(uint type, float distance, bool tracking = false);
        float getDistFood(uint type) {return m_distFood[type];}
        void setDistFood(uint type, bool tracking = false);

        float getInitialDistanceFromFood() {return m_initialDistanceFromFood[0];}
        void setInitialDistanceFromFood(bool tracking = false);

        float getFinalDistanceFromFood() {return m_finalDistanceFromFood[0];}
        void setFinalDistanceFromFood(bool tracking = false);

        float getDifferenceInDistanceFromFood();
        float getDifferenceInDistanceFromFoodInverse(bool tracking = false);

        bool getFoodToLeft(uint type) {return m_foodToLeft[type];}
        bool getFoodToRight(uint type) {return m_foodToRight[type];}
        void setFoodToLeft(uint type, bool isLeft) {m_foodToLeft[type] = isLeft;}
        void setFoodToRight(uint type, bool isRight) {m_foodToRight[type] = isRight;}

        // nest

        bool getInNest() {return m_inNest;}
        void setInNest(bool nest) {m_inNest = nest;}

        void updateDistNestVector(float distance, bool tracking = false);
        float getDistNest() {return m_distNest;}
        void setDistNest(bool tracking = false);

        float getInitialDistanceFromNest() {return m_initialDistanceFromNest;}
        void setInitialDistanceFromNest(bool tracking = false);

        float getFinalDistanceFromNest() {return m_finalDistanceFromNest;}
        void setFinalDistanceFromNest(bool tracking = false);

        float getDifferenceInDistanceFromNest();
        float getDifferenceInDistanceFromNestInverse();

        bool getNestToLeft() {return m_nestToLeft;}
        bool getNestToRight() {return m_nestToRight;}
        void setNestToLeft(bool isLeft) {m_nestToLeft = isLeft;}
        void setNestToRight(bool isRight) {m_nestToRight = isRight;}

        // density

        float getDensity() {return m_density;}
        float getAvgDensity(int count);
        void updateDensityVector(float density, bool tracking = false);
        void setDensity(bool tracking = false);

        void setInitialDensity(bool tracking = false);
        float getInitialDensity() {return m_initialDensity;}
        void setFinalDensity(bool tracking = false);
        float getFinalDensity() {return m_finalDensity;}
        float getDifferenceInDensity(bool tracking = false);
        float getDifferenceInDensityInverse(bool tracking = false);

        // neighbours

        bool getNearestNeighbourToLeft() {return m_nearestNeighbourToLeft;}
        bool getNearestNeighbourToRight() {return m_nearestNeighbourToRight;}
        void setNearestNeighbourToLeft(bool robot) {m_nearestNeighbourToLeft = robot;}
        void setNearestNeighbourToRight(bool robot) {m_nearestNeighbourToRight = robot;}

        // qd

        void addMovement();
        void setMovement(uint movement) {m_movement = movement;}
        int getMovement() {return m_movement;}

        void addRotation();
        void setRotations(uint rotations) {m_rotation = rotations;}
        int getRotations() {return m_rotation;}

        void addCondition() {m_conditions++;}
        void setConditions(int conditions) {m_conditions = conditions;}
        int getConditions() {return m_conditions;}

        void addAction() {m_actions++;}
        void setActions(int actions) {m_actions = actions;}
        int getActions() {return m_actions;}

        float getConditionality();


        // absolute position

        void setInitialAbsoluteDistanceFromFood(double distance, bool tracking = false);
        float getAbsoluteDifferenceInDistanceFromFoodInverse(bool tracking = false);
        void setFinalAbsoluteDistanceFromFood(double distance, bool tracking = false);

        // multi-food foraging

        void incrementFood(uint type, bool tracking = false);
        uint getFoodOfType(uint type);

    private:

        int m_robotId;
        int m_motors;

        // food

        std::vector<bool> m_detectedFood;
        std::vector<bool> m_carryingFood;
        std::vector<bool> m_foodToLeft;
        std::vector<bool> m_foodToRight;

        std::vector<float> m_distFood;
        std::vector<std::vector<float>> m_distFoodVectors;

        std::vector<float> m_initialDistanceFromFood;
        std::vector<float> m_finalDistanceFromFood;

        // nest

        bool m_inNest;
        bool m_nestToLeft;
        bool m_nestToRight;

        float m_distNest;
        std::vector<float> m_distNestVector;

        float m_initialDistanceFromNest;
        float m_finalDistanceFromNest;

        // density

        float m_density;

        std::vector<float> m_densityVector;
        float m_totalDensity;

        float m_initialDensity;
        float m_finalDensity;

        // neighbours

        bool m_nearestNeighbourToLeft;
        bool m_nearestNeighbourToRight;

        // qd

        int m_movement;
        int m_rotation;
        int m_conditions;
        int m_actions;

        // absolute position

        float m_absoluteDistanceFromFoodStart;
        float m_absoluteDistanceFromFoodEnd;

        // multi-food foraging

        std::vector<uint> m_food;
};

#endif
