import streamlit as st
from datetime import datetime
import io
from PIL import Image
import random

# 페이지 설정
st.set_page_config(page_title="🎉 롤링페이퍼", layout="wide")

# CSS 스타일 추가
st.markdown("""
    <style>
    .memo-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .memo-name {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .memo-text {
        font-size: 1em;
        margin-bottom: 10px;
        white-space: pre-wrap;
    }
    .memo-date {
        font-size: 0.8em;
        opacity: 0.8;
        text-align: right;
    }
    .memo-image {
        margin: 10px 0;
        border-radius: 8px;
        max-width: 300px;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "memos" not in st.session_state:
    st.session_state.memos = []
if "camera_photo_captured" not in st.session_state:
    st.session_state.camera_photo_captured = None

# 제목
st.title("🎉 나소영 롤링페이퍼")
st.markdown("소영이에게 하고 싶은 말을 메모로 남겨주세요! ✨")

# 메모 입력 섹션
st.markdown("---")
col_left, col_right = st.columns([0.5, 0.5])

# 왼쪽: 사진
with col_left:
    st.subheader("📸 사진추가")
    camera_photo = st.camera_input("사진을 촬영해주세요", key="camera_input")
    
    uploaded_photo = st.file_uploader("또는 사진 파일 선택", type=["png", "jpg", "jpeg"], key="photo_upload")
    
    # 카메라 또는 업로드 사진 선택
    selected_photo = camera_photo if camera_photo else uploaded_photo


# 오른쪽: 이름과 메모 입력
with col_right:
    st.subheader("✍️ 메시지 작성")
    
    with st.form("memo_form", clear_on_submit=True):
        author_name = st.text_input("이름을 입력해주세요", placeholder="예: 철수")
        memo_text = st.text_area("메모를 작성해주세요", placeholder="친구에게 하고 싶은 말을 써주세요!", height=290)
        
        submitted = st.form_submit_button("메모 추가 ✏️", use_container_width=True)
        
        if submitted:
            if author_name.strip() and memo_text.strip():
                photo_to_save = None
                
                # 사진 리사이즈 로직
                if selected_photo:
                    try:
                        # 이미지 열기
                        img = Image.open(selected_photo)
                        
                        # 메모 카드 너비에 맞게 리사이즈 (메모 너비: 약 200px)
                        max_width = 200
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img_resized = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        
                        # 리사이즈된 이미지를 바이트로 변환
                        img_byte_arr = io.BytesIO()
                        img_resized.save(img_byte_arr, format='PNG')
                        photo_to_save = img_byte_arr.getvalue()
                    except Exception as e:
                        st.error(f"사진 처리 중 오류 발생: {e}")
                        photo_to_save = None
                
                # 랜덤 배경색 생성
                colors = [
                    "#667eea", "#764ba2", "#f093fb", "#4facfe", "#43e97b", 
                    "#fa709a", "#fee140", "#30b0fe", "#a8edea", "#fed6e3",
                    "#ff9a76", "#fcb69f", "#a29bfe", "#6c5ce7", "#00b894",
                    "#ff7675", "#fdcb6e", "#0984e3", "#6c5ce7", "#e17055"
                ]
                random_color = random.choice(colors)
                
                new_memo = {
                    "name": author_name.strip(),
                    "text": memo_text.strip(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "photo": photo_to_save,
                    "color": random_color
                }
                st.session_state.memos.insert(0, new_memo)
                st.success("메모가 추가되었습니다! 🎉")
                st.rerun()
            else:
                st.error("이름과 메모를 모두 입력해주세요!")

# 메모 표시 섹션
st.markdown("---")
st.subheader(f"💌 남겨진 메모 ({len(st.session_state.memos)}개)")

if st.session_state.memos:
    # 메모를 5개씩 한 줄에 표시
    cols = st.columns(5)
    
    for idx, memo in enumerate(st.session_state.memos):
        col_index = idx % 5
        
        with cols[col_index]:
            with st.container():
                # 삭제 버튼
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.memos.pop(idx)
                    st.rerun()
                
                # 사진과 메모를 하나의 카드로
                with st.container():
                    # 사진 표시
                    if memo.get("photo"):
                        st.image(memo["photo"], width='stretch')
                    
                    # 메모 내용 (랜덤 배경색 적용)
                    memo_color = memo.get("color", "#667eea")
                    st.markdown(f"""
                        <div class="memo-box" style="background: linear-gradient(135deg, {memo_color} 0%, {memo_color}dd 100%); min-height: 140px; margin-top: -10px; border-radius: 0 0 10px 10px;">
                            <div class="memo-name">💬 {memo['name']}</div>
                            <div class="memo-text" style="font-size: 0.9em; line-height: 1.4;">{memo['text']}</div>
                            <div class="memo-date">📅 {memo['timestamp']}</div>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.info("아직 메모가 없습니다. 첫 번째 메모를 남겨주세요! 🌟")
