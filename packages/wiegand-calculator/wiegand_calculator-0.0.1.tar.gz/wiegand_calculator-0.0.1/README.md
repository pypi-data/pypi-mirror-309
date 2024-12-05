# Wiegand Calculator
This is a simple calculator for the Wiegand protocol. It can calculate the facility code and card number from a Wiegand number, and vice versa. This is useful for RFID card systems that use the Wiegand protocol.

## Usage
This module exposes two functions:
- `convert_from_wiegand(board_tag: int) -> int`: Converts a Wiegand number to the original card number.
- `converet_to_wiegand(card_number: int) -> int`: Converts a card number to a Wiegand number.
