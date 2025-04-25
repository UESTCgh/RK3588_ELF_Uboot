-- 是否使用IMU数据
use_imu_data = true, 
-- 深度数据最小范围
min_range = 0.,
-- 深度数据最大范围
max_range = 30.,
-- 传感器数据超出有效范围最大值时，按此值来处理
missing_data_ray_length = 5.,
-- 是否使用实时回环检测来进行前端的扫描匹配
use_online_correlative_scan_matching = true
-- 运动过滤，检测运动变化，避免机器人静止时插入数据
motion_filter.max_angle_radians
