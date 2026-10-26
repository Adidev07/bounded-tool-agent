"""Execute a model-proposed tool plan through an allowlisted dispatcher with strict budgets and an audit trail."""
from kit import *
TITLE='Bounded Tool-Calling Agent'
LIVE=True

import ast, operator
def calculate(expression):
    if not isinstance(expression,str) or len(expression)>120:raise ValueError('Expression too large')
    tree=ast.parse(expression,mode='eval');count=0
    operations={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
    def visit(node):
        nonlocal count
        count+=1
        if count>30:raise ValueError('Expression too complex')
        if isinstance(node,ast.Constant) and type(node.value) in (int,float):value=node.value
        elif isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):value=-visit(node.operand)
        elif isinstance(node,ast.BinOp) and type(node.op) in operations:value=operations[type(node.op)](visit(node.left),visit(node.right))
        else:raise ValueError('Unsupported expression')
        if not math.isfinite(value) or abs(value)>1e12:raise ValueError('Numeric limit exceeded')
        return value
    return visit(tree.body)
def execute(plan,documents,budget=4):
    if not isinstance(plan,list) or not 0<len(plan)<=budget:raise ValueError('Tool budget exceeded or empty plan')
    trace=[]
    for call in plan:
        if not isinstance(call,dict) or set(call)!={'tool','argument'} or not isinstance(call['argument'],str):raise ValueError('Invalid call schema')
        if call['tool']=='calculator':observation=calculate(call['argument'])
        elif call['tool']=='search':observation=bm25(call['argument'],chunks(documents),2)
        else:raise ValueError('Tool not allowed')
        trace.append(dict(call=call,observation=observation))
    return trace
def run(d,a):
    schema={'type':'object','properties':{'calls':{'type':'array','items':{'type':'object','properties':{'tool':{'type':'string','enum':['calculator','search']},'argument':{'type':'string'}},'required':['tool','argument'],'additionalProperties':False},'maxItems':4,'minItems':1}},'required':['calls'],'additionalProperties':False}
    plan=json.loads(generate('Plan up to four calculator or search calls. Calculator supports + - * /. Return JSON calls. Task: '+d['task'],a,schema))['calls'] if a.mode=='live' else d['fixture_plan']
    trace=execute(plan,d['documents']);return dict(mode=a.mode,task=d['task'],trace=trace,tools_used=len(trace),budget=4),None

if __name__=="__main__":main(run)
