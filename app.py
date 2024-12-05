from flask import Flask, jsonify
import os
import glob
import subprocess
import threading

app = Flask(__name__)

def start_loophole():
    subprocess.run(["loophole", "http", "8000", "--hostname", "insert-subdomain-here"])

def search_files(search_term, directory="."):
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if search_term.lower() in file.lower():
                file_path = os.path.join(root, file)
                results.append({
                    "filename": file,
                    "path": file_path,
                    "size": os.path.getsize(file_path)
                })
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

if __name__ == '__main__':
    # Start Loophole in a separate thread
    loophole_thread = threading.Thread(target=start_loophole, daemon=True)
    loophole_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)
