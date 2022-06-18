#!/usr/bin/env python3

import sys
from collections import deque

tracing = False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("ERROR: no file path is provided")
        exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r') as f:
        program = [word
                   for line in f.read().splitlines()
                   if not line.lstrip().startswith('#')
                   for word in line.split(' ')
                   if len(word) > 0]

        labels = {}
        for ip in range(len(program)):
            word = program[ip]
            if word.endswith(':'):
                word = word[:-1]
                if word in labels:
                    raise RuntimeError(f"Label `{word}` already defined")
                labels[word] = ip

        data = deque()

        ip = 0
        while ip < len(program):
            word = program[ip]
            if tracing:
                print(f"{ip}: {word} <- {data}")
            left = None
            if word.startswith('!'):
                word = word[1:]
                left = True
            elif word.endswith('!'):
                word = word[:-1]
                left = False
            elif word.endswith(':'):
                ip += 1
                continue

            def push_data(value):
                if left is None:
                    raise RuntimeError(f"Direction is not provided for {word} at {ip}")
                if left:
                    data.appendleft(value)
                else:
                    data.append(value)

            def pop_data():
                if left is None:
                    raise RuntimeError(f"Direction is not provided for {word} at {ip}")
                if left:
                    return data.popleft()
                else:
                    return data.pop()

            if word == 'add':
                a = pop_data()
                b = pop_data()
                push_data(a + b)
                ip += 1
            elif word == 'sub':
                a = pop_data()
                b = pop_data()
                push_data(b - a)
                ip += 1
            elif word == 'dup':
                a = pop_data()
                push_data(a)
                push_data(a)
                ip += 1
            elif word == 'swap':
                a = pop_data()
                b = pop_data()
                push_data(a)
                push_data(b)
                ip += 1
            elif word == 'move':
                a = pop_data()
                left = not left
                push_data(a)
                left = not left
                ip += 1
            elif word == 'over':
                a = pop_data()
                b = pop_data()
                push_data(b)
                push_data(a)
                push_data(b)
                ip += 1
            elif word == 'drop':
                pop_data()
                ip += 1
            elif word == 'shr':
                a = pop_data()
                b = pop_data()
                push_data(b >> a)
                ip += 1
            elif word == 'shl':
                a = pop_data()
                b = pop_data()
                push_data(b << a)
                ip += 1
            elif word == 'eq':
                a = pop_data()
                b = pop_data()
                push_data(a == b)
                ip += 1
            elif word == 'or':
                a = pop_data()
                b = pop_data()
                push_data(a | b)
                ip += 1
            elif word == 'and':
                a = pop_data()
                b = pop_data()
                push_data(a & b)
                ip += 1
            elif word == '>':
                a = pop_data()
                b = pop_data()
                push_data(a > b)
                ip += 1
            elif word == '<':
                a = pop_data()
                b = pop_data()
                push_data(a < b)
                ip += 1
            elif word == '>=':
                a = pop_data()
                b = pop_data()
                push_data(a >= b)
                ip += 1
            elif word == 'jmpif':
                addr = pop_data()
                cond = pop_data()
                if cond:
                    ip = addr
                else:
                    ip += 1
            elif word == 'jmp':
                addr = pop_data()
                ip = addr
            elif word == 'print':
                print(pop_data())
                ip += 1
            elif word == 'exit':
                exit(0)
            elif word == 'trace':
                print(''.join(map(lambda x: '*' if x == 1 else ' ', data)))
                ip += 1
            else:
                try:
                    push_data(int(word))
                    ip += 1
                except ValueError:
                    push_data(labels[word])
                    ip += 1
        if tracing: print(data)
