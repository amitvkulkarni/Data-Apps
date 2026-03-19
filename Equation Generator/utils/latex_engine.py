"""
Latexify engine — pure conversion logic, no Dash imports.
Spec reference: specs/app.spec.md § FR-4
"""

from __future__ import annotations

import ast

from latexify import codegen, config, transformers


def convert_to_latex(source: str) -> dict:
    """
    Convert a Python function source string to a LaTeX string.

    Parameters
    ----------
    source : str
        Full Python function source, e.g.:
            def f(x):
                return x**2 + 1

    Returns
    -------
    dict
        {"latex": str, "error": None}  on success
        {"latex": "",  "error": str}   on failure
    """
    source = source.strip()
    if not source:
        return {"latex": "", "error": "Input is empty. Please enter a Python function."}

    # Parse source to AST — validates syntax without executing anything
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {"latex": "", "error": f"Syntax error: {exc}"}

    # Find the first top-level FunctionDef
    func_def = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)), None)
    if func_def is None:
        return {
            "latex": "",
            "error": (
                "No function definition found. "
                "Please write a complete def statement, e.g.:\n\n"
                "def f(x):\n    return x**2 + 1"
            ),
        }

    # Build a clean Module containing only the FunctionDef and feed into latexify codegen.
    # This bypasses latexify's parse_function() which requires inspect.getsource(),
    # and avoids executing any user code.
    try:
        func_module = ast.Module(body=[func_def], type_ignores=[])
        func_module = transformers.AugAssignReplacer().visit(func_module)

        cfg = config.Config.defaults()
        latex_str = codegen.FunctionCodegen(
            use_math_symbols=cfg.use_math_symbols,
            use_signature=cfg.use_signature,
            use_set_symbols=cfg.use_set_symbols,
        ).visit(func_module)

        return {"latex": latex_str, "error": None}
    except Exception as exc:
        return {"latex": "", "error": f"LaTeX conversion failed: {exc}"}
