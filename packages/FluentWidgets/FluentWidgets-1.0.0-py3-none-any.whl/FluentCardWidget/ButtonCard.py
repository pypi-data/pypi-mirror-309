from typing import Union

from PySide6.QtGui import Qt, QIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import (
    PushButton, PrimaryPushButton, TransparentPushButton, ToolButton, PrimaryToolButton, ComboBox, TitleLabel,
    TransparentToolButton, EditableComboBox, DropDownPushButton, PrimaryDropDownPushButton, FluentIconBase,
    TransparentDropDownPushButton, DropDownToolButton, PrimaryDropDownToolButton, TransparentDropDownToolButton,
    SplitPushButton, PrimarySplitPushButton, HyperlinkButton, CheckBox, RoundMenu, Action, IconWidget, BodyLabel,
    Slider, CaptionLabel, SwitchButton
)

from .CustomWidget.CustomCard import (
    CustomSwitchButtonCard, CustomDropDownCard,ExpandGroupCard, CustomCardParent, CustomButtonCardParent,
    CustomCheckBoxCard, SliderCardParent
)
from .CustomWidget.CustomComboBoxCard import CustomComboBoxCard


class CustomCard(CustomCardParent):
    def __init__(self, icon=None, title=None, content=None, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(80)

    def initLayout(self):
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.hBoxLayout.setContentsMargins(20, 11, 48, 11) # left top right bottom
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addStretch(1)
        return self

    def initIcon(self, icon):
        # set card icon
        self.iconWidget = IconWidget(icon)
        self.iconWidget.setFixedSize(24, 24)
        return self

    def initTitle(self, title):
        # set card title
        self.titleLabel = BodyLabel(title, self)
        return self

    def initContent(self, content):
        # set card content
        self.contentLabel = CaptionLabel(content, self)
        # self.contentLabel.setTextColor("#606060", "#d2d2d2")
        return self


class CustomButtonCard(CustomButtonCardParent, CustomCard):
    def __init__(self, icon, title, content, parent=None, btType=None, btText=None, btIcon=None):
        CustomCard.__init__(self, parent)
        self.initIcon(icon).initTitle(title).initContent(content).initLayout()
        self.initButton(btType)

    def initButton(self, btType):
        self.button = btType(self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        return self

    def setButtonText(self, text: str):
        self.button.setFixedWidth(100)
        self.button.setText(text)
        return self

    def setButtonIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.button.setIcon(icon)
        return self


# 标准按钮
class ButtonCard(CustomButtonCard):
    """ 标准按钮卡片 """
    def __init__(self, icon, title, content, btText=None, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, PushButton)
        self.setButtonText(btText).setButtonIcon(btIcon)


class PrimaryButtonCard(CustomButtonCard):
    """ 主题色按钮卡片 """
    def __init__(self, icon, title, content, btText=None, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, PrimaryPushButton)
        self.setButtonText(btText).setButtonIcon(btIcon)


class TransparentButtonCard(CustomButtonCard):
    """ 透明按钮卡片 """
    def __init__(self, icon, title, content, btText=None, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, TransparentPushButton)
        self.setButtonText(btText).setButtonIcon(btIcon)


# 工具按钮
class ToolButtonCard(CustomButtonCard):
    """ 工具按钮卡片 """
    def __init__(self, icon, title, content, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, ToolButton)
        self.setButtonIcon(btIcon)


class PrimaryToolButtonCard(CustomButtonCard):
    """ 主题色工具按钮卡片 """
    def __init__(self, icon, title, content, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, PrimaryToolButton)
        self.setButtonIcon(btIcon)


class TransparentToolButtonCard(CustomButtonCard):
    """ 透明工具按钮卡片 """
    def __init__(self, icon, title, content, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, TransparentToolButton)
        self.setButtonIcon(btIcon)


# 状态卡关按钮
class SwitchButtonCard(CustomSwitchButtonCard, CustomButtonCard):
    """ 状态卡关按钮 """
    def __init__(self, icon, title, content, isChecked=False, parent=None):
        CustomButtonCard.__init__(self, icon, title, content, parent, SwitchButton)
        self.setButtonChecked(isChecked)
        self.button._onText = "开"
        self.button._offText = "关"

    def setButtonChecked(self, isChecked=False):
        self.button.setChecked(isChecked)


# 复选框
class CheckBoxCard(CustomCheckBoxCard, CustomButtonCard):
    """ 复选框 """
    def __init__(self, icon, title, content, isChecked=False, boxText=None, boxIcon=None, parent=None):
        CustomButtonCard.__init__(self, icon, title, content, parent, CheckBox)
        self.setButtonText(boxText).setButtonIcon(QIcon(boxIcon))
        self.setButtonChecked(isChecked)

    def setButtonChecked(self, isChecked=False):
        self.button.setChecked(isChecked)


# 超链接
class HyperLinkCard(CustomButtonCard):
    """链接按钮"""
    def __init__(self, url: str, icon, title, content, btText=None, btIcon=None, parent=None):
        super().__init__(icon, title, content, parent, HyperlinkButton, btText, btIcon)
        self.setButtonText(btText).setButtonIcon(btIcon)
        self.setUrl(url)

    def setUrl(self, url):
        self.button.setUrl(url)


# 下拉框
class ComboBoxCard(CustomComboBoxCard, CustomCard):
    """ 下拉框卡片 """
    def __init__(self, icon, title, content, items, noSelected=False, info=None, parent=None, boxType=ComboBox):
        CustomCard.__init__(self, parent)
        self.noSelected = noSelected
        self.initIcon(icon).initTitle(title).initContent(content).initLayout()
        self.initComboBox(boxType, items).setPlaceholderText(info)

    def initComboBox(self, boxType, items):
        self.comboBox = boxType(self)
        self.comboBox.addItems(items)
        self.comboBox.setFixedWidth(150)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)
        return self

    def setPlaceholderText(self, text: str):
        if self.isNoSelected():
            self.comboBox.setPlaceholderText(text)
            self.comboBox.setCurrentIndex(-1)
        return self

    def isNoSelected(self):
        return self.noSelected


class EditComboBoxCard(ComboBoxCard):
    """ 可编辑下拉框卡片 """
    def __init__(self, icon, title, content, items, noSelected=None, info=None, parent=None):
        super().__init__(icon, title, content, items, noSelected, info, parent, EditableComboBox)


class DropDownCard(CustomDropDownCard, CustomButtonCard):
    """普通下拉按钮卡片"""
    def __init__(
            self, icon, title, content, btText=None, btIcon=None,
            menuTexts=None, menuIcons=None, triggered=None, parent=None, btType=DropDownPushButton
    ):
        CustomButtonCard.__init__(self, icon, title, content, parent, btType)
        self.setButtonIcon(btIcon).setButtonText(btText)
        self.addMenu(menuTexts, menuIcons, triggered)

    def addMenu(self, texts, icons, triggered):
        self.menu = RoundMenu(parent=self.button)
        if texts:
            if icons:
                for icon, text, in zip(icons, texts):
                    self.menu.addAction(Action(
                        icon, text, triggered=triggered[texts.index(text)] if triggered else None
                    ))
            else:
                for text in texts:
                    self.menu.addAction(Action(
                        text, triggered=triggered[text.index(text)] if triggered else None
                    ))


class PrimaryDropDownCard(DropDownCard):
    """主题色下拉按钮卡片"""
    def __init__(
            self, icon, title, content, btText=None, btIcon=None,
            menuTexts=None, menuIcons=None, triggered=None, parent=None
    ):
        super().__init__(icon, title, content, btText, btIcon, menuTexts, menuIcons, triggered, parent, PrimaryDropDownPushButton)
        self.button.setMenu(self.menu)


class TransparentDropDownCard(DropDownCard):
    """透明下拉按钮卡片"""
    def __init__(
            self, icon, title, content, btText=None, btIcon=None,
            menuTexts=None, menuIcons=None, triggered=None, parent=None
    ):
        super().__init__(icon, title, content, btText, btIcon, menuTexts, menuIcons, triggered, parent, TransparentDropDownPushButton)
        self.button.setMenu(self.menu)


class DropDownToolCard(DropDownCard):
    """下拉工具按钮卡片"""
    def __init__(
            self, icon, title, content, btIcon=None, menuTexts=None, menuIcons=None,
            triggered=None, parent=None, btType=DropDownToolButton
    ):
        super().__init__(icon, title, content, None, btIcon, menuTexts, menuIcons, triggered, parent, btType)
        self.button.setMenu(self.menu)


class PrimaryDropDownToolCard(DropDownToolCard):
    """下拉工具主题色按钮卡片"""
    def __init__(self, icon, title, content, btIcon=None, menuTexts=None, menuIcons=None, triggered=None, parent=None):
        super().__init__(icon, title, content, btIcon, menuTexts, menuIcons, triggered, parent, PrimaryDropDownToolButton)


class TransparentDropDownToolCard(DropDownToolCard):
    """下拉工具透明按钮卡片"""
    def __init__(self, icon, title, content, btIcon=None, menuTexts=None, menuIcons=None, triggered=None, parent=None):
        super().__init__(icon, title, content, btIcon, menuTexts, menuIcons, triggered, parent, TransparentDropDownToolButton)


class SplitCard(DropDownCard):
    """拆分按钮"""
    def __init__(
            self, icon, title, content, btText=None, btIcon=None, menuTexts=None, menuIcons=None,
            triggered=None, parent=None, btType=SplitPushButton
    ):
        super().__init__(icon, title, content, btText, btIcon, menuTexts, menuIcons, triggered, parent, btType)
        self.button.setFlyout(self.menu)

class PrimarySplitCard(SplitCard):
    """主题色拆分按钮"""
    def __init__(
            self, icon, title, content, btText=None, btIcon=None, menuTexts=None,
            menuIcons=None, triggered=None, parent=None
    ):
        super().__init__(icon, title, content, btText, btIcon, menuTexts, menuIcons, triggered, parent, PrimarySplitPushButton)


class SliderCard(SliderCardParent, CustomCard):
    """ 滑动条卡片 """
    def __init__(self, icon, title, content, ranges, defaultValue=0, orientation=Qt.Orientation.Horizontal, parent=None):
        CustomCard.__init__(self, parent=parent)
        self.initIcon(icon).initTitle(title).initContent(content).initLayout()
        self.initSliderLabel(defaultValue).initSlider(ranges, defaultValue, orientation)

    def initSlider(self, ranges, value, orientation=Qt.Orientation.Horizontal):
        self.slider = Slider(orientation, self)
        self.slider.setRange(ranges[0], ranges[1])
        self.slider.setFixedWidth(200)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(
            lambda: self.sliderLabel.setText(str(self.slider.value()))
        )
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignRight)
        return self

    def initSliderLabel(self, value):
        self.sliderLabel = CaptionLabel(str(value), self)
        self.hBoxLayout.addWidget(self.sliderLabel, 0, Qt.AlignmentFlag.AlignRight)
        return self


