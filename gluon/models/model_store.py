"""
    Model store which provides pretrained models.
"""

__all__ = ['get_model_file']

import os
import zipfile
import logging
from mxnet.gluon.utils import download, check_sha1

_model_sha1 = {name: (error, checksum, repo_release_tag) for name, error, checksum, repo_release_tag in [
    ('resnet18', '1008', '4f9f7e8f611a51501a23414fc147a3850b8b307b', 'v0.0.2'),
    ('resnet34', '0792', '5b875f4934da8d83d44afc30d8e91362d3103115', 'v0.0.2'),
    ('resnet50', '0687', '79fae958a0acd7a66d688f6453b2bbbc5fe8b3d3', 'v0.0.2'),
    ('resnet50b', '0644', '27a36c02aed870c0c455774f7fb853223f83abc8', 'v0.0.2'),
    ('resnet101', '0599', 'a6d3a5f4933794d56b61867c050ee730f6310f1b', 'v0.0.2'),
    ('resnet101b', '0560', '6517274e7aacd6b05b50da78cb1bf6b9ef85ab57', 'v0.0.2'),
    ('resnet152', '0561', 'd05971c8f10d991ffdbf10318e58f27c2d3471ef', 'v0.0.2'),
    ('resnet152b', '0537', '4f5bd8799404acd1e9e9c857c83877bdb43e299c', 'v0.0.2'),
    ('preresnet18', '1029', '26f46f0b935779826c35d11b7f232ba4bc82a38d', 'v0.0.2'),
    ('preresnet34', '0811', 'f8fe98a25337d747b8687ffdbd1c83ce0d9b9a34', 'v0.0.2'),
    ('preresnet50', '1829', '2fcfddb13fbb8d7f58fb949f137610bf3d99a892', 'v0.0.2'),
    ('preresnet50b', '0664', '2fcfddb13fbb8d7f58fb949f137610bf3d99a892', 'v0.0.2'),
    ('preresnet101', '1746', '1015145a6228aa16583a975b9c33f879ee2a6fc0', 'v0.0.2'),
    ('preresnet101b', '0588', '1015145a6228aa16583a975b9c33f879ee2a6fc0', 'v0.0.2'),
    ('preresnet152', '1451', 'dc303191ea47ca258f5abadd203b5de24d059d1a', 'v0.0.2'),
    ('preresnet152b', '0575', 'dc303191ea47ca258f5abadd203b5de24d059d1a', 'v0.0.2')]}

imgclsmob_repo_url = 'https://github.com/osmr/tmp1'


def get_model_name_suffix_data(model_name):
    if model_name not in _model_sha1:
        raise ValueError('Pretrained model for {name} is not available.'.format(name=model_name))
    error, sha1_hash, repo_release_tag = _model_sha1[model_name]
    return error, sha1_hash, repo_release_tag


def get_model_file(model_name,
                   local_model_store_dir_path=os.path.join('~', '.mxnet', 'models')):
    """
    Return location for the pretrained on local file system. This function will download from online model zoo when
    model cannot be found or has mismatch. The root directory will be created if it doesn't exist.

    Parameters
    ----------
    model_name : str
        Name of the model.
    local_model_store_dir_path : str, default $MXNET_HOME/models
        Location for keeping the model parameters.

    Returns
    -------
    file_path
        Path to the requested pretrained model file.
    """
    error, sha1_hash, repo_release_tag = get_model_name_suffix_data(model_name)
    short_sha1 = sha1_hash[:8]
    file_name = '{name}-{error}-{short_sha1}.params'.format(
        name=model_name,
        error=error,
        short_sha1=short_sha1)
    local_model_store_dir_path = os.path.expanduser(local_model_store_dir_path)
    file_path = os.path.join(local_model_store_dir_path, file_name)
    if os.path.exists(file_path):
        if check_sha1(file_path, sha1_hash):
            return file_path
        else:
            logging.warning('Mismatch in the content of model file detected. Downloading again.')
    else:
        logging.info('Model file not found. Downloading to {}.'.format(file_path))

    if not os.path.exists(local_model_store_dir_path):
        os.makedirs(local_model_store_dir_path)

    zip_file_path = file_path + '.zip'
    download(
        url='{repo_url}/releases/download/{repo_release_tag}/{file_name}.zip'.format(
            repo_url=imgclsmob_repo_url,
            repo_release_tag=repo_release_tag,
            file_name=file_name),
        path=zip_file_path,
        overwrite=True)
    with zipfile.ZipFile(zip_file_path) as zf:
        zf.extractall(local_model_store_dir_path)
    os.remove(zip_file_path)

    if check_sha1(file_path, sha1_hash):
        return file_path
    else:
        raise ValueError('Downloaded file has different hash. Please try again.')
