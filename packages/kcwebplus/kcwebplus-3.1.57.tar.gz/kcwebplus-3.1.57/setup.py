
# 打包上传 python setup.py sdist upload
# 打包并安装 python setup.py sdist install
#############################################
import os,sys
from setuptools import setup, find_packages,Extension
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, current_dir)
from kcwebplus.config import kcwebplus
confkcw={}
confkcw['name']=kcwebplus['name']                             #项目的名称 
confkcw['version']=kcwebplus['version']							#项目版本
confkcw['description']=kcwebplus['description']       #项目的简单描述
confkcw['long_description']=kcwebplus['long_description']     #项目详细描述
confkcw['license']=kcwebplus['license']                    #开源协议   mit开源
confkcw['url']=kcwebplus['url']
confkcw['author']=kcwebplus['author']  					 #名字
confkcw['author_email']=kcwebplus['author_email'] 	     #邮件地址
confkcw['maintainer']=kcwebplus['maintainer'] 						 #维护人员的名字
confkcw['maintainer_email']=kcwebplus['maintainer_email']    #维护人员的邮件地址
def get_file(folder='./',lists=[]):
    lis=os.listdir(folder)
    for files in lis:
        if not os.path.isfile(folder+"/"+files):
            if files=='__pycache__' or files=='.git':
                pass
            else:
                lists.append(folder+"/"+files)
                get_file(folder+"/"+files,lists)
        else:
            pass
    return lists
b=get_file("kcwebplus",['kcwebplus'])
setup(
    name = confkcw["name"],
    version = confkcw["version"],
    keywords = "kcwebplus"+confkcw['version'],
    description = confkcw["description"],
    long_description = confkcw["long_description"],
    license = confkcw["license"],
    author = confkcw["author"],
    author_email = confkcw["author_email"],
    maintainer = confkcw["maintainer"],
    maintainer_email = confkcw["maintainer_email"],
    url=confkcw['url'],
    packages =  b,
    install_requires = ['kcweb==6.4.8','pyOpenSSL==23.2.0','cryptography==41.0.7','chardet==4.0.0','apscheduler==3.6.3','pillow>=10.0.0','oss2>=2.12.1','websocket-client==1.3.1'], #第三方包 'pyOpenSSL==23.2.0','cryptography==41.0.7'
    package_data = {
        '': ['*.html', '*.js','*.css','*.jpg','*.png','*.gif','server.bat','server.sh','*sqlite/app','*sqlite/index_index'],
    },
    entry_points = {
        'console_scripts':[
            'kcwebplus = kcwebplus.kcwebplus:cill_start'
        ]
    }
)