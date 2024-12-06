#!/bin/bash

reboot_needed=0
task_id=$1
verify_code_type=$2
code_file_uri=$3
pointfoot_repo=$4
start_script=$5
policy_source=$6
operating_verify_env=$7
robot_type=$8
visual_tools=$9
police_info=$10

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

conda_deactivate(){
    local anaconda_dir="$HOME/anaconda3"

    __conda_setup="$('$anaconda_dir/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        # Use eval to apply Conda setup if successful
        eval "$__conda_setup"
    else
        if [ -f "$anaconda_dir/etc/profile.d/conda.sh" ]; then
            # Source the conda.sh script if it exists
            . "$anaconda_dir/etc/profile.d/conda.sh"
        else
            # Fallback to adding Conda to PATH if other methods fail
            export PATH="$anaconda_dir/bin:$PATH"
        fi
    fi
    unset __conda_setup

    info "${yellow}退出 Conda 环境"
    conda deactivate
    check_err "${yellow}退出 Conda 环境失败"
}

update_robot_type(){
    ROBOT_TYPE="$robot_type"
    BASHRC_FILE="$HOME/.bashrc"

    if grep -q '^export ROBOT_TYPE=' "$BASHRC_FILE"; then
        sed -i "s/^export ROBOT_TYPE=.*/export ROBOT_TYPE=$ROBOT_TYPE/" "$BASHRC_FILE"
        info "修改 ROBOT_TYPE $ROBOT_TYPE 文件 $BASHRC_FILE."
    else
        echo "export ROBOT_TYPE=$ROBOT_TYPE" >> "$BASHRC_FILE"
        info "添加 ROBOT_TYPE $ROBOT_TYPE 文件 $BASHRC_FILE."
    fi

    # Reload .bashrc
    source "$BASHRC_FILE"
    info "${yellow}ROBOT_TYPE $ROBOT_TYPE 添加到 $BASHRC_FILE."

}

gazebo_env_init(){
    info "${yellow}开始安装初始化Gazebo环境"
    conda_deactivate

    sleep 3
    local ws_src="$ws_dir/src"
    mkdir -p "$ws_src"
    # 定义项目列表，每个项目包含目标目录和Git仓库地址
    local projects=(
        "$ws_src/pointfoot-sdk-lowlevel https://github.com/limxdynamics/pointfoot-sdk-lowlevel.git"
        "$ws_src/pointfoot-gazebo-ros https://github.com/limxdynamics/pointfoot-gazebo-ros.git"
        "$ws_src/robot-description https://github.com/limxdynamics/robot-description.git"
        "$ws_src/robot-visualization https://github.com/limxdynamics/robot-visualization.git"
        "$ws_src/robot-joystick https://github.com/limxdynamics/robot-joystick.git"
    )

    # 循环检查每个项目
    for project in "${projects[@]}"; do
        # 分离目标目录和Git仓库地址
        project_dir=$(echo "$project" | awk '{print $1}')
        git_url=$(echo "$project" | awk '{print $2}')

        # 检查目录是否存在
        if [ -d "$project_dir" ]; then
            info "${green}目录 $project_dir 已存在，跳过下载。"
        else
            # 创建目标目录并下载Git仓库
            mkdir -p "$(dirname "$project_dir")"
            git clone "$git_url" "$project_dir"
        fi
    done

    cd "$ws_dir"
    catkin_make install
    source install/setup.bash
    check_err "${yellow}初始化Gazebo环境失败"
    info "${yellow}初始化Gazebo环境成功"
}

mogico_env_init(){
    conda_deactivate
    # 下载 MuJoCo 仿真器
    mujoco_dir="$ws_dir/pointfoot-mujoco-sim"
    if [ -d "$mujoco_dir" ]; then
        info "${yellow}MuJoCo 仿真器已存在，跳过下载"
    else
        echo "下载 MuJoCo 仿真器..."
        git clone --recurse https://github.com/limxdynamics/pointfoot-mujoco-sim.git "$mujoco_dir"
        info "${yellow}MuJoCo 仿真器下载完成"
    fi

}


