import math

# Base rates from the (0.2, 0.6, 0.8, 0.4)-sensitive family
p_near = 0.8   # true positive rate (TPR) for similar pairs
p_far  = 0.4   # false positive rate (FPR) for dissimilar pairs

def or_and(p, r, b):
    """
    OR of b bands, each band is AND of r rows:
    p' = 1 - (1 - p^r)^b
    """
    return 1.0 - (1.0 - (p ** r)) ** b

def and_or(p, r, b):
    """
    AND of b groups, each group is OR of r rows:
    p' = (1 - (1 - p)^r)^b
    """
    return (1.0 - (1.0 - p) ** r) ** b

def rates_for_scheme(scheme_fn, r, b):
    """Return amplified (TPR, FPR, FNR) for given scheme and params."""
    tpr = scheme_fn(p_near, r, b)
    fpr = scheme_fn(p_far,  r, b)
    fnr = 1.0 - tpr
    return tpr, fpr, fnr

def find_params(scheme_fn, max_r=40, max_b=60, fpr_max=None, fnr_max=None):
    """
    Find (r,b) meeting constraints. Minimizes total rows used = r*b,
    then breaks ties by smaller b, then smaller r.
    """
    best = None
    best_key = None

    for r in range(1, max_r + 1):
        for b in range(1, max_b + 1):
            tpr, fpr, fnr = rates_for_scheme(scheme_fn, r, b)

            if fpr_max is not None and not (fpr < fpr_max):
                continue
            if fnr_max is not None and not (fnr < fnr_max):
                continue

            key = (r * b, b, r)  # cost metric: total signatures/rows, etc.
            if best is None or key < best_key:
                best = (r, b, tpr, fpr, fnr)
                best_key = key

    return best

def pretty_result(name, res):
    if res is None:
        print(f"{name}: no solution found in search bounds.")
        return
    r, b, tpr, fpr, fnr = res
    print(f"{name}: r={r}, b={b}, total rows r*b={r*b}")
    print(f"  TPR={tpr:.6f}  FPR={fpr:.6f}  FNR={fnr:.6f}")

# --------------------------
# Goal A: FPR < 0.15
# --------------------------
print("GOAL A: Reduce FPR from 0.4 to < 0.15\n")
pretty_result("OR-AND best", find_params(or_and, fpr_max=0.15))
pretty_result("AND-OR best", find_params(and_or, fpr_max=0.15))

# --------------------------
# Goal B: FNR < 0.10
# --------------------------
print("\nGOAL B: Reduce FNR from 0.2 to < 0.10\n")
pretty_result("OR-AND best", find_params(or_and, fnr_max=0.10))
pretty_result("AND-OR best", find_params(and_or, fnr_max=0.10))

# --------------------------
# Goal C: BOTH < 0.05
# --------------------------
print("\nGOAL C: Reduce BOTH FPR and FNR to < 0.05\n")
pretty_result("OR-AND best", find_params(or_and, fpr_max=0.05, fnr_max=0.05))
pretty_result("AND-OR best", find_params(and_or, fpr_max=0.05, fnr_max=0.05))
