#ifndef CBLACKBOARD_H
#define CBLACKBOARD_H

#include <vector>
#include <iostream>
#include <math.h>

class CBlackBoard
{
    public:
        CBlackBoard(int numRobots) : 
            m_motors(0),
            
            // nest
            m_distNest(0),
            m_initialDistanceFromNest(-1.0),
            m_finalDistanceFromNest(-1.0),
            m_timeInNest(0),
            m_distNestChange(0),
            m_firstEnteredNest(-1),
            m_inNest(false),
            
            // food
            m_distFood(1),
            m_initialDistanceFromFood(-1.0),
            m_initialAbsoluteDistanceFromFood(-1.0),
            m_finalDistanceFromFood(-1.0),
            m_finalAbsoluteDistanceFromFood(-1.0),
            m_distFoodChange(0),
            m_firstDetectedFood(-1),
            m_detectedFood(false), 
            m_carryingFood(false),
            
            // density
            m_density(0),
            m_densityChange(0),
            m_totalDensity(0.0),
            m_firstDensityChange(-1),
            m_initialDensity(0.0),
            m_totalDistanceNearestRobot(0.0),
            m_initialNumRobots(-1),
            
            // navigation
            m_nestToLeft(false),
            m_nestToRight(false),
            m_foodToLeft(false),
            m_foodToRight(false),
            m_objectAhead(false),
            m_objectToLeft(false),
            m_objectToRight(false),
            
            // collisions
            m_collisions(0),
            m_movement(0),
            m_rotation(0),
            m_conditions(0),
            m_actions(0)
        {}
        
        int getMotors() {return m_motors;}
        void setMotors(int motors) {m_motors = motors;}
        
        // food
        
        bool getCarryingFood() {return m_carryingFood;}
        void setCarryingFood(bool carryingFood) {m_carryingFood = carryingFood;}
        
        bool getDetectedFood() {return m_detectedFood;}
        void setDetectedFood(int count, bool detected, int robotID = -1);
        float getFirstDetectedFood();
        
        float getDistFood() {return m_distFood;}
        float getFoodChange() {return m_distFoodChange;}
        void updateDistFoodVector(float distance, int robotID = -1);
        void setDistFood(bool first = false, int robotID = -1);
        
        float getInitialDistanceFromFood() {return m_initialDistanceFromFood;}
        void setInitialDistanceFromFood(int robotID);
        void setInitialAbsoluteDistanceFromFood(double distance, int robotID);
        float getFinalDistanceFromFood() {return m_finalDistanceFromFood;}
        float getDifferenceInDistanceFromFood();
        float getDifferenceInDistanceFromFoodInverse(int robotID);
        float getAbsoluteDifferenceInDistanceFromFoodInverse(float radius, int robotID);
        void setFinalDistanceFromFood(int robotID);
        void setFinalAbsoluteDistanceFromFood(double distance, int robotID);
        
        // nest
        
        bool getInNest() {return m_inNest;}
        void setInNest(int count, bool nest, int robotID = -1);

        float getFirstEnteredNest();
        void incrementTimeInNest(bool inNest) {m_timeInNest += (inNest) ? 1 : 0;}
        int getTimeInNest() {return m_timeInNest;}
        
        float getDistNest() {return m_distNest;}
        float getNestChange() {return m_distNestChange;}
        void updateDistNestVector(float distance, int robotID);
        void setDistNest(bool first = false, int robotID = -1);
        
        float getInitialDistanceFromNest() {return m_initialDistanceFromNest;}
        void setInitialDistanceFromNest(int robotID);
        float getFinalDistanceFromNest() {return m_finalDistanceFromNest;}
        float getDifferenceInDistanceFromNest();
        float getDifferenceInDistanceFromNestInverse();
        void setFinalDistanceFromNest(int robotID);
        
        // density
        
        float getDensity() {return m_density;}
        float getDensityChange() {return m_densityChange;}
        float getAvgDensity(int count);
        void updateDensityVector(float density, int robotID = -1);
        void setDensity(bool first = false, int robotID = -1);
        