install_rl_deploy_with_python_demo(){
    conda_deactivate
    local task_dir="$ws_dir/task"

    # 创建工作目录
    mkdir -p "$task_dir"
    echo "工作目录已创建：$task_dir"

    # 下载部署实现
    echo "准备下载部署实现..."
    mkdir -p "$task_dir"
    # 检查 $task_dir 目录下是否有文件夹
    if [ "$(ls -A "$task_dir")" ]; then
        info "${yellow}目录中已有内容，清空目录..."
        rm -rf "$task_dir"/*
    fi
    cd "$task_dir"
    echo "下载新的部署实现代码..."
    # git clone https://github.com/limxdynamics/rl-deploy-with-python.git
    git clone "$pointfoot_repo"
    info "${yellow}部署实现下载完成"
    last_folder=$(ls -d */ | tail -n 1)
    last_folder_name=${last_folder%/}

    # 检查系统架构并安装运动控制开发库
    if pip show limxsdk > /dev/null 2>&1; then
        info "${yellow}limxsdk 已安装，跳过安装"
    else
        architecture=$(uname -m)
        if [ "$architecture" == "x86_64" ]; then
            echo "检测到 Linux x86_64 环境，安装 x86_64 版本的运动控制开发库..."
            pip install "$task_dir/$last_folder_name/python3/amd64/limxsdk-*-py3-none-any.whl"
        elif [ "$architecture" == "aarch64" ]; then
            echo "检测到 Linux aarch64 环境，安装 aarch64 版本的运动控制开发库..."
            pip install "$task_dir/$last_folder_name/python3/aarch64/limxsdk-*-py3-none-any.whl"
        else
            info "${yellow}未识别的系统架构: $architecture"
            exit 1
        fi
    fi

    info "${yellow}运动控制开发库安装完成"
}

install_rl_deploy_with_python_file(){
    conda_deactivate
    local task_dir="$ws_dir/task"

    # 创建工作目录
    mkdir -p "$task_dir"
    echo "工作目录已创建：$task_dir"

    # 下载部署实现
    echo "准备下载部署实现..."
    mkdir -p "$task_dir"
    # 检查 $task_dir 目录下是否有文件夹
    if [ "$(ls -A "$task_dir")" ]; then
        info "${yellow}目录中已有内容，清空目录..."
        rm -rf "$task_dir"/*
    fi
    cd "$task_dir"
    echo "下载新的部署实现代码..."
    # git clone https://github.com/limxdynamics/rl-deploy-with-python.git

    folder_name=$(echo "$pointfoot_repo" | sed -E 's|.*/([^/]+)_.*\.zip.*|\1|')
    filename="$folder_name.zip"
    wget -O $filename "$pointfoot_repo"
    unzip -o "$rl_dir/$filename"
    #mac环境压缩会多出这一部分，删除掉
    if [ -d "$rl_dir/__MACOSX" ]; then
        rm -rf "$rl_dir/__MACOSX"
        info "已删除目录 $rl_dir/__MACOSX"
    fi
    rm -rf "$rl_dir/$filename"

    info "${yellow}部署实现下载完成"
    last_folder=$(ls -d */ | tail -n 1)
    last_folder_name=${last_folder%/}

    # 检查系统架构并安装运动控制开发库
    if pip show limxsdk > /dev/null 2>&1; then
        info "${yellow}limxsdk 已安装，跳过安装"
    else
        architecture=$(uname -m)
        if [ "$architecture" == "x86_64" ]; then
            echo "检测到 Linux x86_64 环境，安装 x86_64 版本的运动控制开发库..."
            pip install "$task_dir/$last_folder_name/python3/amd64/limxsdk-*-py3-none-any.whl"
        elif [ "$architecture" == "aarch64" ]; then
            echo "检测到 Linux aarch64 环境，安装 aarch64 版本的运动控制开发库..."
            pip install "$task_dir/$last_folder_name/python3/aarch64/limxsdk-*-py3-none-any.whl"
        else
            info "${yellow}未识别的系统架构: $architecture"
            exit 1
        fi
    fi

    info "${yellow}运动控制开发库安装完成"
}

