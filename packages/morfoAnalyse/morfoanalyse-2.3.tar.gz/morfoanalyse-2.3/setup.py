import setuptools

setuptools.setup(
   name='morfoAnalyse',
   version='2.3',
   author='Alisher Ismailov Shakirovich',
   author_email='alisherismailov1991@gmail.com',
   description='''This package is desgined to help researcher to find stem of the word and 
   analyse the remaining suffixes. package has 4 input parameter, 1-parameter is input word and 2-parameter is list of stem lecixon
   3-parameter is list Noun suffixes, 4-parameter is list of VERB parameter. 2,3,4 parameter must dictionary''',
   packages=setuptools.find_packages(),
   license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)