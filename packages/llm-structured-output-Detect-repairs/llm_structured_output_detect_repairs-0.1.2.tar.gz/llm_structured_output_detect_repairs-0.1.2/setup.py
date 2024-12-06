# setup.py

from setuptools import setup, find_packages

setup(
    name="llm_structured_output_Detect_repairs",
    version="0.1.2",
    author="jiayanfeng",
    author_email="jyf_bit@163.com",
    description="一个简单的HTTP客户端库，用于与结构化输出API交互",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/lfl_llm_agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'langchain',
        'openai',
    ],
)