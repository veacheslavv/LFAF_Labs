import re

def parse_regex(regex):
    tokens = []
    i = 0

    while i < len(regex):
        if regex[i] == '(':
            j = i
            balance = 0
            while j < len(regex):
                if regex[j] == '(':
                    balance += 1
                elif regex[j] == ')':
                    balance -= 1
                    if balance == 0:
                        break
                j += 1

            content = regex[i+1:j]
            tokens.append(("OR", content.split('|')))
            i = j + 1

        elif i+1 < len(regex) and regex[i+1] == '*':
            tokens.append(("STAR", regex[i]))
            i += 2

        elif i+1 < len(regex) and regex[i+1] == '+':
            tokens.append(("PLUS", regex[i]))
            i += 2

        elif i+1 < len(regex) and regex[i+1] == '^':
            power = int(regex[i+2])
            tokens.append(("POWER", regex[i], power))
            i += 3

        else:
            tokens.append(("CHAR", regex[i]))
            i += 1

    return tokens
