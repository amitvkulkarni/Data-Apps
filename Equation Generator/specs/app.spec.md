# App Specification — Latexify App

**Version:** 1.0  
**Status:** Approved  
**Last Updated:** 2026-03-18

---

## 1. Purpose

Provide a browser-based tool where a user writes a Python function representing a mathematical
expression and immediately sees a publication-ready LaTeX equation rendered on screen.
The app is aimed at students, researchers, and engineers who want to produce clean math
notation without writing LaTeX by hand.

---

## 2. User Story

> As a user, I want to type a Python mathematical function into a text box, click a button,
> and see a properly rendered LaTeX equation that I can copy and use in a paper or presentation.

---

## 3. Functional Requirements

### FR-1 — Input Panel

- A multi-line code editor (`dcc.Textarea`) labelled **"Python Function"**
- Placeholder text: `def f(x):\n    return x**2 + 2*x + 1`
- A **"Generate LaTeX"** button (`dbc.Button`, `id="btn-generate"`)
- A **"Clear"** button (`dbc.Button`, `id="btn-clear"`) that resets both input and output

### FR-2 — Output Panel

- A **rendered equation** area using `dcc.Markdown` with MathJax delimiters (`$$...$$`)
- The raw **LaTeX string** shown in a read-only `dcc.Textarea` labelled **"LaTeX Source"**
- A **"Copy LaTeX"** button (`dbc.Button`, `id="btn-copy"`) that copies the raw string to clipboard via `dcc.Clipboard`

### FR-3 — Examples Sidebar

- A vertical list of **5 clickable example cards** (`dbc.Card`), each containing:
  - A short label (e.g., "Quadratic", "Euler's Identity")
  - The pre-written Python function snippet
- Clicking a card loads that snippet into the input textarea

### FR-4 — Equation Conversion Engine

- Logic lives exclusively in `utils/latex_engine.py`
- Function signature: `convert_to_latex(source: str) -> dict`
- Returns `{"latex": str, "error": None}` on success
- Returns `{"latex": "", "error": str}` on failure
- Uses `latexify.get_latex()` internally (wrapped in try/except)
- Input is the **full Python function source string** (def + body), compiled to a code object via `compile()` + `types.FunctionType` — never `eval()`/`exec()`

### FR-5 — Error Handling

- Syntax errors show a visible red alert (`dbc.Alert`, color="danger") below the input
- The output panel clears when there is an error
- The app must never crash on any user input

### FR-6 — Page Metadata

- Browser tab title: **"Latexify — Math Equation Generator"**
- Top navbar with app name

### FR-7 — Dark / Light Mode Toggle

- A toggle switch (`dbc.Switch`, `id="toggle-theme"`) in the navbar, flanked by sun (`bi-sun-fill`) and moon (`bi-moon-fill`) Bootstrap icons
- Default mode: **Light** (`dbc.themes.BOOTSTRAP`)
- Dark mode uses `dbc.themes.DARKLY`
- Persists for the session (`persistence_type="session"`)
- Switches the Bootstrap stylesheet at runtime via a dynamic `html.Link(id="theme-link")` in the layout — no page reload
- A CSS class `dark-mode` is applied to the `id="app-shell"` wrapper div when dark mode is active, enabling CSS overrides for custom BEM classes
- The navbar remains dark-styled in both modes

---

## 4. Non-Functional Requirements

| ID    | Requirement                                                              |
| ----- | ------------------------------------------------------------------------ |
| NFR-1 | Page must be responsive down to 768 px wide (tablet)                     |
| NFR-2 | Equation rendering must use MathJax (loaded via Dash `external_scripts`) |
| NFR-3 | No page reload on any user interaction — all updates via Dash callbacks  |
| NFR-4 | App starts with `python app.py` on port 8050                             |
| NFR-5 | All dependencies pinned in `requirements.txt`                            |

---

## 5. Layout Blueprint

```
┌─────────────────────────────────────────────────────────────┐
│  NAVBAR: "Equation Generator"       [☀ ●──] Dark toggle
├──────────────┬──────────────────────────────────────────────┤
│  SIDEBAR     │  MAIN CONTENT                                │
│  (col-3)     │  (col-9)                                     │
│              │  ┌──────────────────────────────────────┐    │
│  Examples:   │  │ INPUT PANEL                          │    │
│  ─────────   │  │  [Python Function textarea]          │    │
│  Quadratic   │  │  [Generate LaTeX]  [Clear]           │    │
│  Cubic       │  └──────────────────────────────────────┘    │
│  Trig        │  ┌──────────────────────────────────────┐    │
│  Euler       │  │ OUTPUT PANEL                         │    │
│  Gaussian    │  │  [Rendered equation via MathJax]     │    │
│              │  │  [LaTeX Source textarea]             │    │
│              │  │  [Copy LaTeX]                        │    │
│              │  └──────────────────────────────────────┘    │
│              │  [Error alert — hidden by default]           │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 6. Example Snippets (Sidebar)

```python
# Quadratic
def quadratic(x):
    return x**2 + 2*x + 1

# Cubic
def cubic(x):
    return x**3 - 3*x**2 + 3*x - 1

# Trigonometric
def trig(x):
    return math.sin(x)**2 + math.cos(x)**2

# Gaussian
def gaussian(x):
    return math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)

# Pythagorean
def pythagorean(a, b):
    return math.sqrt(a**2 + b**2)
```

---

## 7. Data Flow

```
User types Python function
        │
        ▼
[Generate LaTeX] clicked
        │
        ▼
Dash callback → utils/latex_engine.convert_to_latex(source)
        │
   ┌────┴────────────┐
success            failure
   │                  │
latex string      error message
   │                  │
rendered in       shown in
dcc.Markdown      dbc.Alert
+ raw textarea
```

---

## 8. Acceptance Criteria

| #    | Given                 | When                   | Then                                      |
| ---- | --------------------- | ---------------------- | ----------------------------------------- |
| AC-1 | Valid Python function | User clicks Generate   | LaTeX is rendered correctly               |
| AC-2 | Invalid Python syntax | User clicks Generate   | Red error alert is shown, output clears   |
| AC-3 | Example card clicked  | —                      | Input area is populated with snippet      |
| AC-4 | Generate → then Clear | User clicks Clear      | Both input and output are emptied         |
| AC-5 | Any input             | Page loads             | No error, placeholder shown in input      |
| AC-6 | LaTeX generated       | User clicks Copy LaTeX | Raw LaTeX is copied to clipboard          |
| AC-7 | Light mode active     | User clicks toggle     | UI switches to dark theme; toggle is ON   |
| AC-8 | Dark mode active      | User clicks toggle     | UI switches to light theme; toggle is OFF |

---

## 9. Out of Scope (v1.0)

- User authentication
- Saving / history of past equations
- Support for multi-function inputs
- Export as image (PNG/SVG)
- Natural language → LaTeX (no NLP)
