#pragma once

#include <atomic>
#include <memory>
#include <mutex>
#include <optional>
#include <queue>
#include <string>
#include <vector>
#include <functional>

#include <Eigen/Geometry>

#include <franka/duration.h>
#include <franka/robot_state.h>

#include <ruckig/ruckig.hpp>

#include "motion/generator.h"
#include "motion/cartesian_motion.hpp"
#include "motion/motion_data.hpp"
#include "panda.h"


namespace motion
{

    struct CartesianMotionGenerator : public CartesianGenerator
    {

        // run base class
        CartesianMotionGenerator(bool keep_running = true, std::function<void()> done_callback = nullptr)
            : keep_running_(keep_running), CartesianGenerator(done_callback) {}

        void addWaypoint(const CartesianMotion &waypoint)
        {
            std::scoped_lock lock(mux_);
            waypoints_.push(waypoint);
            reload_ = true;
        }

        void addWaypoints(const std::vector<CartesianMotion> &waypoints)
        {
            std::scoped_lock lock(mux_);
            for (const auto &waypoint : waypoints)
            {
                this->waypoints_.push(waypoint);
            }
            reload_ = true;
        }

        void clearWaypoints()
        {
            std::scoped_lock lock(mux_);
            while (!waypoints_.empty())
            {
                waypoints_.pop();
            }
            reload_ = true;
        }

        void start(Panda *robot, const franka::RobotState &robot_state,
                   std::shared_ptr<franka::Model> model) override
        {
            panda_ = robot;
            reload_ = true;
            motion_finished_ = false;
            setInputCurrent(robot_state);
            Eigen::Isometry3d O_T_EE = Eigen::Isometry3d(Eigen::Matrix4d::Map(robot_state.O_T_EE.data()));
            // std::cout << "current translation: " << O_T_EE.translation() << std::endl;

            auto translation = O_T_EE.translation();
            auto quat = Eigen::Quaterniond(O_T_EE.rotation());

            input_para_.target_position[0] = translation[0];
            input_para_.target_position[1] = translation[1];
            input_para_.target_position[2] = translation[2];
            input_para_.target_position[3] = quat.x();
            input_para_.target_position[4] = quat.y();
            input_para_.target_position[5] = quat.z();
            input_para_.target_position[6] = quat.w();

            input_para_.target_velocity = toStd(Vector7d::Zero());
            input_para_.target_acceleration = toStd(Vector7d::Zero());

            setProfile(1.0, 1.0, 1.0);
        }

        void stop(const franka::RobotState &robot_state,
                  std::shared_ptr<franka::Model> model) override
        {
            motion_finished_ = true;
        }

        franka::CartesianPose step(const franka::RobotState &robot_state,
                                    franka::Duration period) override
        {

            panda_->_setState(robot_state);
            setTime(getTime() + period.toSec());
            const int steps = std::max<int>(period.toMSec(), 1);
            auto O_T_EE = Eigen::Isometry3d(Eigen::Matrix4d::Map(robot_state.O_T_EE.data()));
            // std::cout << "commanded pose: " << O_T_EE.matrix() << std::endl;

            if (motion_finished_)
            {
                if (current_cooldown_iteration < cooldown_iterations)
                {
                    current_cooldown_iteration += 1;
                    return franka::CartesianPose(robot_state.O_T_EE_c);
                }
                else
                {
                    return franka::MotionFinished(franka::CartesianPose(robot_state.O_T_EE_c));
                }
            }
            for (int i = 0; i < steps; i++)
            {

                if (reload_)
                {
                    loadNextWaypoint(robot_state);
                    reload_ = false;
                }

                // check if new waypoint is available

                // std::cout <<"----------------------"<<std::endl;
                // std::cout << "input_current: " << input_para_.current_position[0] << ", " << input_para_.current_position[1] << ", " << input_para_.current_position[2] << std::endl;
                // std::cout << "input_current_velocity: " << input_para_.current_velocity[0] << ", " << input_para_.current_velocity[1] << ", " << input_para_.current_velocity[2] << std::endl;
                // std::cout << "input_current_acceleration: " << input_para_.current_acceleration[0] << ", " << input_para_.current_acceleration[1] << ", " << input_para_.current_acceleration[2] << std::endl;
                // std::cout << "input_target: " << input_para_.target_position[0] << ", " << input_para_.target_position[1] << ", " << input_para_.target_position[2] << std::endl;
                // std::cout << "input_target_velocity: " << input_para_.target_velocity[0] << ", " << input_para_.target_velocity[1] << ", " << input_para_.target_velocity[2] << std::endl;
                // std::cout << "input_target_acceleration: " << input_para_.target_acceleration[0] << ", " << input_para_.target_acceleration[1] << ", " << input_para_.target_acceleration[2] << std::endl;
                result = trajectory_generator_.update(input_para_, output_para_);
                // std::cout << "output_new_position: " << output_para_.new_position[0] << ", " << output_para_.new_position[1] << ", " << output_para_.new_position[2] << std::endl;

                if (result == ruckig::Result::Finished)
                {
                    if (!waypoints_.empty())
                    {
                        reload_ = true;
                    }
                    else
                    {
                        if (!keep_running_)
                        {
                            if (current_cooldown_iteration < cooldown_iterations)
                            {
                                current_cooldown_iteration += 1;
                                return getPoseFromOutput(robot_state, output_para_);
                            }
                            else
                            {
                                motion_finished_ = true;
                                return franka::MotionFinished(getPoseFromOutput(robot_state, output_para_));
                            }
                        }
                    }
                }
                else if (result != ruckig::Result::Working)
                {
                    std::cout << "[rucking robot] Invalid inputs:" << result << std::endl;
                    motion_finished_ = true;
                    return franka::MotionFinished(franka::CartesianPose(robot_state.O_T_EE_c));
                }

                output_para_.pass_to_input(input_para_);
            }

            return getPoseFromOutput(robot_state, output_para_);
        }

