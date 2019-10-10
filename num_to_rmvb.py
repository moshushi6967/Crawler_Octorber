'''
   作者：lijy
   时间：2019-09-10
   功能：输入浮点数，输出人民币写法
'''


def divide(num):
    '''
    This is a lucky definiation
    :param num:
    :return:
    '''
    integer = int (num)
    fraction = round((num - integer) * 100)
    return (str(integer),str(fraction))


def sum_and_avg(list):
    sum = 0
    count = 0
    for e in list:
        if isinstance(e,int) or isinstance(e,float):
            count += 1
            sum += e
    return sum,sum/count

def fn(n):
    if n == 0:
        return 1
    elif n== 1:
        return 4
    else:
        return 2* fn(n-1) + fn(n-2)
def main():
    # help(divide)
    # print(divide.__doc__)
    # my_list = [20,15,2.8,'a',35,5.9,-1,8]
    # tp = sum_and_avg(my_list)
    # print(tp)
    print(fn(10))

if __name__ == '__main__':
    main()