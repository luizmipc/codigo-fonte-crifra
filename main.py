# Importações de funções utilitárias e menus específicos
import sys
sys.dont_write_bytecode = True
from utils import show_file, list_local_archives, ensure_key_file
from encrypt_file import encrypt_menu
from decrypt_file import decrypt_menu

def menu():
    """
    Função principal que exibe o menu e lida com as opções do usuário.
    Antes de qualquer operação, garante que a chave esteja disponível.
    """
    # Tenta carregar ou gerar a chave de criptografia
    key = None
    user_key = None
    while True:
        user_key = input("Forneça uma chave (8 dígitos hex, vazio para gerar): ").strip()
        if user_key == "":
            # Usuário quer gerar/usar chave automática
            key = ensure_key_file()
            if key is not None:
                break
            else:
                print("Erro ao gerar ou carregar chave automática. Tente novamente.")
        else:
            key = ensure_key_file(user_key)
            if key is not None:
                break
            else:
                print("Chave inválida. Tente novamente.")
        if not key:
            print("Não foi possível carregar ou gerar a chave. Verifique o arquivo.")
            return  # Encerra caso não consiga obter uma chave válida

    # Loop principal do menu
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1) Encriptar arquivo")
        print("2) Decriptar arquivo")
        print("3) Mostrar conteúdo de arquivo")
        print("4) Listar arquivos locais")
        print("0) Sair")
        escolha = input("Escolha uma opção: ").strip()  # Lê e remove espaços extras

        # Encerrar o programa
        if escolha == '0':
            print("Saindo...")
            break
        # Opção de encriptação
        elif escolha == '1':
            encrypt_menu(key)
        # Opção de decriptação
        elif escolha == '2':
            decrypt_menu(key)
        # Opção para visualizar o conteúdo de um arquivo como texto
        elif escolha == '3':
            show_file()
        # Opção para listar os arquivos disponíveis na pasta `files/`
        elif escolha == '4':
            list_local_archives()

        # Caso a entrada não seja reconhecida
        else:
            print("Opção inválida, tente novamente.")

# Ponto de entrada do script: executa o menu se for chamado diretamente
if __name__ == '__main__':
    menu()
