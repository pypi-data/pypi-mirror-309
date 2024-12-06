#!/bin/bash

reboot_needed=0
pointfoot_repo=$1
script_run_url_new=$2
project_file_uri=$3
task_id=$4
code_type=$5
version_type=$6
version_name=$7
run_params=$8
conda_env=$9

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

# 检查 jq 是否已经安装
# if ! command -v jq &> /dev/null; then
#     info "${yellow}jq 未安装，正在安装..."
#     sudo apt-get update
#     sudo apt-get install -y jq
# else
#     info "${yellow}jq 已经安装，跳过安装步骤。"
# fi

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
    info "${yellow}激活 Conda 环境 $conda_env..."
    conda activate $conda_env
    check_err "${yellow}激活 Conda 环境 $conda_env失败"
}

isaacgym_env_init(){
    info "${yellow}开始安装初始化isaacgym环境"
    conda_activate_pointfoot_legged_gym

    sleep 3
    local rl_dir="$HOME/limx_rl/$task_id"
    mkdir -p "$rl_dir"
    wget http://10.0.10.13:9000/limx/env/IsaacGym_Preview_4_Package.tar.gz
    tar -xzvf ./IsaacGym_Preview_4_Package.tar.gz -C "$rl_dir"
    rm -rf ./IsaacGym_Preview_4_Package.tar.gz
    cd "$rl_dir/isaacgym/python"
    pip install -e .
    sed -i 's/np.float/float/' isaacgym/torch_utils.py
    check_err "${yellow}安装初始化isaacgym环境失败"
    cd "$rl_dir"
}

install_pointfoot_legged_gym() {
    project_name=$(echo $script_run_url_new | cut -d'/' -f1)
    info "${yellow}开始安装$project_name..."

    sleep 3

    conda_activate_pointfoot_legged_gym

    local rl_dir="$HOME/limx_rl/$task_id"
    local back_dir="$HOME/limx_rl/bak"

    mkdir -p "$rl_dir"
    mkdir -p "$back_dir"

    # Install pointfoot-legged-gym
    info "${yellow}安装 $project_name 库 ..."
    cd $rl_dir
    # 遍历 JSON 数组并提取字段
    info "pointfoot_repo:$pointfoot_repo"
    echo "$pointfoot_repo" | jq -c '.[]' | while read item; do
        # 提取 codeUrl 字段
        codeUrl=$(echo "$item" | jq -r '.codeUrl')
        # varsionType=$(echo "$item" | jq -r '.varsionType')
        # varsionName=$(echo "$item" | jq -r '.varsionName')
        info "wget:$codeUrl"
        folder_name=$(echo "$codeUrl" | sed -E 's|.*/([^/]+)_.*\.zip.*|\1|')
        # folder_name=$(echo "$codeUrl" | sed -E 's|.*/(rsl_rl[^/]+)\.zip.*|\1|')
        # folder_name=$(echo "$folder_name" | sed -E 's/_(?=[^_]+$)//g' | sed 's/\(.*\)_/\1/')
        filename="$folder_name.zip"
        wget -O $filename "$codeUrl"
        # unzip -o "$rl_dir/$filename"
        unzip -o "$rl_dir/$filename"
        # 获取解压后最新创建的文件夹名称
        # folder_name=$(ls -d "$rl_dir"/*/ | sort -n | tail -n 1 | xargs -n 1 basename)

        rm -rf "$rl_dir/$filename"
        #mac环境压缩会多出这一部分，删除掉
        if [ -d "$rl_dir/__MACOSX" ]; then
            rm -rf "$rl_dir/__MACOSX"
            info "已删除目录 $rl_dir/__MACOSX"
        else
            info "目录 $rl_dir/__MACOSX 不存在"
        fi
        # info "进入目录 $folder_name 执行 pip install -e ."
        # cd "$rl_dir/$folder_name"
        # pip install -e .
        # cd "$rl_dir"
        # check_err "${yellow}安装 $folder_name 库失败"
        # info "${yellow}安装 $folder_name 库成功"
        # sleep 3
    done
    # info "wget:$pointfoot_repo"
    # filename=$(basename "$project_file_uri")
    # name_without_extension_filename="${filename%.*}"
    # wget -O $filename "$pointfoot_repo"
    # info "filename:$filename"
    # #mac环境压缩会多出这一部分，删除掉
    # if [ -d "$rl_dir/__MACOSX" ]; then
    #     rm -rf "$rl_dir/__MACOSX"
    #     info "已删除目录 $rl_dir/__MACOSX"
    # else
    #     info "目录 $rl_dir/__MACOSX 不存在"
    # fi
    # if [ ! -d "$rl_dir/pointfoot-legged-gym" ]; then
    #     unzip "$rl_dir/$filename"
    # else
    #     tar -czf "$back_dir/pointfoot-legged-gym-$(date +%Y%m%d%H%M%S).tar.gz" $rl_dir/pointfoot-legged-gym
    #     rm -rf "$rl_dir/pointfoot-legged-gym"
    #     unzip "$rl_dir/$filename"
    # fi
    # unzip -o "$rl_dir/$filename"
    # rm -rf "$rl_dir/$filename"
    
    # last_folder=$(ls -d */ | tail -n 1)
    # last_folder_name=${last_folder%/}

    # 遍历$rl_dir 下的所有文件夹，进入每个文件夹并执行 pip install -e .
    for folder in "$rl_dir"/*/; do
        # 确保是文件夹
        if [ -d "$folder" ]; then
            info "进入目录 $folder 执行 pip install -e ."
            cd "$folder"
            pip install -e .
            check_err "${yellow}安装 $folder 库失败"
            info "${yellow}安装 $folder 库成功"
        fi
    done

    # info " 切换目录 $rl_dir/$project_name"
    # cd "$rl_dir/$project_name"
    # pip install -e .
    # check_err "${yellow}安装 $project_name 库失败"
    # info "${yellow}安装 $project_name 库成功"
}


install_pointfoot_legged_gym_from_git() {
    project_name=$(echo $script_run_url_new | cut -d'/' -f1)
    info "${yellow}开始安装$project_name..."

    sleep 3

    conda_activate_pointfoot_legged_gym

    local conda_env="pointfoot_legged_gym"
    local rl_dir="$HOME/limx_rl/$task_id"
    local back_dir="$HOME/limx_rl/bak"

    mkdir -p "$rl_dir"
    mkdir -p "$back_dir"

    # Install pointfoot-legged-gym
    info "${yellow}安装 $project_name 库 ..."
    cd $rl_dir
    if [ ! -d "$rl_dir/$project_name" ]; then
        # 遍历 JSON 数组并提取字段
        echo "$pointfoot_repo" | jq -c '.[]' | while read item; do
            # 提取 codeUrl 字段
            codeUrl=$(echo "$item" | jq -r '.codeUrl')
            varsionType=$(echo "$item" | jq -r '.varsionType')
            varsionName=$(echo "$item" | jq -r '.varsionName')
            repo_name=$(basename -s .git "$codeUrl")
            info "wget:$codeUrl"
            if [ "$version_type" == "1" ]; then
                #分支
                git clone -b $version_name "$codeUrl"
            elif [ "$version_type" == "2" ]; then
                #提交
                git clone "$codeUrl"
                # last_folder1=$(ls -d */ | tail -n 1)
                # last_folder_name1=${last_folder1%/}
                # 从 URL 中提取项目名（去掉前缀部分）
                cd "$rl_dir/$repo_name"
                git checkout $version_name
                cd "$rl_dir"
            else
                #tag
                git clone "$codeUrl"
                # last_folder1=$(ls -d */ | tail -n 1)
                # last_folder_name1=${last_folder1%/}
                cd "$rl_dir/$repo_name"
                git checkout $version_name
                cd "$rl_dir"
            fi
            cd "$rl_dir/$repo_name"
            pip install -e .
            cd "$rl_dir"
            check_err "${yellow}安装 $repo_name 库失败"
            info "${yellow}安装 $repo_name 库成功"
        done
        
    fi
}

