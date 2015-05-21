"""Video player for DaliMotion."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from xblockutils.studio_editable import StudioEditableXBlockMixin


class DailyMotionXBlock(StudioEditableXBlockMixin, XBlock):
    """
    Provides a player for videos hosted on DailyMotion.
    """
    video_id = String(display_name="Video ID", help="DailyMotion Video ID",
        scope=Scope.content, default='x2e4j6u')

    editable_fields = ('video_id',)

    def resource_string(self, path):
        """
        Handy helper for getting resources from our kit.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        Shows the videos to students when viewing courses.
        """
        html = self.resource_string("static/html/show.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/dmotion.css"))
        return frag

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
