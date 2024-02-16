# -*- coding:utf-8 -*-
import os
import sys
import paramiko
from PyQt5.QtWidgets import QDesktopWidget,QApplication, QAction,QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox
class SSHWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.width=660
            self.height=600
            screen=QDesktopWidget().screenGeometry()
            self.top = int((screen.width() - self.width) / 2)
            self.left = int((screen.height() - self.height) / 2)
            self.setWindowTitle("远程连接工具")
            self.setGeometry(self.top, self.left,self.width,self.height)
            main_widget=QWidget(self)
            main_layout=QVBoxLayout()
            main_widget.setLayout(main_layout)
            self.setCentralWidget(main_widget)
            # 创建连接信息输入框
            connect_widget = QWidget(self)
            connect_layout = QVBoxLayout()
            connect_widget.setLayout(connect_layout)
            main_layout.addWidget(connect_widget)

            menu = self.menuBar()
            # 如果是Mac的话，菜单栏不会在Window中显示而是屏幕顶部系统菜单栏位置
            # 下面这一行代码使得Mac也按照Windows的那种方式在Window中显示Menu
            menu.setNativeMenuBar(False)
            file_menu = menu.addMenu("文件")
            uploadfiles=QAction("上传文件",self)
            downloadfiles=QAction("下载文件",self)
            quitapp = QAction("退出", self)
            uploadfiles.setShortcut("Ctrl + U")
            uploadfiles.setShortcut("Ctrl + D")
            file_menu.addAction(uploadfiles)
            file_menu.addAction(downloadfiles)
            file_menu.addAction(quitapp)
            uploadfiles.triggered.connect(self.upload_file)
            quitapp.triggered.connect(self.close)
            downloadfiles.triggered.connect(self.download_file)
            About_menu = menu.addMenu("关于")
            About_menu.addAction("关于我们")
            About_menu.triggered.connect(self.aboutus)
            host_layout=QHBoxLayout()
            host_label=QLabel('主机：')
            self.host_Edit= QLineEdit()
            host_layout.addWidget(host_label)
            host_layout.addWidget(self.host_Edit)
            connect_layout.addLayout(host_layout)

            port_layout=QHBoxLayout()
            port_label=QLabel('端口：')
            self.port_Edit=QLineEdit()
            self.port_Edit.setText("22")
            port_layout.addWidget(port_label)
            port_layout.addWidget(self.port_Edit)
            connect_layout.addLayout(port_layout)

            user_layout=QHBoxLayout()
            user_label=QLabel("用户名：")
            self.userEidt=QLineEdit()
            user_layout.addWidget(user_label)
            user_layout.addWidget(self.userEidt)
            connect_layout.addLayout(user_layout)

            passwd_layout=QHBoxLayout()
            passwd_label=QLabel('密码：')
            self.passwd_Edit=QLineEdit()
            self.passwd_Edit.setEchoMode(QLineEdit.Password)
            passwd_layout.addWidget(passwd_label)
            passwd_layout.addWidget(self.passwd_Edit)
            connect_layout.addLayout(passwd_layout)

            filedownload_layout=QHBoxLayout()
            downcloud_label = QLabel('远程文件：')
            self.filedown=QLineEdit()
            passwd_layout.addWidget(downcloud_label)
            passwd_layout.addWidget(self.filedown)
            connect_layout.addLayout(filedownload_layout)


            save_layout=QHBoxLayout()
            connect_botton=QPushButton("连接",self)
            # save_botton = QPushButton("保存", self)
            save_layout.addWidget(connect_botton)
            # save_layout.addWidget(save_botton)
            connect_layout.addLayout(save_layout)
            #upload_button = QPushButton('上传', self)
            connect_botton.clicked.connect(self.connect_ssh)
            #upload_button.clicked.connect(self.upload_file)
            # save_botton.clicked.connect(self.save_config)
            #connect_layout.addWidget(connect_botton)
            #connect_layout.addWidget(upload_button)
            #新的垂直全局布局(工具上小分段的部分了，用两个QvBOXLayout分开)
            command_widget=QWidget(self)
            command_layout=QVBoxLayout()
            command_widget.setLayout(command_layout)
            main_layout.addWidget(command_widget)
            #命令行
            command_label=QLabel('命令：')
            self.command_Edit=QTextEdit()
            command_layout.addWidget(command_label)
            command_layout.addWidget(self.command_Edit)
            #创建小的水平布局，并在水平布局内添加按钮
            executearea_layout=QHBoxLayout()
            execute_button = QPushButton('执行', self)
            clean_button = QPushButton('清除',self)
            execute_button.clicked.connect(self.execute_command)
            clean_button.clicked.connect(self.cleanoutput_edit)
            executearea_layout.addWidget(execute_button)
            executearea_layout.addWidget(clean_button)
            #最后吧水平布局添加至下部分的垂直布局。
            command_layout.addLayout(executearea_layout)

            output_label = QLabel('输出内容:')
            command_layout.addWidget(output_label)

            self.output_edit = QTextEdit()
            self.output_edit.setReadOnly(True)
            command_layout.addWidget(self.output_edit)
        def connect_ssh(self):
            host=self.host_Edit.text()
            port=int(self.port_Edit.text())
            user=self.userEidt.text()
            password=self.passwd_Edit.text()
            self.output_edit.setText('')
            try:
                self.ssh= paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                self.ssh.connect(host,port,user,password)
                self.output_edit.append('Connected to {}:{} as {}.'.format(host,port,user))
            except Exception as e:
                QMessageBox.warning(self,'错误',str(e))
        def execute_command(self):
            command=self.command_Edit.toPlainText()
            self.output_edit.append('{}'.format(command))
            try:
                stdin,stdout,stderr=self.ssh.exec_command(command)
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')
                if output:
                    self.output_edit.append(output)
                if error:
                    self.output_edit.append(error)
            except Exception as e:
                QMessageBox(self,'错误',str(e))
        def cleanoutput_edit(self):
            self.output_edit.setText('')
            self.command_Edit.setText('')

        def closeEvent(self, event):
            reply = QMessageBox.question(self, '确认', "确定要关闭窗口吗？", QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                # 如果点击了"是"按钮，则调用默认的关闭事件处理函数
                super().closeEvent(event)
                self.ssh.close()
            else:
                event.ignore()
        def upload_file(self):
            output_connent=self.output_edit.toPlainText()
            if output_connent != '':
                localfile, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "All Files (*);;Text Files (*.txt)")
                choosename=localfile.split('/')[-1]
                print("已选择文件：" + choosename)
                try:
                    stdin,stdout,stderr= self.ssh.exec_command("pwd")
                    output1 = stdout.read().decode('utf-8')
                    cloudfile=output1.replace("\n","")+'/'+choosename #\n是清除服务器命令执行完返回的换行符
                    print(cloudfile)
                    sftp = self.ssh.open_sftp()
                    localfile1=open(localfile, 'rb')
                    sftp.putfo(localfile1,cloudfile)
                    self.output_edit.append('Upload file to {} success!'.format(self.host_Edit.text()))
                except Exception as e:
                    QMessageBox(self, '错误', str(e))
                finally:
                    # 关闭SFTP会话和SSH连接
                    if sftp is not None:
                        sftp.close()
            else:
                self.output_edit.setText("WrongConnection,Can't upload!!!")
            # def save_config(self):
        #     host1=self.host_Edit.text()
        #     port1=self.port_Edit.text()
        #     user1=self.user_Edit.text()
        #     passwd=self.passwd_Edit.text()
        #     allinone=str(host1+":"+port1+":"+user1+":"+passwd)
        #     file1 = open("C:/Users/HI/Desktop/userinfo.txt", 'w')
        #     file1.write(allinone)
        #     file1.close()
        def download_file(self):
            sftp1 = self.ssh.open_sftp()
            sourcefilename=self.filedown.text().split('/')[-1]
            downtxt=self.filedown.text()
            #dstdirname=os.path.abspath(__file__)
            #dir_path = str(os.path.dirname(dstdirname))
            #dir_path=dir_path.replace("\\","/")+"/"+sourcefilename
            dir_path="D:/"+sourcefilename
            self.output_edit.setText('')
            sftp1.get(downtxt,dir_path)
            self.output_edit.append('Download success!File path:{}'.format(dir_path))
        def aboutus(self):
            self.output_edit.setText('')
            self.output_edit.setText('Version：1.0(240215)\n©2024 Powerd by Eann.cc\n\nContact me:18174831@qq.com      Romote file save directory: D:/')
if __name__ == '__main__':
    appdata=QApplication(sys.argv)
    MainWindow=SSHWindow()
    MainWindow.show()
    sys.exit(appdata.exec_())