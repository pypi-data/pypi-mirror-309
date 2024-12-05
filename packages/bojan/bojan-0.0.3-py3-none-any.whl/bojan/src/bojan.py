import os
import datetime

class BojanConsole:
    def __init__(self, printing=True) -> None:
        self.log = ""
        self.printing = printing

    def log_plain(self, message):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = "INFO"
        if "⚠️" in message:
            prefix = "WARN"
        if "❌" in message:
            prefix = "EROR"
        if "💬" in message:
            prefix = "DBUG"
        if "✅" in message:
            prefix = "RSLT"
    
        self.log += f"{date} [{prefix}]\t{message}\n"
        if self.printing:
            print(message)
        
    def print(self, message, identifier="🕸️", depth=0):
        message = f"{"\t"*depth}{identifier} {message}"
        self.log_plain(message)

    def debug(self, message, depth=0):
        if(type(message) != str):
            message = str(message)
        self.print(bcolors.GREY + message + bcolors.END, "💬", depth=depth)
    
    def error(self, message, depth=0):
        if(type(message) != str):
            message = str(message)
        self.print(bcolors.RED + message + bcolors.END, "❌", depth=depth)
        
    def success(self, message, depth=0):
        if(type(message) != str):
            message = str(message)
        self.print(bcolors.GREEN + message + bcolors.END, "✅", depth=depth)

    def warning(self, message, depth=0):
        if(type(message) != str):
            message = str(message)
        self.print(bcolors.YELLOW + message + bcolors.END, "⚠️", depth=depth)

    def dictionary(self, d, depth=0):
        depth_emoji = ["🏰", "🛖", "🌲", "🐦", "🐛", "🧬"]
        for key, value in d.items():
            if isinstance(value, dict):
                self.print(f"{bcolors.ITALIC}{bcolors.WHITE if depth == 0 else ''}{key}{bcolors.END}:", depth_emoji[depth], depth)
                self.dictionary(value, depth + 1)
            else:
                self.print(f"{key}: {value}", depth_emoji[depth], depth)
    
    def print_parameter(self, section, parameters, icon="🔧"):
        self.log_plain(f"{icon} {bcolors.BOLD}{bcolors.YELLOW}{section}{bcolors.END}:")
        for key, value in parameters.items():
            self.log_plain(f"\t{bcolors.BLUE}{key}{bcolors.END} : {bcolors.BLUE}{value}{bcolors.END}")

    def print_parameters(self, mappings, settings):
        self.log_plain(f"STARTING 🌱 {bcolors.BOLD}{bcolors.GREEN}VELES{bcolors.END}🌱 WITH FOLLOWING PARAMETERS:")
        self.print_parameter("Settings", settings, "⚙️")
        self.print_parameter("Mappings", mappings, "🗺️")
    
    def strip_colors(self, string):
        return string.replace(bcolors.END, "").replace(bcolors.BOLD, "").replace(bcolors.ITALIC, "").replace(bcolors.URL, "").replace(bcolors.BLINK, "").replace(bcolors.BLINK2, "").replace(bcolors.SELECTED, "").replace(bcolors.BLACK, "").replace(bcolors.RED, "").replace(bcolors.GREEN, "").replace(bcolors.YELLOW, "").replace(bcolors.BLUE, "").replace(bcolors.VIOLET, "").replace(bcolors.BEIGE, "").replace(bcolors.WHITE, "").replace(bcolors.BLACKBG, "").replace(bcolors.REDBG, "").replace(bcolors.GREENBG, "").replace(bcolors.YELLOWBG, "").replace(bcolors.BLUEBG, "").replace(bcolors.VIOLETBG, "").replace(bcolors.BEIGEBG, "").replace(bcolors.WHITEBG, "").replace(bcolors.GREY, "").replace(bcolors.RED2, "").replace(bcolors.GREEN2, "").replace(bcolors.YELLOW2, "").replace(bcolors.BLUE2, "").replace(bcolors.VIOLET2, "").replace(bcolors.BEIGE2, "").replace(bcolors.WHITE2, "").replace(bcolors.GREYBG, "").replace(bcolors.REDBG2, "").replace(bcolors.GREENBG2, "").replace(bcolors.YELLOWBG2, "").replace(bcolors.BLUEBG2, "").replace(bcolors.VIOLETBG2, "").replace(bcolors.BEIGEBG2, "").replace(bcolors.WHITEBG2, "")
    
    def save(self, filename):
        if "/" in filename or "\\" in filename:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(self.strip_colors(self.log))

class ProgressBar:
    def __init__(self, total, length=50) -> None:
        self.total = total
        self.length = length
        self.progress = 0
        self.update(0)
    
    def update(self, progress):
        self.progress = progress
    
    def print(self):
        progress = int(self.progress/self.total*self.length)
        print(f"[{'#'*progress}{'-'*(self.length-progress)}] {progress/self.length*100:.2f}%", end="\r")

class bcolors:
    END      = '\33[0m'
    BOLD     = '\33[1m'
    ITALIC   = '\33[3m'
    URL      = '\33[4m'
    BLINK    = '\33[5m'
    BLINK2   = '\33[6m'
    SELECTED = '\33[7m'

    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    BEIGE  = '\33[36m'
    WHITE  = '\33[37m'

    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    BEIGEBG  = '\33[46m'
    WHITEBG  = '\33[47m'

    GREY    = '\33[90m'
    RED2    = '\33[91m'
    GREEN2  = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2   = '\33[94m'
    VIOLET2 = '\33[95m'
    BEIGE2  = '\33[96m'
    WHITE2  = '\33[97m'

    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'
    GREENBG2  = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2   = '\33[104m'
    VIOLETBG2 = '\33[105m'
    BEIGEBG2  = '\33[106m'
    WHITEBG2  = '\33[107m'