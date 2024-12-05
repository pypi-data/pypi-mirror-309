# FileDrop - Simple File Sharing Server

This simple server allows multiple users on the same **local network** to upload and download files via a web interface. It works across different platforms, and the server generates a QR code for easy access to the server URL on other devices.

## Requirements
- Python 3.x
- `qrcode` library (for offline QR code generation)
- Internet browser (Safari for iOS)

### To Install:
1. **Python**: Ensure Python 3 is installed on your machine to run this server.
2. **Optional**: If you want the server to generate QR codes, install the `qrcode` library by running:
   ```bash
   pip install qrcode[pil]
   ```

### To Use on iOS (A-Shell Mini):
1. **Download A-Shell Mini**: Install **A-Shell Mini** or **A-Shell** from the App Store.
2. **Download the Repository**: 
   - Download the ZIP version of this repository.
   - Move the downloaded file to the A-Shell folder or use `Downloads`.
3. **Extract and Move Files**:
   - Open A-Shell and navigate to the folder where you placed the ZIP file.
   - Unzip the file: `unzip FileDrop.zip`
4. **Run the Server**:
   - Navigate to the folder with the extracted files.
   - Run the server with:
     ```bash
     python3 path-to-server.py
     ```
5. **Access the Server**: Open Safari and go to `http://localhost:8000`.

6. **Optional: Create a Shortcut**:
   - You can create a shortcut to automatically run the server and open Safari for you. This can be done through the iOS **Shortcuts app**.

## Features:
- **Upload and Download**: Upload files to the server through the web interface, and all devices on the same local network can download those files.
- **QR Code**: The server generates a QR code that users can scan to easily access the server's web interface.
- **Shared Directory**: Files uploaded to the server are saved in a shared directory and can be downloaded from any device on the same network.

## How it Works:
1. **Start the Server**:
   - Once the server is running, you can access the file-sharing interface by visiting `http://localhost:8000` in your browser.
   
2. **Upload Files**:
   - On the main page, use the "Choose Files" button to select files you want to upload. After selecting the files, they will be uploaded to the server.

3. **Download Files**:
   - Uploaded files will appear as links on the page. You can click the links to download the files.

4. **Generate QR Code**:
   - A QR code will be generated dynamically and displayed on the page. You can scan this QR code from any device on the same network to easily open the server's URL.

## Important Notes:
- **Local Network**: All devices must be connected to the same local network for the server to work. It is recommended to use a **5G** network for faster file transfers.
  
## Troubleshooting:
- If you can't generate the QR code or install `qrcode`, you can try using an online QR code generator, but it is recommended to use the offline generation for better privacy.
- Ensure all devices are connected to the same **local network** for proper file sharing.

## Future Updates:
- Stay tuned for possible improvements to make it even easier to use and access the server.