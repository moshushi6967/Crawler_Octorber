"""
  作者：lijy
  功能：判断密码强度
  版本：1.0
  日期：20190901

"""
import os


class PasswordTool:
    def __init__(self, password):
        self.password = password
        self.strength_level = 0

    def check_number_exist(self):
        return_tag = False
        for c in self.password:
            if c.isnumeric():
                return_tag = True
                break
        return return_tag

    def check_alpha_exist(self):
        return_tag = False
        for c in self.password:
            if c.isalpha():
                return_tag = True
                break
        return return_tag

    def password_strength_judge(self):
        if len(self.password) >= 8:
            self.strength_level += 1
        else:
            print("密码长度至少8位")

        if self.check_number_exist():
            self.strength_level += 1
        else:
            print("密码要求包含数字： ")

        if self.check_alpha_exist():
            self.strength_level += 1
        else:
            print("密码要求包含字母： ")


class FileTool:
    def __init__(self, path):
        self.path = path

    def file_write(self, line):
        f = open(self.path, 'a', encoding='utf-8')
        f.write(line)
        f.close()

    def file_read(self):
        f = open(self.path, 'r', encoding='utf-8')
        file_str = f.read()
        print(file_str)
        f.close()


def main():
    password = input("请输入密码： ")
    password_tool = PasswordTool(password)
    password_tool.password_strength_judge()
    line = '您的密码是：{}，密码强度为： {}\n'.format(password, password_tool.strength_level)
    if password_tool.strength_level == 3:
        print("你输入的密码是强密码！")
    else:
        print("你输入的密码强度不够")
    path = os.path.abspath('.') + '\\' + 'password.txt'
    file_tool = FileTool(path)
    file_tool.file_write(line)
    file_tool.file_read()


if __name__ == '__main__':
    main()