import os
import time

class TuringMachine:
    def __init__(self):
        # Definir los estados y el estado inicial
        self.states = {'q0': 0, 'q1': 1, 'q2': 2, 'q3': 3, 'q4': 4, 'q5': 5, 'q6': 6}
        self.current_state = 'q0'
        self.final_states = ['q6']  # Estados finales
        self.transitions = {
            ('q0', 'a'): ('q1', 'a', 'R'),
            ('q1', 'b'): ('q2', 'b', 'R'),
            ('q2', 'a'): ('q3', 'a', 'R'),
            ('q3', 'a'): ('q1', 'a', 'R'),
            ('q3', 'b'): ('q4', 'b', 'R'),
            ('q4', '#'): ('q5', '#', 'R'),
            ('q5', 'a'): ('q5', 'a', 'R'),
            ('q5', 'b'): ('q5', 'b', 'R'),
            ('q5', '*'): ('q6', '*', 'R'),
        }
        self.transition_log = []  # Almacena las transiciones
        self.tape1 = []
        self.tape2 = []
        self.head1 = 0
        self.head2 = 0

    def reset(self, input_string):
        """Reiniciar la máquina de Turing al estado inicial."""
        self.current_state = 'q0'
        self.transition_log.clear()
        self.tape1 = list(input_string)
        self.tape2 = list(input_string)
        self.head1 = 0
        self.head2 = 0

    def transition(self, symbol):
        """Realizar una transición dado un símbolo y mover las cintas."""
        try:
            new_state, write_symbol, move = self.transitions[(self.current_state, symbol)]
            self.transition_log.append((self.current_state, symbol, new_state))
            self.current_state = new_state

            # Escribir el símbolo en las cintas
            self.tape1[self.head1] = write_symbol
            self.tape2[self.head2] = write_symbol

            # Mover las cabezas de lectura según el movimiento indicado (R para derecha)
            self.head1 += 1 if move == 'R' else -1
            self.head2 += 1 if move == 'R' else -1
        except KeyError:
            self.current_state = None  # Transición inválida

    def is_valid(self):
        """Comprobar si el estado actual es un estado final."""
        return self.current_state in self.final_states

    def process_string(self, input_string):
        """Procesar una cadena a través de la máquina de Turing."""
        self.reset(input_string)
        for symbol in input_string:
            self.transition(symbol)
            if self.current_state is None:
                break
        return self.is_valid()

    def display_turing_machine(self):
        """Mostrar la simbología de la máquina de Turing."""
        print("Máquina de Turing:")
        print(f"M = (Q, Σ, Γ, δ, q0, F)")
        print("Q = {q0, q1, q2, q3, q4, q5, q6}")
        print("Σ = {a, b, #, *}")
        print("Γ = {a, b, #, *, _}")
        print("δ = conjunto de transiciones")
        print("q0 = q0 (estado inicial)")
        print("F = {q6} (estado final)")

    def build_derivation_tree(self, input_string, level=0):
        """Construir el árbol de derivación para una cadena, con indentación para simular una estructura de árbol."""
        tree = []
        self.reset(input_string)
        
        for symbol in input_string:
            if self.current_state is None:
                break
            new_state = self.transitions.get((self.current_state, symbol), (None, '_', '_'))[0]
            # Agregar indentación en función del nivel para crear la estructura de árbol
            tree.append("    " * level + f"{self.current_state} --({symbol})--> {new_state}")
            self.transition(symbol)
            level += 1  # Incrementar el nivel para la próxima transición
        
        return tree

    def build_derivation_table(self, input_string):
        """Construir la tabla de derivación."""
        table = []
        self.reset(input_string)
        for symbol in input_string:
            if self.current_state is None:
                break
            current = self.current_state
            new_state = self.transitions.get((current, symbol), (None, '_', '_'))[0]
            table.append([current, symbol, new_state])
            self.transition(symbol)
        return table

    def simulate_stack(self, input_string):
        """Simular una pila para el procesamiento de la cadena."""
        stack = []
        self.reset(input_string)
        for symbol in input_string:
            # Push al carácter en la pila
            stack.append(symbol)
            print(f"Push: {symbol}, Pila: {stack}")

            # Pop del carácter de la pila cuando se procesa
            stack.pop()
            print(f"Pop: {symbol}, Pila: {stack}")

    def simulate(self, input_string):
        """Simular la máquina de Turing mostrando el proceso en dos cintas."""
        print("\nIniciando simulación de la Máquina de Turing con dos cintas:")
        self.reset(input_string)
        
        while self.current_state is not None and self.head1 < len(self.tape1) and self.head2 < len(self.tape2):
            print(f"\nEstado actual: {self.current_state}")
            
            # Mostrar la posición de la cabeza en cada cinta con los contenidos actuales
            tape1_display = ''.join(self.tape1)
            tape2_display = ''.join(self.tape2)
            print(f"Cinta 1: {tape1_display} | Cabeza en posición {self.head1}")
            print(f"Cinta 2: {tape2_display} | Cabeza en posición {self.head2}")

            # Realizar la transición en la máquina de Turing
            self.transition(self.tape1[self.head1])

            # Verificar si las cabezas se salen de los límites después del movimiento
            if self.head1 >= len(self.tape1):
                print("La cabeza de la cinta 1 ha salido de los límites de la cinta.")
                break
            if self.head2 >= len(self.tape2):
                print("La cabeza de la cinta 2 ha salido de los límites de la cinta.")
                break

        # Mostrar el resultado final
        if self.is_valid():
            print("\nCadena aceptada.")
        else:
            print("\nCadena rechazada.")

# Ejecución del procesamiento de cadenas con la máquina de Turing
def process_strings(file_path):
    """Procesar cadenas del archivo usando la máquina de Turing."""
    turing_machine = TuringMachine()
    strings = read_strings_from_file(file_path)

    for string in strings:
        clear_console()  # Limpiar la consola antes de mostrar cada cadena
        print(f"\nProcesando cadena: {string}")
        turing_machine.display_turing_machine()
        
        # Mostrar árbol de derivación
        derivation_tree = turing_machine.build_derivation_tree(string)
        print("\nÁrbol de derivación:")
        for step in derivation_tree:
            print(step)

        # Mostrar tabla de derivación
        derivation_table = turing_machine.build_derivation_table(string)
        print("\nTabla de derivación:")
        for row in derivation_table:
            print(row)

        # Simulación de la pila
        print("\nSimulación de la pila:")
        turing_machine.simulate_stack(string)

        # Simulación de la máquina de Turing
        turing_machine.simulate(string)

        # Espera a que el usuario presione "Enter" antes de continuar
        input("\nPresiona 'Enter' para continuar a la siguiente cadena...")
        time.sleep(0.5)

# Funciones auxiliares para leer cadenas desde un archivo y limpiar la consola
def read_strings_from_file(file_path):
    with open(file_path, 'r') as file:
        strings = file.read().splitlines()
    return strings

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Cambiar la ruta del archivo si es necesario
file_path = r"C:\Users\evolu\OneDrive\Documentos\Esly U\Segundo Semestre 2024\Lenguajes Formales y Autómatas\automaton_strings.txt"
process_strings(file_path)
