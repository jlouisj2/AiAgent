def calculate(expression):
    tokens = expression.split()

    if len(tokens) < 3:
        return "Invalid expression"

    # First pass: Multiplication and Division
    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '*':
            new_tokens[-1] = float(new_tokens[-1]) * float(tokens[i+1])
            i += 2
        elif tokens[i] == '/':
            new_tokens[-1] = float(new_tokens[-1]) / float(tokens[i+1])
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1

    # Second pass: Addition and Subtraction
    result = float(new_tokens[0])
    for i in range(1, len(new_tokens), 2):
        operator = new_tokens[i]
        operand = float(new_tokens[i+1])

        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        else:
            return "Invalid operator"

    return result