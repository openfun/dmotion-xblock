"""Video player for DaliMotion."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


class DailyMotionXBlock(XBlock):
    """
    Provides a player for videos hosted on DailyMotion.
    """
    video_id = String(help="Video ID", default=None, scope=Scope.content)

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

    def studio_view(self, context):
        """
        Displays the edit view in the Studio.
        """
        html = self.resource_string("static/html/edit.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/dmotion.css"))
        frag.add_javascript(self.resource_string("static/js/src/dmotion.js"))
        frag.initialize_js('DailyMotionXBlockStudio')
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.video_id = data.get('video_id')
        return {'result': 'success'}


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