class ExpandGroupCard(ExpandGroupCard):
    """展开按钮卡片"""
    def __init__(self, icon, title, content, parent=None):
        super().__init__(icon, title, content, parent)

    def addButtonCard(self, title, icon, text, __type=None):
        hLayout = self._initWidget()
        hLayout.addWidget(TitleLabel(title, self))
        button = PushButton(icon, text, self)
        button.setFixedWidth(120)
        hLayout.addStretch(1)
        hLayout.addWidget(button, 0, Qt.AlignmentFlag.AlignRight)

        return button

    def addPrimaryButtonCard(self, title, icon, text):
        return self.addButtonCard(title, icon, text, PrimaryPushButton)

    def addTransparentButtonCard(self, title, icon, text):
        return self.addButtonCard(title, icon, text, TransparentPushButton)

    def addSliderCard(self, title, ranges, defaultValue, orientation=Qt.Orientation.Horizontal):
        slider = Slider(orientation, self)
        slider.setRange(ranges[0], ranges[1])
        slider.setValue(defaultValue)
        slider.setFixedWidth(250)
        label = CaptionLabel(str(slider.value()), self)

        hLayout = self._initWidget()
        hLayout.addWidget(label)
        hLayout.addStretch(1)
        hLayout.addWidget(label, 0, Qt.AlignmentFlag.AlignRight)
        hLayout.addWidget(slider, 0, Qt.AlignmentFlag.AlignRight)

        slider.valueChanged.connect(
            lambda: label.setText(str(slider.value()))
        )

        return slider

    def setAllCardHeight(self):
        pass
