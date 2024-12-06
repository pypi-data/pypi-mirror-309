"""Module that runs the system processes to change the wallpaper"""

import subprocess
import time
from pathlib import Path

from waypaper.config import Config
from waypaper.common import get_monitor_names
from waypaper.translations import Chinese, English, French, German, Polish, Russian, Belarusian, Spanish

def change_wallpaper(image_path: Path, cf: Config, monitor: str,
                     txt: Chinese|English|French|German|Polish|Russian|Belarusian|Spanish):
    """Run system commands to change the wallpaper depending on the backend"""

    try:
        # swaybg backend:
        if cf.backend == "swaybg":

            # Kill previous swaybg instances:
            try:
                subprocess.check_output(["pgrep", "swaybg"], encoding='utf-8')
                subprocess.Popen(["killall", "swaybg"])
                time.sleep(0.005)
            except subprocess.CalledProcessError:
                pass

            fill = cf.fill_option.lower()
            command = ["swaybg"]
            if monitor != "All":
                command.extend(["-o", monitor])
            command.extend(["-i", str(image_path)])
            command.extend(["-m", fill, "-c", cf.color])
            subprocess.Popen(command)
            print(f"{txt.msg_setwith} {cf.backend}")

        # mpvpaper backend:
        elif cf.backend == "mpvpaper":

            fill_types = {
                    "fill": "panscan=1.0",
                    "fit": "panscan=0.0",
                    "center": "",
                    "stretch": "--keepaspect=no",
                    "tile": "",
                    }
            fill = fill_types[cf.fill_option.lower()]

            # If mpvpaper is already active on given monitor, try to call that process in that socket:
            try:
                subprocess.check_output(["pgrep", "-f", f"socket-{monitor}"], encoding='utf-8')
                time.sleep(0.2)
                print("Detected running mpvpaper on {monitor}, now trying to call mpvpaper socket")
                subprocess.Popen(f"echo 'loadfile \"{image_path}\"' | socat - /tmp/mpv-socket-{monitor}", shell=True)

            # If mpvpaper is not running, create a new process in a new socket:
            except subprocess.CalledProcessError:
                print("Detected no running mpvpaper, starting new mpvpaper process")
                command = ["mpvpaper", "--fork"]
                command.extend(["-o", f"input-ipc-server=/tmp/mpv-socket-{monitor} no-audio loop {fill} --background-color='{cf.color}'"])

                # Specify the monitor:
                if monitor == "All":
                    command.extend('*')
                else:
                    command.extend([monitor])

                command.extend([image_path])
                subprocess.Popen(command)
            print(f"{txt.msg_setwith} {cf.backend}")

        # swww backend:
        elif cf.backend == "swww":

            # Check with pgrep if other backends they are running and kill them
            # because swaybg and hyprpaper are known to conflict with swww
            try:
                subprocess.check_output(["pgrep", "swaybg"], encoding='utf-8')
                subprocess.Popen(["killall", "swaybg"])
                time.sleep(0.005)
            except subprocess.CalledProcessError:
                pass
            try:
                subprocess.check_output(["pgrep", "hyprpaper"], encoding='utf-8')
                subprocess.Popen(["killall", "hyprpaper"])
                time.sleep(0.005)
            except subprocess.CalledProcessError:
                pass

            fill_types = {
                    "fill": "crop",
                    "fit": "fit",
                    "center": "no",
                    "stretch": "crop",
                    "tile": "no",
                    }
            fill = fill_types[cf.fill_option.lower()]

            # Check if swww-daemon is already running. If not, launch it:
            try:
                subprocess.check_output(["pgrep", "swww-daemon"], encoding='utf-8')
            except subprocess.CalledProcessError:
                subprocess.Popen(["swww-daemon"])
                print("The swww-daemon launched.")

            command = ["swww", "img", image_path]
            command.extend(["--resize", fill])
            command.extend(["--fill-color", cf.color])
            command.extend(["--transition-type", cf.swww_transition_type])
            command.extend(["--transition-step", str(cf.swww_transition_step)])
            command.extend(["--transition-angle", str(cf.swww_transition_angle)])
            command.extend(["--transition-duration", str(cf.swww_transition_duration)])
            command.extend(["--transition-fps", str(cf.swww_transition_fps)])
            if monitor != "All":
                command.extend(["--outputs", monitor])
            subprocess.Popen(command)
            print(f"{txt.msg_setwith} {cf.backend}")

        # feh backend:
        elif cf.backend == "feh":
            fill_types = {
                    "fill": "--bg-fill",
                    "fit": "--bg-max",
                    "center": "--bg-center",
                    "stretch": "--bg-scale",
                    "tile": "--bg-tile",
                    }
            fill = fill_types[cf.fill_option.lower()]
            command = ["feh", fill, "--image-bg", cf.color]
            command.extend([str(image_path)])
            subprocess.Popen(command)
            print(f"{txt.msg_setwith} {cf.backend}")

        # wallutils backend:
        elif cf.backend == "wallutils":
            fill_types = {
                    "fill": "scale",
                    "fit": "scale",
                    "center": "center",
                    "stretch": "stretch",
                    "tile": "tile",
                    }
            fill = fill_types[cf.fill_option.lower()]

            subprocess.Popen(["setwallpaper", "--mode", fill, image_path])
            print(f"{txt.msg_setwith} {cf.backend}")

        # hyprpaper backend:
        elif cf.backend == "hyprpaper":

            # Check if hyprpaper is already running, otherwise start it, and preload the wallpaper:
            try:
                subprocess.check_output(["pgrep", "hyprpaper"], encoding='utf-8')
            except subprocess.CalledProcessError:
                subprocess.Popen(["hyprpaper"])
                time.sleep(1)
            preload_command = ["hyprctl", "hyprpaper", "preload", image_path]

            # Decide which monitors are affected:
            if monitor == "All":
                monitors = get_monitor_names()
            else:
                monitors: list = [monitor]

            # Change the wallpaper one by one for each affected monitor:
            for m in monitors:
                wallpaper_command = ["hyprctl", "hyprpaper", "wallpaper", f"{m},{image_path}"]
                unload_command = ["hyprctl", "hyprpaper", "unload", "all"]
                result: str = ""
                retry_counter: int = 0

                # Since sometimes hyprpaper fails to change the wallpaper, we try until success:
                while result != "ok" and retry_counter < 10:
                    try:
                        subprocess.check_output(unload_command, encoding="utf-8").strip()
                        subprocess.check_output(preload_command, encoding="utf-8").strip()
                        result = subprocess.check_output(wallpaper_command, encoding="utf-8").strip()
                        time.sleep(0.1)
                    except Exception:
                        retry_counter += 1

        else:
            pass

        # Run a post command:
        if cf.post_command:
            modified_image_path = str(image_path).replace(" ", "\\ ")
            post_command = cf.post_command.replace("$wallpaper", modified_image_path)
            subprocess.Popen(post_command, shell=True)
            print(f'Post command {post_command} executed')

    except Exception as e:
        print(f"{txt.err_wall} {e}")
