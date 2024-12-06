import os
import typer
import sys
from pc_builder.components.gpu import loadGPUsfromJSON
from pc_builder.components.psu import loadPSUsfromJSON
from pc_builder.components.motherboard import loadMBsfromJSON
from pc_builder.components.cpu import loadCPUsfromJSON
from pc_builder.components.cpucooler import loadCPUCoolersfromJSON
from pc_builder.components.ram import loadRAMsfromJSON
from pc_builder.components.ssd import loadSSDsfromJSON
from pc_builder.components.hdd import loadHDDsfromJSON
from pc_builder.components.case import loadCasesfromJSON
from pc_builder.suggestions.cpu import suggestCompatibleCPUs
from pc_builder.suggestions.cpucooler import suggestCompatibleCPUcoolers
from pc_builder.suggestions.gpu import suggestCompatibleGPUs
from pc_builder.suggestions.motherboard import suggestCompatibleMotherboards
from pc_builder.suggestions.psu import suggestCompatiblePSUs
from pc_builder.suggestions.case import suggestCompatibleCases
from pc_builder.suggestions.ram import suggestCompatibleRAMs
from pc_builder.suggestions.ssd import suggestCompatibleSSDs
from pc_builder.suggestions.hdd import suggestCompatibleHDDs


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


app = typer.Typer()


class UserPC:
    def __init__(self):
        self.components = {
            "gpu": [],
            "psu": [],
            "motherboard": [],
            "cpu": [],
            "cpucooler": [],
            "ram": [],
            "ssd": [],
            "hdd": [],
            "case": [],
        }
        self.total_price = 0.0

    def add_component(self, component_type, part):
        price = float(part.price.replace("€", "").replace("$", "").strip())
        self.components[component_type].append(part)
        self.total_price += price

    def remove_component(self, component_type, index):
        if component_type in self.components and index < len(
            self.components[component_type]
        ):
            price = float(
                self.components[component_type][index]
                .price.replace("€", "")
                .replace("$", "")
                .strip()
            )
            self.total_price -= price
            del self.components[component_type][index]

    def display(self):
        # Define the order of components to be displayed
        display_order = [
            "gpu",
            "cpu",
            "cpucooler",
            "motherboard",
            "case",
            "psu",
        ]

        # Display the components in the defined order
        for component_type in display_order:
            if self.components[component_type]:
                for part in self.components[component_type]:
                    typer.echo(
                        f"{component_type.upper()}: {clean_name(part.name)} - {part.price}"
                    )

        # Display the MEMORY section
        ram_parts = self.components["ram"]
        if ram_parts:
            typer.echo(typer.style("\n--- MEMORY ---", fg=typer.colors.YELLOW))
            for part in ram_parts:
                typer.echo(f"RAM: {clean_name(part.name)} - {part.price}")

        # Display the STORAGE section
        ssd_parts = self.components["ssd"]
        hdd_parts = self.components["hdd"]
        if ssd_parts or hdd_parts:
            typer.echo(typer.style("\n--- STORAGE ---", fg=typer.colors.YELLOW))
            for part in ssd_parts:
                typer.echo(f"SSD: {clean_name(part.name)} - {part.price}")
            typer.echo("---------------")
            for part in hdd_parts:
                typer.echo(f"HDD: {clean_name(part.name)} - {part.price}")

        # Display the total price
        typer.echo(
            typer.style(
                f"\n--- PRICE ---\nTotal Price: €{self.total_price:.2f}",
                fg=typer.colors.BLUE,
            )
        )


user_pc = UserPC()


@app.command()
def main():
    clear_screen()
    """Welcome to the PC Builder App"""
    typer.echo(typer.style("Welcome to the PC Builder App", fg=typer.colors.YELLOW))
    start()


