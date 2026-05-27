from search import search_prompt


def main():
    print("Chat iniciado. Digite 'sair' para encerrar.\n")

    while True:
        question = input("PERGUNTA: ")

        if question.lower() in ["sair", "exit", "quit"]:
            print("Chat encerrado.")
            break

        answer = search_prompt(question) 
        print(f"RESPOSTA: {answer}\n")


if __name__ == "__main__":
    main()