        void setInitialDensity(int robotID = -1);
        float getInitialDensity() {return m_initialDensity;}
        void setFinalDensity(int robotID = -1);
        float getFinalDensity() {return m_finalDensity;}
        float getDifferenceInDensity(int robotID = -1);
        float getDifferenceInDensityInverse(int robotID = -1);
        void setFirstDensityChange(int count);
        int getFirstDensityChange() {return m_firstDensityChange;}
        
        float getAvgDistanceNearestRobot();
        float getStdDevDistanceNearestRobot();
        void saveDistanceNearestRobot(float distance, int robotID);
        
        int getInitialNumRobots() {return m_initialNumRobots;}
        int getFinalNumRobots() {return m_totalNumNeighbours.back();}
        float getAvgNumNeighbours();
        float getStdDevNumNeighbours();
        void saveNumNeighbours(int neighbours, int robotID);
        
        // navigation
        
        bool getNestToLeft() {return m_nestToLeft;}
        bool getNestToRight() {return m_nestToRight;}
        bool getFoodToLeft() {return m_foodToLeft;}
        bool getFoodToRight() {return m_foodToRight;}
        
        void setNestToLeft(bool isLeft) {m_nestToLeft = isLeft;}
        void setNestToRight(bool isRight) {m_nestToRight = isRight;}
        void setFoodToLeft(bool isLeft) {m_foodToLeft = isLeft;}
        void setFoodToRight(bool isRight) {m_foodToRight = isRight;}
        
        bool getObjectAhead() {return m_objectAhead;}
        bool getObjectToLeft() {return m_objectToLeft;}
        bool getObjectToRight() {return m_objectToRight;}
        
        void setObjectAhead(bool object) {m_objectAhead = object;}
        void setObjectToLeft(bool object) {m_objectToLeft = object;}
        void setObjectToRight(bool object) {m_objectToRight = object;}
        
        bool getNearestNeighbourToLeft() {return m_nearestNeighbourToLeft;}
        bool getNearestNeighbourToRight() {return m_nearestNeighbourToRight;}
        
        void setNearestNeighbourToLeft(bool robot) {m_nearestNeighbourToLeft = robot;}
        void setNearestNeighbourToRight(bool robot) {m_nearestNeighbourToRight = robot;}
        
        // collisions
        
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
        
    private:
    
        int m_motors;
        
        // food
        bool m_detectedFood;
        int m_firstDetectedFood;
        bool m_carryingFood;
        
        float m_distFood;
        float m_distFoodChange;
        std::vector<float> m_distFoodVector;
        
        float m_initialDistanceFromFood;
        float m_initialAbsoluteDistanceFromFood;
        float m_finalDistanceFromFood;
        float m_finalAbsoluteDistanceFromFood;
        
        // nest
        
        float m_distNest;
        float m_distNestChange;
        std::vector<float> m_distNestVector;
        
        float m_initialDistanceFromNest;
        float m_finalDistanceFromNest;
        
        bool m_inNest;
        int m_firstEnteredNest;
        int m_timeInNest;
        
        // density
        
        float m_density;
        
        float m_densityChange;
        std::vector<float> m_densityVector;
        float m_totalDensity;
        
        int m_firstDensityChange;
        float m_initialDensity;
        float m_finalDensity;
        int m_initialNumRobots;
        
        std::vector<int> m_totalNumNeighbours;
        std::vector<float> m_totalDistanceNearestRobot;
        
        // navigation
        
        bool m_nestToLeft;
        bool m_nestToRight;
        bool m_foodToLeft;
        bool m_foodToRight;
        
        bool m_objectAhead;
        bool m_objectToLeft;
        bool m_objectToRight;
        
        bool m_nearestNeighbourToLeft;
        bool m_nearestNeighbourToRight;
        
        // collisions
        
        int m_collisions;
        
        // qd
        
        int m_movement;
        int m_rotation;
        int m_conditions;
        int m_actions;
};

#endif
