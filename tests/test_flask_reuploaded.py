"""
:copyright: 2010 Matthew "LeafStorm" Frazier
:copyright: 2019-2020 Jürgen Gmach <juergen.gmach@googlemail.com>
:license:   MIT/X11, see LICENSE for details
"""

import os
import os.path
from typing import Dict
from typing import List
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from flask import Flask
from flask import url_for
from flask_uploads import ALL
from flask_uploads import AllExcept
from flask_uploads import TestingFileStorage
from flask_uploads import UploadConfiguration
from flask_uploads import UploadNotAllowed
from flask_uploads import UploadSet
from flask_uploads import addslash
from flask_uploads import config_for_set
from flask_uploads import configure_uploads
from flask_uploads import extension
from flask_uploads import lowercase_ext


class TestMiscellaneous:
    def test_tfs(self) -> None:
        tfs = TestingFileStorage(filename='foo.bar')
        assert tfs.filename == 'foo.bar'
        assert tfs.name is None
        assert tfs.saved is None
        tfs.save('foo_bar.txt')
        assert tfs.saved == 'foo_bar.txt'

    def test_extension(self) -> None:
        assert extension('foo.txt') == 'txt'
        assert extension('foo') == ''
        assert extension('archive.tar.gz') == 'gz'
        assert extension('audio.m4a') == 'm4a'

    def test_lowercase_ext(self) -> None:
        assert lowercase_ext('foo.txt') == 'foo.txt'
        assert lowercase_ext('FOO.TXT') == 'FOO.txt'
        assert lowercase_ext('foo') == 'foo'
        assert lowercase_ext('FOO') == 'FOO'
        assert lowercase_ext('archive.tar.gz') == 'archive.tar.gz'
        assert lowercase_ext('ARCHIVE.TAR.GZ') == 'ARCHIVE.TAR.gz'
        assert lowercase_ext('audio.m4a') == 'audio.m4a'
        assert lowercase_ext('AUDIO.M4A') == 'AUDIO.m4a'

    def test_addslash(self) -> None:
        assert (addslash('http://localhost:4000') ==
                'http://localhost:4000/')
        assert (addslash('http://localhost/uploads') ==
                'http://localhost/uploads/')
        assert (addslash('http://localhost:4000/') ==
                'http://localhost:4000/')
        assert (addslash('http://localhost/uploads/') ==
                'http://localhost/uploads/')

    def test_custom_iterables(self) -> None:
        assert 'txt' in ALL
        assert 'exe' in ALL
        ax = AllExcept(['exe'])
        assert 'txt' in ax
        assert 'exe' not in ax


Config = UploadConfiguration