        bool isRunning() { return !motion_finished_; }

        const std::string name() { return "Joint Motion Generator"; }

    private:
        std::mutex mux_;
        std::atomic<bool> motion_finished_;
        std::queue<CartesianMotion> waypoints_;
        std::optional<CartesianMotion> current_waypoint_;
        ruckig::Ruckig<7> trajectory_generator_{ Panda::control_rate }; // xyz + quaternion
        ruckig::InputParameter<7> input_para_;
        ruckig::OutputParameter<7> output_para_;
        ruckig::Result result;
        bool reload_ = false;
        bool keep_running_ = true;
        const size_t cooldown_iterations{5};
        size_t current_cooldown_iteration{0};

        void setProfile(double velocity_rel, double acceleration_rel,
                        double jerk_rel)
        {
            auto translation_factor = 0.4;
            auto derivative_factor = 0.4;
            for (int dof = 0; dof < 3; dof += 1)
            {
                input_para_.max_velocity[dof] =
                    0.8 * translation_factor * Panda::max_translation_velocity * panda_->velocity_rel * velocity_rel;
                input_para_.max_acceleration[dof] =
                    0.3 * translation_factor * derivative_factor * Panda::max_translation_acceleration * panda_->acceleration_rel *
                    acceleration_rel;
                input_para_.max_jerk[dof] =
                    0.3 * translation_factor * derivative_factor * Panda::max_translation_jerk * panda_->jerk_rel * jerk_rel;
            }
            auto quat_factor = 0.5; // dq/dt = 0.5*w*q (w: angular velocity, q: quaternion)
            for(int dof=3; dof<3+4; dof+=1) {
                input_para_.max_velocity[dof] =
                    quat_factor * Panda::max_rotation_velocity * panda_->velocity_rel * velocity_rel;
                input_para_.max_acceleration[dof] =
                    quat_factor * 0.3 * Panda::max_rotation_acceleration * panda_->acceleration_rel *
                    acceleration_rel;
                input_para_.max_jerk[dof] =
                    quat_factor * 0.3 * Panda::max_rotation_jerk * panda_->jerk_rel * jerk_rel;
            }

        }

        void setInputCurrent(const franka::RobotState &robot_state)
        {

            auto X_WE = Eigen::Isometry3d(Eigen::Matrix4d::Map(robot_state.O_T_EE.data()));
            auto translation = X_WE.translation();
            auto rotation = X_WE.rotation();
            Eigen::Quaterniond q(rotation);

            // std::cout<<"inputCurrent: "<<translation<<std::endl;

            // input_para_.current_position = toStd3(translation);

            input_para_.current_position[0] = translation[0];
            input_para_.current_position[1] = translation[1];
            input_para_.current_position[2] = translation[2];
            input_para_.current_position[3] = q.x();
            input_para_.current_position[4] = q.y();
            input_para_.current_position[5] = q.z();
            input_para_.current_position[6] = q.w();

            input_para_.current_velocity = toStd(Vector7d::Zero());
            input_para_.current_acceleration = toStd(Vector7d::Zero());
            // input_para_.current_velocity = toStd3(Eigen::Vector3d::Zero());
            // input_para_.current_acceleration = toStd3(Eigen::Vector3d::Zero());
        }