install_rl_deploy_ros_cpp() {
    conda_deactivate
    info "${yellow}开始安装rl-deploy-ros-cpp..."

    sleep 3

    local ws_src="$ws_dir/src"

    mkdir -p "$ws_src"

    # Install rl-deploy-ros-cpp
    info "${yellow}安装 rl-deploy-ros-cpp 库 ..."
    cd $ws_src
    info "wget:$pointfoot_repo"
    filename=$(basename "$project_file_uri")
    name_without_extension_filename="${filename%.*}"
    wget -O $filename "$pointfoot_repo"
    info "filename:$filename"
    #mac环境压缩会多出这一部分，删除掉
    if [ -d "$ws_src/__MACOSX" ]; then
        rm -rf "$ws_src/__MACOSX"
        info "已删除目录 $ws_src/__MACOSX"
    else
        info "目录 $ws_src/__MACOSX 不存在"
    fi
    # if [ ! -d "$ws_dir/pointfoot-legged-gym" ]; then
    #     unzip "$ws_dir/$filename"
    # else
    #     tar -czf "$back_dir/pointfoot-legged-gym-$(date +%Y%m%d%H%M%S).tar.gz" $ws_dir/pointfoot-legged-gym
    #     rm -rf "$ws_dir/pointfoot-legged-gym"
    #     unzip "$ws_dir/$filename"
    # fi
    unzip -o "$ws_src/$filename"
    rm -rf "$ws_src/$filename"
    
    last_folder=$(ls -d */ | tail -n 1)
    last_folder_name=${last_folder%/}

    cd "$ws_src/$last_folder_name"
    pip install -e .
    check_err "${yellow}安装 rl-deploy-ros-cpp 库失败"
    info "${yellow}安装 rl-deploy-ros-cpp 库成功"
}

