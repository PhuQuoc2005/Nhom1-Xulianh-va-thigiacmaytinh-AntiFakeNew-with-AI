import logging

def get_logger(module_name: str):
    """
    Tiện ích khởi tạo Logger chuẩn cho toàn bộ dự án.
    Giúp các thành viên in log ra terminal một cách đồng nhất thay vì dùng hàm print() bừa bãi.
    """
    logger = logging.getLogger(module_name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # In ra Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
