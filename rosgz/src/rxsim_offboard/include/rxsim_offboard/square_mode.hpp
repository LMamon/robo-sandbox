#pragma once

#include <Eigen/Eigen>

#include <rclcpp/rclcpp.hpp>

#include <px4_ros2/components/mode.hpp>
#include <px4_ros2/components/mode_executor.hpp>

#include <px4_ros2/control/setpoint_types/goto.hpp>
#include <px4_ros2/control/setpoint_types/experimental/trajectory.hpp>
#include <px4_ros2/odometry/local_position.hpp>

using namespace std::chrono_literals;

static const std::string kName = "Square";

class SquareMode : public px4_ros2::ModeBase {
    public:
        explicit SquareMode(rclcpp::Node & node) : ModeBase(node, Settings{kName}), _node(node) {
            _goto_setpoint = std::make_shared<px4_ros2::GotoSetpointType>(*this);

            _trajectory_setpoint = std::make_shared<px4_ros2::TrajectorySetpointType>(*this);
            _vehicle_local_position = std::make_shared<px4_ros2::OdometryLocalPosition>(*this);

            setSetpointUpdateRate(30.0f);
        }

        ~SquareMode() override = default;

        void onActivate() override {
            RCLCPP_INFO(_node.get_logger(), "SquareMode activated");

            _start_position_m = _vehicle_local_position->positionNed();
            _target_position_m = _vehicle_local_position->positionNed();
            _start_heading_rad = _vehicle_local_position->heading();


            _state = State::Hover1;
            _state_start_time = _node.now();
        }

        void onDeactivate() override {
            RCLCPP_INFO(_node.get_logger(), "SquareMode deactivated");
        }

