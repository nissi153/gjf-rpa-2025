import pyautogui
import pyperclip
import time

# === 설정값 ===
friend_name = "홍길동"  # 메시지를 보낼 친구 이름
message = "안녕! 자동화로 보낸 메시지야 😄"

# === Step 1. 카카오톡 창 활성화 ===
# Alt + Tab을 사용해 카카오톡으로 전환 (필요에 따라 여러 번 반복)
pyautogui.hotkey('alt', 'tab')
time.sleep(1)

# === Step 2. 친구 검색창 열기 (Ctrl + F) ===
pyautogui.hotkey('ctrl', 'f')
time.sleep(1)

# === Step 3. 친구 이름 클립보드에 복사 후 붙여넣기 ===
pyperclip.copy(friend_name)  # 친구 이름을 클립보드에 복사
pyautogui.hotkey('ctrl', 'v')  # 클립보드 내용 붙여넣기
time.sleep(1)

# === Step 4. 채팅방 열기 ===
pyautogui.press('enter')
time.sleep(1)

# === Step 5. 메시지 클립보드에 복사 후 붙여넣기 및 전송 ===
pyperclip.copy(message)  # 메시지를 클립보드에 복사
pyautogui.hotkey('ctrl', 'v')  # 클립보드 내용 붙여넣기
time.sleep(0.5)
pyautogui.press('enter')

print("메시지 전송 완료!")
