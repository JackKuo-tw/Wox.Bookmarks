import os
import json
import subprocess
from wox import Wox

class EdgeBookmarks(Wox):
    BOOKMARKS_FILE = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks")

    def query(self, query):
        results = []

        # Check if the bookmark file exists
        if not os.path.exists(self.BOOKMARKS_FILE):
            results.append({
                "Title": "Edge Bookmarks file not found",
                "SubTitle": "Ensure Edge is installed and bookmarks are saved",
                "IcoPath": "Images/app.png",
                "JsonRPCAction": {
                    "method": "do_nothing",
                    "parameters": [],
                    "dontHideAfterAction": True
                }
            })
            return results

        # Load bookmarks JSON
        with open(self.BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            bookmarks_data = json.load(f)

        # Extract bookmarks from JSON structure
        bookmarks = []
        for k,v in bookmarks_data["roots"].items():
            bookmarks.extend(self.extract_bookmarks(v))

        # Filter based on query
        for bookmark in bookmarks:
            if query.lower() in bookmark["name"].lower():
                results.append({
                    "Title": bookmark["name"],
                    "SubTitle": bookmark["url"],
                    "IcoPath": "Images/link.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [bookmark["url"]],
                        "dontHideAfterAction": False
                    }
                })

        return results

    def extract_bookmarks(self, node):
        """Recursively extract all bookmarks from the node."""
        bookmarks = []
        if "children" in node:
            for child in node["children"]:
                bookmarks.extend(self.extract_bookmarks(child))
        elif node.get("type") == "url":
            bookmarks.append({"name": node["name"], "url": node["url"]})
        return bookmarks

    def open_url(self, url):
        """Open the URL in the default web browser."""
        subprocess.Popen(["start", url], shell=True)

    def do_nothing(self):
        """Placeholder action."""
        pass


if __name__ == "__main__":
    EdgeBookmarks()
