import json
import os
import sys
import time

import questionary
import yt_dlp
from pyfiglet import Figlet
from rich import print as rprint
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

# Initial Configuration
console = Console()
SETTINGS_FILE = "settings.json"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_settings():
    """Loads configuration from JSON file."""
    default_settings = {"download_path": ""}
    if not os.path.exists(SETTINGS_FILE):
        return default_settings

    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return default_settings


def save_settings(settings):
    """Saves configuration to JSON file."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        rprint(f"[red]Error saving settings: {e}[/red]")
        return False


def show_banner():
    clear_screen()
    f = Figlet(font="slant")
    title = f.renderText("EJ  TOOLS")

    panel = Panel(
        Align.center(
            f"[bold cyan]{title}[/bold cyan]\n"
            "[bold white]Made by [link=https://x.com/ej3mplo]@ej3mplo[/link][/bold white]\n"
        ),
        border_style="cyan",
        expand=False,
    )
    rprint(panel)
    time.sleep(0.5)


def get_download_path_opt():
    """Reads settings and returns the yt-dlp 'paths' dict if a custom path is set."""
    settings = load_settings()
    path = settings.get("download_path", "")

    if path and os.path.isdir(path):
        return {"home": path}
    elif path:
        try:
            os.makedirs(path, exist_ok=True)
            return {"home": path}
        except:
            pass

    return {}


def get_video_opts(url, quality, mute_audio=False):
    """Configures download options."""
    height_map = {"4k": 2160, "1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
    target_height = height_map.get(quality, 1080)

    if mute_audio:
        format_str = f"bestvideo[height={target_height}]/bestvideo"
        merge_format = "mp4"
    else:
        format_str = f"bestvideo[height={target_height}]+bestaudio/best[height={target_height}]/best"
        merge_format = "mkv" if quality == "4k" else "mp4"

    return {
        "format": format_str,
        "merge_output_format": merge_format,
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "paths": get_download_path_opt(),
        "ffmpeg_location": "./" if os.path.exists("./ffmpeg.exe") else None,
    }


def get_audio_opts(quality):
    """Configures audio download options."""
    bitrate_map = {
        "High (320kbps)": "320",
        "Medium (192kbps)": "192",
        "Low (128kbps)": "128",
    }

    return {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate_map.get(quality, "192"),
            }
        ],
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "paths": get_download_path_opt(),
        "ffmpeg_location": "./" if os.path.exists("./ffmpeg.exe") else None,
    }


def download_media(url, options, type_desc):
    """Executes the download with a progress bar."""

    save_path = options.get("paths", {}).get("home", "Current Folder")
    console.print(f"\n[bold green]➜ Starting download: {type_desc}...[/bold green]")
    console.print(f"[dim]➜ Saving to: {save_path}[/dim]")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            transient=True,
        ) as progress:
            task_id = progress.add_task(f"Downloading...", total=100)

            def progress_hook(d):
                if d["status"] == "downloading":
                    try:
                        p = d.get("_percent_str", "0%").replace("%", "")
                        progress.update(
                            task_id,
                            completed=float(p),
                            description=f"[cyan]Downloading: {d.get('filename', 'File')}...",
                        )
                    except:
                        pass
                elif d["status"] == "finished":
                    progress.update(
                        task_id,
                        completed=100,
                        description="[green]Processing conversion...[/green]",
                    )

            options["progress_hooks"] = [progress_hook]

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])

        rprint(f"\n[bold green]✔ Download completed successfully![/bold green]\n")

    except yt_dlp.utils.DownloadError as e:
        rprint(f"\n[bold red]✘ Download Error:[/bold red] {e}")
    except Exception as e:
        rprint(f"\n[bold red]✘ Unexpected Error:[/bold red] {e}")


def menu_settings():
    """Sub-menu to handle configuration."""
    while True:
        clear_screen()
        settings = load_settings()
        current_path = settings.get("download_path", "")
        if not current_path:
            current_path = "[Default: Current Script Folder]"

        rprint(
            Panel(
                f"[bold]Current Download Path:[/bold]\n[yellow]{current_path}[/yellow]",
                title="Settings",
                border_style="yellow",
            )
        )

        action = questionary.select(
            "Settings Menu:",
            choices=["Change Download Path", "Reset to Default", "Back to Main Menu"],
        ).ask()

        if action is None:
            return

        if action == "Back to Main Menu":
            break

        elif action == "Reset to Default":
            settings["download_path"] = ""
            save_settings(settings)
            rprint("[green]Path reset to default.[/green]")
            time.sleep(1)

        elif action == "Change Download Path":
            new_path = questionary.path(
                "Enter absolute path (e.g., C:/Downloads or /home/user/):"
            ).ask()

            if new_path is None:
                continue

            if (
                os.path.exists(new_path)
                or questionary.confirm(
                    f"Path '{new_path}' does not exist. Create it?"
                ).ask()
            ):
                try:
                    if not os.path.exists(new_path):
                        os.makedirs(new_path, exist_ok=True)

                    settings["download_path"] = new_path
                    save_settings(settings)
                    rprint("[green]Path updated successfully![/green]")
                    time.sleep(1)
                except Exception as e:
                    rprint(f"[red]Error creating directory: {e}[/red]")
                    input("Press Enter...")
            else:
                rprint("[yellow]Change cancelled.[/yellow]")
                time.sleep(1)


def main():
    try:
        while True:
            show_banner()

            action = questionary.select(
                "What do you want to do?",
                choices=[
                    "Video (With Audio)",
                    "Video (No Audio)",
                    "Audio (Music/Podcast)",
                    "Settings",
                    "Exit",
                ],
                style=questionary.Style(
                    [
                        ("qmark", "fg:#00ff00 bold"),
                        ("question", "fg:#ffffff bold"),
                        ("answer", "fg:#00ffff bold"),
                        ("pointer", "fg:#00ff00 bold"),
                    ]
                ),
            ).ask()

            if action is None:
                raise KeyboardInterrupt

            if action == "Exit":
                clear_screen()
                rprint(
                    Panel.fit(
                        "[bold cyan]Thanks for using EJ Tools! Goodbye.[/bold cyan]",
                        border_style="cyan",
                    )
                )
                # Espera 2 segundos para leer el mensaje y luego cierra todo
                time.sleep(2)
                sys.exit(0)

            if action == "Settings":
                menu_settings()
                continue

            # --- Input de URL ---
            url = questionary.text(
                "Paste the URL (Youtube, Instagram, TikTok, Twitter...):"
            ).ask()

            if url is None:
                raise KeyboardInterrupt
            if not url.strip():
                continue

            # --- Procesar Video/Audio ---
            if "Video" in action:
                is_muted = "(No Audio)" in action

                quality = questionary.select(
                    "Select video quality:",
                    choices=["4k", "1080p", "720p", "480p", "360p"],
                ).ask()

                if quality is None:
                    raise KeyboardInterrupt

                opts = get_video_opts(url, quality, mute_audio=is_muted)
                label = f"Video ({quality}) {'[Muted]' if is_muted else ''}"
                download_media(url, opts, label)

            elif "Audio" in action:
                quality = questionary.select(
                    "Select audio quality:",
                    choices=["High (320kbps)", "Medium (192kbps)", "Low (128kbps)"],
                ).ask()

                if quality is None:
                    raise KeyboardInterrupt

                opts = get_audio_opts(quality)
                download_media(url, opts, f"Audio MP3")

            rprint("\n[dim]Press Enter to continue or Ctrl+C to exit...[/dim]")
            input()

    except KeyboardInterrupt:
        rprint("\n\n[bold red]! Operation cancelled by user.[/bold red]")
        sys.exit(0)


if __name__ == "__main__":
    main()
