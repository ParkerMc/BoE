import chat, sys
if __name__ == "__main__":
    if "-t" in sys.argv: chat.bash()
    else: chat.main()
