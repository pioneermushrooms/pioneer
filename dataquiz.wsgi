
import sys
import os
from dataquiz import app as application  # Replace 'app' with the name of your main Flask file, if different

# Add the project directory to the system path
sys.path.insert(0, '/home/ec2-user/pioneer')

if __name__ == "__main__":
    application.run()

