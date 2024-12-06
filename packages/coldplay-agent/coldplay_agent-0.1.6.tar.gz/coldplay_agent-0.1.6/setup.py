from setuptools import setup, find_packages

setup(
    name='coldplay_agent',  # 包名
    version='0.1.6',    # 版本号
    description='coldplay agent package',  # 简短描述
    author='Joey',
    author_email='joeym@limxdynamics.com',
    url='https://github.com/zoie438730732/limx-coldplay-agent',  # 项目主页链接
    packages=find_packages(),  # 自动发现包
    include_package_data=True,  # 这一行确保 package_data 会生效
    package_data={
        '': ['scripts/*.sh'],  # 包含所有脚本文件
    },
    install_requires=[  # 依赖包
        'pika==1.3.2',
        'requests==2.31.0'
    ],
    entry_points={
        'console_scripts': [
            'coldplayagent = app.main:main',  # 指定入口函数
            'coldplayagent-init = app.init:initialize',  # 创建初始化命令
        ],
    },
    classifiers=[  # 分类标记
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # 支持的Python版本
)
