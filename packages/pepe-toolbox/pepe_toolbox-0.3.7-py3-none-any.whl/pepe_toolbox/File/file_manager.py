from typing import Callable
import os
import zipfile
import shutil
from typing import Optional, Set
from pkg_resources import FileMetadata
from tqdm import tqdm

from image_converter import ImageConverter


class FileManager:

    @staticmethod
    def remove_empty_dirs(path: str) -> None:
        """
        주어진 경로에서 빈 디렉토리를 재귀적으로 제거합니다.
        Recursively remove empty directories from the given path.

        Args:
            path (str): 검사할 디렉토리 경로 / Path to the directory to check
        """
        # 디렉토리 내의 모든 항목을 검사
        for root, dirs, files in os.walk(path, topdown=False):
            # 파일이 없고, 하위 디렉토리도 모두 비어있는 경우
            if not files and not dirs:
                os.rmdir(root)
                print(f"빈 디렉토리가 제거되었습니다: {root} / Empty directory removed: {root}")

    @staticmethod
    def extract_zip(zip_path: str, extract_to: Optional[str] = None, delete_original: bool = False) -> None:
        """
        단일 ZIP 파일을 해제하는 함수입니다.
        Function to extract a single ZIP file.

        Args:
            zip_path (str): 압축 파일의 경로 / Path to the ZIP file
            extract_to (Optional[str]): 압축 해제할 디렉토리 경로. 기본값은 None으로, ZIP 파일이 있는 폴더에 추출합니다.
                                        Path to extract the contents. If None, extracts to a folder with the same name as the ZIP file.
            delete_original (bool): 압축 해제 후 원본 파일 삭제 여부. 기본값은 False입니다.
                                    Whether to delete the original file after extraction. Defaults to False.

        Raises:
            zipfile.BadZipFile: 잘못된 ZIP 파일일 경우 / If the ZIP file is invalid
            FileNotFoundError: ZIP 파일을 찾을 수 없는 경우 / If the ZIP file is not found
        """
        try:
            if extract_to is None:
                # ZIP 파일 이름과 같은 이름의 폴더 생성
                zip_name = os.path.splitext(os.path.basename(zip_path))[0]
                extract_to = os.path.join(os.path.dirname(zip_path), zip_name)

            # 같은 이름의 폴더가 있으면 삭제
            if os.path.exists(extract_to):
                shutil.rmtree(extract_to)

            # 폴더 생성
            os.makedirs(extract_to)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # tqdm을 사용하여 진행 상황을 표시합니다.
                for file in tqdm(zip_ref.namelist(), desc=f"Extracting {zip_path}"):
                    zip_ref.extract(file, extract_to)

            if delete_original:
                os.remove(zip_path)
                print(f"원본 파일이 삭제되었습니다: {zip_path} / Original file deleted: {zip_path}")
        except zipfile.BadZipFile:
            print(f"잘못된 ZIP 파일입니다: {zip_path} / Invalid ZIP file: {zip_path}")
        except FileNotFoundError:
            print(f"ZIP 파일을 찾을 수 없습니다: {zip_path} / ZIP file not found: {zip_path}")

    @staticmethod
    def extract_all(path: str, delete_original: bool = False, remove_empty_dirs: bool = False, processed: Optional[Set[str]] = None) -> None:
        """
        폴더 내의 모든 ZIP 파일을 전부 압축 해제하는 함수입니다.
        Function to recursively extract all ZIP files in a folder.

        Args:
            path (str): 처리할 폴더 또는 ZIP 파일의 경로 / Path to the folder or ZIP file to process
            delete_original (bool): 압축 해제 후 원본 파일 삭제 여부. 기본값은 False입니다.
                                    Whether to delete the original files after extraction. Defaults to False.
            processed (Set[str]): 이미 처리된 파일 경로를 저장하는 집합 / Set to track processed file paths
        """
        if processed is None:
            processed = set()

        if path in processed:
            return

        processed.add(path)

        if os.path.isfile(path) and path.lower().endswith(".zip"):
            # ZIP 파일인 경우 압축 해제
            FileManager.extract_zip(path, delete_original=delete_original)
            # 압축 해제된 폴더 내의 모든 항목을 재귀적으로 처리
            extract_to = os.path.splitext(path)[0]
            FileManager.extract_all(extract_to, delete_original,
                                remove_empty_dirs, processed)
        elif os.path.isdir(path):
            # 디렉토리 내의 모든 항목을 처리
            for item in tqdm(os.listdir(path), desc=f"Processing directory {path}"):
                item_path = os.path.join(path, item)
                if item_path not in processed:
                    FileManager.extract_all(
                        item_path, delete_original, remove_empty_dirs, processed)
            if remove_empty_dirs:
                FileManager.remove_empty_dirs(path)

    @staticmethod
    def process_directory(path: str, job: Callable[[str], None], file_type: str) -> None:
        """
        주어진 경로를 재귀적으로 탐색하여 파일을 마주했을 때 job을 수행합니다.
        Recursively traverse the given path and perform the specified job on each file encountered.

        Args:
            path (str): 탐색할 디렉토리 경로 / Path to the directory to traverse
            job (Callable[[str], None]): 파일에 대해 수행할 작업 함수 / Function to perform on each file
        """
        for root, dirs, files in os.walk(path):
            print(f"현재 작업 중인 디렉토리: {root}")
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(file_type):
                    job(file_path)


if __name__ == "__main__":
    example_path = "/Users/kinest1997/Downloads/아폴로"
    FileManager.extract_all(example_path, True, remove_empty_dirs=True)
    FileManager.process_directory(example_path, ImageConverter.convert_image(keep_original=False), ".pdf")
