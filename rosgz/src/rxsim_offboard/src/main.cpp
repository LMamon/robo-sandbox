#include "rxsim_offboard/square_mode.hpp"

#include <rclcpp/rclcpp.hpp>
#include <px4_ros2/components/node_with_mode.hpp>

using SquareModeExecutorNode = px4_ros2::NodeWithModeExecutor<SquareModeExecutor, SquareMode>;

static const std::string kNodeName = "square_mode";
static const bool kEnableDebugOutput = true;

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SquareModeExecutorNode>(kNodeName, kEnableDebugOutput));
  rclcpp::shutdown();
  return 0;
}