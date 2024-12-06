#!/bin/bash

reboot_needed=0
script_run_url_new=$1
task_id=$2
load_run=$3
checkpoint=$4
conda_env=$5

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

conda_activate_pointfoot_legged_gym() {
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

    # Activate the newly created environment
    info "${yellow}激活 Conda 环境 $conda_env ..."
    conda activate $conda_env
    check_err "${yellow}激活 Conda 环境 $conda_env 失败"
}

rerun_task() {
    project_name=$(echo $script_run_url_new | cut -d'/' -f1)
    info "${yellow} - 激活 $conda_env 的conda环境"

    sleep 3

    conda_activate_pointfoot_legged_gym

    local rl_dir="$HOME/limx_rl/$task_id"
    cd $rl_dir

    # 无头模式下继续训练
    cd "$rl_dir/$project_name"
    info "$rl_dir/$project_name"
    #python legged_gym/scripts/train.py --task=pointfoot_rough --headless --load_run $load_run --checkpoint $checkpoint
    pid_file="$rl_dir/xunlian_pids.txt"
    nohup python $script_run_url_new $run_params --task_id=$task_id --headless --load_run $load_run --checkpoint $checkpoint > ./pointfoot_legged_gym_output.log 2>&1 & echo $! > $pid_file
    check_err "${yellow}运行失败"
    info "${yellow}运行成功"
}

rerun_task


