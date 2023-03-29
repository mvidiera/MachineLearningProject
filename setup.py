from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='MelissaVidiera',
author_email='melissavidiera5@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)


'''from setuptools import find_packages,setup #find all packages
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    
    This funtion will return the list of reqirements
    
    requirements=[]
    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        #when I use readlines() \n will be automatically added, as i am installing packages \n doesnt work for next package
        # to avoid this I am using list comprehension where I replace \n with space
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

#it is more like metadata info about project
setup(
name= 'MachineLearningProject',
version= "0.0.1",
author= "MelissaVidiera",
author_email= "melissavidiera5@gmail.com",
# finds packages automatically
packages= find_packages(),
#basic libearies that needs to be installed
install_requires=get_requirements('requirements.txt')
)
'''