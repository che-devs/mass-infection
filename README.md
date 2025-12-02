# Mass Infection (Massenansteckung)

Mass Infection is an interactive game designed for group participation and optimized for Raspberry Pi. It combines physical actions with digital tracking to create a fun and engaging experience. Players register using a barcode scanner and progress through multiple levels by completing tasks such as clapping, interacting with others, and performing specific actions.


## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Contributing](#contributing)
4. [License](#license)


## Installation

To install the project locally, please follow these steps:

1. **Clone the repository**:
   ```
   git clone https://github.com/username/projectname.git
   cd projectname
   ```


2. **Run the setup script**:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Linux ESC/POS Printer Configuration**

   To use an Epson ESC/POS printer on Linux, add the following udev rule:

   ```bash
   sudo nano /etc/udev/rules.d/99-escpos.rules
   ```

   Add:

   ```bash
   SUBSYSTEM=="usb", ATTR{idVendor}=="04b8", ATTR{idProduct}=="0e2a", MODE="0666"
   ```

   Reload the rules and trigger udev:

   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

## Usage
```
chmod +x start.sh
./start.sh
```

## Contributing
Contributions to the project are welcome! If you want to suggest an improvement or fix a bug, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

