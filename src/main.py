from textnode import TextNode, TextType

def main():
    tn = TextNode("Hello, World!", TextType.TEXT, "https://www.boot.dev")
    print(tn)

if __name__ == "__main__":
    main()