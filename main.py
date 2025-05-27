import sys
from pathlib import Path

plugindir = Path(__file__).parent.resolve()
sys.path = [str(plugindir / "lib")] + sys.path


from flowlauncher import FlowLauncher
from howlongtobeatpy import HowLongToBeat
import webbrowser


class TimeToBeat(FlowLauncher):

    def query(self, query):
        if len(query.strip()) < 3:
            return [{
                "title": "Keep typing...",
                "subTitle": "Enter at least 3 characters to search for a game.",
                "icoPath": "icon.png"
            }]
        
        results = HowLongToBeat().search(query)

        if not results:
            return [{
                "title": f"No results found for '{query}'",
                "subTitle": "Try a different game name.",
                "icoPath": "icon.png"
            }]
        
        best_match = max(results, key=lambda x: x.similarity)

        playtime_summary = f"Main: {best_match.main_story}h | Main+Extra: {best_match.main_extra}h | 100%: {best_match.completionist}h"

        game_url = f"https://howlongtobeat.com/game/{best_match.game_id}" if best_match.game_id else "https://howlongtobeat.com"

        return [{
            "title": best_match.game_name,
            "subTitle": playtime_summary,
            "icoPath": "icon.png",
            "jsonRPCAction": {
                "method": "open_url",
                "parameters": [game_url]
            },
            "score": 100
        }]

    def context_menu(self, data):
        return [
            {
                "title": "View on HowLongToBeat.com",
                "subTitle": "Opens the website",
                "icoPath": "icon.png",
                "jsonRPCAction": {
                    "method": "open_url",
                    "parameters": ["https://howlongtobeat.com"]
                },
                "score": 0
            }
        ]

    def open_url(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    TimeToBeat()
