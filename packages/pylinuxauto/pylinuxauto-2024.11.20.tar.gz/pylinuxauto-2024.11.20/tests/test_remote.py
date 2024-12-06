from pylinuxauto.remote import remote_pylinuxauto

rpl = remote_pylinuxauto(
    user="uos",
    ip="192.168.1.100",
    password="123456",
    auto_restart=False
)

rpl.click_element_by_attr_path("/dde-dock/Btn_文件管理器")

rpl.click_element_by_ocr("计算机", "192.168.1.101")