import math
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', choices=['diff', 'annuity'])
    parser.add_argument('--payment', type=int)
    parser.add_argument('--principal', type=int)
    parser.add_argument('--periods', type=int)
    parser.add_argument('--interest', type=float)
    args = parser.parse_args()
    values = {k: v for k, v in vars(args).items() if v}
    if (
        ('type' not in values) or
        (len(values) != 4) or
        ('interest' not in values) or
        (values['type'] == 'diff' and 'payment' in values)
    ):
        print('Incorrect parameters')
    else:
        select_calc(values)


def select_calc(values):
    values['interest'] = values['interest'] * 0.01 / 12
    if values['type'] == 'diff':
        get_diff_payment(values['principal'], values['periods'], values['interest'])
    elif values['type'] == 'annuity':
        if 'periods' not in values:
            get_periods(values['payment'], values['principal'], values['interest'])
        elif 'payment' not in values:
            get_annuity_payment(values['principal'], values['periods'], values['interest'])
        elif 'principal' not in values:
            get_principal(values['payment'], values['periods'], values['interest'])


def get_diff_payment(principal, periods, interest):
    payments_total = 0
    for x in range(1, periods + 1):
        diff_pay = math.ceil(principal / periods + interest * (principal - ((principal * (x - 1)) / periods)))
        print(f"Month {x}: payment is {diff_pay}")
        payments_total += diff_pay
    print(f"Overpayment = {payments_total - principal}")


def get_periods(payment, principal, interest):
    periods = math.ceil(math.log(payment / (payment - interest * principal), 1 + interest))
    if periods < 12:
        duration = f'{periods} {"month" if periods == 1 else "months"}'
    elif periods == 12:
        duration = '1 year'
    elif periods > 12:
        duration = f'{periods // 12} {"year" if periods // 12 == 1 else "years"} ' \
            + f'and {periods % 12} {"month" if periods % 12 == 1 else "months"}'
    print(f'It will take {duration} to repay this loan!')
    print(f"Overpayment = {payment * periods - principal}")


def get_annuity_payment(principal, periods, interest):
    payment = math.ceil(principal * ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1)))
    print(f'Your annuity payment = {payment}!')
    print(f"Overpayment = {payment * periods - principal}")


def get_principal(payment, periods, interest):
    principal = math.floor(payment / ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1)))
    print(f'Your loan principal = {principal}!')
    print(f"Overpayment = {payment * periods - principal}")


if __name__ == '__main__':
    main()
