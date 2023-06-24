from django.core.mail import send_mail


def send_mail_remind(project_name):
    subject = "AIGC共创网站-项目人员招募成功提醒"
    html_message = """
        <p>尊敬的用户 您好</p>
        <p>您发起的项目 %s，已有开发者申请加入，请及时与开发者联系，感谢你的使用! </p>
    """ % project_name
    # recipient_list = '2951121599@qq.com'  # 接收者邮件列表
    send_mail(subject, "", "2951121599@qq.com", html_message=html_message, recipient_list=['2951121599@qq.com'])
