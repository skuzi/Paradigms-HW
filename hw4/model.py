class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.val = {}

    def __getitem__(self, key):
        if key not in self.val:
            return self.parent.val[key]
        else:
            return self.val[key]

    def __setitem__(self, key, value):
        self.val[key] = value


class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __hash__(self, other):
        return hash(self.value)

    def evaluate(self, scope):
        return self


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Список имен аргументов - список имен
    формальных параметров функции.
    Аналогично Number, метод evaluate должен возвращать self.
    """

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        num = self.condition.evaluate(scope).value
        value = None
        if num == 0:
            if self.if_false is not None:
                for expr in self.if_false:
                    value = expr.evaluate(scope)
        else:
            for expr in self.if_true:
                value = expr.evaluate(scope)
        return value if value is not None else 0


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        num = self.expr.evaluate(scope)
        print(num.value)
        return num


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = int(input())
        scope[self.name] = Number(a)
        return Number(a)


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        call_scope = Scope(scope)
        function = self.fun_expr.evaluate(scope)
        for name, expr in zip(function.args, self.args):
            call_scope[name] = expr.evaluate(scope)
        for expr in function.body:
            val = expr.evaluate(call_scope)
        return val


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope).value
        right = self.rhs.evaluate(scope).value
        op = self.op
        results = {'+': Number(left + right),
                   '-': Number(left - right),
                   '*': Number(left * right),
                   '/': Number(-1 if right == 0 else left / right),
                   '==': Number(1 if left == right else 0),
                   '!=': Number(0 if left == right else 1),
                   '<': Number(1 if left < right else 0),
                   '>': Number(0 if left < right else 1),
                   '<=': Number(1 if left <= right else 0),
                   '>=': Number(1 if left >= right else 0),
                   '&&': Number(1 if left != 0 and right != 0 else 0),
                   '||': Number(1 if left != 0 or right != 0 else 0)}
        return results[op]


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope)
        if self.op == '-':
            return Number(-expr.value)
        else:
            return Number(1 if expr.value == 0 else 0)


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def main():
    example()
    my_tests()


def my_tests():
    """ tests: a * b
               a - b
               a + b
               a / b
               a * a + b * b
               c == 0 """
    scope = Scope()

    def sqr(a):
        return a*a
    plus = FunctionDefinition('plus',
                              Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                                    '+',
                                                                    Reference('b'))]))
    mult = FunctionDefinition('mult',
                              Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                                    '*',
                                                                    Reference('b'))]))
    div = FunctionDefinition('div',
                             Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                                   '/',
                                                                   Reference('b'))]))
    minus = FunctionDefinition('minus',
                               Function(('a', 'b'), [BinaryOperation(Reference('a'),
                                                                     '-',
                                                                     Reference('b'))]))
    Read('a').evaluate(scope)
    Read('b').evaluate(scope)
    a = scope['a']
    b = scope['b']

    t = FunctionCall(plus, [a, b]).evaluate(scope)
    print('plus check for', a.value, b.value)
    print('correct' if a.value + b.value == t.value else 'wrong')

    t = FunctionCall(mult, [a, b]).evaluate(scope)
    print('mult check for', a.value, b.value)
    print('correct' if a.value * b.value == t.value else 'wrong')

    t = FunctionCall(div, [a, b]).evaluate(scope)
    print('div check for', a.value, b.value)
    print('correct' if a.value / b.value == t.value else 'wrong')

    t = FunctionCall(minus, [a, b]).evaluate(scope)
    print('minus check for', a.value, b.value)
    print('correct' if a.value - b.value == t.value else 'wrong')

    scalar = FunctionDefinition('scalar', Function(('a', 'b', 'c', 'd'),
                                                   [BinaryOperation(FunctionCall(mult, [Reference('a'), Reference('c')]),
                                                                    '+',
                                                                    FunctionCall(mult, [Reference('b'), Reference('d')]))]))

    t = FunctionCall(scalar, [a, b, a, b]).evaluate(scope)
    print('scalar check for', a.value, b.value, a.value, b.value)
    print('correct' if sqr(a.value) + sqr(b.value) == t.value else 'incorrect')

    Read('c').evaluate(scope)
    c = scope['c']

    print('check', c.value, '== 0')
    condition = Conditional(BinaryOperation(UnaryOperation('!', c),
                                            '&&',
                                            BinaryOperation(UnaryOperation('-', BinaryOperation(c, '+', c)),
                                                            '==',
                                                            BinaryOperation(c, '+', c))),
                            [Print(UnaryOperation('!', c))],
                            [Print(UnaryOperation('!', UnaryOperation('!', UnaryOperation('!', c))))])
    condition.evaluate(scope)


if __name__ == '__main__':
    main()
