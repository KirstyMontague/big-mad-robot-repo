#ifndef PERCEPTRON_MULTI_H
#define PERCEPTRON_MULTI_H

#include "neural_network.h"

class CPerceptronMulti : public CNeuralNetwork {

public:

    CPerceptronMulti();
    virtual ~CPerceptronMulti();

    void Init(TConfigurationNode& t_tree, UInt32 numInputs, UInt32 numHidden, UInt32 numOutputs);
    void Load(const Real* chromosome, bool tracking);
    virtual void Destroy();

    virtual void LoadNetworkParameters(const Real* chromosome, bool tracking);
    virtual void ComputeOutputs(bool tracking);

private:

    Real sigmoid(Real value);

    UInt32   m_unNumberOfWeights;
    Real*    m_pfWeights;
    Real     m_weight;

    Real* m_pfInputToHiddenWeights;
    Real* m_pfHiddenToOutputWeights;

    Real* m_pfHiddenBiases;
    Real* m_pfHiddenTaus;
    Real* m_pfHiddenDeltaStates;
    Real* m_pfHiddenStates;


    Real* m_pfOutputBiases;
    Real* m_pfOutputTaus;

    UInt32 m_numHidden;
    Real m_fTimeStep;

    Real* m_pfHidden;
};

#endif
