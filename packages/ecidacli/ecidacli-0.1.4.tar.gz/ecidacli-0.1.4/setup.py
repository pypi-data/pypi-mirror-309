import setuptools
with open("README.md", "r") as fh:
   long_description = fh.read()
   
setuptools.setup(
   name='ecidacli',
   version='0.1.4',
   author="Mostafa Hadadian",
   author_email="hadadian@caidel.com",
   description="The ECiDA-CLI for python to make things easier",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://gitlab.com/ecida",
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
   ],
   py_modules=['ecidacli', 'docker_interface'],
   install_requires=[
      'pyyaml',
      'importlib-metadata',
      'packaging',
      'kafka-python',
      'requests',      
      # 'importlib-metadata ; python_version<"3.8"'
   ],
   entry_points={
      'console_scripts': [
         'ecidacli=ecidacli:main',
      ],
   },
)