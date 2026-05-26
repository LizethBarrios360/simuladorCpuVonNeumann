import tkinter as tk
from tkinter import ttk, messagebox
import time

class VonNeumannSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de CPU Von Neumann - Material de Apoyo UTP")
        self.root.geometry("900x650")
        self.root.configure(bg="#2c3e50")

        # --- Componentes de la Arquitectura Von Neumann ---
        self.memory = [0] * 16  # Memoria de 16 posiciones (0 a 15)
        self.PC = 0             # Program Counter (Contador de Programa)
        self.MAR = 0            # Memory Address Register
        self.MBR = 0            # Memory Buffer Register
        self.IR = "NOP"         # Instruction Register (Registro de Instrucción)
        self.AC = 0             # Accumulator (Acumulador de la ALU)
        
        # Estado de simulación
        self.step_phase = "FETCH" # Fases: FETCH -> DECODE -> EXECUTE
        self.current_instruction = ""
        
        # Inicializar memoria con un programa básico por defecto:
        self.memory[0] = "LDA 12"  # Cargar dirección 12 en AC
        self.memory[1] = "ADD 13"  # Sumar dirección 13 al AC
        self.memory[2] = "STA 14"  # Guardar AC en dirección 14
        self.memory[3] = "HLT"     # Detener programa
        self.memory[12] = 5        # Dato 1
        self.memory[13] = 10       # Dato 2

        self.create_widgets()
        self.update_ui_values()

    def create_widgets(self):
        # Título Principal
        title_label = tk.Label(self.root, text="SIMULADOR DE CPU VON NEUMANN (PASO A PASO)", 
                               font=("Arial", 16, "bold"), fg="#ecf0f1", bg="#2c3e50")
        title_label.pack(pady=10)

        # Contenedor Principal (Paneles)
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- PANEL IZQUIERDO: CPU (Registros y ALU) ---
        cpu_frame = tk.LabelFrame(main_frame, text=" CENTRAL PROCESSING UNIT (CPU) ", 
                                  font=("Arial", 12, "bold"), fg="#e74c3c", bg="#34495e", bd=3)
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Registros básicos de la CPU
        self.lbl_pc = self.create_register_row(cpu_frame, "Program Counter (PC):", "Muestra la dirección de la siguiente instrucción.")
        self.lbl_mar = self.create_register_row(cpu_frame, "Memory Addr Reg (MAR):", "Contiene la dirección de memoria a leer/escribir.")
        self.lbl_mbr = self.create_register_row(cpu_frame, "Memory Buff Reg (MBR):", "Almacena el dato/instrucción leído o a escribir.")
        self.lbl_ir = self.create_register_row(cpu_frame, "Instruction Reg (IR):", "Guarda la instrucción actual que se va a decodificar.")
        
        # ALU & Acumulador
        alu_frame = tk.LabelFrame(cpu_frame, text=" Arithmetic / Logic Unit (ALU) ", 
                                  font=("Arial", 10, "bold"), fg="#f1c40f", bg="#2c3e50")
        alu_frame.pack(fill=tk.X, expand=True, padx=10, pady=15)
        
        self.lbl_ac = self.create_register_row(alu_frame, "Accumulator (AC):", "Registro intermedio para operaciones de la ALU.")

        # --- PANEL DERECHO: MEMORIA PRINCIPAL ---
        mem_frame = tk.LabelFrame(main_frame, text=" MAIN MEMORY (RAM) ", 
                                  font=("Arial", 12, "bold"), fg="#2ecc71", bg="#34495e", bd=3)
        mem_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

        self.mem_cells = []
        for i in range(16):
            cell_frame = tk.Frame(mem_frame, bg="#34495e")
            cell_frame.pack(fill=tk.X, padx=5, pady=2)
            
            lbl_addr = tk.Label(cell_frame, text=f"[{i:02d}]", font=("Courier", 10, "bold"), fg="#bdc3c7", bg="#34495e", width=5)
            lbl_addr.pack(side=tk.LEFT)
            
            lbl_val = tk.Label(cell_frame, text=str(self.memory[i]), font=("Courier", 10, "bold"), fg="#000000", bg="#ecf0f1", width=12, relief="sunken")
            lbl_val.pack(side=tk.LEFT, padx=5)
            self.mem_cells.append(lbl_val)

        # --- PANEL INFERIOR: UNIDAD DE CONTROL ---
        control_frame = tk.LabelFrame(self.root, text=" UNIDAD DE CONTROL (ESTADO Y ACCIONES) ", 
                                      font=("Arial", 11, "bold"), fg="#3498db", bg="#34495e", bd=2)
        control_frame.pack(fill=tk.X, padx=30, pady=15)

        self.lbl_status = tk.Label(control_frame, text="Fase actual del ciclo: FETCH (Siguiente paso: Captar instrucción)", 
                                   font=("Arial", 11, "bold"), fg="#f39c12", bg="#34495e")
        self.lbl_status.pack(pady=5)

        btn_step = tk.Button(control_frame, text="Siguiente Paso del Ciclo", font=("Arial", 10, "bold"), 
                             bg="#2ecc71", fg="white", command=self.execute_next_step, height=2, width=25)
        btn_step.pack(side=tk.LEFT, padx=40, pady=5)

        btn_reset = tk.Button(control_frame, text="Reiniciar Simulador", font=("Arial", 10, "bold"), 
                              bg="#e74c3c", fg="white", command=self.reset_simulator, height=2, width=15)
        btn_reset.pack(side=tk.RIGHT, padx=40, pady=5)

    def create_register_row(self, parent, name, desc):
        frame = tk.Frame(parent, bg=parent.cget("bg"))
        frame.pack(fill=tk.X, padx=10, pady=6)
        
        lbl_name = tk.Label(frame, text=name, font=("Arial", 10, "bold"), fg="#ecf0f1", bg=parent.cget("bg"), width=20, anchor="w")
        lbl_name.pack(side=tk.LEFT)
        
        lbl_val = tk.Label(frame, text="0", font=("Courier", 12, "bold"), fg="#2c3e50", bg="#ecf0f1", width=10, relief="raised")
        lbl_val.pack(side=tk.LEFT, padx=5)
        
        lbl_desc = tk.Label(frame, text=desc, font=("Arial", 8, "italic"), fg="#b2bec3", bg=parent.cget("bg"))
        lbl_desc.pack(side=tk.LEFT, padx=10)
        
        return lbl_val

    def update_ui_values(self):
        self.lbl_pc.config(text=str(self.PC))
        self.lbl_mar.config(text=str(self.MAR))
        self.lbl_mbr.config(text=str(self.MBR))
        self.lbl_ir.config(text=str(self.IR))
        self.lbl_ac.config(text=str(self.AC))
        
        for i in range(16):
            self.mem_cells[i].config(text=str(self.memory[i]), bg="#ecf0f1", fg="#000000")
        
        if self.PC < 16:
            self.mem_cells[self.PC].config(bg="#ffeaa7")

    def flash_widget(self, widget, color="#ff7675"):
        original_color = widget.cget("bg")
        widget.config(bg=color)
        self.root.update()
        time.sleep(0.2)
        widget.config(bg=original_color)

    def execute_next_step(self):
        if self.step_phase == "FETCH":
            if self.PC >= 16:
                messagebox.showinfo("Fin", "El PC ha alcanzado el límite de memoria.")
                return
            
            self.MAR = self.PC
            self.flash_widget(self.lbl_pc)
            self.flash_widget(self.lbl_mar, "#74b9ff")
            
            self.MBR = self.memory[self.MAR]
            self.flash_widget(self.mem_cells[self.MAR], "#74b9ff")
            self.flash_widget(self.lbl_mbr, "#74b9ff")
            
            self.lbl_status.config(text=f"Fase: DECODE -> Instrucción '{self.MBR}' leída. Lista para analizar.")
            self.step_phase = "DECODE"
            self.update_ui_values()
            
        elif self.step_phase == "DECODE":
            self.IR = self.MBR
            self.flash_widget(self.lbl_mbr)
            self.flash_widget(self.lbl_ir, "#fdcb6e")
            
            self.PC += 1
            
            self.lbl_status.config(text=f"Fase: EXECUTE -> Instrucción '{self.IR}' decodificada. Lista para ejecutarse.")
            self.step_phase = "EXECUTE"
            self.update_ui_values()
            
        elif self.step_phase == "EXECUTE":
            inst = self.IR
            self.flash_widget(self.lbl_ir)
            
            if inst == "NOP":
                self.lbl_status.config(text="Ejecutado: NOP (No operación). Siguiente fase: FETCH.")
            elif inst == "HLT":
                self.lbl_status.config(text="PROGRAMA FINALIZADO CON ÉXITO (Instrucción HLT detectada).")
                messagebox.showinfo("HLT", "El simulador ha encontrado la instrucción de parada (HLT).")
                self.step_phase = "FINISHED"
                self.update_ui_values()
                return
            else:
                try:
                    parts = inst.split()
                    opcode = parts[0]
                    operand = int(parts[1])
                    
                    if opcode == "LDA":
                        self.MAR = operand
                        self.MBR = self.memory[self.MAR]
                        self.AC = int(self.MBR)
                        self.flash_widget(self.mem_cells[operand], "#2ecc71")
                        self.flash_widget(self.lbl_ac, "#2ecc71")
                        self.lbl_status.config(text=f"Ejecutado: Cargar en AC el valor {self.AC} de la dirección {operand}.")
                        
                    elif opcode == "ADD":
                        self.MAR = operand
                        self.MBR = self.memory[self.MAR]
                        viejos_datos = self.AC
                        self.AC += int(self.MBR)
                        self.flash_widget(self.mem_cells[operand], "#f1c40f")
                        self.flash_widget(self.lbl_ac, "#f1c40f")
                        self.lbl_status.config(text=f"Ejecutado (ALU): Sumar {viejos_datos} + {self.MBR} = {self.AC}.")
                        
                    elif opcode == "STA":
                        self.MAR = operand
                        self.memory[self.MAR] = self.AC
                        self.flash_widget(self.lbl_ac, "#e74c3c")
                        self.flash_widget(self.mem_cells[operand], "#e74c3c")
                        self.lbl_status.config(text=f"Ejecutado: Guardado el valor {self.AC} en la dirección de memoria {operand}.")
                    else:
                        raise ValueError
                except:
                    messagebox.showerror("Error", f"Error de sintaxis o ejecución en la instrucción: '{inst}'")
            
            if self.step_phase != "FINISHED":
                self.step_phase = "FETCH"
                self.update_ui_values()

    def reset_simulator(self):
        self.memory = [0] * 16
        self.PC = 0
        self.MAR = 0
        self.MBR = 0
        self.IR = "NOP"
        self.AC = 0
        self.step_phase = "FETCH"
        
        self.memory[0] = "LDA 12"
        self.memory[1] = "ADD 13"
        self.memory[2] = "STA 14"
        self.memory[3] = "HLT"
        self.memory[12] = 5
        self.memory[13] = 10
        
        self.lbl_status.config(text="Simulador reiniciado. Fase actual del ciclo: FETCH")
        self.update_ui_values()

if __name__ == "__main__":
    root = tk.Tk()
    app = VonNeumannSimulator(root)
    root.mainloop()