        void setInputTarget(const franka::RobotState& robot_state, const CartesianMotion &waypoint)
        {
            auto X_WE_target = waypoint.target;


            if (waypoint.reference_frame == ReferenceFrame::RELATIVE)
            {
                auto X_WE = Eigen::Isometry3d(Eigen::Matrix4d::Map(robot_state.O_T_EE.data()));
                X_WE_target = X_WE * waypoint.target;
            }
            auto translation = X_WE_target.translation();
            auto rotation = X_WE_target.rotation();
            Eigen::Quaterniond q(rotation);
            q.normalize();

            // std::cout << "InputTarget: " << translation << std::endl;

            // input_para_.target_position = toStd3(translation);
            input_para_.target_position[0] = translation[0];
            input_para_.target_position[1] = translation[1];
            input_para_.target_position[2] = translation[2];
            input_para_.target_position[3] = q.x();
            input_para_.target_position[4] = q.y();
            input_para_.target_position[5] = q.z();
            input_para_.target_position[6] = q.w();

            input_para_.target_velocity = toStd(Vector7d::Zero());
            input_para_.target_acceleration = toStd(Vector7d::Zero());
            // input_para_.target_velocity = toStd3(Eigen::Vector3d::Zero());
            // input_para_.target_acceleration = toStd3(Eigen::Vector3d::Zero());
            setProfile(waypoint.velocity_rel, waypoint.acceleration_rel,
                       waypoint.jerk_rel);
        }

        void loadNextWaypoint(const franka::RobotState &robot_state)
        {
            if (waypoints_.empty())
            {
                Eigen::Isometry3d X_WE(Eigen::Matrix4d::Map(robot_state.O_T_EE_c.data()));
                auto target = CartesianMotion(X_WE);
                current_waypoint_.emplace(target);
            }
            else
            {
                std::scoped_lock lock(mux_);
                current_waypoint_.emplace(waypoints_.front());
                waypoints_.pop();
            }
            setInputTarget(robot_state, *current_waypoint_);
        }

        // franka::CartesianPose getPoseFromOutput(ruckig::OutputParameter<7> &output)
        franka::CartesianPose getPoseFromOutput(const franka::RobotState& robot_state, ruckig::OutputParameter<7> &output)
        {
            // Eigen::Isometry3d pose = Eigen::Isometry3d::Identity();
            // pose.translation() = Eigen::Vector3d(output.new_position[0], output.new_position[1], output.new_position[2]);

            // Eigen::Map<Eigen::Matrix<double, 4, 4, Eigen::ColMajor>> pose(robot_state.O_T_EE.data());
            // std::cout<<"New position: "<<output.new_position[0]<<" "<<output.new_position[1]<<" "<<output.new_position[2]<<std::endl;
            auto pose = Eigen::Isometry3d(Eigen::Matrix<double, 4, 4, Eigen::ColMajor>::Map(robot_state.O_T_EE_c.data()));
            pose.translation() = Eigen::Vector3d(output.new_position[0], output.new_position[1], output.new_position[2]);
            Eigen::Quaterniond q(output.new_position[6], output.new_position[3], output.new_position[4], output.new_position[5]);
            q.normalize();
            pose.linear() = q.toRotationMatrix();
            
            // std::cout << "pose: " << pose.matrix() << std::endl;

            std::array<double, 16> vec;
            Eigen::Map<Eigen::Matrix<double, 4, 4, Eigen::ColMajor>>(vec.data()) = pose.matrix();
            // std::cout<< "vec: "<< vec[0] << " " << vec[1] << " " << vec[2] << " " << vec[3] << " " << vec[4] << " " << vec[5] << " " << vec[6] << " " << vec[7] << " " << vec[8] << " " << vec[9] << " " << vec[10] << " " << vec[11] << " " << vec[12] << " " << vec[13] << " " << vec[14] << " " << vec[15] << std::endl;
            // std::cout<<"dat: "<< robot_state.O_T_EE[0] << " " << robot_state.O_T_EE[1] << " " << robot_state.O_T_EE[2] << " " << robot_state.O_T_EE[3] << " " << robot_state.O_T_EE[4] << " " << robot_state.O_T_EE[5] << " " << robot_state.O_T_EE[6] << " " << robot_state.O_T_EE[7] << " " << robot_state.O_T_EE[8] << " " << robot_state.O_T_EE[9] << " " << robot_state.O_T_EE[10] << " " << robot_state.O_T_EE[11] << " " << robot_state.O_T_EE[12] << " " << robot_state.O_T_EE[13] << " " << robot_state.O_T_EE[14] << " " << robot_state.O_T_EE[15] << std::endl;

            // return franka::CartesianPose(vec, robot_state.elbow);
            return franka::CartesianPose(vec);
        }
    };
} // namespace motion
