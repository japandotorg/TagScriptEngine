from typing import Any, List, Optional
from appJar import gui as GUI

import TagScriptEngine as tse
from TagScriptEngine import Interpreter, block

blocks: List[tse.Block] = [
    block.MathBlock(),
    block.RandomBlock(),
    block.RangeBlock(),
    block.AnyBlock(),
    block.IfBlock(),
    block.AllBlock(),
    block.BreakBlock(),
    block.StrfBlock(),
    block.StopBlock(),
    block.AssignmentBlock(),
    block.FiftyFiftyBlock(),
    block.ShortCutRedirectBlock("message"),
    block.LooseVariableGetterBlock(),
    block.SubstringBlock(),
]
x: Interpreter = Interpreter(blocks)


def press(button: Any) -> None:
    o: Optional[str] = x.process(app.getTextArea("input")).body
    app.clearTextArea("output")
    app.setTextArea("output", o)


app: GUI = GUI("TSE Playground", "750x450")
app.setPadding([2, 2])
app.setInPadding([2, 2])
app.addTextArea("input", text="I see {rand:1,2,3,4} new items!", row=0, column=0)
app.addTextArea("output", text="Press process to continue", row=0, column=1)
app.addButton("process", press, row=1, column=0, colspan=2)
app.go()
