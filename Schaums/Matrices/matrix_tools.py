# matrix_tools.py
import sympy as sp

def row_echelon_form(matrices, matrix_name, form="both", show_steps=False):
    """
    REF / RREF for a matrix from a user-provided dictionary.

    Parameters
    ----------
    matrices : dict
        Dictionary where keys are matrix names and values are sympy.Matrix objects.
    matrix_name : str
        Name of the matrix to process.
    """
    name = matrix_name.strip().upper()
    if name not in matrices:
        print(f"Error: Matrix '{matrix_name}' not found!")
        print("Available:", ', '.join(matrices.keys()))
        return None, None, None, None

    M_orig = matrices[name]
    print(f"Selected matrix: {name}")
    sp.pprint(M_orig)
    print()

    # --- forward elimination (REF) ---
    M = M_orig.copy()
    rows, cols = M.shape
    lead = 0
    ref_steps = []

    for r in range(rows):
        if lead >= cols:
            break

        pivot_row = None
        for i in range(r, rows):
            if M[i, lead] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            lead += 1
            continue

        if pivot_row != r:
            M.row_swap(r, pivot_row)
            if show_steps:
                ref_steps.append((f"Swap R{r+1} ↔ R{pivot_row+1}", M.copy()))

        pivot = M[r, lead]
        if pivot != 1:
            M.row_op(r, lambda v, _: v / pivot)
            if show_steps:
                ref_steps.append((f"R{r+1} ← R{r+1} / ({pivot})", M.copy()))

        for i in range(r + 1, rows):
            if M[i, lead] != 0:
                factor = M[i, lead]
                M.row_op(i, lambda v, j: v - factor * M[r, j])
                if show_steps:
                    ref_steps.append((f"R{i+1} ← R{i+1} - ({factor})·R{r+1}", M.copy()))
        lead += 1

    # --- back-substitution (RREF) ---
    rref = None
    rref_steps = []
    if form in ("rref", "both"):
        rref = M.copy()
        pivots = []
        lead = 0
        for row in range(rows):
            if lead >= cols:
                break
            if rref[row, lead] != 0:
                pivots.append((row, lead))
                lead += 1
            else:
                lead += 1
        for pr, lead in reversed(pivots):
            for i in range(pr):
                if rref[i, lead] != 0:
                    factor = rref[i, lead]
                    rref.row_op(i, lambda v, j: v - factor * rref[pr, j])
                    if show_steps:
                        rref_steps.append((f"R{i+1} ← R{i+1} - ({factor})·R{pr+1}", rref.copy()))

    # --- print steps ---
    if show_steps:
        def _p(title, steps):
            if steps:
                print(title)
                for msg, mat in steps:
                    print(msg)
                    sp.pprint(mat)
                    print()
        _p("--- REF steps ---", ref_steps)
        if rref_steps:
            _p("--- RREF steps ---", rref_steps)

    # --- pivots ---
    def _pivots(mat):
        p = []
        lead = 0
        for row in range(mat.rows):
            if lead >= mat.cols:
                break
            if mat[row, lead] != 0:
                p.append(lead)
                lead += 1
            else:
                lead += 1
        return p

    ref_pivots = _pivots(M)

    if form in ("ref", "both"):
        print("Row Echelon Form (REF):")
        sp.pprint(M)
        print("Pivot columns (REF):", ref_pivots)

    if form in ("rref", "both"):
        print("\nReduced Row Echelon Form (RREF):")
        sp.pprint(rref)
        print("Pivot columns (RREF):", ref_pivots)

    return (
        M if form in ("ref", "both") else None,
        rref if form in ("rref", "both") else None,
        ref_pivots if form in ("ref", "both") else None,
        ref_pivots
    )