install_rl_deploy_ros_cpp_from_git_demo() {
    conda_deactivate
    info "${yellow}开始安装rl-deploy-ros-cpp..."

    local rl_dir="$ws_dir/src/task"

    mkdir -p "$rl_dir"

    # Install rl-deploy-ros-cpp git clone https://github.com/limxdynamics/rl-deploy-ros-cpp.git
    info "${yellow}安装 rl-deploy-ros-cpp 库 ..."
    cd $rl_dir
    info "rl_dir:$rl_dir"
    # 检查 $rl_dir 目录下是否有文件夹
    if [ "$(ls -A "$rl_dir")" ]; then
        info "${yellow}目录中已有内容，清空目录..."
        rm -rf "$rl_dir"/*
    fi

    info "${yellow}安装 rl-deploy-ros-cpp 库..."
    git clone "$pointfoot_repo"

    cd "$ws_dir"
    catkin_make install
    source install/setup.bash
    check_err "${yellow}安装 rl-deploy-ros-cpp 库失败"
    info "${yellow}安装 rl-deploy-ros-cpp 库成功"
}

run_mujoco(){
    sleep 3
    conda_deactivate
    info "${yellow}开始运行 mujoco..."

    # 后台运行 MuJoCo，并记录进程ID
    python3 $ws_dir/pointfoot-mujoco-sim/simulator.py & MUJOCO_PID=$!
    info "${yellow}mujoco 进程已启动，PID: $MUJOCO_PID"

    echo "MUJOCO_PID=$MUJOCO_PID" >> "$pid_file"
    info "${yellow}mujoco进程ID已记录到文件 $pid_file"
}

run_gazebo(){
    sleep 3
    conda_deactivate
    info "${yellow}开始运行 gazebo..."

    # 后台运行 gazebo，并记录进程ID
    cd "$ws_dir" || { echo "工作目录不存在: $ws_dir"; return 1; }
    roslaunch pointfoot_gazebo empty_world.launch & GAZEBO_PID=$!
    info "${yellow}gazebo 进程已启动，PID: $GAZEBO_PID"

    echo "GAZEBO_PID=$GAZEBO_PID" >> "$pid_file"
    info "${yellow}gazebo进程ID已记录到文件 $pid_file"
}

run_plotjugler(){
    sleep 3
    conda_deactivate
    info "${yellow}开始运行 Plotjugler..."

    # 后台运行 Plotjugler ，并记录进程ID
    cd "$ws_dir" || { echo "工作目录不存在: $ws_dir"; return 1; }
    #roslaunch robot_visualization pointfoot_plot_sim.launch
    roslaunch robot_visualization pointfoot_plot_sim.launch & PLOTJUGLER_PID=$!
    info "${yellow} Plotjugler 进程已启动，PID: $PLOTJUGLER_PID"

    echo "PLOTJUGLER_PID=$PLOTJUGLER_PID" >> "$pid_file"
    info "${yellow}Plotjugler进程ID已记录到文件 $pid_file"
}

run_rviz(){
    sleep 3
    conda_deactivate
    info "${yellow}开始运行 RViz..."

    # 后台运行 RViz ，并记录进程ID
    cd "$ws_dir" || { echo "工作目录不存在: $ws_dir"; return 1; }
    #roslaunch robot_visualization pointfoot_rviz_hw.launch
    roslaunch robot_visualization pointfoot_rviz_sim.launch & RVIZ_PID=$!
    info "${yellow} RViz 进程已启动，PID: $RVIZ_PID"

    echo "RVIZ_PID=$RVIZ_PID" >> "$pid_file"
    info "${yellow}RViz进程ID已记录到文件 $pid_file"
}

run_robot_joystick(){
    sleep 3
    conda_deactivate
    info "${yellow}开始运行 robot-joystick..."

    # 后台运行 robot-joystick，并记录进程ID
    cd "$ws_dir"
    ./src/robot-joystick/robot-joystick & JOYSTICK_PID=$!
    info "${yellow}robot-joystick 进程已启动，PID: $JOYSTICK_PID"

    echo "JOYSTICK_PID=$JOYSTICK_PID" >> "$pid_file"
    info "${yellow}robot-joystick进程ID已记录到文件 $pid_file"
}

run_rl_deploy_with_python_demo(){
    conda_deactivate
    info "${yellow}开始运行 rl-deploy-with-python..."

    local task_dir="$ws_dir/task"

    cd "$ws_dir" || { echo "工作目录不存在: $ws_dir"; return 1; }

    # 后台运行 MuJoCo，并记录进程ID
    run_mujoco

    sleep 3
    cd "$task_dir"
    last_folder=$(ls -d */ | tail -n 1)
    last_folder_name=${last_folder%/}
    # python3 /home/yons/coldplay/limx_ws/task/rl-deploy-with-python/pointfoot_controller.py & CONTROLLER_PID=$!
    eval "$start_script"
    info "${yellow}controller 进程已启动，PID: $CONTROLLER_PID"
    cd "$ws_dir"

    # 后台运行 robot-joystick，并记录进程ID
    run_robot_joystick

    # 将进程ID写入文件
    echo "CONTROLLER_PID=$CONTROLLER_PID" >> "$pid_file"
    info "${yellow}进程ID已记录到文件 $pid_file"
}

run_rl_deploy_ros_cpp_demo() {
    conda_deactivate
    info "${yellow}开始运行 rl-deploy-ros-cpp..."

    # 后台运行 gazebo，并记录进程ID
    run_gazebo

    sleep 3
    # 后台运行 roslaunch，并记录进程ID
    # roslaunch robot_hw pointfoot_hw_sim.launch & ROSLAUNCH_PID=$!
    eval "$start_script"
    info "${yellow}roslaunch 进程已启动，PID: $ROSLAUNCH_PID"

    # 后台运行 robot-joystick，并记录进程ID
    run_robot_joystick

    # 将进程ID写入文件
    echo "ROSLAUNCH_PID=$ROSLAUNCH_PID" >> "$pid_file"
    info "${yellow}进程ID已记录到文件 $pid_file"
}

