from yat.model import Conditional, FunctionDefinition, FunctionCall, Function, Number, Read, Print, BinaryOperation, UnaryOperation, Reference

class PrettyPrinter:
    """docstring for PrettyPrinter"""
    def __init__(self, ind="    ", ind_len=0):
        self.ind_len = ind_len
        self.ind = ind

    def indent(self):
        print(self.ind * self.ind_len, end='')

    def visit(self, tree, is_statement=True):
        name = tree.__class__.__name__
        method_name = 'visit' + name
        if hasattr(self, method_name):
            fn = getattr(self, 'visit' + name)
        else:
            raise NotImplementedError(method_name)
        if is_statement:
        	self.indent()
        try:
        	return fn(tree)
        finally:
        	if is_statement:
        		print(';')

    def visitConditional(self, conditional):
        print('if (', end='')
        self.visit(conditional.condition, False)
        print(') {')
        self.ind_len += 1
        for expr in conditional.if_true:
            self.visit(expr)
        self.ind_len -= 1
        self.indent()
        print('}', end='')
        self.ind_len += 1
        if conditional.if_false is not None:
            print(' else {')
            for expr in conditional.if_false:
                self.visit(expr)
            self.ind_len -= 1
            self.indent()
            print('}', end='')
        else:
            self.ind_len -= 1

    def visitFunctionDefinition(self, fdef):
        print('def', fdef.name, end='')
        print('(', end='')
        function = fdef.function
        if function.args:
            for args in function.args[:-1]:
                print(args + ', ', end='')
            print(function.args[-1], end='')
        print(') {')
        self.ind_len += 1
        for expr in function.body:
            self.visit(expr)
        self.ind_len -= 1
        self.indent()
        print('}', end='')

    def visitNumber(self, num):
        print(num.value, end='')

    def visitFunctionCall(self, fcall):
        self.visit(fcall.fun_expr, False)
        print('(', end='')
        for arg in fcall.args[:-1]:
            self.visit(arg, False)
            print(',', end=' ')
        self.visit(fcall.args[-1], False)
        print(')', end='')

    def visitBinaryOperation(self, boper):
        left = boper.lhs
        right = boper.rhs
        print('(', end='')
        self.visit(left, False)
        print(') ' + boper.op + ' (', end='')
        self.visit(right, False)
        print(')', end='')

    def visitUnaryOperation(self, uoper):
        print(uoper.op + '(', end='')
        self.visit(uoper.expr, False)
        print(')', end='')

    def visitReference(self, refer):
        print(refer.name, end='')

    def visitPrint(self, prnt):
        print('print', end=' ')
        self.visit(prnt.expr, False)

    def visitRead(self, read):
        print('read ' + read.name, end='')

if __name__ == '__main__':
    printer = PrettyPrinter()
    function = Function(['a', 'b'], [Conditional(Number(42), [Number(42)], None)])
    definition = FunctionDefinition('x', function)
    conditional = Conditional(BinaryOperation(Number(42), '-', Number(42)), [Conditional(BinaryOperation(BinaryOperation(Number(42),
                                                                                                                        '+',
                                                                                                                        Reference('a')),
                                                                                                        '*',
                                                                                                        Number(0)), 
                                                                                        [],
                                                                                        [Conditional(Number(42), [definition], [])])], [])
    printer.visit(definition)
    printer.visit(conditional)
    printer.visit(Read('x'))
    printer.visit(Print(BinaryOperation(Number(2), '+', Reference('a'))))
