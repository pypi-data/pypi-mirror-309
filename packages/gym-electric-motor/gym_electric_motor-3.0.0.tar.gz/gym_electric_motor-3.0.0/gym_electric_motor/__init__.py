import sys

import gymnasium
from gymnasium.envs.registration import register
from packaging import version

import gym_electric_motor.core
import gym_electric_motor.envs
import gym_electric_motor.physical_system_wrappers
import gym_electric_motor.physical_systems
import gym_electric_motor.reference_generators
import gym_electric_motor.reward_functions
import gym_electric_motor.visualization

from .constraints import Constraint, LimitConstraint
from .core import (
    ConstraintMonitor,
    ElectricMotorEnvironment,
    ElectricMotorVisualization,
    PhysicalSystem,
    ReferenceGenerator,
    RewardFunction,
    SimulationEnvironment,
)
from .random_component import RandomComponent

make = ElectricMotorEnvironment.make


# Add all superclasses of the modules to the registry.

# Deactivate the order enforce wrapper that is put around a created env per default from gymnasium-version 0.21.0 onwards
# registration_kwargs = (
#    dict(order_enforce=False) if version.parse(gymnasium.__version__) >= version.parse("0.21.0") else dict()
# )
# registration_kwargs["disable_env_checker"] = True

registration_kwargs = dict()
# disable the environment checker for pytest
if "pytest" in sys.modules:
    registration_kwargs["disable_env_checker"] = True


envs_path = "gym_electric_motor.envs:"

# Permanently Excited DC Motor Environments
register(
    id="Finite-SC-PermExDc-v0",
    entry_point=envs_path + "FiniteSpeedControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-PermExDc-v0",
    entry_point=envs_path + "ContSpeedControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-PermExDc-v0",
    entry_point=envs_path + "FiniteTorqueControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-PermExDc-v0",
    entry_point=envs_path + "ContTorqueControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-PermExDc-v0",
    entry_point=envs_path + "FiniteCurrentControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-PermExDc-v0",
    entry_point=envs_path + "ContCurrentControlDcPermanentlyExcitedMotorEnv",
    **registration_kwargs,
)

# Externally Excited DC Motor Environments
register(
    id="Finite-SC-ExtExDc-v0",
    entry_point=envs_path + "FiniteSpeedControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-ExtExDc-v0",
    entry_point=envs_path + "ContSpeedControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-ExtExDc-v0",
    entry_point=envs_path + "FiniteTorqueControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-ExtExDc-v0",
    entry_point=envs_path + "ContTorqueControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-ExtExDc-v0",
    entry_point=envs_path + "FiniteCurrentControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-ExtExDc-v0",
    entry_point=envs_path + "ContCurrentControlDcExternallyExcitedMotorEnv",
    **registration_kwargs,
)

# Series DC Motor Environments
register(
    id="Finite-SC-SeriesDc-v0", entry_point=envs_path + "FiniteSpeedControlDcSeriesMotorEnv", **registration_kwargs
)
register(id="Cont-SC-SeriesDc-v0", entry_point=envs_path + "ContSpeedControlDcSeriesMotorEnv", **registration_kwargs)
register(
    id="Finite-TC-SeriesDc-v0", entry_point=envs_path + "FiniteTorqueControlDcSeriesMotorEnv", **registration_kwargs
)
register(id="Cont-TC-SeriesDc-v0", entry_point=envs_path + "ContTorqueControlDcSeriesMotorEnv", **registration_kwargs)
register(
    id="Finite-CC-SeriesDc-v0", entry_point=envs_path + "FiniteCurrentControlDcSeriesMotorEnv", **registration_kwargs
)
register(id="Cont-CC-SeriesDc-v0", entry_point=envs_path + "ContCurrentControlDcSeriesMotorEnv", **registration_kwargs)

