import os
import pprint
from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.file import TrackedFile,GenericRunAction
 
class AbstractRVOption(GenericRunAction):
    """
    Abstract run action which instantiate an RV runner,
    with its default version.
    """
    def runner_name_and_tags(self):
        return 'RV', []
    
    def get_version(self, button):
        return None

class CompareWithAnimsplineAction(AbstractRVOption):

    _MANAGER_TYPE = _Manager

    ICON = ('icons.libreflow', 'compare-previews')

    _file = flow.Parent()
    _task = flow.Parent(3)
    _shot = flow.Parent(5)

    _animspline_path = flow.SessionParam('').ui(hidden=True)

    @classmethod
    def supported_extensions(cls):
        return ["mp4","mov"]

    def allow_context(self, context):
        self._animspline_path.revert_to_default()
        # file_name = self._animspline_path.get().split('/')[1] if self._animspline_path.get() != '' else ''
        return (
            context 
            and self._task.name() == 'comp'
            and self._file.format.get() in self.supported_extensions()
        )

    def needs_dialog(self):
        self._animspline_path.set(self._get_animspline_path())
        # if self._animspline_path.get() != '':
        #     task_name, file_name = self._animspline_path.get().split('/')
        #     self._animspline_path.set(
        #         self._get_last_revision_path(task_name, file_name)
        #     )

        return (self._animspline_path.get() == '')
    
    def get_buttons(self):
        if self._animspline_path.get() == '':
            self.message.set(
                '''
                <h2>Animspline movie not found.</h2>\n
                '''
            )
        
        return ['Close']
    
    def extra_argv(self):
        return [
            '-wipe', '-autoRetime', '0',
            '[', '-rs', '1', self._file.get_head_revision().get_path(), ']',
            '[', '-volume', '0', '-rs', '1', self._animspline_path.get(), ']'
        ]

    def run(self, button):
        if button == 'Close':
            return
        
        return super(CompareWithAnimsplineAction, self).run(button)

    def _get_animspline_path(self):
        path = ''

        if self._shot.tasks.has_mapped_name('animspline'):
            task = self._shot.tasks['animspline']
            file_list = task.get_files(file_type='Outputs')

            if len(file_list) >= 1 :
                file = file_list[-1]

                r = file.get_head_revision()

                if r is not None and r.get_sync_status() == 'Available':
                    path = r.get_path()

        return path


def compare_with_animspline(parent):
    if isinstance(parent, (TrackedFile)):
        r = flow.Child(CompareWithAnimsplineAction)
        r.name = 'compare_with_animspline'
        r.index = None
        return r


def install_extensions(session):
    return {
        "compare_with_animspline": [
            compare_with_animspline,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
