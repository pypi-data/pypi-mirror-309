import os
import gazu
import re
import glob
import time
import pathlib
import tempfile
import json
from kabaret import flow
from kabaret.app import resources
from kabaret.flow_contextual_dict import get_contextual_dict
from libreflow.baseflow import ProjectSettings
from libreflow.baseflow.file import GenericRunAction
from libreflow.baseflow.task import Task
from libreflow.resources.icons import gui as _
from libreflow.resources import file_templates as _
from .build_utils import wrap_python_expr

from . import _version
__version__ = _version.get_versions()['version']



class AssetStatus(flow.values.ChoiceValue):

    CHOICES = ["NotAvailable", "Downloadable", "Available"]


class TaskFileDependency(flow.Object):

    _parent = flow.Parent()
    _shot = flow.Parent(5)

    asset_lib = flow.Computed(store_value=False)
    asset_type = flow.Computed(store_value=False)
    asset_name = flow.Computed(store_value=False)
    asset_number = flow.Computed(store_value=False)
    asset_path = flow.Computed(store_value=False)
    asset_oid = flow.Computed(store_value=False)
    asset_file_oid = flow.Computed(store_value=False)
    asset_revision_oid = flow.Computed(store_value=False)
    available = flow.Computed(store_value=False)

    def compute_child_value(self, child_value):
        asset_data = self._parent.asset_data(self.name())

        if child_value is self.asset_lib:
            child_value.set(asset_data['asset_lib'])
        elif child_value is self.asset_type:
            child_value.set(asset_data['asset_type'])
        elif child_value is self.asset_number and 'asset_number' in asset_data:
            child_value.set(asset_data['asset_number'])
        elif child_value is self.asset_oid:
            if self.name() == "animatic":
                oid = f"{self._shot.oid()}/tasks/animatic"
            else:
                asset_lib = self.asset_lib.get()
                asset_type = self.asset_type.get()
                asset = None
                asset_name = self.name()
                oid = self.root().project().oid() + f"/asset_libs/{asset_lib}/asset_types/{asset_type}/assets/{asset_name}"
                if not self.root().session().cmds.Flow.exists(oid): # ensure asset exists
                    self.root().session().log_warning(f'Scene Builder - undefined asset {oid}')
                    oid = None
            child_value.set(oid)
        elif child_value is self.asset_file_oid:
            asset_lib = self.asset_lib.get()
            asset_type = self.asset_type.get()
            asset_oid = self.asset_oid.get()

            if asset_oid is not None:
                asset = self.root().get_object(asset_oid)
            else:
                child_value.set(None)
                return

            file_name = self._parent.asset_type_file_name(asset_type)
            files = self._parent.files_from_asset_type(asset, asset_type)

            if files is None or not files.has_mapped_name(file_name):
                child_value.set(None)
            else:
                child_value.set(files[file_name].oid())
        elif child_value is self.asset_name:
            oid = self.asset_oid.get()
            if oid is None:
                child_value.set(None)
            else:
                asset = self.root().get_object(oid)
                child_value.set(asset.name())
        elif child_value is self.asset_revision_oid:
            asset_file_oid = self.asset_file_oid.get()

            if asset_file_oid:
                file = self.root().get_object(asset_file_oid)
                rev = file.get_head_revision()

                if rev and rev.exists():
                    child_value.set(rev.oid())
                else:
                    child_value.set(None)
            else:
                child_value.set(None)
        elif child_value is self.asset_path:
            asset_revision_oid = self.asset_revision_oid.get()
            asset_type = self.asset_type.get()

            if not asset_revision_oid:
                child_value.set(None)
            else:
                rev = self.root().get_object(asset_revision_oid)
                if not rev.exists():
                    child_value.set(None)
                else:
                    child_value.set(rev.get_path())
        elif child_value is self.available:
            asset_path = self.asset_path.get()

            if self.asset_revision_oid.get():
                child_value.set("Available")
            elif self.asset_file_oid.get():
                child_value.set("Downloadable")
            else:
                child_value.set("NotAvailable")


