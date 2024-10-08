import sys
import os

# Path to your project
project_home = '/home/ec2-user/pioneer'
sys.path.insert(0, project_home)

# Set the virtual environment paths
python_home = '/home/ec2-user/miniconda3/envs/myenv'
sys.path.append(python_home)
sys.path.append(os.path.join(python_home, 'lib/python3.9/site-packages'))

# Set the PYTHONHOME and PYTHONPATH environment variables
os.environ['PYTHONHOME'] = python_home
os.environ['PYTHONPATH'] = os.path.join(python_home, 'lib/python3.9/site-packages')

# Import the Flask app
from dataquiz import app as application

