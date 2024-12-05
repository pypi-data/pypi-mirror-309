# django-ace-widget

Django admin widget using ACE editor for TextField.

## 安装

```shell
pip install django-ace-widget
```

## 使用

*app/admin.py*

```python
from django.db import models
from django.contrib import admin

from django_ace_widget.widgets import ace_widget
from .models import Page
from .models import Block


class BlockInline(admin.TabularInline):
    model = Block
    extra = 0
    formfield_overrides = {
        models.TextField: {
            # inline模式下，使用100%显示不友好，请使用px指定宽度。
            "widget": ace_widget("java", width="800px"),
        },
    }


class PageAdmin(admin.ModelAdmin):
    list_display = ["title"]
    formfield_overrides = {
        models.TextField: {
            "widget": ace_widget("python"),
        },
    }
    inlines = [
        BlockInline,
    ]


admin.site.register(Page, PageAdmin)

```

## ace_widget参数

```python
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
```

## ace皮肤

- clouds
- cobalt
- eclipse
- nord_dark
- dawn
- solarized_light
- chaos
- monokai
- github
- merbivore_soft
- katzenmilch
- chrome
- tomorrow
- clouds_midnight
- tomorrow_night_blue
- gob
- gruvbox
- xcode
- textmate
- iplastic
- crimson_editor
- tomorrow_night_bright
- mono_industrial
- merbivore
- sqlserver
- idle_fingers
- ambiance
- kuroir
- pastel_on_dark
- kr_theme
- twilight
- solarized_dark
- tomorrow_night
- terminal
- dracula
- one_dark
- vibrant_ink
- tomorrow_night_eighties
- dreamweaver

## 版本记录

### v0.1.0

- 版本首发。
