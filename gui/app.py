import tkinter as tk
from tkinter import messagebox
import time
import threading
import os

from solver_sat.core import resolver_com_sat, gerar_tabuleiro_inicial
from gui.image_handler import load_and_slice_image

GRID_SIZE_PX = 360
MAX_STEPS_SOLVER = 25

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'puzzle_image.png')

class EightPuzzleSAT_GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8-Puzzle Solver (SAT)")
        self.resizable(False, False)

        self.image_pieces = load_and_slice_image(IMAGE_PATH, GRID_SIZE_PX)

        if not self.image_pieces:
            self.destroy()
            return
            
        self.tiles = {}
        self.initial_state_2d = None
        self.current_state_2d = None
        self.solution_result = None

        self._create_widgets()
        self.shuffle_puzzle()

    def _create_widgets(self):
        puzzle_frame = tk.Frame(self, bg="#BBB", bd=4)
        puzzle_frame.grid(row=0, column=0, padx=10, pady=10)
        for i in range(9):
            row, col = divmod(i, 3)
            tile = tk.Label(puzzle_frame, bg="#CCC", relief="raised", bd=2)
            tile.grid(row=row, column=col, padx=1, pady=1)
            self.tiles[i] = tile
        
        control_frame = tk.Frame(self)
        control_frame.grid(row=1, column=0, pady=5)
        self.shuffle_button = tk.Button(control_frame, text="Embaralhar", font=("Helvetica", 12), command=self.shuffle_puzzle)
        self.shuffle_button.pack(side="left", padx=10)
        self.solve_button = tk.Button(control_frame, text="Resolver (SAT)", font=("Helvetica", 12), command=self.start_solver)
        self.solve_button.pack(side="left", padx=10)

        self.status_label = tk.Label(self, text="Clique em 'Embaralhar' para começar.", font=("Helvetica", 12))
        self.status_label.grid(row=2, column=0, pady=5)
        self.info_label = tk.Label(self, text=f"Solver tentará até {MAX_STEPS_SOLVER-1} movimentos.", font=("Helvetica", 10, "italic"))
        self.info_label.grid(row=3, column=0, pady=5)

    def update_grid(self):
        flat_state = [item for sublist in self.current_state_2d for item in sublist]
        for i, tile_value in enumerate(flat_state):
            tile_widget = self.tiles[i]
            if tile_value == 0:
                tile_widget.config(image='', bg="#CCC", relief="sunken")
            else:
                image_piece = self.image_pieces.get(tile_value) # Use .get para segurança
                if image_piece:
                    tile_widget.config(image=image_piece, relief="raised")
                    tile_widget.image = image_piece
        self.update_idletasks()
        
    def shuffle_puzzle(self):
        self.initial_state_2d = gerar_tabuleiro_inicial()
        self.current_state_2d = [row[:] for row in self.initial_state_2d]
        self.update_grid()
        self.status_label.config(text="Pronto para resolver!")
        self.info_label.config(text=f"Solver tentará até {MAX_STEPS_SOLVER-1} movimentos.")
        self.solve_button.config(state="normal")
        self.shuffle_button.config(state="normal")
    
    def start_solver(self):
        self.status_label.config(text="Resolvendo... O Solver SAT está pensando...")
        self.info_label.config(text="Isso pode demorar alguns segundos...")
        self.solve_button.config(state="disabled")
        self.shuffle_button.config(state="disabled")
        self.update_idletasks()
        
        self.solution_result = "pending"
        solver_thread = threading.Thread(target=self._run_solver_thread, daemon=True)
        solver_thread.start()
        self._check_solver_result()

    def _run_solver_thread(self):
        start_time = time.time()
        solution_moves, num_steps = resolver_com_sat(self.initial_state_2d, MAX_STEPS_SOLVER)
        end_time = time.time()
        if solution_moves:
            self.solution_result = {
                "moves": solution_moves,
                "steps": len(solution_moves),
                "time": end_time - start_time
            }
        else:
            self.solution_result = None

    def _check_solver_result(self):
        if self.solution_result == "pending":
            self.after(200, self._check_solver_result)
        elif self.solution_result is None:
            messagebox.showerror("Sem Solução", f"O solver não encontrou solução em {MAX_STEPS_SOLVER-1} movimentos.")
            self.shuffle_puzzle()
        else:
            info = self.solution_result
            self.info_label.config(text=f"Solução encontrada em {info['steps']} movimentos.\n"
                                        f"Tempo: {info['time']:.3f}s")
            self._animate_solution(info['moves'])

    def _animate_solution(self, moves_dict):
        sorted_moves = sorted(moves_dict.items())
        if not sorted_moves:
            self.status_label.config(text="Resolvido!")
            self.shuffle_button.config(state="normal")
            return
        
        _passo, direcao = sorted_moves.pop(0)
        
        lin_vazio, col_vazio = -1, -1
        for r, row in enumerate(self.current_state_2d):
            if 0 in row:
                lin_vazio, col_vazio = r, row.index(0)
                break
        
        if direcao == 'C': lin_vizinho, col_vizinho = lin_vazio - 1, col_vazio
        elif direcao == 'B': lin_vizinho, col_vizinho = lin_vazio + 1, col_vazio
        elif direcao == 'E': lin_vizinho, col_vizinho = lin_vazio, col_vazio - 1
        else: lin_vizinho, col_vizinho = lin_vazio, col_vazio + 1
        
        self.current_state_2d[lin_vazio][col_vazio], self.current_state_2d[lin_vizinho][col_vizinho] = \
            self.current_state_2d[lin_vizinho][col_vizinho], self.current_state_2d[lin_vazio][col_vazio]
        
        self.update_grid()
        self.after(400, lambda: self._animate_solution(dict(sorted_moves)))