#+
#   ARES/HADES/BORG Package -- ./extra/borg/scripts/generate_vobs_tests.py
#   Copyright (C) 2019 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+

import os
import sys

output_cmake_file = sys.argv[1]
input_config = sys.argv[2]
base_dir = sys.argv[3]

with open(input_config, mode="r") as f:
  config = {}
  exec(f.read(), {}, config)
  config = config['tests']

tests = config['tests']

with open(output_cmake_file, "wt") as f:

    for test_name in tests:
      test = tests[test_name]
      includes = test['includes']
      likelihood = test['likelihood']
      model = test['model']
      model_args = test.get('model_args', 'comm, box, 0.001');
      model_code=""

      f.write("""
add_executable(test_vobs_%(test_name)s %(base_dir)s/%(test_source)s)
target_link_libraries(test_vobs_%(test_name)s test_library_LSS LSS ${LIBS})
ares_add_test_targets(test_vobs_%(test_name)s)
"""
         % dict(test_name=test_name, base_dir=base_dir, test_source="test_%s_vobs.cpp" % (test_name,)
      ))

      includes_str = \
        "\n".join(
            map(lambda x: "#include \"%s\"" % (x,), includes)
        )


      if 'model' in test:
        args = test.get('model_args', 'comm, box, 0.001')

      with open(os.path.join(base_dir,"test_%s_vobs.cpp" % (test_name,)), mode="wt") as f2:
        f2.write("""%(includes)s
#include "libLSS/samplers/rgen/hmc/hmc_density_sampler.hpp"
#include "libLSS/physics/likelihoods/base.hpp"

namespace L = LibLSS::Likelihood;
using LibLSS::LikelihoodInfo;
using LibLSS::HMCDensitySampler;
using LibLSS::MarkovState;
using LibLSS::BoxModel;

typedef %(likelihood)s ThisLikelihood;


auto makeModel(MarkovState& state, BoxModel const& box, LikelihoodInfo& info) {
  auto comm = L::getMPI(info);
  return std::make_shared<%(model)s>(%(model_args)s);
}

#include "libLSS/tests/generic_borg_vobs_test.cpp"
""" % dict(includes=includes_str,likelihood=likelihood,model=model,model_args=model_args))

# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2019
