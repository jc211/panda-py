from __future__ import annotations
import numpy
import panda_py.libfranka
import pybind11_stubgen.typing_ext
import typing
__all__ = ['AppliedForce', 'AppliedTorque', 'CartesianImpedance', 'CartesianMotion', 'CartesianMotionGenerator', 'CartesianTrajectory', 'Force', 'Generator', 'IntegratedVelocity', 'JointMotion', 'JointMotionGenerator', 'JointPosition', 'JointTrajectory', 'MotionData', 'Panda', 'PandaContext', 'ReferenceFrame', 'TorqueController', 'fk', 'ik', 'ik_full']
M = typing.TypeVar("M", bound=int)
class AppliedForce(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., filter_coeff: float = 1.0) -> None:
        ...
    def set_control(self, force: numpy.ndarray[tuple[typing.Literal[6], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_damping(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_filter(self, filter_coeff: float) -> None:
        ...
class AppliedTorque(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., filter_coeff: float = 1.0) -> None:
        ...
    def set_control(self, torque: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_damping(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_filter(self, filter_coeff: float) -> None:
        ...
class CartesianImpedance(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, impedance: numpy.ndarray[tuple[typing.Literal[6], typing.Literal[6]], numpy.dtype[numpy.float64]] = ..., damping_ratio: float = 1.0, nullspace_stiffness: float = 0.5, filter_coeff: float = 1.0) -> None:
        """
                       Cartesian impedance controller. Takes the end-effector pose in robot
                       base frame, as well as desired nullspace joint positions as input.
        
                       Args:
                         impedance: Cartesian impedance expressed as a matrix
                           :math:`\in \mathbb{R}^{6\times 6}`.
                         damping_ratio: Cartesian damping is computed based on the given
                           impedance and damping ratio.
                         nullspace_stiffness: Control gain of the nullspace term.
                         filter_coeff: TP1 filter coefficient used to filter input signals.
        """
    def set_control(self, position: numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]], orientation: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]], q_nullspace: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ...) -> None:
        ...
    def set_damping_ratio(self, damping: float) -> None:
        ...
    def set_filter(self, filter_coeff: float) -> None:
        ...
    def set_impedance(self, impedance: numpy.ndarray[tuple[typing.Literal[6], typing.Literal[6]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_nullspace_stiffness(self, nullspace_stiffness: float) -> None:
        ...
class CartesianMotion:
    acceleration_rel: float
    jerk_rel: float
    reference_frame: ReferenceFrame
    velocity_rel: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, position: numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]], orientation: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]], reference_frame: ReferenceFrame = ...) -> None:
        ...
    @typing.overload
    def __init__(self, pose: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]], reference_frame: ReferenceFrame = ...) -> None:
        ...
class CartesianMotionGenerator(Generator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, keep_running: bool = False, done_callback: typing.Callable[[], None] = None) -> None:
        ...
    def add_waypoint(self, waypoint: CartesianMotion) -> None:
        ...
    def add_waypoints(self, waypoints: list[CartesianMotion]) -> None:
        ...
    def clear_waypoints(self) -> None:
        ...
class CartesianTrajectory:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, positions: list[numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]]], orientations: list[numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]]], speed_factor: float = 0.2, max_deviation: float = 0, timeout: float = 30.0) -> None:
        ...
    @typing.overload
    def __init__(self, poses: list[numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]]], speed_factor: float = 0.2, max_deviation: float = 0, timeout: float = 30.0) -> None:
        ...
    def get_duration(self) -> float:
        ...
    def get_orientation(self, time: float) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def get_pose(self, time: float) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]]:
        ...
    def get_position(self, time: float) -> numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