def start():
    clear_screen()
    """Main Menu"""
    while True:
        typer.echo(typer.style("\n--- Main Menu ---", fg=typer.colors.YELLOW))
        typer.echo(typer.style("1) Add details to purchase", fg=typer.colors.CYAN))
        typer.echo(typer.style("2) View purchase", fg=typer.colors.CYAN))
        # Handle Main Menu display according to whether there are components added or no
        if any(user_pc.components[component] for component in user_pc.components):
            typer.echo(typer.style("3) Remove component", fg=typer.colors.RED))
            typer.echo(typer.style("4) Finish build", fg=typer.colors.GREEN))
            typer.echo(typer.style("5) Exit", fg=typer.colors.BRIGHT_RED))
        else:
            typer.echo(typer.style("3) Exit", fg=typer.colors.BRIGHT_RED))

        choice = typer.prompt("Choose an option", type=int)

        if choice == 1:
            choose_component()
        elif choice == 2:
            view_purchase()
        elif choice == 3 and not any(
            user_pc.components[component] for component in user_pc.components
        ):
            typer.echo(
                typer.style(
                    "Thank you for using the PC Builder App!", fg=typer.colors.GREEN
                )
            )
            break
        elif choice == 3 and any(
            user_pc.components[component] for component in user_pc.components
        ):
            remove_component()
        elif choice == 4 and any(
            user_pc.components[component] for component in user_pc.components
        ):
            finish_build()
        elif choice == 5 and any(
            user_pc.components[component] for component in user_pc.components
        ):
            typer.echo(
                typer.style(
                    "Thank you for using the PC Builder App!", fg=typer.colors.GREEN
                )
            )
            break
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clear_screen()


def choose_component():
    clear_screen()
    """Select and add components to your build."""
    while True:
        typer.echo(typer.style("\n--- Choose a Component ---", fg=typer.colors.YELLOW))
        typer.echo("1) GPU")
        typer.echo("2) PSU")
        typer.echo("3) Motherboard")
        typer.echo("4) CPU")
        typer.echo("5) CPU cooler")
        typer.echo("6) RAM")
        typer.echo("7) SSD")
        typer.echo("8) HDD")
        typer.echo("9) Case")
        typer.echo(typer.style("10) Back to Main Menu", fg=typer.colors.CYAN))

        choice = typer.prompt("Choose a component to add", type=int)

        if choice == 1:
            clear_screen()
            select_component("gpu")
        elif choice == 2:
            clear_screen()
            select_component("psu")
        elif choice == 3:
            clear_screen()
            select_component("motherboard")
        elif choice == 4:
            clear_screen()
            select_component("cpu")
        elif choice == 5:
            clear_screen()
            select_component("cpucooler")
        elif choice == 6:
            clear_screen()
            select_component("ram")
        elif choice == 7:
            clear_screen()
            select_component("ssd")
        elif choice == 8:
            clear_screen()
            select_component("hdd")
        elif choice == 9:
            clear_screen()
            select_component("case")
        elif choice == 10:
            clear_screen()
            return  # Return to Main Menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clear_screen()


def format_specifications(specs):
    """Format the specifications of a part for better readability."""
    typer.echo(typer.style("\nFull Specifications:", fg=typer.colors.YELLOW))

    # Iterate over each specification and print in readable format
    for key, value in specs.items():
        # Skip none or empty values
        if value is None or value == "":
            continue

        # If the value is a list, join non-None values
        if isinstance(value, list):
            readable_value = ", ".join(
                [str(v) for v in value if v is not None and v != ""]
            )
        else:
            readable_value = str(value)

        # Print only if there is a valid value
        if readable_value:
            print(f"{key.replace('_', ' ').capitalize()}: {readable_value}")


def clean_name(name):
    """Remove text within the last set of parentheses and any redundant repeating words in the component name."""
    # Find the last opening parenthesis
    last_open = name.rfind("(")
    if last_open != -1:
        # Remove the text in the last parentheses and the parentheses themselves
        name = name[:last_open].strip()

    # Simplify repeating words in the component name
    words = name.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return " ".join(unique_words)


