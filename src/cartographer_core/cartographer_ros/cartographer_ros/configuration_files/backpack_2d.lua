include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  -- 用来发布子地图的ROS坐标系ID，位姿的父坐标系，通常是map。
  map_frame = "map",
  -- SLAM算法跟随的坐标系ID
  tracking_frame = "base_link",
  -- 将发布map到published_frame之间的tf
  published_frame = "base_link",
  -- 位于“published_frame ”和“map_frame”之间，用来发布本地SLAM结果（非闭环），通常是“odom”
  odom_frame = "odom",
  -- 是否提供里程计
  provide_odom_frame = true,
  -- 只发布二维位姿态（不包含俯仰角）
  publish_frame_projected_to_2d = false,
  -- 是否使用里程计数据
  use_odometry = false,
  -- 是否使用GPS定位
  use_nav_sat = false,
  -- 是否使用路标
  use_landmarks = false,
  -- 订阅的laser scan topics的个数
  num_laser_scans = 0,
  -- 订阅多回波技术laser scan topics的个数
  num_multi_echo_laser_scans = 1,
  -- 分割雷达数据的个数
  num_subdivisions_per_laser_scan = 10,
  -- 订阅的点云topics的个数
  num_point_clouds = 0,
  -- 使用tf2查找变换的超时秒数
  lookup_transform_timeout_sec = 0.2,
  -- 发布submap的周期间隔
  submap_publish_period_sec = 0.3,
  -- 发布姿态的周期间隔
  pose_publish_period_sec = 5e-3,
  -- 轨迹发布周期间隔
  trajectory_publish_period_sec = 30e-3,
  -- 测距仪的采样率
  rangefinder_sampling_ratio = 1.,
  --里程记数据采样率
  odometry_sampling_ratio = 1.,
  -- 固定的frame位姿采样率
  fixed_frame_pose_sampling_ratio = 1.,
  -- IMU数据采样率
  imu_sampling_ratio = 1.,
  -- 路标采样率
  landmarks_sampling_ratio = 1.,
}
