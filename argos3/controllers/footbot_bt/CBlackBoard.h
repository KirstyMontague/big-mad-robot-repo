#ifndef CBLACKBOARD_H
#define CBLACKBOARD_H

#include <vector>
#include <iostream>
#include <math.h>

class CBlackBoard
{
    public:
        CBlackBoard() :
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

            // neighbours
            m_nearestNeighbourStart(0.0),
            m_nearestNeighbourTotal(0.0),
            m_nearestNeighbourAverage(0.0),

            // proximity detection
            m_objectAhead(false),
            m_objectToLeft(false),
            m_objectToRight(false),
            m_collisions(0),

            // qd
            m_movement(0),
            m_rotation(0),
            m_conditions(0),
            m_actions(0),

            // absolute position
            m_absoluteDistanceFromNestStart(0.0),
            m_absoluteDistanceFromNestEnd(0.0),
            m_absoluteDistanceFromNestAvg(0.0),
            m_absoluteDistanceFromNestTotal(0.0),
            m_absoluteDistanceFromFoodStart(0.0),
            m_absoluteDistanceFromFoodEnd(0.0),
            m_absoluteDistanceFromFoodAvg(0.0),
            m_absoluteDistanceFromFoodTotal(0.0)
        {
            for (uint i = 0; i < 3; ++i)
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
        void setDetectedFood(uint type, bool detected, int robotID = -1);

        void updateDistFoodVector(uint type, float distance, int robotID = -1);
        float getDistFood(uint type) {return m_distFood[type];}
        void setDistFood(uint type, int robotID);

        float getInitialDistanceFromFood() {return m_initialDistanceFromFood[0];}
        void setInitialDistanceFromFood(int robotID);

        float getFinalDistanceFromFood() {return m_finalDistanceFromFood[0];}
        void setFinalDistanceFromFood(int robotID);

        float getDifferenceInDistanceFromFood();
        float getDifferenceInDistanceFromFoodInverse(int robotID);

        bool getFoodToLeft(uint type) {return m_foodToLeft[type];}
        bool getFoodToRight(uint type) {return m_foodToRight[type];}
        void setFoodToLeft(uint type, bool isLeft) {m_foodToLeft[type] = isLeft;}
        void setFoodToRight(uint type, bool isRight) {m_foodToRight[type] = isRight;}

        // nest

        bool getInNest() {return m_inNest;}
        void setInNest(bool nest) {m_inNest = nest;}

        void updateDistNestVector(float distance, int robotID);
        float getDistNest() {return m_distNest;}
        void setDistNest(int robotID);

        float getInitialDistanceFromNest() {return m_initialDistanceFromNest;}
        void setInitialDistanceFromNest(int robotID);

        float getFinalDistanceFromNest() {return m_finalDistanceFromNest;}
        void setFinalDistanceFromNest(int robotID);

        float getDifferenceInDistanceFromNest();
        float getDifferenceInDistanceFromNestInverse();

        bool getNestToLeft() {return m_nestToLeft;}
        bool getNestToRight() {return m_nestToRight;}
        void setNestToLeft(bool isLeft) {m_nestToLeft = isLeft;}
        void setNestToRight(bool isRight) {m_nestToRight = isRight;}

        // density

        float getDensity() {return m_density;}
        float getAvgDensity(int count);
        void updateDensityVector(float density, int robotID = -1);
        void setDensity(int robotID);

        void setInitialDensity(int robotID = -1);
        float getInitialDensity() {return m_initialDensity;}
        void setFinalDensity(int robotID = -1);
        float getFinalDensity() {return m_finalDensity;}
        float getDifferenceInDensity(int robotID = -1);
        float getDifferenceInDensityInverse(int robotID = -1);

        // neighbours

        void setInitialNeighbourDistance(double distance, int robotID);
        void accumulateNeighbourDistances(float distance, int robotID);
        float getNeighbourDistanceAvg() {return m_nearestNeighbourAverage;}
        void setNeighbourDistanceAvg(int count, int robotID);

        bool getNearestNeighbourToLeft() {return m_nearestNeighbourToLeft;}
        bool getNearestNeighbourToRight() {return m_nearestNeighbourToRight;}
        void setNearestNeighbourToLeft(bool robot) {m_nearestNeighbourToLeft = robot;}
        void setNearestNeighbourToRight(bool robot) {m_nearestNeighbourToRight = robot;}

        // proximity detection

        bool getObjectAhead() {return m_objectAhead;}
        bool getObjectToLeft() {return m_objectToLeft;}
        bool getObjectToRight() {return m_objectToRight;}

        void setObjectAhead(bool object) {m_objectAhead = object;}
        void setObjectToLeft(bool object) {m_objectToLeft = object;}
        void setObjectToRight(bool object) {m_objectToRight = object;}

        void addCollision() {m_collisions++;}
        void setCollisions(uint collisions) {m_collisions = collisions;}
        int getCollisions() {return m_collisions;}

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

        void setInitialAbsolutePosition(float x, float y);
        void setFinalAbsolutePosition(float x, float y);
        float getAbsoluteDelta();

        void setInitialAbsoluteDistanceFromFood(double distance, int robotID);
        float getAbsoluteDifferenceInDistanceFromFood(int robotID);
        float getAbsoluteDifferenceInDistanceFromFoodInverse(int robotID);
        void setFinalAbsoluteDistanceFromFood(double distance, int robotID);

        void accumulateAbsoluteDistanceToFood(float distance, int robotID);
        float getAbsoluteDistanceToFoodAvg() {return m_absoluteDistanceFromFoodAvg;}
        void setAbsoluteDistanceToFoodAvg(int count, int robotID);

        float getAbsoluteDifferenceInDistanceFromNest(int robotID);
        float getAbsoluteDifferenceInDistanceFromNestInverse(int robotID);
        void setInitialAbsoluteDistanceFromNest(double distance, int robotID);
        void setFinalAbsoluteDistanceFromNest(double distance, int robotID);

        void accumulateAbsoluteDistanceToNest(float distance);
        float getAbsoluteDistanceToNestAvg() {return m_absoluteDistanceFromNestAvg;}
        void setAbsoluteDistanceToNestAvg(int count, int robotID);

        // multi-food foraging

        void incrementFood(uint type, int robotID);
        uint getFoodOfType(uint type);
        uint getTotalFood();

    private:

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
        float m_nearestNeighbourStart;
        float m_nearestNeighbourTotal;
        float m_nearestNeighbourAverage;

        // proximity detection

        bool m_objectAhead;
        bool m_objectToLeft;
        bool m_objectToRight;
        int m_collisions;

        // qd

        int m_movement;
        int m_rotation;
        int m_conditions;
        int m_actions;

        // absolute position

        std::pair<float, float> m_initialAbsolutePosition;
        std::pair<float, float> m_finalAbsolutePosition;

        float m_absoluteDistanceFromFoodStart;
        float m_absoluteDistanceFromFoodEnd;
        float m_absoluteDistanceFromFoodAvg;
        float m_absoluteDistanceFromFoodTotal;

        float m_absoluteDistanceFromNestTotal;
        float m_absoluteDistanceFromNestStart;
        float m_absoluteDistanceFromNestEnd;
        float m_absoluteDistanceFromNestAvg;

        // multi-food foraging

        std::vector<uint> m_food;
};

#endif
