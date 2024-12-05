from setuptools import setup, find_packages

setup(
    name="ClassHoster",                      
    version="0.1.0",                        
    description="Host ANY Class", 
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    author="Conner Sommerfield",                     
    author_email="conner.sommerfield@gmail.com",  
    url="https://github.com/RepoFactory/ClassHoster",  
    packages=find_packages(where="src"),
    package_dir={"": "src"}, include_package_data=True,              
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'robot = classhoster.ROBOT:main',      
            'host =  classhoster.host_cls:main', 
        ],
    },
    python_requires=">=3.8",                
)


