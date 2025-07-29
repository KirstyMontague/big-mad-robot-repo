#include "perceptron_multi.h"

#include <fstream>
#include <cmath>

/****************************************/
/****************************************/

CPerceptronMulti::CPerceptronMulti() :
    m_pfHiddenBiases(NULL),
    m_pfHiddenTaus(NULL),
    m_pfHiddenDeltaStates(NULL),
    m_pfHiddenStates(NULL),
    m_pfInputToHiddenWeights(NULL),
    m_pfHiddenToOutputWeights(NULL),
    m_pfOutputBiases(NULL),
    m_pfOutputTaus(NULL),
    m_numHidden(0),
    m_fTimeStep(0.1f)
{}

/****************************************/
/****************************************/

CPerceptronMulti::~CPerceptronMulti()
{
    if(m_pfInputToHiddenWeights) delete[] m_pfInputToHiddenWeights;
    if(m_pfHiddenToOutputWeights) delete[] m_pfHiddenToOutputWeights;
    if(m_pfHiddenBiases) delete[] m_pfHiddenBiases;
    if(m_pfOutputBiases) delete[] m_pfOutputBiases;
    if(m_pfHiddenTaus) delete[] m_pfHiddenTaus;
    if(m_pfHiddenDeltaStates) delete[] m_pfHiddenDeltaStates;
    if(m_pfHiddenStates) delete[] m_pfHiddenStates;
}

/****************************************/
/****************************************/

void CPerceptronMulti::Init(TConfigurationNode& t_tree, UInt32 numInputs, UInt32 numHidden, UInt32 numOutputs)
{
    CNeuralNetwork::Init(t_tree, numInputs, numOutputs);
    m_numHidden = numHidden;
    m_pfHidden = new Real[m_numHidden];
}

void CPerceptronMulti::Load(const Real* chromosome, bool tracking)
{
    LoadNetworkParameters(chromosome, tracking);
}

/****************************************/
/****************************************/

void CPerceptronMulti::Destroy()
{
    m_numHidden = 0;

    if( m_pfInputToHiddenWeights )  delete[] m_pfInputToHiddenWeights;
    m_pfInputToHiddenWeights = NULL;

    if( m_pfHiddenToOutputWeights ) delete[] m_pfHiddenToOutputWeights;
    m_pfHiddenToOutputWeights = NULL;

    if( m_pfHiddenBiases )          delete[] m_pfHiddenBiases;
    m_pfHiddenBiases = NULL;

    if( m_pfOutputBiases )          delete[] m_pfOutputBiases;
    m_pfOutputBiases = NULL;

    if( m_pfHiddenTaus )            delete[] m_pfHiddenTaus;
    m_pfHiddenTaus = NULL;

    if( m_pfHiddenDeltaStates )     delete[] m_pfHiddenDeltaStates;
    m_pfHiddenDeltaStates = NULL;

    if( m_pfHiddenStates )          delete[] m_pfHiddenStates;
    m_pfHiddenStates = NULL;
}

/****************************************/
/****************************************/

void CPerceptronMulti::LoadNetworkParameters(const Real* chromosome, bool tracking)
{

    uint pos = 1;
    
    // if (tracking) std::cout << chromosome[0] << "\n";

    m_pfInputToHiddenWeights = new Real[m_unNumberOfInputs * m_numHidden];
    for( uint i = 0; i < m_unNumberOfInputs * m_numHidden; i++ )
    {
        m_pfInputToHiddenWeights[i] = chromosome[pos++];
        // if (tracking) std::cout << m_pfInputToHiddenWeights[i] << "\n";
    }

    // if (tracking) std::cout << m_pfInputToHiddenWeights[0] << "\n";

    m_pfHiddenBiases = new Real[m_numHidden];
    for( uint i = 0; i < m_numHidden; i++ )
    {
        m_pfHiddenBiases[i] = chromosome[pos++];
        // if (tracking) std::cout << m_pfHiddenBiases[i] << "\n";
    }

    // if (tracking) std::cout <<  "\n";

    m_pfHiddenToOutputWeights = new Real[m_numHidden * m_unNumberOfOutputs];
    for( uint i = 0; i < m_numHidden * m_unNumberOfOutputs; i++ )
    {
        m_pfHiddenToOutputWeights[i] = chromosome[pos++];
        // if (tracking) std::cout << m_pfHiddenToOutputWeights[i] << "\n";
    }

    // if (tracking) std::cout <<  "\n";

    m_pfOutputBiases = new Real[m_unNumberOfOutputs];
    for( uint i = 0; i < m_unNumberOfOutputs; i++ )
    {
        m_pfOutputBiases[i] = chromosome[pos++];
        // if (tracking) std::cout << m_pfOutputBiases[i] << "\n";
    }

    // if (tracking) std::cout << m_pfOutputBiases[1] << "\n";

    // if (tracking) std::cout <<  "\n";
}

/****************************************/
/****************************************/

void CPerceptronMulti::ComputeOutputs(bool tracking)
{
    for(size_t i = 0; i < m_numHidden; ++i)
    {
        // Add the bias
        m_pfHidden[i] = m_pfHiddenBiases[i];

        // Add the weighted input
        for(size_t j = 0; j < m_unNumberOfInputs; ++j)
        {
            m_pfHidden[i] += m_pfInputToHiddenWeights[i * m_unNumberOfInputs + j] * m_pfInputs[j];
        }

        // Activation function
        m_pfHidden[i] = sigmoid(m_pfHidden[i]);
    }
    
    for(size_t i = 0; i < m_unNumberOfOutputs; ++i)
    {
        // Add the bias
        m_pfOutputs[i] = m_pfOutputBiases[i];

        // Add the weighted input
        for(size_t j = 0; j < m_numHidden; ++j)
        {
            m_pfOutputs[i] += m_pfHiddenToOutputWeights[i * m_numHidden + j] * m_pfHidden[j];
        }

        // Activation function
        m_pfOutputs[i] = sigmoid(m_pfOutputs[i]);
        
        // if (tracking) std::cout << m_pfOutputs[i] << "\n";
        m_pfOutputs[i] *= 7;
   }

}

/****************************************/
/****************************************/

Real CPerceptronMulti::sigmoid(Real value)
{
    return Real(1.0)/( exp(-(value)) + 1.0 );
}
