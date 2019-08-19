import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sls
import _utils
import run_search
def search(problem, search_function, pname, sname, hstring, parameter=None):
    ip = _utils.PrintableProblem(problem)
    start = _utils.timer()
    if parameter is not None:
        node = search_function(ip, parameter)
    else:
        node = search_function(ip)
    end = _utils.timer()
    print("\n# Actions   Expansions   Goal Tests   New Nodes")
    print("{}\n".format(ip))
#     _utils.show_solution(node, end - start)
    actions,expansions,goal_tests,new_nodes= str(ip).split()
    return {'pname':pname, 'sname':sname, 'hstring':hstring,'actions':actions,'expansions':expansions,'goal_tests':goal_tests,'new_nodes':new_nodes,'plan_length':len(node.solution()),'time_elapsed':end-start,'solution':node.solution()}


def main(p_choices, s_choices):
    problems = [run_search.PROBLEMS[i-1] for i in map(int, p_choices)]
    searches = [run_search.SEARCHES[i-1] for i in map(int, s_choices)]
    solutions = []

    for pname, problem_fn in problems:
        for sname, search_fn, heuristic in searches:
            hstring = heuristic if not heuristic else " with {}".format(heuristic)
            print("\nSolving {} using {}{}...".format(pname, sname, hstring))

            problem_instance = problem_fn()
            heuristic_fn = None if not heuristic else getattr(problem_instance, heuristic)
            solutions.append(search(problem_instance, search_fn,pname, sname, hstring, heuristic_fn))
    return solutions

if __name__=='__main__':
    sol=main(range(1,len(run_search.PROBLEMS)+1),range(1,len(run_search.SEARCHES)+1))
    df=pd.DataFrame(sol)
    df.to_csv('./statistics1.csv')