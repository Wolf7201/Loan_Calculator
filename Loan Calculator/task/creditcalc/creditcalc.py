import argparse
from math import ceil, log

def_dict = {
    'annuity': 'Hi',
    'diff': 'Hello'
}

calc_set = {'principal', 'payment', 'periods', 'interest'}

desc_msg = 'This is calculator the capacity to compute differentiated payments.'

errors = (KeyError,
          AttributeError,
          ValueError,
          argparse.ArgumentError)


def annuity_payment_func(P, n, i):
    A = ceil(P * ((i * pow((1 + i), n)) / (pow(1 + i, n) - 1)))
    print(f'Your annuity payment = {A}!')
    over = (A * n) - P
    print(f'Overpayment = {over}')


def loan_principal_func(A, n, i):
    P = int(A / ((i * pow((1 + i), n)) / (pow(1 + i, n) - 1)))
    print(f'Your loan principal = {P}!')
    over = (A * n) - P
    print(f'Overpayment = {over}')


def number_payments_func(P, A, i):
    n = ceil(log((A / (A - i * P)), 1 + i))
    years = int(n // 12)
    months = ceil(n % 12)
    if years == 0:
        print(f'It will take {months} months to repay this loan!')
    elif months == 0:
        print(f'It will take {years} years to repay this loan!')
    else:
        print(f'It will take {years} years and {months} months to repay this loan!')
    over = (A * n) - P
    print(f'Overpayment = {over}')


def differentiated_payment(P, i, n):
    summ = 0
    for m in range(1, n + 1):
        D = ceil(P / n + i * (P - (P * (m - 1) / n)))
        summ += D
        print(f"Month {m}: payment is {D}")
    over = summ - P
    print(f'\nOverpayment = {over}')


def correct_num(num):
    num = int(num)
    if num > 0:
        return num
    raise ValueError


def interest_func(num):
    num = float(num)
    if num > 0:
        return num / (12 * 100)
    raise ValueError


def remove_none_arg(namespace):
    if not namespace.type:
        raise ValueError
    elif namespace.payment and namespace.type == 'diff':
        raise ValueError

    namespace_dict = namespace.__dict__
    del_key = [arg for arg in namespace_dict if namespace_dict[arg] is None]
    for key in del_key:
        del namespace_dict[key]

    if len(namespace_dict) < 4:
        raise ValueError

    return namespace_dict


parser = argparse.ArgumentParser(description=desc_msg, exit_on_error=False)
parser.add_argument("--type", choices=['annuity', 'diff'])
parser.add_argument("--principal", type=correct_num)
parser.add_argument("--periods", type=correct_num)
parser.add_argument("--interest", type=interest_func)
parser.add_argument("--payment", type=correct_num)

try:
    args = parser.parse_args()
    args_dict = remove_none_arg(args)
    args_set = set(args_dict.keys())
    calc_set = list(calc_set - args_set)[0]
    if args.type == 'diff':
        differentiated_payment(args.principal, args.interest, args.periods)
    elif calc_set == 'principal':
        loan_principal_func(args.payment, args.periods, args.interest)
    elif calc_set == 'periods':
        number_payments_func(args.principal, args.payment, args.interest)
    elif calc_set == 'payment':
        annuity_payment_func(args.principal, args.periods, args.interest)


except errors:
    print('Incorrect parameters.')
