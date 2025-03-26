import textnode as tn

def main():

    dummy = tn.TextNode("some text", tn.TextType.LINKS, "https://google.com")
    print(dummy)

if __name__ == "__main__":
    main()