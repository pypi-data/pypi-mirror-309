import os
import boto3
import botocore

class digitalocean_spaces :

    session = None
    client  = None
    SPACES_BUCKET_NAME = None

    def __init__(self):
        # 環境変数を取得
        SPACES_ACCESS_KEY  = os.getenv('SPACES_ACCESS_KEY')
        SPACES_SECRET_KEY  = os.getenv('SPACES_SECRET_KEY')
        SPACES_REGION      = os.getenv('SPACES_REGION')
        SPACES_BUCKET_NAME = os.getenv('SPACES_BUCKET_NAME')

        # Boto3セッションの作成
        self.session = boto3.session.Session()
        self.client = self.session.client(
            's3',
            endpoint_url            = f'https://{SPACES_REGION}.digitaloceanspaces.com',
            config                  = botocore.config.Config(s3={'addressing_style': 'virtual'}),
            region_name             = SPACES_REGION,
            aws_access_key_id       = SPACES_ACCESS_KEY,
            aws_secret_access_key   = SPACES_SECRET_KEY
        )
        self.SPACES_BUCKET_NAME = SPACES_BUCKET_NAME
    

    def sendfile_to_spaces(self, targetfile_path:str, targetfld_to:str):
        """
        指定されたファイルをDigitalOcean Spacesにアップロードする関数です。

        Args:
            targetfile_path (str): アップロードするファイルのパス。このファイルがSpacesにアップロードされます。
            targetfld_to (str): アップロード先のSpaces内のフォルダパス。このパスにファイルが保存されます。
                                ルートフォルダに保存する場合は、空白にしてください。（"."ではなく）

        """

        # ファイルをS3バケットにアップロード
        targetfile_to = os.path.join(targetfld_to, os.path.basename(targetfile_path))
        targetfile_to = targetfile_to.replace('\\', '/')
        with open(targetfile_path, 'rb') as data:
            self.client.put_object(
                Bucket   = self.SPACES_BUCKET_NAME,
                Key      = targetfile_to,
                Body     = data,
                ACL      = 'private',
                Metadata = {'x-amz-meta-my-key': 'your-value'}
            )


    def download_from_spaces(self, targetfile_fullpath:str, targetfld_to:str):
        """
        DigitalOcean Spacesから指定されたファイルをダウンロードする関数です。

        Args:
            targetfile_fullpath (str): ダウンロードするファイルのSpaces内での完全なパス。区切りは「/」で書いてください。
            targetfld_to (str): ダウンロードしたファイルを保存するローカルフォルダ名。
                                このパスにファイルが保存されます。
        """
        # ファイルをS3バケットからダウンロード
        fn = os.path.basename(targetfile_fullpath)
        self.client.download_file(self.SPACES_BUCKET_NAME, targetfile_fullpath.replace('\\', '/'), os.path.join(targetfld_to, fn))



    def list_files_and_folders(self, folder_name:str) -> dict:
        """
        指定されたフォルダ内のファイルとサブフォルダの一覧を取得する関数です。

        Args:
            folder_name (str): 一覧を取得したいフォルダの名前。このフォルダ内のファイルとサブフォルダがリストされます。
                               フォルダ名の末尾にスラッシュがない場合は自動的に追加されます。

        Returns:
            dict: 'file' キーにはフォルダ内のファイルのリストが、'folder' キーにはサブフォルダのリストが含まれます。
        """

        prefix = folder_name + ('/' if folder_name[-1:] != '/' else  '')
        contents = {'file': [], 'folder': []}
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.SPACES_BUCKET_NAME, Prefix=prefix, Delimiter='/'):
            # ファイルを追加
            for obj in page.get('Contents', []):
                key = obj['Key']
                if key != prefix:  # プレフィックス自体は除外
                    contents['file'].append(key[len(prefix):])

            # フォルダを追加
            for prefix_info in page.get('CommonPrefixes', []):
                folder_name = prefix_info['Prefix'][len(prefix):-1]  # 末尾のスラッシュを除去
                contents['folder'].append(folder_name)

        return contents





# サンプルコード
if __name__ == '__main__':

    spaces = digitalocean_spaces()

    # #ファイルのアップロード
    # spaces.sendfile_to_spaces('requirements.txt', 'test/test2')
    # #ファイルのダウンロード
    # spaces.download_from_spaces('test/requirements.txt', 'test')


    # # フォルダ内のファイル・フォルダ一覧を取得
    # def getfiles_from_spaces(folder_name):
    #     # フォルダ内のファイル・フォルダ一覧を取得
    #     contents = spaces.list_files_and_folders(folder_name)

    #     print(f'[ {folder_name} ]')
    #     print('---ファイル一覧---')
    #     for file_key in contents['file']:
    #         print(file_key)
    #     print('---フォルダ一覧---')
    #     for folder_key in contents['folder']:
    #         print(folder_key)

    #     #download all files 
    #     for file_key in contents['file']:
    #         spaces.download_from_spaces(os.path.join(folder_name, file_key), f'digitalocean_spaces/{folder_name}')

    # getfiles_from_spaces('folder1/userdata')
    # getfiles_from_spaces('folder2/userdata')

