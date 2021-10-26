# This is a base config file which contains base_dir, driver path and so on!
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = os.path.join(base_dir , r"config/config.ini")


template_group_2 = os.path.join(base_dir,r"utils/compare/template/template")
picture_type="bar"

