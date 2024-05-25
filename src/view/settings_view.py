from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from qfluentwidgets import (ComboBoxSettingCard, FluentIcon, Icon, PushSettingCard, RangeSettingCard, SettingCardGroup,
                            SwitchSettingCard, ToolTipFilter)
from qfluentwidgets.components import (
    ExpandLayout,
    LargeTitleLabel,
    SmoothScrollArea,

    )

from src.config import cfg
from src.view.message_base_view import MessageBaseView


class SettingView(MessageBaseView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout()
        self.smooth_scroll_area = SmoothScrollArea()

        # 这里是一个补丁,因为不知道为什么MessageBaseView没有调用父类的构造函数
        # 所以这里手动初始化一下
        self.is_state_tooltip_running: bool = False

        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        self.setting_title = LargeTitleLabel()
        self.setting_title.setText("设置")

        self._create_card_group()
        self._create_card()
        self._set_up_tooltip()
        self._set_up_layout()
        self._initialize()

    def _create_card_group(self):
        self.video_group = SettingCardGroup("视频", self.scroll_widget)
        self.general_group = SettingCardGroup("通用", self.scroll_widget)

    def _create_card(self):
        # 全局设置
        self.ffmpeg_file_card = PushSettingCard("FFmpeg路径", Icon(FluentIcon.CHEVRON_RIGHT), "设置FFmpeg的路径",
                                                "您可以选择您自己编译的ffmpeg.exe,该软件仅使用了基础的ffmpeg,可能对某些视频格式不支持",
                                                self.general_group)
        self.temp_dir_card = PushSettingCard("临时目录", Icon(FluentIcon.CHEVRON_RIGHT), "设置临时目录",
                                             "软件在运行的过程中会产生过程文件，请确保目标目录有足够的空间",
                                             self.general_group)
        self.delete_temp_dir_card = SwitchSettingCard(Icon(FluentIcon.CHEVRON_RIGHT), "删除临时目录",
                                                      "软件在完成后是否删除临时目录", cfg.delete_temp_dir,
                                                      self.general_group)
        self.preview_video_remove_black_card = SwitchSettingCard(Icon(FluentIcon.CHEVRON_RIGHT), "预览视频去黑边",
                                                                 "最终拼接合成的视频不一定和去黑边一样,拼接的结果是多个帧优化之后的结果,单张图片效果不是很好",
                                                                 cfg.preview_video_remove_black,
                                                                 self.general_group)
        self.preview_frame_card = ComboBoxSettingCard(cfg.preview_frame, Icon(FluentIcon.CHEVRON_RIGHT), "预览视频帧",
                                                        "设置预览视频的封面为第几帧的图片", ["第一帧", "最后一帧", "随机帧"], self.general_group)

        # 视频质量
        self.output_file_path_card = PushSettingCard("输出文件路径", Icon(FluentIcon.CHEVRON_RIGHT), "设置输出文件路径",
                                                     "设置输出文件路径", self.video_group)
        self.noise_reduction_card = SwitchSettingCard(Icon(FluentIcon.CHEVRON_RIGHT), "视频降噪",
                                                      "使用ffmpeg的hqdn3d默认参数对视频进行降噪",
                                                      cfg.noise_reduction, self.video_group)
        self.audio_normalization_card = SwitchSettingCard(Icon(FluentIcon.CHEVRON_RIGHT), "视频音量自动调整",
                                                          "将声音过大或者过小的视频音频自动调整到合适的响度",
                                                          cfg.audio_normalization, self.video_group)
        self.shake_card = SwitchSettingCard(Icon(FluentIcon.CHEVRON_RIGHT), "视频去抖动",
                                            "如果视频本身视角转动过快会导致画面大幅无规律异常抖动,请谨慎使用",
                                            cfg.shake, self.video_group)
        self.video_fps_card = RangeSettingCard(cfg.video_fps, Icon(FluentIcon.CHEVRON_RIGHT), "输出视频帧率",
                                               "调整输出视频的帧率,默认为30fps", self.video_group)
        self.video_sample_rate_card = RangeSettingCard(cfg.video_sample_rate, Icon(FluentIcon.CHEVRON_RIGHT),
                                                       "去黑边采样率",
                                                       "视频黑边的采样率,默认为5", self.video_group)
        self.scaling_quality_card = ComboBoxSettingCard(cfg.scaling_quality, Icon(FluentIcon.CHEVRON_RIGHT), "分辨率缩放算法",
                                                        "调整视频分辨率的时候使用的算法",
                                                        ["速度最快,效果最差", "速度中等,效果中等", "速度最慢,效果最好"],
                                                        self.video_group)
        self.rate_adjustment_type_card = ComboBoxSettingCard(cfg.rate_adjustment_type, Icon(FluentIcon.CHEVRON_RIGHT),
                                                             "视频补帧算法",
                                                             "调整视频帧率的算法",
                                                             ["普通补帧", "光流法补帧(效果好速度慢)"],
                                                             self.video_group)
        self.output_codec_card = ComboBoxSettingCard(cfg.output_codec, Icon(FluentIcon.CHEVRON_RIGHT), "输出视频编码",
                                                     "调整视频编码的算法",
                                                     ["H264", "H264Intel", "H264AMD", "H264Nvidia",
                                                             "H265", "H265Intel", "H265AMD", "H265Nvidia"],
                                                     self.video_group)

    def _set_up_tooltip(self):
        
        ...

    def _set_up_layout(self):
        """设置布局"""
        self.smooth_scroll_area.setWidget(self.scroll_widget)

        self.expand_layout.addWidget(self.general_group)
        self.expand_layout.addWidget(self.video_group)
        self.scroll_widget.setLayout(self.expand_layout)
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(60, 10, 60, 0)

        # 给卡片组添加卡片
        self.general_group.addSettingCards([
                self.ffmpeg_file_card,
                self.temp_dir_card,
                self.delete_temp_dir_card,
                self.preview_video_remove_black_card,
                self.preview_frame_card
                ])
        self.video_group.addSettingCards([
                self.output_file_path_card,
                self.noise_reduction_card,
                self.audio_normalization_card,
                self.shake_card,
                self.video_fps_card,
                self.video_sample_rate_card,
                self.scaling_quality_card,
                self.rate_adjustment_type_card,
                self.output_codec_card,
                ])

    def _initialize(self) -> None:
        """初始化窗体"""
        self.setWindowTitle("设置")
        self.setObjectName("setting_view")
        self.resize(1100, 800)
        self.smooth_scroll_area.setWidgetResizable(True)
        self.smooth_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.setting_title.setMargin(30)
        self.setting_title.setFixedWidth(200)

        self.main_layout.addWidget(self.setting_title)
        self.main_layout.addWidget(self.smooth_scroll_area)
        self.setLayout(self.main_layout)

        # 这里因为背景色不一样,我手动打个补丁
        self.setStyleSheet("background-color: #fcfcfc")
        self.smooth_scroll_area.setStyleSheet("background-color: #fcfcfc")

        for each in self.findChildren(QWidget):
            each.installEventFilter(ToolTipFilter(each, 200))


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication()
    s = SettingView()
    s.show()
    app.exec()