run_rl_deploy_with_python(){
    conda_deactivate
    info "${yellow}开始运行 python controller..."

    local task_dir="$ws_dir/task"

    cd "$ws_dir" || { echo "工作目录不存在: $ws_dir"; return 1; }

    sleep 3
    cd "$task_dir"
    last_folder=$(ls -d */ | tail -n 1)
    last_folder_name=${last_folder%/}
    # python3 /home/yons/coldplay/limx_ws/task/rl-deploy-with-python/pointfoot_controller.py & CONTROLLER_PID=$!
    eval "$start_script"
    info "${yellow}controller 进程已启动，PID: $CONTROLLER_PID"
    cd "$ws_dir"

    # 将进程ID写入文件
    echo "CONTROLLER_PID=$CONTROLLER_PID" >> "$pid_file"
    info "${yellow}进程ID已记录到文件 $pid_file"
}

run_rl_deploy_ros_cpp() {
    conda_deactivate
    info "${yellow}开始运行 ros controller..."

    sleep 3
    # 后台运行 roslaunch，并记录进程ID
    # roslaunch robot_hw pointfoot_hw_sim.launch & ROSLAUNCH_PID=$!
    eval "$start_script"
    info "${yellow}roslaunch 进程已启动，PID: $ROSLAUNCH_PID"

    # 将进程ID写入文件
    echo "ROSLAUNCH_PID=$ROSLAUNCH_PID" >> "$pid_file"
    info "${yellow}进程ID已记录到文件 $pid_file"
}

#初始化gazebo环境
gazebo_env_init
#初始化mojoco环境
mogico_env_init
#选择机器人型号
update_robot_type

if [ "$verify_code_type" -eq "0" ]; then
    if [ "$operating_verify_env" -eq "1" ]; then
        # 如果operating_verify_env为1且verify_code_type为0，官方示例gazebo验证环境，执行以下命令
        install_rl_deploy_ros_cpp_from_git_demo
        run_rl_deploy_ros_cpp_demo
    elif [ "$operating_verify_env" -eq "2" ]; then
        # 如果operating_verify_env为2且verify_code_type为0，官方示例MuJoCo验证环境，执行以下命令
        install_rl_deploy_with_python_demo
        run_rl_deploy_with_python_demo
    else
        info "${yellow}没有匹配的条件，未执行任何仿真验证环境启动操作"
    fi
elif [ "$verify_code_type" -eq "1" ]; then
    # 安装上传代码
    install_rl_deploy_with_python_file
    if [ "$operating_verify_env" -eq "1" ]; then
        # 如果operating_verify_env为1且verify_code_type为1，本地上传gazebo验证环境,执行以下命令
        run_gazebo
    elif [ "$operating_verify_env" -eq "2" ]; then
        # 如果operating_verify_env为2且verify_code_type为1，本地上传MuJoCo验证环境,执行以下命令
        run_mujoco
    else
        info "${yellow}没有匹配的条件，未执行任何仿真验证环境启动操作"
    fi
    # 运行本地python代码
    run_rl_deploy_with_python
    # 后台运行 robot-joystick，并记录进程ID
    run_robot_joystick
elif [ "$verify_code_type" -eq "2" ]; then
    # 如果verify_code_type为1且policy_source为1，部署版本gazebo验证环境,执行以下命令
    if [ "$operating_verify_env" -eq "1" ]; then
        # 如果operating_verify_env为1且verify_code_type为1，部署版本gazebo验证环境,执行以下命令
        run_gazebo
    elif [ "$operating_verify_env" -eq "2" ]; then
        # 如果operating_verify_env为2且verify_code_type为1，部署版本MuJoCo验证环境,执行以下命令
        run_mujoco
    else
        info "${yellow}没有匹配的条件，未执行任何仿真验证环境启动操作"
    fi
    # 运行本地ros1环境代码
    run_rl_deploy_ros_cpp
    # 后台运行 robot-joystick，并记录进程ID
    run_robot_joystick
else
    info "${yellow}没有匹配的条件"

fi

case "$visual_tools" in
    "1")
        run_plotjugler
        ;;
    "2")
        run_rviz
        ;;
    "1,2")
        run_plotjugler
        run_rviz
        ;;
    *)
        echo "Invalid value for visual_tools: $visual_tools"
        ;;
esac