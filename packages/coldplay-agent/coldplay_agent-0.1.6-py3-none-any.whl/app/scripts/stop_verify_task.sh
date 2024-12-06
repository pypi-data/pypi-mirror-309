#!/bin/bash

reboot_needed=0
task_id=$1
operating_verify_env=$2
verify_code_type=$3

# bash fonts colors
red='\e[31m'
yellow='\e[33m'
gray='\e[90m'
green='\e[92m'
blue='\e[94m'
magenta='\e[95m'
cyan='\e[96m'
none='\e[0m'
_red() { echo -e ${red}$@${none}; }
_blue() { echo -e ${blue}$@${none}; }
_cyan() { echo -e ${cyan}$@${none}; }
_green() { echo -e ${green}$@${none}; }
_yellow() { echo -e ${yellow}$@${none}; }
_magenta() { echo -e ${magenta}$@${none}; }
_red_bg() { echo -e "\e[41m$@${none}"; }

is_err=$(_red_bg 错误：)
is_warn=$(_red_bg 警告：)
is_info=$(_red_bg 提示：)

err() {
    echo -e "\n$is_err $@\n" && exit 1
}

warn() {
    echo -e "\n$is_warn $@\n"
}

info() {
    echo -e "\n$is_info $@\n"
}

check_err() {
    if [[ $? != 0 ]]; then echo -e "\n$is_err $@\n" && exit 1; fi
}

if [[ $(lsb_release -rs) != "20.04" || $(lsb_release -is) != "Ubuntu" || $(uname -m) != "x86_64" ]]; then
    err "仅支持 ${yellow}(Ubuntu 20.04 和 x86_64 架构)${none}"
fi

ws_dir="$HOME/coldplay/limx_ws"
pid_file="$ws_dir/rl_deploy_pids.txt"

# 关闭 MuJoCo 和 robot-joystick 进程的函数
stop_rl_deploy() {

    info "${yellow}停止 rl-deploy..."

    if [ -f "$pid_file" ]; then
        # 从文件中读取进程ID
        source "$pid_file"

        if [ -n "$MUJOCO_PID" ] && kill -0 "$MUJOCO_PID" 2>/dev/null; then
            kill "$MUJOCO_PID"
            info "${yellow}MuJoCo 进程已停止，PID: $MUJOCO_PID"
        else
            info "${yellow}MuJoCo 进程未运行或已停止"
        fi

        if [ -n "$GAZEBO_PID" ] && kill -0 "$GAZEBO_PID" 2>/dev/null; then
            kill "$GAZEBO_PID"
            info "${yellow}GAZEBO 进程已停止，PID: $GAZEBO_PID"
        else
            info "${yellow}GAZEBO 进程未运行或已停止"
        fi

        if [ -n "$CONTROLLER_PID" ] && kill -0 "$CONTROLLER_PID" 2>/dev/null; then
            kill "$CONTROLLER_PID"
            info "${yellow}controller 进程已停止，PID: $CONTROLLER_PID"
        else
            info "${yellow}controller 进程未运行或已停止"
        fi

        if [ -n "$ROSLAUNCH_PID" ] && kill -0 "$ROSLAUNCH_PID" 2>/dev/null; then
            kill "$ROSLAUNCH_PID"
            info "${yellow}roslaunch 进程已停止，PID: $ROSLAUNCH_PID"
        else
            info "${yellow}roslaunch 进程未运行或已停止"
        fi

        if [ -n "$JOYSTICK_PID" ] && kill -0 "$JOYSTICK_PID" 2>/dev/null; then
            kill "$JOYSTICK_PID"
            info "${yellow}robot-joystick 进程已停止，PID: $JOYSTICK_PID"
        else
            info "${yellow}robot-joystick 进程未运行或已停止"
        fi

        if [ -n "$PLOTJUGLER_PID" ] && kill -0 "$PLOTJUGLER_PID" 2>/dev/null; then
            kill "$PLOTJUGLER_PID"
            info "${yellow}Plotjugler 进程已停止，PID: $PLOTJUGLER_PID"
        else
            info "${yellow}Plotjugler 进程未运行或已停止"
        fi

        if [ -n "$RVIZ_PID" ] && kill -0 "$RVIZ_PID" 2>/dev/null; then
            kill "$RVIZ_PID"
            info "${yellow}RViz 进程已停止，PID: $RVIZ_PID"
        else
            info "${yellow}RViz 进程未运行或已停止"
        fi

        # 删除PID文件
        rm -f "$pid_file"
        info "${yellow}PID文件已删除：$pid_file"
    else
        info "${yellow}未找到PID文件：$pid_file"
    fi
}
# 关闭 roslaunch 和 robot-joystick 进程的函数
# stop_rl_deploy_ros_cpp() {

#     info "${yellow}停止 rl-deploy-ros-cpp..."

#     if [ -f "$pid_file" ]; then
#         # 从文件中读取进程ID
#         source "$pid_file"

#         if [ -n "$GAZEBO_PID" ] && kill -0 "$GAZEBO_PID" 2>/dev/null; then
#             kill "$GAZEBO_PID"
#             info "${yellow}GAZEBO 进程已停止，PID: $GAZEBO_PID"
#         else
#             info "${yellow}GAZEBO 进程未运行或已停止"
#         fi

#         if [ -n "$ROSLAUNCH_PID" ] && kill -0 "$ROSLAUNCH_PID" 2>/dev/null; then
#             kill "$ROSLAUNCH_PID"
#             info "${yellow}roslaunch 进程已停止，PID: $ROSLAUNCH_PID"
#         else
#             info "${yellow}roslaunch 进程未运行或已停止"
#         fi

#         if [ -n "$JOYSTICK_PID" ] && kill -0 "$JOYSTICK_PID" 2>/dev/null; then
#             kill "$JOYSTICK_PID"
#             info "${yellow}robot-joystick 进程已停止，PID: $JOYSTICK_PID"
#         else
#             info "${yellow}robot-joystick 进程未运行或已停止"
#         fi

#         # 删除PID文件
#         rm -f "$pid_file"
#         info "${yellow}PID文件已删除：$pid_file"
#     else
#         info "${yellow}未找到PID文件：$pid_file"
#     fi
# }
stop_rl_deploy

# if [ "$operating_verify_env" -eq "0" ] && [ "$verify_code_type" -eq "0" ]; then
#     # 如果verify_code_type为1且policy_source为1，执行以下命令
#     stop_rl_deploy_ros_cpp
# elif [ "$operating_verify_env" -eq "1" ] && [ "$verify_code_type" -eq "0" ]; then
#     # 如果verify_code_type为2且policy_source为1，执行以下命令
#     stop_rl_deploy_with_python
# else
#     echo "没有匹配的条件，未执行任何操作"
# fi

