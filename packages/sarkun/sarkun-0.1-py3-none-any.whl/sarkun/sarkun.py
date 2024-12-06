import argparse
import pyfiglet
import sys
import time
from colorama import init, Fore, Back, Style
import emoji

# Initialize colorama
init(autoreset=True)

# Function to print the title with figlet and color
def print_banner(text):
    banner = pyfiglet.figlet_format(text, font="slant")
    print(Fore.CYAN + banner)  # Cyan colored banner

# Function to display community information with icons and colors
def community_info():
    print(Fore.GREEN + emoji.emojize(":globe_with_meridians:") + " Welcome to the Cybersecurity & Network Community Tool!")
    print(Fore.YELLOW + "\nThis tool helps you access community info, news, and more.")
    print(Fore.LIGHTBLUE_EX + "Stay connected and informed. Our community is a space for knowledge exchange, security discussions, and collaboration.")
    print(Fore.MAGENTA + "\nFollow us on: @sarkunsec")
    print(Fore.CYAN + "Join us at: https://sarkun.com")
    print(Fore.WHITE + "For support, email us: support@sarkun.com")

# Function to check network status (dummy function with color and icon)
def check_network_status():
    print(Fore.GREEN + emoji.emojize(":desktop_computer:") + " Checking network status...")
    time.sleep(2)  # Simulate checking network status
    print(Fore.GREEN + "[✔] Network status: OK - All systems are operational.\n")

# Function to display recent cybersecurity news (dummy data with color and icons)
def display_news():
    print(Fore.LIGHTYELLOW_EX + emoji.emojize(":newspaper:") + " Recent Cybersecurity News:")
    news_items = [
        "Zero-Day Exploit Found in Major Web Framework!",
        "Ransomware Attacks Rise: Here's What You Need to Know.",
        "New Networking Protocols: What They Mean for Cybersecurity."
    ]
    
    for idx, item in enumerate(news_items, 1):
        print(Fore.CYAN + f"{idx}. {item}")

# Function to display help message with icons and color
def show_help():
    print(Fore.MAGENTA + emoji.emojize(":question:") + " Available commands:")
    print(Fore.YELLOW + "  - " + Fore.CYAN + "info" + Fore.WHITE + "                Show community info")
    print(Fore.YELLOW + "  - " + Fore.CYAN + "network-status" + Fore.WHITE + "      Check network status")
    print(Fore.YELLOW + "  - " + Fore.CYAN + "news" + Fore.WHITE + "                Display recent cybersecurity news")
    print(Fore.YELLOW + "  - " + Fore.CYAN + "help" + Fore.WHITE + "                Show this help message\n")

# Main function to parse arguments and execute the appropriate command
def main():
    parser = argparse.ArgumentParser(description="Cybersecurity & Network Community Tool")

    # Add arguments
    parser.add_argument('command', choices=['info', 'network-status', 'news', 'help'], help="Command to run")

    # Parse the arguments
    args = parser.parse_args()

    # Print banner
    print_banner("SARKUN")

    # Execute based on the command provided
    if args.command == 'info':
        community_info()
    elif args.command == 'network-status':
        check_network_status()
    elif args.command == 'news':
        display_news()
    elif args.command == 'help':
        show_help()

# Entry point
if __name__ == "__main__":
    main()
