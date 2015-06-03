"""Video player for DailyMotion."""

import os
import pkg_resources

from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from xblockutils.studio_editable import StudioEditableXBlockMixin


class DailyMotionXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Provides a player for videos hosted on DailyMotion.
    """
    video_url = String(display_name="Video URL",
                      help="DailyMotion Video URL, of the form "
                            "'http://www.dailymotion.com/video/x2e4j6u' or "
                            "'http://dai.ly/x2e4j6u'",
                      scope=Scope.content,
                      default='http://dai.ly/x2e4j6u')

    editable_fields = ('video_url',)

    @property
    def video_id(self):
        return os.path.basename(self.video_url.strip("/"))

    def student_view(self, context=None):
        """
        Show the video to students when viewing courses.
        """
        fragment = self.get_content()
        fragment.initialize_js("InitializeDmotionXblockStudent")
        return fragment

    def get_content(self):
        return self.add_content(Fragment())

    def add_content(self, fragment):
        template_content = self.resource_string("templates/video.html")
        template = Template(template_content)
        content = template.render(Context({"self": self}))

        fragment.add_content(content)
        # Note that this requires us to load the dailymotion sdk for every xblock
        fragment.add_javascript(self.resource_string("public/js/dailymotion-sdk.js"))
        fragment.add_javascript(self.resource_string("public/js/dmotion-xblock.js"))
        fragment.initialize_js("InitializeDmotionXblockStudent")
        return fragment

    def resource_string(self, path):
        """
        Handy helper for getting resources from our kit.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def workbench_scenarios():
        """
        A canned scenario for display in the workbench.
        """
        return [
            ("DailyMotionXBlock",
             """<vertical_demo>
                <dmotion/>
                <dmotion/>
                <dmotion/>
                </vertical_demo>
             """),
        ]
