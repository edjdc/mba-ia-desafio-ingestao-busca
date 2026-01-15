import sys
import os

# Add root directory to sys.path to allow imports from src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.search import search_prompt

def main():
    print("\nBem-vindo ao Chat de Busca Semântica!")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            print("Faça sua pergunta:")
            pergunta = input().strip()

            if not pergunta:
                continue

            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("Encerrando...")
                break

            print(f"\nPERGUNTA: {pergunta}")
            
            # Simple loading indicator
            sys.stdout.write("Processando...")
            sys.stdout.flush()
            
            resposta = search_prompt(pergunta)
            
            # Clear loading line
            sys.stdout.write("\r" + " " * 20 + "\r")
            
            print(f"RESPOSTA: {resposta}\n")
            print("-" * 30 + "\n")

        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}\n")

if __name__ == "__main__":
    main()