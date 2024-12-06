/*+
    ARES/HADES/BORG Package -- ./extra/hades/libLSS/samplers/bias_model_params.hpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#pragma once
#ifndef __LIBLSS_HADES_BIAS_MODEL_PARAMS_SAMPLER_HPP
#  define __LIBLSS_HADES_BIAS_MODEL_PARAMS_SAMPLER_HPP

#  include "libLSS/mpi/generic_mpi.hpp"
#  include "libLSS/mcmc/global_state.hpp"
#  include "libLSS/tools/fftw_allocator.hpp"
#  include "libLSS/samplers/core/markov.hpp"
#  include "libLSS/samplers/core/random_number.hpp"
#  include "libLSS/samplers/core/types_samplers.hpp"
#  include "libLSS/physics/forward_model.hpp"
#  include "libLSS/samplers/core/gridLikelihoodBase.hpp"
#  include <vector>

namespace LibLSS {

  class BiasModelParamsSampler : public MarkovSampler {
  protected:
    MPI_Communication *comm;
    std::vector<std::string> paramsToSample;
    std::shared_ptr<BORGForwardModel> model;
    std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood;
    ModelDictionnary init_state;
    int numBias;
    ArrayType1d *biasElement;
    std::set<int> bias_to_freeze;
    typedef std::function<void()> HookType;

    HookType pre_hook, post_hook;
    std::string prefix;

  public:
    BiasModelParamsSampler(
        MPI_Communication *comm_,
        std::shared_ptr<GridDensityLikelihoodBase<3>> likelihood_,
        std::shared_ptr<BORGForwardModel> model_, int numBias_,
        std::string const &prefix);
    virtual ~BiasModelParamsSampler();

    void freezeSet(std::set<int> bias_to_freeze) {
      this->bias_to_freeze = bias_to_freeze;
    }

    void initialize(MarkovState &state) override;
    void restore(MarkovState &state) override;
    void sample(MarkovState &state) override;

    void setLimiterHooks(HookType pre_hook_, HookType post_hook_) {
      pre_hook = pre_hook_;
      post_hook = post_hook_;
    }
  };

} // namespace LibLSS

#endif
