"""
interface.py - Module giao diện (TV4)

Trách nhiệm:
    - Nhận tốc độ và khoảng cách từ người dùng.
    - Gọi callback on_submit(speed, distance).
    - Hiển thị status, message, recommendation (và rule_id, d_min nếu có).

KHÔNG làm trong module này (theo module_contracts.md):
    - Không tính D_min.
    - Không tự xác định SAFE / WARNING / DANGER.
    - Không tự validation dữ liệu (việc của TV3, được TV5 gọi).
"""

import tkinter as tk
from tkinter import ttk

# Chỉ là màu hiển thị theo trạng thái do hệ thống trả về, không phải logic suy luận.
STATUS_COLORS = {
    "SAFE": "#2e7d32",
    "WARNING": "#ef6c00",
    "DANGER": "#c62828",
    "ERROR": "#6a1b9a",
}
DEFAULT_COLOR = "#455a64"


class CollisionWarningApp:
    def __init__(self, root, on_submit):
        self.root = root
        self.on_submit = on_submit

        root.title("Hệ thống cảnh báo va chạm")
        root.geometry("460x470")
        root.resizable(False, False)

        self.speed_var = tk.StringVar()
        self.distance_var = tk.StringVar()
        self.status_var = tk.StringVar(value="—")
        self.message_var = tk.StringVar(value="Chưa có kết quả.")
        self.recommendation_var = tk.StringVar(value="—")
        self.extra_var = tk.StringVar(value="")

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="HỆ THỐNG CẢNH BÁO VA CHẠM",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(0, 12))

        # --- Khung nhập liệu
        form = ttk.LabelFrame(main, text="Dữ liệu đầu vào", padding=12)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Tốc độ (km/h):").grid(row=0, column=0, sticky="w", pady=4)
        self.speed_entry = ttk.Entry(form, textvariable=self.speed_var)
        self.speed_entry.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=4)

        ttk.Label(form, text="Khoảng cách (m):").grid(row=1, column=0, sticky="w", pady=4)
        self.distance_entry = ttk.Entry(form, textvariable=self.distance_var)
        self.distance_entry.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=4)

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=12)
        ttk.Button(buttons, text="Đánh giá", command=self.submit).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(buttons, text="Xóa", command=self.clear).pack(side="left", expand=True, fill="x", padx=(4, 0))

        # --- Khung kết quả
        result = ttk.LabelFrame(main, text="Kết quả", padding=12)
        result.pack(fill="both", expand=True)

        self.status_label = tk.Label(
            result,
            textvariable=self.status_var,
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=DEFAULT_COLOR,
            pady=8,
        )
        self.status_label.pack(fill="x", pady=(0, 10))

        ttk.Label(result, text="Thông báo:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(result, textvariable=self.message_var, wraplength=400, justify="left").pack(anchor="w", pady=(0, 8))

        ttk.Label(result, text="Khuyến nghị:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Label(result, textvariable=self.recommendation_var, wraplength=400, justify="left").pack(anchor="w", pady=(0, 8))

        ttk.Label(result, textvariable=self.extra_var, foreground="#607d8b").pack(anchor="w")

        # Phím tắt
        self.root.bind("<Return>", lambda _e: self.submit())
        self.speed_entry.focus_set()

    # ------------------------------------------------------------- Actions
    def submit(self):
        """Lấy dữ liệu người dùng nhập và gọi callback on_submit(speed, distance).

        Dữ liệu được truyền nguyên dạng (chỉ bỏ khoảng trắng đầu/cuối);
        việc kiểm tra hợp lệ do validate_input() của TV3 đảm nhiệm.
        """
        speed = self.speed_var.get().strip()
        distance = self.distance_var.get().strip()

        try:
            result = self.on_submit(speed, distance)
        except Exception as exc:  # lỗi bất ngờ từ các module phía sau
            result = {
                "status": "ERROR",
                "message": f"Đã xảy ra lỗi khi xử lý: {exc}",
                "recommendation": "Vui lòng thử lại hoặc liên hệ nhóm phát triển.",
            }

        self.show_result(result)

    def clear(self):
        self.speed_var.set("")
        self.distance_var.set("")
        self.status_var.set("—")
        self.message_var.set("Chưa có kết quả.")
        self.recommendation_var.set("—")
        self.extra_var.set("")
        self.status_label.config(bg=DEFAULT_COLOR)
        self.speed_entry.focus_set()

    def show_result(self, result):
        """Chỉ hiển thị dữ liệu nhận được, không tự suy luận lại."""
        if not isinstance(result, dict):
            result = {}

        status = str(result.get("status", "ERROR"))
        message = result.get("message", "Không nhận được thông báo từ hệ thống.")
        recommendation = result.get("recommendation", "—")

        self.status_var.set(status)
        self.message_var.set(message)
        self.recommendation_var.set(recommendation)
        self.status_label.config(bg=STATUS_COLORS.get(status, DEFAULT_COLOR))

        # Các trường tùy chọn mà TV3 có thể bổ sung
        extras = []
        if result.get("rule_id") is not None:
            extras.append(f"Luật: {result['rule_id']}")
        if result.get("d_min") is not None:
            extras.append(f"D_min: {result['d_min']}")
        self.extra_var.set("   |   ".join(extras))


def run_app(on_submit):
    """Khởi chạy giao diện.

    Args:
        on_submit: callback on_submit(speed, distance) -> dict
            (dict có tối thiểu: status, message, recommendation).
    """
    root = tk.Tk()
    CollisionWarningApp(root, on_submit)
    root.mainloop()


if __name__ == "__main__":
    # Chạy thử độc lập giao diện bằng callback giả (không chứa logic suy luận thật).
    def _fake_on_submit(speed, distance):
        return {
            "status": "WARNING",
            "message": f"[Dữ liệu giả] Nhận speed={speed}, distance={distance}.",
            "recommendation": "[Dữ liệu giả] Chỉ dùng để kiểm tra giao diện.",
            "rule_id": "R_DEMO",
            "d_min": 0.0,
        }

    run_app(_fake_on_submit)