        void updateSetpoint(float dt_s) override { //state machine for square mode
            (void)dt_s;

            switch (_state) {
            case State::Hover1: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Hover");
                _goto_setpoint->update(
                    _vehicle_local_position->positionNed(),
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "hold");
                if (hoverComplete(3.0)) {
                    _state = State::FirstLeg;

                }
                break;
            }

            case State::FirstLeg: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "First Leg");
                _target_position_m = _start_position_m + Eigen::Vector3f(10.f, 0.f, 0.f);

                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "moving");
                if (positionReached(_target_position_m)) {
                    _target_position_m = _vehicle_local_position->positionNed();
                    _state = State::Hover2;

                    _state_start_time = _node.now();
                }
                break;
            }

            case State::Hover2: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Hover hold");
                
                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "holding");
                if (hoverComplete(3.0)) {
                    _state = State::SecondLeg;
                }
                break;
            }

            case State::SecondLeg: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Second Leg");
                _target_position_m = _start_position_m + Eigen::Vector3f(10.f, -10.f, 0.f);

                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "moving");
                if (positionReached(_target_position_m)) {
                    _target_position_m = _vehicle_local_position->positionNed();
                    _state = State::Hover3;

                    _state_start_time = _node.now();
                }
                break;
            }

            case State::Hover3: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Hover hold");
                
                
                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "hold");
                if (hoverComplete(3.0)) {
                    _state = State::ThirdLeg;
                }
                break;
            }

            case State::ThirdLeg: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Third Leg");
                _target_position_m = _start_position_m + Eigen::Vector3f(0.f, -10.f, 0.f);

                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "moving");
                if (positionReached(_target_position_m)) {
                    _target_position_m = _vehicle_local_position->positionNed();
                    _state = State::Hover4;

                    _state_start_time = _node.now();
                }
                break;
            }

            case State::Hover4: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Hover hold");
                
                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "holding");
                if (hoverComplete(3.0)) {
                    _target_position_m = _start_position_m;
                    _state = State::FourthLeg;
                }
                break;
            }

            case State::FourthLeg: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Forth Leg");

                _goto_setpoint->update(
                    _target_position_m,
                    _start_heading_rad,
                    _horizontal_speed_m_s
                );

                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "moving");
                if (positionReached(_target_position_m)) {
                    _state = State::Done;
                }
                break;
            }

            case State::Done: {
                RCLCPP_INFO_THROTTLE(_node.get_logger(), *_node.get_clock(), 1000, "Done");
                completed(px4_ros2::Result::Success);
                break;
            }
            }
        }
    public:    
        std::shared_ptr<px4_ros2::OdometryLocalPosition> _vehicle_local_position;

    private:
        enum class State {
            SettlingAtStart = 0,
            Takeoff,
            Hover1,
            FirstLeg,
            Hover2,
            SecondLeg,
            Hover3,
            ThirdLeg,
            Hover4,
            FourthLeg,
            Done
        };

        bool positionReached(const Eigen::Vector3f & target_position_m) const {
            static constexpr float kPositionErrorThreshold = 0.30f;
            static constexpr float kVelocityErrorThreshold = 0.20f;

            const Eigen::Vector3f position_error_m = target_position_m - _vehicle_local_position->positionNed();

            return (position_error_m.norm() < kPositionErrorThreshold) && (
                _vehicle_local_position->velocityNed().norm() < kVelocityErrorThreshold
            );
        }

        bool hoverComplete(double duration_s) {
            return (_node.now() - _state_start_time).seconds() >= duration_s;
        }

        float normalizeYaw(float yaw) {
            while (yaw > static_cast<float>(M_PI)) {
                yaw -= static_cast<float>(2.0 * M_PI);
            }

            while (yaw < static_cast<float>(-M_PI)) {
                yaw += static_cast<float>(2.0 * M_PI);
            }
            return yaw;
        }

    private:
        rclcpp::Node & _node;

        std::shared_ptr<px4_ros2::TrajectorySetpointType> _trajectory_setpoint;
        std::shared_ptr<px4_ros2::GotoSetpointType> _goto_setpoint;

        State _state{State::SettlingAtStart};

        rclcpp::Time _state_start_time;

        Eigen::Vector3f _start_position_m;
        Eigen::Vector3f _hover_position_m;
        Eigen::Vector3f _target_position_m;

        float _start_heading_rad{0.f};

        float _horizontal_speed_m_s{0.6f};
    };

    class SquareModeExecutor : public px4_ros2::ModeExecutorBase {
        public:
            enum class State {
                Reset,
                Arming,
                TakingOff,
                RunningSquare,
                RTL,
                WaitUntilDisarmed
            };

            SquareModeExecutor(rclcpp::Node & node, SquareMode & owned_mode) : ModeExecutorBase(
                    node,
                    Settings{px4_ros2::ModeExecutorBase::Settings::Activation:: ActivateAlways},
                    owned_mode
                ),
    
            _node(node),
            _square_mode(owned_mode)
            {
            }

            void onActivate() override {
                RCLCPP_INFO(_node.get_logger(), "SquareModeExecutor activated");

                runState(State::Reset, px4_ros2::Result::Success);
            }

            void onDeactivate(DeactivateReason reason) override {
                RCLCPP_INFO(_node.get_logger(), "SquareModeExecutor deactivated");

                (void)reason;
            }

            void runState(State state, px4_ros2::Result previous_result) {
                if (previous_result != px4_ros2::Result::Success) {
                    RCLCPP_ERROR(_node.get_logger(), "State %i: previous state failed: %s", (int)state,
                    resultToString(previous_result));

                    return;
                }

                switch (state) {
                case State::Reset: {
                    RCLCPP_INFO(_node.get_logger(), "reset*");
                    waitReadyToArm([this](px4_ros2::Result result) {
                            runState(State::Arming, result);
                        }
                    );
                    break;
                }
                case State::Arming:{
                    RCLCPP_INFO(_node.get_logger(), "Arming");
                    arm([this](px4_ros2::Result result) {
                            if (result != px4_ros2::Result::Success) {
                                runState(State::Reset, result);
                                return;
                            }

                            RCLCPP_INFO(_node.get_logger(), "Vehicle armed");

                            runState(State::TakingOff, result);
                        }
                    );
                    break;
                }

                case State::TakingOff: {
                    RCLCPP_INFO(_node.get_logger(), "Taking off");
                    takeoff([](px4_ros2::Result){});

                    _takeoff_timer = _node.create_wall_timer(std::chrono::milliseconds(100), [this]() {
                            auto pos = _square_mode._vehicle_local_position;

                            if (pos && pos->positionNed().z() < -1.0f && std::abs(pos->velocityNed().z()) < 0.3f) {
                                _takeoff_timer->cancel();

                                runState(State::RunningSquare, px4_ros2::Result::Success);
                            }
                        }
                    );

                    break;
                }

                case State::RunningSquare: {
                    RCLCPP_INFO(_node.get_logger(), "Running square");
                    scheduleMode(ownedMode().id(), [this](px4_ros2::Result result) {
                            runState(State::RTL, result);
                        }
                    );
                    break;
                }

                case State::RTL: {
                    RCLCPP_INFO(_node.get_logger(), "Returning to landing");
                    land([this](px4_ros2::Result result) {
                            runState(State::WaitUntilDisarmed, result);
                        }
                    );
                    break;
                }

                case State::WaitUntilDisarmed: {
                    RCLCPP_INFO(_node.get_logger(), "disarming");
                    waitUntilDisarmed([this](px4_ros2::Result result) {
                            if (result == px4_ros2::Result::Success) {
                                RCLCPP_INFO(_node.get_logger(), "Mission complete");
                            }
                        }
                    );
                    break;
                }

                default:
                    break;
                }
            }

        private:
            rclcpp::Node & _node;
            SquareMode & _square_mode;
            rclcpp::TimerBase::SharedPtr _takeoff_timer;
        };