class RefreshDependencies(flow.Action):
    ICON = ('icons.gui', 'refresh')
    _map = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._map.refresh()


class TaskFileDependencies(flow.DynamicMap):
    refresh_action = flow.Child(RefreshDependencies).ui(
        label="Refresh")
    _task = flow.Parent(2)
    _shot = flow.Parent(4)
    _sequence = flow.Parent(6)
    _updated = flow.BoolParam(False)

    def __init__(self, parent, name):
        super(TaskFileDependencies, self).__init__(parent, name)
        self._assets_data_time = time.time()
        self._assets_data = None

    def mapped_names(self, page_num=0, page_size=None):
        if not self._assets_data or time.time() - self._assets_data_time > 30.0:
            self._assets_data = self._get_assets_data()
            self._assets_data_time = time.time()

        return list(self._assets_data.keys())

    def get_kitsu_casting(self, casting):
        kitsu_api = self.root().project().kitsu_api()
        kitsu_casting = kitsu_api.get_shot_casting(self._shot.name(), self._sequence.name())
        if kitsu_casting is None:
            return

        # Kitsu assets
        for asset in kitsu_casting:
            asset_name = asset['asset_name']
            asset_type = asset['asset_type_name']
            asset_data = kitsu_api.get_asset_data(asset_name)
            
            asset_lib = None
            if asset_data.get('source_id', None):
                episode_data = gazu.shot.get_episode(asset_data['source_id'])
                asset_lib = episode_data['name']

            casting[asset_name.replace('-', '_')] = dict(
                asset_type=asset_type.lower(),
                asset_number=asset['nb_occurences']
            )

            if asset_lib:
                casting[asset_name.replace('-', '_')].update(
                    dict(asset_lib=asset_lib.lower())
                )


    def get_animatic_casting(self, casting):
        # Animatic
        casting['animatic'] = dict(
            asset_type='animatic',
            asset_lib='',
        )

    def _get_assets_data(self):
        raise NotImplementedError

    def asset_data(self, asset_name):
        return self._assets_data[asset_name]

    @classmethod
    def mapped_type(cls):
        return TaskFileDependency

    def columns(self):
        return ["Name", "Type", "Lib", "Revision"]

    def asset_type_file_name(self, asset_type):
        return {
            "chars": "modeling_blend",
            "animatic": "animatic_mov",
        }[asset_type]

    def files_from_asset_type(self, asset, asset_type):
        if asset_type == 'sets' and asset.tasks.has_mapped_name('design'):
            return asset.tasks['design'].files
        elif asset_type == 'animatic':
            return asset.files
        elif asset_type == 'chars' and asset.tasks.has_mapped_name('modeling'):
            return asset.tasks['modeling'].files
        else:
            return None

    def refresh(self):
        self._assets_data = None
        self.touch()

    def _fill_row_cells(self, row, item):
        row["Name"] = item.name()
        row["Type"] = item.asset_type.get()
        row["Lib"] = item.asset_lib.get()

        rev_oid = item.asset_revision_oid.get()
        rev_name = rev_oid.split("/")[-1] if rev_oid else ""
        row["Revision"] = rev_name

    def _fill_row_style(self, style, item, row):
        icon_by_status = {
            "NotAvailable": ("icons.libreflow", "cross-mark-on-a-black-circle-background-colored"),
            "Downloadable": ("icons.libreflow", "exclamation-sign-colored"),
            "Available": ("icons.libreflow", "checked-symbol-colored"),
        }
        style["icon"] = icon_by_status[item.available.get()]


