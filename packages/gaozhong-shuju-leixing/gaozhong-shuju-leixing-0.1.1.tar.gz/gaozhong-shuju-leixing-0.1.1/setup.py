from setuptools import setup, find_packages

setup(
    name='gaozhong-shuju-leixing',  # 在PyPI上发布的包名，需唯一
    version='0.1.1',  # 初始版本号
    author='Your Name',
    author_email='your.email@example.com',
    description='A collection of fundamental data structures implemented in Python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your-repo',  # 如果有，提供GitHub仓库URL
    py_modules=['gz'],  # 包含的模块
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 支持的Python版本
    install_requires=[
        # 如果有依赖包，在此处列出
    ],
)
