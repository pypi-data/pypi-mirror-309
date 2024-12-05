# FileDrop - Simple File Sharing Server

**FileDrop** is a simple server that allows users on the same local network to easily upload and download files through a web interface. It also generates a QR code for quick access to the server URL from any device on the same network.

### Key Features:
- **File Sharing**: Upload and download files through a simple web interface.
- **QR Code Generation**: Dynamically generates a QR code for easy access to the server.
- **Local Network Only**: Works across multiple devices connected to the same local network.
- **Cross-Platform**: Use on any device that supports Python (Windows, macOS, Linux, iOS via A-Shell mini, etc.)

### Requirements:
- Python 3.x
- **Install via pip**:
   ```bash
   pip install filedrop
   ```

   This will install all required dependencies, including the **qrcode** library for QR code generation.

### Usage on iOS (A-Shell Mini):

1. **Install A-Shell Mini**: Install **A-Shell Mini** or **A-Shell** from the App Store.
2. **Install the Python Package**:
   - Open **A-Shell** or **A-Shell Mini**.
   - Install **FileDrop** by running:
     ```bash
     pip install filedrop
     ```
3. **Run the Server**:
   - After installation, run the server with:
     ```bash
     python3 -m filedrop
     ```
4. **Access the Server**: Open **Safari** on your iOS device and go to `http://localhost:8000`.

5. **Optional: Create a Shortcut**:
   - You can create a shortcut in the **Shortcuts app** to automatically run the server and open the browser.
   - I may provide a shortcut for automatic setup in future updates.

### How it Works:
- Once the server is running, you can access the web interface at `http://localhost:8000`.
- You can upload files through the web interface.
- Files are stored in a shared directory, and anyone on the same local network can download them.
- The server generates a QR code that you can scan to easily open the server's web interface on another device.

### Important Notes:
- **Local Network**: All devices must be connected to the same **local network**.
- **Recommendation**: Use a **5G network** for faster file transfers between devices.

### Troubleshooting:
- Ensure that all devices are connected to the **same local network** for proper communication.

### Future Updates:
- I plan to work on a shortcut to automatically download the bundled server and open it when the app is launched. Stay tuned for more features!

Feel free to use this simple file-sharing server as needed. Enjoy sharing files easily across your local network!