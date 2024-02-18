import os
import sys
import subprocess
import psutil
import pyautogui
import time


if getattr(sys, 'frozen', False):
    # Running in executable mode
    base_path = sys._MEIPASS
else:
    # Running in normal Python mode
    base_path = os.path.abspath(".")


game_path = "C:/Program Files (x86)/Aiming Inc/danchroen/danchro.exe"

img_dir = os.path.join(base_path, "img")

result_path = os.path.join(img_dir, 'template_result.png')
matching_path = os.path.join(img_dir, 'template_matching.png')
tap_screen_path = os.path.join(img_dir, 'tap_screen.png')
begin_matchmaking_path = os.path.join(img_dir, 'begin_matchmaking.png')
clock_path = os.path.join(img_dir, 'playing_clock.png')
ping_path = os.path.join(img_dir, 'ping.png')
rank_up_rewards_path = os.path.join(img_dir, 'rank_up_rewards.png')
rank_up_close_path = os.path.join(img_dir, 'rank_up_close.png')
arena_path = os.path.join(img_dir, 'arena_main_menu.png')
start_game_path = os.path.join(img_dir, 'start_game.png')
mss_path = os.path.join(img_dir, 'mss.png')

total_matches = 0
start = time.time()


def check_process_running(process_name):
    for process in psutil.process_iter():
        try:
            # Get process name and check if it matches the provided process_name
            if process_name.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def get_image_location(template_path, threshold=None):
    if not threshold:
        threshold = 0.6
    try:
        return pyautogui.locateOnScreen(template_path, confidence=threshold)
    except pyautogui.ImageNotFoundException:
        return None


def is_matching():
    return get_image_location(matching_path)


def is_done():
    return get_image_location(result_path)


def is_playing():
    return get_image_location(clock_path, 0.9) or get_image_location(ping_path, 0.9)


def is_waiting():
    return get_image_location(begin_matchmaking_path)


def is_ranked_up():
    return get_image_location(rank_up_rewards_path)


def start_game():
    subprocess.Popen(game_path)
    started = False
    while not started:
        try:
            start_game_menu = pyautogui.locateOnScreen(start_game_path, confidence=0.6)
        except pyautogui.ImageNotFoundException:
            continue
        if start_game_menu:
            started = True
            assert started
            print('Game started')
            return start_game_menu


def goto_mss(game_menu_button):
    pyautogui.click(game_menu_button.left, game_menu_button.top)
    arena = False
    while not arena:
        try:
            arena_button = pyautogui.locateOnScreen(arena_path, confidence=0.6)
            if arena_button:
                arena = True
                print('Main menu loaded. Going to arena.')
                time.sleep(2)
                pyautogui.click(arena_button.left + 100, arena_button.top + 150)
                print('Clicked on Arena')
        except pyautogui.ImageNotFoundException:
            continue

    print('Waiting for MSS to load...')
    mss = False
    while not mss:
        try:
            mss_button = pyautogui.locateOnScreen(mss_path, confidence=0.6)
            if mss_button:
                mss = True
                print('MSS loaded.')
                time.sleep(2)
                pyautogui.click(mss_button.left, mss_button.top)
                print('Clicked on MSS')
                time.sleep(2)
        except pyautogui.ImageNotFoundException:
            continue


if __name__ == '__main__':
    if not check_process_running("danchro.exe"):
        print("Game not running, starting game...")
        start_game_menu_button = start_game()
        time.sleep(2)
        print("Waiting for main menu to load...")
        goto_mss(start_game_menu_button)

    try:
        while True:
            if is_playing():
                print('Playing...')
                time.sleep(20)
                continue
            elif is_matching():
                print('Matching...')
                time.sleep(20)
                continue
            elif is_ranked_up():
                print('Ranked up ! Accepting rewards...')
                rank_up_rewards = get_image_location(rank_up_close_path)
                pyautogui.click(rank_up_rewards.left, rank_up_rewards.top)
                time.sleep(5)
                print('Rewards Accepted!')
                continue
            elif is_waiting():
                # If not found it means is not matching
                print('Not matching, clicking on begin_matchmaking')
                try:
                    begin_matchmaking = pyautogui.locateOnScreen(begin_matchmaking_path, confidence=0.6)
                except pyautogui.ImageNotFoundException:
                    continue
                pyautogui.click(begin_matchmaking.left, begin_matchmaking.top)
                print('Clicked on begin_matchmaking')
                total_matches += 1
                time.sleep(10)
                continue
            elif is_done():
                print('Done ! Going back to MSS menu...')
                try:
                    tap_screen = pyautogui.locateOnScreen(result_path, confidence=0.6)
                except pyautogui.ImageNotFoundException:
                    continue
                # Click two times as the result screen has two steps
                pyautogui.click(tap_screen.left, tap_screen.top)
                time.sleep(5)
                pyautogui.click(tap_screen.left, tap_screen.top)
                time.sleep(10)
                print('Back to MSS menu!')
                continue
            else:
                print('Nothing found, probably between menus')
                time.sleep(10)
    except KeyboardInterrupt:
        print("Total matches: ", total_matches)
        end = time.time()
        print("Total time elapsed: ", end - start)
        print("Ctrl+C pressed. Exiting program.")