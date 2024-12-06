import os
import importlib.util

class WindowsModelSelector:
    
    def __init__(self):
        self.options = ["gpt4"]
        self.running = True

    def clear_screen(self):
        os.system('cls')

    def print_menu(self):
        self.clear_screen()
        print("\n" + "=" * 20 + " Agente planificador - Danilo Florez " + "=" * 20 + "\n")
        for idx, option in enumerate(self.options):
            print(f"{idx + 1}. {option}")
        print("\nIngresa el número de la opción para seleccionar, o 0 para salir.")

    def load_model(self, model_name):
        base_directory = os.path.dirname(__file__)
        model_file = model_name.lower().replace("-", "_") + ".py"
        file_path = os.path.join(base_directory, model_file)
        
        try:
            if not os.path.isfile(file_path):
                raise ImportError(f"No se pudo encontrar {file_path}")
            
            spec = importlib.util.spec_from_file_location(model_name, file_path)
            if spec is None:
                raise ImportError(f"No se pudo encontrar {file_path}")
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print(f"\nIniciando {model_name}...")
            
        except ImportError as e:
            print(f"\nError: {str(e)}")
            input("Presiona Enter para continuar...")
        except Exception as e:
            print(f"\nError al cargar el modelo: {str(e)}")
            input("Presiona Enter para continuar...")

    def run(self):
        while self.running:
            self.print_menu()
            choice = input("Selecciona una opción: ")
            
            if choice.isdigit():
                choice = int(choice)
                if choice == 0:
                    self.clear_screen()
                    print("\nSaliendo...")
                    break
                elif choice == 1:
                    selected_model = self.options[choice - 1]
                    self.clear_screen()
                    self.load_model(selected_model)
                    break
                else:
                    print("\nOpción inválida. Inténtalo de nuevo.")
            else:
                print("\nEntrada inválida. Inténtalo de nuevo.")

if __name__ == "__main__":
    selector = WindowsModelSelector()
    selector.run()