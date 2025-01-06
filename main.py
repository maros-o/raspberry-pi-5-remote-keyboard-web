import keyboard
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Remote Keyboard</title>
    <script>
        let ctrlPressed = false;
        let shiftPressed = false;
        let altPressed = false;

        function handleInput(event) {
            const input = event.target;
            const key = input.value.slice(-1);
            input.value = '';
            const keyCombination = {
                key: key,
                ctrl: ctrlPressed,
                shift: shiftPressed,
                alt: altPressed
            };
            fetch("/keypress", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(keyCombination)
            });
            const keyDisplay = (ctrlPressed ? "Ctrl+" : "") +
                             (shiftPressed ? "Shift+" : "") +
                             (altPressed ? "Alt+" : "") +
                             key;
            document.getElementById("lastKey").innerText = keyDisplay;
        }

        document.addEventListener("keydown", (event) => {
            if (event.key === "Control" || event.key === "ControlLeft" || event.key === "ControlRight") {
                ctrlPressed = true;
            }
            if (event.key === "Shift" || event.key === "ShiftLeft" || event.key === "ShiftRight") {
                shiftPressed = true;
            }
            if (event.key === "Alt" || event.key === "AltLeft" || event.key === "AltRight") {
                altPressed = true;
            }
            const keyCombination = {
                key: event.key,
                ctrl: ctrlPressed,
                shift: shiftPressed,
                alt: altPressed
            };
            fetch("/keypress", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(keyCombination)
            });
            const keyDisplay = (ctrlPressed ? "Ctrl+" : "") +
                               (shiftPressed ? "Shift+" : "") +
                               (altPressed ? "Alt+" : "") +
                               event.key;

            document.getElementById("lastKey").innerText = keyDisplay;
            event.preventDefault();
        });

        document.addEventListener("keyup", (event) => {
            if (event.key === "Control" || event.key === "ControlLeft" || event.key === "ControlRight") {
                ctrlPressed = false;
            }
            if (event.key === "Shift" || event.key === "ShiftLeft" || event.key === "ShiftRight") {
                shiftPressed = false;
            }
            if (event.key === "Alt" || event.key === "AltLeft" || event.key === "AltRight") {
                altPressed = false;
            }
        });
    </script>
</head>
<body>
    <input placeholder="click here" autofocus type="text" oninput="handleInput(event)" />
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(html_template)

@app.route("/keypress", methods=["POST"])
def keypress():
    data = request.json
    key = data.get("key", "").lower()
    ctrl = data.get("ctrl", False)
    shift = data.get("shift", False)
    alt = data.get("alt", False)

    if ctrl:
        key = "ctrl+" + key
    if shift:
        key = "shift+" + key
    if alt:
        key = "alt+" + key

    try:
        keyboard.send(key)
        print(f"Simulated key: {key}")
    except Exception as e:
        print(f"Error simulating key: {str(e)}")
        return str(e), 500

    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
