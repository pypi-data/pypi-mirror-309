from rich.prompt import Prompt
from rich.console import Console

def encode_name_to_numbers(name):
    return [ord(char.lower()) - 96 for char in name if char.isalpha()]

def main():
    console = Console()
    name = Prompt.ask("Enter your name to encode")
    encoded = encode_name_to_numbers(name)
    console.print(f"Encoded Name: {encoded}")

if __name__ == "__main__":
    main()