def select_component(component_type):
    """Select a component from available options."""

    no_limit_parts = ["ram", "hdd", "ssd"]

    # Check if the component already exists in the user's build
    if (
        component_type not in no_limit_parts
        and component_type in user_pc.components
        and user_pc.components[component_type]
    ):
        typer.echo(
            typer.style(
                f"Error: You already have a {component_type.upper()} in your build. Remove it first if you want to add a new one.",
                fg=typer.colors.RED,
            )
        )
        return

    parts = get_components(component_type)
    page_size = 10
    total_parts = len(parts)
    total_pages = (total_parts + page_size - 1) // page_size
    current_page = 0

    while True:
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, total_parts)

        typer.echo(
            typer.style(
                f"\n--- {component_type.upper()} Selection (Page {current_page + 1}/{total_pages}) ---",
                fg=typer.colors.YELLOW,
            )
        )

        # Display parts for the current page
        for i, part in enumerate(parts[start_idx:end_idx], start=1):
            cleaned_name = clean_name(part.name)
            typer.echo(f"{i}) {cleaned_name} - {part.price}")

        # Show page navigation if applicable
        if current_page < total_pages - 1:
            typer.echo(typer.style(f"{page_size + 1}) Next Page", fg=typer.colors.BLUE))

        if current_page > 0:
            typer.echo(
                typer.style(f"{page_size + 2}) Previous Page", fg=typer.colors.MAGENTA)
            )

        typer.echo(
            typer.style(
                f"{page_size + (3 if total_pages > 1 else 1)}) Exit to Component Menu",
                fg=typer.colors.RED,
            )
        )

        choice = typer.prompt(
            f"Choose a {component_type.upper()} or navigate pages", type=int
        )

        # Handle selection of a component
        if 1 <= choice <= page_size and (start_idx + choice - 1) < total_parts:
            selected_part = parts[start_idx + choice - 1]
            typer.echo(
                typer.style(
                    f"Checking compatibility for {clean_name(selected_part.name)}...",
                    fg=typer.colors.YELLOW,
                )
            )
            is_compatible, comp = selected_part.checkCompatibility(user_pc)
            typer.echo(
                typer.style(
                    f"Compatibility check result: {is_compatible}",
                    fg=typer.colors.BRIGHT_YELLOW,
                )
            )

            # Display detailed incompatibility messages, filtering out empty messages
            if not is_compatible:
                display_incompatibility_messages(comp.messages, component_type, user_pc)

            if is_compatible:
                cleaned_name = clean_name(selected_part.name)
                typer.echo(
                    typer.style(
                        f"\nYou selected {cleaned_name} for {selected_part.price}",
                        fg=typer.colors.GREEN,
                    )
                )
                format_specifications(selected_part.specs.to_dict())

                confirm_choice = typer.prompt(
                    "Do you want to add this to your build? (y/n)", type=str
                )

                if confirm_choice.lower() == "y":
                    user_pc.add_component(component_type, selected_part)
                    typer.echo(
                        typer.style(
                            f"{component_type.upper()} added to your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                    return  # Exit to Main Menu after adding component
                else:
                    typer.echo(
                        typer.style("Selection cancelled.", fg=typer.colors.GREEN)
                    )

        # Next Page
        elif choice == page_size + 1 and current_page < total_pages - 1:
            current_page += 1
        # Previous Page
        elif choice == page_size + 2 and current_page > 0:
            current_page -= 1
        # Exit to Component Menu
        elif choice == page_size + (3 if total_pages > 1 else 1):
            clear_screen()
            return  # Properly exit to the component menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clear_screen()


def display_incompatibility_messages(messages, component_type, user_pc):
    """Display any incompatibility messages."""
    # Filter out empty messages
    filtered_messages = {key: value for key, value in messages.items() if value}

    if filtered_messages:
        typer.echo(
            typer.style(f"\nIssues with {component_type.upper()}:", fg=typer.colors.RED)
        )
        for key, msgs in filtered_messages.items():
            for message in msgs:
                typer.echo(f" - {message}")

        suggest_alternatives = typer.prompt(
            "Would you like to see a few compatible alternatives? (y/n)", type=str
        )
        if suggest_alternatives.lower() == "y":
            suggest_component(user_pc, component_type, messages)


def suggest_component(user_pc, component_type, messages):
    clear_screen()
    # Dictionary for all the suggestion functions
    suggestion_functions = {
        "cpu": suggestCompatibleCPUs,
        "psu": suggestCompatiblePSUs,
        "gpu": suggestCompatibleGPUs,
        "case": suggestCompatibleCases,
        "cpucooler": suggestCompatibleCPUcoolers,
        "motherboard": suggestCompatibleMotherboards,
        "ram": suggestCompatibleRAMs,
        "ssd": suggestCompatibleSSDs,
        "hdd": suggestCompatibleHDDs,
    }
    suggest_func = suggestion_functions.get(component_type)

    if suggest_func:
        while True:
            suggested_parts = suggest_func(
                user_pc, messages
            )  # Get 5 suggestions for the build
            typer.echo(
                typer.style(
                    f"\nSuggested compatible {component_type.upper()}s:",
                    fg=typer.colors.YELLOW,
                )
            )
            for i, part in enumerate(suggested_parts, start=1):
                typer.echo(f"{i}) {clean_name(part.name)} - {part.price}")

            # Giving user an option to choose
            skip_option = len(suggested_parts) + 1
            typer.echo(
                typer.style(
                    f"{skip_option}) Skip adding a suggested part",
                    fg=typer.colors.YELLOW,
                )
            )

            choice = typer.prompt(
                f"Choose a suggested {component_type} to add or skip", type=int
            )

            if choice == skip_option:
                typer.echo(
                    typer.style(
                        f"Skipping the addition of a suggested {component_type}.",
                        fg=typer.colors.GREEN,
                    )
                )
                break
            elif 1 <= choice <= len(suggested_parts):
                selected_part = suggested_parts[choice - 1]
                typer.echo(
                    typer.style(
                        f"You selected {clean_name(selected_part.name)} for {selected_part.price}",
                        fg=typer.colors.YELLOW,
                    )
                )
                format_specifications(selected_part.specs.to_dict())

                confirm_choice = typer.prompt(
                    "Do you want to add this to your build? (y/n)", type=str
                )

                if confirm_choice.lower() == "y":
                    user_pc.add_component(component_type, selected_part)
                    typer.echo(
                        typer.style(
                            f"{component_type.upper()} added to your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                    break
                else:
                    typer.echo(
                        typer.style(
                            "\nSelection cancelled. You can choose another part or skip.",
                            fg=typer.colors.RED,
                        )
                    )
            else:
                typer.echo(
                    typer.style(
                        "Invalid choice. Please try again.", fg=typer.colors.RED
                    )
                )
                clear_screen()
    else:
        typer.echo(
            typer.style(
                f"\nNo compatible alternatives found for {component_type}.",
                fg=typer.colors.RED,
            )
        )


def view_purchase():
    clear_screen()
    """View the current purchase and total price."""
    typer.echo(typer.style("\n--- Current Build ---", fg=typer.colors.YELLOW))
    user_pc.display()


def get_components(component_type):
    """Fetch components based on the type (GPU or PSU)"""
    try:
        if component_type == "gpu":
            return loadGPUsfromJSON()
        elif component_type == "psu":
            return loadPSUsfromJSON()
        elif component_type == "motherboard":
            return loadMBsfromJSON()
        elif component_type == "cpu":
            return loadCPUsfromJSON()
        elif component_type == "cpucooler":
            return loadCPUCoolersfromJSON()
        elif component_type == "ram":
            return loadRAMsfromJSON()
        elif component_type == "ssd":
            return loadSSDsfromJSON()
        elif component_type == "hdd":
            return loadHDDsfromJSON()
        elif component_type == "case":
            return loadCasesfromJSON()
    except Exception as e:
        typer.echo(
            typer.style(
                f"An error occurred while fetching {component_type.upper()} data. Please try again later.",
                fg=typer.colors.RED,
            )
        )
    return []


def finish_build():
    clear_screen()
    """Finalize and display the build"""
    typer.echo(typer.style("\n--- Final Build ---", fg=typer.colors.YELLOW))
    user_pc.display()

    while True:
        typer.echo(typer.style("1) Confirm build", fg=typer.colors.GREEN))
        typer.echo(typer.style("2) Return to Main Menu", fg=typer.colors.MAGENTA))
        action = typer.prompt("Choose an option", type=int)

        if action == 1:
            typer.echo(
                typer.style(
                    "Build confirmed. Thank you for using the PC Builder App!",
                    fg=typer.colors.GREEN,
                )
            )
            sys.exit()  # Exit the program
        elif action == 2:
            clear_screen()
            return  # Return to go back to main menu
        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clear_screen()


def remove_component():
    clear_screen()
    """Remove a component from the build if it exists."""

    # List component types that are available to remove
    component_options = [
        ("gpu", "Remove GPU"),
        ("psu", "Remove PSU"),
        ("motherboard", "Remove motherboard"),
        ("cpu", "Remove CPU"),
        ("cpucooler", "Remove CPU cooler"),
        ("ram", "Remove RAM"),
        ("ssd", "Remove SSD"),
        ("hdd", "Remove HDD"),
        ("case", "Remove case"),
    ]

    while True:
        typer.echo(
            typer.style(
                "\n--- Select a Component to Remove ---", fg=typer.colors.YELLOW
            )
        )
        option_num = 1
        valid_options = {}
        components_exist = False

        # Display only the components that are in the user's build
        for comp_type, label in component_options:
            if user_pc.components[comp_type]:
                components_exist = True
                typer.echo(f"{option_num}) {label}")
                valid_options[option_num] = comp_type
                option_num += 1

        # Dynamically add option to remove all components if any exist
        if components_exist:
            typer.echo(
                typer.style(
                    f"{option_num}) Remove all components", fg=typer.colors.BRIGHT_RED
                )
            )
            remove_all_option = option_num
            option_num += 1

        typer.echo(
            typer.style(f"{option_num}) Back to previous menu", fg=typer.colors.CYAN)
        )

        choice = typer.prompt("Choose a component to remove", type=int)

        if choice in valid_options:
            comp_type = valid_options[choice]

            # Handle components that allow multiple instances
            if comp_type in ["ram", "ssd", "hdd"]:
                typer.echo(f"\n--- Available {comp_type.upper()}s ---")
                for i, part in enumerate(user_pc.components[comp_type], start=1):
                    typer.echo(f"{i}) {clean_name(part.name)} - {part.price}")

                part_choice = typer.prompt(
                    f"Select {comp_type.upper()} to remove or choose '0' to remove all",
                    type=int,
                )

                # Check if user wants to remove all
                if part_choice == 0:
                    confirm = typer.prompt(
                        f"Are you sure you want to remove all {comp_type.upper()}s? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        for part in user_pc.components[comp_type]:
                            price = float(
                                part.price.replace("€", "").replace("$", "").strip()
                            )
                            user_pc.total_price -= price
                        user_pc.components[comp_type] = []
                        typer.echo(
                            typer.style(
                                f"All {comp_type.upper()}s removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.RED)
                        )
                elif 1 <= part_choice <= len(user_pc.components[comp_type]):
                    part_to_remove = user_pc.components[comp_type][part_choice - 1]
                    confirm = typer.prompt(
                        f"Are you sure you want to remove {clean_name(part_to_remove.name)}? (y/n)",
                        type=str,
                    )
                    if confirm.lower() == "y":
                        user_pc.remove_component(comp_type, part_choice - 1)
                        typer.echo(
                            typer.style(
                                f"{comp_type.upper()} removed from your build.",
                                fg=typer.colors.GREEN,
                            )
                        )
                    else:
                        typer.echo(
                            typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                        )
                else:
                    typer.echo(
                        typer.style(
                            "Invalid choice, please try again.", fg=typer.colors.RED
                        )
                    )
                    clear_screen()

            else:
                part_to_remove = user_pc.components[comp_type][0]
                confirm = typer.prompt(
                    f"Are you sure you want to remove {clean_name(part_to_remove.name)}? (y/n)",
                    type=str,
                )
                if confirm.lower() == "y":
                    user_pc.remove_component(comp_type, 0)
                    typer.echo(
                        typer.style(
                            f"{comp_type.upper()} removed from your build.",
                            fg=typer.colors.GREEN,
                        )
                    )
                else:
                    typer.echo(
                        typer.style("Operation cancelled.", fg=typer.colors.GREEN)
                    )

            # Display updated build
            typer.echo(typer.style("\n--- Updated Build ---", fg=typer.colors.YELLOW))
            user_pc.display()

        # Handle 'Remove all components' choice dynamically
        elif components_exist and choice == remove_all_option:
            confirm = typer.prompt(
                "Are you sure you want to remove all components? (y/n)", type=str
            )
            if confirm.lower() == "y":
                for key in user_pc.components:
                    user_pc.components[key] = []
                user_pc.total_price = 0.00
                typer.echo(
                    typer.style(
                        "All components have been removed from your build.",
                        fg=typer.colors.GREEN,
                    )
                )
                user_pc.display()
            else:
                typer.echo(typer.style("Operation cancelled.", fg=typer.colors.GREEN))

        elif choice == option_num:
            clear_screen()
            return

        else:
            typer.echo(
                typer.style("Invalid choice, please try again.", fg=typer.colors.RED)
            )
            clear_screen()


if __name__ == "__main__":
    app()
