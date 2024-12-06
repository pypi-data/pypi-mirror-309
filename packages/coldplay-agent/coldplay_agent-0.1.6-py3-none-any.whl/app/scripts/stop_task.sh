#!/bin/bash

reboot_needed=0

script_run_url_new=$1
task_id=$2
run_params=$3

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
PID_FILE="./pointfoot_legged_gym_pid.log"

if [[ $(lsb_release -rs) != "20.04" || $(lsb_release -is) != "Ubuntu" || $(uname -m) != "x86_64" ]]; then
    err "仅支持 ${yellow}(Ubuntu 20.04 和 x86_64 架构)${none}"
fi

stop_task() {
    info "关闭训练"

    rl_dir="$HOME/limx_rl/$task_id"
    pid_file="$rl_dir/xunlian_pids.txt"
    info "${yellow}文件路径：$pid_file"
    cript_run_url_real=$(echo $script_run_url_new | cut -d'/' -f2-)
    # ps aux | grep "python $cript_run_url_real $run_params --task_id=$task_id" | grep -v grep | awk '{print $2}' | xargs kill -9
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        info "${yellow}PID $PID 正在关闭进程..."
        kill $PID 2>/dev/null
        if [ $? -eq 0 ]; then
            info "${yellow}关闭成功。"
            rm -f "$pid_file"
        else
            info "${yellow}关闭失败，进程不存在。"
        fi
    else
        info "${yellow}PID文件不存在。确定是否运行"
    fi

    check_err "${yellow}关闭失败"
    info "${yellow}关闭成功"
}

stop_task


