from flask import render_template


def register_errors(problem):
    return render_template('register.html', problem=problem)

def contains_number(input_str):
    return any(char.isdigit() for char in input_str)