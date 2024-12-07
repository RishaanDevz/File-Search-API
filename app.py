from flask import Flask, jsonify, request
import os
import glob
import subprocess
import threading
import interpreter

app = Flask(__name__)

def start_loophole():
    process = subprocess.Popen(
        ["loophole", "http", "8000", "--hostname", "insert-subdomain-here"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def search_files(search_term, directory="."):
    results = []
    for entry in os.scandir(directory):
        try:
            if entry.is_file(follow_symlinks=False):
                if search_term.lower() in entry.name.lower():
                    results.append({
                        "filename": entry.name,
                        "path": str(entry.path),
                        "size": entry.stat().st_size,
                        "modified": entry.stat().st_mtime
                    })
            elif entry.is_dir(follow_symlinks=False):
                results.extend(search_files(search_term, entry.path))
        except PermissionError:
            continue
    return results

@app.route('/search/<term>')
def search_endpoint(term):
    downloads_path = os.path.expanduser("~/Downloads")
    results = search_files(term, downloads_path)
    return jsonify({
        "search_term": term,
        "results": results,
        "count": len(results)
    })
    
@app.route('/files/<extension>')
def search_by_extension(extension):
    files = glob.glob(f"**/*.{extension}", recursive=True)
    results = [{
        "filename": os.path.basename(f),
        "path": f,
        "size": os.path.getsize(f)
    } for f in files]
    return jsonify({
        "extension": extension,
        "results": results,
        "count": len(results)
    })

@app.route('/send')
def send_email():
    try:
        file_path = request.args.get('file')
        email = request.args.get('email')
        
        if not file_path or not email:
            return jsonify({
                "error": "Missing parameters. Both 'file' and 'email' are required"
            }), 400

        # Convert to proper file path
        file_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                "error": "File not found",
                "path": file_path
            }), 404

        # Send email with attachment
        subject = f"File: {os.path.basename(file_path)}"
        body = f"Please find attached the file: {os.path.basename(file_path)}"
        interpreter.computer.mail.send(email, subject, body, [file_path])

        return jsonify({
            "status": "success",
            "message": "Email sent successfully",
            "file": os.path.basename(file_path),
            "recipient": email
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500

if __name__ == '__main__':
    loophole_process = start_loophole()
    try:
        app.run(host='0.0.0.0', port=8000, debug=False)
    finally:
        loophole_process.terminate()