run_task() {
    project_name=$(echo $script_run_url_new | cut -d'/' -f1)
    info "${yellow} - 激活 $conda_env 的conda环境"

    sleep 3

    conda_activate_pointfoot_legged_gym

    local conda_env="pointfoot_legged_gym"
    local rl_dir="$HOME/limx_rl/$task_id"
    cd $rl_dir
    # last_folder=$(ls -d */ | tail -n 1)
    # last_folder_name=${last_folder%/}

    # 无头模式下继续训练
    cd "$rl_dir/$project_name"
    info "$rl_dir/$project_name"
    #python legged_gym/scripts/train.py --task=pointfoot_rough --headless
    cript_run_url_real=$(echo $script_run_url_new | cut -d'/' -f2-)
    # nohup python $cript_run_url_real $run_params --task_id=$task_id --headless > ./pointfoot_legged_gym_output.log 2>&1 &
    pid_file="$rl_dir/xunlian_pids.txt"
    nohup python $cript_run_url_real $run_params --task_id=$task_id --headless > ./pointfoot_legged_gym_output.log 2>&1 & echo $! > $pid_file

    check_err "${yellow}运行失败"
    info "${yellow}运行成功"
}

del_task(){
    local rl_dir="$HOME/limx_rl"
    # 删除以 TASK_ 开头的所有文件夹
    find "$rl_dir" -type d -name "TASK_*" -exec rm -rf {} +
}

# 根据code_type判断执行哪个安装函数 如果为1则代码安装 如果为2则git安装
info "code_type：${code_type}"
if [ "$code_type" == "1" ]; then
    info "${yellow}删除之前的task "
    del_task
    info "${yellow}压缩包安装 "
    # isaacgym_env_init
    install_pointfoot_legged_gym
elif [ "$code_type" == "2" ]; then
    info "${yellow}删除之前的task "
    del_task
    info "${yellow}git安装 "
    # isaacgym_env_init
    install_pointfoot_legged_gym_from_git
else
    err "无效的code_type: $code_type"
fi

run_task


