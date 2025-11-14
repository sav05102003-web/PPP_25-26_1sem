def caesar_shift_char(char, shift):
    if 'a' <= char <= 'z':
        new_pos = (ord(char) - ord('a') + shift) % 26
        return chr(ord('a') + new_pos)
    return char

def reverse_string(s):
    return s[::-1]

def process_commands_step_by_step(initial_string, commands_list):
    current_string = initial_string
    history = [current_string]

    for command in commands_list:
        if command.startswith('c'):
            try:
                shift = int(command[1:])
                new_string = ''
                for char in current_string:
                    new_string += caesar_shift_char(char, shift)
                current_string = new_string
            except ValueError:
                print(f"Ошибка: Некорректный параметр для команды 'c': {command}")
                break 
        elif command == 'r':
            current_string = reverse_string(current_string)
        else:
            print(f"Ошибка: Неизвестная команда: {command}")
            break
        
        history.append(current_string) 

    return history

initial_str = str(input('Введите текст для шифрования:'))
commands = []
number = int(input('Введите колличество комманд для шифрования:'))
for i in range(number):
    command = input('Введите команду:')
    commands.append(command)

all_steps = process_commands_step_by_step(initial_str, commands)

print(f"Начальная строка: {initial_str}")
print(f"Список команд: {commands}")
print('Пошаговая история изменений:')
for i, state in enumerate(all_steps):
    print(f"Шаг {i}: {state}")

final_output = all_steps[-1]

print(f"Итоговый результат :{final_output}")
