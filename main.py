from utils import show_file, list_local_archives, ensure_key_file
from encrypt_file import encrypt_menu
from decrypt_file import decrypt_menu

def menu():
    key = ensure_key_file()
    if not key:
        print("Não foi possível carregar ou gerar a chave. Verifique o arquivo.")
        return

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1) Encriptar arquivo")
        print("2) Decriptar arquivo")
        print("3) Mostrar conteudo de arquivo")
        print("4) Listar arquivos locais")
        print("0) Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '0':
            print("Saindo...")
            break
        elif escolha == '1':
            encrypt_menu(key)  # ✅ usa a função do módulo, não o módulo como função
        elif escolha == '2':
            decrypt_menu(key)
        elif escolha == '3':
            fname = input("Arquivo a ser mostrado: ").strip()
            show_file(fname)
        elif escolha == '4':
            list_local_archives()
        else:
            print("Opção inválida, tente novamente.")

if __name__ == '__main__':
    menu()
