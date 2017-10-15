from yat.model import Conditional, FunctionDefinition, FunctionCall, Function, Number, Read, Print, BinaryOperation, UnaryOperation, Reference, Scope
from yat.printer import PrettyPrinter
import copy


class ConstantFolder:
    def visit(self, tree):
        name = tree.__class__.__name__
        method_name = 'visit' + name
        if hasattr(self, method_name):
            fn = getattr(self, 'visit' + name)
        else:
            raise NotImplementedError(method_name)
        new_tree = copy.deepcopy(tree)
        return fn(new_tree)

    def visitConditional(self, conditional):
        conditional.condition = self.visit(conditional.condition)
        if_true = conditional.if_true
        if_false = conditional.if_false
        for i in range(len(if_true)):
            if_true[i] = self.visit(if_true[i])
        if if_false is not None:
            for i in range(len(if_false)):
                if_false[i] = self.visit(if_false[i])
        return conditional

    def visitFunctionDefinition(self, fdef):
        for i in range(len(fdef.function.body)):
            fdef.function.body[i] = self.visit(fdef.function.body[i])
        return fdef

    def visitNumber(self, num):
        return num

    def visitFunctionCall(self, fcall):
        fcall.fun_expr = self.visit(fcall.fun_expr)
        for i in range(fcall.args):
            fcall.args[i] = self.visit(fcall.args[i])
        return fcall

    def visitBinaryOperation(self, boper):
        boper.lhs = self.visit(boper.lhs)
        boper.rhs = self.visit(boper.rhs)
        left = boper.lhs
        right = boper.rhs
        if isinstance(left, Number) and isinstance(right, Number):
            return BinaryOperation(left, boper.op, right).evaluate(Scope())
        if boper.op == '*' and (isinstance(left, Number) and left.value == 0 or isinstance(right, Number) and right.value == 0):
            return Number(0)
        if isinstance(left, Reference) and isinstance(right, Reference) and right.name == left.name:
            return Number(0)
        return boper

    def visitUnaryOperation(self, uoper):
        uoper.expr = self.visit(uoper.expr)
        if(isinstance(uoper.expr, Number)):
            return UnaryOperation(uoper.op, uoper.expr).evaluate(Scope())
        else:
            return uoper

    def visitReference(self, refer):
        return refer

    def visitPrint(self, prnt):
        prnt.expr = self.visit(prnt.expr)
        return prnt

    def visitRead(self, read):
        return read


if __name__ == '__main__':
    printer = PrettyPrinter()
    folder = ConstantFolder()
    function = Function(['a', 'b'], [Conditional(Number(42), [Number(42)], None)])
    definition = FunctionDefinition('x', function)
    conditional = Conditional(BinaryOperation(Reference('a'), '-', BinaryOperation(Reference('a'), '-', Reference('a'))), [Conditional(BinaryOperation(BinaryOperation(Number(42),
                                                                                                                        '+',
                                                                                                                        Reference('a')),
                                                                                                        '*',
                                                                                                        Number(0)),
                                                                                        [],
                                                                                        [Conditional(Number(42), [definition], [])])], [])
    printer.visit(conditional)
    conditional = folder.visit(conditional)
    prnt = Print(BinaryOperation(Number(1), '+', BinaryOperation(Number(2), '+', BinaryOperation(Reference('a'), '-', Reference('a')))))
    printer.visit(prnt)
    prnt = folder.visit(prnt)
    printer.visit(conditional)
    printer.visit(prnt)
