from setuptools import setup, find_packages

setup(
    name='lpslabtools',  # 包名称
    version='0.1.0',  # 版本号
    packages=find_packages(),  # 自动发现包
    install_requires=[  # 依赖的其他包  
        # 如果没有其他依赖，可以保留为空列表   
    ],
    description='A tool to processing  spectrometer file in LPS-LENP',  # 简短描述
    long_description=open('README.md', encoding='utf-8').read(),  # 详细描述
    long_description_content_type='text/markdown',  # README 的格式
    author='HETAO',  # 作者
    author_email='2300566779@qq.com',  # 作者邮箱
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',  # 许可证信息
)
