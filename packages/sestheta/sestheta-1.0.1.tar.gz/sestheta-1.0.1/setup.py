import setuptools #导入setuptools打包工具
""" 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 """
setuptools.setup(
    name="sestheta", # 用自己的名替换其中的YOUR_USERNAME_
    version="1.0.1",    #包版本号，便于维护版本
    author="街角的猫_wjz",    #作者，可以写自己的姓名
    author_email="wjz-space@outlook.com",    #作者联系方式，可写自己的邮箱地址
    description="Quantitative research tool for social interpersonal relationships and psychology, achieving linear prediction through fitting analysis. Special thanks to Ericas, the theoretical proposer of this project.",#包的简述
    #long_description=long_description,    #包的详细介绍，一般在README.md文件内
    #long_description_content_type="text/markdown",
    url="https://space.bilibili.com/3493290083093446",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',    #对python的最低版本要求
)
