import os
import sys

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────
SIZE = 5


# ─────────────────────────────────────────────
#  UTILIDADES DE TERMINAL
# ─────────────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_key():
    input("\n  Presiona Enter para continuar...")


def print_header(title: str = ""):
    print("╔══════════════════════════════════════╗")
    print("║          C O M E   S O L O           ║")
    if title:
        centered = title.center(38)
        print(f"║{centered}║")
    print("╚══════════════════════════════════════╝")
    print()


# ─────────────────────────────────────────────
#  MAPAS DE POSICIÓN  (número ↔ coordenada)
# ─────────────────────────────────────────────
def build_maps(size: int) -> tuple[dict, dict]:
    """Devuelve (pos_map, rev_map).
    pos_map : número → (fila, col)
    rev_map : (fila, col) → número
    """
    pos_map: dict[int, tuple[int, int]] = {}
    rev_map: dict[tuple[int, int], int] = {}
    n = 1
    for i in range(size):
        for j in range(i + 1):
            pos_map[n] = (i, j)
            rev_map[(i, j)] = n
            n += 1
    return pos_map, rev_map


# ─────────────────────────────────────────────
#  TABLERO
# ─────────────────────────────────────────────
def new_board(size: int, empty_pos: int, pos_map: dict) -> list[list[bool]]:
    board = [[True] * (i + 1) for i in range(size)]
    r, c = pos_map[empty_pos]
    board[r][c] = False
    return board


def count_pegs(board: list[list[bool]]) -> int:
    return sum(v for row in board for v in row)


# ─────────────────────────────────────────────
#  MOVIMIENTOS
# ─────────────────────────────────────────────
DIRECTIONS = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]


def is_valid_move(
    board: list[list[bool]],
    fr: int, fc: int,
    tr: int, tc: int,
) -> bool:
    size = len(board)
    if not (0 <= fr < size and 0 <= fc <= fr):
        return False
    if not (0 <= tr < size and 0 <= tc <= tr):
        return False
    if not board[fr][fc] or board[tr][tc]:
        return False
    dr, dc = tr - fr, tc - fc
    if (dr, dc) not in DIRECTIONS:
        return False
    mr, mc = fr + dr // 2, fc + dc // 2
    if not (0 <= mr < size and 0 <= mc <= mr):
        return False
    return board[mr][mc]


