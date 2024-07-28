from __future__ import division, annotations

import math
import operator
from typing import Any, Callable, Dict, List, Tuple, cast, Optional as TypingOptional

from pyparsing import (
    CaselessLiteral,
    Combine,
    Forward,
    Group,
    Literal,
    Optional,
    ParserElement,
    Word,
    ZeroOrMore,
    alphas,
    nums,
    oneOf,
)

from ..interface import Block
from ..interpreter import Context


__all__: Tuple[str, ...] = ("MathBlock",)


class NumericStringParser(object):
    """
    Most of this code comes from the fourFn.py pyparsing example

    """

    def pushFirst(self, strg: Any, loc: Any, toks: Any) -> Any:
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg: Any, loc: Any, toks: Any) -> Any:
        if toks and toks[0] == "-":
            self.exprStack.append("unary -")

    def __init__(self) -> None:
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point: Literal = Literal(".")
        e: CaselessLiteral = CaselessLiteral("E")
        fnumber: Combine = Combine(
            Word("+-" + nums, nums)
            + Optional(point + Optional(Word(nums)))
            + Optional(e + Word("+-" + nums, nums))
        )
        ident: Word = Word(alphas, alphas + nums + "_$")
        mod: Literal = Literal("%")
        plus: Literal = Literal("+")
        minus: Literal = Literal("-")
        mult: Literal = Literal("*")
        iadd: Literal = Literal("+=")
        imult: Literal = Literal("*=")
        idiv: Literal = Literal("/=")
        isub: Literal = Literal("-=")
        div: Literal = Literal("/")
        lpar: ParserElement = Literal("(").suppress()
        rpar: ParserElement = Literal(")").suppress()
        addop: ParserElement = plus | minus
        multop: ParserElement = mult | div | mod
        iop: ParserElement = iadd | isub | imult | idiv
        expop: Literal = Literal("^")
        pi: CaselessLiteral = CaselessLiteral("PI")
        expr: Forward = Forward()
        atom: ParserElement = (
            (
                Optional(oneOf("- +"))
                + (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst)
            )
            | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
        ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor: Forward = Forward()
        factor << atom + ZeroOrMore((expop + factor).setParseAction(self.pushFirst))  # type: ignore
        term: ParserElement = factor + ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + ZeroOrMore((addop + term).setParseAction(self.pushFirst))  # type: ignore
        final: ParserElement = expr + ZeroOrMore((iop + expr).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf: ParserElement = final
        # map operator symbols to corresponding arithmetic operations
        epsilon: float = 1e-12
        self.opn: Dict[str, Callable[[Any, Any], Any]] = {
            "+": operator.add,
            "-": operator.sub,
            "+=": operator.iadd,
            "-=": operator.isub,
            "*": operator.mul,
            "*=": operator.imul,
            "/": operator.truediv,
            "/=": operator.itruediv,
            "^": operator.pow,
            "%": operator.mod,
        }
        self.fn: Dict[str, Any] = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "exp": math.exp,
            "abs": abs,
            "trunc": lambda a: int(a),
            "round": round,
            "sgn": lambda a: abs(a) > epsilon and ((a > 0) - (a < 0)) or 0,
            "log": lambda a: math.log(a, 10),
            "ln": math.log,
            "log2": math.log2,
            "sqrt": math.sqrt,
        }

    def evaluateStack(self, s: List[Any]) -> Any:
        op = s.pop()
        if op == "unary -":
            return -self.evaluateStack(s)
        if op in self.opn:
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string: str, parseAll: bool = True) -> Any:
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)  # noqa: F841
        return self.evaluateStack(self.exprStack[:])


NSP: NumericStringParser = NumericStringParser()


class MathBlock(Block):
    ACCEPTED_NAMES: Tuple[str, ...] = ("math", "m", "+", "calc")

    def process(self, ctx: Context) -> TypingOptional[str]:
        try:
            return str(NSP.eval(cast(str, ctx.verb.payload).strip(" ")))
        except Exception:
            return None
