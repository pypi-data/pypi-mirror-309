/*+
    ARES/HADES/BORG Package -- ./extra/borg/libLSS/tests/test_borg_conv_gradient.cpp
    Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
    Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>

    Additional contributions from:
       Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
    
+*/
#include "libLSS/samplers/borg/borg_conv_likelihood.hpp"
#include "libLSS/physics/forwards/borg_lpt.hpp"
#define LIKELIHOOD_TO_TEST(obj) BorgConvDensitySampler obj(comm, 10, 0.1)
#define BORG_SUPERSAMPLING 1
#define MODEL_TO_TEST(obj,box) BorgLptModel<> *obj = new BorgLptModel<>(comm, box, false /* norsd*/, BORG_SUPERSAMPLING /* ss factor */, 0.001, false)
#include "generic_gradient_test.cpp"
