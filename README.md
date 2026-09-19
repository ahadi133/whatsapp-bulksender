# WhatsApp Message Sender

A simple desktop application built with Python and Tkinter for sending WhatsApp messages through [`pywhatkit`](https://github.com/Ankit404butfound/PyWhatKit).

The application supports:

- Sending a message to one phone number.
- Sending the same message to multiple phone numbers loaded from a comma-separated text file.
- International phone-number validation using the `+countrycode...` format.
- A status panel showing successful sends and skipped or failed numbers.
- Background sending so the main window remains responsive while messages are being processed.

## Requirements

- Python 3.8 or newer
- An active internet connection
- WhatsApp Web access
- A supported web browser
- A phone with WhatsApp available for authentication

Install the Python dependency with:

```bash
pip install pywhatkit
```

`tkinter` is included with most standard Python installations. On some Linux distributions, it must be installed separately, for example:

```bash
sudo apt-get install python3-tk
```

## Installation

1. Save the Python code in a file such as `whatsapp_sender.py`.
2. Install the required dependency:

   ```bash
   pip install pywhatkit
   ```

3. Start the application:

   ```bash
   python whatsapp_sender.py
   ```

4. When prompted by the browser, scan the WhatsApp Web QR code if you are not already signed in.

## Usage

### Send to one number

1. Select **Single Number**.
2. Enter the recipient's phone number in international format, including the plus sign.
3. Enter the message.
4. Click **Send WhatsApp Message(s)**.

Example:

```text
+8801712345678
```

### Send to multiple numbers

1. Select **Upload Contact List (Comma Separated)**.
2. Create a `.txt` file containing numbers separated by commas.
3. Click **Browse** and select the file.
4. Enter the message.
5. Click **Send WhatsApp Message(s)**.

Example contact-list file:

```text
+8801712345678,+14155552671,+447911123456
```

Numbers that do not begin with `+` are skipped and reported in the status panel.

## How it works

The interface is implemented with Tkinter. When sending begins, the application starts a separate thread and calls `pywhatkit.sendwhatmsg_instantly()` for each valid number. The status panel is updated as each number is processed.

The browser may open or switch to WhatsApp Web while messages are being sent. Sending speed and reliability depend on the browser, internet connection, WhatsApp Web session, and `pywhatkit` behavior.

## Important notes

- Use this tool only to message people who have agreed to receive your messages.
- Avoid bulk or unsolicited messaging. WhatsApp may restrict accounts that violate its terms or trigger anti-spam systems.
- Keep WhatsApp Web signed in before sending multiple messages.
- The contact list must use comma-separated values. One number per line is not handled by the current code unless the file format is adapted.
- The current validation only checks that a number starts with `+`; it does not verify that the number is active or correctly formatted for a specific country.
- Do not close the browser while messages are being sent.
- The application reports completion after processing the list, but delivery itself is controlled by WhatsApp.

## Troubleshooting

### `ModuleNotFoundError: No module named 'pywhatkit'`

Install the dependency in the same Python environment used to run the application:

```bash
python -m pip install pywhatkit
```

### The browser does not open or the message is not sent

- Confirm that the internet connection is working.
- Open WhatsApp Web manually and verify that the account is signed in.
- Check that the number includes the correct country code and starts with `+`.
- Make sure the browser is not blocked by another window or security policy.
- Try sending to one number before processing a contact list.

### Some contacts are skipped

Only values beginning with `+` are accepted. Remove extra text, quotes, or formatting from the contact list and separate numbers with commas.
