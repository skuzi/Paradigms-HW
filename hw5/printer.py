from yat.model import Conditional, FunctionDefinition, FunctionCall, Function, Number, Read, Print, BinaryOperation, UnaryOperation, Reference

class PrettyPrinter:
    """docstring for PrettyPrinter"""
    ind_len = 0
    ind = "    "

    def visit(self, tree, is_statement=True):
        name = tree.__class__.__name__
        method_name = 'visit' + name
        if hasattr(self, method_name):
            fn = getattr(self, 'visit' + name)
        else:
            raise NotImplementedError(method_name)
        return fn(tree, is_statement)

    def visitConditional(self, conditional, is_statement=True):
        print(self.ind * self.ind_len + 'if (', end='')
        self.visit(conditional.condition, False)
        print('){')
        self.ind_len += 1
        for expr in conditional.if_true:
            self.visit(expr)
        self.ind_len -= 1
        print(self.ind * self.ind_len + '}', end='')
        self.ind_len += 1
        if conditional.if_false is not None:
            print('else{')
            for expr in conditional.if_false:
                self.visit(expr)
            self.ind_len -= 1
            print(self.ind * self.ind_len + '};')
        else:
            print(';')
            self.ind_len -= 1

    def visitFunctionDefinition(self, fdef, is_statement=True):
        print(self.ind * self.ind_len + 'def', fdef.name, end='')
        print('(', end='')
        function = fdef.function
        if(len(function.args) > 0):
            for args in function.args[:-1]:
                print(args + ', ', end='')
            print(function.args[-1], end='')
        print(') {')
        self.ind_len += 1
        for expr in function.body:
            self.visit(expr)
        self.ind_len -= 1
        print(self.ind * self.ind_len + '};')

    def visitNumber(self, num, is_statement=True):
        print(self.ind * self.ind_len if is_statement else '', end='')
        print(num.value, end=';\n' if is_statement else '')

    def visitFunctionCall(self, fcall, is_statement=True):
        self.visit(fcall.fun_expr, False)
        print('(', end='')
        for arg in fcall.args[:-1]:
            self.visit(arg, False)
            print(',', end=' ')
        self.visit(fcall.args[-1], False)
        print(')', end=';\n' if is_statement else '')

    def visitBinaryOperation(self, boper, is_statement=True):
        left = boper.lhs
        right = boper.rhs
        if is_statement:
            print(self.ind * self.ind_len, end='')
        print('(', end='')
        self.visit(left, False)
        print(') ' + boper.op + ' (', end='')
        self.visit(right, False)
        print(')', end=';\n' if is_statement else '')

    def visitUnaryOperation(self, uoper, is_statement=True):
        if is_statement:
            print(self.ind * self.ind_len, end='')
        print(uoper.op + '(', end='')
        self.visit(uoper.expr, False)
        print(')', end=';\n' if is_statement else '')

    def visitReference(self, refer, is_statement=True):
        print(self.ind * self.ind_len if is_statement else '' + refer.name, end=';\n' if is_statement else '')

    def visitPrint(self, prnt, is_statement=True):
        print(self.ind * self.ind_len + 'print', end=' ')
        self.visit(prnt.expr, False)
        print('', end=';\n' if is_statement else '')

    def visitRead(self, read, is_statement=True):
        print(self.ind * self.ind_len + 'read ' + read.name + ';')

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