class TestConfiguration:
    def setup_method(self) -> None:
        self.app = Flask(__name__)

    def teardown_method(self) -> None:
        del self.app

    def configure(
        self, *sets: 'UploadSet', **options: str
    ) -> Dict[str, UploadConfiguration]:
        self.app.config.update(options)
        configure_uploads(self.app, sets)
        return self.app.upload_set_config  # type: ignore

    def test_compare_upload_configurations(self) -> None:
        """UploadConfigurations are only comparable to UploadConfigurations"""
        rv = Config("/var/files", "http://localhost").__eq__("abc")
        assert rv is NotImplemented

    def test_manual(self) -> None:
        f, p = UploadSet('files'), UploadSet('photos')
        setconfig = self.configure(
            f, p,
            UPLOADED_FILES_DEST='/var/files',
            UPLOADED_FILES_URL='http://localhost:6001/',
            UPLOADED_PHOTOS_DEST='/mnt/photos',
            UPLOADED_PHOTOS_URL='http://localhost:6002/'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config('/var/files', 'http://localhost:6001/')
        assert photo_conf == Config('/mnt/photos', 'http://localhost:6002/')

    def test_selfserve(self) -> None:
        f, p = UploadSet('files'), UploadSet('photos')
        setconfig = self.configure(
            f, p,
            UPLOADED_FILES_DEST='/var/files',
            UPLOADED_PHOTOS_DEST='/mnt/photos'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config('/var/files', None)
        assert photo_conf == Config('/mnt/photos', None)

    def test_defaults(self) -> None:
        f, p = UploadSet('files'), UploadSet('photos')
        setconfig = self.configure(
            f, p,
            UPLOADS_DEFAULT_DEST='/var/uploads',
            UPLOADS_DEFAULT_URL='http://localhost:6000/'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config(
            '/var/uploads/files', 'http://localhost:6000/files/')
        assert photo_conf == Config(
            '/var/uploads/photos', 'http://localhost:6000/photos/')

    def test_default_selfserve(self) -> None:
        f, p = UploadSet('files'), UploadSet('photos')
        setconfig = self.configure(
            f, p,
            UPLOADS_DEFAULT_DEST='/var/uploads'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config('/var/uploads/files', None)
        assert photo_conf == Config('/var/uploads/photos', None)

    def test_mixed_defaults(self) -> None:
        f, p = UploadSet('files'), UploadSet('photos')
        setconfig = self.configure(
            f, p,
            UPLOADS_DEFAULT_DEST='/var/uploads',
            UPLOADS_DEFAULT_URL='http://localhost:6001/',
            UPLOADED_PHOTOS_DEST='/mnt/photos',
            UPLOADED_PHOTOS_URL='http://localhost:6002/'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config(
            '/var/uploads/files', 'http://localhost:6001/files/')
        assert photo_conf == Config('/mnt/photos', 'http://localhost:6002/')

    def test_default_destination_callable(self) -> None:
        f = UploadSet('files', default_dest=lambda app: os.path.join(
            app.config['INSTANCE'], 'files'
        ))
        p = UploadSet('photos')
        setconfig = self.configure(
            f, p,
            INSTANCE='/home/me/webapps/thisapp',
            UPLOADED_PHOTOS_DEST='/mnt/photos',
            UPLOADED_PHOTOS_URL='http://localhost:6002/'
        )
        file_conf, photo_conf = setconfig['files'], setconfig['photos']
        assert file_conf == Config('/home/me/webapps/thisapp/files', None)
        assert photo_conf == Config('/mnt/photos', 'http://localhost:6002/')


class TestPreconditions:
    def test_filenames(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        namepairs = (
            ('foo.txt', True),
            ('boat.jpg', True),
            ('warez.exe', False)
        )
        for name, result in namepairs:
            tfs = TestingFileStorage(filename=name)
            assert uset.file_allowed(tfs, name) is result

    def test_underscores_are_not_allowed_for_names_in_upload_sets(
        self
    ) -> None:
        with pytest.raises(ValueError):
            UploadSet("__not__allowed__")

    def test_default_extensions(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        extpairs = (('txt', True), ('jpg', True), ('exe', False))
        for ext, result in extpairs:
            assert uset.extension_allowed(ext) is result

    def test_app_is_properly_configured(self) -> None:
        """`configure_uploads` needs to be called

        otherwise a RuntimeError gets raised
        """
        app = Flask(__name__)
        files = UploadSet("files", ALL)
        # In order to cause a RuntimeError the application must not be properly
        # configured, that is, the following line must not be executed:
        # configure_uploads(app, files)
        with app.test_request_context(environ_base={'HTTP_NAME': 'value'}):
            with pytest.raises(RuntimeError) as excinfo:
                files.config
        expected = "The application is not properly configured. "
        expected += "Please make sure to use `configure_uploads`."
        assert str(excinfo.value) == expected


@patch("os.makedirs", Mock(return_value=None))
class TestSaving:
    def test_filestorage_requires_name(self) -> None:
        uset = UploadSet('files')
        # no name passed in here
        tfs = TestingFileStorage()
        with pytest.raises(ValueError):
            uset.save(tfs)

    def test_saved(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo.txt')
        res = uset.save(tfs)
        assert res == 'foo.txt'
        assert tfs.saved == '/uploads/foo.txt'

    def test_save_folders(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo.txt')
        res = uset.save(tfs, folder='someguy')
        assert res == 'someguy/foo.txt'
        assert tfs.saved == '/uploads/someguy/foo.txt'

    def test_save_named(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo.txt')
        res = uset.save(tfs, name='file_123.txt')
        assert res == 'file_123.txt'
        assert tfs.saved == '/uploads/file_123.txt'

    def test_save_namedext(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='boat.jpg')
        res = uset.save(tfs, name='photo_123.')
        assert res == 'photo_123.jpg'
        assert tfs.saved == '/uploads/photo_123.jpg'

    def test_folder_namedext(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='boat.jpg')
        res = uset.save(tfs, folder='someguy', name='photo_123.')
        assert res == 'someguy/photo_123.jpg'
        assert tfs.saved == '/uploads/someguy/photo_123.jpg'

    def test_implicit_folder(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='boat.jpg')
        res = uset.save(tfs, name='someguy/photo_123.')
        assert res == 'someguy/photo_123.jpg'
        assert tfs.saved == '/uploads/someguy/photo_123.jpg'

    def test_secured_filename(self) -> None:
        uset = UploadSet('files', ALL)
        uset._config = Config('/uploads')
        tfs1 = TestingFileStorage(filename='/etc/passwd')
        tfs2 = TestingFileStorage(filename='../../my_app.wsgi')
        res1 = uset.save(tfs1)
        assert res1 == 'etc_passwd'
        assert tfs1.saved == '/uploads/etc_passwd'
        res2 = uset.save(tfs2)
        assert res2 == 'my_app.wsgi'
        assert tfs2.saved == '/uploads/my_app.wsgi'

    def test_storage_is_not_a_werkzeug_datastructure(self) -> None:
        """UploadSet.save needs a valid FileStorage object.

        When something different is passed in, a TypeError gets raised.
        """
        uset = UploadSet('files', ALL)
        uset._config = Config('/uploads')
        non_storage = 'this is no werkzeug.datastructure.FileStorage'

        with pytest.raises(TypeError):
            uset.save(non_storage)  # type: ignore

    def test_file_not_allowed(self) -> None:
        """Raise UploadNotAllowed for not allowed file extensions."""
        uset = UploadSet('files', ('png'))
        uset._config = Config('/uploads')
        testing_filestorage = TestingFileStorage(filename='picture.gif')
        with pytest.raises(UploadNotAllowed):
            uset.save(testing_filestorage)


@patch("os.makedirs", Mock(return_value=None))
class TestConflictResolution:
    def setup_method(self) -> None:
        self.extant_files: List[str] = []
        self.old_exists = os.path.exists
        os.path.exists = self.exists  # type: ignore

    def teardown_method(self) -> None:
        os.path.exists = self.old_exists
        del self.extant_files, self.old_exists

    def extant(self, *files: str) -> None:
        self.extant_files.extend(files)

    def exists(self, file_name: str) -> None:
        return file_name in self.extant_files  # type: ignore

    def test_self(self) -> None:
        assert not os.path.exists('/uploads/foo.txt')
        self.extant('/uploads/foo.txt')
        assert os.path.exists('/uploads/foo.txt')

    def test_conflict(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo.txt')
        self.extant('/uploads/foo.txt')
        res = uset.save(tfs)
        assert res == 'foo_1.txt'

    def test_multi_conflict(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo.txt')
        self.extant('/uploads/foo.txt',
                    *('/uploads/foo_%d.txt' % n for n in range(1, 6)))
        res = uset.save(tfs)
        assert res == 'foo_6.txt'

    def test_conflict_without_extension(self) -> None:
        uset = UploadSet('files', extensions=(''))
        uset._config = Config('/uploads')
        tfs = TestingFileStorage(filename='foo')
        self.extant('/uploads/foo')
        res = uset.save(tfs)
        assert res == 'foo_1'


class TestPathsAndURLs:
    def test_path(self) -> None:
        uset = UploadSet('files')
        uset._config = Config('/uploads')
        assert uset.path('foo.txt') == '/uploads/foo.txt'
        assert uset.path('someguy/foo.txt') == '/uploads/someguy/foo.txt'
        assert (uset.path('foo.txt', folder='someguy') ==
                '/uploads/someguy/foo.txt')
        assert (uset.path('foo/bar.txt', folder='someguy') ==
                '/uploads/someguy/foo/bar.txt')

    def test_url_generated(self) -> None:
        app = Flask(__name__)
        app.config.update(
            UPLOADED_FILES_DEST='/uploads'
        )
        app.config["UPLOADS_AUTOSERVE"] = True
        uset = UploadSet('files')
        configure_uploads(app, uset)
        with app.test_request_context():
            url = uset.url('foo.txt')
            gen = url_for('_uploads.uploaded_file', setname='files',
                          filename='foo.txt', _external=True)
            assert url == gen

    def test_url_based(self) -> None:
        app = Flask(__name__)
        app.config.update(
            UPLOADED_FILES_DEST='/uploads',
            UPLOADED_FILES_URL='http://localhost:5001/'
        )
        uset = UploadSet('files')
        configure_uploads(app, uset)
        with app.test_request_context():
            url = uset.url('foo.txt')
            assert url == 'http://localhost:5001/foo.txt'
        assert '_uploads' not in app.blueprints


def test_configure_for_set_throws_runtimeerror() -> None:
    """when there is no destination for an UploadSet"""
    upload_set = UploadSet("files")
    app = Flask(__name__)
    with pytest.raises(RuntimeError):
        config_for_set(upload_set, app)