def make_move(
    board: list[list[bool]],
    fr: int, fc: int,
    tr: int, tc: int,
) -> list[list[bool]]:
    nb = [row.copy() for row in board]
    dr, dc = tr - fr, tc - fc
    nb[fr][fc] = False
    nb[fr + dr // 2][fc + dc // 2] = False
    nb[tr][tc] = True
    return nb


def get_all_moves(board: list[list[bool]]) -> list[tuple[int, int, int, int]]:
    moves = []
    for i, row in enumerate(board):
        for j, has_peg in enumerate(row):
            if has_peg:
                for dr, dc in DIRECTIONS:
                    tr, tc = i + dr, j + dc
                    if is_valid_move(board, i, j, tr, tc):
                        moves.append((i, j, tr, tc))
    return moves


# ─────────────────────────────────────────────
#  RENDERIZADO
# ─────────────────────────────────────────────
PEG_FULL  = "◉"
PEG_EMPTY = "○"
PEG_FROM  = "◈"   # ficha seleccionada
PEG_TO    = "◎"   # destino posible


def _board_row_str(
    board: list[list[bool]],
    row_idx: int,
    size: int,
    highlight_from: tuple[int, int] | None = None,
    highlight_to: list[tuple[int, int]] | None = None,
) -> str:
    padding = "  " * (size - row_idx - 1)
    cells = []
    for j, has_peg in enumerate(board[row_idx]):
        coord = (row_idx, j)
        if highlight_from and coord == highlight_from:
            cells.append(PEG_FROM)
        elif highlight_to and coord in highlight_to:
            cells.append(PEG_TO)
        elif has_peg:
            cells.append(PEG_FULL)
        else:
            cells.append(PEG_EMPTY)
    return padding + "  ".join(cells)


def print_board(
    board: list[list[bool]],
    rev_map: dict,
    highlight_from: tuple[int, int] | None = None,
    highlight_to: list[tuple[int, int]] | None = None,
):
    size = len(board)
    for i in range(size):
        row_str = _board_row_str(board, i, size, highlight_from, highlight_to)
        print(f"  {row_str}")
    print()
    print(f"  Fichas restantes: {count_pegs(board)}")
    print()


def print_numbered_board(size: int, pos_map: dict, empty: int | None = None):
    """Muestra el tablero con números para elegir posición."""
    rev = {v: k for k, v in pos_map.items()}
    for i in range(size):
        padding = "    " * (size - i - 1)
        cells = []
        for j in range(i + 1):
            n = rev[(i, j)]
            if empty and n == empty:
                cells.append(" ○")
            else:
                cells.append(f"{n:02d}")
        print(f"  {padding}{'   '.join(cells)}")
    print()


# ─────────────────────────────────────────────
#  SOLUCIONADOR  (DFS iterativo con memo)
# ─────────────────────────────────────────────
def board_key(board: list[list[bool]]) -> tuple:
    return tuple(tuple(row) for row in board)


def solve(start_board: list[list[bool]]) -> list[tuple] | None:
    """DFS iterativo. Devuelve lista de movimientos o None si no hay solución."""
    visited: set = set()
    # stack de (tablero, camino)
    stack = [(start_board, [])]

    while stack:
        board, path = stack.pop()

        if count_pegs(board) == 1:
            return path

        key = board_key(board)
        if key in visited:
            continue
        visited.add(key)

        for fr, fc, tr, tc in get_all_moves(board):
            nb = make_move(board, fr, fc, tr, tc)
            stack.append((nb, path + [(fr, fc, tr, tc)]))

    return None


# ─────────────────────────────────────────────
#  FLUJOS DE JUEGO
# ─────────────────────────────────────────────
def choose_empty_position(pos_map: dict, size: int) -> int:
    total = size * (size + 1) // 2
    print_numbered_board(size, pos_map)
    while True:
        raw = input(f"  Posición vacía inicial (1–{total}): ").strip()
        if raw.isdigit():
            n = int(raw)
            if n in pos_map:
                return n
        print(f"  ✗ Ingresa un número entre 1 y {total}.")


def play_manual(
    board: list[list[bool]],
    pos_map: dict,
    rev_map: dict,
):
    """Modo interactivo: el jugador hace los movimientos."""
    history: list[list[list[bool]]] = []

    while True:
        clear_screen()
        print_header("Modo manual")
        print_board(board, rev_map)

        pegs = count_pegs(board)
        moves = get_all_moves(board)

        if pegs == 1:
            print("  ★ ¡GANASTE! Facil y con la zurda.\n")
            wait_for_key()
            return

        if not moves:
            print(f"  ✗ Ni modo suerte la proxima. Quedan {pegs} fichas.\n")
            wait_for_key()
            return

        print("  Comandos:  <desde> <hasta>  |  u = deshacer  |  q = salir")
        print("  (usa los números de posición)\n")
        raw = input("  > ").strip().lower()

        if raw == "q":
            return
        if raw == "u":
            if history:
                board = history.pop()
            else:
                print("  No hay movimientos para deshacer, no has hecho nada.")
                wait_for_key()
            continue

        parts = raw.split()
        if len(parts) != 2 or not all(p.isdigit() for p in parts):
            print("  ✗ Formato inválido :/.")
            wait_for_key()
            continue

        fn, tn = int(parts[0]), int(parts[1])
        if fn not in pos_map or tn not in pos_map:
            print("  ✗ No se puede bro.")
            wait_for_key()
            continue

        fr, fc = pos_map[fn]
        tr, tc = pos_map[tn]

        if not is_valid_move(board, fr, fc, tr, tc):
            print("  ✗ Tas mal, eso no se vale.")
            wait_for_key()
            continue

        history.append([row.copy() for row in board])
        board = make_move(board, fr, fc, tr, tc)


def show_solution(
    board: list[list[bool]],
    solution: list[tuple],
    rev_map: dict,
):
    """Muestra la solución paso a paso."""
    current = [row.copy() for row in board]
    step = 0

    clear_screen()
    print_header("Solución — estado base")
    print_board(current, rev_map)
    wait_for_key()

    summary = []

    for fr, fc, tr, tc in solution:
        step += 1
        fn = rev_map[(fr, fc)]
        tn = rev_map[(tr, tc)]
        summary.append(f"  {step:02d}. {fn:02d} → {tn:02d}")

        current = make_move(current, fr, fc, tr, tc)

        clear_screen()
        print_header(f"Movimiento {step} de {len(solution)}")
        print(f"  {fn:02d} → {tn:02d}\n")
        print_board(current, rev_map)
        wait_for_key()

    # Resumen final
    clear_screen()
    print_header("Resumen de movimientos")
    for line in summary:
        print(line)
    print()
    if count_pegs(current) == 1:
        print("  ★ ¡Solución completada con 1 ficha restante!\n")
    wait_for_key()


# ─────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────────
def main_menu() -> str:
    print("  1. No skill EZ (Auto)")
    print("  2. Estandar como los carritos")
    print("  3. Bye Bye")
    print()
    while True:
        opt = input("  Opción: ").strip()
        if opt in ("1", "2", "3"):
            return opt
        print("  ✗ Elige 1, 2 o 3.")


def main():
    pos_map, rev_map = build_maps(SIZE)

    while True:
        clear_screen()
        print_header()
        opt = main_menu()

        if opt == "3":
            clear_screen()
            print("  ¡Hasta la proximaaaaa \(°o°)/!\n")
            sys.exit(0)

        # ── Elegir posición vacía
        clear_screen()
        print_header("Elige posición vacía")
        empty = choose_empty_position(pos_map, SIZE)
        board = new_board(SIZE, empty, pos_map)

        if opt == "2":
            play_manual(board, pos_map, rev_map)
            continue

        # ── Resolver automáticamente
        clear_screen()
        print_header("Pensando a niveles descomunales…")
        print_board(board, rev_map)
        print("  Ya casi, no son enchiladas…\n")

        solution = solve(board)

        if solution is None:
            print("  ✗ Ni modo no pude :c (Sin solucion).\n")
            wait_for_key()
            continue

        print(f"  ✔ Estuvo tan facil que solo me tomo:  {len(solution)} movimientos.\n")
        wait_for_key()
        show_solution(board, solution, rev_map)


if __name__ == "__main__":
    main()