class Force(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, k_p: float = 1.0, k_i: float = 2.0, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., threshold: float = 0.01, filter_coeff: float = 0.001) -> None:
        ...
    def set_control(self, force: numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_filter(self, filter_coeff: float) -> None:
        ...
    def set_integral_gain(self, k_i: float) -> None:
        ...
    def set_proportional_gain(self, k_p: float) -> None:
        ...
    @property
    def name(self) -> str:
        ...
class Generator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def set_done_callback(self, done_callback: typing.Callable[[], None]) -> None:
        ...
class IntegratedVelocity(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, stiffness: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ...) -> None:
        ...
    def get_qd(self) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def set_control(self, velocity: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_damping(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_stiffness(self, stiffness: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
class JointMotion:
    acceleration_rel: float
    jerk_rel: float
    velocity_rel: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, target: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(7)]) -> None:
        ...
    @property
    def target(self) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
class JointMotionGenerator(Generator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, keep_running: bool = False, done_callback: typing.Callable[[], None] = None) -> None:
        ...
    def add_waypoint(self, waypoint: JointMotion) -> None:
        ...
    def add_waypoints(self, waypoints: list[JointMotion]) -> None:
        ...
    def clear_waypoints(self) -> None:
        ...
class JointPosition(TorqueController):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, stiffness: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., filter_coeff: float = 1.0) -> None:
        ...
    def set_control(self, position: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]], velocity: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ...) -> None:
        ...
    def set_damping(self, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
    def set_filter(self, filter_coeff: float) -> None:
        ...
    def set_stiffness(self, stiffness: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> None:
        ...
class JointTrajectory:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, waypoints: list[numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]], speed_factor: float = 0.2, max_deviation: float = 0, timeout: float = 30.0) -> None:
        ...
    def get_duration(self) -> float:
        ...
    def get_joint_accelerations(self, time: float) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def get_joint_positions(self, time: float) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
    def get_joint_velocities(self, time: float) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
class MotionData:
    acceleration_rel: float
    jerk_rel: float
    velocity_rel: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, velocity: float = 1.0, acceleration: float = 1.0, jerk: float = 1.0) -> None:
        ...
    def with_max_dynamics(self) -> MotionData:
        ...
class Panda:
    """
    
         The main interface of panda-py to control the robot.
      
    """
    acceleration_rel: float
    jerk_rel: float
    velocity_rel: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, hostname: str, name: str = 'panda', realtime_config: panda_py.libfranka.RealtimeConfig = panda_py.libfranka.RealtimeConfig.kIgnore) -> None:
        ...
    def create_context(self, frequency: float, max_runtime: float = 0.0, max_iter: int = 0) -> PandaContext:
        ...
    def disable_logging(self) -> None:
        ...
    def enable_logging(self, buffer_size: int) -> None:
        ...
    def get_log(self) -> dict[str, list[numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]]]:
        ...
    def get_model(self) -> panda_py.libfranka.Model:
        ...
    def get_orientation(self, scalar_first: bool = False) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
                       Get current end-effector orientation
                       :math:`\mathbf q = (\vec{v},\ r),~~ \mathbf q \in \mathbb{H},~~ \vec{v}\in \mathbb{R}^3,~~ r \in \mathbb{R}`
                       in robot base frame.
        
                       Args:
                         scalar_first: If True returns quaternion in scalar first
                           representation (default: False)
                       
                       Returns:
                         Vector of shape (4,) holding quaternion coefficients.
        """
    def get_pose(self) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]]:
        ...
    def get_position(self) -> numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
                  Current end-effector position in robot base frame.
        """
    def get_robot(self) -> panda_py.libfranka.Robot:
        """
                       Get a reference to the :py:class:`libfranka.Robot` class behind this instance.
        """
    def get_state(self) -> panda_py.libfranka.RobotState:
        """
                  Get a copy of the last :py:class:`libfranka.RobotState` received from the robot.
        """
    def is_moving(self) -> bool:
        ...
    def raise_error(self) -> None:
        """
                  Raises a `RuntimeError` in Python when the robot has an active error.
                  As panda-py controllers run asynchroneously, encountered errors don't
                  propagate to the proces' main thread. Use this function or
                  :py:class:`PandaContext` to catch errors.
        """
    def recover(self) -> None:
        ...
    def set_default_behavior(self) -> None:
        ...
    def start_controller(self, controller: TorqueController) -> None:
        ...
    def start_generator(self, generator: ...) -> None:
        ...
    def stop(self) -> None:
        ...
    def stop_controller(self) -> None:
        ...
    def stop_generator(self) -> None:
        ...
    def teaching_mode(self, active: bool, damping: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ...) -> None:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def q(self) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
        ...