class BuildBlenderScene(GenericRunAction):
    ICON = ('icons.libreflow', 'blender')

    _task = flow.Parent()
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)

    def runner_name_and_tags(self):
        return 'Blender', []

    def get_run_label(self):
        return "Build scene"

    def get_buttons(self):
        # Make build action behave as base RunAction by default
        return RunAction.get_buttons(self)

    def needs_dialog(self):
        return True

    def extra_env(self):
        return {
            "ROOT_PATH": self.root().project().get_root()
        }

    def target_file_extension(self):
        return 'blend'

    def get_template_path(self, default_file):
        template_oid = default_file.template_file.get()
        if template_oid is None or not self.root().session().cmds.Flow.exists(template_oid): # check file template
            print(f'Scene Builder -  template of {self._task.name()}/{default_file.name()} is undefined -> use default template')
            return None

        template = self.root().get_object(template_oid)
        if template is None: # check file template
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is undefined -> use default template')
            return None

        rev_name = default_file.template_file_revision.get()
        if rev_name == 'Latest': # check template revision
            rev = template.get_head_revision()
        else:
            rev = template.get_revision(rev_name)
        if rev is None or rev.get_sync_status() != 'Available':
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is not available -> use default template')
            return None

        rev_path = rev.get_path()
        if not os.path.exists(rev_path):
            print(f'Scene Builder - template of {self._task.name()}/{default_file.name()} is not available -> use default template')
            return None

        print(f'Scene Builder - custom template found: {self._task.name()}/{default_file.name()} -> {rev_path}')
        return rev_path

    def get_default_file(self, task_name, filename):
        file_mapped_name = filename.replace('.', '_')
        template_path = resources.get("file_templates", "template.blend")
        mng = self.root().project().get_task_manager()
        if not mng.default_tasks.has_mapped_name(task_name): # check default task
            # print(f'Scene Builder - no default task {task_name} -> use default template')
            return None

        dft_task = mng.default_tasks[task_name]
        if not dft_task.files.has_mapped_name(file_mapped_name): # check default file
            # print(f'Scene Builder - default task {task_name} has no default file {filename} -> use default template')
            return None

        dft_file = dft_task.files[file_mapped_name]
        return dft_file

    def get_path_format(self, task_name, filename):
        dft_file = self.get_default_file(task_name, filename)
        if dft_file is None:
            return None

        return dft_file.path_format.get()

    def _ensure_file(self, name, format, path_format,
                     folder=False, to_edit=False,
                     src_path=None, publish_comment="",
                     task=None, file_type=None):
        if task is None:
            task = self._task

        files = task.files
        file_name = "%s_%s" % (name, format)

        if files.has_file(name, format):
            file = files[file_name]
        else:
            file = files.add_file(
                name=name,
                extension=format,
                tracked=True,
                default_path_format=path_format,
            )

        if not to_edit and not src_path:
            return None

        if to_edit:
            revision = file.create_working_copy(source_path=src_path)
        else:
            revision = file.publish(source_path=src_path, comment=publish_comment)

        if file_type is not None:
            file.file_type.set(file_type)

        return revision.get_path()

    def _ensure_folder(self, name, path_format,
                       to_edit=False,
                       src_path=None, publish_comment="",
                       task=None, file_type=None):
        if task is None:
            task = self._task

        files = task.files

        if files.has_folder(name):
            folder = files[name]
        else:
            folder = files.add_folder(
                name=name,
                tracked=True,
                default_path_format=path_format,
            )

        # XXX Could we publish without creating a working copy?
        folder.create_working_copy(path_format=path_format)
        if not to_edit:
            revision = folder.publish(comment=publish_comment)

        if file_type is not None:
            folder.file_type.set(file_type)

        return revision.get_path()

    def _blender_cmd(self, operator, **kwargs):
        '''
        Returns Blender scene builder operator command as a string.

        Operator must be one of the following:
        `setup`, `setup_anim`,
        `add_asset`, `add_set`,
        `add_animatic`, `update_animatic`,
        `add_audio`, `add_board`, (deprecated, use add_animatic instead)
        `update_audio`, `update_board`, (deprecated, use update_animatic instead without args)
        `export_ae`, `setup_render`,
        'create_collections', 'setup_render_layers', 'setup_render_node_tree',
        `cleanup`, `save`.
        '''

        blender_operators = {
            "setup": {'operator_command': "bpy.ops.pipeline.scene_builder_setup",
                      'args': "frame_start={frame_start}, frame_end={frame_end}, resolution_x={resolution_x}, resolution_y={resolution_y}, fps={fps}, create_camera=False"},
            "setup_anim": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_animation",
                           'args': 'alembic_filepath="{alembic_filepath}", assets={assets}, create_ghost={create_ghost}'},

            "add_asset": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_asset',
                          'args': 'filepath="{filepath}", asset_name="{asset_name}", target_collection="{asset_type}"'},
            "add_animatic": {'operator_command': 'bpy.ops.pipeline.scene_builder_add_animatic',
                             'args': 'filepath="{filepath}"'},
            "add_set": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_set',
                        'args': 'directory="{set_dir}", files={set_dicts}'},
            "add_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_audio',
                          'args': 'filepath="{filepath}"'},
            "add_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_import_storyboard',
                          'args': 'filepath="{filepath}", use_corner={use_corner}'},

            "update_animatic": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_animatic',
                                'args': ''},
            "update_audio": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_audio',
                             'args': ''},
            "update_board": {'operator_command': 'bpy.ops.pipeline.scene_builder_update_storyboard',
                             'args': 'filepath="{filepath}"'},

            "export_ae": {'operator_command': 'bpy.ops.pipeline.scene_builder_export_ae',
                          'args': 'filepath="{filepath}"'},

            "setup_render": {'operator_command': "bpy.ops.pipeline.scene_builder_setup_render",
                             'args': 'kitsu_duration={kitsu_duration}'},

            "create_collections": {'operator_command': "bpy.ops.pipeline.setup_render_create_collections",
                                   'args': ''},
            "setup_render_layers": {'operator_command': "bpy.ops.pipeline.setup_render_layers",
                                    'args': ''},
            "setup_render_node_tree": {'operator_command': "bpy.ops.pipeline.setup_render_node_tree",
                                       'args': '"EXEC_DEFAULT", directory="{directory}"'},

            "cleanup": {'operator_command': 'bpy.ops.pipeline.scene_builder_cleanup',
                        'args': ''},
            "save": {'operator_command': 'bpy.ops.wm.save_mainfile',
                     'args': 'filepath="{filepath}", compress=True'},
        }

        op = blender_operators[operator]
        operator_command = op['operator_command']
        args = op['args'].format(**kwargs)
        command = f"if {operator_command}.poll(): {operator_command}({args})\n"
        return command


