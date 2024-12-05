/*
# =============================================================================
# Copyright (c) 2016 - 2021 Blue Brain Project/EPFL
#
# See top-level LICENSE file for details.
# =============================================================================
*/

#pragma once

// Use MAJOR.MINOR for public version
#define CORENEURON_VERSION 900

#ifdef __cplusplus
extern "C" {
#endif

/// All-in-one initialization of mechanisms and solver
extern int solve_core(int argc, char** argv);

/// Initialize mechanisms
extern void mk_mech_init(int argc, char** argv);
/// Run core solver
extern int run_solve_core(int argc, char** argv);

#ifdef __cplusplus
}
#endif
