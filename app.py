import streamlit as st
import pandas as pd
import hashlib

# ==========================================
# PHẦN 1: CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(page_title="Phân tích Data Hasaki & TGSK", layout="wide")

# ==========================================
# PHẦN 2: XÂY DỰNG CHỨC NĂNG ĐĂNG NHẬP & ĐĂNG KÝ
# ==========================================

# Mở rộng Database người dùng, thêm mã hóa mật khẩu để an toàn hơn
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "admin": {
            "password_hash": hashlib.sha256("123".encode()).hexdigest(),
            "role": "Admin",
            "name": "Quản trị viên"
        },
        "nguoidung": {
            "password_hash": hashlib.sha256("123".encode()).hexdigest(),
            "role": "Analyst",
            "name": "Nhà phân tích"
        }
    }

# Trạng thái phiên
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.role = "Guest"

def authenticate_user():
    st.sidebar.title("🔐 Xác thực Người dùng")
    
    # Tạo các tab (thẻ) để chuyển đổi giữa Đăng nhập và Đăng ký
    tab_login, tab_signup = st.sidebar.tabs(["Đăng nhập", "Đăng ký"])

    # --- TAB ĐĂNG NHẬP ---
    with tab_login:
        st.subheader("Đăng nhập hệ thống")
        username_login = st.text_input("Tên đăng nhập", key="login_user")
        password_login = st.text_input("Mật khẩu", type="password", key="login_pass")
        
        if st.button("Đăng nhập", key="btn_login"):
            hashed_pwd = hashlib.sha256(password_login.encode()).hexdigest()
            if username_login in st.session_state.user_db and st.session_state.user_db[username_login]["password_hash"] == hashed_pwd:
                st.session_state.logged_in = True
                st.session_state.current_user = st.session_state.user_db[username_login]["name"]
                st.session_state.role = st.session_state.user_db[username_login]["role"]
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Tên đăng nhập hoặc mật khẩu không đúng!")

    # --- TAB ĐĂNG KÝ ---
    with tab_signup:
        st.subheader("Tạo tài khoản mới")
        new_name = st.text_input("Họ và Tên")
        new_username = st.text_input("Tên đăng nhập muốn tạo")
        new_password = st.text_input("Mật khẩu", type="password")
        confirm_password = st.text_input("Nhập lại mật khẩu", type="password")
        
        # Mặc định tài khoản đăng ký mới sẽ có quyền 'Analyst' (hoặc 'Guest' tùy bạn quyết định)
        if st.button("Đăng ký tài khoản"):
            if new_username in st.session_state.user_db:
                st.error("Tên đăng nhập này đã tồn tại! Vui lòng chọn tên khác.")
            elif new_password != confirm_password:
                st.error("Mật khẩu nhập lại không khớp!")
            elif not new_username or not new_password or not new_name:
                st.warning("Vui lòng điền đầy đủ thông tin.")
            else:
                # Thêm user mới vào "Database" tạm thời (Session State)
                hashed_new_pwd = hashlib.sha256(new_password.encode()).hexdigest()
                st.session_state.user_db[new_username] = {
                    "password_hash": hashed_new_pwd,
                    "role": "Analyst", # Mặc định quyền Analyst
                    "name": new_name
                }
                st.success("Tạo tài khoản thành công! Bạn có thể chuyển sang tab Đăng nhập.")

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.role = "Guest"
    st.rerun()

# ==========================================
# PHẦN 3: GIAO DIỆN CHÍNH (GUI) - Cải thiện thẩm mỹ
# ==========================================
def main_app():
    # Sử dụng CSS tùy chỉnh để làm đẹp (Tùy chọn, bạn có thể thêm nhiều CSS hơn nếu muốn)
    st.markdown("""
        <style>
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            h1 {
                color: #2E86C1; /* Màu xanh nước biển cho tiêu đề */
                text-align: center;
                padding-bottom: 20px;
            }
            .stMetric {
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.write(f"### 👋 Xin chào, {st.session_state.current_user}")
        st.info(f"🛡️ Quyền hạn: **{st.session_state.role}**")
        if st.button("Đăng xuất", use_container_width=True): # Nút tràn viền cho đẹp
            logout()
            
        st.markdown("---")
        
        # Menu Navigation sử dụng radio button cho giống thanh điều hướng hơn
        menu = ["📊 Tổng quan Dữ liệu", "📈 Trực quan hóa (EDA)", "🤖 Mô hình Học máy"]
        
        if st.session_state.role == "Admin":
            menu.append("⚙️ Quản trị Dữ liệu (CRUD)")
            
        choice = st.radio("Chuyển hướng Menu:", menu)

    # --- NỘI DUNG CHÍNH ---
    st.title("HỆ THỐNG PHÂN TÍCH DỮ LIỆU SỨC KHỎE - LÀM ĐẸP")
    st.markdown("<h4 style='text-align: center; color: gray;'>Nguồn dữ liệu thực tế từ Hasaki & Thế Giới Skinfood</h4>", unsafe_allow_html=True)
    st.divider() # Đường kẻ ngang

    # Hiển thị nội dung tương ứng
    if choice == "📊 Tổng quan Dữ liệu":
        st.header("1. Tổng quan thị trường")
        
        # Sử dụng columns để hiển thị các chỉ số (Metrics) cho giống Dashboard chuyên nghiệp
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Tổng số Sản phẩm (Hasaki)", value="12,450", delta="5%")
        with col2:
            st.metric(label="Tổng số Sản phẩm (TGSK)", value="8,920", delta="-2%")
        with col3:
            st.metric(label="Giá trị trung bình", value="350k VNĐ")
            
        st.write("---")
        st.write("Nơi hiển thị bảng dữ liệu tóm tắt...")

    elif choice == "📈 Trực quan hóa (EDA)":
        st.header("2. Trực quan hóa dữ liệu (EDA)")
        # ... (Nơi gọi hàm vẽ biểu đồ của Người 2)
        st.write("Khu vực hiển thị biểu đồ.")

    elif choice == "🤖 Mô hình Học máy":
        st.header("3. Tích hợp Mô hình Machine Learning")
        # ... (Nơi tích hợp code của Người 2)
        st.write("Giao diện cấu hình và chạy mô hình phân tích.")

    elif choice == "⚙️ Quản trị Dữ liệu (CRUD)":
        st.header("4. Quản trị và Thao tác Dữ liệu")
        # ... (Nơi gọi hàm CRUD của Người 2)
        st.write("Giao diện Thêm/Sửa/Xóa dữ liệu.")

# ==========================================
# KHỞI CHẠY ỨNG DỤNG
# ==========================================
if not st.session_state.logged_in:
    authenticate_user()
else:
    main_app()