class PandaContext:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __enter__(self) -> PandaContext:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> bool:
        ...
    def ok(self) -> bool:
        ...
    @property
    def num_ticks(self) -> int:
        ...
    @property
    def time(self) -> float:
        ...
class ReferenceFrame:
    """
    Members:
    
      GLOBAL
    
      RELATIVE
    """
    GLOBAL: typing.ClassVar[ReferenceFrame]  # value = <ReferenceFrame.GLOBAL: 0>
    RELATIVE: typing.ClassVar[ReferenceFrame]  # value = <ReferenceFrame.RELATIVE: 1>
    __members__: typing.ClassVar[dict[str, ReferenceFrame]]  # value = {'GLOBAL': <ReferenceFrame.GLOBAL: 0>, 'RELATIVE': <ReferenceFrame.RELATIVE: 1>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TorqueController:
    """
    
              Base class for all torque controllers. Torque controllers
              provide the robot with torques at 1KHz and the user with
              an asynchronous interface to provide control signals.
          
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def get_time(self) -> float:
        """
                  Get time in seconds since this controller was started.
        """
def fk(q: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]]:
    """
         Computes end-effector pose in base frame from joint positions.
    """
@typing.overload
def ik(O_T_EE: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]], q_init: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., q_7: float = 0.7853981633974483) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
    """
              Compute analytical inverse kinematics. 
              Solution is case consistent with configuration  given in `q_init`.
    
              Args:
                O_T_EE: Homogeneous transform :math:`\mathbb{R}^{4\times 4}` describing
                  the end-effector pose.
                q_init: Reference joint positions, the result will be consistent
                  with this configuration.
                q_7: Joint 7 is considered the redundant joint, use `q_7` to set the
                  desired joint position (default: :math:`\frac{\pi}{4}`).
    
              Returns:
                Vector of shape (7,) containing joint positions.
    """
@typing.overload
def ik(position: numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]], orientation: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]], q_init: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., q_7: float = 0.7853981633974483) -> numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]]:
    """
              Same as :py:func:`ik` above, but takes position and orientation arguments.
    """
@typing.overload
def ik_full(O_T_EE: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float64]], q_init: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., q_7: float = 0.7853981633974483) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[7]], numpy.dtype[numpy.float64]]:
    ...
@typing.overload
def ik_full(position: numpy.ndarray[tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]], orientation: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]], q_init: numpy.ndarray[tuple[typing.Literal[7], typing.Literal[1]], numpy.dtype[numpy.float64]] = ..., q_7: float = 0.7853981633974483) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[7]], numpy.dtype[numpy.float64]]:
    ...
_DTAU_J_MAX: numpy.ndarray  # value = array([1000., 1000., 1000., 1000., 1000., 1000., 1000.])
_JOINT_LIMITS_LOWER: numpy.ndarray  # value = array([-2.8973, -1.7628, -2.8973, -3.0718, -2.8973, -0.0175, -2.8973])
_JOINT_LIMITS_UPPER: numpy.ndarray  # value = array([ 2.8973,  1.7628,  2.8973, -0.0698,  2.8973,  3.7525,  2.8973])
_JOINT_POSITION_START: numpy.ndarray  # value = array([ 0.        , -0.78539816,  0.        , -2.35619449,  0.        ,...
_TAU_J_MAX: numpy.ndarray  # value = array([87., 87., 87., 87., 12., 12., 12.])
