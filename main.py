import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from page_classes import homePageUI, loginPageUI


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance

    page_stack = QtWidgets.QStackedWidget()  # Create a stack to hold different pages

    home_screen = homePageUI(page_stack)  # Initialize the home page
    login_screen = loginPageUI(page_stack)  # Initialize the login page

    page_stack.addWidget(login_screen)  # Add the login page to the stack
    page_stack.show()  # Show the stack (which will display the login page)

    app.exec()  # Start the application's event loop