class LayoutDependencies(TaskFileDependencies):

    def _get_assets_data(self):
        casting = dict()
        self.get_kitsu_casting(casting)
        self.get_animatic_casting(casting)
        return casting


class BuildLayoutScene(BuildBlenderScene):

    dependencies = flow.Child(LayoutDependencies).ui(expanded=True)

    def get_run_label(self):
        return 'Build layout scene'

    def extra_argv(self):
        def to_int(x, default=24):
            '''Try to convert the given value into an integer. If not possible,
            return the given default value. If x is a floating-point value or a
            string representing one, it is truncated towards zero.
            '''
            try:
                return int(float(x))
            except (TypeError, ValueError):
                return default

        # Get scene builder arguments
        frame_start = 101
        frame_end = 101 + self._shot_data["nb_frames"] - 1
        resolution_x = self.root().project().admin.project_settings.width.get()
        resolution_y = self.root().project().admin.project_settings.height.get()
        fps = to_int(self.root().project().admin.project_settings.frame_rate.get()) # get FPS as an int

        assets = self._shot_data["assets_data"]
        sets = self._shot_data["sets_data"]
        animatic_path = self._shot_data.get("animatic_path", None)
        layout_path = self._shot_data["layout_scene_path"] # Mandatory
        template_path = resources.get("file_templates", "template.blend")

        # Build Blender Python expression
        python_expr = "import bpy\n"
        python_expr += self._blender_cmd("setup", frame_start=frame_start, frame_end=frame_end,
                                         resolution_x=resolution_x, resolution_y=resolution_y, fps=fps)
        python_expr += self._blender_cmd("save", filepath=layout_path)

        for name, path, asset_type, asset_number in assets:
            for i in range(asset_number):
                python_expr += self._blender_cmd(
                    "add_asset", filepath=path, asset_name=name, asset_type=asset_type)
        for set_dir, set_dicts in sets:
            python_expr += self._blender_cmd("add_set",
                                             set_dir=set_dir, set_dicts=set_dicts)
        if animatic_path:
            python_expr += self._blender_cmd("add_animatic",
                                             filepath=animatic_path)

        # python_expr += self._blender_cmd("cleanup")
        python_expr += self._blender_cmd("save", filepath=layout_path)

        return [
            "-b", template_path,
            "--addons", "lfs_scene_builder",
            "--python-expr", wrap_python_expr(python_expr)
        ]

    def get_buttons(self):
        msg = "<h2>Build layout shot</h2>"

        for dep in self.dependencies.mapped_items():
            if dep.available.get() in ["Downloadable", "NotAvailable"]:
                msg += (
                    "<h3><font color=#D66700>"
                    "Some dependencies are still missing, either because they do not already exists or need to be downloaded on your site.\n"
                    "You can build the scene anyway, but you will have to manually update it when missing dependencies will be available."
                    "</font></h3>"
                )
                break

        self.message.set(msg)

        return ["Build and edit", "Build and publish", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        if button == "Refresh":
            self.dependencies.touch()
            return self.get_result(refresh=True, close=False)

        shot_name = self._shot.name()
        sequence_name = self._sequence.name()

        # Get shot data
        kitsu_api = self.root().project().kitsu_api()
        shot_data = kitsu_api.get_shot_data(shot_name, sequence_name)

        # Store dependencies file paths for Blender script building
        self._shot_data = {}
        self._shot_data["nb_frames"] = shot_data["nb_frames"]
        if self._shot_data["nb_frames"] is None:
            self._shot_data["nb_frames"] = 0
        self._shot_data["assets_data"] = []
        self._shot_data["sets_data"] = []

        for dep in self.dependencies.mapped_items():
            if dep.available.get() != "Available":
                continue

            asset_type = dep.asset_type.get()
            asset_number = dep.asset_number.get()
            path = dep.asset_path.get().replace("\\", "/")
            path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", path) # check drive name

            if asset_type == "animatic":
                self._shot_data["animatic_path"] = path
            else: # characters/props/animals
                self._shot_data["assets_data"].append((dep.asset_name.get(), path, asset_type, asset_number))

        # Get layout file preset to resolve template and path format
        default_file = self.get_default_file(self._task.name(), "layout.blend")
        path_format = None
        if default_file is not None:
            # self._shot_data["layout_template_path"] = self.get_template_path(default_file)
            path_format = default_file.path_format.get()
        # Configure layout file
        layout_path = self._ensure_file(
            name='layout',
            format='blend',
            path_format=path_format,
            to_edit=(button == 'Build and edit'),
            src_path=resources.get("file_templates", "template.blend"),
            publish_comment="Created with scene builder"
        )

        self._task.touch()

        # Store layout output path
        layout_path = layout_path.replace("\\", "/")
        layout_path = re.sub(r"^//([^/]+)/", r"\\\\\\\\\1\\\\", layout_path) # check drive name
        self._shot_data["layout_scene_path"] = layout_path

        # Build
        super(BuildLayoutScene, self).run(button)



def build_scene_action(parent):
    if isinstance(parent, Task) :
        r = flow.Child(BuildLayoutScene)
        r.name = 'build_scene'
        r.index = None
        return r

def install_extensions(session):
    return {
        "scene_builder": [
            build_scene_action
        ]
    }

