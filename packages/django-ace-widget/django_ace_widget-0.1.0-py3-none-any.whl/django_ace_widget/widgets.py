import uuid
from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe


def ace_widget(
    language,
    theme="xcode",
    width="100%",
    minLines=15,
    maxLines=15,
):
    """创建AceWidget类。

    参数：
        language: 语言，如：html, java, python等。
        theme: 编辑器皮肤。默认为：xcode。
        width: 编辑器宽度。默认为：100%。可以设置为800px等。
        minLines: 初始行数。默认为：15。
        maxLines: 最大行数。默认为：15。

    返回值：
        AceWidget类

    """

    class AceWidget(Textarea):
        class Media:
            css = {
                "screen": [
                    "django_ace_widget/ace_widget.css",
                ]
            }
            js = [
                "admin/js/vendor/jquery/jquery.js",
                "ace-builds/ace.js",
                "django_ace_widget/ace_widget.js",
                "admin/js/jquery.init.js",
            ]

        def render(self, name, value, **kwargs):
            random_id = uuid.uuid4().hex
            html = super().render(name, value, **kwargs)
            html += f"""<div class="django_ace_widget_wrapper"
    id="django_ace_widget_wrapper_{random_id}"
    language="{language}"
    textarea_id="id_{name}"
    theme="{theme}"
    minLines="{minLines}"
    maxLines="{maxLines}"
    style="width: {width};"></div>"""
            return mark_safe(html)

    return AceWidget