# Shunt DC Motor Environments
register(id="Finite-SC-ShuntDc-v0", entry_point=envs_path + "FiniteSpeedControlDcShuntMotorEnv", **registration_kwargs)
register(id="Cont-SC-ShuntDc-v0", entry_point=envs_path + "ContSpeedControlDcShuntMotorEnv", **registration_kwargs)
register(id="Finite-TC-ShuntDc-v0", entry_point=envs_path + "FiniteTorqueControlDcShuntMotorEnv", **registration_kwargs)
register(id="Cont-TC-ShuntDc-v0", entry_point=envs_path + "ContTorqueControlDcShuntMotorEnv", **registration_kwargs)
register(
    id="Finite-CC-ShuntDc-v0", entry_point=envs_path + "FiniteCurrentControlDcShuntMotorEnv", **registration_kwargs
)
register(id="Cont-CC-ShuntDc-v0", entry_point=envs_path + "ContCurrentControlDcShuntMotorEnv", **registration_kwargs)

# Permanent Magnet Synchronous Motor Environments
register(
    id="Finite-SC-PMSM-v0",
    entry_point=envs_path + "FiniteSpeedControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-PMSM-v0",
    entry_point=envs_path + "FiniteTorqueControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-PMSM-v0",
    entry_point=envs_path + "FiniteCurrentControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-PMSM-v0",
    entry_point=envs_path + "ContCurrentControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-PMSM-v0",
    entry_point=envs_path + "ContTorqueControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-PMSM-v0",
    entry_point=envs_path + "ContSpeedControlPermanentMagnetSynchronousMotorEnv",
    **registration_kwargs,
)

# Externally Excited Synchronous Motor Environments
register(
    id="Finite-SC-EESM-v0",
    entry_point=envs_path + "FiniteSpeedControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-EESM-v0",
    entry_point=envs_path + "FiniteTorqueControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-EESM-v0",
    entry_point=envs_path + "FiniteCurrentControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-EESM-v0",
    entry_point=envs_path + "ContCurrentControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-EESM-v0",
    entry_point=envs_path + "ContTorqueControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-EESM-v0",
    entry_point=envs_path + "ContSpeedControlExternallyExcitedSynchronousMotorEnv",
    **registration_kwargs,
)
# Synchronous Reluctance Motor Environments
register(
    id="Finite-SC-SynRM-v0",
    entry_point=envs_path + "FiniteSpeedControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-SynRM-v0",
    entry_point=envs_path + "FiniteTorqueControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-SynRM-v0",
    entry_point=envs_path + "FiniteCurrentControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-SynRM-v0",
    entry_point=envs_path + "ContCurrentControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-SynRM-v0",
    entry_point=envs_path + "ContTorqueControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-SynRM-v0",
    entry_point=envs_path + "ContSpeedControlSynchronousReluctanceMotorEnv",
    **registration_kwargs,
)

# Squirrel Cage Induction Motor Environments
register(
    id="Finite-SC-SCIM-v0",
    entry_point=envs_path + "FiniteSpeedControlSquirrelCageInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-SCIM-v0",
    entry_point=envs_path + "FiniteTorqueControlSquirrelCageInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-SCIM-v0",
    entry_point=envs_path + "FiniteCurrentControlSquirrelCageInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-SCIM-v0",
    entry_point=envs_path + "ContCurrentControlSquirrelCageInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-TC-SCIM-v0",
    entry_point=envs_path + "ContTorqueControlSquirrelCageInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-SC-SCIM-v0", entry_point=envs_path + "ContSpeedControlSquirrelCageInductionMotorEnv", **registration_kwargs
)

# Doubly Fed Induction Motor Environments
register(
    id="Finite-SC-DFIM-v0",
    entry_point=envs_path + "FiniteSpeedControlDoublyFedInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-TC-DFIM-v0",
    entry_point=envs_path + "FiniteTorqueControlDoublyFedInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Finite-CC-DFIM-v0",
    entry_point=envs_path + "FiniteCurrentControlDoublyFedInductionMotorEnv",
    **registration_kwargs,
)
register(
    id="Cont-CC-DFIM-v0", entry_point=envs_path + "ContCurrentControlDoublyFedInductionMotorEnv", **registration_kwargs
)
register(
    id="Cont-TC-DFIM-v0", entry_point=envs_path + "ContTorqueControlDoublyFedInductionMotorEnv", **registration_kwargs
)
register(
    id="Cont-SC-DFIM-v0", entry_point=envs_path + "ContSpeedControlDoublyFedInductionMotorEnv", **registration_kwargs
)
