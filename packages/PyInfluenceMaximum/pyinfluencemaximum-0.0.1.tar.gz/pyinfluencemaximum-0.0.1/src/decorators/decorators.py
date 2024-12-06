from functools import wraps


def not_implemented_for(func, name):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result

    return wrapper


@not_implemented_for('direct')
def greet(name):
    """This function greets a person by name."""
    print(f"Hello, {name}!")


# 现在greet函数的元数据被保留了
print(greet.__name__)  # 输出: greet
print(greet.__doc__)  # 输出: This function greets a person by name.
greet('xx')
